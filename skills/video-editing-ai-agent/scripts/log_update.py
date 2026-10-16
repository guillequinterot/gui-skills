#!/usr/bin/env python
"""Registra una actualización de la skill en logs/UPDATE-LOG.md y logs/update-log.jsonl.

Uso:
  python log_update.py --engine shotcut --kind learning --change "..." --evidence "..." [--project caso-video-02] [--tools "Shotcut 26.8.1; MLT 7.41"]
Tipos: learning | fix | engine-add | engine-verify | source | deprecation | candidate
'candidate' = hipótesis sin verificar (no se promueve a regla hasta repetirse o aprobarse).
Después: anota el cambio en `HANDSHAKE.md` / `HANDOFF.md` de la skill (repo gui-skills); si el usuario usa Obsidian, refléjalo además en su nota de registro de skills.
"""
import argparse, datetime, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGS = os.path.join(ROOT, "logs")
KINDS = ["learning", "fix", "engine-add", "engine-verify", "source", "deprecation", "candidate"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--engine", required=True)
    ap.add_argument("--kind", required=True, choices=KINDS)
    ap.add_argument("--change", required=True)
    ap.add_argument("--evidence", default="")
    ap.add_argument("--project", default="")
    ap.add_argument("--tools", default="")
    a = ap.parse_args()
    os.makedirs(LOGS, exist_ok=True)
    now = datetime.datetime.now().astimezone()
    entry = {"date": now.strftime("%Y-%m-%d"), "time": now.strftime("%H:%M"), "engine": a.engine, "kind": a.kind, "change": a.change,
             "evidence": a.evidence, "project": a.project, "tools": a.tools}
    with open(os.path.join(LOGS, "update-log.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    md = os.path.join(LOGS, "UPDATE-LOG.md")
    row = f"| {entry['date']} | {a.engine} | {a.kind} | {a.change} | {a.evidence} | {a.project} | {a.tools} |\n"
    if not os.path.exists(md):
        with open(md, "w", encoding="utf-8") as f:
            f.write("# UPDATE-LOG — Video-Editing-AI-Agent\n\n| Fecha | Motor | Tipo | Cambio | Evidencia | Proyecto | Herramientas |\n|---|---|---|---|---|---|---|\n")
    lines = open(md, encoding="utf-8").read().splitlines(keepends=True)
    # insertar tras la última fila de la tabla principal (antes de cualquier sección posterior)
    last = -1
    for i, ln in enumerate(lines):
        if ln.startswith("## ") and last >= 0:
            break
        if ln.startswith("|"):
            last = i
    lines.insert(last + 1, row)
    with open(md, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print("registrado:", row.strip())


if __name__ == "__main__":
    main()
