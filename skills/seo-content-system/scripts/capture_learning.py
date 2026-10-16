#!/usr/bin/env python3
"""Registra un aprendizaje candidato.

Sin bóveda de Obsidian (lo normal) lo guarda en ``memoria/aprendizaje/inbox/`` dentro de la skill, creando
la carpeta si no existe. Con bóveda configurada lo guarda en su ``06_Aprendizaje/Inbox/``.
"""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from datetime import date, timedelta
from pathlib import Path

from paths import CASE_CODE, privacy_findings, resolve_memory


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", ascii_text).strip("-").lower()
    return slug[:80] or "aprendizaje"


def unique_path(folder: Path, stem: str) -> Path:
    path = folder / f"{stem}.md"
    counter = 2
    while path.exists():
        path = folder / f"{stem}-{counter}.md"
        counter += 1
    return path


def yaml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Guarda un aprendizaje candidato en memoria/aprendizaje/inbox/ (o en la bóveda de Obsidian si está configurada)."
    )
    parser.add_argument("--title", required=True)
    parser.add_argument("--summary", required=True)
    parser.add_argument("--evidence", default="")
    parser.add_argument("--context", default="")
    parser.add_argument("--limitations", default="")
    parser.add_argument("--project", default="", help="código del caso (caso-<tipo>-<NN>); nunca el nombre del cliente")
    parser.add_argument("--source", action="append", default=[])
    parser.add_argument("--topic", action="append", default=["seo"])
    parser.add_argument("--confidence", choices=["low", "medium", "high"], default="low")
    parser.add_argument("--status", choices=["candidate", "testing", "promoted", "discarded"], default="candidate")
    parser.add_argument("--review-days", type=int, default=30)
    parser.add_argument("--vault", help="ruta de la bóveda de Obsidian (opcional)")
    parser.add_argument("--sin-chequeo-privacidad", action="store_true",
                        help="no revisar nombres de clientes/correos/rutas (solo para la bóveda privada)")
    args = parser.parse_args()

    memory = resolve_memory(args.vault)

    if not memory.is_vault and not args.sin_chequeo_privacidad:
        problems: list[str] = []
        if args.project and not CASE_CODE.match(args.project):
            problems.append("--project debe ser un código de caso (caso-<tipo>-<NN>)")
        blob = "\n".join([args.title, args.summary, args.evidence, args.context, args.limitations,
                          args.project, *args.source])
        problems += privacy_findings(blob)
        if problems:
            print("No se escribió nada: este texto iría al repo y la revisión de privacidad encontró:")
            for item in problems:
                print(f"  - {item}")
            print("Anonimiza (códigos de caso, sin correos, rutas ni nombres de clientes) y vuelve a correr.")
            return 2

    folder = memory.learning_inbox
    folder.mkdir(parents=True, exist_ok=True)
    today = date.today()
    stem = f"{today.isoformat()}-{slugify(args.title)}"
    path = unique_path(folder, stem)

    topics = "\n".join(f"  - {yaml_string(topic)}" for topic in args.topic)
    sources = "\n".join(f"  - {yaml_string(source)}" for source in args.source) or "  []"
    projects = f"\n  - {yaml_string(args.project)}" if args.project else " []"
    if memory.is_vault:
        relaciones = "- [[Mapa de aprendizaje SEO]]\n- [[Protocolo de actualización]]"
    else:
        relaciones = ("- `HANDOFF.md` §5 (reglas candidatas) de la skill\n"
                      "- `references/update-governance-and-research.md` (cómo se promueve un aprendizaje)")
    content = f"""---
type: learning
status: {args.status}
created: {today.isoformat()}
updated: {today.isoformat()}
confidence: {args.confidence}
review_after: {(today + timedelta(days=args.review_days)).isoformat()}
topics:
{topics}
sources:
{sources}
projects:{projects}
---

# {args.title}

## Resumen

{args.summary}

## Contexto

{args.context or "Pendiente de documentar."}

## Evidencia

{args.evidence or "Pendiente de adjuntar."}

## Limitaciones

{args.limitations or "Pendiente de evaluar."}

## Próxima validación

- Contrastar con datos o una fuente independiente.
- Definir en qué contextos aplica.
- Decidir si se promueve, se mantiene en prueba o se descarta.

## Relaciones

{relaciones}
"""
    path.write_text(content, encoding="utf-8")
    print(path)
    print(f"({memory.describe()})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
