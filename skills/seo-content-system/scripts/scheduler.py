#!/usr/bin/env python3
"""Muestra o instala una programación local del recopilador de novedades (solo lectura).

La bóveda de Obsidian es opcional: sin ella el recopilador escribe en ``memoria/novedades/`` de la skill.
"""

from __future__ import annotations

import argparse
import json
import platform
import shlex
import subprocess
import sys
from pathlib import Path

from paths import load_config, load_gui_config, resolve_vault, skill_root


MARKER = "seo-content-system-research"


def command(vault: Path | None) -> list[str]:
    cmd = [sys.executable, str(skill_root() / "scripts" / "research_update.py")]
    if vault is not None:
        cmd += ["--vault", str(vault)]
    return cmd


def cron_line(cmd: list[str], frequency: str, hour: int, weekday: int) -> str:
    escaped = " ".join(shlex.quote(part) for part in cmd)
    if frequency == "daily":
        spec = f"0 {hour} * * *"
    elif frequency == "monthly":
        spec = f"0 {hour} 1 * *"
    else:
        spec = f"0 {hour} * * {weekday}"
    return f"{spec} {escaped} # {MARKER}"


def install_linux(line: str) -> None:
    current = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    lines = [item for item in current.stdout.splitlines() if MARKER not in item]
    lines.append(line)
    subprocess.run(["crontab", "-"], input="\n".join(lines) + "\n", text=True, check=True)


def install_macos(cmd: list[str], frequency: str, hour: int, weekday: int) -> Path:
    interval = (
        f"<key>Hour</key><integer>{hour}</integer>"
        if frequency == "daily"
        else f"<key>Weekday</key><integer>{weekday + 1}</integer><key>Hour</key><integer>{hour}</integer>"
        if frequency == "weekly"
        else f"<key>Day</key><integer>1</integer><key>Hour</key><integer>{hour}</integer>"
    )
    args = "".join(f"<string>{part}</string>" for part in cmd)
    plist = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
<key>Label</key><string>com.seo-content-system.research</string>
<key>ProgramArguments</key><array>{args}</array>
<key>StartCalendarInterval</key><dict>{interval}</dict>
<key>RunAtLoad</key><false/>
</dict></plist>
"""
    path = Path.home() / "Library" / "LaunchAgents" / "com.seo-content-system.research.plist"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(plist, encoding="utf-8")
    subprocess.run(["launchctl", "unload", str(path)], capture_output=True)
    subprocess.run(["launchctl", "load", str(path)], check=True)
    return path


def windows_schedule(frequency: str, hour: int, weekday: int) -> tuple[str, list[str]]:
    schedule = {"daily": "DAILY", "weekly": "WEEKLY", "monthly": "MONTHLY"}[frequency]
    days = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]
    extra = ["/D", days[weekday]] if frequency == "weekly" else ["/D", "1"] if frequency == "monthly" else []
    return schedule, extra


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["show", "install"])
    parser.add_argument("--frequency", choices=["daily", "weekly", "monthly"], default="weekly")
    parser.add_argument("--hour", type=int, default=9)
    parser.add_argument("--weekday", type=int, choices=range(0, 7), default=1, help="0=domingo, 1=lunes")
    parser.add_argument("--vault", help="ruta de la bóveda de Obsidian (opcional)")
    args = parser.parse_args()
    if not 0 <= args.hour <= 23:
        raise SystemExit("--hour debe estar entre 0 y 23")

    vault = resolve_vault(args.vault, required=False)
    cmd = command(vault)
    system = platform.system()
    preview = {"platform": system, "frequency": args.frequency, "command": cmd, "vault": str(vault) if vault else None,
               "config": {**load_config(), **load_gui_config()}}
    if args.action == "show":
        if system in {"Linux", "Darwin"}:
            preview["schedule"] = cron_line(cmd, args.frequency, args.hour, args.weekday)
        else:
            preview["schedule"] = f"{args.frequency} a las {args.hour:02d}:00"
        print(json.dumps(preview, ensure_ascii=False, indent=2))
        return 0

    if system == "Linux":
        install_linux(cron_line(cmd, args.frequency, args.hour, args.weekday))
    elif system == "Darwin":
        print(install_macos(cmd, args.frequency, args.hour, args.weekday))
    elif system == "Windows":
        schedule, extra = windows_schedule(args.frequency, args.hour, args.weekday)
        task_command = subprocess.list2cmdline(cmd)
        subprocess.run(
            ["schtasks", "/Create", "/F", "/TN", "SEO Content System Research", "/SC", schedule, "/ST", f"{args.hour:02d}:00", *extra, "/TR", task_command],
            check=True,
        )
    else:
        raise SystemExit(f"Plataforma no soportada automáticamente: {system}")
    print("Programación instalada.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

