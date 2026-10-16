#!/usr/bin/env python
"""video-aprender: UNA llamada para aprender de un video (link o archivo) y poder EJECUTAR a partir de lo aprendido.

Tres modos (--modo):
  contenido  una clase / tutorial / video con ecuaciones, diapositivas o pizarra (p. ej. finanzas): transcribe el audio, extrae
             cada estado estable de la pantalla y los ALINEA (que se decia mientras se mostraba cada cosa) -> contenido.md
  reunion    una reunion grabada: igual, y la plantilla de analisis pide decisiones, cambios solicitados con cita y minuto,
             pendientes con responsable y un plan de ejecucion a CONFIRMAR antes de tocar nada
  estilo     un video de referencia para aprender su forma (ritmo, gancho, voz, volumen) -> ficha-aprendizaje.md

Uso:
  python video_aprender.py FUENTE [--modo contenido|reunion|estilo] [--goal "que quiero aprender"] [-o carpeta]
                           [--lang es] [--model small] [--rapido] [--section 0-600] [--max-slides 40] [--sens 1.0]
                           [--sin-pantalla] [--lead 3] [--max-height 720] [--glosario trading] [--vocab "a,b"] [--muestreo N] [--cookies-from-browser firefox] [--no-transcribe]
  FUENTE: URL (se baja con fetch_reference.py y SUS protecciones) o ruta de un archivo local.
Todo se procesa EN LOCAL (Whisper local, sin subir audio ni video a ningun servicio): una reunion con un cliente es confidencial.
Despues Claude lee las imagenes EN ORDEN, completa analisis.md con evidencia (cita + minuto), verifica las ecuaciones
recalculandolas y, solo tras tu confirmacion, ejecuta. Procedimiento: references/video-aprender.md
"""
import argparse, datetime, hashlib, json, os, re, statistics, subprocess, sys, tempfile, time

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from _common import measure_loudness, probe_duration  # noqa: E402


def tc(t):
    t = max(0.0, t)
    return f"{int(t // 60):02d}:{t % 60:05.2f}"


def py(args, **kw):
    return subprocess.run([sys.executable] + args, capture_output=True, text=True, encoding="utf-8", errors="replace", **kw)


def slug_for(url):
    m = re.search(r"(?:v=|youtu\.be/|shorts/)([\w-]{11})", url)
    if m:
        return "yt_" + m.group(1)
    return "web_" + hashlib.sha1(url.encode()).hexdigest()[:8]


