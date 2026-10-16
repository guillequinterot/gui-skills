#!/usr/bin/env python
"""Extrae los ESTADOS ESTABLES de una pantalla/pizarra/diapositiva (para leer ecuaciones, graficos, codigo, hojas de calculo).

El detector de planos de video_understand.py mira cambios de COLOR y no sirve aqui: una diapositiva que gana una linea de
ecuacion cambia ~1 % de los pixeles. Este script compara la pantalla contra la ULTIMA captura y guarda un fotograma nuevo
cuando (a) cambio una fraccion suficiente de BLOQUES de 8x8 y (b) la imagen ya se quedo quieta (no cojas la animacion a medias).

Uso:
  python slides_extract.py video.mp4 [-o carpeta] [--sens 1.0] [--max 40] [--min-gap 3] [--size 1280] [--from 0 --to 600]
  --sens      >1 detecta cambios mas pequenos (pizarra con una linea nueva), <1 solo cambios grandes (cambio de diapositiva)
  --max       tope de capturas (si hay mas, sube el umbral solo hasta cumplirlo y lo avisa)
  --min-gap   segundos minimos entre capturas
  --roi       region x,y,w,h (fracciones 0-1) a vigilar: en un VIDEO DE AULA con la diapositiva proyectada en un rincon, el profesor
              se mueve y el cuadro completo nunca esta quieto; vigilando solo la pantalla proyectada si se detectan sus cambios.
              OJO: recortar no inventa resolucion: si la pantalla ocupa 190 px del video, las ecuaciones NO seran legibles.
  --size      lado largo de cada captura en px (1280 permite leer ecuaciones; sube a 1600 si son muy pequenas)
Salida: <carpeta>/slides/slide_NN_mmss.jpg, slides.json (n, t, t_hasta, cambio %, nitidez) y hojas 2x2 en overview/.
Limites honestos: una camara de personas en movimiento NO tiene estados estables (saldran pocas capturas); no hace OCR (Claude
lee las imagenes con Read); texto muy pequeno puede requerir recortar y ampliar con frame_probe.py --crop --scale.
"""
import argparse, json, math, os, shutil, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import FFMPEG, probe_duration, probe_stream  # noqa: E402

W = 320                    # ancho de analisis; el alto se calcula (multiplo de 8) segun la region
BG, ACC = (18, 18, 22), (255, 140, 60)


def tc(t):
    return f"{int(t // 60):02d}:{t % 60:05.2f}"


def font(sz):
    for f in (r"C:\Windows\Fonts\consola.ttf", r"C:\Windows\Fonts\arial.ttf"):
        if os.path.exists(f):
            return ImageFont.truetype(f, sz)
    return ImageFont.load_default()


def analysis_size(path, roi):
    """(ancho, alto) de analisis: ancho 320 y alto multiplo de 8 respetando la proporcion de la region."""
    st = probe_stream(path)
    vw, vh = float(st.get("width") or 16), float(st.get("height") or 9)
    rot = 0
    for sd in st.get("side_data_list", []) or []:
        if "rotation" in sd:
            rot = int(round(float(sd["rotation"]))) % 360
    if rot in (90, 270):
        vw, vh = vh, vw
    rw, rh = (vw * roi[2], vh * roi[3]) if roi else (vw, vh)
    return W, max(8, int(round(W * rh / rw / 8)) * 8)


def roi_filter(roi):
    if not roi:
        return ""
    x, y, w, h = roi
    return f"crop=iw*{w}:ih*{h}:iw*{x}:ih*{y},"


def decode_gray(path, fps, t0, dur, roi=None):
    wa, ha = analysis_size(path, roi)
    cmd = [FFMPEG, "-v", "error"]
    if t0:
        cmd += ["-ss", f"{t0:.3f}"]
    if dur:
        cmd += ["-t", f"{dur:.3f}"]
    cmd += ["-i", path, "-an", "-vf", f"fps={fps},{roi_filter(roi)}scale={wa}:{ha}:flags=area,format=gray", "-f", "rawvideo", "-"]
    raw = subprocess.run(cmd, capture_output=True).stdout
    n = len(raw) // (wa * ha)
    return np.frombuffer(raw[: n * wa * ha], np.uint8).reshape(n, ha, wa)


