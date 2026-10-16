#!/usr/bin/env python3
"""Ayudante para instalar la skill en destinos que el instalador general del repo no cubre.

La fuente es SIEMPRE esta carpeta del repo gui-skills (``<repo>/skills/seo-content-system``). Ya no
"refresca" copias desde ninguna bóveda de Obsidian: la instalación en Claude Code la hace
``tools/install.ps1`` / ``tools/install.sh`` por enlaces. Este script sirve para Codex, Antigravity o una
instalación por proyecto, y también crea enlaces (o copia si el sistema no permite enlaces).
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

from paths import load_gui_config, save_gui_config, skill_root

SKILL_NAME = "seo-content-system"
VALID_TARGETS = {"codex", "claude", "antigravity"}


def parse_targets(value: str) -> list[str]:
    targets = [part.strip().lower() for part in value.split(",") if part.strip()]
    invalid = sorted(set(targets) - VALID_TARGETS)
    if invalid:
        raise argparse.ArgumentTypeError(f"Targets no válidos: {', '.join(invalid)}")
    return targets


def destinations(targets: list[str], scope: str, project: Path | None) -> dict[str, Path]:
    base = Path.home() if scope == "user" else project
    if base is None:
        raise SystemExit("--project es obligatorio con --scope project")
    result: dict[str, Path] = {}
    for target in targets:
        folder = ".claude" if target == "claude" else ".agents"
        result[target] = base / folder / "skills" / SKILL_NAME
    return result


def is_link_to(destination: Path, source: Path) -> bool:
    try:
        return destination.exists() and destination.resolve() == source.resolve() and (
            destination.is_symlink() or _is_junction(destination)
        )
    except OSError:
        return False


def _is_junction(path: Path) -> bool:
    checker = getattr(os.path, "isjunction", None)
    return bool(checker and checker(path))


def make_link(source: Path, destination: Path) -> str:
    """Crea un enlace de directorio; si no se puede, copia. Devuelve 'enlace' o 'copia'."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        os.symlink(source, destination, target_is_directory=True)
        return "enlace"
    except (OSError, NotImplementedError):
        pass
    if os.name == "nt":
        result = subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(destination), str(source)], capture_output=True, text=True
        )
        if result.returncode == 0:
            return "enlace"
    ignore = shutil.ignore_patterns(".git", "__pycache__", ".DS_Store", "*.pyc")
    shutil.copytree(source, destination, ignore=ignore)
    return "copia"


def install_one(source: Path, destination: Path, force: bool) -> str:
    if source == destination or source in destination.parents:
        raise SystemExit(f"Destino inseguro o recursivo: {destination}")
    if is_link_to(destination, source):
        return "ya enlazado"
    if destination.exists() or destination.is_symlink():
        if not force:
            raise SystemExit(
                f"{destination} ya existe y no es un enlace a esta skill. Revísalo, o usa --force para "
                "respaldarlo (.bak-AAAAMMDD) y reemplazarlo."
            )
        backup = destination.with_name(f"{destination.name}.bak-{date.today():%Y%m%d}")
        n = 2
        while backup.exists():
            backup = destination.with_name(f"{destination.name}.bak-{date.today():%Y%m%d}-{n}")
            n += 1
        if destination.is_symlink() or _is_junction(destination):
            destination.unlink() if destination.is_symlink() else os.rmdir(destination)
        else:
            destination.rename(backup)
            print(f"Respaldo: {backup}")
    mode = make_link(source, destination)
    if not (destination / "SKILL.md").exists():
        raise SystemExit(f"La instalación no contiene SKILL.md: {destination}")
    return mode


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Instala la skill desde el repo gui-skills (por enlace) en Codex, Antigravity o un proyecto."
    )
    parser.add_argument("--targets", type=parse_targets, default=parse_targets("codex,antigravity"))
    parser.add_argument("--scope", choices=["user", "project"], default="user")
    parser.add_argument("--project", type=Path)
    parser.add_argument("--vault", type=Path, help="guarda obsidian_vault en ~/.gui-skills/config.json (opcional)")
    parser.add_argument("--force", action="store_true", help="respalda y reemplaza un destino que ya existe")
    parser.add_argument("--refresh", action="store_true", help="obsoleto: ya no hay nada que refrescar desde la bóveda; equivale a reinstalar")
    parser.add_argument("--schedule", choices=["none", "daily", "weekly", "monthly"], default="none")
    parser.add_argument("--schedule-hour", type=int, default=9)
    parser.add_argument("--schedule-weekday", type=int, choices=range(0, 7), default=1)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    source = skill_root()
    project = args.project.expanduser().resolve() if args.project else None
    dests = destinations(args.targets, args.scope, project)
    unique_paths = sorted(set(dests.values()), key=str)

    plan = {
        "source": str(source),
        "scope": args.scope,
        "destinations": {key: str(value) for key, value in dests.items()},
        "vault": str(args.vault.expanduser().resolve()) if args.vault else None,
        "schedule": args.schedule,
        "nota": "claude en el nivel usuario lo instala tools/install.ps1 / tools/install.sh",
    }
    if args.refresh:
        print("Aviso: --refresh ya no copia desde ninguna bóveda; la skill se instala por enlace desde el repo.", file=sys.stderr)
    if args.dry_run:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return 0

    for destination in unique_paths:
        print(f"{destination}: {install_one(source, destination, args.force)}")

    if args.vault:
        vault = args.vault.expanduser().resolve()
        vault.mkdir(parents=True, exist_ok=True)
        config = load_gui_config()
        config["obsidian_vault"] = str(vault)
        print(f"Configuración: {save_gui_config(config)} (obsidian_vault={vault})")

    if args.schedule != "none":
        cmd = [
            sys.executable, str(source / "scripts" / "scheduler.py"), "install",
            "--frequency", args.schedule, "--hour", str(args.schedule_hour),
            "--weekday", str(args.schedule_weekday),
        ]
        if args.vault:
            cmd += ["--vault", str(args.vault.expanduser().resolve())]
        subprocess.run(cmd, check=True)
    print(f"Skill instalada en {len(unique_paths)} ubicación(es).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
