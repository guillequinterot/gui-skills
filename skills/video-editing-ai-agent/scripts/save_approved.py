#!/usr/bin/env python
"""Biblioteca de VIDEOS APROBADOS por el usuario: de cada pieza que el usuario aprueba se guarda la receta, lo bueno, lo malo y lo que quedó sin decidir.

Idea (Guille, mantenedor, 2026-10-16): «cada video aprobado: a futuro aprendas de eso». Un video aprobado es la evidencia más fuerte que hay de lo que le gusta
(más que una regla escrita), pero **una receta es una recomendación que nombra su origen, nunca una orden** (production-workflow.md §4, memoria).
Reglas:
  - `add` EXIGE la cita textual del usuario que aprueba (--quote). Sin cita no se guarda: no se aprueba por suposición.
  - Lo que el usuario NO aprobó o no eligió va en --open (p. ej. «con o sin empuje de cámara»); queda marcado «sin decidir» y no se usa como preferencia.
  - Lo malo (--bad) se guarda con su costo y su evidencia; las lecciones generales van además a references/errores-conocidos-y-aciertos.md.
  - Al empezar una pieza nueva: `suggest` (misma ruta/formato/etiquetas) y leer `recipe ID`; al cerrar una pieza aprobada: `add`.

Uso:
  python save_approved.py add --name "Reel caso-reel-01" --project RUTA --piece "Reel Instagram 9:16" --format 1080x1920 --duration 29.9
        --route musica-al-compas --engine hyperframes --message "una frase" --quote "palabras textuales del usuario"
        --approved "textos en ingles" --approved "estructura" --open "con o sin empuje de camara"
        --structure "hero > proceso > alcance > tension > drop > funcion > CTA" --recipe "B(n)=t0+T*n; push 0.6 s ..."
        --good "..." --bad "... (costo)" --metrics "-15.3 LUFS; hueco 0 %" --tags reel,musica,fotos [--files ruta1 --files ruta2]
  python save_approved.py list [--tag t]
  python save_approved.py show ID
  python save_approved.py recipe ID            # resumen listo para leer al empezar una pieza parecida
  python save_approved.py suggest [--route r] [--format f] [--tag t]
Archivos (carpeta de memoria: $VEA_MEMORY_DIR, o memoria/ de la skill, relativa a este script): videos-aprobados.jsonl (fuente de verdad) y videos-aprobados.md (vista; no editar a mano).
"""
import argparse, datetime, json, os, sys

try:
    sys.stdout.reconfigure(errors="replace")
except Exception:  # noqa
    pass

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import memory_dir  # noqa: E402
MEM = memory_dir()
JSONL = os.path.join(MEM, "videos-aprobados.jsonl")
MD = os.path.join(MEM, "videos-aprobados.md")


def load():
    if not os.path.exists(JSONL):
        return []
    return [json.loads(l) for l in open(JSONL, encoding="utf-8") if l.strip()]


def render(rows):
    L = ["# Videos aprobados por el usuario", "",
         "> Vista generada por `scripts/save_approved.py` (fuente de verdad: `videos-aprobados.jsonl`). Cada entrada lleva la **cita textual** con la que el usuario aprobó. "
         "Una receta es una **recomendación que nombra su origen**, no una orden; lo «sin decidir» no es una preferencia. No editar a mano.", ""]
    for r in rows:
        L += [f"## {r['id']} · {r['nombre']} · {r['fecha']}", "",
              f"- **Pieza:** {r['pieza']} · {r['formato']} · {r['duracion']} s · ruta `{r['ruta']}` · motor {r['motor']} · proyecto `{r['proyecto']}`",
              f"- **Mensaje:** {r['mensaje']}",
              f"- **Aprobado por {r['aprobado_por']}:** «{r['cita']}»",
              f"- **Aprobado explícitamente:** {'; '.join(r['aprobado']) or '(no se detalló: aprobación general de la pieza)'}",
              f"- **Sin decidir (no usar como preferencia):** {'; '.join(r['sin_decidir']) or 'nada'}",
              f"- **Estructura:** {r['estructura']}",
              f"- **Receta:** {r['receta']}",
              f"- **Medido:** {r['medido']}", "", "**Lo bueno (repetir)**"]
        L += [f"- {x}" for x in r["bueno"]] or ["- (nada registrado)"]
        L += ["", "**Lo malo (evitar)**"]
        L += [f"- {x}" for x in r["malo"]] or ["- (nada registrado)"]
        if r["archivos"]:
            L += ["", "**Archivos:** " + "; ".join(f"`{x}`" for x in r["archivos"])]
        L += ["", f"Etiquetas: {', '.join(r['etiquetas']) or '—'}", ""]
    os.makedirs(MEM, exist_ok=True)
    open(MD, "w", encoding="utf-8").write("\n".join(L))


