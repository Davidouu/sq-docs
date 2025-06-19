"""check_commits.py

Scan the Git repo for Markdown changes under `docs/modules/**` since the last
successful build and, if any, trigger BuildSite for the affected modules.

Typical usage (cron, systemd‑timer, or manual):
------------------------------------------------
from pathlib import Path
from check_commits import CheckCommits

checker = CheckCommits(
    repo_root=Path(__file__).resolve().parent,  # repo root
    output_root=Path("./"),                    # where site_<module>/ go
)
checker.run()

A hidden file `.last_build` (at the repo root) stores the commit SHA of the
most recent build so the next execution only picks up new work.
"""
from __future__ import annotations

import subprocess
from pathlib import Path
from typing import List, Set

from build_sites import BuildSite, BuildSiteError

__all__ = ["CheckCommits"]


class CheckCommits:
    """Detect modified modules and rebuild them.

    Parameters
    ----------
    repo_root : Path
        The root directory of the Git repository.
    output_root : Path
        Where the `BuildSite` class will output the individual `site_<module>`
        folders and temporary files.
    state_file : Path, optional
        File that stores the last successful build commit SHA. If *None*
        (default) use ``repo_root/''.last_build'``.
    languages : list[str], optional
        List of language codes present in each module (default: ["fr", "en", "es"]).
    md_files : list[str], optional
        Markdown file names expected inside each language directory. Must match
        the list used by your generation process. Defaults to BuildSite._DEFAULT_MD_FILES.
    """

    def __init__(
        self,
        *,
        repo_root: Path,
        output_root: Path,
        state_file: Path | None = None,
        languages: List[str] | None = None,
        md_files: List[str] | None = None,
    ) -> None:
        self.repo_root = repo_root.expanduser().resolve()
        self.output_root = output_root.expanduser().resolve()
        self.state_file = state_file or self.repo_root / ".last_build"
        self.languages = languages or ["fr", "en", "es"]
        self.md_files = md_files or BuildSite._DEFAULT_MD_FILES.copy()

    # ------------------------------------------------------------------
    # High‑level public method
    # ------------------------------------------------------------------
    def run(self) -> None:
        """Main entry point: detect changed modules, rebuild them, update SHA."""
        self._git("fetch", "origin")
        self._git("pull", "--ff-only", "origin", "master")

        head_sha = self._git("rev-parse", "HEAD").strip()
        prev_sha = self._read_prev_sha()

        print(prev_sha, head_sha)

        if prev_sha == head_sha:
            print("🔸 Aucune nouvelle modification détectée – build sauté.")
            return

        modules = self._changed_modules(prev_sha, head_sha)
        if not modules:
            print("🔸 Aucun fichier Markdown modifié dans docs/modules – build sauté.")
            self._write_state(head_sha)
            return

        print("🔧 Modules à reconstruire:", ", ".join(sorted(modules)))
        for module in sorted(modules):
            try:
                builder = BuildSite(
                    module_name=module,
                    source_dir=self.repo_root / "docs/modules" / module,
                    output_root=self.output_root,
                    languages=self.languages,
                    md_files=self.md_files,
                )
                builder.run()
            except BuildSiteError as exc:
                print(f"❌ Erreur build {module}: {exc}")
                # Ne pas interrompre la boucle, construire le reste

        # Tous les builds terminés (ou ignorés) → consigne la SHA courante
        self._write_state(head_sha)
        print("🏁 Fin de la passe de build sélectif.")

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _read_prev_sha(self) -> str:
        try:
            return self.state_file.read_text().strip()
        except FileNotFoundError:
            return ""

    def _write_state(self, sha: str) -> None:
        self.state_file.write_text(sha)

    def _git(self, *args: str) -> str:
        return subprocess.check_output(["git", *args], cwd=self.repo_root, text=True)
    
    def _changed_modules(self, prev_sha: str, head_sha: str) -> set[str]:
        diff_range = f"{prev_sha}..{head_sha}" if prev_sha else head_sha

        # --- DEBUG ----------------------------------------------------------
        print(f"🔎 Diff range = {diff_range}")
        raw = self._git("diff", "--name-only", f"{prev_sha}..{head_sha}", "--", "docs/modules")
        print("🔎 git diff output:")
        print(raw or "   (vide)")
        # -------------------------------------------------------------------

        modules = set()
        for path in raw.splitlines():
            if path.lower().endswith(".md"):
                parts = Path(path.replace('\\', '/')).parts
                if len(parts) >= 3 and parts[0:2] == ("docs", "modules"):
                    modules.add(parts[2])

        print(f"🔎 Modules détectés = {modules or 'aucun'}")
        return modules
