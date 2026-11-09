#!/usr/bin/env python
"""Valida un PLAN de video (tabla de planos o timeline.json) ANTES de escribir código o renderizar. Barato, sin ffmpeg.

Para qué: la mayoría de los defectos de una pieza animada nacen en el plan (planos sin objeto concreto, texto que no se alcanza a
leer, la misma cámara en cada plano, huecos en la línea de tiempo, gancho sin texto legible antes de 3 s). Verlos aquí cuesta un
segundo; verlos en el render cuesta de 4 a 20 minutos. Reglas tomadas de las ideas de huashu-art-motion, video-director y take-one
(todas MIT), reimplementadas desde cero. Los umbrales son PUNTOS DE PARTIDA de esas fuentes, sin calibrar con nuestro material:
dilo cuando reportes y ajusta con `--max-text-words`, `--max-shot`, etc. No decide si el plan es BUENO; solo atrapa lo mecánico.

Entrada 1: tabla markdown (cualquier .md con una fila de cabecera que incluya tiempo | objeto | accion; camara y texto opcionales).
  | tiempo   | objeto               | acción                    | cámara        | texto en pantalla |
  | 0-3      | una mano rasga bolsa | rasga y saca el pan       | parada        | pan con moho      |
Entrada 2: timeline.json mínimo  {"meta": {"dur": 30}, "scenes": [{"id","start","end","object","action","camera","text"}],
  "texts": [{"role": "hook|cta|term", "from": 0, "to": 3, "px": 90}]}

Uso:
  python storyboard_lint.py plan.md [--script guion.txt] [--expected-duration 54] [--max-text-words 6] [--max-shot 8] [--json salida.json]
Salida: semáforo por plano y global. Código de salida 1 si hay ROJO. «Verde» no significa «bueno», significa «sin defectos mecánicos».
"""
import argparse, json, os, re, sys, unicodedata

for _st in (sys.stdout, sys.stderr):  # Windows: consola cp1252 + tuberia; los caracteres imposibles se sustituyen en vez de lanzar UnicodeEncodeError
    try:
        _st.reconfigure(errors="replace")
    except Exception:
        pass

LAYOUT_WORDS = {"titulo", "título", "vineta", "viñeta", "viñetas", "tarjeta", "fondo", "icono", "ícono", "pantalla", "slide", "diapositiva",
                "logo", "texto", "rotulo", "rótulo", "eslogan", "frase", "cartel", "banner"}
EMPTY_OBJECTS = {"plano vacio", "plano vacío", "color liso", "negro", "fondo liso", "pantalla negra", "nada", "-", "—", ""}
WEAK_ACTIONS = {"aparece", "muestra", "se muestra", "fundido de entrada", "entra", "fade in", "fade-in", "sale", "se ve", "-", "—", ""}
TEXT_OBJECTS = ("texto", "titular", "frase", "rotulo", "rótulo", "titulo", "título", "eslogan", "cita", "lista", "viñetas", "vinetas", "cifra")
STILL = ("parada", "fija", "quieta", "estatica", "estática", "ninguna", "sin movimiento", "corte", "-", "—", "")
PUSH_IN = ("empuje", "acerca", "zoom in", "zoom-in", "push", "entra en", "acercamiento")
ACCENT = ("empuje rapido", "empuje rápido", "golpe", "latigazo", "whip", "slam", "crash zoom", "punch")


def fold(s):
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn").strip()


def parse_time(s):
    """'0-3' | '0:00-0:03' | '0.0–3.5 s' -> (ini, fin)"""
    s = s.replace("–", "-").replace("—", "-").replace("s", "").strip()
    m = re.match(r"^\s*([\d:.]+)\s*-\s*([\d:.]+)\s*$", s)
    if not m:
        return None
    def one(x):
        if ":" in x:
            p = x.split(":")
            return sum(float(v) * 60 ** (len(p) - 1 - i) for i, v in enumerate(p))
        return float(x)
    try:
        return one(m.group(1)), one(m.group(2))
    except ValueError:
        return None


