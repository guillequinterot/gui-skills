"""Shared helpers for the gui-skills tools (stdlib only, Python >= 3.9)."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True

ALIAS_RE = r"^[a-z0-9][a-z0-9_-]{1,30}$"


def setup_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def gui_home() -> Path:
    """Per-person private folder, outside the repo. GUI_SKILLS_HOME overrides (tests)."""
    env = os.environ.get("GUI_SKILLS_HOME")
    return Path(env) if env else Path.home() / ".gui-skills"


def load_config() -> dict:
    path = gui_home() / "config.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


def script_repo_root(script_file: str) -> Path:
    return Path(script_file).resolve().parent.parent


def resolve_repo(arg: str | None, script_file: str) -> Path:
    """--repo, else repo_path from config.json, else the script's parent's parent."""
    if arg:
        return Path(arg).expanduser().resolve()
    cfg = load_config().get("repo_path")
    if cfg:
        return Path(str(cfg)).expanduser().resolve()
    return script_repo_root(script_file)


def is_maintainer() -> bool:
    """True only when ~/.gui-skills/config.json has "mantenedor": true (a real JSON boolean)."""
    return load_config().get("mantenedor") is True
