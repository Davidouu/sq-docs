"""build_site.py – v4

Cette version corrige la configuration des plugins :
* **search** → options autorisées par MkDocs‑Material 9.x (`separator` ≠ supporté).
* **i18n** → syntaxe du plugin *mkdocs‑static‑i18n* (`default_language` → `default_language`, mais `languages` doit être un **mapping** `{code: {name: …}}`).

Aucun fichier persistant ; build strict dans un dossier temp puis sortie dans
`site_<module>/`.
"""
from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List, Any

import yaml

__all__ = ["BuildSite", "BuildSiteError"]

DEFAULT_MD_FILES = [
    "index.md",
    "doc_tech.md",
    "config_interface.md",
    "trouble_faq.md",
]


class BuildSiteError(RuntimeError):
    """Exception propagée si `mkdocs build` échoue."""


class BuildSite:
    """Génère un sous‑site MkDocs multilingue sans résidu."""

    def __init__(
        self,
        *,
        module_name: str,
        source_dir: Path,
        output_root: Path,
        languages: List[str] | None = None,
        md_files: List[str] | None = None,
        site_url: str | None = None,
    ) -> None:
        self.module = module_name
        self.source_dir = source_dir.resolve()
        self.output_root = output_root.resolve()
        self.languages = languages or ["fr", "en", "es"]
        self.md_files = md_files or DEFAULT_MD_FILES
        self.site_url = site_url or "http://localhost:81/documentation/"

        self.site_dir = self.output_root / f"site_{self.module}"

    # ------------------------------------------------------------------
    def run(self) -> None:
        """Copie → mkdocs.yml temp → build → clean."""
        with tempfile.TemporaryDirectory(dir=self.output_root) as tmp:
            tmp_path = Path(tmp)
            docs_dir = tmp_path / "docs"
            docs_dir.mkdir()
            self._copy_markdown(docs_dir)

            mkcfg = tmp_path / "mkdocs.yml"
            mkcfg.write_text(self._mkdocs_config(docs_dir), encoding="utf-8")
            self._mkdocs_build(mkcfg)
            print(f"✅ {self.module}: site généré dans {self.site_dir}")

    # ------------------------------------------------------------------
    def _copy_markdown(self, target: Path) -> None:
        for lang in self.languages:
            lang_path = self.source_dir / lang
            if not lang_path.is_dir():
                raise BuildSiteError(f"Lang folder missing: {lang_path}")
            for fname in self.md_files:
                src = lang_path / fname
                if not src.is_file():
                    raise BuildSiteError(f"File missing: {src}")
                dst = target / (fname if lang == "fr" else f"{Path(fname).stem}.{lang}.md")
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)

    # ------------------------------------------------------------------
    def _mkdocs_config(self, docs_dir: Path) -> str:
        cfg: Dict[str, Any] = {
            "site_name": self.module.replace("_", " ").title(),
            "docs_dir": str(docs_dir),
            "site_dir": str(self.site_dir),
            "theme": {"name": "material"},
            "plugins": [
                "search",  # plugin builtin Material (sans opt avancées)
                {
                    "i18n": {
                        "default_language": "fr",
                        "languages": {
                            code: {"name": code.upper(), "build": True}
                            for code in self.languages
                        },
                    }
                },
            ],
            "markdown_extensions": [
                "toc",
                "admonition",
                "footnotes",
                "tables",
                {"codehilite": {"guess_lang": False, "linenums": True}},
                {"pymdownx.superfences": {}},
            ],
            "nav": [
                {"Documentation Hub": self.site_url},
                {"Accueil": "index.md"},
                {
                    "Documentation": [
                        {"Overview, Configuration & Interface": "config_interface.md"},
                        {"Documentation Technique": "doc_tech.md"},
                        {"TroubleShooting & FAQ": "trouble_faq.md"},
                    ]
                },
            ],
        }
        return yaml.dump(cfg, sort_keys=False, allow_unicode=True)

    # ------------------------------------------------------------------
    @staticmethod
    def _mkdocs_build(mkcfg: Path) -> None:
        try:
            subprocess.run(
                ["mkdocs", "build", "-f", str(mkcfg), "--strict"],
                check=True,
                capture_output=True,
                text=True,
            )
        except subprocess.CalledProcessError as exc:
            raise BuildSiteError(exc.stderr) from exc