def load_table(path):
    rows, header = [], None
    for line in open(path, encoding="utf-8"):
        if "|" not in line:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-{2,}:?", c) or not c for c in cells):
            continue
        names = [fold(c) for c in cells]
        if header is None:
            if any(n.startswith("tiempo") or n in ("t", "time") for n in names) and any(n.startswith("objeto") for n in names):
                header = names
            continue
        d = dict(zip(header, cells))
        def col(*keys):
            for k, v in d.items():
                if any(k.startswith(x) for x in keys):
                    return v
            return ""
        t = parse_time(col("tiempo", "t", "time"))
        rows.append({"raw_time": col("tiempo", "t", "time"), "t": t, "object": col("objeto"), "action": col("accion", "acción", "verbo"),
                     "camera": col("camara", "cámara"), "text": col("texto"), "how": col("como", "cómo")})
    if header is None:
        sys.exit("ERROR: no encontré una tabla con cabecera «tiempo | objeto | acción». Mira el formato en la cabecera del script.")
    return rows, {}


def load_json(path):
    d = json.load(open(path, encoding="utf-8"))
    rows = []
    for s in d.get("scenes", []):
        rows.append({"raw_time": f"{s.get('start')}-{s.get('end')}", "t": (s.get("start"), s.get("end")), "object": s.get("object", ""),
                     "action": s.get("action", ""), "camera": s.get("camera", ""), "text": s.get("text", ""), "how": ""})
    return rows, d


def words(t):
    return [w for w in re.split(r"\s+", t.strip()) if w]


