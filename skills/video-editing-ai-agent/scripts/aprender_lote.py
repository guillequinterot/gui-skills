#!/usr/bin/env python
"""Lote de video-aprender: varios links o archivos, UNO tras otro (con pausa), reanudable, con un resumen al final.

Nacio del primer uso real (2026-10-16): 11 reels de Instagram = 26 min de pared, sin intervencion. Respeta las protecciones de fetch_reference
(un video por llamada, pausa entre peticiones, sin cookies salvo que el sitio las pida, todo en local).

Uso:
  python aprender_lote.py fuentes.txt -o <carpeta del proyecto>/referencias/<tema> --goal "que quiero aprender" [--modo contenido]
                          [--glosario trading] [--rapido] [--lang es] [--max-height 1280] [--pausa 8] [--prefijo reel]
                          [--extra "--max-slides 25"] [--timeout 3600] [--dry-run]
  fuentes.txt: una fuente por linea (URL o ruta de archivo); las lineas vacias y las que empiezan por # se ignoran.
Resultado en <carpeta>: <prefijo>_NN_<codigo>/ por fuente (contenido.md, analisis.md, pantalla/...), _log_NN.txt y lote-resumen.md.
Se puede relanzar: salta las fuentes que ya tienen contenido.md. Un fallo en una fuente NO detiene el lote.
Medido (reels de 0.8-2.9 min, Ryzen 7 3700U, Whisper small CPU): ~1 min de pared por minuto de audio (descarga incluida); --rapido ahorra ~18 %.
"""
import argparse, os, re, shlex, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
try:
    sys.stdout.reconfigure(errors="replace")
except Exception:  # noqa
    pass


def codigo(src):
    if re.match(r"^https?://", src):
        partes = [p for p in src.split("?")[0].rstrip("/").split("/") if p]
        c = partes[-1] if partes else "fuente"
    else:
        c = os.path.splitext(os.path.basename(src))[0]
    return re.sub(r"[^\w\-]+", "_", c)[:40] or "fuente"


def leer(path):
    out = []
    for l in open(path, encoding="utf-8"):
        l = l.strip()
        if l and not l.startswith("#"):
            out.append(l)
    return out


def fila(out_dir, n, src, estado, seg):
    d = {"n": n, "fuente": src, "estado": estado, "seg": seg, "palabras": "", "estados": "", "muestreo": "", "canal": ""}
    cm = os.path.join(out_dir, "contenido.md")
    if os.path.exists(cm):
        t = open(cm, encoding="utf-8").read()
        m = re.search(r"(\d+) palabras", t)
        d["palabras"] = m.group(1) if m else ""
        m = re.search(r"Pantalla: (\d+) estados", t)
        d["estados"] = m.group(1) if m else ""
        m = re.search(r"Muestreo de fotogramas: (\d+)", t)
        d["muestreo"] = m.group(1) if m else ""
        m = re.search(r"canal: ([^;)]*)", t)
        d["canal"] = m.group(1).strip() if m else ""
    return d


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("fuentes"); ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--modo", default="contenido"); ap.add_argument("--goal", default="(no indicado)")
    ap.add_argument("--glosario"); ap.add_argument("--rapido", action="store_true"); ap.add_argument("--lang")
    ap.add_argument("--max-height", type=int, default=1280); ap.add_argument("--pausa", type=float, default=8.0)
    ap.add_argument("--prefijo", default="fuente"); ap.add_argument("--extra", default="", help="argumentos crudos para video_aprender.py")
    ap.add_argument("--timeout", type=int, default=3600); ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    fuentes = leer(a.fuentes)
    if not fuentes:
        sys.exit("fuentes.txt no tiene ninguna fuente")
    out = os.path.abspath(a.out)
    skill = os.path.dirname(HERE)
    try:
        if os.path.commonpath([out, skill]) == skill:
            sys.exit("no se escribe dentro de la carpeta de la skill: usa la carpeta del proyecto (-o)")
    except ValueError:
        pass
    os.makedirs(out, exist_ok=True)
    filas, t_lote = [], time.time()
    for i, src in enumerate(fuentes, 1):
        d = os.path.join(out, f"{a.prefijo}_{i:02d}_{codigo(src)}")
        if os.path.exists(os.path.join(d, "contenido.md")):
            print(f"[{i:02d}/{len(fuentes)}] {codigo(src)}: ya procesado, salto", flush=True)
            filas.append(fila(d, i, src, "ya estaba", 0))
            continue
        cmd = [sys.executable, os.path.join(HERE, "video_aprender.py"), src, "--modo", a.modo, "--goal", a.goal, "-o", d, "--max-height", str(a.max_height)]
        if a.glosario:
            cmd += ["--glosario", a.glosario]
        if a.rapido:
            cmd += ["--rapido"]
        if a.lang:
            cmd += ["--lang", a.lang]
        cmd += shlex.split(a.extra, posix=False) if a.extra else []
        if a.dry_run:
            print(f"[{i:02d}] DRY-RUN: " + " ".join(cmd), flush=True)
            continue
        t0 = time.time()
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=a.timeout)
            log = (r.stdout or "") + "\n--- STDERR ---\n" + (r.stderr or "")
            ok = os.path.exists(os.path.join(d, "contenido.md"))
            estado = "OK" if ok else f"FALLO (codigo {r.returncode})"
        except subprocess.TimeoutExpired:
            log, estado = f"tiempo limite de {a.timeout} s", "FALLO (tiempo limite)"
        seg = round(time.time() - t0)
        os.makedirs(out, exist_ok=True)
        open(os.path.join(out, f"_log_{i:02d}.txt"), "w", encoding="utf-8").write(log)
        print(f"[{i:02d}/{len(fuentes)}] {codigo(src)}: {estado} en {seg} s", flush=True)
        filas.append(fila(d, i, src, estado, seg))
        if i < len(fuentes):
            time.sleep(a.pausa)
    if a.dry_run:
        return
    L = ["# Resumen del lote", "", f"Generado por `aprender_lote.py` · {len(fuentes)} fuente(s) · {(time.time() - t_lote) / 60:.1f} min · modo {a.modo}"
         + (f" · glosario {a.glosario}" if a.glosario else "") + (" · rapido" if a.rapido else ""), "",
         "| # | Estado | s | Canal | Palabras | Estados de pantalla | Fotogramas de muestreo | Carpeta |", "|---|---|---|---|---|---|---|---|"]
    for f in filas:
        L.append(f"| {f['n']:02d} | {f['estado']} | {f['seg']} | {f['canal']} | {f['palabras']} | {f['estados']} | {f['muestreo']} | `{a.prefijo}_{f['n']:02d}_{codigo(f['fuente'])}` |")
    L += ["", "Siguiente: leer `contenido.md` de cada carpeta (y `pantalla/muestreo/hoja.jpg` o `pantalla/slides/`), verificar cifras con Python y completar `analisis.md`."]
    open(os.path.join(out, "lote-resumen.md"), "w", encoding="utf-8").write("\n".join(L))
    print(f"LOTE TERMINADO en {(time.time() - t_lote) / 60:.1f} min -> {os.path.join(out, 'lote-resumen.md')}", flush=True)


if __name__ == "__main__":
    main()
