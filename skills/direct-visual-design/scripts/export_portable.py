#!/usr/bin/env python3
"""Export the skill as a portable project context with optional root adapters."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


ADAPTERS = ("AGENTS.md", "CLAUDE.md", "GEMINI.md", "PROJECT-INSTRUCTIONS.md")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("target", help="Project directory receiving .design-director")
    parser.add_argument(
        "--root-adapters",
        action="store_true",
        help="Copy adapter files to project root only when the filename is absent",
    )
    return parser.parse_args()


def copy_tree_clean(source: Path, destination: Path) -> None:
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(source, destination)


def main() -> int:
    args = parse_args()
    skill_root = Path(__file__).resolve().parent.parent
    target_root = Path(args.target).expanduser().resolve()
    portable = target_root / ".design-director"
    portable.mkdir(parents=True, exist_ok=True)

    shutil.copy2(skill_root / "SKILL.md", portable / "SKILL.md")
    copy_tree_clean(skill_root / "references", portable / "references")
    copy_tree_clean(skill_root / "scripts", portable / "scripts")
    copy_tree_clean(skill_root / "assets" / "platform-adapters", portable / "adapters")

    memory = portable / "design-memory.jsonl"
    memory.touch(exist_ok=True)

    installed = []
    skipped = []
    if args.root_adapters:
        for name in ADAPTERS:
            source = portable / "adapters" / name
            destination = target_root / name
            if destination.exists():
                skipped.append(name)
            else:
                shutil.copy2(source, destination)
                installed.append(name)

    print(f"portable={portable}")
    print(f"installed={','.join(installed)}")
    print(f"skipped={','.join(skipped)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
