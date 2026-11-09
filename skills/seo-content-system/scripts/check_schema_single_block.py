#!/usr/bin/env python3
"""Puerta OBLIGATORIA de schema: la página debe tener UN solo bloque JSON-LD con @graph.

Qué comprueba (sobre una URL pública o un archivo HTML guardado):
  1. Exactamente UN `<script type="application/ld+json">` (ni cero ni varios: nada de bloques sueltos por tipo).
  2. Que su JSON sea válido y traiga `@graph` (lista de nodos).
  3. Que todo nodo tenga `@id` y que no se repita.
  4. Que toda referencia `{"@id": "..."}` (en cualquier nivel) apunte a un nodo definido en el mismo grafo.
  5. Que no haya dos nodos del mismo tipo "único" (Organization, WebSite, WebPage, BreadcrumbList, Person, Article/BlogPosting).

Uso:
  python check_schema_single_block.py https://ejemplo.com/articulo/
  python check_schema_single_block.py pagina-guardada.html
  python check_schema_single_block.py cuerpo-del-articulo.html --cuerpo      # fuente antes de fundirse con el SEO plugin
  python check_schema_single_block.py URL --json                              # salida para máquinas

`--cuerpo`: el artículo todavía no incluye los nodos que añade el plugin de SEO (WebPage, Organization…). Las referencias a esos @id
(`#webpage`, `#organization`, `#website`, `#person`, `#breadcrumb`, `#primaryImage`) se aceptan como externas. En la página final (sin `--cuerpo`)
todas las referencias deben resolverse dentro del mismo bloque.
Salida: 0 si pasa, 1 si falla, 2 si no se pudo leer. Solo biblioteca estándar. No ejecuta JavaScript: lee el HTML tal como lo sirve el servidor."""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request

RE_BLOQUE = re.compile(r'<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', re.S | re.I)
UNICOS = ("Organization", "WebSite", "WebPage", "BreadcrumbList", "Person")
ARTICULO = ("Article", "BlogPosting", "NewsArticle")
EXTERNOS_OK = ("#webpage", "#organization", "#website", "#person", "#breadcrumb", "#primaryimage", "#richsnippet", "#place")


def leer(fuente: str) -> str:
    if re.match(r"https?://", fuente):
        req = urllib.request.Request(fuente, headers={"User-Agent": "Mozilla/5.0 (compatible; schema-check/1.0)"})
        return urllib.request.urlopen(req, timeout=40).read().decode("utf-8", "ignore")
    with open(fuente, encoding="utf-8", errors="ignore") as f:
        return f.read()


def tipos(n: dict) -> list:
    t = n.get("@type")
    return t if isinstance(t, list) else [t]


def referencias(obj, acc=None):
    """Referencias puras {"@id": "..."} (un objeto cuya única clave es @id) en cualquier nivel."""
    acc = [] if acc is None else acc
    if isinstance(obj, dict):
        if set(obj.keys()) == {"@id"} and isinstance(obj["@id"], str):
            acc.append(obj["@id"])
        for v in obj.values():
            referencias(v, acc)
    elif isinstance(obj, list):
        for v in obj:
            referencias(v, acc)
    return acc


def revisar(html: str, cuerpo: bool = False) -> dict:
    bloques = RE_BLOQUE.findall(html)
    fallos, avisos, nodos = [], [], []
    if len(bloques) != 1:
        fallos.append(f"hay {len(bloques)} bloques JSON-LD (debe haber exactamente 1)")
    jsons = []
    for i, b in enumerate(bloques, 1):
        try:
            jsons.append(json.loads(b))
        except Exception as e:  # noqa: BLE001
            fallos.append(f"el bloque {i} no es JSON válido: {e}")
    for j in jsons:
        g = j.get("@graph") if isinstance(j, dict) else None
        if not isinstance(g, list) or not g:
            fallos.append("un bloque no usa @graph (lista de nodos)")
        else:
            nodos += [n for n in g if isinstance(n, dict)]
    ids = [n.get("@id") for n in nodos]
    sin_id = [tipos(n) for n in nodos if not n.get("@id")]
    if sin_id:
        fallos.append(f"nodos sin @id: {sin_id}")
    dup = sorted({i for i in ids if i and ids.count(i) > 1})
    if dup:
        fallos.append(f"@id repetidos: {dup}")
    definidos = {i for i in ids if i}
    sueltas = []
    for r in referencias(nodos):
        if r in definidos:
            continue
        if cuerpo and r.lower().endswith(EXTERNOS_OK) or (cuerpo and any(r.lower().endswith(x) for x in EXTERNOS_OK)):
            continue
        sueltas.append(r)
    if sueltas:
        fallos.append(f"referencias a @id que no están definidos en el grafo: {sorted(set(sueltas))}")
    for t in UNICOS:
        n = sum(1 for x in nodos if t in tipos(x))
        if n > 1:
            fallos.append(f"hay {n} nodos {t} (debe haber uno)")
    if sum(1 for x in nodos if any(a in tipos(x) for a in ARTICULO)) > 1:
        fallos.append("hay más de un nodo Article/BlogPosting")
    if not nodos and len(bloques) == 1:
        avisos.append("el bloque no trae nodos")
    return {"bloques": len(bloques), "nodos": [tipos(n) for n in nodos], "fallos": fallos, "avisos": avisos, "pasa": not fallos}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # con `python -I` no se leen las variables PYTHON*
    except Exception:  # noqa: BLE001
        pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("fuente", help="URL pública o archivo .html")
    ap.add_argument("--cuerpo", action="store_true", help="fuente del artículo antes de fundirse con el plugin de SEO")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    try:
        html = leer(a.fuente)
    except Exception as e:  # noqa: BLE001
        print(f"ERROR no pude leer {a.fuente}: {e}")
        return 2
    r = revisar(html, a.cuerpo)
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=1))
    else:
        print(f"{'PASA' if r['pasa'] else 'FALLA'} · {r['bloques']} bloque(s) JSON-LD · nodos: {r['nodos']}")
        for f in r["fallos"]:
            print("  ✗", f)
        for x in r["avisos"]:
            print("  !", x)
    return 0 if r["pasa"] else 1


if __name__ == "__main__":
    sys.exit(main())
