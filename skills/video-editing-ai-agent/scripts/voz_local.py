#!/usr/bin/env python
"""Voz LOCAL (Kokoro, sin créditos ni salida de datos): guion hablado -> voz.wav + tiempos por palabra con el texto correcto del guion.

Por qué: la voz de marca va por ElevenLabs (créditos, el texto sale a un servicio externo). Para borradores, pruebas de tiempo,
versiones derivadas y piezas internas, esto da una voz gratis en la propia máquina. Método de explainroo/argo (MIT) reimplementado
aquí: se trocea el guion en frases, cada frase se sintetiza por separado (silencio entre frases 0.3 s, entre párrafos 0.55 s,
`[pause s]` explícito), se recorta el silencio de cada trozo, se une, y el resultado se re-transcribe con Whisper local y se alinea
con el guion (`align_script.py`) para sacar tiempos por palabra y un `matchRate`.

Instalación (una vez; ver references/narracion-y-demos.md §4): un entorno propio FUERA del repo en ~/.gui-skills/kokoro con
`kokoro-onnx` (MIT) y los modelos `kokoro-v1.0.onnx` (310 MB) y `voices-v1.0.bin` (26 MB) de la release oficial. Este script se
ejecuta con el python de ESE entorno (Kokoro) y llama al python base (faster-whisper) para la alineación:
  ~/.gui-skills/kokoro/venv/Scripts/python scripts/voz_local.py guion.txt -o salida/ [--voice ef_dora] [--speed 0.95] [--align] [--lang es]
  ~/.gui-skills/kokoro/venv/Scripts/python scripts/voz_local.py --doctor

Sintaxis del guion: la misma de align_script.py: [#marca], [pause 0.6], {mostrado|hablado}, líneas `> nota`; una línea en blanco = párrafo.
Salida: voz.wav (24 kHz mono), voz-chunks.json (frases con inicio/fin, hash), y con --align: voz-words.json (transcripción) y guion-words.json.
Caché por hash de (frase hablada, voz, velocidad, idioma, tamaño del modelo): solo se regenera lo que cambió.
Voces en español: ef_dora (femenina), em_alex y em_santa (masculinas). NO se puede oír desde aquí: el control es el `matchRate` de Whisper
sobre la propia voz (si Whisper entiende el guion, la dicción es al menos inteligible); la decisión de la voz de marca es de una persona que escucha.
Palabras en inglés dentro de un texto en español pueden pronunciarse raro («bot»): escríbelas con {bot|bót} o como se pronunciarían.
"""
import argparse, hashlib, json, os, re, subprocess, sys

for _st in (sys.stdout, sys.stderr):  # Windows: consola cp1252 + tuberia
    try:
        _st.reconfigure(errors="replace")
    except Exception:
        pass

HERE = os.path.dirname(os.path.abspath(__file__))
KDIR = os.environ.get("VEA_KOKORO_DIR") or os.path.join(os.path.expanduser("~"), ".gui-skills", "kokoro")
MODEL = os.path.join(KDIR, "models", "kokoro-v1.0.onnx")
VOICES = os.path.join(KDIR, "models", "voices-v1.0.bin")
SR = 24000
GAP_SENT, GAP_PARA = 0.30, 0.55


def spoken_text(raw):
    """Guion -> lista de ('texto', pausa_antes_en_s). Usa la forma HABLADA de {mostrado|hablado}; quita marcadores y notas."""
    out, para_break, carry = [], False, 0.0
    for line in raw.splitlines():
        if line.lstrip().startswith(">") or line.lstrip().startswith("#"):
            continue
        if not line.strip():
            para_break = True
            continue
        s = re.sub(r"\{[^|}]+\|([^}]+)\}", r"\1", line)
        pause = 0.0
        for m in re.finditer(r"\[pause\s+([\d.]+)\]", s):
            pause += min(10.0, float(m.group(1)))
        s = re.sub(r"\[pause\s+[\d.]+\]", " ", s)
        s = re.sub(r"\[#[\w-]+\]", "", s)
        s = re.sub(r"\s+", " ", s).strip()
        if not s:
            carry += pause                      # [pause x] en su propia linea: se suma a la pausa de la frase siguiente
            continue
        pause += carry
        carry = 0.0
        parts = [p.strip() for p in re.split(r"(?<=[.!?…])\s+", s) if p.strip()]
        for i, p in enumerate(parts):
            gap = GAP_PARA if (para_break and i == 0 and out) else (GAP_SENT if out else 0.0)
            if i == 0:
                gap += pause
            out.append((p, gap))
        para_break = False
    return out