def run_tree(args, timeout):
    """Ejecuta un script con tiempo limite y, si vence, cierra TODO el arbol de procesos (yt-dlp -> ffmpeg incluidos). None = vencio."""
    p = subprocess.Popen([sys.executable] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace")
    try:
        out, err = p.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        subprocess.run(["taskkill", "/F", "/T", "/PID", str(p.pid)], capture_output=True)
        p.communicate()
        return None
    return subprocess.CompletedProcess(p.args, p.returncode, out, err)


def newest_video(outdir, exclude=()):
    vids = [os.path.join(outdir, f) for f in os.listdir(outdir) if f.lower().endswith((".mp4", ".mkv", ".webm", ".mov")) and os.path.join(outdir, f) not in exclude]
    return sorted(vids, key=os.path.getmtime)[-1] if vids else None


def fetch(url, outdir, a):
    base = [os.path.join(HERE, "fetch_reference.py"), "video", url, "-o", outdir, "--max-height", str(a.max_height)]
    if a.cookies_from_browser:
        base += ["--cookies-from-browser", a.cookies_from_browser]
    r = None
    if a.section:
        # Descargar un TRAMO (yt-dlp + ffmpeg sobre la transmision remota) puede quedarse colgado sin avisar (visto: 18 min con 1 s de CPU).
        print(f"  descargando el tramo {a.section[0]:g}-{a.section[1]:g} s (limite {a.fetch_timeout} s)...")
        r = run_tree(base + ["--section", f"{a.section[0]:g}-{a.section[1]:g}"], a.fetch_timeout)
        if r is None:
            print("  AVISO: la descarga por tramo se colgo y se cancelo. Plan B: bajar el video completo y recortar el tramo en local.")
            for f in os.listdir(outdir):
                if f.endswith((".part", ".ytdl")) or ".part" in f:
                    try:
                        os.remove(os.path.join(outdir, f))
                    except OSError:
                        pass
    if r is None or not a.section:
        r = run_tree(base, 3600)
        if r is None:
            sys.exit("La descarga del video completo tampoco termino en 60 min; se cancelo.")
        full = True
    else:
        full = False
    sys.stdout.write(r.stdout)
    if r.returncode != 0:
        sys.exit("No se pudo descargar:\n" + (r.stderr or r.stdout)[-600:])
    vid = newest_video(outdir)
    if not vid:
        sys.exit("La descarga termino pero no hay archivo de video en " + outdir)
    if a.section and full:
        from _common import FFMPEG
        cut = os.path.join(outdir, f"tramo_{a.section[0]:g}-{a.section[1]:g}.mp4")
        print(f"  recortando {a.section[0]:g}-{a.section[1]:g} s en local -> {os.path.basename(cut)}")
        c = subprocess.run([FFMPEG, "-v", "error", "-y", "-ss", str(a.section[0]), "-t", str(a.section[1] - a.section[0]), "-i", vid,
                            "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-c:a", "aac", cut], capture_output=True, text=True)
        if c.returncode != 0 or not os.path.exists(cut):
            sys.exit("No se pudo recortar el tramo:\n" + c.stderr[-400:])
        vid = cut
    meta = {}
    logp = os.path.join(outdir, "fetch-log.jsonl")
    if os.path.exists(logp):
        for line in open(logp, encoding="utf-8"):
            try:
                rec = json.loads(line)
            except ValueError:
                continue
            if rec.get("mode") == "video" and rec.get("url") == url:
                meta = rec
    return vid, meta


# ----------------------------------------------------------------------------- modo ESTILO
def compute(data, lufs, peak):
    info, shots, dur = data["info"], data["shots"], data["info"]["duration"]
    n = len(shots)
    durs = [s["duration"] for s in shots]
    m = {"duracion_s": round(dur, 2), "ancho": info["width"], "alto": info["height"], "fps": info["fps"],
         "orientacion": "vertical" if info["height"] > info["width"] else "horizontal" if info["width"] > info["height"] else "cuadrado",
         "planos": n, "plano_medio_s": round(statistics.mean(durs), 2), "plano_mediana_s": round(statistics.median(durs), 2),
         "plano_min_s": round(min(durs), 2), "plano_max_s": round(max(durs), 2),
         "cortes_por_minuto": round((n - 1) / dur * 60, 1) if dur else 0,
         "cortes_secos": sum(1 for s in shots if s.get("enters_with") == "seco"),
         "cortes_gradual_animado": sum(1 for s in shots if s.get("enters_with") == "gradual/animado"),
         "movimiento": {k: sum(1 for s in shots if s["motion_label"] == k) for k in ("estatico", "suave", "medio", "alto")},
         "lufs": lufs, "pico_dbfs": peak}
    h1 = [s["duration"] for s in shots if s["start"] < dur / 2]
    h2 = [s["duration"] for s in shots if s["start"] >= dur / 2]
    m["plano_medio_1a_mitad_s"] = round(statistics.mean(h1), 2) if h1 else None
    m["plano_medio_2a_mitad_s"] = round(statistics.mean(h2), 2) if h2 else None
    m["planos_mas_largos"] = [(s["id"], s["start"], s["duration"]) for s in sorted(shots, key=lambda s: -s["duration"])[:3]]
    if n >= 5:
        best = min(range(n - 4), key=lambda i: shots[i + 4]["end"] - shots[i]["start"])
        m["rafaga_mas_rapida"] = {"desde": shots[best]["start"], "hasta": shots[best + 4]["end"], "planos": 5}
    hook = [s for s in shots if s["start"] < 3]
    cov = [(min(s["end"], 3) - s["start"], s) for s in hook]
    m["gancho"] = {"planos_en_3s": len(hook), "cortes_en_3s": max(len(hook) - 1, 0),
                   "movimiento_medio": round(sum(w * s["motion"] for w, s in cov) / max(sum(w for w, _ in cov), 1e-6), 4)}
    sp = data.get("speech") or {}
    segs = [g for g in sp.get("segments", []) if not g.get("suspect")]
    words = sum(len(g["text"].split()) for g in segs)
    vs = data.get("speech_seconds", 0)
    vad = data.get("vad") or {}
    m["voz"] = {"segundos_fiables": vs, "ratio_vad": vad.get("speech_ratio"), "palabras": words,
                "palabras_por_minuto": round(words / (vs / 60), 0) if vs > 1 else None, "idioma": sp.get("language"),
                "pausas_ge_0_4s": len(vad.get("pauses", [])) if vad else None,
                "primera_voz_s": (vad["speech"][0][0] if vad.get("speech") else (segs[0]["s"] if segs else None))}
    m["gancho"]["voz_en_3s"] = bool(m["voz"]["primera_voz_s"] is not None and m["voz"]["primera_voz_s"] < 3)
    last = shots[-1]
    m["cierre"] = {"ultimo_plano_s": last["duration"], "casi_negro": any("casi negros" in g and str(last["id"]) in g for g in data.get("gaps", []))}
    th = []
    for i in range(3):
        a, b = dur * i / 3, dur * (i + 1) / 3
        ss = [s for s in shots if a <= s["start"] < b]
        th.append({"tramo": f"{tc(a)}–{tc(b)}", "planos": len(ss), "medio_s": round(statistics.mean([s["duration"] for s in ss]), 2) if ss else None,
                   "movimiento": {k: sum(1 for s in ss if s["motion_label"] == k) for k in ("estatico", "suave", "medio", "alto")}})
    m["tercios"] = th
    return m


def md_medido(m):
    L = ["| Dato | Valor |", "|---|---|",
         f"| Formato | {m['ancho']}×{m['alto']} ({m['orientacion']}), {m['fps']} fps, {tc(m['duracion_s'])} |",
         f"| Planos | {m['planos']} (media {m['plano_medio_s']} s, mediana {m['plano_mediana_s']} s, mín {m['plano_min_s']} s, máx {m['plano_max_s']} s) |",
         f"| Ritmo de cortes | {m['cortes_por_minuto']} por minuto · secos {m['cortes_secos']} · gradual/animado {m['cortes_gradual_animado']} (heurístico) |",
         f"| Aceleración | plano medio 1.ª mitad {m['plano_medio_1a_mitad_s']} s → 2.ª mitad {m['plano_medio_2a_mitad_s']} s |",
         f"| Movimiento (planos) | estático {m['movimiento']['estatico']} · suave {m['movimiento']['suave']} · medio {m['movimiento']['medio']} · alto {m['movimiento']['alto']} |",
         f"| Gancho (0–3 s) | {m['gancho']['planos_en_3s']} planos, {m['gancho']['cortes_en_3s']} cortes, movimiento medio {m['gancho']['movimiento_medio']}, voz en los 3 s: {'sí' if m['gancho']['voz_en_3s'] else 'no'} |",
         "| Planos más largos | " + "; ".join(f"#{i} en {tc(s)} ({d} s)" for i, s, d in m["planos_mas_largos"]) + " |"]
    if m.get("rafaga_mas_rapida"):
        r = m["rafaga_mas_rapida"]
        L.append(f"| Ráfaga más rápida | 5 planos entre {tc(r['desde'])} y {tc(r['hasta'])} |")
    v = m["voz"]
    L.append(f"| Voz | {v['segundos_fiables']} s fiables ({v['idioma'] or '—'}); " +
             (f"{v['palabras']} palabras → {int(v['palabras_por_minuto'])} palabras/min; " if v["palabras_por_minuto"] else "sin voz fiable; ") +
             f"pausas ≥ 0.4 s: {v['pausas_ge_0_4s']}; primera voz: {v['primera_voz_s']} s |")
    L.append(f"| Volumen | {m['lufs']} LUFS integrado, pico {m['pico_dbfs']} dBFS |")
    L.append(f"| Cierre | último plano {m['cierre']['ultimo_plano_s']} s{' (casi negro)' if m['cierre']['casi_negro'] else ''} |")
    return "\n".join(L)


def md_tercios(m):
    L = ["| Tramo | Planos | Plano medio | Movimiento (est/sua/med/alt) |", "|---|---|---|---|"]
    for t in m["tercios"]:
        mv = t["movimiento"]
        L.append(f"| {t['tramo']} | {t['planos']} | {t['medio_s']} s | {mv['estatico']}/{mv['suave']}/{mv['medio']}/{mv['alto']} |")
    return "\n".join(L)


def modo_estilo(a, video, outdir, titulo, fuente, meta):
    print("[2/4] mapa del video (planos, voz, hojas)...")
    mapdir = os.path.join(outdir, "mapa")
    cmd = [os.path.join(HERE, "video_understand.py"), video, "-o", mapdir, "--budget", str(a.budget)]
    if a.lang:
        cmd += ["--lang", a.lang]
    if a.no_transcribe:
        cmd += ["--no-transcribe"]
    r = py(cmd, timeout=7200)
    if r.returncode != 0:
        sys.exit("video_understand fallo:\n" + (r.stderr or r.stdout)[-800:])
    data = json.load(open(os.path.join(mapdir, "video-map.json"), encoding="utf-8"))
    print("[3/4] midiendo el estilo...")
    lufs, peak = (measure_loudness(video) if data["info"]["has_audio"] else (None, None))
    m = compute(data, lufs, peak)
    json.dump(m, open(os.path.join(outdir, "metricas.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("[4/4] escribiendo la ficha...")
    tpl = open(os.path.join(SKILL, "assets", "ficha-aprendizaje-template.md"), encoding="utf-8").read()
    segs = (data.get("speech") or {}).get("segments", [])
    trans = "\n".join(f"- [{tc(g['s'])}–{tc(g['e'])}] {g['text']}" + ("  **[SOSPECHOSO, no usar]**" if g.get("suspect") else "") for g in segs) or "_Sin voz fiable (música o ambiente): lo que se oye no se puede transcribir ni verificar._"
    hojas = "\n".join(f"- `mapa/{p}` — fotogramas #{[k for k in data['keyframes'] if k['sheet'] == i][0]['n']}–#{[k for k in data['keyframes'] if k['sheet'] == i][-1]['n']}"
                      for i, p in enumerate(data["sheets"], 1))
    ficha = (tpl.replace("{{TITULO}}", titulo).replace("{{FUENTE}}", fuente).replace("{{FECHA}}", datetime.date.today().isoformat())
             .replace("{{CARPETA}}", outdir).replace("{{OBJETIVO}}", a.goal).replace("{{MEDIDO}}", md_medido(m))
             .replace("{{TERCIOS}}", md_tercios(m)).replace("{{HOJAS}}", hojas).replace("{{TRANSCRIPCION}}", trans))
    fp = os.path.join(outdir, "ficha-aprendizaje.md")
    open(fp, "w", encoding="utf-8").write(ficha)
    print(f"\nlisto: {fp}\n  planos={m['planos']}  cortes/min={m['cortes_por_minuto']}  gancho: {m['gancho']['cortes_en_3s']} cortes en 3 s  voz={m['voz']['palabras_por_minuto']} pal/min  {m['lufs']} LUFS")
    print("  SIGUIENTE (Claude): 1) Read de cada hoja en mapa/sheets/ EN ORDEN; 2) completar las secciones 5-12 de la ficha con evidencia;")
    print("                      3) guardar cada aprendizaje con: python scripts/save_learning.py add ...  (candidato hasta repetirse o ser aprobado)")


# ----------------------------------------------------------------------------- modos CONTENIDO / REUNION
def transcribe_long(video, outjson, lang, model_name, fast, section=None, cut=True, hotwords=None):
    """Whisper local con vad_filter. Guarda avance parcial en outjson y lo REUTILIZA si ya esta completo."""
    if os.path.exists(outjson):
        d = json.load(open(outjson, encoding="utf-8"))
        if d.get("completo") and d.get("hotwords") == hotwords and any(g.get("palabras") for g in d.get("segmentos", [])):
            print(f"  transcripcion en cache: {outjson}")
            return d
    try:
        from faster_whisper import WhisperModel
        from video_understand import HALLUCINATION
    except Exception as e:  # noqa
        sys.exit(f"Falta faster-whisper ({e}); pip install faster-whisper")
    from _common import FFMPEG
    wav = os.path.join(tempfile.gettempdir(), "va_audio.wav")
    cmd = [FFMPEG, "-v", "error", "-y"]
    if section and cut:
        cmd += ["-ss", str(section[0]), "-t", str(section[1] - section[0])]
    subprocess.run(cmd + ["-i", video, "-vn", "-ar", "16000", "-ac", "1", wav], check=True)
    total = os.path.getsize(wav) / 32000.0
    t0 = time.time()
    model = WhisperModel(model_name, device="cpu", compute_type="int8")
    segs, info = model.transcribe(wav, language=lang, vad_filter=True, condition_on_previous_text=False, beam_size=1 if fast else 5, word_timestamps=True, hotwords=hotwords)
    out, lastp = [], 0.0
    off = section[0] if section else 0.0
    for sg in segs:
        why = []
        if sg.no_speech_prob >= 0.6:
            why.append(f"no_speech={sg.no_speech_prob:.2f}")
        if HALLUCINATION.search(sg.text):
            why.append("frase tipica de alucinacion de Whisper")
        dud = sg.avg_logprob < -1.0 and not why      # blando: se CONSERVA marcado; descartarlo perderia contenido real
        out.append({"s": round(sg.start + off, 2), "e": round(sg.end + off, 2), "text": sg.text.strip(), "suspect": bool(why),
                    "dudoso": dud, "why": "; ".join(why) or (f"logprob={sg.avg_logprob:.2f}" if dud else ""),
                    "palabras": [[round(w.start + off, 2), round(w.end + off, 2), w.word.strip()] for w in (sg.words or [])]})
        if sg.end - lastp >= 60:
            lastp = sg.end
            el = time.time() - t0
            print(f"  transcrito {tc(sg.end)} / {tc(total)}  ({el / 60:.1f} min transcurridos; ritmo {sg.end / max(el, 1):.2f}x tiempo real)")
            json.dump({"completo": False, "idioma": info.language, "segmentos": out}, open(outjson, "w", encoding="utf-8"), ensure_ascii=False)
    d = {"completo": True, "idioma": info.language, "prob_idioma": round(float(info.language_probability), 2), "segmentos": out,
         "modelo": model_name, "rapido": fast, "hotwords": hotwords}
    json.dump(d, open(outjson, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return d



# ----------------------------------------------------------------------------- diapositivas en PDF (video de aula + archivo original)
STOP = set("""this that with from have they their there which would could should about these those were been being what when where while will your
than then them also into over only more most much many some such very just like said says does done make made well here ahead because
cuando donde como pero para esto esta este estos estas entre sobre desde hasta porque tambien tiene tienen puede pueden hacer""".split())


def words_of(text):
    return [w for w in re.findall(r"[a-z\u00e1\u00e9\u00ed\u00f3\u00fa\u00f1\u00fc]{4,}", text.lower()) if w not in STOP]


def render_pdf(pdf, outdir, width=1280):
    import fitz
    os.makedirs(outdir, exist_ok=True)
    doc = fitz.open(pdf)
    pages = []
    for i, pg in enumerate(doc, 1):
        z = width / max(pg.rect.width, 1)
        pth = os.path.join(outdir, f"p_{i:02d}.jpg")
        pg.get_pixmap(matrix=fitz.Matrix(z, z)).save(pth)
        raw = pg.get_text()
        seen, lines = set(), []
        for ln in (l.strip() for l in raw.splitlines()):
            if ln and ln not in seen:                   # los PDF de diapositivas repiten lineas (capa de texto duplicada)
                seen.add(ln); lines.append(ln)
        txt = " | ".join(lines)
        pages.append({"n": i, "file": os.path.relpath(pth, os.path.dirname(outdir)), "text": txt, "words": sorted(set(words_of(txt)))})
    return pages


def align_pages(pages, segments, bucket=30.0, lam=0.12, min_shared=3, min_raw=6.0, min_windows=4, min_coherence=0.7):
    """Alineacion HEURISTICA y MONOTONA de paginas con la voz por palabras compartidas (idf).
    PUERTA DE COHERENCIA (calibrada con una clase real de MIT, 3 tramos): ninguna ventana aislada separa la explicacion real de una charla
    ajena (puntajes de 20 en charla ajena, de 8 en explicacion real), pero la SECUENCIA si: si el profesor explica el PDF, las mejores
    paginas de cada ventana caen juntas (3,5,9,5,5,9,3); si habla de otra cosa saltan por todo el documento (37,8,34,36,35,19...).
    Si la coherencia es baja no se asigna NADA. Devuelve (asignacion, descartadas_por_baja, meta); meta explica la decision."""
    import math
    m = len(pages)
    meta = {"ventanas": 0, "con_evidencia": 0, "coherencia": None, "motivo": ""}
    if not m or not segments:
        meta["motivo"] = "sin paginas o sin voz"
        return {}, 0, meta
    df = {}
    for pg in pages:
        for w in pg["words"]:
            df[w] = df.get(w, 0) + 1
    idf = {w: math.log((m + 1) / (c + 0.5)) for w, c in df.items()}
    tmax = max(g["e"] for g in segments)
    n = int(tmax // bucket) + 1
    bags = [dict() for _ in range(n)]
    for g in segments:
        for w in words_of(g["text"]):
            b = bags[min(int(g["s"] // bucket), n - 1)]
            b[w] = b.get(w, 0) + 1
    raw = [[0.0] * m for _ in range(n)]
    shared = [[[] for _ in range(m)] for _ in range(n)]
    habladas = 0
    for i, b in enumerate(bags):
        if sum(b.values()) >= 8:
            habladas += 1
        for j, pg in enumerate(pages):
            ws = set(pg["words"])
            sh = [w for w in b if w in ws and idf[w] >= 1.0]
            if len(sh) >= min_shared:
                r = sum(idf[w] * min(b[w], 2) for w in sh)
                if r >= min_raw:
                    raw[i][j] = r
                    shared[i][j] = sorted(sh, key=lambda w: -idf[w])
    best = [max(range(m), key=lambda j: raw[i][j]) for i in range(n)]
    cand = [i for i in range(n) if raw[i][best[i]] > 0]
    meta["ventanas"], meta["con_evidencia"] = habladas, len(cand)
    if len(cand) < min_windows or len(cand) < 0.5 * max(habladas, 1):
        meta["motivo"] = f"pocas ventanas con evidencia ({len(cand)} de {habladas} con voz; se piden >= {min_windows} y la mitad)"
        return {}, 0, meta
    pgs = sorted(best[i] for i in cand)
    med = pgs[len(pgs) // 2]
    band = max(2, int(round(0.15 * m)))      # la banda escala con el tamano del PDF (37 pag -> 6; 8 pag -> 2); una fija de 6 cubria TODO un PDF corto
    coh = sum(1 for i in cand if abs(best[i] - med) <= band) / len(cand)
    meta["coherencia"] = round(coh, 2)
    if coh < min_coherence:
        meta["motivo"] = f"coherencia {coh:.2f} < {min_coherence}: las mejores paginas saltan por todo el PDF; este tramo no parece explicar ese archivo (o es otro archivo/tramo)"
        return {}, 0, meta
    gmax = max(raw[i][best[i]] for i in cand)
    S = [[v / gmax for v in row] for row in raw]
    dp = [[0.0] * m for _ in range(n)]
    bk = [[0] * m for _ in range(n)]
    dp[0] = list(S[0])
    for i in range(1, n):
        for j in range(m):
            stay = dp[i - 1][j]
            k = max(range(j), key=lambda q: dp[i - 1][q]) if j else None
            jump = dp[i - 1][k] - lam if k is not None else -1e9
            if stay >= jump:
                dp[i][j], bk[i][j] = S[i][j] + stay, j
            else:
                dp[i][j], bk[i][j] = S[i][j] + jump, k
    j = max(range(m), key=lambda q: dp[n - 1][q])
    path = [0] * n
    for i in range(n - 1, -1, -1):
        path[i] = j
        j = bk[i][j]
    out = {}
    for i, j in enumerate(path):
        if raw[i][j] <= 0:
            continue
        d = out.setdefault(j + 1, {"t0": i * bucket, "t1": (i + 1) * bucket, "n": [], "pal": [], "raw": []})
        d["t1"] = (i + 1) * bucket
        d["n"].append(len(shared[i][j]))
        d["raw"].append(raw[i][j])
        d["pal"] += shared[i][j][:4]
    res = {}
    for k, v in out.items():
        mean = sum(v["n"]) / len(v["n"])
        mraw = sum(v["raw"]) / len(v["raw"])
        nivel = "alta" if (len(v["n"]) >= 2 and mraw >= 15) else "media" if mraw >= 8 else "baja"
        res[k] = {"t0": v["t0"], "t1": v["t1"], "ventanas": len(v["n"]), "palabras_comunes_media": round(mean, 1), "puntaje_medio": round(mraw, 1),
                  "ejemplos": sorted(set(v["pal"]))[:8], "evidencia": nivel}
    keep = {k: v for k, v in res.items() if v["evidencia"] != "baja"}
    meta["motivo"] = f"coherencia {coh:.2f}: la voz de este tramo sigue una zona coherente del PDF (paginas ~{max(1, med - band)}-{min(m, med + band)})"
    return keep, len(res) - len(keep), meta


def pdf_md(pages, al, tr, n_baja=0, meta=None):
    L = ["## Diapositivas del archivo original (PDF) y lo que se decía", "",
         f"_{len(pages)} páginas. **La alineación con la voz es HEURÍSTICA** (palabras distintivas de cada página frente a lo dicho, en orden): es una propuesta, no una verdad; "
         "confírmala con el contexto antes de afirmar «en el minuto X explicó la página N». Evidencia **baja** (una sola ventana o pocas palabras en común) = adivinanza; no la uses para afirmar nada. Las páginas «sin tramo asignado» pueden haberse saltado, o no haberse nombrado. "
         "Las ecuaciones se leen en la imagen de la página (o en su texto), no en el video._", ""]
    if meta and meta.get("motivo"):
        L += [f"**Alineación: {meta['motivo']}.**" + (" No se asignó ninguna página: lo que sigue son las páginas del archivo, sin tiempos." if not al else ""), ""]
    segs = [g for g in (tr or {}).get("segmentos", []) if not g.get("suspect")]
    for pg in pages:
        a = al.get(pg["n"])
        head = f"### Página {pg['n']:02d}" + (f" · probable {tc(a['t0'])} → {tc(a['t1'])}  (evidencia **{a['evidencia']}**: {a['ventanas']} ventana(s), puntaje medio {a['puntaje_medio']}, ~{a['palabras_comunes_media']} palabras en común: {', '.join(a['ejemplos'])})" if a else " · sin tramo asignado")
        L += [head, f"![p{pg['n']}]({pg['file'].replace(os.sep, '/')})", "", f"Texto de la página: {pg['text'][:700] or '_(sin texto)_'}", ""]
        if a:
            mine = [g for g in segs if a["t0"] <= (g["s"] + g["e"]) / 2 < a["t1"]]
            L += [f"- [{tc(g['s'])}] {g['text']}" for g in mine[:25]] + ([f"- … (+{len(mine) - 25} frases más en ese tramo)"] if len(mine) > 25 else [])
            L.append("")
    return "\n".join(L)


def run_slides(video, outdir, a):
    cmd = [os.path.join(HERE, "slides_extract.py"), video, "-o", outdir, "--max", str(a.max_slides), "--sens", str(a.sens)]
    if a.section and not a.is_url:
        cmd += ["--from", f"{a.section[0]:g}", "--to", f"{a.section[1]:g}"]
    if a.roi:
        cmd += ["--roi", a.roi]
    r = py(cmd, timeout=7200)
    sys.stdout.write("".join("  " + l + "\n" for l in r.stdout.strip().splitlines()[-14:]))
    if r.returncode != 0:
        sys.exit("slides_extract fallo:\n" + (r.stderr or r.stdout)[-600:])
    return json.load(open(os.path.join(outdir, "slides.json"), encoding="utf-8"))



# ----------------------------------------------------------------------------- glosario de dominio y muestreo de fotogramas (v1.4)
GLOS = None


def cargar_glosario(nombre):
    """assets/glosarios/<nombre>.json (o una ruta). Devuelve None si no se pidio."""
    if not nombre:
        return None
    p = nombre if os.path.exists(nombre) else os.path.join(SKILL, "assets", "glosarios", nombre + ".json")
    if not os.path.exists(p):
        sys.exit(f"no existe el glosario: {nombre} (busque {p})")
    g = json.load(open(p, encoding="utf-8"))
    g["_corr"] = [(re.compile(rx, re.I), rep_) for rx, rep_ in g.get("correcciones", [])]
    g["_cues"] = [re.compile(rx, re.I) for rx in g.get("pistas_pantalla", [])]
    return g


def fx(text):
    """Corrige errores de oido CONOCIDOS del glosario en el texto mostrado (transcripcion.json conserva el crudo)."""
    if not GLOS:
        return text
    for rx, rep_ in GLOS["_corr"]:
        text = rx.sub(rep_, text)
    return text


def contar_correcciones(tr):
    if not GLOS or not tr:
        return 0
    n = 0
    for g in tr.get("segmentos", []):
        for rx, _ in GLOS["_corr"]:
            n += len(rx.findall(g["text"]))
    return n


def _nitidez(arr):
    import numpy as np
    g = arr.astype("float32")
    lap = 4 * g[1:-1, 1:-1] - g[:-2, 1:-1] - g[2:, 1:-1] - g[1:-1, :-2] - g[1:-1, 2:]
    return float(lap.var())


def mejor_fotograma(video, t, dur, destino, ancho):
    """Guarda el fotograma MAS NITIDO de [t-0.5, t+0.5] (evita la borrosidad de movimiento de una mano o de la camara) a `ancho` px. Devuelve su tiempo."""
    import numpy as np
    from _common import FFMPEG
    t0 = min(max(0.0, t - 0.5), max(0.0, dur - 1.0))
    raw = subprocess.run([FFMPEG, "-v", "error", "-ss", f"{t0:.2f}", "-t", "1.0", "-i", video, "-vf", "fps=6,scale=256:256,format=gray", "-f", "rawvideo", "-"],
                         capture_output=True, timeout=90).stdout
    n = len(raw) // 65536
    best = t
    if n:
        fr = np.frombuffer(raw[: n * 65536], dtype=np.uint8).reshape(n, 256, 256)
        best = min(t0 + int(np.argmax([_nitidez(f) for f in fr])) / 6.0, max(0.0, dur - 0.1))
    subprocess.run([FFMPEG, "-v", "error", "-y", "-ss", f"{best:.2f}", "-i", video, "-frames:v", "1", "-vf", f"scale={ancho}:-2", "-q:v", "3", destino], check=True, timeout=90)
    return round(best, 2)


def muestrear(video, outdir, tr, dur, n, ancho=720, base=0.0):
    """Cuando la pantalla NO tiene estados estables (una persona hablando a camara, o una camara filmando un monitor con manos delante):
    n fotogramas repartidos + uno en cada momento en que la voz SENALA la pantalla ('podemos ver', 'miren'... del glosario). Hoja de contacto incluida."""
    from PIL import Image, ImageDraw
    carpeta = os.path.join(outdir, "pantalla", "muestreo")
    os.makedirs(carpeta, exist_ok=True)
    pedidos = [((i + 0.5) * dur / n, "uniforme") for i in range(n)]
    if GLOS:
        for g in (tr or {}).get("segmentos", []):
            if g.get("suspect"):
                continue
            if any(rx.search(g["text"]) for rx in GLOS["_cues"]):
                t = min(max(g["s"] - base, 0.0) + 1.0, max(dur - 0.2, 0.0))
                if all(abs(t - u) > 4.0 for u, _ in pedidos):
                    pedidos.append((t, "pista hablada"))
    pedidos = sorted(pedidos)[:28]
    out = []
    for k, (t, why) in enumerate(pedidos, 1):
        tt = t + base
        nombre = f"m_{k:02d}_{int(tt) // 60:02d}m{int(tt) % 60:02d}s.jpg"
        real = mejor_fotograma(video, t, dur, os.path.join(carpeta, nombre), ancho)
        out.append({"n": k, "t": round(real + base, 2), "motivo": why, "file": os.path.join("pantalla", "muestreo", nombre)})
    tw, cols = 270, 4
    tiles = []
    for m in out:
        im = Image.open(os.path.join(outdir, m["file"])).convert("RGB")
        im = im.resize((tw, max(1, int(im.height * tw / im.width))))
        tiles.append((m, im))
    th = max(im.height for _, im in tiles)
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw, rows * (th + 16)), (20, 20, 20))
    d = ImageDraw.Draw(sheet)
    for i, (m, im) in enumerate(tiles):
        x, y = (i % cols) * tw, (i // cols) * (th + 16)
        sheet.paste(im, (x, y + 16))
        d.text((x + 3, y + 2), f"M{m['n']:02d} {tc(m['t'])}" + (" *" if m["motivo"] != "uniforme" else ""), fill=(255, 255, 0))
    hoja = os.path.join(carpeta, "hoja.jpg")
    sheet.save(hoja, quality=82)
    return {"fotogramas": out, "hoja": os.path.join("pantalla", "muestreo", "hoja.jpg")}


def contenido_md(titulo, fuente, modo, dur, tr, sl, lead, pdfblock="", section_note=False, mu=None):
    segs = [g for g in (tr or {}).get("segmentos", []) if not g.get("suspect")]
    words = sum(len(g["text"].split()) for g in segs)
    sp = sum(max(min(g["e"], dur) - g["s"], 0) for g in segs)
    L = [f"# Contenido — {titulo}", f"Fuente: {fuente} · Modo: {modo} · Generado: {datetime.date.today().isoformat()} · Duración del archivo analizado: {tc(dur)}", "",
         ("**Todos los minutos de este documento son los de la clase/grabación ORIGINAL** (no los del recorte analizado)." if section_note else "Los minutos son los del archivo analizado."), "",
         "> Esto es la **evidencia cruda**: lo que se dijo (transcripción local, puede tener errores) alineado con lo que se mostró (estados estables de la pantalla). "
         "El análisis y las conclusiones van en `analisis.md`, citando minuto y fotograma. **Claude no oye ni ve en movimiento: lee texto e imágenes.**", "",
         "## Lo medido", ""]
    if tr:
        L.append(f"- Voz transcrita: {tc(sp)} ({sp / dur * 100:.0f} % del video), {words} palabras"
                 + (f", {words / (sp / 60):.0f} palabras/min" if sp > 30 else "") + f", idioma {tr.get('idioma', '—')}.")
    else:
        L.append("- Sin transcripción (se omitió o no hay audio).")
    sus = [g for g in (tr or {}).get("segmentos", []) if g.get("suspect")]
    dud = [g for g in (tr or {}).get("segmentos", []) if g.get("dudoso")]
    if dud:
        L.append(f"- {len(dud)} segmento(s) **dudosos** (baja confianza del reconocimiento): se conservan marcados; contrastarlos con la imagen o el audio.")
    if sus:
        L.append(f"- {len(sus)} segmento(s) **descartados** (sin voz o frase típica de alucinación de Whisper): " + "; ".join(f"[{tc(g['s'])}] {g['why']}" for g in sus[:6]))
    if sl:
        L.append(f"- Pantalla: {len(sl['slides'])} estados estables (umbral {sl['umbral_bloques_pct']} % de bloques).")
    nc = contar_correcciones(tr)
    if GLOS:
        L.append(f"- Glosario «{GLOS.get('nombre', '?')}»: {nc} termino(s) corregido(s) de oido en este documento (el texto crudo sigue en `transcripcion.json`); el vocabulario tambien se paso al reconocedor.")
    if mu:
        L.append(f"- Muestreo de fotogramas: {len(mu['fotogramas'])} (la pantalla no tuvo estados estables suficientes; ver la seccion de muestreo).")
    L.append("")
    if sl and sl["slides"]:
        L += ["## Pantalla y lo que se decía mientras tanto", "",
              f"_Cada bloque lista lo dicho desde {lead:g} s antes de que aparezca hasta {lead:g} s antes del siguiente cambio (quien explica suele hablar antes de escribir)._", ""]
        slides = sl["slides"]
        used = set()
        for k, s in enumerate(slides):
            lo, hi = s["t"] - lead, (slides[k + 1]["t"] - lead) if k + 1 < len(slides) else 1e9
            mine = []
            for j, g in enumerate((tr or {}).get("segmentos", [])):
                if g.get("suspect"):
                    continue
                ws = g.get("palabras") or []
                if ws:
                    sel = [w for w in ws if lo <= (w[0] + w[1]) / 2 < hi]
                    if not sel:
                        continue
                    txt = fx(("… " if sel[0] is not ws[0] else "") + " ".join(w[2] for w in sel) + (" …" if sel[-1] is not ws[-1] else ""))
                    mine.append((j, g, txt, sel[0][0], sel[-1][1]))
                else:                                           # cache sin palabras: por solape del segmento
                    ov = min(g["e"], hi) - max(g["s"], lo)
                    if ov > 0 and (ov >= 1.0 or lo <= (g["s"] + g["e"]) / 2 < hi):
                        mine.append((j, g, fx(g["text"]), g["s"], g["e"]))
            used.update(j for j, *_ in mine)
            L += [f"### #{s['n']:02d} · {tc(s['t'])} → {tc(s['t_hasta'])}  (cambio {s['cambio_pct']} % de la pantalla)",
                  f"![#{s['n']}]({s['file'].replace(os.sep, '/')})", ""]
            L += [f"- [{tc(t0)}–{tc(t1)}] {txt}" + ("  _(dudoso: " + g["why"] + ")_" if g.get("dudoso") else "")
                  for _, g, txt, t0, t1 in mine] or ["- _(sin voz en este tramo)_"]
            L.append("")
        pre = [g for j, g in enumerate((tr or {}).get("segmentos", [])) if j not in used and not g.get("suspect")]
        if pre:
            L += ["### Dicho fuera de cualquier tramo", ""] + [f"- [{tc(g['s'])}–{tc(g['e'])}] {fx(g['text'])}" for g in pre] + [""]
    elif tr:
        L += ["## Transcripción con tiempos", ""] + [f"- [{tc(g['s'])}–{tc(g['e'])}] {fx(g['text'])}" + ("  **[DESCARTADO: " + g["why"] + "]**" if g.get("suspect") else "  _(dudoso: " + g["why"] + ")_" if g.get("dudoso") else "") for g in tr["segmentos"]] + [""]
    if mu:
        L += ["## Muestreo de fotogramas (la pantalla no tuvo estados estables)", "",
              "_Hay una persona hablando a cámara o una cámara filmando un monitor (con manos delante): el detector de cambios no encuentra estados estables. "
              "Se tomaron fotogramas repartidos por el video y uno en cada momento en que la voz señala la pantalla («podemos ver», «miren»…, marcados con `*`). "
              "Cada uno es el más nítido de ±0.5 s. **Mira primero `hoja.jpg` (todo de un vistazo) y abre solo los que importen**; las cifras de un gráfico se leen en el fotograma, no en la voz._", "",
              f"![hoja]({mu['hoja'].replace(os.sep, '/')})", ""]
        segs_ = (tr or {}).get("segmentos", [])
        for m in mu["fotogramas"]:
            lo, hi = m["t"] - 2.5, m["t"] + 2.5
            ws_ = [w[2] for g in segs_ if not g.get("suspect") for w in (g.get("palabras") or []) if lo <= (w[0] + w[1]) / 2 <= hi]
            dicho = fx(" ".join(ws_)) if ws_ else fx(" ".join(g["text"] for g in segs_ if not g.get("suspect") and g["e"] > lo and g["s"] < hi))
            L += [f"### M{m['n']:02d} · {tc(m['t'])} ({m['motivo']})", f"![M{m['n']}]({m['file'].replace(os.sep, '/')})", f"- dicho alrededor: «{dicho or '(sin voz)'}»", ""]
    if pdfblock:
        L += [pdfblock, ""]
    L += ["## Límites de esta lectura (declararlos siempre)", "",
          "- **No distingue quién habla** (no hay diarización): en una reunión, atribuir una frase a una persona solo vale si el propio audio lo dice o el usuario lo confirma.",
          "- La transcripción puede equivocar **cifras, nombres propios, siglas y términos técnicos**: toda cifra o fórmula importante se contrasta con la imagen y se recalcula.",
          "- Una ecuación escrita se lee **desde la imagen**; si es pequeña, ampliar con `frame_probe.py --at T --crop x,y,w,h --scale 2`. Lo ilegible se marca, no se adivina.",
          "- Un gesto, un tono o un silencio incómodo en una reunión **no se pueden verificar**.",
          "- Entre dos capturas puede haber pasado algo (una animación, una corrección): si la explicación salta, pedir más sondas.",
          "- **Video de aula con cámara(s)**: la diapositiva proyectada ocupa una parte pequeña del cuadro y las cámaras cambian de ángulo y de zoom, así que la detección de cambios de diapositiva **no es fiable** (ni con `--roi`) y las ecuaciones no son legibles si el video es de baja resolución. Pide el **archivo original de las diapositivas** y usa `--slides archivo.pdf`.", ""]
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source"); ap.add_argument("--modo", default="contenido", choices=["contenido", "reunion", "estilo"])
    ap.add_argument("--goal", default="(no indicado)"); ap.add_argument("-o", "--out")
    ap.add_argument("--lang"); ap.add_argument("--model", default="small"); ap.add_argument("--rapido", action="store_true")
    ap.add_argument("--section", help="tramo en segundos, p. ej. 0-600 (descarga y analisis solo de ese tramo)")
    ap.add_argument("--max-slides", type=int, default=40); ap.add_argument("--sens", type=float, default=1.0)
    ap.add_argument("--sin-pantalla", action="store_true"); ap.add_argument("--lead", type=float, default=3.0)
    ap.add_argument("--slides", help="PDF con las diapositivas ORIGINALES (para video de aula): se renderizan, se lee su texto y se propone en que tramo de la voz se explico cada pagina")
    ap.add_argument("--roi", help="region x,y,w,h (fracciones 0-1) de la pantalla proyectada en un video de aula")
    ap.add_argument("--budget", type=int, default=24); ap.add_argument("--max-height", type=int, default=720)
    ap.add_argument("--cookies-from-browser"); ap.add_argument("--no-transcribe", action="store_true")
    ap.add_argument("--glosario", help="glosario de dominio (assets/glosarios/<nombre>.json, p. ej. trading) o ruta: vocabulario para el reconocedor + correccion de terminos mal oidos")
    ap.add_argument("--vocab", help="palabras extra para el reconocedor, separadas por comas (se suman al glosario)")
    ap.add_argument("--muestreo", type=int, default=-1, help="fotogramas repartidos cuando la pantalla no tiene estados estables: -1 automatico (si hay < 4 estados), 0 desactivado, N = N fotogramas siempre")
    ap.add_argument("--muestreo-ancho", type=int, default=720)
    ap.add_argument("--fetch-timeout", type=int, default=600, help="segundos maximos para descargar un TRAMO antes del plan B (video completo + recorte local)")
    a = ap.parse_args()
    a.section = tuple(float(x) for x in a.section.split("-")) if a.section else None
    if a.section and a.section[1] <= a.section[0]:
        sys.exit("--section debe ser INICIO-FIN con FIN > INICIO")
    a.is_url = bool(re.match(r"^https?://", a.source))
    global GLOS
    GLOS = cargar_glosario(a.glosario)
    hot = ", ".join(x for x in ((GLOS or {}).get("vocab"), a.vocab) if x) or None

    meta = {}
    if a.is_url:
        outdir = os.path.abspath(a.out or os.path.join("referencias", slug_for(a.source)))
        os.makedirs(outdir, exist_ok=True)
        print(f"[1] descargando (fetch_reference) -> {outdir}")
        video, meta = fetch(a.source, outdir, a)
    else:
        video = os.path.abspath(a.source)
        if not os.path.exists(video):
            sys.exit("no existe: " + video)
        outdir = os.path.abspath(a.out or os.path.join(os.path.dirname(video), "aprendizaje", os.path.splitext(os.path.basename(video))[0]))
        os.makedirs(outdir, exist_ok=True)
        print(f"[1] archivo local: {video}")
    titulo = meta.get("title") or os.path.splitext(os.path.basename(video))[0]
    fuente = a.source + (f" (canal: {meta.get('uploader')}; licencia declarada: {meta.get('license') or 'no declarada'})" if meta else "")
    dur = probe_duration(video)

    if a.modo == "estilo":
        return modo_estilo(a, video, outdir, titulo, fuente, meta)

    tr = sl = None
    if not a.no_transcribe:
        print(f"[2] transcribiendo en local (modelo {a.model}{', rapido' if a.rapido else ''}); en esta CPU ~1x el tiempo del audio con 'small'...")
        # si el video ya es el tramo descargado (URL con --section), no se vuelve a recortar
        tr = transcribe_long(video, os.path.join(outdir, "transcripcion.json"), a.lang, a.model, a.rapido,
                             a.section, cut=not a.is_url, hotwords=hot)     # URL con tramo: el archivo YA es el tramo (solo se desplaza el reloj)
    if not a.sin_pantalla:
        print("[3] extrayendo los estados estables de la pantalla...")
        sl = run_slides(video, os.path.join(outdir, "pantalla"), a)
        base = a.section[0] if (a.is_url and a.section) else 0.0
        for s in sl["slides"]:
            s["file"] = os.path.join("pantalla", s["file"])
            s["t"] = round(s["t"] + base, 2)
            s["t_hasta"] = round(s["t_hasta"] + base, 2)
    mu = None
    n_est = len(sl["slides"]) if sl else 0
    if not a.sin_pantalla and a.muestreo != 0 and dur >= 20 and (a.muestreo > 0 or n_est < 4):
        nmu = a.muestreo if a.muestreo > 0 else max(8, min(16, round(dur / 10)))
        print(f"[3a] pocos estados estables ({n_est}): muestreo de {nmu} fotogramas repartidos + los que la voz senala...")
        mu = muestrear(video, outdir, tr, dur, nmu, a.muestreo_ancho, base=(a.section[0] if (a.is_url and a.section) else 0.0))
        print(f"  {len(mu['fotogramas'])} fotogramas; hoja: {mu['hoja']}")
    pdfblock = ""
    if a.slides:
        if not os.path.exists(a.slides):
            sys.exit("no existe el PDF: " + a.slides)
        print("[3b] renderizando el PDF y alineando paginas con la voz (heuristico)...")
        pages = render_pdf(os.path.abspath(a.slides), os.path.join(outdir, "diapositivas"))
        segs = [g for g in (tr or {}).get("segmentos", []) if not g.get("suspect")]
        al, n_baja, meta_al = align_pages(pages, segs) if segs else ({}, 0, {"motivo": "sin voz"})
        json.dump({"paginas": [{k: v for k, v in pg.items() if k != "words"} for pg in pages], "alineacion": al}, open(os.path.join(outdir, "diapositivas.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"  {len(pages)} paginas; con tramo asignado (evidencia suficiente): {len(al)}" + (" -> " + ", ".join(f"p{k}({v['evidencia']})" for k, v in sorted(al.items())) if al else "") + (f" · {n_baja} descartada(s) por evidencia baja (ruido)" if n_baja else "") + f"\n  alineacion: {meta_al.get('motivo', '')}")
        pdfblock = pdf_md(pages, al, tr, n_baja, meta_al)
    print("[4] escribiendo contenido.md y analisis.md ...")
    open(os.path.join(outdir, "contenido.md"), "w", encoding="utf-8").write(contenido_md(titulo, fuente, a.modo, dur, tr, sl, a.lead, pdfblock, bool(a.section), mu))
    tplname = "analisis-reunion-template.md" if a.modo == "reunion" else "analisis-contenido-template.md"
    tpl = open(os.path.join(SKILL, "assets", tplname), encoding="utf-8").read()
    open(os.path.join(outdir, "analisis.md"), "w", encoding="utf-8").write(
        tpl.replace("{{TITULO}}", titulo).replace("{{FUENTE}}", fuente).replace("{{FECHA}}", datetime.date.today().isoformat())
        .replace("{{OBJETIVO}}", a.goal).replace("{{CARPETA}}", outdir))
    n = len(sl["slides"]) if sl else 0
    print(f"\nlisto: {outdir}\n  contenido.md (evidencia cruda)   analisis.md (a completar)   pantalla/: {n} estados" + (f" + {len(mu['fotogramas'])} fotogramas de muestreo (mira hoja.jpg)" if mu else ""))
    print("  SIGUIENTE (Claude): 1) Read de contenido.md; 2) Read de cada imagen de pantalla/slides/ EN ORDEN (ecuaciones: ampliar con frame_probe.py);")
    print("                      3) completar analisis.md con evidencia; 4) RECALCULAR cada ecuacion/cifra con Python; 5) proponer el plan de ejecucion y ESPERAR confirmacion.")


if __name__ == "__main__":
    main()