def lint(rows, meta, opts):
    issues = []                                    # (nivel, indice o None, mensaje)
    def add(level, i, msg):
        issues.append((level, i, msg))
    prev_end = None
    total = 0.0
    n = len(rows)
    text_dominated = 0
    for i, r in enumerate(rows):
        tag = f"plano {i + 1} ({r['raw_time']})"
        if not r["t"]:
            add("ROJO", i, f"{tag}: tiempo ilegible")
            continue
        a, b = r["t"]
        d = b - a
        total += d
        if d <= 0:
            add("ROJO", i, f"{tag}: duración <= 0")
        if prev_end is not None and a - prev_end > 0.05:
            add("AMARILLO", i, f"{tag}: hueco de {a - prev_end:.2f} s respecto al plano anterior")
        if prev_end is not None and prev_end - a > 0.05:
            add("AMARILLO", i, f"{tag}: se solapa {prev_end - a:.2f} s con el anterior")
        prev_end = b
        obj, act = fold(r["object"]), fold(r["action"])
        if obj in EMPTY_OBJECTS or all(w in {fold(x) for x in LAYOUT_WORDS} for w in obj.split()):
            add("ROJO", i, f"{tag}: el objeto está vacío o es solo maquetación («{r['object']}»); nombra una COSA concreta (sustantivo)")
        if act in WEAK_ACTIONS:
            add("ROJO", i, f"{tag}: la acción es vacía o débil («{r['action']}»); nombra qué HACE el objeto (verbo)")
        tw = len(words(r["text"]))
        if tw > opts.max_text_words:
            add("ROJO", i, f"{tag}: {tw} palabras en pantalla (máx. {opts.max_text_words}); el texto no debe repetir la narración")
        if tw > 3 and d < 1.0 + 0.3 * tw:
            add("AMARILLO", i, f"{tag}: texto de {tw} palabras en {d:.1f} s; para leerse necesita >= {1.0 + 0.3 * tw:.1f} s (1 s + 0.3 s por palabra)")
        if d > opts.max_shot:
            add("ROJO", i, f"{tag}: dura {d:.1f} s (> {opts.max_shot} s): trocéalo o dale un segundo acontecimiento")
        elif d > 6:
            add("AMARILLO", i, f"{tag}: dura {d:.1f} s (6-{opts.max_shot} s: ¿pasa algo nuevo cada 2-4 s?)")
        elif 0 < d < 2 and n > 3:
            add("AMARILLO", i, f"{tag}: dura {d:.1f} s (< 2 s: ¿se alcanza a leer/entender?)")
        is_text = tw > 0 and any(k in obj for k in TEXT_OBJECTS)
        if is_text:
            text_dominated += 1
            if i in (0, n - 1):
                add("ROJO", i, f"{tag}: {'el primer' if i == 0 else 'el último'} plano está dominado por texto; abre y cierra con una acción")
        n_labels = len(re.findall(r"[;/]|\by\b", r["text"])) + (1 if r["text"] else 0)
        if n_labels > 3:
            add("AMARILLO", i, f"{tag}: más de 3 etiquetas en un plano")
    if n and text_dominated / n > 0.30:
        add("ROJO", None, f"{text_dominated} de {n} planos ({text_dominated / n:.0%}) están dominados por texto (> 30 %): se lee como diapositivas")
    # cámara
    cams = [fold(r["camera"]) for r in rows]
    def moving(c):
        return not any(c == s or c.startswith(s) for s in STILL if s)
    for i in range(n - 2):
        trio = cams[i:i + 3]
        if all(moving(c) and c == trio[0] for c in trio):
            add("AMARILLO", i + 2, f"planos {i + 1}-{i + 3}: la misma acción de cámara tres veces seguidas («{trio[0]}»); el mismo movimiento en cada plano es el mismo defecto")
        if all(any(p in c for p in PUSH_IN) for c in trio):
            add("AMARILLO", i + 2, f"planos {i + 1}-{i + 3}: tres empujes hacia dentro seguidos")
    acc = sum(1 for c in cams if any(a in c for a in ACCENT))
    if n and acc / n > 1 / 3:
        add("AMARILLO", None, f"{acc} de {n} planos usan acentos de cámara (golpe/empuje rápido/latigazo): pierden efecto si son más de 1/3")
    # duración total
    if opts.expected_duration and total and abs(total - opts.expected_duration) > max(0.5, 0.03 * opts.expected_duration):
        add("AMARILLO", None, f"duración sumada {total:.1f} s vs esperada {opts.expected_duration:.1f} s")
    # guion: números en pantalla deben existir en lo dicho
    if opts.script:
        said = fold(open(opts.script, encoding="utf-8").read())
        for i, r in enumerate(rows):
            for num in re.findall(r"\d+(?:[.,]\d+)?", r["text"]):
                if num not in said and num.replace(",", ".") not in said:
                    add("ROJO", i, f"plano {i + 1}: el número «{num}» sale en pantalla y no aparece en el guion (¿de dónde sale?). Si el guion lo dice con letras, ponlo también en cifras en el guion o confírmalo")
    # timeline.json: gancho y tamaños
    for t in meta.get("texts", []) if meta else []:
        role = t.get("role")
        if role == "hook" and (t.get("from", 0) or 0) > 3.0:
            add("ROJO", None, f"el texto del gancho aparece a los {t.get('from')} s (> 3 s)")
        floor = {"hook": 84, "cta": 48, "term": 48}.get(role)
        if floor and t.get("px") and t["px"] < floor * (min(meta.get("meta", {}).get("w", 1080), meta.get("meta", {}).get("h", 1080)) / 1080):
            add("AMARILLO", None, f"texto «{role}» de {t['px']} px < suelo orientativo {floor} px a 1080 px de lado corto")
    if meta and meta.get("texts") is not None and not any(t.get("role") == "hook" for t in meta["texts"]):
        add("AMARILLO", None, "el plan no declara un texto con rol «hook» visible antes de 3 s")
    return issues, total


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("plan")
    ap.add_argument("--script")
    ap.add_argument("--expected-duration", type=float)
    ap.add_argument("--max-text-words", type=int, default=6)
    ap.add_argument("--max-shot", type=float, default=8.0)
    ap.add_argument("--json")
    a = ap.parse_args()
    rows, meta = load_json(a.plan) if a.plan.lower().endswith(".json") else load_table(a.plan)
    issues, total = lint(rows, meta, a)
    reds = [x for x in issues if x[0] == "ROJO"]
    yel = [x for x in issues if x[0] == "AMARILLO"]
    print(f"# plan: {len(rows)} planos, {total:.1f} s sumados")
    for lvl, _, msg in issues:
        print(f"  {lvl:<8} {msg}")
    verdict = "ROJO" if reds else ("AMARILLO" if yel else "VERDE")
    print(f"VEREDICTO: {verdict} ({len(reds)} rojos, {len(yel)} amarillos). Verde = sin defectos mecánicos, no = plan bueno; umbrales sin calibrar con nuestro material.")
    if a.json:
        json.dump({"planos": len(rows), "duracion": total, "rojos": [m for _, _, m in reds], "amarillos": [m for _, _, m in yel], "veredicto": verdict},
                  open(a.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    sys.exit(1 if reds else 0)


if __name__ == "__main__":
    main()
