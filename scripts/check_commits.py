"""check_commits.py – v2

Détecte les fichiers Markdown modifiés sous `docs/modules/**` depuis le dernier
build et reconstruit uniquement les modules concernés en utilisant
`BuildSite` (v2, sans _DEFAULT_MD_FILES).

• Stocke le SHA du dernier build dans `.last_build` (à la racine du dépôt).
• Fait un `git pull --ff-only` pour récupérer les commits poussés par le CMS.
• Exécute toutes les commandes Git dans `repo_root` grâce au paramètre `cwd=`.
"""
from __future__ import annotations

import subprocess
from pathlib import Path
from typing import List, Set

from build_sites import BuildSite, BuildSiteError

__all__ = ["CheckCommits"]


class CheckCommits:
    """Déclenche des builds sélectifs selon les commits Git."""

    def __init__(
        self,
        *,
        repo_root: Path,
        output_root: Path,
        state_file: Path | None = None,
        languages: List[str] | None = None,
    ) -> None:
        self.repo_root = repo_root.expanduser().resolve()
        self.output_root = output_root.expanduser().resolve()
        self.state_file = state_file or self.repo_root / ".last_build"
        self.languages = languages or ["fr", "en", "es"]

    # ------------------------------------------------------------------
    def run(self) -> None:
        """Point d’entrée principal."""
        # 1) Récupère et avance la branche locale
        self._git("pull", "--ff-only", "origin", "master")  # adapte si main

        head_sha = self._git("rev-parse", "HEAD").strip()
        prev_sha = self._read_prev_sha()

        if prev_sha == head_sha:
            print("🔸 Aucune nouvelle modification détectée – build sauté.")
            return

        modules = self._changed_modules(prev_sha, head_sha)
        if not modules:
            print("🔸 Aucun fichier Markdown modifié dans docs/modules – build sauté.")
            self._write_state(head_sha)
            return

        print("🔧 Modules à reconstruire :", ", ".join(sorted(modules)))
        for module in sorted(modules):
            try:
                BuildSite(
                    module_name=module,
                    source_dir=self.repo_root / "docs/modules" / module,
                    output_root=self.output_root,
                    languages=self.languages,
                ).run()
            except BuildSiteError as exc:
                print(f"❌ Erreur build {module}: {exc}")

        # 3) Mémorise la SHA courante
        self._write_state(head_sha)
        print("🏁 Fin de la passe de build sélectif.")

    # ------------------------------------------------------------------
    # Helpers internes
    # ------------------------------------------------------------------
    def _git(self, *args: str) -> str:
        return subprocess.check_output(["git", *args], cwd=self.repo_root, text=True)

    def _read_prev_sha(self) -> str:
        try:
            return self.state_file.read_text().strip()
        except FileNotFoundError:
            return ""

    def _write_state(self, sha: str) -> None:
        self.state_file.write_text(sha)

    def _changed_modules(self, prev_sha: str, head_sha: str) -> Set[str]:
        diff_range = f"{prev_sha}..{head_sha}" if prev_sha else head_sha
        raw = self._git("diff", "--name-only", diff_range, "--", "docs/modules")

        modules: Set[str] = set()
        for path in raw.splitlines():
            if not path.lower().endswith(".md"):
                continue
            parts = Path(path.replace("\\", "/")).parts  # normalise Windows
            # docs / modules / <module> / ...
            if len(parts) >= 3 and parts[0:2] == ("docs", "modules"):
                modules.add(parts[2])
        return modules