def block_change(a, b, blk=8, level=10):
    """Fraccion de BLOQUES 8x8 cuya diferencia media supera `level` (0-255). Un trazo de texto cambia bloques enteros;
    el ruido de compresion casi nunca cambia un bloque entero -> mucho mas robusto que contar pixeles sueltos."""
    h, w = a.shape
    d = np.abs(a.astype(np.int16) - b.astype(np.int16)).reshape(h // blk, blk, w // blk, blk).mean(axis=(1, 3))
    return float((d > level).mean())


def detect(frames, fps, thr, min_gap, quiet=0.0035):
    """Indices de fotogramas a capturar (estado estable que difiere de la ultima captura)."""
    n = len(frames)
    prev = np.zeros(n)
    for i in range(1, n):
        prev[i] = block_change(frames[i], frames[i - 1])
    caps, ref, last_t = [], None, -1e9
    for i in range(n - 2):
        still = prev[i + 1] <= quiet and prev[i + 2] <= quiet and prev[i] <= quiet * 3          # ya quieta ~1 s
        if not still:
            continue
        t = i / fps
        ch = 1.0 if ref is None else block_change(frames[i], frames[ref])
        blank = float(frames[i].std()) < 3 and float(frames[i].mean()) < 12                     # negro puro: no es una diapositiva
        if (ref is None or ch >= thr) and (ref is None or t - last_t >= min_gap) and not blank:
            caps.append((i, ch))
            ref, last_t = i, t
    # el ultimo estado estable, si difiere de la ultima captura (cierre de la explicacion)
    for i in range(n - 1, max(n - 2 * int(fps * 6), 2), -1):
        if prev[i] <= quiet and prev[max(i - 1, 0)] <= quiet:
            if ref is not None and i != ref:
                ch = block_change(frames[i], frames[ref])
                if ch >= thr * 0.7 and i / fps - last_t >= min_gap:
                    caps.append((i, ch))
            break
    return caps


def sharp(img):
    g = np.asarray(img.convert("L").resize((256, max(int(256 * img.height / img.width), 8))), np.float32)
    lap = g[1:-1, 1:-1] * 4 - g[:-2, 1:-1] - g[2:, 1:-1] - g[1:-1, :-2] - g[1:-1, 2:]
    return float(lap.var())


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video"); ap.add_argument("-o", "--out"); ap.add_argument("--sens", type=float, default=1.0)
    ap.add_argument("--max", type=int, default=40); ap.add_argument("--min-gap", type=float, default=3.0)
    ap.add_argument("--size", type=int, default=1280); ap.add_argument("--fps", type=float, default=2.0)
    ap.add_argument("--roi", help="region a vigilar x,y,w,h en FRACCIONES 0-1 (p. ej. 0.04,0.12,0.39,0.44 = la pantalla proyectada en un video de aula)")
    ap.add_argument("--from", dest="t0", type=float, default=0.0); ap.add_argument("--to", dest="t1", type=float, default=0.0)
    a = ap.parse_args()
    video = os.path.abspath(a.video)
    if not os.path.exists(video):
        sys.exit("no existe: " + video)
    dur = probe_duration(video)
    roi = tuple(float(v) for v in a.roi.split(",")) if a.roi else None
    if roi and (len(roi) != 4 or not all(0 <= v <= 1 for v in roi) or roi[0] + roi[2] > 1.001 or roi[1] + roi[3] > 1.001):
        sys.exit("--roi necesita x,y,w,h entre 0 y 1 y que la region quepa en el cuadro")
    span = (a.t1 or dur) - a.t0
    out = os.path.abspath(a.out or os.path.join(os.path.dirname(video), "lectura", os.path.splitext(os.path.basename(video))[0]))
    sd, od = os.path.join(out, "slides"), os.path.join(out, "overview")
    for d in (sd, od):
        shutil.rmtree(d, ignore_errors=True)
        os.makedirs(d, exist_ok=True)

    print(f"decodificando {span:.0f} s a {a.fps} fps (gris{', region ' + a.roi if roi else ''}) ...")
    frames = decode_gray(video, a.fps, a.t0, span, roi)
    if len(frames) < 6:
        sys.exit("muy pocos fotogramas decodificados")
    thr = 0.007 / max(a.sens, 0.05)                     # 0.7 % de los bloques (~6 de 880) = una linea corta de texto nueva
    caps = detect(frames, a.fps, thr, a.min_gap)
    raised = 0
    while len(caps) > a.max and raised < 8:
        thr *= 1.5
        raised += 1
        caps = detect(frames, a.fps, thr, a.min_gap)
    if raised:
        print(f"AVISO: habia mas de {a.max} estados; se subio el umbral {raised} vez/veces (ahora {thr * 100:.1f} % de bloques). Si se pierde detalle, usa --max mas alto o --from/--to por tramos.")
    moving = float(np.mean([np.abs(frames[i].astype(np.int16) - frames[i - 1].astype(np.int16)).mean() for i in range(1, len(frames), max(len(frames) // 200, 1))]))
    if len(caps) < 3 and span > 60:
        print("AVISO: muy pocas capturas para un video largo: probablemente es camara de personas/video en movimiento y no una pantalla. "
              "Prueba --sens 2, o usa el modo estilo (planos) en vez de este.")

    slides = []
    for k, (i, ch) in enumerate(caps, 1):
        t = a.t0 + i / a.fps
        p = os.path.join(sd, f"slide_{k:02d}_{int(t // 60):02d}m{int(t % 60):02d}s.jpg")
        vf = roi_filter(roi) + f"scale='if(gt(iw,ih),{a.size},-2)':'if(gt(iw,ih),-2,{a.size})':flags=lanczos"
        subprocess.run([FFMPEG, "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", video, "-frames:v", "1", "-vf", vf, "-q:v", "2", p],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if os.path.exists(p):
            slides.append({"n": k, "t": round(t, 2), "cambio_pct": round(ch * 100, 1), "file": os.path.relpath(p, out), "nitidez": round(sharp(Image.open(p)), 1)})
    for k, s in enumerate(slides):
        s["t_hasta"] = round(slides[k + 1]["t"], 2) if k + 1 < len(slides) else round(a.t0 + span, 2)
    json.dump({"video": video, "roi": list(roi) if roi else None, "duracion": round(dur, 2), "umbral_bloques_pct": round(thr * 100, 2), "slides": slides}, open(os.path.join(out, "slides.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    # hojas 2x2 de vista general (cada celda ~780 px de ancho: se leen titulos y estructura, NO ecuaciones pequenas)
    per = 4
    for s0 in range(0, len(slides), per):
        chunk = slides[s0: s0 + per]
        ims = [Image.open(os.path.join(out, s["file"])).convert("RGB") for s in chunk]
        cw = 780
        ims = [im.resize((cw, int(cw * im.height / im.width)), Image.LANCZOS) for im in ims]
        ch_ = max(i.height for i in ims)
        sheet = Image.new("RGB", (cw * 2, (ch_ + 22) * math.ceil(len(ims) / 2)), BG)
        d = ImageDraw.Draw(sheet)
        for j, (im, s) in enumerate(zip(ims, chunk)):
            x, y = (j % 2) * cw, (j // 2) * (ch_ + 22)
            sheet.paste(im, (x, y))
            d.text((x + 4, y + ch_ + 3), f"#{s['n']:02d}  {tc(s['t'])} -> {tc(s['t_hasta'])}", fill=ACC, font=font(14))
        sheet.save(os.path.join(od, f"overview_{s0 // per + 1:02d}.png"), "PNG", optimize=True)

    print(f"{len(slides)} estados estables en {span:.0f} s (umbral {thr * 100:.1f} % de bloques, movimiento medio {moving:.1f}/255)")
    for s in slides[:12]:
        print(f"  #{s['n']:02d} {tc(s['t'])} -> {tc(s['t_hasta'])}  cambio {s['cambio_pct']} %  nitidez {s['nitidez']}")
    if len(slides) > 12:
        print(f"  ... (+{len(slides) - 12} mas; ver slides.json)")
    print("escrito:", out)


if __name__ == "__main__":
    main()
