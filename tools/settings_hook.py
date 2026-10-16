#!/usr/bin/env python3
"""Merge (or remove) the gui-skills SessionStart hook in a Claude Code settings.json.

Keeps every existing key and hook, never duplicates, backs the file up before changing it.
Exit codes: 0 ok (changed or not), 1 unreadable/invalid settings.json (file untouched), 2 usage.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True

MARKER = "check_update.py"
MATCHER = "startup|resume|clear"


def is_ours(hook: dict) -> bool:
    cmd = hook.get("command") if isinstance(hook, dict) else None
    return isinstance(cmd, str) and MARKER in cmd and "--hook" in cmd


def build_command(python: str, script: str) -> str:
    # forward slashes work in bash, cmd, PowerShell and Python alike
    return f'{python} "{script.replace(chr(92), "/")}" --hook'


def merge(settings: dict, command: str) -> str:
    """Mutate settings; return 'added', 'updated' or 'unchanged'."""
    hooks = settings.setdefault("hooks", {})
    if not isinstance(hooks, dict):
        raise ValueError("'hooks' en settings.json no es un objeto")
    groups = hooks.setdefault("SessionStart", [])
    if not isinstance(groups, list):
        raise ValueError("'hooks.SessionStart' en settings.json no es una lista")
    for group in groups:
        for hook in (group.get("hooks", []) if isinstance(group, dict) else []):
            if is_ours(hook):
                if hook.get("command") == command:
                    return "unchanged"
                hook["command"] = command
                return "updated"
    groups.append({"matcher": MATCHER, "hooks": [{"type": "command", "command": command, "timeout": 20}]})
    return "added"


def remove(settings: dict) -> str:
    groups = settings.get("hooks", {}).get("SessionStart") if isinstance(settings.get("hooks"), dict) else None
    if not isinstance(groups, list):
        return "unchanged"
    changed = False
    for group in list(groups):
        if not isinstance(group, dict) or not isinstance(group.get("hooks"), list):
            continue
        kept = [h for h in group["hooks"] if not is_ours(h)]
        if len(kept) != len(group["hooks"]):
            changed = True
            group["hooks"] = kept
            if not kept:
                groups.remove(group)
    if changed and not groups:
        del settings["hooks"]["SessionStart"]
        if not settings["hooks"]:
            del settings["hooks"]
    return "removed" if changed else "unchanged"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--settings", required=True)
    ap.add_argument("--command", help="comando completo del hook")
    ap.add_argument("--python", help="ejecutable de Python (junto con --script arma el comando)")
    ap.add_argument("--script", help="ruta de check_update.py (junto con --python)")
    ap.add_argument("--backup-dir", help="carpeta para la copia de seguridad (por defecto, junto al archivo)")
    ap.add_argument("--remove", action="store_true")
    a = ap.parse_args(argv)
    if not a.remove and not a.command:
        if not (a.python and a.script):
            print("ERROR: falta --command, o --python junto con --script", file=sys.stderr)
            return 2
        a.command = build_command(a.python, a.script)

    path = Path(a.settings)
    existed = path.is_file()
    settings = {}
    if existed:
        try:
            settings = json.loads(path.read_text(encoding="utf-8-sig"))
            if not isinstance(settings, dict):
                raise ValueError("la raíz no es un objeto JSON")
        except (OSError, ValueError) as exc:
            print(f"ERROR: no puedo leer {path} como JSON ({exc}); no se tocó.", file=sys.stderr)
            return 1
    try:
        result = remove(settings) if a.remove else merge(settings, a.command)
    except ValueError as exc:
        print(f"ERROR: {exc}; no se tocó {path}.", file=sys.stderr)
        return 1

    if result == "unchanged":
        print(f"unchanged {path}")
        return 0
    if existed:
        bdir = Path(a.backup_dir) if a.backup_dir else path.parent
        bdir.mkdir(parents=True, exist_ok=True)
        backup = bdir / f"{path.name}.bak-{time.strftime('%Y%m%d-%H%M%S')}"
        shutil.copy2(path, backup)
        print(f"backup {backup}")
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(settings, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(path)
    print(f"{result} {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
