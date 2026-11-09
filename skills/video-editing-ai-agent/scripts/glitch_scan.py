#!/usr/bin/env python
"""Busca en un MP4 renderizado los defectos que se ven poco y se notan mucho: flashes y «pops» de UN fotograma, fotograma 0 plano o
negro, tramos congelados y (con --loop) la costura de un bucle. Trabaja con fotogramas de 96x54 en gris: es barato (segundos).

Ideas de video-director, huashu-motion y take-one (MIT), reimplementadas aquí. Cubre el hueco anotado en references/visual-qa.md.
  flash/pop : un fotograma i difiere con fuerza de i-1 y de i+1, mientras i-1 e i+1 se parecen entre sí (el fotograma «salta y vuelve»).
              flash = salto >= 6 niveles de gris (se ve claro); pop = entre 2 y 6 (se nota al repasar). Un CORTE no cuenta: tras un corte
              i-1 e i+1 NO se parecen.
  fotograma 0 : medio < 12 o contraste (desviación) < 6 sobre 255 = plano o negro. Es el póster de la pieza: casi siempre un defecto.
  congelado : cambio medio < 0.25 durante >= 1.0 s. Cada tramo debe ser una pausa diseñada (un cierre con logo quieto es normal).
  bucle     : con --loop, diferencia del último contra el primer fotograma frente al paso mediano.
Los umbrales vienen de las fuentes y no están calibrados con nuestro material; el script mide, la decisión es de quien mira el fotograma
(usa `frame_probe.py --at T` para verlo). Código de salida 1 si hay flashes o el fotograma 0 es plano.

Uso: python glitch_scan.py pieza.mp4 [--freeze 1.0] [--loop] [--json salida.json]
"""
import argparse, json, os, subprocess, sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import FFMPEG, probe_stream  # noqa: E402

W, H = 96, 54


def load(path):
    st = probe_stream(path)
    a, _, b = (st.get("avg_frame_rate") or "30/1").partition("/")
    try:
        fps = float(a) / float(b or 1) or 30.0
    except ValueError:
        fps = 30.0
    raw = subprocess.run([FFMPEG, "-v", "error", "-i", path, "-vf", f"scale={W}:{H}:flags=area,format=gray", "-f", "rawvideo", "-"],
                         capture_output=True, timeout=900).stdout
    n = len(raw) // (W * H)
    return np.frombuffer(raw[:n * W * H], dtype=np.uint8).reshape(n, H * W).astype(np.float32), fps


def scan(path, freeze_s=1.0, loop=False):
    F, fps = load(path)
    n = len(F)
    rep = {"video": path, "fotogramas": int(n), "fps": round(fps, 3), "flashes": [], "pops": [], "congelados": [], "fotograma0": {}}
    if n < 4:
        rep["error"] = "menos de 4 fotogramas"
        return rep
    d = np.abs(F[1:] - F[:-1]).mean(axis=1)                 # d[i] = cambio entre fotograma i e i+1
    med = float(np.median(d))
    for i in range(1, n - 1):
        a, b = float(d[i - 1]), float(d[i])
        around = float(np.abs(F[i + 1] - F[i - 1]).mean())
        lo = min(a, b)
        if lo > max(2.0, 3 * med) and around < lo / 3:
            item = {"fotograma": i, "t": round(i / fps, 3), "salto": round(lo, 1)}
            (rep["flashes"] if lo >= 6 else rep["pops"]).append(item)
    f0 = F[0]
    rep["fotograma0"] = {"medio": round(float(f0.mean()), 1), "contraste": round(float(f0.std()), 1)}
    rep["fotograma0"]["plano_o_negro"] = bool(f0.mean() < 12 or f0.std() < 6)
    run = None
    for i, v in enumerate(d < 0.25):
        if v and run is None:
            run = i
        if (not v or i == len(d) - 1) and run is not None:
            end = i if not v else i + 1
            if (end - run) / fps >= freeze_s:
                rep["congelados"].append({"desde": round(run / fps, 2), "hasta": round(end / fps, 2)})
            run = None
    if loop:
        seam = float(np.abs(F[-1] - F[0]).mean())
        rep["bucle"] = {"costura": round(seam, 2), "paso_mediano": round(med, 2), "ok": bool(seam <= max(2 * med, 0.5))}
    return rep


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("--freeze", type=float, default=1.0)
    ap.add_argument("--loop", action="store_true")
    ap.add_argument("--json")
    a = ap.parse_args()
    r = scan(a.video, a.freeze, a.loop)
    if "error" in r:
        print("ERROR:", r["error"]); sys.exit(2)
    print(f"# glitch_scan - {os.path.basename(a.video)}: {r['fotogramas']} fotogramas a {r['fps']} fps")
    f0 = r["fotograma0"]
    print(f"fotograma 0: medio {f0['medio']}, contraste {f0['contraste']} -> {'PLANO O NEGRO (es el poster: revisalo)' if f0['plano_o_negro'] else 'ok'}")
    print(f"flashes de un fotograma: {len(r['flashes'])}" + "".join(f"\n  FLASH en {x['t']} s (fotograma {x['fotograma']}, salto {x['salto']})" for x in r["flashes"]))
    print(f"pops: {len(r['pops'])}" + "".join(f"\n  pop en {x['t']} s (fotograma {x['fotograma']}, salto {x['salto']})" for x in r["pops"]))
    print(f"tramos congelados >= {a.freeze} s: {len(r['congelados'])}" + "".join(f"\n  {x['desde']}-{x['hasta']} s (debe ser una pausa disenada)" for x in r["congelados"]))
    if "bucle" in r:
        b = r["bucle"]
        print(f"bucle: costura {b['costura']} vs paso mediano {b['paso_mediano']} -> {'ok' if b['ok'] else 'SE NOTA EL SALTO'}")
    print("Umbrales de las fuentes, sin calibrar con nuestro material. Mira el fotograma (frame_probe.py --at T) antes de dar un defecto por cierto.")
    if a.json:
        json.dump(r, open(a.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    sys.exit(1 if (r["flashes"] or f0["plano_o_negro"]) else 0)


if __name__ == "__main__":
    main()
