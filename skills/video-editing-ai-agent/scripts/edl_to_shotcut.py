#!/usr/bin/env python
"""EDL (formato video-use / assets/edl-schema.json) -> proyecto editable de Shotcut, via shotcut-mcp.

EDL minimo:
{"version":1,"sources":{"A":"C:/ruta/a.mp4"},
 "ranges":[{"source":"A","start":2.42,"end":6.85,"beat":"HOOK","quote":"...","reason":"..."}],
 "grade":"subtle" | "auto" | "<cadena ffmpeg>",          (opcional)
 "overlays":[{"file":"x.mp4","start_in_output":0.0,"duration":5.0}],   (solo con cortes duros)
 "subtitles":"master.srt"}                                (opcional, solo con cortes duros)

Uso: python edl_to_shotcut.py edl.json --project D:/carpeta/Proyecto.mlt [--width 1080 --height 1920 --fps 30]
        [--pad-in 0.05 --pad-out 0.08] [--transition-frames 0] [--audio-fade-ms 30] [--denoise 0.9] [--overwrite]
Reglas aplicadas (video-use, MIT): tiempos en limites de palabra + padding 30-200 ms (regla 6/7), fundidos de audio de
~30 ms en cada corte duro (regla 3), marcadores por "beat", notas con quote/reason. Con transiciones el timeline se acorta
(los solapes consumen fotogramas): overlays y subtitulos por tiempo de salida solo se admiten con cortes duros.
No exporta: eso lo decide el usuario (start_render).
"""
import argparse, json, os, re, sys

sys.path.insert(0, os.path.dirname(__file__))
from shotcut_mcp_call import Shotcut
from _common import probe_duration
import grade as G


