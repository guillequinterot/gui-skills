#!/usr/bin/env python
"""Obtener material de referencia (YouTube, TikTok, Instagram...) con yt-dlp, con protecciones incorporadas.

Uso:
  python fetch_reference.py info  URL                         # solo metadatos (titulo, canal, licencia, duracion, formatos)
  python fetch_reference.py subs  URL [--langs es,en]         # subtitulos/auto-subtitulos -> .vtt + transcripcion .txt limpia
  python fetch_reference.py audio URL [--section 0-30]        # solo audio (wav 16 kHz mono, listo para transcribir)
  python fetch_reference.py video URL [--max-height 720] [--section 10-40]
Opciones comunes:
  -o CARPETA                  salida (por defecto ./referencias, que es la carpeta del PROYECTO; nunca la de la skill)
  --cookies-from-browser B    firefox | edge | chrome | brave ... SOLO se usa si el intento sin cookies falla por login/edad/limite
  --cookies-always            usa las cookies desde el primer intento (no recomendado)

Protecciones (en el codigo):
  - un solo video por llamada (--no-playlist, --max-downloads 1); sin descargas masivas ni "scrapers";
  - pausas entre peticiones (--sleep-requests, --sleep-interval) para no provocar bloqueos;
  - sin cookies por defecto; con --cookies-from-browser se intenta PRIMERO sin ellas; las cookies nunca se
    guardan en disco ni se imprimen; el log solo anota "cookies usadas: si/no" y el navegador;
  - se niega a escribir dentro de la carpeta de la skill;
  - cada obtencion queda registrada en <salida>/fetch-log.jsonl (URL, titulo, canal, licencia, que se bajo, tamano);
  - no evade DRM, pagos ni cuentas privadas: si el sitio exige algo mas que cookies propias, falla y lo dice.
Uso previsto: analisis y referencia de material propio o con derecho de uso. No republicar lo descargado.
Notas Windows: Chrome/Edge (v127+) cifran las cookies y yt-dlp suele NO poder leerlas sin permisos de administrador;
Firefox funciona. Para YouTube se usa Node como motor de JavaScript (--js-runtimes node).
"""
import argparse, datetime, json, os, re, shutil, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import FFMPEG  # noqa: E402

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# nunca escribir en ninguna copia de la skill (la que corre, su ruta real si se ejecuta por un enlace/junction y la instalada en ~/.claude/skills)
PROTECTED = [SKILL_DIR, os.path.realpath(SKILL_DIR), os.path.expanduser(os.path.join("~", ".claude", "skills", "video-editing-ai-agent"))]


def inside(path, parent):
    try:
        return os.path.commonpath([os.path.normcase(os.path.abspath(path)), os.path.normcase(os.path.abspath(parent))]) == os.path.normcase(os.path.abspath(parent))
    except ValueError:  # discos distintos
        return False
LOGIN_HINTS = re.compile(r"sign in|log ?in|login|cookies|age[- ]restricted|confirm your age|private video|rate.?limit|too many requests|"
                         r"429|403|members.only|not a bot|requiring login|authentication", re.I)


def base_cmd(a, cookies=None, limit=True):
    """limit=True agrega --max-downloads 1 (solo para descargas reales: en la consulta de metadatos aborta antes de imprimir)."""
    cmd = [sys.executable, "-m", "yt_dlp", "--no-playlist"] + (["--max-downloads", "1"] if limit else []) + ["--windows-filenames",
           "--sleep-requests", "1", "--sleep-interval", "2", "--max-sleep-interval", "5", "--retries", "3", "--no-warnings"]
    if shutil.which("node"):
        cmd += ["--js-runtimes", "node"]
    ffdir = os.path.dirname(FFMPEG)
    if os.path.isdir(ffdir):
        cmd += ["--ffmpeg-location", ffdir]
    if cookies:
        cmd += ["--cookies-from-browser", cookies]
    return cmd


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.returncode, (r.stdout or ""), (r.stderr or "")


def attempt(a, build):
    """Intenta sin cookies; si falla por login/edad/limite y hay --cookies-from-browser, reintenta con ellas."""
    first_cookies = a.cookies_from_browser if a.cookies_always else None
    code, out, err = run(build(first_cookies))
    code = 0 if code == 101 else code   # 101 = --max-downloads alcanzado: es el exito esperado
    used = first_cookies
    if code != 0 and a.cookies_from_browser and not a.cookies_always and LOGIN_HINTS.search(out + err):
        print(f"  El sitio pide sesion/edad/limite: reintentando con cookies de {a.cookies_from_browser} (no se guardan ni se imprimen)...")
        code, out, err = run(build(a.cookies_from_browser))
        code = 0 if code == 101 else code
        used = a.cookies_from_browser
        if code != 0 and re.search(r"decrypt|DPAPI|could not (find|copy)|database is locked", out + err, re.I):
            print("  AVISO: no se pudieron leer las cookies (Chrome/Edge v127+ las cifran; cierra el navegador o usa Firefox).")
    return code, out, err, used


