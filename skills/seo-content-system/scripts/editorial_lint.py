#!/usr/bin/env python3
"""Flag mechanical editorial patterns without rewriting the text."""

from __future__ import annotations

import argparse
import json
import re
import statistics
from pathlib import Path


PATTERNS = {
    "apertura_genérica": [
        r"\ben el mundo actual\b",
        r"\ben la era digital\b",
        r"\ben un entorno cada vez más competitivo\b",
    ],
    "relleno": [
        r"\bes importante destacar que\b",
        r"\bcabe mencionar que\b",
        r"\ba continuación,? exploraremos\b",
    ],
    "cierre_genérico": [r"\ben conclusión\b", r"\ben resumen\b"],
    "contraste_repetible": [r"\bno se trata solo de\b.+\bsino (también )?de\b"],
    "adjetivo_sin_evidencia": [r"\b(innovador|revolucionario|único|líder|disruptivo)\b"],
}


def lint(text: str) -> list[dict[str, object]]:
    findings: list[dict[str, object]] = []
    lower = text.lower()
    for category, patterns in PATTERNS.items():
        for pattern in patterns:
            matches = list(re.finditer(pattern, lower, flags=re.DOTALL))
            if matches:
                findings.append(
                    {
                        "category": category,
                        "count": len(matches),
                        "examples": [text[max(0, m.start() - 25) : m.end() + 35].replace("\n", " ") for m in matches[:3]],
                    }
                )

    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip() and not p.lstrip().startswith(("#", "-", "|", "```"))]
    word_counts = [len(re.findall(r"\b\w+\b", p, flags=re.UNICODE)) for p in paragraphs]
    if len(word_counts) >= 5:
        mean = statistics.mean(word_counts)
        stdev = statistics.pstdev(word_counts)
        if mean and stdev / mean < 0.18:
            findings.append(
                {
                    "category": "longitud_uniforme",
                    "count": len(word_counts),
                    "detail": "Los párrafos tienen longitudes muy similares; revisar ritmo.",
                }
            )
    long_paragraphs = [count for count in word_counts if count > 180]
    if long_paragraphs:
        findings.append(
            {
                "category": "párrafo_extenso",
                "count": len(long_paragraphs),
                "detail": "Revisar si cada párrafo mantiene una sola unidad de sentido.",
            }
        )

    headings = re.findall(r"^#{1,6}\s+(.+)$", text, flags=re.MULTILINE)
    title_case = [h for h in headings if len(re.findall(r"\b[A-ZÁÉÍÓÚÑ][^\s]*", h)) >= 3]
    if title_case:
        findings.append(
            {
                "category": "mayúsculas_en_títulos",
                "count": len(title_case),
                "examples": title_case[:5],
            }
        )
    return findings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    text = args.file.read_text(encoding="utf-8")
    findings = lint(text)
    if args.json:
        print(json.dumps({"file": str(args.file), "findings": findings}, ensure_ascii=False, indent=2))
    elif not findings:
        print("Sin señales mecánicas detectadas.")
    else:
        for finding in findings:
            print(f"- {finding['category']}: {finding.get('count', 1)}")
            for example in finding.get("examples", []):
                print(f"  · {example}")
            if finding.get("detail"):
                print(f"  · {finding['detail']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

