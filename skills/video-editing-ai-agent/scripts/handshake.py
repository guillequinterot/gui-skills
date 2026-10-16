#!/usr/bin/env python
"""Handshake de capacidades para Video-Editing-AI-Agent.

Uso: python handshake.py [--project CARPETA] [--json]
Escribe handshake.json en la carpeta del proyecto (si se indica) e imprime el resultado.
Solo lee: no instala ni modifica nada del sistema.
"""
import argparse, glob, json, os, shutil, subprocess, sys, datetime, importlib.util

SHOTCUT_DIR = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Programs", "Shotcut")
KEY_FILTERS = ["drawtext", "ass", "subtitles", "xfade", "zoompan", "loudnorm", "arnndn", "silencedetect", "freezedetect", "blackdetect", "signalstats", "zscale", "tonemap"]


def run(cmd, timeout=40):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except Exception as e:  # noqa
        return -1, str(e)


def find_bin(name):
    cand = os.path.join(SHOTCUT_DIR, name + ".exe")
    if os.path.exists(cand):
        return cand
    return shutil.which(name)


def ffmpeg_info(path):
    if not path:
        return {"found": False}
    _, ver = run([path, "-version"])
    _, filt = run([path, "-hide_banner", "-filters"])
    have = {f: (f" {f} " in filt) for f in KEY_FILTERS}
    return {"found": True, "path": path, "version": ver.splitlines()[0] if ver else "?", "filters": have}


def shotcut_mcp():
    info = {"registered": False, "melt": None, "shotcut": None, "note": ""}
    info["melt"] = find_bin("melt")
    info["shotcut"] = find_bin("shotcut")
    claude = shutil.which("claude") or shutil.which("claude.cmd")
    if claude:
        code, out = run([claude, "mcp", "list"], timeout=90)
        for line in out.splitlines():
            if line.strip().lower().startswith("shotcut"):
                info["registered"] = True
                info["status_line"] = line.strip()
    else:
        info["note"] = "CLI claude no encontrado en PATH; no se pudo listar MCP."
    info["note"] += " Las tools mcp__shotcut__* solo aparecen tras reiniciar la sesión si se registró después."
    return info