def log(outdir, rec):
    rec["ts"] = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
    with open(os.path.join(outdir, "fetch-log.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def vtt_to_text(path):
    """VTT (con repeticiones de auto-subtitulos) -> lineas '[mm:ss] texto' sin duplicados consecutivos."""
    out, last = [], ""
    t = ""
    for line in open(path, encoding="utf-8", errors="replace"):
        line = line.rstrip("\n")
        m = re.match(r"(\d+):(\d\d):(\d\d)\.\d+ --> ", line) or re.match(r"(\d\d):(\d\d)\.\d+ --> ", line)
        if m:
            g = m.groups()
            t = f"{int(g[-2]):02d}:{int(g[-1]):02d}" if len(g) == 2 else f"{int(g[0]) * 60 + int(g[1]):02d}:{int(g[2]):02d}"
            continue
        if not line.strip() or line.startswith(("WEBVTT", "Kind:", "Language:", "NOTE")) or "-->" in line:
            continue
        txt = re.sub(r"<[^>]+>", "", line).strip()
        if txt and txt != last:
            out.append(f"[{t}] {txt}")
            last = txt
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("mode", choices=["info", "subs", "audio", "video"])
    ap.add_argument("url")
    ap.add_argument("-o", "--out", default="referencias")
    ap.add_argument("--langs", default="es,en")
    ap.add_argument("--section", help="tramo en segundos, p. ej. 10-40")
    ap.add_argument("--max-height", type=int, default=720)
    ap.add_argument("--cookies-from-browser", dest="cookies_from_browser")
    ap.add_argument("--cookies-always", action="store_true")
    a = ap.parse_args()

    outdir = os.path.abspath(a.out)
    if any(inside(outdir, p) for p in PROTECTED):
        sys.exit("ERROR: no se escribe dentro de la carpeta de la skill (la salida por defecto es la carpeta ACTUAL: si ejecutas desde la skill, cae aqui). "
                 "Pasa -o <carpeta del proyecto>/referencias (o ejecuta desde la carpeta del proyecto).")
    if not re.match(r"^https?://", a.url):
        sys.exit("ERROR: la URL debe empezar por http(s)://")
    os.makedirs(outdir, exist_ok=True)

    # metadatos siempre primero (tambien sirven para el registro)
    code, out, err, used = attempt(a, lambda c: base_cmd(a, c, limit=False) + ["--skip-download", "--dump-single-json", a.url])
    if code != 0:
        sys.exit("ERROR al leer metadatos:\n" + (err or out)[-600:])
    meta = json.loads(out)
    rec = {"url": a.url, "mode": a.mode, "title": meta.get("title"), "uploader": meta.get("uploader"), "license": meta.get("license"),
           "duration": meta.get("duration"), "cookies_used": bool(used), "cookies_browser": used}
    print(f"{meta.get('title')}  |  {meta.get('uploader')}  |  {meta.get('duration')} s  |  licencia: {meta.get('license') or 'no declarada'}")
    if a.mode == "info":
        subs = sorted((meta.get("subtitles") or {}).keys())
        auto = sorted((meta.get("automatic_captions") or {}).keys())
        print(f"  subtitulos manuales: {', '.join(subs[:12]) or 'ninguno'}  |  automaticos: {len(auto)} idiomas")
        print(f"  mejor resolucion: {meta.get('width')}x{meta.get('height')}  fps {meta.get('fps')}")
        log(outdir, rec)
        return

    tpl = os.path.join(outdir, "%(title).70s [%(id)s].%(ext)s")
    before = set(os.listdir(outdir))
    sect = ["--download-sections", f"*{a.section}", "--force-keyframes-at-cuts"] if a.section else []
    if a.mode == "subs":
        build = lambda c: base_cmd(a, c) + ["--skip-download", "--write-subs", "--write-auto-subs", "--sub-langs", a.langs,
                                            "--sub-format", "vtt", "--sleep-subtitles", "4", "--ignore-errors", "-o", tpl, a.url]
    elif a.mode == "audio":
        build = lambda c: base_cmd(a, c) + ["-x", "--audio-format", "wav", "--postprocessor-args", "ffmpeg:-ar 16000 -ac 1"] + sect + ["-o", tpl, a.url]
    else:
        h = a.max_height
        build = lambda c: base_cmd(a, c) + ["-f", f"bv*[height<={h}]+ba/b[height<={h}]", "--merge-output-format", "mp4"] + sect + ["-o", tpl, a.url]
    code, out, err, used2 = attempt(a, build)
    rec["cookies_used"] = bool(used or used2)
    rec["cookies_browser"] = used or used2
    new = sorted(set(os.listdir(outdir)) - before - {"fetch-log.jsonl"})
    if code != 0 and new:
        print("  AVISO: se obtuvo parte del material; el resto fallo: " + ((err or out).strip().splitlines() or ["?"])[-1][:160])
        rec["warning"] = (err or out)[-300:]
    if code != 0 and not new:
        log(outdir, {**rec, "error": (err or out)[-300:]})
        sys.exit("ERROR:\n" + (err or out)[-600:])
    rec["files"] = [{"name": f, "bytes": os.path.getsize(os.path.join(outdir, f))} for f in new]
    if a.mode == "subs":
        vtts = [f for f in new if f.endswith(".vtt")]
        if not vtts:
            print("  Sin subtitulos en los idiomas pedidos (" + a.langs + "). Alternativa: audio + transcribe_words.py.")
        for v in vtts:
            txt = os.path.join(outdir, v[:-4] + ".txt")
            open(txt, "w", encoding="utf-8").write(vtt_to_text(os.path.join(outdir, v)))
            print("  transcripcion limpia:", txt)
    for f in rec["files"]:
        print(f"  {f['name']}  ({f['bytes'] / 1e6:.2f} MB)")
    log(outdir, rec)
    print("  registrado en fetch-log.jsonl. Recordatorio: referencia/analisis; no republicar.")


if __name__ == "__main__":
    main()
