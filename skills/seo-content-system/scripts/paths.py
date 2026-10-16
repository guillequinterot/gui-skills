#!/usr/bin/env python3
"""Resolución de rutas compartida por los scripts de SEO Content System.

Dos modos de memoria, sin que ningún script falle por no tener Obsidian:

* ``vault``: hay una bóveda de Obsidian configurada (opcional). Se usa su carpeta de la skill
  (``06_Aprendizaje/Inbox``, ``02_Investigacion/Novedades``, ``08_Fuentes``...).
* ``repo``: no hay bóveda. Se usa la carpeta ``memoria/`` dentro de la propia skill del repo gui-skills
  (``memoria/aprendizaje/inbox``, ``memoria/novedades``, ``memoria/fuentes``...), creándola si falta.

Orden para encontrar la bóveda: argumento ``--vault`` > variable ``SEO_OBSIDIAN_VAULT`` > clave
``obsidian_vault`` de ``~/.gui-skills/config.json`` > clave heredada ``vault`` de
``~/.seo-content-system.json``.
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

# Variable de entorno heredada: ruta alternativa al archivo ~/.seo-content-system.json
CONFIG_ENV = "SEO_CONTENT_SYSTEM_CONFIG"
# Ruta alternativa al archivo ~/.gui-skills/config.json
GUI_CONFIG_ENV = "GUI_SKILLS_CONFIG"
VAULT_ENV = "SEO_OBSIDIAN_VAULT"

SEO_FOLDER_NAME = "SEO Content System"


# ---------------------------------------------------------------- configuración

def gui_home() -> Path:
    """Carpeta privada de cada persona, fuera del repo (GUI_SKILLS_HOME la reemplaza, como en tools/)."""
    env = os.environ.get("GUI_SKILLS_HOME")
    return Path(env).expanduser() if env else Path.home() / ".gui-skills"


def gui_config_path() -> Path:
    override = os.environ.get(GUI_CONFIG_ENV)
    if override:
        return Path(override).expanduser().resolve()
    return gui_home() / "config.json"


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def load_gui_config() -> dict[str, Any]:
    return _read_json(gui_config_path())


def save_gui_config(data: dict[str, Any]) -> Path:
    path = gui_config_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def config_path() -> Path:
    """Archivo de configuración heredado (anterior al repo)."""
    override = os.environ.get(CONFIG_ENV)
    if override:
        return Path(override).expanduser().resolve()
    return Path.home() / ".seo-content-system.json"


def load_config() -> dict[str, Any]:
    return _read_json(config_path())


def save_config(data: dict[str, Any]) -> Path:
    path = config_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


# ---------------------------------------------------------------- bóveda (opcional)

def _find_seo_folder(base: Path, hinted: str | None) -> Path:
    """Dada una ruta de bóveda (o de la carpeta de la skill), devuelve la carpeta de trabajo de la skill."""
    if hinted:
        hint = Path(hinted).expanduser()
        hint = hint if hint.is_absolute() else base / hint
        if hint.is_dir():
            return hint.resolve()
    if (base / "06_Aprendizaje").is_dir():
        return base
    conocida = base / "maestro" / "03 Recursos" / SEO_FOLDER_NAME
    if conocida.is_dir():
        return conocida
    # búsqueda acotada (3 niveles) de una carpeta con el nombre de la skill
    base_depth = len(base.parts)
    for dirpath, dirnames, _files in os.walk(base):
        dirnames[:] = [d for d in dirnames if not d.startswith(".") and d != "node_modules"]
        if len(Path(dirpath).parts) - base_depth >= 3:
            dirnames[:] = []
        for d in dirnames:
            if d == SEO_FOLDER_NAME:
                return Path(dirpath) / d
    return base / SEO_FOLDER_NAME  # se creará al escribir


def resolve_vault(explicit: str | None = None, required: bool = False) -> Path | None:
    """Carpeta de la skill dentro de la bóveda de Obsidian, o None si no hay bóveda configurada."""
    gui = load_gui_config()
    legacy = load_config()
    candidates = [
        (explicit, None),
        (os.environ.get(VAULT_ENV), None),
        (gui.get("obsidian_vault"), gui.get("obsidian_seo_folder")),
        (legacy.get("vault"), None),
    ]
    for candidate, hinted in candidates:
        if not candidate:
            continue
        base = Path(str(candidate)).expanduser()
        if base.exists() and base.is_dir():
            return _find_seo_folder(base.resolve(), hinted)
    if required:
        raise SystemExit(
            "No se encontró una bóveda de Obsidian. Usa --vault, SEO_OBSIDIAN_VAULT o la clave "
            "obsidian_vault de ~/.gui-skills/config.json (la bóveda es opcional)."
        )
    return None


# ---------------------------------------------------------------- memoria (repo o bóveda)

@dataclass(frozen=True)
class Memory:
    kind: str  # "vault" o "repo"
    root: Path
    learning_inbox: Path
    decisions: Path
    news: Path
    sources: Path
    state_file: Path

    @property
    def is_vault(self) -> bool:
        return self.kind == "vault"

    def describe(self) -> str:
        return f"{'bóveda de Obsidian' if self.is_vault else 'memoria del repo'}: {self.root}"


def resolve_memory(explicit_vault: str | None = None) -> Memory:
    """Decide dónde se guarda la memoria. Nunca falla por no tener bóveda."""
    vault = resolve_vault(explicit_vault, required=False)
    if vault is not None:
        return Memory(
            kind="vault",
            root=vault,
            learning_inbox=vault / "06_Aprendizaje" / "Inbox",
            decisions=vault / "06_Aprendizaje" / "Decisiones",
            news=vault / "02_Investigacion" / "Novedades",
            sources=vault / "08_Fuentes",
            state_file=vault / ".seo-content-system" / "research-state.json",
        )
    root = skill_root() / "memoria"
    return Memory(
        kind="repo",
        root=root,
        learning_inbox=root / "aprendizaje" / "inbox",
        decisions=root / "decisiones",
        news=root / "novedades",
        sources=root / "fuentes",
        # el estado del recopilador es de cada persona: fuera del repo
        state_file=gui_home() / "seo-research-state.json",
    )


# ---------------------------------------------------------------- privacidad (solo para escribir en el repo)

_GENERIC_PRIVACY = [
    ("correo", re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")),
    ("ruta personal", re.compile(r"[A-Za-z]:[\\/]+(?:Users|Usuarios)[\\/]|/Users/[^/\s]+/|/home/[^/\s]+/", re.IGNORECASE)),
    ("credencial", re.compile(r"github_pat_|ghp_[A-Za-z0-9]|sk-[A-Za-z0-9]{10,}|AIza[0-9A-Za-z_-]{20,}|Bearer\s+[A-Za-z0-9._-]{20,}")),
]


def private_terms_path() -> Path:
    return gui_home() / "private-terms.txt"


def privacy_findings(text: str) -> list[str]:
    """Devuelve descripciones de lo que NO debería escribirse en el repo (sin repetir el término)."""
    findings: list[str] = []
    for label, rx in _GENERIC_PRIVACY:
        if rx.search(text):
            findings.append(f"patrón genérico: {label}")
    path = private_terms_path()
    if path.exists():
        for lineno, raw in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            try:
                if line.startswith("re:"):
                    rx = re.compile(line[3:])
                else:
                    rx = re.compile(r"(?<!\w)" + re.escape(line) + r"(?!\w)", re.IGNORECASE)
            except re.error:
                continue
            if rx.search(text):
                findings.append(f"término de la lista privada (línea {lineno} de private-terms.txt)")
    return findings


CASE_CODE = re.compile(r"^caso-[a-z0-9]+(?:-[a-z0-9]+)*-\d{2}$")
