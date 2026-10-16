#!/usr/bin/env python3
"""Append a work-log entry to skills/<skill>/HANDOFF.md (section 4) after a privacy check."""
from __future__ import annotations

import argparse
import re
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import gui_common  # noqa: E402
import privacy_scan  # noqa: E402

CASE_RE = re.compile(r"^(?:caso-[a-z0-9-]+-\d{2}|banco-pruebas-[a-z0-9-]+)$")
SKILL_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
MARK_START = "<!-- registro:inicio -->"
MARK_END = "<!-- registro:fin -->"
RULES_HEADING = re.compile(r"^##\s+5\.\s+Reglas candidatas", re.M)


def clean(text: str) -> str:
    """One line per field so the entry format cannot be broken."""
    return " ".join((text or "").split())


def fail(msg: str, code: int = 1) -> int:
    print(f"ERROR: {msg}", file=sys.stderr)
    return code


def build_entry(a, fields: dict) -> str:
    mal = fields["mal"]
    if fields["incidencia"]:
        mal = f"{mal} Incidencia: {fields['incidencia']}" if mal else f"Incidencia: {fields['incidencia']}"
    return "\n".join([
        f"### {a.fecha} · {a.caso} · {fields['alias']}",
        "",
        f"- **Qué se hizo:** {fields['hecho']}",
        f"- **Salió bien:** {fields['bien']}",
        f"- **Salió mal / incidencia:** {mal or 'nada relevante'}",
        f"- **Regla candidata:** {fields['regla'] or 'ninguna'}",
        f"- **Herramientas:** {fields['herramientas'] or 'no indicadas'}",
    ]) + "\n"


def add_rule_row(content: str, nl: str, regla: str, caso: str) -> str:
    m = RULES_HEADING.search(content)
    if not m:
        raise ValueError("no encuentro la sección '## 5. Reglas candidatas' en el HANDOFF")
    pos = m.end()
    last_end = None
    for line in content[m.end():].splitlines(keepends=True):
        body = line.rstrip("\r\n")
        if body.strip().startswith("|"):
            last_end = pos + len(body)
        elif last_end is not None:
            break
        pos += len(line)
    if last_end is None:
        raise ValueError("la sección 'Reglas candidatas' no tiene tabla")
    row = f"| {regla.replace('|', '/')} | {caso} | candidata |"
    return content[:last_end] + nl + row + content[last_end:]


def main(argv=None) -> int:
    gui_common.setup_stdio()
    ap = argparse.ArgumentParser(description="Agrega una entrada al Registro de trabajos del HANDOFF de una skill.")
    ap.add_argument("--skill", required=True, help="nombre de la carpeta en skills/")
    ap.add_argument("--caso", required=True, help="caso-<tipo>-<NN> o banco-pruebas-<tema>")
    ap.add_argument("--hecho", required=True)
    ap.add_argument("--bien", required=True)
    ap.add_argument("--mal", required=True, help='lo que salió mal, o "nada relevante"')
    ap.add_argument("--incidencia", default="")
    ap.add_argument("--regla-candidata", default="")
    ap.add_argument("--herramientas", default="")
    ap.add_argument("--alias")
    ap.add_argument("--fecha", default=time.strftime("%Y-%m-%d"))
    ap.add_argument("--repo")
    ap.add_argument("--dry-run", action="store_true", help="muestra la entrada sin escribir nada")
    a = ap.parse_args(argv)

    if not SKILL_RE.match(a.skill):
        return fail("--skill solo admite minúsculas, números y guiones")
    if not CASE_RE.match(a.caso):
        return fail("--caso debe ser 'caso-<tipo>-<NN>' (p. ej. caso-web-universidad-01) "
                    "o 'banco-pruebas-<tema>'; nunca el nombre del cliente")
    if not DATE_RE.match(a.fecha):
        return fail("--fecha debe ser AAAA-MM-DD")
    alias = (a.alias or gui_common.load_config().get("alias") or "").strip()
    if not alias:
        return fail("falta el alias: usa --alias o define 'alias' en ~/.gui-skills/config.json")
    if not re.match(r"^[\w.-]{1,40}$", alias):
        return fail("el alias solo admite letras, números, punto, guion y guion bajo")

    repo = gui_common.resolve_repo(a.repo, __file__)
    handoff = repo / "skills" / a.skill / "HANDOFF.md"
    if not handoff.is_file():
        return fail(f"no existe {handoff} (¿nombre de la skill?)")

    fields = {
        "alias": alias, "hecho": clean(a.hecho), "bien": clean(a.bien), "mal": clean(a.mal),
        "incidencia": clean(a.incidencia), "regla": clean(a.regla_candidata),
        "herramientas": clean(a.herramientas),
    }
    for key in ("hecho", "bien", "mal"):
        if not fields[key]:
            return fail(f"--{key} no puede estar vacío")
    for name, value in list(fields.items()) + [("caso", a.caso)]:
        if "<!--" in value or value.startswith("#"):
            return fail(f"el campo '{name}' no puede contener marcadores HTML ni empezar con '#'")

    try:
        scanner = privacy_scan.build_scanner(use_terms=True, repo=repo)
    except ValueError as exc:
        return fail(str(exc), 2)
    labels = {"alias": "--alias", "hecho": "--hecho", "bien": "--bien", "mal": "--mal",
              "incidencia": "--incidencia", "regla": "--regla-candidata", "herramientas": "--herramientas"}
    hits = []
    for key, label in labels.items():
        hits += scanner.scan_text(fields[key], label)
    hits += scanner.scan_text(a.caso, "--caso")
    if hits:
        print("Entrada rechazada por el escáner de privacidad (no se escribió nada):", file=sys.stderr)
        for h in hits:
            print(f"  {h.file}: [{h.category}] {h.detail}", file=sys.stderr)
        print("Reescribe esos campos sin datos de cliente: usa solo el código del caso, "
              "sin nombres, marcas, dominios, contactos ni rutas personales.", file=sys.stderr)
        return 1

    raw = handoff.read_bytes().decode("utf-8")
    content = raw.lstrip("\N{ZERO WIDTH NO-BREAK SPACE}")
    bom = raw[:len(raw) - len(content)]
    nl = "\r\n" if "\r\n" in content else "\n"
    if content.count(MARK_START) != 1 or content.count(MARK_END) != 1:
        return fail(f"{handoff} debe tener exactamente un '{MARK_START}' y un '{MARK_END}'")
    start, end = content.index(MARK_START), content.index(MARK_END)
    if end < start:
        return fail("el marcador de fin aparece antes que el de inicio")

    entry = build_entry(a, fields).replace("\n", nl)
    head = content[:end].rstrip("\r\n")
    updated = head + nl + nl + entry.rstrip("\r\n") + nl + nl + content[end:]
    if fields["regla"]:
        try:
            updated = add_rule_row(updated, nl, fields["regla"], a.caso)
        except ValueError as exc:
            return fail(str(exc))

    if a.dry_run:
        print(f"[dry-run] se agregaría esto a {handoff}:\n")
        print(entry)
        if fields["regla"]:
            print(f"[dry-run] y una fila en 'Reglas candidatas': {fields['regla']} | {a.caso} | candidata")
        return 0

    handoff.write_bytes((bom + updated).encode("utf-8"))
    print(f"Registrado en {handoff} ({a.fecha} · {a.caso} · {alias}).")
    if fields["regla"]:
        print("Regla candidata agregada a la tabla de la sección 5.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
