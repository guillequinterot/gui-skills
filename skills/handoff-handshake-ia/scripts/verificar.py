#!/usr/bin/env python3
"""Comprueba el formato de continuidad. Estados y orden son heurísticas, no semántica.

Solo detecta líneas Estado: y fechas ISO en filas o encabezados cuando se declara
«más nuevo arriba». Las rutas se detectan por separador o extensión en comillas invertidas; pueden existir falsos positivos y omisiones. La fecha se comprueba por formato, no por validez de calendario. Los comentarios HTML no cuentan para el tope.
"""
import argparse
import json
import re
from pathlib import Path

FIELDS = ("De", "Para", "Objetivo", "Hecho y rutas de evidencia", "Último trabajo real", "Falta", "No consta", "Skills a cargar", "QA cumplimiento", "QA calidad")

def revisar(root, tope=None, rutas=False, combinado=None):
    out = []
    def add(level, msg): out.append({"nivel": level, "mensaje": msg})
    texts = {}
    names = (str(combinado),) if combinado is not None else ("HANDSHAKE.md", "HANDOFF.md")
    for name in names:
        path = root / name
        if not path.is_file():
            add("BLOQUEA", "Falta " + name)
            texts[name] = ""
        else:
            texts[name] = path.read_text(encoding="utf-8")
    hs = texts[names[0]]
    ho = "" if combinado is not None else texts["HANDOFF.md"]
    if combinado is not None: add("AVISA", "Archivo combinado: conviene separar HANDOFF y HANDSHAKE")
    marker = re.search(r'<!--\s*handshake-tope:\s*(\d+)\s*-->', hs, re.I)
    limit = tope if tope is not None else int(marker.group(1)) if marker else 150
    sin_comentarios = re.sub(r'(?m)^[ \t]*<!--(?:(?!-->).)*-->[ \t]*(?:\r?\n|$)', '', hs, flags=re.S)
    if len(sin_comentarios.splitlines()) > limit: add("BLOQUEA", "HANDSHAKE supera el tope de %s líneas" % limit)
    for key, pattern in (("fecha", r'^Fecha:[ \t]*\d{4}-\d{2}-\d{2}(?:T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2}))?(?=$|[ \t])'), ("firma", r'^Firma:[ \t]*(?!NO CONSTA[ \t]*$)\S')):
        if not re.search(pattern, hs, re.I | re.M): add("BLOQUEA", "Falta " + key + " en estado")
    if combinado is None:
        for field in FIELDS:
            if not re.search(r'^' + re.escape(field) + r':[ \t]*\S', ho, re.I | re.M): add("BLOQUEA", "Falta campo " + field)
    for field in ("Último trabajo real", "Contradicciones y qué manda"):
        if not re.search(r'^' + re.escape(field) + r':[ \t]*\S', hs, re.I | re.M): add("AVISA", "Falta campo " + field + " en estado")
    if len(ho.splitlines()) > 80: add("AVISA", "Ficha supera 80 líneas")
    for field in ("Objetivo", "Estado", "Próximo paso"):
        if re.search(r'^' + re.escape(field) + r':[ 	]*NO CONSTA[ 	]*$', hs, re.I | re.M): add("AVISA", "Campo sin rellenar en estado: " + field)
    a = re.search(r'^Estado:\s*(.+)$', hs, re.I | re.M)
    if a and len(a.group(1).strip()) > 200: add("AVISA", "Estado supera 200 caracteres; revisar si es una frase citable")
    b = re.search(r'^Estado:\s*(.+)$', ho, re.I | re.M)
    if a and b and a.group(1).strip().casefold() != b.group(1).strip().casefold(): add("AVISA", "Estado duplicado con texto distinto; revisar")
    # Convención opcional: ID: clave | Estado: valor, una entrada por línea.
    def estados_id(content):
        pairs = re.findall(r'^ID:\s*([^|\n]+)\s*\|\s*Estado:\s*(.+)$', content, re.I | re.M)
        return {key.strip().casefold(): value.strip().casefold() for key, value in pairs}
    ids_a, ids_b = estados_id(hs), estados_id(ho)
    for key in ids_a.keys() & ids_b.keys():
        if ids_a[key] != ids_b[key]: add("AVISA", "ID con estados distintos: " + key)
    for name, content in texts.items():
        if re.search(r'm[aá]s nuevo arriba', content, re.I):
            dates = re.findall(r'^(?:#{1,6}\s*|\|\s*)(\d{4}-\d{2}-\d{2})', content, re.M)
            if dates != sorted(dates, reverse=True): add("AVISA", name + ": orden de fechas no descendente")
        if rutas:
            for value in re.findall(r'`([^`\n]+)`', content):
                if ('/' in value or chr(92) in value or re.search(r'\.[A-Za-z0-9]{1,8}$', value)) and not (root / value.replace(chr(92), '/')).exists(): add("BLOQUEA", name + ": ruta inexistente " + value)
    if not out: add("OK", "Sin hallazgos automáticos")
    return out

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("proyecto", type=Path)
    parser.add_argument("--tope", type=int)
    parser.add_argument("--rutas", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--combinado", type=Path, help="archivo combinado relativo al proyecto o ruta absoluta")
    args = parser.parse_args()
    if args.tope is not None and args.tope < 1: parser.error("--tope debe ser positivo")
    try: result = revisar(args.proyecto, args.tope, args.rutas, args.combinado)
    except (OSError, UnicodeError) as exc: result = [{"nivel": "BLOQUEA", "mensaje": str(exc)}]
    if args.json: print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for item in result: print(item["nivel"] + ": " + item["mensaje"])
    return int(any(item["nivel"] == "BLOQUEA" for item in result))

if __name__ == "__main__":
    raise SystemExit(main())
