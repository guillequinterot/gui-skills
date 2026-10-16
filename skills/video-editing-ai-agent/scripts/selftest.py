#!/usr/bin/env python
"""Prueba automatica de la skill (v1.3): crea un video SINTETICO con ffmpeg y comprueba cada script.

Uso:
  python selftest.py                 # rapida (~30 s, sin red, sin Whisper)
  python selftest.py --speech        # + voz sintetica de Windows (SAPI) para validar el VAD con habla real
  python selftest.py --whisper       # + transcripcion con faster-whisper (necesita --speech; descarga/usa el modelo local)
  python selftest.py --network       # + fetch_reference.py info contra una URL publica (necesita internet)
  python selftest.py --hyperframes   # + requisitos de HyperFrames (Node>=22, navegador headless); NO renderiza
  python selftest.py --keep          # conserva la carpeta temporal para inspeccionar
Sale con codigo 1 si algo falla. Tambien sirve de "doctor" tras instalar la skill en otra maquina.

Incluye pruebas de REGRESION de fallos reales ya corregidos:
  - fetch_reference: commonpath entre discos distintos (C: vs D:) no debe lanzar excepcion;
  - fetch_reference: el codigo 101 de yt-dlp (--max-downloads) es exito;
  - video_understand: debe avisar si el audio es mas corto que el video;
  - cut_dip: un corte directo da hueco 0 % y un corte con negro intermedio da hueco alto.
"""
import argparse, glob, importlib, json, os, re, shutil, subprocess, sys, tempfile, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from _common import FFMPEG, FFPROBE  # noqa: E402

RESULTS = []


def check(name, fn):
    t = time.time()
    try:
        ok, detail = fn()
    except Exception as e:  # noqa
        ok, detail = False, f"{type(e).__name__}: {e}"
    RESULTS.append((name, ok, detail, time.time() - t))
    print(f"  {'OK  ' if ok else 'FALLA'}  {name:<52} {detail}"[:200])
    return ok


