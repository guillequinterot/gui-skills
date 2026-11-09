#!/usr/bin/env python
"""Alinea un GUION (texto hablado) con los tiempos por palabra de una transcripción y mide cuánto coinciden.

Para qué: la transcripción de Whisper acierta los TIEMPOS pero se equivoca en nombres, cifras y siglas; el guion tiene las palabras
correctas pero no tiene tiempos. Este script las une con programación dinámica (distancia de edición entre lo que se quería decir y lo
que se oyó) y entrega, por cada palabra del guion: el texto mostrado, el hablado, inicio, fin y si se confirmó con el oído.
Es la idea de explainroo (MIT) reimplementada aquí desde cero, sin copiar su código.

Sintaxis del guion (texto plano o .md):
  [#nombre]          marcador: toma el inicio de la palabra siguiente (o el fin de la última si va al final)
  [pause 0.6]        pausa (solo se anota; no se alinea)
  {mostrado|hablado} lo que se ve en pantalla es distinto de lo que se dice: {20|veinte}, {API|a pe i}, {SQL|sécuel}
  > nota             línea ignorada
  Las cifras enteras (0 a 999 999, con o sin puntos de miles, y con «%») se leen solas en español, tanto en el guion como en lo que oyó Whisper
  («35» = treinta y cinco). Decimales, fechas, siglas y URL se escriben en su forma HABLADA o con {mostrado|hablado}.

Uso:
  python align_script.py guion.txt words.json [--key clip.mp4] [-o guion-words.json] [--srt guion.srt]
  words.json es la salida de transcribe_words.py: {"clip.mp4": [{"s":0.0,"e":0.4,"w":"Hola"}, ...]}

Control de calidad que imprime (mide, no oye):
  matchRate         fracción de palabras habladas confirmadas por el oído; < 0.85 = revisa el guion o el audio (< 0.5: archivo equivocado)
  sin_confirmar     palabras habladas que Whisper no oyó o oyó distinto (sus tiempos se interpolan, NO son medidos)
  palabras largas   una palabra con duración > 1.2 s suele ser un tiempo estirado sobre un silencio: comprueba con la forma de onda
Una palabra de varias partes solo cuenta como confirmada si se oyeron todas.
"""
import argparse, json, os, re, sys, unicodedata

for _st in (sys.stdout, sys.stderr):  # Windows: consola cp1252 + tuberia; los caracteres imposibles se sustituyen en vez de lanzar UnicodeEncodeError
    try:
        _st.reconfigure(errors="replace")
    except Exception:
        pass

TOKEN = re.compile(r"\[#([\w-]+)\]|\[pause\s+([\d.]+)\]|\{([^|}]+)\|([^}]+)\}|([^\s\[\]{}]+)", re.U)
SIM = 0.34        # distancia de edición / longitud máxima para considerar dos palabras «la misma»
SUB_COST = 1.6
MIN_DUR = 0.05


def fold(w):
    w = unicodedata.normalize("NFD", w.lower())
    w = "".join(c for c in w if unicodedata.category(c) != "Mn")
    return re.sub(r"[^\w]", "", w, flags=re.U)


_U = ["cero", "uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve", "diez", "once", "doce", "trece", "catorce", "quince",
      "dieciseis", "diecisiete", "dieciocho", "diecinueve", "veinte", "veintiuno", "veintidos", "veintitres", "veinticuatro", "veinticinco",
      "veintiseis", "veintisiete", "veintiocho", "veintinueve"]
_D = {3: "treinta", 4: "cuarenta", 5: "cincuenta", 6: "sesenta", 7: "setenta", 8: "ochenta", 9: "noventa"}
_C = ["", "ciento", "doscientos", "trescientos", "cuatrocientos", "quinientos", "seiscientos", "setecientos", "ochocientos", "novecientos"]


def num_es(n):
    """Palabras (sin tildes, como las compara `fold`) de un entero 0..999999 en español: 35 -> [treinta, y, cinco]; 2026 -> [dos, mil, veintiseis]."""
    if n < 30:
        return [_U[n]]
    if n < 100:
        d, u = divmod(n, 10)
        return [_D[d]] + (["y", _U[u]] if u else [])
    if n == 100:
        return ["cien"]
    if n < 1000:
        c, r = divmod(n, 100)
        return [_C[c]] + (num_es(r) if r else [])
    m, r = divmod(n, 1000)
    head = ["mil"] if m == 1 else num_es(m) + ["mil"]
    return head + (num_es(r) if r else [])


def expand_digits(raw):
    """«35», «1.000», «5%» -> lista de palabras habladas en español; None si no es una cifra entera que sepamos leer (decimales, fechas...)."""
    t = raw.strip().strip(".,;:!?¿¡()\"'")
    pct = t.endswith("%")
    t = t.rstrip("%")
    if re.fullmatch(r"\d{1,3}([.,]\d{3})+", t):
        t = re.sub(r"[.,]", "", t)
    if not re.fullmatch(r"\d{1,6}", t):
        return None
    out = num_es(int(t))
    return out + (["por", "ciento"] if pct else [])


