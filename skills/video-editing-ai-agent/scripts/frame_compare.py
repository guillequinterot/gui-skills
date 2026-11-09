#!/usr/bin/env python
"""Compara dos clips cuadro a cuadro (referencia vs recreación) y mide bucles de GIF/loop.

Para qué: cuando se recrea una animación de referencia (una web, un motion graphic, un reel) no basta con «se ve parecido»:
se mide si el MOVIMIENTO ocurre en el mismo momento y con la misma curva, y si la imagen coincide. Método tomado de la idea de
«grabar -> especificar -> construir -> volver a grabar igual -> comparar» (reanimate, MIT), reimplementado aquí sin copiar su código
y sin pixelmatch: solo ffmpeg + numpy.

Subcomandos
  compare REF CLON   curva de actividad (cambio entre fotogramas consecutivos) de cada clip, ventana de movimiento (primer/último
                     fotograma activo y pico), error de tiempo (clon - referencia), desfase óptimo y desajuste de imagen por fotograma.
  loop CLIP          costura (último vs primer fotograma) y excursión (máxima diferencia contra el fotograma 0) de un bucle.

Uso:
  python frame_compare.py compare ref.mp4 clon.mp4 [--fps 25] [--width 320] [--region x,y,w,h] [--max-shift 15]
                          [--fidelity movimiento|pixel] [--sheet hoja.png --every 5] [--json salida.json]
  python frame_compare.py loop bucle.gif [--fps 20] [--json salida.json]

Reglas de lectura (leer antes de confiar en un número):
  * Misma resolución, fps, recorte, disparador y duración en ambos lados. Si difieren, el script lo AVISA («estás midiendo tu
    configuración, no tu trabajo»). Con otro tamaño reescala el clon al de la referencia (con pérdida).
  * Con video natural (cámara, compresión) el desajuste de imagen tiene ruido: no perseguirlo; la curva de actividad y la ventana de
    movimiento son más fiables que el desajuste por fotograma.
  * Umbrales (tiempo ±0.08 s; imagen: media <= 2 %, ningún fotograma > 5 %) vienen de una fuente externa y NO están calibrados aquí
    con nuestro material: tómalos como punto de partida y di cuáles usaste. No bajes umbrales en silencio para «pasar».
  * Mide el suelo de ruido: compara la referencia contra una segunda captura de sí misma antes de juzgar el clon.
Mide, no juzga: que dos clips coincidan en números no demuestra que el resultado sea bueno.
"""
import argparse, json, os, subprocess, sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import FFMPEG, probe_stream  # noqa: E402

ACTIVE = 0.2          # % de cambio medio entre fotogramas consecutivos a partir del cual hay «movimiento»
PIX_THR = 26          # niveles de gris (de 255, ~ 0.1) a partir de los cuales un píxel cuenta como distinto
TOL_S = 0.08          # tolerancia de tiempo del nivel «movimiento»
PIXEL_MEAN, PIXEL_MAX = 0.02, 0.05


def parse_region(s):
    if not s:
        return None
    x, y, w, h = [int(v) for v in s.split(",")]
    return x, y, w, h


def load(path, fps, width, region=None, size=None, max_seconds=30):
    """Fotogramas en gris (n, H, W) float32 a `fps` fijos. `size` fuerza (W, H); si no, se calcula con el ancho dado."""
    vf = []
    if region:
        x, y, w, h = region
        vf.append(f"crop={w}:{h}:{x}:{y}")
    vf.append(f"fps={fps}")
    if size:
        vf.append(f"scale={size[0]}:{size[1]}")
    else:
        vf.append(f"scale={width}:-2")
    vf.append("format=gray")
    cmd = [FFMPEG, "-v", "error", "-t", str(max_seconds), "-i", str(path), "-vf", ",".join(vf), "-f", "rawvideo", "-"]
    if size is None:
        # primero averigua el tamaño real de salida con una pasada corta (1 fotograma)
        probe = subprocess.run([FFMPEG, "-v", "error", "-i", str(path), "-vf", ",".join(vf), "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"],
                               capture_output=True)
        from PIL import Image
        import io
        im = Image.open(io.BytesIO(probe.stdout))
        size = im.size
    raw = subprocess.run(cmd, capture_output=True, timeout=900).stdout
    n = len(raw) // (size[0] * size[1])
    arr = np.frombuffer(raw[: n * size[0] * size[1]], dtype=np.uint8).reshape(n, size[1], size[0]).astype(np.float32)
    return arr, size


def activity(F):
    """% de cambio medio (0-100) entre cada fotograma y el anterior; el índice 0 es el paso 0->1."""
    return np.abs(F[1:] - F[:-1]).mean(axis=(1, 2)) / 255.0 * 100.0


def motion_window(a, fps):
    idx = np.where(a > ACTIVE)[0]
    if len(idx) == 0:
        return None
    return {"start_s": round(float(idx[0] / fps), 3), "end_s": round(float((idx[-1] + 1) / fps), 3),
            "peak_s": round(float((int(np.argmax(a)) + 1) / fps), 3), "peak_pct": round(float(a.max()), 2)}