def run(args, timeout=None, **kw):
    """Como subprocess.run, pero si vence el tiempo mata TODO el arbol de procesos (taskkill /T): un ffmpeg hijo no debe quedar huerfano."""
    p = subprocess.Popen([sys.executable] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace", **kw)
    try:
        out, err = p.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        subprocess.run(["taskkill", "/F", "/T", "/PID", str(p.pid)], capture_output=True)
        out, err = p.communicate()
        return subprocess.CompletedProcess(p.args, 124, out or "", (err or "") + "\nTIMEOUT: arbol de procesos cerrado")
    return subprocess.CompletedProcess(p.args, p.returncode, out, err)


def ff(args):
    return subprocess.run([FFMPEG, "-v", "error", "-y"] + args, capture_output=True, text=True)


def build_media(tmp):
    """base.mp4: rojo 2 s -> azul 2 s -> testsrc 2 s (cortes secos en 2.0 y 4.0), audio seno 6 s.
    gap.mp4: rojo 2 s -> NEGRO 0.3 s -> azul 2 s (hueco intermedio).  short_audio.mp4: base con solo 3 s de audio."""
    s = "320x240"
    base = os.path.join(tmp, "base.mp4")
    r = ff(["-f", "lavfi", "-i", f"color=c=red:s={s}:r=30:d=2", "-f", "lavfi", "-i", f"color=c=blue:s={s}:r=30:d=2",
            "-f", "lavfi", "-i", f"testsrc=s={s}:r=30:d=2", "-f", "lavfi", "-i", "sine=f=440:d=6:sample_rate=16000",
            "-filter_complex", "[0:v][1:v][2:v]concat=n=3:v=1:a=0[v]", "-map", "[v]", "-map", "3:a",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", base])
    gap = os.path.join(tmp, "gap.mp4")
    ff(["-f", "lavfi", "-i", f"color=c=red:s={s}:r=30:d=2", "-f", "lavfi", "-i", f"color=c=black:s={s}:r=30:d=0.3",
        "-f", "lavfi", "-i", f"color=c=blue:s={s}:r=30:d=2", "-filter_complex", "[0:v][1:v][2:v]concat=n=3:v=1:a=0[v]",
        "-map", "[v]", "-c:v", "libx264", "-pix_fmt", "yuv420p", gap])
    short = os.path.join(tmp, "short_audio.mp4")
    ff(["-i", base, "-c:v", "copy", "-af", "atrim=0:3", "-c:a", "aac", short])
    return base, gap, short, r.returncode == 0 and os.path.exists(base)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--speech", action="store_true"); ap.add_argument("--whisper", action="store_true")
    ap.add_argument("--network", action="store_true"); ap.add_argument("--hyperframes", action="store_true")
    ap.add_argument("--keep", action="store_true")
    a = ap.parse_args()
    tmp = tempfile.mkdtemp(prefix="vea_selftest_")
    print(f"Selftest video-editing-ai-agent  |  carpeta temporal: {tmp}\n")

    # ---------------- entorno
    check("ffmpeg y ffprobe encontrados", lambda: (os.path.exists(FFMPEG) or bool(shutil.which(FFMPEG))) and (True, FFMPEG))
    check("modulos: numpy, PIL", lambda: (__import__("numpy") and __import__("PIL") and (True, "numpy+PIL")))
    check("faster-whisper (voz, VAD)", lambda: (bool(__import__("importlib.util").util.find_spec("faster_whisper")), "faster_whisper"))
    base, gap, short, built = build_media(tmp)
    if not check("video sintetico creado con ffmpeg", lambda: (built, "base.mp4 6 s con cortes en 2.0 y 4.0")):
        print("\nNo se pudo crear el video de prueba; se aborta."); sys.exit(1)

    # ---------------- mapa de comprension
    out = os.path.join(tmp, "map")
    r = run([os.path.join(HERE, "video_understand.py"), base, "-o", out, "--no-transcribe", "--budget", "8"])
    data = {}
    if os.path.exists(os.path.join(out, "video-map.json")):
        data = json.load(open(os.path.join(out, "video-map.json"), encoding="utf-8"))
    check("video_understand: genera mapa, hojas y fotogramas", lambda: (r.returncode == 0 and bool(data.get("sheets")) and bool(data.get("keyframes")),
                                                                        f"{len(data.get('shots', []))} planos, {len(data.get('keyframes', []))} fotogramas"))
    check("video_understand: detecta 3 planos y cortes en 2.0 y 4.0", lambda: (
        len(data.get("shots", [])) == 3 and all(abs(s - e) < 0.15 for s, e in zip([x["start"] for x in data["shots"][1:]], [2.0, 4.0])),
        "cortes en " + ", ".join(str(x["start"]) for x in data.get("shots", [])[1:])))
    out2 = os.path.join(tmp, "map_short")
    r2 = run([os.path.join(HERE, "video_understand.py"), short, "-o", out2, "--no-transcribe", "--budget", "6"])
    d2 = json.load(open(os.path.join(out2, "video-map.json"), encoding="utf-8")) if os.path.exists(os.path.join(out2, "video-map.json")) else {}
    check("REGRESION: avisa si el audio es mas corto que el video", lambda: (any("MAS CORTO" in g for g in d2.get("gaps", [])), "aviso presente" if any("MAS CORTO" in g for g in d2.get("gaps", [])) else "sin aviso"))

    # ---------------- sondas
    p1 = os.path.join(tmp, "burst.png"); p2 = os.path.join(tmp, "diff.png"); p3 = os.path.join(tmp, "crop.png")
    rb = run([os.path.join(HERE, "frame_probe.py"), base, "--from", "1.8", "--to", "2.2", "--n", "4", "-o", p1])
    rd = run([os.path.join(HERE, "frame_probe.py"), base, "--at", "2.1", "--diff", "0.3", "-o", p2])
    rc = run([os.path.join(HERE, "frame_probe.py"), base, "--at", "1.0", "--crop", "0.1,0.1,0.5,0.5", "--scale", "2", "-o", p3])
    check("frame_probe: rafaga, --diff y --crop", lambda: (all(os.path.exists(p) and os.path.getsize(p) > 500 for p in (p1, p2, p3)) and rb.returncode == rd.returncode == rc.returncode == 0, "3 PNG"))

    # ---------------- cut_dip
    def dip(path, cut):
        r = run([os.path.join(HERE, "cut_dip.py"), path, "--cuts", str(cut), "--json", os.path.join(tmp, "dip.json")])
        return json.load(open(os.path.join(tmp, "dip.json"), encoding="utf-8"))[0]
    d_direct, d_gap = dip(base, 2.0), dip(gap, 2.15)
    check("cut_dip: corte directo = hueco 0 %", lambda: (d_direct.get("gap_max_pct", 99) < 2, f"hueco {d_direct.get('gap_max_pct')} %"))
    check("cut_dip: corte con negro intermedio = hueco alto", lambda: (d_gap.get("gap_max_pct", 0) > 50, f"hueco {d_gap.get('gap_max_pct')} %"))

    # ---------------- VAD
    def vad_sine():
        j = os.path.join(tmp, "vad.json")
        r = run([os.path.join(HERE, "vad_segments.py"), base, "-o", j])
        v = json.load(open(j, encoding="utf-8")) if os.path.exists(j) else {}
        return r.returncode == 0 and v.get("speech_ratio", 1) < 0.3, f"speech_ratio {v.get('speech_ratio')} (un seno NO es voz)"
    check("vad_segments: un tono puro no cuenta como voz", vad_sine)

    # ---------------- fetch_reference (sin red) y regresiones
    fr = importlib.import_module("fetch_reference")
    skill_inside = os.path.join(fr.SKILL_DIR, "referencias_x")
    r_in = run([os.path.join(HERE, "fetch_reference.py"), "info", "https://example.com/x", "-o", skill_inside])
    check("fetch_reference: se niega a escribir dentro de la skill", lambda: (r_in.returncode != 0 and "no se escribe" in (r_in.stdout + r_in.stderr), "rechazado"))
    r_url = run([os.path.join(HERE, "fetch_reference.py"), "info", "ftp://x", "-o", os.path.join(tmp, "ref")])
    check("fetch_reference: rechaza URL que no sea http(s)", lambda: (r_url.returncode != 0 and "http" in (r_url.stdout + r_url.stderr), "rechazada"))
    other = "C:\\" if os.path.splitdrive(fr.SKILL_DIR)[0].upper() != "C:" else "D:\\"
    check("REGRESION: inside() no falla entre discos distintos", lambda: (fr.inside(os.path.join(other, "tmp", "x"), fr.SKILL_DIR) is False, f"{other} vs {fr.SKILL_DIR[:2]}"))
    orig = fr.run
    fr.run = lambda cmd: (101, "{}", "")
    try:
        class A:  # args minimos
            cookies_from_browser = None; cookies_always = False
        code, _, _, _ = fr.attempt(A(), lambda c: ["x"])
    finally:
        fr.run = orig
    check("REGRESION: codigo 101 de yt-dlp cuenta como exito", lambda: (code == 0, f"codigo {code}"))
    check("yt-dlp instalado", lambda: ((lambda rr: (rr.returncode == 0, "version " + rr.stdout.strip().splitlines()[-1]) if rr.returncode == 0 else (False, "no instalado: pip install \"yt-dlp[default]\""))(run(["-m", "yt_dlp", "--version"]))))

    # ---------------- subtitulos para HyperFrames (agrupacion, sin render)
    def captions_rules():
        import random
        rnd = random.Random(7)
        words, t = [], 0.4
        for i in range(120):
            d = rnd.uniform(0.18, 0.5)
            w = "palabra%d" % i + ("." if i % 9 == 8 else "," if i % 5 == 4 else "")
            words.append({"w": w, "s": round(t, 3), "e": round(t + d, 3)})
            t += d + (rnd.choice([0.02, 0.05, 0.1, 0.5]) if i % 7 else 0.02)
        hc = importlib.import_module("hf_captions")
        g = hc.group_words(words, fps=30)
        sizes = [len(x["words"]) for x in g]
        covered = sum(sizes) == len(words)
        order_ok = all(b["start"] >= a["end"] for a, b in zip(g, g[1:]))
        dur_ok = all(x["end"] - x["start"] >= 0.5 - 1e-6 for x in g[:-1])
        size_ok = all(2 <= n <= 5 for n in sizes[:-1])
        return covered and order_ok and dur_ok and size_ok, f"{len(g)} rotulos, {min(sizes)}-{max(sizes)} palabras, sin solapes={order_ok}, >=0.5 s={dur_ok}"
    check("hf_captions: 2-5 palabras, >=0.5 s, sin solapes, todo cubierto", captions_rules)

    # ---------------- video-aprender: pantalla/pizarra, biblioteca de aprendizajes y llamada unica (sin Whisper)
    def build_board():
        from PIL import Image, ImageDraw, ImageFont
        try:
            f1 = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 54); f2 = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 40)
        except Exception:
            f1 = f2 = ImageFont.load_default()
        eq = ["PV = FV / (1 + r)^n", "FV = PV * (1 + r)^n", "n = ln(FV/PV) / ln(1 + r)"]

        def slide(name, title, lines, bg):
            im = Image.new("RGB", (1920, 1080), bg)
            d = ImageDraw.Draw(im)
            d.text((100, 80), title, fill=(20, 20, 60), font=f1)
            for i, l in enumerate(lines):
                d.text((120, 260 + i * 110), l, fill=(30, 30, 30), font=f2)
            pth = os.path.join(tmp, name); im.save(pth); return pth
        seq = [(slide("b1.png", "Valor del dinero", ["Hoy vale mas que manana"], (250, 250, 245)), 3)]
        seq += [(slide(f"bw{k}.png", "Formulas", eq[:k], (255, 255, 255)), 3) for k in (1, 2, 3)]
        seq += [(slide("b5.png", "Resumen", ["Tasa r", "Periodos n"], (240, 248, 255)), 3)]
        args = ["-y"]
        for pth, d in seq:
            args += ["-loop", "1", "-t", str(d), "-framerate", "10", "-i", pth]
        n = len(seq)
        args += ["-filter_complex", "".join(f"[{i}:v]" for i in range(n)) + f"concat=n={n}:v=1:a=0,format=yuv420p[v]", "-map", "[v]", "-c:v", "libx264", os.path.join(tmp, "pizarra.mp4")]
        ff(args)
        ff(["-loop", "1", "-t", "20", "-framerate", "10", "-i", os.path.join(tmp, "bw3.png"), "-c:v", "libx264", "-crf", "38", "-pix_fmt", "yuv420p", os.path.join(tmp, "estatica.mp4")])
        return os.path.exists(os.path.join(tmp, "pizarra.mp4")) and os.path.exists(os.path.join(tmp, "estatica.mp4"))
    board_ok = build_board()

    def slides_ok():
        out = os.path.join(tmp, "slides_out")
        r = run([os.path.join(HERE, "slides_extract.py"), os.path.join(tmp, "pizarra.mp4"), "-o", out], timeout=120)
        d = json.load(open(os.path.join(out, "slides.json"), encoding="utf-8"))["slides"]
        ts = [x["t"] for x in d]
        want = [0.0, 3.5, 6.5, 9.5, 12.5]
        ok = r.returncode == 0 and len(ts) == 5 and all(abs(a - b) <= 1.0 for a, b in zip(ts, want))
        return ok, f"{len(ts)} estados en {ts} (esperado ~{want})"
    check("slides_extract: detecta una linea nueva de ecuacion y cada diapositiva", slides_ok if board_ok else (lambda: (False, "no se pudo crear el video de pizarra")))

    def static_ok():
        out = os.path.join(tmp, "static_out")
        run([os.path.join(HERE, "slides_extract.py"), os.path.join(tmp, "estatica.mp4"), "-o", out], timeout=120)
        n = len(json.load(open(os.path.join(out, "slides.json"), encoding="utf-8"))["slides"])
        return n == 1, f"{n} estado(s) en una diapositiva estatica muy comprimida (esperado 1: sin ruido de compresion)"
    check("slides_extract: sin falsos positivos por ruido de compresion", static_ok if board_ok else (lambda: (False, "sin video")))

    def learnings_rules():
        env = dict(os.environ, VEA_MEMORY_DIR=os.path.join(tmp, "memoria"))
        sl = os.path.join(HERE, "save_learning.py")
        for i, src in enumerate(["https://youtu.be/AAAAAAAAAAA", "https://youtu.be/BBBBBBBBBBB", "C:/x/c.mp4"]):
            run([sl, "add", "--source", src, "--when", "gancho", "--do", "cortar cada 2 s", "--evidence", f"#0{i} 00:0{i}; 2.{i} s/plano"], env=env)
        no_quote = run([sl, "promote", "A001", "--by", "usuario"], env=env).returncode != 0
        two = run([sl, "promote", "A001", "--by", "repeticion", "--with", "A002", "--why", "mismo patron de corte"], env=env).returncode != 0
        three = run([sl, "promote", "A001", "--by", "repeticion", "--with", "A002,A003", "--why", "mismo patron de corte"], env=env).returncode == 0
        return no_quote and two and three, f"sin cita rechaza={no_quote}, 2 fuentes rechaza={two}, 3 fuentes distintas aprueba={three}"
    check("save_learning: un candidato solo se promueve con cita o 3 fuentes", learnings_rules)

    def aprender_call():
        out = os.path.join(tmp, "aprender_out")
        r = run([os.path.join(HERE, "video_aprender.py"), os.path.join(tmp, "pizarra.mp4"), "--modo", "contenido", "--no-transcribe", "--goal", "prueba", "-o", out], timeout=180)
        ok = r.returncode == 0 and all(os.path.exists(os.path.join(out, f)) for f in ("contenido.md", "analisis.md", os.path.join("pantalla", "slides.json")))
        return ok, "contenido.md + analisis.md + pantalla/ creados" if ok else (r.stderr or r.stdout)[-150:]
    check("video_aprender: una llamada genera contenido.md, analisis.md y pantalla/", aprender_call if board_ok else (lambda: (False, "sin video")))

    def utf8_print():
        code = "import sys; sys.path.insert(0, r'%s'); import _common; print('Ses 2\uff1a Present Value \u00e9\u4e2d')" % HERE
        r = run(["-c", code])
        return r.returncode == 0 and "Present Value" in r.stdout, "imprime un titulo con \uff1a por una tuberia (cp1252) sin UnicodeEncodeError" if r.returncode == 0 else r.stderr[-120:]
    check("REGRESION: imprimir titulos con caracteres raros por una tuberia (Windows)", utf8_print)

    # ---------------- video-aprender: --roi y alineacion de diapositivas PDF (con casos NEGATIVOS)
    def roi_ok():
        res = {}
        for nombre, roi in (("izquierda", "0,0.15,0.5,0.8"), ("derecha", "0.55,0.15,0.4,0.8")):
            out = os.path.join(tmp, "roi_" + nombre)
            run([os.path.join(HERE, "slides_extract.py"), os.path.join(tmp, "pizarra.mp4"), "-o", out, "--roi", roi], timeout=120)
            res[nombre] = len(json.load(open(os.path.join(out, "slides.json"), encoding="utf-8"))["slides"])
        return res["izquierda"] == 5 and res["derecha"] == 1, f"region con el texto: {res['izquierda']} estados (esperado 5); region vacia: {res['derecha']} (esperado 1)"
    check("slides_extract --roi: vigila solo la region pedida", roi_ok if board_ok else (lambda: (False, "sin video")))

    def align_ok():
        import fitz
        va = importlib.import_module("video_aprender")
        temas = [["perpetuidad", "creciente", "flujo", "descuento", "valuacion", "formula", "infinito", "convergencia"],
                 ["anualidad", "periodos", "pagos", "tabla", "factor", "constante", "cuotas", "amortizacion"],
                 ["inflacion", "nominal", "real", "rendimiento", "capitalizacion", "compuesto", "precios", "deflactor"],
                 ["bonos", "cupon", "vencimiento", "tasa", "emision", "rendimiento", "duracion", "convexidad"],
                 ["opciones", "prima", "ejercicio", "volatilidad", "cobertura", "derivados", "subyacente", "delta"],
                 ["riesgo", "diversificacion", "correlacion", "portafolio", "varianza", "covarianza", "beta", "mercado"],
                 ["apalancamiento", "deuda", "capital", "estructura", "impuestos", "escudo", "costo", "quiebra"],
                 ["subasta", "oferta", "informacion", "valor", "privada", "licitacion", "comprador", "precio"]]
        doc = fitz.open()
        for t in temas:
            pg = doc.new_page(); pg.insert_text((72, 100), "Diapositiva\n" + "\n".join(t), fontsize=20)
        pdf = os.path.join(tmp, "d.pdf"); doc.save(pdf)
        pages = va.render_pdf(pdf, os.path.join(tmp, "dpages"))
        # voz sintetica: 0-60 s habla de la pagina 1, 60-120 de la 2, 120-180 de la 3 (cada frase usa 4 palabras de ese tema)
        segs = []
        for k in range(3):
            for i in range(6):
                w = temas[k]
                segs.append({"s": k * 60 + i * 10, "e": k * 60 + i * 10 + 8, "text": f"hablamos de la {w[0]} y la {w[1]} con {w[2]} y {w[3]} {w[4]}", "suspect": False})
        al, nb, _m = va.align_pages(pages, segs)
        orden = [al[k]["t0"] for k in sorted(al)]
        pos = sorted(al) == [1, 2, 3] and orden == sorted(orden) and abs(al[2]["t0"] - 60) <= 30
        # NEGATIVO: una charla sin relacion con las diapositivas (como la apertura de la clase real) no debe asignar nada con evidencia
        neg = [{"s": i * 10, "e": i * 10 + 8, "text": "la subasta del telefono fue interesante y los estudiantes compraron cosas baratas", "suspect": False} for i in range(12)]
        al2, _, _m2 = va.align_pages(pages, neg)
        # la unica diapositiva con 'subasta' es la 8: puede salir como mucho esa; nunca paginas 1-7
        neg_ok = all(k == 8 for k in al2)
        # NEGATIVO DURO: coincidencias FUERTES pero INCOHERENTES (cada ventana habla de una pagina distinta, saltando por todo el documento
        # como la charla ajena de la clase real): la puerta de coherencia debe rechazarlo todo
        salto = [0, 7, 2, 5, 1, 6, 3, 4, 7, 0, 5, 2]
        inc = [{"s": i * 30, "e": i * 30 + 25, "text": " ".join(f"{temas[pg][k]} {temas[pg][k + 1]}" for pg in [salto[i]] for k in (0, 2, 4)), "suspect": False} for i in range(12)]
        al3, _, m3 = va.align_pages(pages, inc)
        coh_ok = not al3 and (m3.get("coherencia") is not None and m3["coherencia"] < 0.7)
        return pos and neg_ok and coh_ok, f"positivo: paginas {sorted(al)} en orden temporal={orden == sorted(orden)}; negativo: {sorted(al2) or 'ninguna'}; incoherente: {sorted(al3) or 'ninguna'} (coherencia {m3.get('coherencia')})"
    check("video_aprender: alinea paginas PDF con la voz y no inventa sin evidencia", align_ok)

    def tree_kill():
        va = importlib.import_module("video_aprender")
        mk = os.path.join(tmp, "hijo_vivo.txt")
        hijo = os.path.join(tmp, "hijo.py")
        padre = os.path.join(tmp, "padre.py")
        open(hijo, "w", encoding="utf-8").write(f"import time\ntime.sleep(7)\nopen(r'{mk}', 'w').write('x')\n")
        open(padre, "w", encoding="utf-8").write(f"import subprocess, sys, time\nsubprocess.Popen([sys.executable, r'{hijo}'])\ntime.sleep(60)\n")
        t0 = time.time()
        r = va.run_tree([padre], 2)
        dt = time.time() - t0
        time.sleep(9)                                  # el hijo escribiria su marca a los 7 s si siguiera vivo
        vivo = os.path.exists(mk)
        return r is None and dt < 10 and not vivo, f"vencio a los {dt:.1f} s: {r is None}; el proceso hijo {'SOBREVIVIO (huerfano)' if vivo else 'fue cerrado'}"
    check("REGRESION: el tiempo limite cierra tambien a los procesos hijos (no deja ffmpeg huerfano)", tree_kill)

    def beatgrid_ok():
        import wave, numpy as np
        bg = importlib.import_module("beat_grid")
        sr, T0, ph0, dur = 22050, 60 / 122.0, 0.2, 16
        x = np.zeros(int(sr * dur), dtype=np.float32)
        k = 0
        while ph0 + k * T0 < dur - 0.3:
            i = int((ph0 + k * T0) * sr)
            n = int(0.12 * sr)
            tt = np.arange(n) / sr
            x[i:i + n] += (np.sin(2 * np.pi * 60 * tt) * np.exp(-tt * 28)).astype(np.float32)   # bombo sintetico
            k += 1
        x += np.random.default_rng(3).normal(0, 0.01, len(x)).astype(np.float32)
        r = bg.fit(x, 80, 170)
        err_ph = ((r["t0"] - ph0 + T0 / 2) % T0) - T0 / 2
        # REGRESION: la autocorrelacion gruesa daba 123 BPM (lag entero de 23 ms): el ajuste fino debe dar 122.0
        return abs(r["bpm"] - 122.0) < 0.12 and abs(err_ph) < 0.02, f"BPM {r['bpm']:.2f} (real 122.00), fase {err_ph * 1000:+.0f} ms"
    check("REGRESION: beat_grid ajusta el compas a 0.1 BPM (la autocorrelacion gruesa se desviaba 1 BPM)", beatgrid_ok)

    def approved_rules():
        mem = os.path.join(tmp, "mem_aprobados")
        env = dict(os.environ, VEA_MEMORY_DIR=mem)
        base = [os.path.join(HERE, "save_approved.py"), "add", "--name", "Prueba", "--project", tmp, "--piece", "Reel", "--format", "1080x1920", "--duration", "10",
                "--route", "musica-al-compas", "--engine", "hyperframes", "--message", "m", "--structure", "a > b", "--recipe", "r", "--good", "algo bueno", "--tags", "reel,musica"]
        sin = run(base + ["--quote", ""], env=env)                                    # sin cita: debe rechazar
        sin_leccion = run([x for x in base if x not in ("--good", "algo bueno")] + ["--quote", "genial, aprobado"], env=env)  # sin lecciones: debe rechazar
        con = run(base + ["--quote", "genial, aprobado", "--open", "con o sin empuje"], env=env)
        sug = run([os.path.join(HERE, "save_approved.py"), "suggest", "--route", "musica-al-compas"], env=env)
        rec = run([os.path.join(HERE, "save_approved.py"), "recipe", "V001"], env=env)
        ok = (sin.returncode != 0 and sin_leccion.returncode != 0 and con.returncode == 0 and "V001" in sug.stdout
              and "genial, aprobado" in rec.stdout and "con o sin empuje" in rec.stdout)
        return ok, f"sin cita rechaza={sin.returncode != 0}; sin lecciones rechaza={sin_leccion.returncode != 0}; con cita guarda={con.returncode == 0}; suggest/recipe ok={'V001' in sug.stdout}"
    check("save_approved: un video solo se aprueba con la cita del usuario y guarda lo sin decidir", approved_rules)

    def approved_suggest_none():
        mem = os.path.join(tmp, "mem_vacia")
        r = run([os.path.join(HERE, "save_approved.py"), "suggest", "--route", "inexistente", "--tag", "x"], env=dict(os.environ, VEA_MEMORY_DIR=mem))
        return r.returncode == 0 and "Ningún" in r.stdout.replace("Ning�n", "Ningún"), "sin coincidencias no falla ni inventa (REGRESION: suggest sin un filtro fallaba con TypeError)"
    check("REGRESION: save_approved suggest con un solo filtro no revienta", approved_suggest_none)

    def motion_ok():
        r = run([os.path.join(HERE, "motion_energy.py"), base, "--min-run", "0.5"], timeout=120)
        return r.returncode == 0 and "tramos quietos" in r.stdout and "movimiento medio" in r.stdout, "reporta movimiento por segundo y tramos quietos (el video sintetico tiene dos colores fijos)"
    check("motion_energy: mide movimiento por segundo y tramos quietos", motion_ok)

    def hs_prod():
        r = run([os.path.join(HERE, "handshake.py"), "--json"])
        d = json.loads(r.stdout)
        pr = d.get("production", {})
        hf = d.get("engines", {}).get("hyperframes", {})
        ok = all(pr.get("scripts", {}).get(n) for n in ("beat_grid.py", "motion_energy.py", "save_approved.py")) and pr.get("preflight") and "status" in hf and "env_block_git_bash" in hf
        return ok, f"production.scripts ok, preflight={pr.get('preflight')}, hyperframes.status={hf.get('status')}, videos aprobados={pr.get('approved_videos', {}).get('count')}"
    check("handshake v1.4: bloque production y HyperFrames con variables de entorno", hs_prod)

    def glosario_ok():
        va = importlib.import_module("video_aprender")
        va.GLOS = va.cargar_glosario("trading")
        try:
            a = va.fx("el modelo Garche y el exponente de Horst, el shared ratio y el esoblos del Cuckoo con tripela barrera")
            neutro = va.fx("escriba la palabra Horst y mira tu directo")        # sin contexto de Hurst no se toca
        finally:
            va.GLOS = None
        ok = all(t in a for t in ("GARCH", "exponente de Hurst", "Sharpe ratio", "stop loss", "QQQ", "triple barrera")) and "Horst" in neutro
        return ok, f"corrige los errores de oido conocidos y no toca 'Horst' fuera de contexto: {a[:70]}..."
    check("video_aprender: el glosario de trading corrige terminos mal oidos sin inventar", glosario_ok)

    def hotwords_ok():
        import inspect
        va = importlib.import_module("video_aprender")
        from faster_whisper import WhisperModel
        return ("hotwords" in inspect.signature(va.transcribe_long).parameters and "hotwords" in inspect.signature(WhisperModel.transcribe).parameters,
                "el vocabulario va como hotwords (initial_prompt solo actua en la 1.a ventana de 30 s con condition_on_previous_text=False)")
    check("video_aprender: el vocabulario llega al reconocedor como hotwords", hotwords_ok)

    def muestreo_ok():
        va = importlib.import_module("video_aprender")
        out_m = os.path.join(tmp, "muestreo_test")
        r = va.muestrear(base, out_m, None, 6.0, 3)
        files = [os.path.join(out_m, m["file"]) for m in r["fotogramas"]]
        return (len(files) == 3 and all(os.path.exists(f) and os.path.getsize(f) > 500 for f in files) and os.path.exists(os.path.join(out_m, r["hoja"])),
                f"{len(files)} fotogramas nitidos + hoja de contacto (pantalla sin estados estables: persona/camara)")
    check("video_aprender: el muestreo de fotogramas genera imagenes y hoja de contacto", muestreo_ok)

    def lote_ok():
        fuentes = os.path.join(tmp, "fuentes.txt")
        open(fuentes, "w", encoding="utf-8").write("# prueba" + chr(10) + base + chr(10) + chr(10) + gap + chr(10))
        out_l = os.path.join(tmp, "lote_test")
        args = [os.path.join(HERE, "aprender_lote.py"), fuentes, "-o", out_l, "--prefijo", "t", "--pausa", "0", "--extra", "--no-transcribe --sin-pantalla"]
        dry = run(args + ["--dry-run"], timeout=60)
        r1 = run(args, timeout=240)
        res = os.path.join(out_l, "lote-resumen.md")
        txt = open(res, encoding="utf-8").read() if os.path.exists(res) else ""      # se lee ANTES de la 2.a corrida (la reescribe con "ya estaba")
        r2 = run(args, timeout=240)
        ok = (dry.returncode == 0 and "DRY-RUN" in dry.stdout and r1.returncode == 0 and txt.count("| OK |") == 2 and r2.returncode == 0 and r2.stdout.count("ya procesado") == 2)
        return ok, ("dry-run ok, 2 fuentes procesadas (resumen con 2 OK), segunda corrida salta las 2 ya hechas" if ok else f"dry={dry.returncode} r1={r1.returncode} OK={txt.count(chr(124) + chr(32) + chr(79) + chr(75))} r2skip={r2.stdout.count(chr(121) + chr(97) + chr(32) + chr(112))} err={(r1.stderr or r1.stdout)[-160:]!r}")
    check("aprender_lote: procesa varias fuentes, escribe el resumen y es reanudable", lote_ok)

    # ---------------- handshake
    def hs():
        r = run([os.path.join(HERE, "handshake.py"), "--json"])
        d = json.loads(r.stdout)
        md = open(os.path.join(os.path.dirname(HERE), "SKILL.md"), encoding="utf-8").read()
        m = re.search(r"\(v(\d+\.\d+)\)", md)
        same = bool(m) and d.get("skill_version", "").startswith(m.group(1))
        return r.returncode == 0 and "video_understanding" in d and same, f"handshake {d.get('skill_version')} vs SKILL.md v{m.group(1) if m else '?'}; ready={d.get('video_understanding', {}).get('ready')}"
    check("handshake: capacidades y version = SKILL.md", hs)

    # ---------------- opcionales
    if a.speech or a.whisper:
        wav = os.path.join(tmp, "habla.wav")
        ps1 = os.path.join(tmp, "tts.ps1")
        open(ps1, "w", encoding="utf-8").write(
            "Add-Type -AssemblyName System.Speech\n$s = New-Object System.Speech.Synthesis.SpeechSynthesizer\n"
            f"$s.SetOutputToWaveFile('{wav}')\n$s.Speak('This is a test of the voice activity detector. One. Two. Three. The quick brown fox jumps over the lazy dog.')\n$s.Dispose()\n")
        subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", ps1], capture_output=True)
        if os.path.exists(wav) and os.path.getsize(wav) > 1000:
            def vad_speech():
                j = os.path.join(tmp, "vad_sp.json")
                run([os.path.join(HERE, "vad_segments.py"), wav, "-o", j])
                v = json.load(open(j, encoding="utf-8"))
                return v["speech_ratio"] > 0.5, f"speech_ratio {v['speech_ratio']} sobre voz sintetica"
            check("vad_segments: detecta voz sintetica (SAPI)", vad_speech)

            def carve():
                bed = os.path.join(tmp, "ruido.wav")
                ff(["-f", "lavfi", "-i", "anoisesrc=color=pink:duration=14:amplitude=0.5:sample_rate=48000", "-ac", "2", bed])
                outm = os.path.join(tmp, "mezcla.wav")
                t0 = time.time()
                r = run([os.path.join(HERE, "carve_music.py"), "--voice", wav, "--bed", bed, "-o", outm, "--strength", "0.8", "--verify"], timeout=150)
                dt = time.time() - t0
                m = {k: float(v) for k, v in re.findall(r"^\s+(graves|medios|agudos)\s+([+-]?\d+\.\d)", r.stdout, re.M)}
                ok = r.returncode == 0 and len(m) == 3 and m["medios"] <= -4 and abs(m["graves"]) <= 2.5 and abs(m["agudos"]) <= 2.5 and dt < 60
                return ok, f"medios {m.get('medios')} dB, graves {m.get('graves')}, agudos {m.get('agudos')}, {dt:.0f} s (limite 60 s: guarda contra el bloqueo de alimiter)"
            check("carve_music: baja solo la banda de la voz y no se cuelga", carve)
            if a.whisper:
                vid = os.path.join(tmp, "habla.mp4")
                ff(["-f", "lavfi", "-i", "color=c=gray:s=320x240:r=30:d=8", "-i", wav, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", vid])
                o3 = os.path.join(tmp, "map_sp")
                run([os.path.join(HERE, "video_understand.py"), vid, "-o", o3, "--lang", "en", "--budget", "4"])
                d3 = json.load(open(os.path.join(o3, "video-map.json"), encoding="utf-8"))
                check("video_understand + Whisper: voz fiable en voz sintetica", lambda: (d3.get("speech_seconds", 0) > 2, f"{d3.get('speech_seconds')} s de voz fiable"))
        else:
            print("  OMITIDA  voz sintetica: no hay voz SAPI disponible en este Windows")

    if a.network:
        r = run([os.path.join(HERE, "fetch_reference.py"), "info", "https://www.youtube.com/watch?v=YE7VzlLtp-4", "-o", os.path.join(tmp, "ref_net")])
        check("fetch_reference info (YouTube, red)", lambda: (r.returncode == 0 and "Big Buck Bunny" in r.stdout, (r.stdout.strip().splitlines() or [r.stderr[-100:]])[0][:100]))

    if a.hyperframes:
        node = shutil.which("node")
        ver = subprocess.run([node, "--version"], capture_output=True, text=True).stdout.strip() if node else ""
        check("HyperFrames: Node >= 22", lambda: (bool(ver) and int(ver.lstrip("v").split(".")[0]) >= 22, ver or "node no encontrado"))
        shells = glob.glob(os.path.join(os.environ.get("LOCALAPPDATA", ""), "ms-playwright", "chromium_headless_shell-*", "chrome-headless-shell-win64", "chrome-headless-shell.exe"))
        check("HyperFrames: chrome-headless-shell de Playwright", lambda: (bool(shells), shells[-1] if shells else "no encontrado (ver references/engine-hyperframes.md)"))

    # ---------------- resumen
    bad = [r for r in RESULTS if not r[1]]
    print(f"\n{len(RESULTS) - len(bad)}/{len(RESULTS)} pruebas OK  ({sum(r[3] for r in RESULTS):.0f} s)")
    if a.keep:
        print("carpeta conservada:", tmp)
    else:
        shutil.rmtree(tmp, ignore_errors=True)
    if bad:
        print("FALLAN:", "; ".join(r[0] for r in bad))
        sys.exit(1)


if __name__ == "__main__":
    main()