def lev(a, b):
    if a == b:
        return 0
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def near_exact(a, b):
    """Para unir dos palabras en una (p. ej. «example» + «com»): casi idénticas, no solo parecidas."""
    return bool(a) and bool(b) and (a == b or lev(a, b) / max(len(a), len(b)) <= 0.15)


def similar(a, b):
    if not a or not b:
        return False
    if a == b:
        return True
    if min(len(a), len(b)) <= 3:
        return False
    return lev(a, b) / max(len(a), len(b)) <= SIM


def parse_script(text):
    """-> tokens [{shown, spoken:[...], marks:[...]}], pausas. Una pareja {mostrado|hablado} es UN token con varias palabras habladas."""
    toks, pending, pauses = [], [], []
    for line in text.splitlines():
        if line.lstrip().startswith(">") or line.lstrip().startswith("#"):
            continue
        for m in TOKEN.finditer(line):
            if m.group(1):
                pending.append(m.group(1))
            elif m.group(2):
                pauses.append({"after_token": len(toks) - 1, "s": float(m.group(2))})
            elif m.group(3):
                sp = [fold(x) for x in m.group(4).split() if fold(x)]
                if sp:
                    toks.append({"shown": m.group(3).strip(), "spoken": sp, "marks": pending}); pending = []
            else:
                ex = expand_digits(m.group(5))
                f = fold(m.group(5))
                if ex:
                    toks.append({"shown": m.group(5), "spoken": ex, "marks": pending}); pending = []
                elif f:
                    toks.append({"shown": m.group(5), "spoken": [f], "marks": pending}); pending = []
    return toks, pauses, pending


def align(spoken, heard):
    """DP entre palabras habladas S y oídas H. Devuelve, por palabra hablada, el índice de la(s) oída(s) o None."""
    n, m = len(spoken), len(heard)
    INF = 1e9
    dp = [[INF] * (m + 1) for _ in range(n + 1)]
    bk = [[None] * (m + 1) for _ in range(n + 1)]
    dp[0][0] = 0.0
    for i in range(n + 1):
        for j in range(m + 1):
            c = dp[i][j]
            if c >= INF:
                continue
            def go(i2, j2, cost, mv):
                if i2 <= n and j2 <= m and c + cost < dp[i2][j2] - 1e-9:
                    dp[i2][j2] = c + cost; bk[i2][j2] = (i, j, mv)
            if i < n and j < m:
                go(i + 1, j + 1, 0.0 if similar(spoken[i], heard[j]) else SUB_COST, "m" if similar(spoken[i], heard[j]) else "x")
            if i < n:
                go(i + 1, j, 1.0, "s")                      # palabra hablada que no se oyó
            if j < m:
                go(i, j + 1, 1.0, "h")                      # palabra oída que no estaba en el guion
            if i < n and j + 1 < m and near_exact(spoken[i], heard[j] + heard[j + 1]):
                go(i + 1, j + 2, 0.0, "m2")                 # una hablada = dos oídas («example» «com»)
            if i + 1 < n and j < m and near_exact(spoken[i] + spoken[i + 1], heard[j]):
                go(i + 2, j + 1, 0.0, "2m")                 # dos habladas = una oída
    res = [None] * n
    i, j = n, m
    while (i, j) != (0, 0):
        pi, pj, mv = bk[i][j]
        if mv == "m":
            res[pi] = (pj, pj)
        elif mv == "m2":
            res[pi] = (pj, pj + 1)
        elif mv == "2m":
            res[pi] = res[pi + 1] = (pj, pj)
        i, j = pi, pj
    return res


