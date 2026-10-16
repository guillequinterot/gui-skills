"""Utilidades compartidas: localizar ffmpeg/ffprobe (Shotcut o PATH) y helpers de medicion."""
import json, os, re, shutil, subprocess, sys

# Windows: con stdout redirigido (tuberia) Python usa cp1252 y revienta al imprimir un titulo con caracteres como "：" (dos puntos de
# ancho completo que yt-dlp pone en los nombres de archivo). Los caracteres imposibles se sustituyen en vez de lanzar UnicodeEncodeError.
for _st in (sys.stdout, sys.stderr):
    try:
        _st.reconfigure(errors="replace")
    except Exception:
        pass

SC_DIR = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Programs", "Shotcut")


def _bin(name):
    p = os.path.join(SC_DIR, name + ".exe")
    return p if os.path.exists(p) else (shutil.which(name) or name)


FFMPEG = _bin("ffmpeg")
FFPROBE = _bin("ffprobe")


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def probe_duration(path):
    r = run([FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)])
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0


def probe_stream(path):
    r = run([FFPROBE, "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height,avg_frame_rate,r_frame_rate,color_transfer:stream_side_data=rotation", "-of", "json", str(path)])
    try:
        return (json.loads(r.stdout).get("streams") or [{}])[0]
    except Exception:
        return {}


def measure_loudness(path, ss=None, t=None):
    """LUFS integrado y pico (dBFS) de un tramo."""
    cmd = [FFMPEG, "-hide_banner"]
    if ss is not None:
        cmd += ["-ss", str(ss)]
    if t is not None:
        cmd += ["-t", str(t)]
    cmd += ["-i", str(path), "-vn", "-af", "ebur128=peak=true", "-f", "null", "-"]
    err = run(cmd).stderr
    i = re.findall(r"I:\s+(-?\d+\.?\d*) LUFS", err)  # privacy-scan: ignore (regex del texto de ffmpeg, no es una ruta)
    p = re.findall(r"Peak:\s+(-?\d+\.?\d*) dBFS", err)
    return (float(i[-1]) if i else None), (float(p[-1]) if p else None)


def pcm_mono(path, ss=None, t=None, sr=16000):
    """Audio mono float [-1,1] a `sr` Hz (numpy)."""
    import numpy as np, tempfile
    raw = os.path.join(tempfile.gettempdir(), "vea_pcm.raw")
    cmd = [FFMPEG, "-v", "error", "-y"]
    if ss is not None:
        cmd += ["-ss", str(ss)]
    if t is not None:
        cmd += ["-t", str(t)]
    cmd += ["-i", str(path), "-vn", "-ac", "1", "-ar", str(sr), "-f", "s16le", raw]
    subprocess.run(cmd, check=True)
    return np.fromfile(raw, dtype="<i2").astype(float) / 32768


def memory_dir():
    """Carpeta de memoria (videos aprobados, aprendizajes). Orden: $VEA_MEMORY_DIR > <skill>/memoria (relativa a este script).
    En el repo gui-skills la memoria vive dentro de la propia skill (`memoria/`), asi que se versiona con ella; al instalar la skill
    como enlace en ~/.claude/skills, la ruta resuelve al mismo clon y hay UNA sola memoria. Nunca se escribe una ruta personal fija."""
    env = os.environ.get("VEA_MEMORY_DIR")
    if env:
        return env
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "memoria")
