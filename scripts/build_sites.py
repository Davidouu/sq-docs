"""build_site.py – v3

Construit un sous‑site MkDocs multilingue **sans rien laisser traîner** :
• crée un répertoire temporaire `.build_<module>/` (hors dépôt) ;
• y copie les fichiers FR à la racine + suffixe `.en.md`, `.es.md`… ;
• écrit un `mkdocs.yml` dans ce même tmp ;
• exécute `mkdocs build` pour produire `site_<module>/` à la racine ;
• nettoie entièrement le dossier temporaire à la fin.

La structure générée dans `site_<module>/` est celle que tu avais avant :
│ 404.html
│ index.html              ← page FR (langue par défaut)
├─ en/
├─ es/
└─ assets/

Le dépôt ne contient donc : **aucun mkdocs.yml** supplémentaire, **aucun
fichier copié**.
"""
from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List, Any

import yaml

__all__ = ["BuildSite", "BuildSiteError"]

# ---------------------------------------------------------------------------
DEFAULT_MD_FILES = [
    "index.md",
    "doc_tech.md",
    "config_interface.md",
    "trouble_faq.md",
]


class BuildSiteError(RuntimeError):
    """Erreur levée lorsque `mkdocs build` échoue."""


class BuildSite:
    """Build MkDocs pour un module sans laisser de fichiers auxiliaires."""

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
    def run(self) -> None:  # noqa: D401
        """Pipeline complet : copy → mkdocs.yml → build → cleanup."""
        with tempfile.TemporaryDirectory(dir=self.output_root) as tmp:
            tmp_path = Path(tmp)
            docs_dir = tmp_path / "docs"
            docs_dir.mkdir(parents=True, exist_ok=True)

            self._copy_markdown(docs_dir)
            mkcfg = tmp_path / "mkdocs.yml"
            self._write_mkdocs_yml(mkcfg, docs_dir)
            self._mkdocs_build(mkcfg)
            print(f"✅ {self.module}: site généré dans {self.site_dir}")
        # tmp dir supprimé automatiquement

    # ------------------------------------------------------------------
    def _copy_markdown(self, docs_dir: Path) -> None:
        """Copie FR à la racine, EN/ES avec suffixes."""
        for lang in self.languages:
            lang_dir = self.source_dir / lang
            if not lang_dir.is_dir():
                raise BuildSiteError(f"Dossier langue manquant : {lang_dir}")
            for md_name in self.md_files:
                src = lang_dir / md_name
                if not src.is_file():
                    raise BuildSiteError(f"Fichier manquant : {src}")
                if lang == "fr":
                    dst = docs_dir / md_name
                else:
                    dst = docs_dir / f"{Path(md_name).stem}.{lang}{Path(md_name).suffix}"
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)

    # ------------------------------------------------------------------
    def _write_mkdocs_yml(self, mkcfg: Path, docs_dir: Path) -> None:
        cfg: Dict[str, Any] = {
            "site_name": self.module.replace("_", " ").title(),
            "docs_dir": str(docs_dir),
            "site_dir": str(self.site_dir),
            "theme": {"name": "material"},
            "plugins": [
                {
                    "search": {
                        "lang": self.languages,
                        "separator": r"[\s\-]+",
                        "prebuild_index": True,
                    }
                },
                {
                    "i18n": {
                        "default_language": "fr",
                        "languages": [
                            {
                                "locale": code,
                                "name": code.upper(),
                                "build": True,
                                "default": code == "fr",
                            }
                            for code in self.languages
                        ],
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
        mkcfg.write_text(yaml.dump(cfg, allow_unicode=True, sort_keys=False), encoding="utf-8")

    # ------------------------------------------------------------------
    def _mkdocs_build(self, mkcfg: Path) -> None:
        try:
            subprocess.run([
                "mkdocs", "build", "-f", str(mkcfg), "--strict"
            ], check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as exc:
            raise BuildSiteError(exc.stderr) from exc
