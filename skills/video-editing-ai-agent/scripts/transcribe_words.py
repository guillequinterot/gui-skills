#!/usr/bin/env python
"""Transcripción local por palabra (faster-whisper). No sube audio a ningún servicio.

Uso: python transcribe_words.py clip1.mp4 [clip2.mp4 ...] --lang en --model small --out words.json
Salida: {"clip1.mp4": [{"s":0.0,"e":0.4,"w":"Good"}, ...], ...}
Aviso: el inicio de la primera palabra tras un silencio largo suele salir en 0.0 → corrige con silencedetect
(ver references/captions-subtitles.md). El copy oficial manda sobre el texto transcrito.
"""
import argparse, json, os, subprocess, tempfile, shutil


def ffmpeg_path():
    sc = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Programs", "Shotcut", "ffmpeg.exe")
    return sc if os.path.exists(sc) else shutil.which("ffmpeg")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("clips", nargs="+")
    ap.add_argument("--lang", default="en")
    ap.add_argument("--model", default="small")
    ap.add_argument("--out", default="words.json")
    a = ap.parse_args()
    from faster_whisper import WhisperModel
    ff = ffmpeg_path()
    model = WhisperModel(a.model, device="cpu", compute_type="int8")
    out = {}
    for c in a.clips:
        wav = os.path.join(tempfile.gettempdir(), "tw_" + os.path.basename(c) + ".wav")
        subprocess.run([ff, "-v", "error", "-y", "-i", c, "-ar", "16000", "-ac", "1", wav], check=True)
        segs, _ = model.transcribe(wav, word_timestamps=True, language=a.lang)
        out[os.path.basename(c)] = [{"s": round(w.start, 3), "e": round(w.end, 3), "w": w.word.strip()} for sg in segs for w in sg.words]
        print(os.path.basename(c), " ".join(x["w"] for x in out[os.path.basename(c)]))
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("guardado", a.out)


if __name__ == "__main__":
    main()
