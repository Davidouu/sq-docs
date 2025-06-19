"""build_site.py

A reusable class that takes one module (with its multilingual Markdown
sources) and produces a fully‑built MkDocs site in `site_<module>/`.

Usage example
-------------
from pathlib import Path
from build_site import BuildSite

builder = BuildSite(
    module_name="gestion_attributes",
    source_dir=Path("./docs/modules/gestion_attributes"),
    output_root=Path("./"),
)
builder.run()  # copies docs/, writes mkdocs.yml, builds the site
"""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from typing import List, Dict, Any

import yaml

# ---------------------------------------------------------------------------
# Helper exceptions
# ---------------------------------------------------------------------------
class BuildSiteError(RuntimeError):
    """Base exception raised by BuildSite"""


class MissingFileError(BuildSiteError):
    """Raised when an expected Markdown file is missing."""


class BuildProcessError(BuildSiteError):
    """Raised when `mkdocs build` fails."""


# ---------------------------------------------------------------------------
# BuildSite class
# ---------------------------------------------------------------------------
class BuildSite:
    """Generate a multilingual MkDocs site for a single module.

    Parameters
    ----------
    module_name : str
        Human‑readable slug used for the output directory (e.g. "gestion_attributes").
    source_dir : Path
        Points to the folder that contains one sub‑directory per language
        (`fr/`, `en/`, `es/` …). Each sub‑directory must hold the same Markdown
        file set (index.md, doc_tech.md, …).
    output_root : Path
        Parent folder where the built site will be written as `site_<module_name>/`.
    languages : List[str], optional
        ISO language codes that exist under *source_dir* (default: ["fr", "en", "es"]).
    md_files : List[str], optional
        Basename list of Markdown files expected in every language folder.
    site_url : str | None, optional
        Absolute URL of the documentation hub (used in the nav).
    """

    #: Default list of Markdown files each language must contain
    _DEFAULT_MD_FILES: List[str] = [
        "index.md",
        "doc_tech.md",
        "config_interface.md",
        "trouble_faq.md",
    ]

    def __init__(
        self,
        module_name: str,
        source_dir: Path,
        output_root: Path,
        *,
        languages: List[str] | None = None,
        md_files: List[str] | None = None,
        site_url: str | None = None,
    ) -> None:
        self.module_name = module_name
        self.source_dir = source_dir.expanduser().resolve()
        self.output_root = output_root.expanduser().resolve()
        self.languages = languages or ["fr", "en", "es"]
        self.md_files = md_files or self._DEFAULT_MD_FILES.copy()
        self.site_url = site_url or "http://localhost:81/documentation/"

        self.docs_dir = self.output_root / f"tmp_docs_{module_name}"
        self.mkdocs_file = self.output_root / f"mkdocs_{module_name}.yml"
        self.site_dir = self.output_root / f"site_{module_name}"

    # ---------------------------------------------------------------------
    # Public API
    # ---------------------------------------------------------------------
    def run(self) -> None:
        """High‑level convenience wrapper: copy docs, write mkdocs.yml, build."""
        self._prepare_docs_tree()
        self._write_mkdocs_config()
        self._build_site()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _prepare_docs_tree(self) -> None:
        """Copy multilingual Markdown files into a *docs/* folder as expected by MkDocs.
        The default language ("fr") keeps plain filenames, others get a suffix
        (`filename.en.md`). Existing folder is removed for a fresh build.
        """
        if self.docs_dir.exists():
            shutil.rmtree(self.docs_dir)
        self.docs_dir.mkdir(parents=True, exist_ok=True)

        for lang in self.languages:
            lang_path = self.source_dir / lang
            if not lang_path.is_dir():
                raise MissingFileError(f"Dossier langue manquant: {lang_path}")

            for md_name in self.md_files:
                src = lang_path / md_name
                if not src.is_file():
                    raise MissingFileError(f"Fichier manquant: {src}")

                if lang == "fr":
                    dst = self.docs_dir / md_name
                else:
                    stem = src.stem
                    dst = self.docs_dir / f"{stem}.{lang}{src.suffix}"

                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)

    # --------------------------------------------
    def _write_mkdocs_config(self) -> None:
        nav = self._build_nav()
        cfg: Dict[str, Any] = {
            "site_name": self.module_name.replace("_", " ").title(),
            "theme": {"name": "material"},
            "site_dir": str(self.site_dir),
            "nav": nav,
            "markdown_extensions": [
                "toc",
                "admonition",
                "footnotes",
                "tables",
                {"codehilite": {"guess_lang": False, "linenums": True}},
                {"pymdownx.superfences": {}},
            ],
            "plugins": [
                {
                    "search": {
                        "lang": self.languages,
                        "separator": r"[\s\-]+",
                        "prebuild_index": True,
                        "include_html": True,
                    }
                },
                {
                    "i18n": {
                        "default_language": "fr",
                        "languages": [
                            {"locale": code, "name": code.upper(), "build": True, "default": code == "fr"}
                            for code in self.languages
                        ],
                    }
                },
            ],
        }
        with self.mkdocs_file.open("w", encoding="utf-8") as fh:
            yaml.dump(cfg, fh, sort_keys=False, allow_unicode=True)

    # --------------------------------------------
    def _build_nav(self) -> List[Dict[str, Any]]:
        """Return a FR‑centric nav structure."""
        nav = [
            {"Documentation Hub": self.site_url},
            {"Accueil": "index.md"},
            {
                "Documentation": [
                    {"Overview, Configuration & Interface": "config_interface.md"},
                    {"Documentation Technique": "doc_tech.md"},
                    {"TroubleShooting & FAQ": "trouble_faq.md"},
                ]
            },
        ]
        return nav

    # --------------------------------------------
    def _build_site(self) -> None:
        try:
            subprocess.run(
                ["mkdocs", "build", "-f", str(self.mkdocs_file)],
                check=True,
                capture_output=True,
                text=True,
            )
            print(f"✅ Site '{self.module_name}' généré dans {self.site_dir}")
        except subprocess.CalledProcessError as exc:
            raise BuildProcessError(exc.stderr) from exc

    # ------------------------------------------------------------------
    # Dunder helpers
    # ------------------------------------------------------------------
    def __repr__(self) -> str:  # pragma: no cover
        return f"<BuildSite module={self.module_name} source={self.source_dir}>"
