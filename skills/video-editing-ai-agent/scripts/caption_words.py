#!/usr/bin/env python
"""Subtítulos palabra por palabra como clips de texto de Shotcut (editables), vía shotcut-mcp.

Entrada: JSON con la secuencia de palabras en TIEMPO GLOBAL (segundos):
{
  "project": "C:/.../Reel.mlt",
  "track": "Subtitulos",
  "fps": 30,
  "key_words": ["communication", "preparation"],      # en acento
  "hook_words": ["TIRED", "OF", "RUSHED", "PAINT", "JOBS?"],  # opcional: todas en acento
  "style": {"family":"Arial","size":"112","weight":"900","accent":"#ffd700","base":"#ffffff","bg":"#a6000000","pad":"26","center_y":0.68},
  "phrases": [
     {"end": 2.85, "hook": true,  "words": [["TIRED",0.0],["OF",1.0],["RUSHED",1.35],["PAINT",2.05],["JOBS?",2.4]]},
     {"end": 4.85, "words": [["Good",2.733],["painting",3.153]]}
  ]
}
Cada palabra dura hasta la siguiente; la última de cada frase hasta `end` y hace fade-out.
Si la pista ya tiene clips de texto, se eliminan antes (reemplazo completo). Requiere shotcut-mcp.
Uso: python caption_words.py words_seq.json [--keep-old]
"""
import argparse, json, os, sys

sys.path.insert(0, os.path.dirname(__file__))
from shotcut_mcp_call import Shotcut  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("--keep-old", action="store_true")
    a = ap.parse_args()
    spec = json.load(open(a.spec, encoding="utf-8"))
    fps = spec.get("fps", 30)
    track = spec.get("track", "Subtitulos")
    st = {"family": "Arial", "size": "112", "weight": "900", "accent": "#ffd700", "base": "#ffffff", "bg": "#a6000000", "pad": "26", "center_y": 0.68}
    st.update(spec.get("style", {}))
    keys = {k.strip(".?,!") for k in spec.get("key_words", [])}

    sc = Shotcut()
    try:
        info = sc.call("inspect_project", {"path": spec["project"]})
        ops = []
        names = [t["name"] for t in info["tracks"]]
        if track not in names:
            ops.append({"op": "add_track", "kind": "video", "name": track})
        elif not a.keep_old:
            t = [t for t in info["tracks"] if t["name"] == track][0]
            ops += [{"op": "remove_item", "item_ref": it["item_ref"], "ripple": False} for it in t["items"] if it.get("type") == "clip" and it.get("item_ref")]
        kf = lambda f, sc_, op: {"frame": f, "center_x": 0.5, "center_y": st["center_y"], "scale": sc_, "rotation_degrees": 0, "opacity": op}
        n = 0
        for ph in spec["phrases"]:
            words = ph["words"]
            for i, (w, t0) in enumerate(words):
                t1 = words[i + 1][1] if i + 1 < len(words) else ph["end"]
                sf = round(t0 * fps)
                L = max(5, round(t1 * fps) - sf)
                accent = ph.get("hook") or w.strip(".?,!") in keys
                ops.append({"op": "add_generator", "track": track, "generator": "text", "duration_frames": L, "position_frame": sf, "mode": "overwrite",
                            "text": w, "properties": {"family": st["family"], "size": st["size"], "weight": st["weight"], "fgcolour": st["accent"] if accent else st["base"],
                                                       "olcolour": "#000000", "outline": "3", "bgcolour": st["bg"], "align": "center", "pad": st["pad"]}, "as": f"w{n}"})
                p1, p2, tail = min(3, L - 1), min(7, L - 1), L - 1
                frames = [kf(0, 0.78, 0), kf(p1, 1.12, 1)]
                if p2 > p1:
                    frames.append(kf(p2, 1.0, 1))
                if i + 1 == len(words):
                    if tail - 3 > frames[-1]["frame"]:
                        frames.append(kf(tail - 3, 1.0, 1))
                    frames.append(kf(tail, 1.0, 0))
                elif tail > frames[-1]["frame"]:
                    frames.append(kf(tail, 1.0, 1))
                ops.append({"op": "animate_clip", "item_ref": f"@w{n}", "interpolation": "smooth", "keyframes": frames})
                n += 1
        res = sc.call("edit_project", {"project_path": spec["project"], "expected_revision": info["revision"], "operations": ops})
        print("edited:", res.get("edited"), "revision:", res.get("revision"), "words:", n)
    finally:
        sc.close()


if __name__ == "__main__":
    main()
