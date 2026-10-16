#!/usr/bin/env python
"""Correccion/gradacion de color: presets, auto-grade por analisis de fotogramas y traduccion a filtros de Shotcut.

Uso:
  python grade.py --list-presets
  python grade.py --print-preset warm_cinematic
  python grade.py --analyze clip.mp4 [--start 0 --duration 5]          # stats + filtro recomendado (auto)
  python grade.py clip.mp4 -o graded.mp4 [--preset NAME | --filter 'eq=...' | --auto]   # ffmpeg (audio copiado)
  python grade.py --mlt-ops warm_cinematic                              # ops add_filter para shotcut-mcp (avfilter.*)
Filosofia (video-use, MIT): razonar sobre la imagen, no aplicar un preset a ciegas; auto-grade limitado a +-8 %
y SIN cambios de color creativos. Modelo mental ASC CDL: out=(in*slope+offset)^power (slope=luces, offset=sombras,
power=medios). Probar tonos de piel antes de ser agresivo. Aplicar POR CLIP (no tras concatenar) si se usa ffmpeg.
Presets y reglas adaptados de browser-use/video-use helpers/grade.py (MIT).
"""
import argparse, os, re, subprocess, sys, tempfile

sys.path.insert(0, os.path.dirname(__file__))
from _common import FFMPEG, probe_duration

PRESETS = {
    "subtle": "eq=contrast=1.03:saturation=0.98",
    "neutral_punch": "eq=contrast=1.06:brightness=0.0:saturation=1.0,curves=master='0/0 0.25/0.23 0.75/0.77 1/1'",
    "warm_cinematic": ("eq=contrast=1.12:brightness=-0.02:saturation=0.88,"
                       "colorbalance=rs=0.02:gs=0.0:bs=-0.03:rm=0.04:gm=0.01:bm=-0.02:rh=0.08:gh=0.02:bh=-0.05,"
                       "curves=master='0/0 0.25/0.22 0.75/0.78 1/1'"),
    "none": "",
}


def stats(video, start=0.0, duration=None, n=10):
    duration = duration or min(probe_duration(video), 10.0)
    fps = max(0.5, min(n / max(duration, 0.1), 10.0))
    # ruta RELATIVA (cwd = temp): "C:\..." rompe el argumento del filtro en Windows
    tmpdir = tempfile.gettempdir()
    meta = os.path.join(tmpdir, "vea_sig.txt")
    if os.path.exists(meta):
        os.remove(meta)
    subprocess.run([FFMPEG, "-y", "-hide_banner", "-nostats", "-ss", f"{start:.3f}", "-i", os.path.abspath(video), "-t", f"{duration:.3f}", "-vf", f"fps={fps:.2f},signalstats,metadata=print:file=vea_sig.txt", "-f", "null", "-"],
                   capture_output=True, cwd=tmpdir)
    ya, yn, yx, sa, bd = [], [], [], [], 8
    try:
        for line in open(meta):
            v = line.strip().rsplit("=", 1)[-1]
            if "YBITDEPTH" in line: bd = int(float(v))
            elif "YAVG" in line: ya.append(float(v))
            elif "YMIN" in line: yn.append(float(v))
            elif "YMAX" in line: yx.append(float(v))
            elif "SATAVG" in line: sa.append(float(v))
    except FileNotFoundError:
        pass
    if not ya:
        return {"y_mean": 0.5, "y_range": 0.7, "sat_mean": 0.25}
    mx = 2 ** bd - 1
    avg = lambda l: sum(l) / len(l)
    return {"y_mean": avg(ya) / mx, "y_range": (avg(yx) - avg(yn)) / mx if yx and yn else 0.7, "sat_mean": avg(sa) / mx if sa else 0.25}


def auto_filter(s):
    """Correccion sutil acotada (+-8 %): sube gamma si oscuro, contraste si plano, satura si muy apagado."""
    yr, ym, sm = s["y_range"], s["y_mean"], s["sat_mean"]
    con = 1.08 - 0.05 * max(0, min(1, (yr - 0.50) / 0.15)) if yr < 0.65 else 1.03
    gam = 1.10 - 0.08 * max(0, min(1, (ym - 0.30) / 0.12)) if ym < 0.42 else (0.97 if ym > 0.60 else 1.0)
    sat = 1.04 if sm < 0.18 else (0.96 if sm > 0.38 else 0.98)
    con, gam, sat = max(0.94, min(1.08, con)), max(0.94, min(1.10, gam)), max(0.94, min(1.06, sat))
    parts = [f"{k}={v:.3f}" for k, v in (("contrast", con), ("gamma", gam), ("saturation", sat)) if abs(v - 1) > 0.005]
    return ("eq=" + ":".join(parts)) if parts else ""


def mlt_ops(filter_string):
    """Traduce una cadena ffmpeg (eq/colorbalance/curves) a ops add_filter de shotcut-mcp (servicios avfilter.*).
    Devuelve ops SIN target/item_ref: el llamador debe anadirlos (target:'clip', item_ref:...)."""
    def split_top(s, sep):
        out, cur, q = [], "", False
        for ch in s:
            if ch == "'":
                q = not q
            if ch == sep and not q:
                out.append(cur); cur = ""
            else:
                cur += ch
        out.append(cur)
        return out

    ops = []
    for part in split_top(filter_string, ","):
        part = part.strip()
        if not part:
            continue
        name, _, args = part.partition("=")
        props = {}
        for kv in split_top(args, ":"):
            if "=" in kv:
                k, v = kv.split("=", 1)
                props["av." + k.strip()] = v.strip().strip("'")
        if name in ("eq", "colorbalance", "curves"):
            ops.append({"op": "add_filter", "service": "avfilter." + name, "properties": props})
    return ops


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input", nargs="?"); ap.add_argument("-o", "--output")
    ap.add_argument("--preset", choices=list(PRESETS)); ap.add_argument("--filter"); ap.add_argument("--auto", action="store_true")
    ap.add_argument("--list-presets", action="store_true"); ap.add_argument("--print-preset"); ap.add_argument("--analyze")
    ap.add_argument("--mlt-ops", help="nombre de preset o cadena ffmpeg"); ap.add_argument("--start", type=float, default=0.0); ap.add_argument("--duration", type=float)
    a = ap.parse_args()
    if a.list_presets:
        for k, v in PRESETS.items():
            print(f"{k}: {v or '(sin filtro)'}")
        return
    if a.print_preset:
        print(PRESETS[a.print_preset]); return
    if a.analyze:
        s = stats(a.analyze, a.start, a.duration)
        print(f"y_mean={s['y_mean']:.3f} y_range={s['y_range']:.3f} sat_mean={s['sat_mean']:.3f}\nfiltro auto: {auto_filter(s) or '(ninguno)'}"); return
    if a.mlt_ops:
        import json
        print(json.dumps(mlt_ops(PRESETS.get(a.mlt_ops, a.mlt_ops)), indent=1)); return
    if not a.input or not a.output:
        ap.error("input y -o son obligatorios")
    if os.path.exists(a.output):
        sys.exit(f"ya existe {a.output}")
    f = a.filter or (PRESETS[a.preset] if a.preset else auto_filter(stats(a.input, a.start, a.duration)))
    cmd = [FFMPEG, "-y", "-hide_banner", "-i", a.input] + (["-vf", f] if f else []) + ["-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "copy", a.output]
    r = subprocess.run(cmd, capture_output=True, text=True)
    print("ok ->" if r.returncode == 0 else r.stderr[-600:], a.output, "| filtro:", f or "(ninguno)")


if __name__ == "__main__":
    main()