def trim(x, thr=0.004, keep=0.04):
    import numpy as np
    win = int(0.01 * SR)
    if len(x) < win * 4:
        return x
    n = len(x) // win
    peak = np.abs(x[:n * win]).reshape(n, win).max(axis=1)
    idx = np.where(peak > thr)[0]
    if len(idx) == 0:
        return x
    a = max(0, idx[0] * win - int(keep * SR))
    b = min(len(x), (idx[-1] + 1) * win + int(keep * SR))
    return x[a:b]


def doctor():
    ok = True
    for name, p in (("modelo", MODEL), ("voces", VOICES)):
        e = os.path.exists(p)
        ok &= e
        print(f"{'OK ' if e else 'FALTA'} {name}: {p}" + (f" ({os.path.getsize(p) // 1048576} MB)" if e else ""))
    try:
        import kokoro_onnx  # noqa: F401
        print("OK  kokoro_onnx importable")
    except Exception as e:  # noqa
        ok = False
        print("FALTA kokoro_onnx en este python:", e, "-> usa el python de ~/.gui-skills/kokoro/venv")
    base = os.path.join(sys.base_prefix, "python.exe")
    print(("OK  " if os.path.exists(base) else "AVISO ") + "python base para Whisper:", base)
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("guion", nargs="?")
    ap.add_argument("-o", "--out", default="voz-local")
    ap.add_argument("--voice", default="ef_dora")
    ap.add_argument("--speed", type=float, default=0.95)
    ap.add_argument("--lang", default="es")
    ap.add_argument("--align", action="store_true", help="re-transcribir con Whisper local y alinear con el guion")
    ap.add_argument("--doctor", action="store_true")
    a = ap.parse_args()
    if a.doctor:
        sys.exit(doctor())
    if not a.guion:
        ap.error("falta el guion (o usa --doctor)")
    import numpy as np, soundfile as sf
    from kokoro_onnx import Kokoro
    if not (os.path.exists(MODEL) and os.path.exists(VOICES)):
        sys.exit("ERROR: faltan los modelos de Kokoro; mira --doctor y references/narracion-y-demos.md §4")
    chunks = spoken_text(open(a.guion, encoding="utf-8").read())
    if not chunks:
        sys.exit("ERROR: el guion no tiene texto hablado")
    os.makedirs(a.out, exist_ok=True)
    cache = os.path.join(a.out, "cache")
    os.makedirs(cache, exist_ok=True)
    k = None
    msize = os.path.getsize(MODEL)
    pieces, meta, t = [], [], 0.0
    for text, gap in chunks:
        h = hashlib.sha256(json.dumps([text, a.voice, a.speed, a.lang, msize], ensure_ascii=False).encode()).hexdigest()[:16]
        cp = os.path.join(cache, h + ".wav")
        if os.path.exists(cp):
            x, _ = sf.read(cp, dtype="float32")
            src = "cache"
        else:
            if k is None:
                k = Kokoro(MODEL, VOICES)
            x, sr = k.create(text, voice=a.voice, speed=a.speed, lang=a.lang)
            x = trim(np.asarray(x, dtype="float32"))
            sf.write(cp, x, SR)
            src = "nuevo"
        if gap > 0:
            pieces.append(np.zeros(int(gap * SR), dtype="float32")); t += gap
        start = t
        pieces.append(x); t += len(x) / SR
        meta.append({"text": text, "from": round(start, 3), "to": round(t, 3), "hash": h, "origen": src})
    wav = os.path.join(a.out, "voz.wav")
    sf.write(wav, np.concatenate(pieces), SR)
    json.dump({"voz": a.voice, "velocidad": a.speed, "idioma": a.lang, "duracion_s": round(t, 3), "chunks": meta},
              open(os.path.join(a.out, "voz-chunks.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    nuevos = sum(1 for m in meta if m["origen"] == "nuevo")
    print(f"voz.wav {t:.1f} s, {len(meta)} frases ({nuevos} generadas, {len(meta) - nuevos} de caché) -> {wav}")
    if a.align:
        py = os.path.join(sys.base_prefix, "python.exe")
        words = os.path.join(a.out, "voz-words.json")
        r = subprocess.run([py, os.path.join(HERE, "transcribe_words.py"), wav, "--lang", a.lang, "--out", words], capture_output=True, text=True)
        if r.returncode != 0:
            sys.exit("ERROR al transcribir: " + (r.stderr or r.stdout)[-300:])
        r = subprocess.run([py, os.path.join(HERE, "align_script.py"), a.guion, words, "--key", "voz.wav", "-o", os.path.join(a.out, "guion-words.json"),
                            "--srt", os.path.join(a.out, "guion.srt")], capture_output=True, text=True, encoding="utf-8", errors="replace")
        print(r.stdout.strip())
        sys.exit(r.returncode)


if __name__ == "__main__":
    main()
