#!/usr/bin/env python3
"""Valida la memoria de la skill: la carpeta ``memoria/`` del repo y, si hay bóveda, su estructura.

Sin bóveda de Obsidian (lo normal) comprueba ``memoria/`` dentro de la skill. Con bóveda configurada
comprueba además la estructura esperada y que el frontmatter de sus notas esté cerrado.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from paths import resolve_memory, resolve_vault, skill_root

VAULT_REQUIRED = [
    "00_Inicio",
    "01_Conocimiento",
    "02_Investigacion",
    "03_Estrategia",
    "04_Produccion",
    "05_Medicion",
    "06_Aprendizaje",
    "07_Plantillas",
    "08_Fuentes",
    "09_Proyectos",
]

REPO_REQUIRED = [
    "aprendizaje/inbox",
    "decisiones",
    "novedades",
    "fuentes",
]

FRONTMATTER_OK = re.compile(r"^---\r?\n.*?\r?\n---\r?\n", flags=re.DOTALL)


def check_frontmatter(base: Path, errors: list[str]) -> int:
    notes = [n for n in base.rglob("*.md") if ".git" not in n.parts]
    for note in notes:
        text = note.read_text(encoding="utf-8", errors="replace")
        if text.startswith("---") and not FRONTMATTER_OK.match(text):
            errors.append(f"Frontmatter sin cierre: {note.relative_to(base)}")
    return len(notes)


def main() -> int:
    parser = argparse.ArgumentParser(description="Valida memoria/ del repo y, si existe, la bóveda de Obsidian.")
    parser.add_argument("--vault", help="ruta de la bóveda de Obsidian (opcional)")
    parser.add_argument("--init", action="store_true", help="crear las carpetas de memoria/ que falten")
    args = parser.parse_args()

    errors: list[str] = []

    # 1. memoria del repo (siempre)
    memoria = skill_root() / "memoria"
    for rel in REPO_REQUIRED:
        folder = memoria / rel
        if not folder.is_dir():
            if args.init:
                folder.mkdir(parents=True, exist_ok=True)
                print(f"Creada: memoria/{rel}")
            else:
                errors.append(f"Falta carpeta: memoria/{rel} (usa --init para crearla)")
    total = check_frontmatter(memoria, errors) if memoria.is_dir() else 0
    print(f"Memoria del repo: {memoria} ({total} notas Markdown)")

    # 2. bóveda (solo si está configurada)
    vault = resolve_vault(args.vault, required=False)
    if vault is None:
        print("Sin bóveda de Obsidian configurada: se valida solo la memoria del repo (es lo normal).")
    elif not vault.is_dir():
        print(f"Bóveda configurada pero la carpeta de la skill aún no existe: {vault} (se creará al escribir).")
    else:
        for folder in VAULT_REQUIRED:
            if not (vault / folder).is_dir():
                # la estructura de la bóveda es una sugerencia: se avisa, no se falla
                print(f"Aviso: la bóveda no tiene la carpeta sugerida {folder}")
        count = check_frontmatter(vault, errors)
        print(f"Bóveda: {vault} ({count} notas Markdown)")

    _ = resolve_memory(args.vault)  # comprueba que la resolución no falla
    if errors:
        for error in errors:
            print(f"- {error}")
        return 1
    print("Memoria válida.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
