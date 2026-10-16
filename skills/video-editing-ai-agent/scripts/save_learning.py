#!/usr/bin/env python
"""Biblioteca de aprendizajes sacados de videos de referencia: candidato -> aprobado, con evidencia.

Regla (de tus reglas globales de diseno): una observacion de UNA fuente es solo un CANDIDATO. Se promueve a regla
unicamente (a) con aprobacion explicita del usuario, citando sus palabras, o (b) si se repite en >= 3 fuentes DISTINTAS.
Nada de eso lo decide el script por su cuenta: exige la cita o los ids que lo justifican.

Uso:
  python save_learning.py add --source URL_o_ruta --when "situacion" --do "accion con rango/valor" --evidence "#12 00:23; 2.1 s/plano"
                              [--type medido|visto|inferido] [--tags ritmo,gancho] [--scope general|proyecto:NOMBRE]
  python save_learning.py list [--estado candidato|aprobado|rechazado] [--tag t]
  python save_learning.py show ID
  python save_learning.py promote ID --by usuario --quote "palabras textuales del usuario"
  python save_learning.py promote ID --by repeticion --with ID2,ID3 --why "por que son el mismo aprendizaje"
  python save_learning.py reject ID --why "motivo"
Archivos (carpeta de memoria: $VEA_MEMORY_DIR, o memoria/ de la skill, relativa a este script): aprendizajes.jsonl (fuente de verdad) y aprendizajes.md (vista).
"""
import argparse, datetime, hashlib, json, os, re, sys

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import memory_dir  # noqa: E402
MEM = memory_dir()
JSONL = os.path.join(MEM, "aprendizajes.jsonl")
MD = os.path.join(MEM, "aprendizajes.md")


def load():
    if not os.path.exists(JSONL):
        return []
    return [json.loads(l) for l in open(JSONL, encoding="utf-8") if l.strip()]


