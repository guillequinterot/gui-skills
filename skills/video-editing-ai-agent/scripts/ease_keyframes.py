#!/usr/bin/env python
"""Genera keyframes de zoom con easing para animate_clip (Shotcut) o parámetros para ffmpeg.

Uso:
  python ease_keyframes.py --frames 92 --from 1.0 --to 1.12 [--anchor 0.22] [--curve smoothstep|cubic_in_out|cubic_out|spring] [--points 5]
Imprime JSON de keyframes {frame, center_x, center_y, scale, rotation_degrees}.
Fórmula de anclaje superior: center_y = a + s*(0.5 - a)  (a=0.22 mantiene la cabeza en el tercio superior).
"""
import argparse, json, math


def smoothstep(t):
    return t * t * (3 - 2 * t)


def cubic_in_out(t):
    return 4 * t ** 3 if t < 0.5 else 1 - (-2 * t + 2) ** 3 / 2


def cubic_out(t):
    return 1 - (1 - t) ** 3


def spring(t, damping=11.0, freq=3.0):
    # respuesta subamortiguada normalizada (llega a 1 con leve rebote)
    return 1 - math.exp(-damping * t / 3) * math.cos(2 * math.pi * freq * t * 0.5)


CURVES = {"smoothstep": smoothstep, "cubic_in_out": cubic_in_out, "cubic_out": cubic_out, "spring": spring}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--frames", type=int, required=True)
    ap.add_argument("--from", dest="a", type=float, required=True)
    ap.add_argument("--to", dest="b", type=float, required=True)
    ap.add_argument("--anchor", type=float, default=0.22)
    ap.add_argument("--curve", default="smoothstep", choices=CURVES)
    ap.add_argument("--points", type=int, default=5)
    a = ap.parse_args()
    f = CURVES[a.curve]
    last = a.frames - 1
    out = []
    for i in range(a.points):
        p = i / (a.points - 1)
        fr = round(p * last)
        s = a.a + (a.b - a.a) * f(p)
        out.append({"frame": fr, "center_x": 0.5, "center_y": round(a.anchor + s * (0.5 - a.anchor), 4), "scale": round(s, 4), "rotation_degrees": 0})
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