def mismatch(A, B):
    """Fracción de píxeles distintos (> PIX_THR) por fotograma y cambio medio absoluto (%)."""
    n = min(len(A), len(B))
    d = np.abs(A[:n] - B[:n])
    return (d > PIX_THR).mean(axis=(1, 2)), d.mean(axis=(1, 2)) / 255.0 * 100.0


def best_shift(A, B, a_ref, fps, max_shift):
    """Desfase k (en fotogramas, + = el clon va TARDE) que minimiza el desajuste medio alrededor de la ventana de movimiento de la
    referencia. Un desfase grande se arregla en el disparador del clon; no se esconde con la alineación."""
    idx = np.where(a_ref > ACTIVE)[0]
    lo, hi = (max(0, int(idx[0]) - 5), min(len(A), int(idx[-1]) + 7)) if len(idx) else (0, min(len(A), 10))
    best = (None, 1e9)
    for k in range(-max_shift, max_shift + 1):
        # el fotograma i de la referencia se compara con el i+k del clon
        i0, i1 = max(lo, -k), min(hi, len(B) - k)
        if i1 - i0 < 5:
            continue
        m = np.abs(A[i0:i1] - B[i0 + k:i1 + k]).mean() / 255.0 * 100.0
        if m < best[1] - 1e-9:
            best = (k, m)
    return best


def bars(a, width=40, scale=None):
    m = scale or (float(a.max()) or 1.0)
    return ["#" * int(round(v / m * width)) for v in a]


def sheet(A, B, path, every, fps):
    from PIL import Image, ImageDraw
    n = min(len(A), len(B))
    rows = list(range(0, n, every))[:12]
    h, w = A.shape[1], A.shape[2]
    out = Image.new("L", (w * 3, (h + 12) * len(rows)), 255)
    dr = ImageDraw.Draw(out)
    for r, i in enumerate(rows):
        y = r * (h + 12)
        dr.text((2, y), f"#{i} t={i / fps:.2f}s   referencia | clon | diferencia", fill=0)
        for c, img in enumerate((A[i], B[i], np.clip(np.abs(A[i] - B[i]) * 3, 0, 255))):
            out.paste(Image.fromarray(img.astype(np.uint8)), (c * w, y + 12))
    out.save(path)
    return path