def save(rows):
    os.makedirs(MEM, exist_ok=True)
    with open(JSONL, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    render(rows)


def source_key(src):
    m = re.search(r"(?:v=|youtu\.be/|shorts/)([\w-]{11})", src)
    if m:
        return "yt_" + m.group(1)
    if re.match(r"^https?://", src):
        return "web_" + hashlib.sha1(src.split("?")[0].encode()).hexdigest()[:8]
    return "file_" + hashlib.sha1(os.path.basename(src).lower().encode()).hexdigest()[:8]


def render(rows):
    L = ["# Aprendizajes de videos de referencia", "",
         "> Vista generada por `scripts/save_learning.py` (fuente de verdad: `aprendizajes.jsonl`). **Candidato** = una observación de una sola fuente, sin validar. "
         "**Aprobado** = aprobado por el usuario (con su cita) o repetido en ≥ 3 fuentes distintas. No editar a mano.", ""]
    for estado, titulo in (("aprobado", "Aprobados"), ("candidato", "Candidatos (sin validar)"), ("rechazado", "Rechazados")):
        sel = [r for r in rows if r["estado"] == estado]
        L += [f"## {titulo} ({len(sel)})", ""]
        for r in sel:
            hip = " _(hipótesis)_" if r["tipo"] == "inferido" else ""
            L.append(f"- **{r['id']}** · {r['fecha']} · `{r['ambito']}` · {', '.join(r['etiquetas']) or 'sin etiquetas'}{hip}")
            L.append(f"  - **Cuando** {r['cuando']} → **hacer** {r['hacer']}")
            L.append(f"  - Evidencia ({r['tipo']}): {r['evidencia']} — fuente: {r['fuente']}")
            if r.get("aprobado_por"):
                L.append(f"  - Aprobado: {r['aprobado_por']}" + (f" — «{r['cita']}»" if r.get("cita") else "") + (f" (con {', '.join(r['con'])}: {r.get('porque', '')})" if r.get("con") else ""))
            if r.get("rechazo"):
                L.append(f"  - Rechazado: {r['rechazo']}")
        L.append("")
    os.makedirs(MEM, exist_ok=True)
    open(MD, "w", encoding="utf-8").write("\n".join(L))


def find(rows, i):
    for r in rows:
        if r["id"] == i:
            return r
    sys.exit(f"no existe el aprendizaje {i}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a_ = sub.add_parser("add")
    a_.add_argument("--source", required=True); a_.add_argument("--when", required=True); a_.add_argument("--do", required=True)
    a_.add_argument("--evidence", required=True); a_.add_argument("--type", default="visto", choices=["medido", "visto", "inferido"])
    a_.add_argument("--tags", default=""); a_.add_argument("--scope", default="general")
    l_ = sub.add_parser("list"); l_.add_argument("--estado"); l_.add_argument("--tag")
    s_ = sub.add_parser("show"); s_.add_argument("id")
    p_ = sub.add_parser("promote"); p_.add_argument("id"); p_.add_argument("--by", required=True, choices=["usuario", "repeticion"])
    p_.add_argument("--quote"); p_.add_argument("--with", dest="with_"); p_.add_argument("--why")
    r_ = sub.add_parser("reject"); r_.add_argument("id"); r_.add_argument("--why", required=True)
    a = ap.parse_args()
    rows = load()

    if a.cmd == "add":
        if len(a.evidence.strip()) < 6:
            sys.exit("--evidence es obligatoria y concreta (fotograma/tiempo o cifra medida)")
        nid = f"A{len(rows) + 1:03d}"
        rows.append({"id": nid, "fecha": datetime.date.today().isoformat(), "estado": "candidato", "fuente": a.source,
                     "fuente_clave": source_key(a.source), "ambito": a.scope, "etiquetas": [t.strip() for t in a.tags.split(",") if t.strip()],
                     "cuando": a.when.strip(), "hacer": a.do.strip(), "evidencia": a.evidence.strip(), "tipo": a.type})
        save(rows)
        print(f"guardado {nid} como CANDIDATO (una sola fuente: no es una regla). Vista: {MD}")
    elif a.cmd == "list":
        sel = [r for r in rows if (not a.estado or r["estado"] == a.estado) and (not a.tag or a.tag in r["etiquetas"])]
        for r in sel:
            print(f"{r['id']} [{r['estado']}] ({r['tipo']}) {r['fuente_clave']}: cuando {r['cuando']} -> {r['hacer']}")
        print(f"{len(sel)} de {len(rows)}")
    elif a.cmd == "show":
        print(json.dumps(find(rows, a.id), ensure_ascii=False, indent=1))
    elif a.cmd == "promote":
        r = find(rows, a.id)
        if r["estado"] == "aprobado":
            sys.exit("ya esta aprobado")
        if a.by == "usuario":
            if not a.quote or len(a.quote.strip()) < 4:
                sys.exit("Aprobar 'por usuario' exige --quote con sus palabras textuales (no se promueve por suposicion).")
            r.update({"estado": "aprobado", "aprobado_por": "usuario", "cita": a.quote.strip()})
        else:
            ids = [x.strip() for x in (a.with_ or "").split(",") if x.strip()]
            others = [find(rows, i) for i in ids]
            keys = {r["fuente_clave"]} | {o["fuente_clave"] for o in others}
            if len(keys) < 3:
                sys.exit(f"Promover por repeticion exige >= 3 fuentes DISTINTAS (hay {len(keys)}). Ese aprendizaje sigue siendo candidato.")
            if not a.why or len(a.why.strip()) < 10:
                sys.exit("--why debe explicar por que son el mismo aprendizaje (la equivalencia la afirmas tu, queda registrada).")
            r.update({"estado": "aprobado", "aprobado_por": "repeticion", "con": ids, "porque": a.why.strip()})
        save(rows)
        print(f"{a.id} -> APROBADO por {r['aprobado_por']}")
    elif a.cmd == "reject":
        r = find(rows, a.id)
        r.update({"estado": "rechazado", "rechazo": a.why.strip()})
        save(rows)
        print(f"{a.id} -> RECHAZADO")


if __name__ == "__main__":
    main()
