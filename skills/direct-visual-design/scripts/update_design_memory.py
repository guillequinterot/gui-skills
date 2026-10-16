#!/usr/bin/env python3
"""Append one validated design-learning record to a JSONL memory file."""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path


SCOPES = {"global", "brand", "project"}
STATUSES = {"candidate", "approved", "deprecated"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", default=".design-director/design-memory.jsonl")
    parser.add_argument("--scope", required=True, choices=sorted(SCOPES))
    parser.add_argument("--context", required=True)
    parser.add_argument("--learning", required=True)
    parser.add_argument("--evidence", required=True)
    parser.add_argument("--status", default="candidate", choices=sorted(STATUSES))
    parser.add_argument("--source", default="user feedback")
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    record = {
        "timestamp": args.date,
        "scope": args.scope,
        "context": args.context.strip(),
        "learning": args.learning.strip(),
        "evidence": args.evidence.strip(),
        "status": args.status,
        "source": args.source.strip(),
    }
    if not all(record[key] for key in ("context", "learning", "evidence", "source")):
        raise SystemExit("context, learning, evidence, and source must not be empty")

    line = json.dumps(record, ensure_ascii=False, separators=(",", ":"))
    if args.dry_run:
        print(line)
        return 0

    target = Path(args.file).expanduser().resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("a", encoding="utf-8") as stream:
        stream.write(line + "\n")
    print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