def build(script_text, heard_words):
    toks, pauses, tail_marks = parse_script(script_text)
    spoken, owner = [], []
    for ti, t in enumerate(toks):
        for w in t["spoken"]:
            spoken.append(w); owner.append(ti)
    hw, ref = [], []
    for h in heard_words:
        ex = expand_digits(h["w"])
        if ex and len(ex) > 1:                    # «35» -> treinta y cinco: reparte el tiempo por longitud
            tot = sum(len(x) for x in ex)
            cur = h["s"]
            for x in ex:
                d = (h["e"] - h["s"]) * len(x) / tot
                hw.append(x); ref.append({"s": cur, "e": cur + d, "w": x}); cur += d
        else:
            f = ex[0] if ex else fold(h["w"])
            if f:
                hw.append(f); ref.append(h)
    pairs = align(spoken, hw)
    s_t, e_t, ok = [None] * len(spoken), [None] * len(spoken), [False] * len(spoken)
    for k, p in enumerate(pairs):
        if p is not None:
            a, b = p
            s_t[k], e_t[k], ok[k] = ref[a]["s"], ref[b]["e"], True
    # los que comparten una oída (2m) reparten su palabra por longitud
    k = 0
    while k < len(spoken) - 1:
        if pairs[k] is not None and pairs[k] == pairs[k + 1]:
            s0, e0 = s_t[k], e_t[k]
            l1, l2 = len(spoken[k]), len(spoken[k + 1])
            mid = s0 + (e0 - s0) * l1 / (l1 + l2)
            e_t[k], s_t[k + 1] = mid, mid
            k += 1
        k += 1
    # interpolar las no confirmadas por longitud de caracteres entre vecinos confirmados
    k = 0
    while k < len(spoken):
        if ok[k]:
            k += 1; continue
        j = k
        while j < len(spoken) and not ok[j]:
            j += 1
        left = e_t[k - 1] if k > 0 and e_t[k - 1] is not None else (s_t[j] if j < len(spoken) else 0.0)
        right = s_t[j] if j < len(spoken) and s_t[j] is not None else left + 0.3 * (j - k)
        right = max(right, left)
        tot = sum(len(spoken[x]) for x in range(k, j)) or 1
        cur = left
        for x in range(k, j):
            d = (right - left) * len(spoken[x]) / tot
            s_t[x], e_t[x] = cur, cur + d
            cur += d
        k = j
    # monotonía
    last = 0.0
    for k in range(len(spoken)):
        s_t[k] = max(s_t[k], last)
        e_t[k] = max(e_t[k], s_t[k] + MIN_DUR)
        last = s_t[k]
    words, marks = [], {}
    for ti, t in enumerate(toks):
        idx = [k for k, o in enumerate(owner) if o == ti]
        s, e = s_t[idx[0]], e_t[idx[-1]]
        conf = all(ok[k] for k in idx)
        for mk in t["marks"]:
            marks[mk] = round(s, 3)
        words.append({"text": t["shown"], "spoken": " ".join(t["spoken"]), "s": round(s, 3), "e": round(e, 3), "matched": conf})
    if tail_marks and words:
        for mk in tail_marks:
            marks[mk] = words[-1]["e"]
    n_ok = sum(ok)
    rate = n_ok / len(spoken) if spoken else 0.0
    unmatched = [{"spoken": spoken[k], "token": toks[owner[k]]["shown"]} for k in range(len(spoken)) if not ok[k]]
    long_words = [w for w in words if w["e"] - w["s"] > 1.2]
    return {"words": words, "marks": marks, "matchRate": round(rate, 3), "sin_confirmar": unmatched,
            "palabras_largas": long_words, "pausas": pauses, "oidas_sin_usar": max(0, len(hw) - n_ok)}


def srt_time(t):
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def to_srt(words, max_chars=42, gap=0.6, max_s=6.0):
    """Frases desde los tiempos por palabra: corta por puntuación final, pausa > gap o duración > max_s; máx. max_chars por línea."""
    cues, cur = [], []
    for k, w in enumerate(words):
        cur.append(w)
        end_punct = re.search(r"[.!?…]$", w["text"])
        nxt = words[k + 1] if k + 1 < len(words) else None
        dur = w["e"] - cur[0]["s"]
        if end_punct or nxt is None or nxt["s"] - w["e"] > gap or dur > max_s:
            cues.append(cur); cur = []
    out = []
    for i, c in enumerate(cues, 1):
        text = " ".join(w["text"] for w in c)
        if len(text) > max_chars:
            half = len(text) // 2
            cut = min((m.start() for m in re.finditer(" ", text)), key=lambda p: abs(p - half), default=None)
            if cut:
                text = text[:cut] + "\n" + text[cut + 1:]
        end = c[-1]["e"] + 0.25
        out.append(f"{i}\n{srt_time(c[0]['s'])} --> {srt_time(end)}\n{text}\n")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("guion"); ap.add_argument("words")
    ap.add_argument("--key", help="clip dentro de words.json (por defecto, el único)")
    ap.add_argument("-o", "--out", default="guion-words.json")
    ap.add_argument("--srt")
    a = ap.parse_args()
    data = json.load(open(a.words, encoding="utf-8"))
    key = a.key or (list(data)[0] if len(data) == 1 else None)
    if key is None or key not in data:
        sys.exit(f"ERROR: indica --key; claves disponibles: {list(data)}")
    res = build(open(a.guion, encoding="utf-8").read(), data[key])
    json.dump(res, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"matchRate {res['matchRate']:.2f} | {len(res['words'])} palabras del guion | sin confirmar: {len(res['sin_confirmar'])} | oídas sin usar: {res['oidas_sin_usar']}")
    if res["matchRate"] < 0.5:
        print("ERROR DE ARCHIVO: matchRate < 0.5, el guion o el audio no corresponden")
    elif res["matchRate"] < 0.85:
        print("AVISO: matchRate < 0.85: revisa el guion (¿lo que se dijo es lo que está escrito?) o el audio")
    for u in res["sin_confirmar"][:10]:
        print(f"  sin confirmar: «{u['spoken']}» (de «{u['token']}») -> tiempo interpolado, NO medido")
    for w in res["palabras_largas"][:5]:
        print(f"  palabra larga ({w['e'] - w['s']:.2f} s): «{w['text']}» en {w['s']:.2f}: ¿tiempo estirado sobre un silencio? comprueba con la forma de onda")
    if res["marks"]:
        print("marcadores:", {k: v for k, v in res["marks"].items()})
    if a.srt:
        open(a.srt, "w", encoding="utf-8").write(to_srt(res["words"]))
        print("SRT:", a.srt)
    sys.exit(0 if res["matchRate"] >= 0.85 else 1)


if __name__ == "__main__":
    main()