def cmd_compare(a):
    region = parse_region(a.region)
    warns = []
    sr, sc = probe_stream(a.ref), probe_stream(a.clon)
    if (sr.get("width"), sr.get("height")) != (sc.get("width"), sc.get("height")) and not region:
        warns.append(f"tamaños distintos (ref {sr.get('width')}x{sr.get('height')} vs clon {sc.get('width')}x{sc.get('height')}): "
                     "el clon se reescala al de la referencia (con pérdida); mide con el mismo viewport")
    A, size = load(a.ref, a.fps, a.width, region, max_seconds=a.max_seconds)
    B, _ = load(a.clon, a.fps, a.width, region, size=size, max_seconds=a.max_seconds)
    aa, ab = activity(A), activity(B)
    wa, wb = motion_window(aa, a.fps), motion_window(ab, a.fps)
    pix, mean = mismatch(A, B)
    k, m_k = best_shift(A, B, aa, a.fps, a.max_shift)
    rep = {"ref": a.ref, "clon": a.clon, "fps": a.fps, "frames": [int(len(A)), int(len(B))], "avisos": warns,
           "ventana_ref": wa, "ventana_clon": wb,
           "desajuste_pixeles_medio_pct": round(float(pix.mean()) * 100, 2), "desajuste_pixeles_max_pct": round(float(pix.max()) * 100, 2),
           "cambio_medio_abs_pct": round(float(mean.mean()), 2),
           "desfase_optimo_fotogramas": k, "desfase_optimo_s": None if k is None else round(k / a.fps, 3),
           "desajuste_medio_con_desfase_pct": None if k is None else round(float(m_k), 2)}
    timing_ok = None
    if wa and wb:
        err = {"inicio": round(wb["start_s"] - wa["start_s"], 3), "fin": round(wb["end_s"] - wa["end_s"], 3),
               "duracion": round((wb["end_s"] - wb["start_s"]) - (wa["end_s"] - wa["start_s"]), 3), "pico": round(wb["peak_s"] - wa["peak_s"], 3)}
        rep["error_tiempo_s"] = err
        timing_ok = all(abs(v) <= TOL_S for v in (err["inicio"], err["fin"], err["pico"]))
    elif wa and not wb:
        rep["error_tiempo_s"] = "el clon no tiene movimiento donde la referencia sí"
        timing_ok = False
    rep["tiempo_ok"] = timing_ok
    pixel_ok = bool(pix.mean() <= PIXEL_MEAN and pix.max() <= PIXEL_MAX)
    rep["imagen_ok"] = pixel_ok
    rep["veredicto"] = ("COINCIDE" if (timing_ok and (pixel_ok or a.fidelity == "movimiento")) else "NO COINCIDE")
    rep["nivel"] = a.fidelity
    if a.sheet:
        rep["hoja"] = sheet(A, B, a.sheet, a.every, a.fps)

    print(f"# comparación cuadro a cuadro ({a.fidelity}) — {a.fps} fps, {len(A)} vs {len(B)} fotogramas")
    for w in warns:
        print("AVISO:", w)
    print("curva de actividad (% de cambio entre fotogramas; ref | clon):")
    n = max(len(aa), len(ab))
    scale = max(float(aa.max()) if len(aa) else 1, float(ab.max()) if len(ab) else 1, 1e-6)
    ba, bb = bars(aa, 24, scale), bars(ab, 24, scale)
    step = max(1, n // 40)
    for i in range(0, n, step):
        ra = f"{aa[i]:5.2f} {ba[i]:<24}" if i < len(aa) else " " * 30
        rb = f"{ab[i]:5.2f} {bb[i]:<24}" if i < len(ab) else ""
        print(f"  {i / a.fps:5.2f}s {ra} | {rb}")
    print("ventana de movimiento  ref:", wa or "sin movimiento", " clon:", wb or "sin movimiento")
    if "error_tiempo_s" in rep:
        print("error de tiempo (clon - ref, s):", rep["error_tiempo_s"], f"(tolerancia ±{TOL_S} s) ->", "OK" if timing_ok else "FUERA")
    print(f"desajuste de imagen: media {rep['desajuste_pixeles_medio_pct']} % de píxeles, máximo {rep['desajuste_pixeles_max_pct']} %; "
          f"cambio medio {rep['cambio_medio_abs_pct']} %")
    if k is not None:
        lado = "TARDE" if k > 0 else ("TEMPRANO" if k < 0 else "en sitio")
        print(f"desfase óptimo: {k:+d} fotogramas ({rep['desfase_optimo_s']:+.3f} s, el clon va {lado}); desajuste con ese desfase {rep['desajuste_medio_con_desfase_pct']} %")
        if abs(k) > 2:
            print("  -> arregla el DISPARADOR/retardo del clon; no escondas el desfase alineando")
    print("VEREDICTO:", rep["veredicto"], "| lectura: mide coincidencia, no calidad; revisa la hoja de contacto con el visor de imágenes")
    if a.json:
        json.dump(rep, open(a.json, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    return 0 if rep["veredicto"] == "COINCIDE" else 1


def cmd_loop(a):
    F, _ = load(a.clip, a.fps, 216, max_seconds=a.max_seconds)
    if len(F) < 3:
        print("ERROR: el clip tiene menos de 3 fotogramas")
        return 2
    seam = float(np.abs(F[-1] - F[0]).mean())
    exc = float(max(np.abs(f - F[0]).mean() for f in F))
    mid = float(np.abs(F[len(F) // 2] - F[0]).mean())
    rep = {"clip": a.clip, "fotogramas": int(len(F)), "costura": round(seam, 2), "excursion": round(exc, 2), "diferencia_a_mitad": round(mid, 2)}
    notas = []
    if seam > 0.3:
        notas.append("costura > 0.3: se notará el salto al repetir (último fotograma != primero)")
    if exc < 0.7:
        notas.append("excursión < 0.7: casi nada se mueve")
    if exc > 0:
        notas.append("no midas el movimiento solo en el fotograma de la mitad: una oscilación vuelve a 0 ahí" if mid < 0.3 * exc else "")
    rep["notas"] = [n for n in notas if n]
    print(f"# bucle — {rep['fotogramas']} fotogramas a {a.fps} fps")
    print(f"costura (último vs primero, gris 0-255): {rep['costura']}   excursión (máx. vs fotograma 0): {rep['excursion']}")
    for n in rep["notas"]:
        print("  -", n)
    print("referencia externa de portadas reales (sin calibrar aquí): costura 0.0–0.3, excursión ~ 0.7–2.8")
    if a.json:
        json.dump(rep, open(a.json, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    return 0 if seam <= 0.3 else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("compare")
    c.add_argument("ref"); c.add_argument("clon")
    c.add_argument("--fps", type=float, default=25)
    c.add_argument("--width", type=int, default=320)
    c.add_argument("--region")
    c.add_argument("--max-shift", type=int, default=15)
    c.add_argument("--max-seconds", type=float, default=30)
    c.add_argument("--fidelity", choices=["movimiento", "pixel"], default="movimiento")
    c.add_argument("--sheet"); c.add_argument("--every", type=int, default=5)
    c.add_argument("--json")
    l = sub.add_parser("loop")
    l.add_argument("clip")
    l.add_argument("--fps", type=float, default=20)
    l.add_argument("--max-seconds", type=float, default=60)
    l.add_argument("--json")
    a = ap.parse_args()
    sys.exit(cmd_compare(a) if a.cmd == "compare" else cmd_loop(a))


if __name__ == "__main__":
    main()