def has_module(name):
    return importlib.util.find_spec(name) is not None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    ff = ffmpeg_info(find_bin("ffmpeg"))
    sc = shotcut_mcp()
    tools = {m: has_module(m) for m in ["faster_whisper", "PIL", "numpy", "cv2"]}
    fonts_dir = r"C:\Windows\Fonts"
    fonts = {f: os.path.exists(os.path.join(fonts_dir, f)) for f in ["arial.ttf", "arialbd.ttf", "ariblk.ttf", "segoeui.ttf"]}
    warnings = []
    if ff.get("found"):
        if not ff["filters"].get("drawtext"):
            warnings.append("ffmpeg sin drawtext: texto por PNG (Pillow) + overlay o clips de texto de Shotcut.")
        if not (ff["filters"].get("ass") or ff["filters"].get("subtitles")):
            warnings.append("ffmpeg sin ass/subtitles: no quemar ASS/SRT con ffmpeg.")
    else:
        warnings.append("ffmpeg no encontrado.")
    if not tools["faster_whisper"]:
        warnings.append("faster-whisper ausente: sin transcripción local (pip install faster-whisper).")
    scripts_dir = os.path.dirname(os.path.abspath(__file__))
    understand = {
        "ready": bool(ff.get("found")) and tools["numpy"] and tools["PIL"],
        "transcription": tools["faster_whisper"],
        "scripts": {n: os.path.exists(os.path.join(scripts_dir, n)) for n in ("video_understand.py", "frame_probe.py")},
        "note": "Sin faster-whisper el mapa sale sin voz (usar --no-transcribe). Sin OCR: el texto en pantalla se lee con Read sobre los fotogramas.",
    }
    if not understand["ready"]:
        warnings.append("Comprension de video no disponible: falta ffmpeg, numpy o Pillow.")
    if not sc["registered"]:
        warnings.append("shotcut-mcp no aparece registrado: ver references/engine-shotcut.md (instalación).")

    node = shutil.which("node")
    node_ver = run([node, "--version"])[1].strip() if node else None
    chrome = next((c for c in (r"C:\Program Files\Google\Chrome\Application\chrome.exe", r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe") if os.path.exists(c)), None)
    try:
        node_ok = bool(node_ver) and int(node_ver.lstrip("v").split(".")[0]) >= 22
    except ValueError:
        node_ok = False
    ytdlp_ver = run([sys.executable, "-m", "yt_dlp", "--version"])[1].strip().splitlines()[-1:] or [""]
    hyperframes_ytdlp = {"installed": bool(ytdlp_ver[0]) and ytdlp_ver[0][0].isdigit(), "version": ytdlp_ver[0],
                         "js_runtime": "node" if node_ok else None,
                         "note": "references/fetch-reference.md; scripts/fetch_reference.py. Cookies: Firefox funciona; Chrome/Edge v127+ suelen fallar en Windows."}
    la = os.environ.get("LOCALAPPDATA", "")
    shells = sorted(glob.glob(os.path.join(la, "ms-playwright", "chromium_headless_shell-*", "chrome-headless-shell-win64", "chrome-headless-shell.exe")))
    sc_ffmpeg, sc_ffprobe = os.path.join(SHOTCUT_DIR, "ffmpeg.exe"), os.path.join(SHOTCUT_DIR, "ffprobe.exe")
    hf_ready = node_ok and bool(shells) and os.path.exists(sc_ffmpeg) and os.path.exists(sc_ffprobe)
    hyperframes = {
        "status": "tested" if hf_ready else "needs_setup",
        "version_pinned": "0.8.162",
        "node": node_ver, "node_ok": node_ok,
        "headless_shell": shells[-1] if shells else None,
        "ffmpeg_shotcut": os.path.exists(sc_ffmpeg), "ffprobe_shotcut": os.path.exists(sc_ffprobe),
        "env_block_git_bash": ([
            f'export HYPERFRAMES_BROWSER_PATH="{shells[-1]}"' if shells else "# falta chrome-headless-shell de Playwright",
            f'export HYPERFRAMES_FFMPEG_PATH="{sc_ffmpeg}"', f'export HYPERFRAMES_FFPROBE_PATH="{sc_ffprobe}"',
            "export HYPERFRAMES_NO_TELEMETRY=1 HYPERFRAMES_NO_UPDATE_CHECK=1 HYPERFRAMES_SKIP_SKILLS=1"]),
        "note": ("Probado con una pieza completa (Reel V001, 2026-10-16): init/check/snapshot/beats/render/--batch. NO usar el chrome.exe del sistema "
                 "(--version abre el navegador y la comprobacion se agota): usar el headless shell de Playwright. FFmpeg y FFprobe por variable de entorno, "
                 "no por PATH. 'beats' tambien necesita HYPERFRAMES_FFPROBE_PATH. Guardar versiones del HTML FUERA de la carpeta del proyecto. "
                 "Ver references/engine-hyperframes.md y references/errores-conocidos-y-aciertos.md."),
    }
    sys.path.insert(0, scripts_dir)
    from _common import memory_dir
    mem_dir = memory_dir()
    jl = os.path.join(mem_dir, "videos-aprobados.jsonl")
    rows = []
    if os.path.exists(jl):
        rows = [json.loads(l) for l in open(jl, encoding="utf-8") if l.strip()]
    approved = {"count": len(rows), "file": jl, "latest": [f"{r['id']} {r['nombre']} ({r['ruta']}, {r['formato']})" for r in rows[-3:]]}
    if not hf_ready:
        warnings.append("HyperFrames no esta listo: falta Node>=22, el headless shell de Playwright o el ffmpeg/ffprobe de Shotcut (ver engines.hyperframes).")
    engines = {
        "shotcut_mcp": {"status": "ready" if (sc["registered"] and sc["melt"]) else "unavailable", **sc},
        "ffmpeg": {"status": "ready" if ff.get("found") else "unavailable", **ff},
        "hyperframes": hyperframes,
        "yt_dlp": hyperframes_ytdlp,
    }
    rec = "shotcut" if engines["shotcut_mcp"]["status"] == "ready" else ("ffmpeg" if ff.get("found") else "none")
    result = {
        "skill_version": "1.4.0",
        "generated": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
        "os": sys.platform,
        "python": sys.version.split()[0],
        "engines": engines,
        "tools": tools,
        "video_understanding": understand,
        "video_aprender": {
            "scripts": {n: os.path.exists(os.path.join(scripts_dir, n)) for n in ("video_aprender.py", "aprender_lote.py", "slides_extract.py", "save_learning.py", "fetch_reference.py")},
            "glosarios": sorted(os.path.splitext(os.path.basename(g))[0] for g in glob.glob(os.path.join(os.path.dirname(scripts_dir), "assets", "glosarios", "*.json"))),
            "subskill_instalada": os.path.exists(os.path.join(os.path.expanduser("~"), ".claude", "skills", "video-aprender", "SKILL.md")),
            "pymupdf": has_module("fitz"),
            "nota": "Sub-skill video-aprender: aprender de un link/archivo (clase, reunion, referencia); varios links -> aprender_lote.py; --glosario <dominio> (hotwords + correcciones); muestreo de fotogramas automatico si la pantalla no tiene estados estables. Instagram publico sin cookies. Sin PyMuPDF no se pueden leer PDF de diapositivas (--slides)."},
        "production": {
            "scripts": {n: os.path.exists(os.path.join(scripts_dir, n)) for n in ("beat_grid.py", "motion_energy.py", "cut_dip.py", "self_eval.py", "carve_music.py", "hf_captions.py", "save_approved.py")},
            "preflight": os.path.exists(os.path.join(os.path.dirname(scripts_dir), "references", "errores-conocidos-y-aciertos.md")),
            "approved_videos": approved,
            "nota": "Antes de una pieza nueva: leer references/errores-conocidos-y-aciertos.md y correr `python scripts/save_approved.py suggest --route R --format F`. Al cerrar una pieza APROBADA: `save_approved.py add` con la cita del usuario."},
        "fonts": fonts,
        "future_engines": {k: "not_configured" for k in ["capcut", "canva", "premiere_pro", "after_effects"]},
        "recommended_engine": rec,
        "warnings": warnings,
    }
    text = json.dumps(result, indent=2, ensure_ascii=False)
    if a.project:
        os.makedirs(a.project, exist_ok=True)
        with open(os.path.join(a.project, "handshake.json"), "w", encoding="utf-8") as f:
            f.write(text)
    print(text)


if __name__ == "__main__":
    main()