def parse_srt(path):
    items = []
    for blk in re.split(r"\n\s*\n", open(path, encoding="utf-8").read().strip()):
        ls = blk.strip().splitlines()
        m = re.search(r"(\d+):(\d+):(\d+)[,.](\d+)\s*-->\s*(\d+):(\d+):(\d+)[,.](\d+)", blk)
        if not m:
            continue
        g = [int(x) for x in m.groups()]
        s = ((g[0] * 60 + g[1]) * 60 + g[2]) * 1000 + g[3]
        e = ((g[4] * 60 + g[5]) * 60 + g[6]) * 1000 + g[7]
        txt = "\n".join(l for l in ls if "-->" not in l and not l.strip().isdigit())
        items.append({"start_ms": s, "end_ms": e, "text": txt})
    return items


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("edl"); ap.add_argument("--project", required=True)
    ap.add_argument("--width", type=int, default=1080); ap.add_argument("--height", type=int, default=1920); ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--pad-in", type=float, default=0.05); ap.add_argument("--pad-out", type=float, default=0.08)
    ap.add_argument("--transition-frames", type=int, default=0); ap.add_argument("--audio-fade-ms", type=int, default=30)
    ap.add_argument("--denoise", type=float, default=0.0); ap.add_argument("--overwrite", action="store_true")
    a = ap.parse_args()
    edl = json.load(open(a.edl, encoding="utf-8"))
    base = os.path.dirname(os.path.abspath(a.edl))
    src = {k: (v if os.path.isabs(v) else os.path.join(base, v)) for k, v in edl["sources"].items()}
    if os.path.exists(a.project):
        if not a.overwrite:
            sys.exit(f"ya existe {a.project} (usa --overwrite)")
        os.remove(a.project)
    clips, ranges = [], edl["ranges"]
    for i, r in enumerate(ranges):
        d = probe_duration(src[r["source"]])
        cin, cout = max(0.0, r["start"] - a.pad_in), min(d, r["end"] + a.pad_out)
        clips.append({"path": src[r["source"]], "track": "V1", "in_seconds": round(cin, 3), "out_seconds": round(cout, 3),
                      "caption": f"{r.get('beat', i + 1)} [{r['source']} {cin:.2f}-{cout:.2f}s]"})
    sc = Shotcut()
    try:
        sc.call("create_project", {"project_path": a.project, "width": a.width, "height": a.height, "fps_num": a.fps, "fps_den": 1,
                                   "tracks": [{"kind": "video", "name": "Overlays"}], "clips": clips})

        def v1():
            info = sc.call("inspect_project", {"path": a.project})
            return info, [t for t in info["tracks"] if t["name"] == "V1"][0]["items"]

        for k in range(len(ranges) - 1 if a.transition_frames > 0 else 0):
            info, items = v1()
            cl = [i for i in items if i.get("type") == "clip"]
            sc.call("edit_project", {"project_path": a.project, "expected_revision": info["revision"], "operations": [
                {"op": "add_transition", "item_ref": cl[k]["item_ref"], "duration_frames": a.transition_frames, "service": "luma", "audio_crossfade": True, "name": f"Transicion {k + 1}", "properties": {"softness": 0.35}}]})
        info, items = v1()
        cl = [i for i in items if i.get("type") == "clip"]
        ops, hard = [], a.transition_frames == 0
        fade = max(1, round(a.audio_fade_ms / 1000 * a.fps))
        grade = edl.get("grade")
        for i, (c, r) in enumerate(zip(cl, ranges)):
            n = c["duration_frames"]
            if hard and n > 4 * fade:  # fundidos de audio ~30 ms en cada borde
                ops.append({"op": "animate_clip", "item_ref": c["item_ref"], "interpolation": "linear", "keyframes": [
                    {"frame": 0, "volume_db": -40}, {"frame": fade, "volume_db": 0}, {"frame": n - 1 - fade, "volume_db": 0}, {"frame": n - 1, "volume_db": -40}]})
            if a.denoise > 0:
                ops.append({"op": "add_filter", "target": "clip", "item_ref": c["item_ref"], "service": "rnnoise", "properties": {"mix": str(a.denoise)}})
            if grade:
                if grade == "auto":
                    fs = G.auto_filter(G.stats(src[r["source"]], r["start"], max(0.5, r["end"] - r["start"])))
                else:
                    fs = G.PRESETS.get(grade, grade)
                for o in G.mlt_ops(fs):
                    ops.append({**o, "target": "clip", "item_ref": c["item_ref"]})
            ops.append({"op": "add_marker", "start_frame": c["start_frame"], "text": f"{r.get('beat', i + 1)}", "color": "#ffd700"})
        notes = "\n".join(f"{r.get('beat', i + 1)}: {r.get('quote', '')} | {r.get('reason', '')}" for i, r in enumerate(ranges))
        ops.append({"op": "set_notes", "notes": "EDL: " + os.path.basename(a.edl) + "\n" + notes})
        if hard:
            for j, o in enumerate(edl.get("overlays", [])):
                ops.append({"op": "add_clip", "track": "Overlays", "path": o["file"] if os.path.isabs(o["file"]) else os.path.join(base, o["file"]),
                            "position_frame": round(o["start_in_output"] * a.fps), "image_duration_seconds": o["duration"], "mode": "overwrite"})
            if edl.get("subtitles"):
                p = edl["subtitles"] if os.path.isabs(edl["subtitles"]) else os.path.join(base, edl["subtitles"])
                ops.append({"op": "set_subtitle_track", "name": "Subtitulos", "language": "eng", "burn_in": True, "items": parse_srt(p),
                            "style": {"family": "Arial", "size": 84, "weight": 900, "fgcolour": "#ffffff", "olcolour": "#000000", "outline": 8, "halign": "centre", "valign": "bottom", "geometry": "6%/56%:88%x14%:100"}})
        elif edl.get("overlays") or edl.get("subtitles"):
            print("AVISO: overlays/subtitulos por tiempo de salida omitidos porque hay transiciones (el timeline se acorta). Usa cortes duros o reubica a mano.")
        res = sc.call("edit_project", {"project_path": a.project, "expected_revision": info["revision"], "operations": ops})
        p = res["project"]
        print(f"proyecto listo: {a.project}\n  {len(ranges)} tramos, {p['duration_frames']} f = {p['duration_frames'] / a.fps:.2f} s, transiciones: {a.transition_frames or 'cortes duros'}")
    finally:
        sc.close()


if __name__ == "__main__":
    main()