def save(rows):
    os.makedirs(MEM, exist_ok=True)
    with open(JSONL, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    render(rows)


def find(rows, i):
    for r in rows:
        if r["id"].lower() == i.lower():
            return r
    sys.exit(f"no existe el video aprobado {i}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a_ = sub.add_parser("add")
    a_.add_argument("--name", required=True); a_.add_argument("--project", required=True); a_.add_argument("--piece", required=True)
    a_.add_argument("--format", required=True); a_.add_argument("--duration", type=float, required=True)
    a_.add_argument("--route", required=True); a_.add_argument("--engine", required=True)
    a_.add_argument("--message", required=True); a_.add_argument("--quote", required=True, help="palabras textuales del usuario que aprueba")
    a_.add_argument("--by", default="usuario")
    a_.add_argument("--approved", action="append", default=[]); a_.add_argument("--open", action="append", default=[])
    a_.add_argument("--structure", required=True); a_.add_argument("--recipe", required=True)
    a_.add_argument("--good", action="append", default=[]); a_.add_argument("--bad", action="append", default=[])
    a_.add_argument("--metrics", default=""); a_.add_argument("--tags", default="")
    a_.add_argument("--files", action="append", default=[])
    l_ = sub.add_parser("list"); l_.add_argument("--tag")
    s_ = sub.add_parser("show"); s_.add_argument("id")
    r_ = sub.add_parser("recipe"); r_.add_argument("id")
    g_ = sub.add_parser("suggest"); g_.add_argument("--route"); g_.add_argument("--format"); g_.add_argument("--tag")
    a = ap.parse_args()
    rows = load()

    if a.cmd == "add":
        if len(a.quote.strip()) < 4:
            sys.exit("--quote es obligatoria: las palabras textuales del usuario al aprobar. Sin cita no se guarda (no se aprueba por suposición).")
        if not a.good and not a.bad:
            sys.exit("Registra al menos una lección: --good y/o --bad (con evidencia o costo). Sin lecciones no hay nada que aprender.")
        nid = f"V{len(rows) + 1:03d}"
        rows.append({"id": nid, "fecha": datetime.date.today().isoformat(), "nombre": a.name.strip(), "proyecto": a.project, "pieza": a.piece,
                     "formato": a.format, "duracion": a.duration, "ruta": a.route, "motor": a.engine, "mensaje": a.message.strip(),
                     "aprobado_por": a.by, "cita": a.quote.strip(), "aprobado": [x.strip() for x in a.approved], "sin_decidir": [x.strip() for x in a.open],
                     "estructura": a.structure.strip(), "receta": a.recipe.strip(), "bueno": [x.strip() for x in a.good], "malo": [x.strip() for x in a.bad],
                     "medido": a.metrics.strip(), "etiquetas": [t.strip().lower() for t in a.tags.split(",") if t.strip()], "archivos": a.files})
        save(rows)
        print(f"guardado {nid} · {a.name} (aprobado por {a.by}). Vista: {MD}")
    elif a.cmd == "list":
        sel = [r for r in rows if not a.tag or a.tag.lower() in r["etiquetas"]]
        for r in sel:
            print(f"{r['id']} · {r['fecha']} · {r['nombre']} · {r['formato']} · {r['duracion']} s · {r['ruta']} · {', '.join(r['etiquetas'])}")
        print(f"{len(sel)} de {len(rows)}")
    elif a.cmd == "show":
        print(json.dumps(find(rows, a.id), ensure_ascii=False, indent=1))
    elif a.cmd == "recipe":
        r = find(rows, a.id)
        print(f"RECETA {r['id']} · {r['nombre']} (aprobada por {r['aprobado_por']} el {r['fecha']}: «{r['cita']}»)")
        print("Recomendación con origen conocido, no una orden. Lo «sin decidir» NO es preferencia.")
        print(f"Estructura: {r['estructura']}\nReceta: {r['receta']}\nMedido: {r['medido']}")
        print("Aprobado:", "; ".join(r["aprobado"]) or "(general)")
        print("Sin decidir:", "; ".join(r["sin_decidir"]) or "nada")
        print("Repetir:", *[f"\n  + {x}" for x in r["bueno"]])
        print("Evitar:", *[f"\n  - {x}" for x in r["malo"]])
    elif a.cmd == "suggest":
        sel = []
        for r in rows:
            score = 2 * bool(a.route and r["ruta"] == a.route) + bool(a.format and r["formato"] == a.format) + 2 * bool(a.tag and a.tag.lower() in r["etiquetas"])
            if score:
                sel.append((score, r))
        if not sel:
            print("Ningún video aprobado coincide: empieza desde `production-workflow.md` y `errores-conocidos-y-aciertos.md`.")
        for score, r in sorted(sel, key=lambda t: -t[0]):
            print(f"{r['id']} (coincidencia {score}) · {r['nombre']} · {r['formato']} · {r['ruta']} → `python scripts/save_approved.py recipe {r['id']}`")


if __name__ == "__main__":
    main()
