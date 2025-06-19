"""build_site.py – v2

Génère un sous‑site MkDocs multilingue **directement** depuis le dossier
`docs/modules/<module>/` sans recopier les fichiers dans un répertoire
intermédiaire. Le dossier d’origine reste intact ; seul le répertoire
`site_<module>/` est créé (et peut être déployé tel quel).

Hypothèse d’arborescence d’une *feature* :
└─ docs/modules/gestion_attributs/
   ├─ fr/
   │   ├─ index.md
   │   ├─ config_interface.md
   │   └─ ...
   ├─ en/
   │   └─ index.md …
   └─ es/
       └─ index.md …

Usage
-----
from pathlib import Path
from build_site import BuildSite

builder = BuildSite(
    module_name="gestion_attributs",
    source_dir=Path("docs/modules/gestion_attributs"),
    output_root=Path("."),
)
builder.run()
"""
from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Dict, List, Any

import yaml

__all__ = ["BuildSite", "BuildSiteError"]

# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------
class BuildSiteError(RuntimeError):
    """Erreur levée lorsque mkdocs build échoue."""


# ---------------------------------------------------------------------------
# Classe principale
# ---------------------------------------------------------------------------
class BuildSite:
    """Compile un module multilingue MkDocs sans copie intermédiaire.

    Parameters
    ----------
    module_name : str
        Slug du module (dossier dans docs/modules).
    source_dir : Path
        Dossier qui contient les sous‑dossiers `fr/`, `en/`, `es/`…
    output_root : Path
        Répertoire parent où `site_<module>/` sera écrit.
    languages : list[str], optional
        Codes langue à prendre en compte (défaut : ["fr", "en", "es"]).
    site_url : str, optional
        Lien vers la page d’accueil globale (hub) – utilisé dans le *nav*.
    """

    def __init__(
        self,
        *,
        module_name: str,
        source_dir: Path,
        output_root: Path,
        languages: List[str] | None = None,
        site_url: str | None = None,
    ) -> None:
        self.module = module_name
        self.source_dir = source_dir.resolve()
        self.output_root = output_root.resolve()
        self.languages = languages or ["fr", "en", "es"]
        self.site_url = site_url or "http://localhost:81/documentation/"

        self.site_dir = self.output_root / f"site_{self.module}"
        self.mkcfg = self.output_root / f"mk_{self.module}.yml"

    # ------------------------------------------------------------------
    # API publique
    # ------------------------------------------------------------------
    def run(self) -> None:  # noqa: D401
        """Génère le site pour ce module."""
        self._write_mkdocs_yml()
        self._call_mkdocs_build()

    # ------------------------------------------------------------------
    # Écriture du mkdocs.yml
    # ------------------------------------------------------------------
    def _write_mkdocs_yml(self) -> None:
        cfg: Dict[str, Any] = {
            "site_name": self.module.replace("_", " ").title(),
            "docs_dir": str(self.source_dir),
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
            "nav": self._make_nav_fr(),
        }
        with self.mkcfg.open("w", encoding="utf-8") as fh:
            yaml.dump(cfg, fh, allow_unicode=True, sort_keys=False)

    def _make_nav_fr(self) -> List[Dict[str, Any]]:
        """Construit la navigation FR (langue par défaut)."""
        return [
            {"Documentation Hub": self.site_url},
            {"Accueil": "fr/index.md"},
            {
                "Documentation": [
                    {"Overview, Configuration & Interface": "fr/config_interface.md"},
                    {"Documentation Technique": "fr/doc_tech.md"},
                    {"TroubleShooting & FAQ": "fr/trouble_faq.md"},
                ]
            },
        ]

    # ------------------------------------------------------------------
    # Build
    # ------------------------------------------------------------------
    def _call_mkdocs_build(self) -> None:
        try:
            subprocess.run(
                ["mkdocs", "build", "-f", str(self.mkcfg)],
                check=True,
                capture_output=True,
                text=True,
            )
            print(f"✅ {self.module}: site généré dans {self.site_dir}")
        except subprocess.CalledProcessError as exc:
            raise BuildSiteError(exc.stderr) from exc

    # ------------------------------------------------------------------
    def __repr__(self) -> str:  # pragma: no cover
        return f"<BuildSite module={self.module}>"
