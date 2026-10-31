"""verificar_vectorizado.py — reporte de calidad de un SVG vectorizado (o dibujado) contra su original.

  python -I verificar_vectorizado.py logo.svg --source original.png --out-dir verificacion
  python -I verificar_vectorizado.py logo.svg                      # sin original: solo auditoría del SVG

Corre, con los scripts vendor del repo:
  1. render + superposición + IoU (pixel2svg-html/render_overlay.py), si se da --source;
  2. auditoría de uniones de curvas Bézier (pixel2svg-html/svg_path_audit.py);
  3. auditoría de principios de logo (logo-design-skill/svg_audit.py).
Escribe reporte.json y reporte.md en --out-dir con un semáforo. El IoU NO es una compuerta: un SVG con IoU
alto pero bordes en escalera o decenas de nodos de trazado automático se marca en rojo igual.
Salida 0 siempre que los scripts corran; el semáforo está en el reporte (no en el código de salida).
"""
import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE = Path(__file__).resolve().parent
P2S = HERE / "vendor" / "pixel2svg-html"
LDS = HERE / "vendor" / "logo-design-skill"


def find_chrome():
    if os.environ.get("CHROME_BIN") and os.path.exists(os.environ["CHROME_BIN"]):
        return os.environ["CHROME_BIN"]
    for c in (
        "C:/Program Files/Google/Chrome/Application/chrome.exe",
        "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe",
        "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
        "C:/Program Files/Microsoft/Edge/Application/msedge.exe",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    ):
        if os.path.exists(c):
            return c
    return None


def run(cmd, env):
    p = subprocess.run([sys.executable, *map(str, cmd)], capture_output=True, text=True, env=env, encoding="utf-8", errors="replace")
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("svg", type=Path)
    ap.add_argument("--source", type=Path, help="raster original para IoU y superposición")
    ap.add_argument("--out-dir", type=Path, default=Path("verificacion"))
    ap.add_argument("--budget", type=int, help="máximo de segmentos cúbicos que admite esta marca (opcional)")
    args = ap.parse_args()

    svg = args.svg.resolve()
    out = args.out_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    chrome = find_chrome()
    if chrome:
        env["CHROME_BIN"] = chrome

    rep = {"svg": str(svg.name), "chrome": bool(chrome), "checks": {}}
    flags = []  # (nivel, texto)  nivel: ROJO / AMARILLO

    # 1. superposición + IoU
    if args.source:
        if not chrome:
            rep["checks"]["overlay"] = "OMITIDO: no hay Chrome/Edge (exporta CHROME_BIN)"
            flags.append(("AMARILLO", "No se pudo comparar con el original: falta navegador headless."))
        else:
            mjson = out / "metricas.json"
            code, log = run([P2S / "render_overlay.py", svg, args.source.resolve(), "--out", out / "superposicion.png",
                             "--render-out", out / "render.png", "--report", mjson], env)
            if code == 0 and mjson.exists():
                m = json.loads(mjson.read_text(encoding="utf-8"))
                rep["checks"]["overlay"] = {k: m.get(k) for k in ("iou", "src_only_px", "render_only_px")}
                if (m.get("iou") or 0) < 0.90:
                    flags.append(("AMARILLO", f"IoU {m.get('iou')}: revisa la superposición; puede haber un desajuste estructural."))
            else:
                rep["checks"]["overlay"] = "FALLÓ: " + log.strip()[-300:]
                flags.append(("AMARILLO", "render_overlay.py falló; revisa el log del reporte."))

    # 2. uniones Bézier
    code, log = run([P2S / "svg_path_audit.py", svg, "--out-svg", out / "segmentos.svg", "--report", out / "bezier.json"]
                    + (["--budget", str(args.budget)] if args.budget else []), env)
    bj = out / "bezier.json"
    if code == 0 and bj.exists():
        b = json.loads(bj.read_text(encoding="utf-8"))
        warns = b.get("join_angle_warnings", [])
        rep["checks"]["bezier"] = {
            "segmentos_cubicos": b.get("cubic_segments"), "segmentos_recta": b.get("line_segments"),
            "uniones_>umbral": len(warns), "umbral_grados": b.get("join_angle_threshold_degrees"),
            "sobre_presupuesto": b.get("over_budget"),
        }
        cub, lin = b.get("cubic_segments") or 0, b.get("line_segments") or 0
        has_arcs = any(re.search(r"[aA]", d) for d in re.findall(r'\sd="([^"]*)"', svg.read_text(encoding="utf-8", errors="replace")))
        if has_arcs:
            # el auditor aproxima los arcos SVG con rectas: sus avisos de unión serían falsos positivos
            rep["checks"]["bezier"]["nota"] = "El trazado usa arcos (A/a): el auditor los aproxima con rectas; uniones no fiables, se omiten."
            warns = []
        if lin > 40 and lin > cub * 3:
            flags.append(("ROJO", f"{lin} segmentos rectos y {cub} curvas: parece un trazado automático por píxeles (bordes en escalera al ampliar). Reajusta con curvas o primitivas."))
        elif warns:
            flags.append(("AMARILLO", f"{len(warns)} uniones con quiebre > {b.get('join_angle_threshold_degrees')}°: confirma cuáles son esquinas de diseño; las demás son defectos."))
        if b.get("over_budget"):
            flags.append(("AMARILLO", "Más segmentos que el presupuesto indicado."))
    else:
        rep["checks"]["bezier"] = "OMITIDO/FALLÓ (el SVG puede no tener un <path> auditable): " + log.strip()[-200:]

    # 3. principios de logo
    code, log = run([LDS / "svg_audit.py", svg, "--json"], env)
    try:
        a = json.loads(log)[0]
        rep["checks"]["svg_audit"] = {k: a.get(k) for k in ("score", "anchors", "colors", "gradients", "margins", "bbox_fill_ratio")}
        rep["checks"]["svg_audit"]["hallazgos"] = a.get("findings", [])
        for f in a.get("findings", []):
            if f.get("level") == "WARN":
                flags.append(("AMARILLO", f"[{f.get('code')}] {f.get('message')}"))
            elif f.get("level") in ("ERROR", "FAIL"):
                flags.append(("ROJO", f"[{f.get('code')}] {f.get('message')}"))
    except Exception:
        rep["checks"]["svg_audit"] = "FALLÓ: " + log.strip()[-300:]
        flags.append(("AMARILLO", "svg_audit.py no devolvió JSON legible."))

    semaforo = "ROJO" if any(n == "ROJO" for n, _ in flags) else ("AMARILLO" if flags else "VERDE")
    rep["semaforo"] = semaforo
    rep["alertas"] = [{"nivel": n, "texto": t} for n, t in flags]
    (out / "reporte.json").write_text(json.dumps(rep, indent=2, ensure_ascii=False), encoding="utf-8")

    md = [f"# Verificación de vectorizado — {svg.name}", "", f"**Semáforo: {semaforo}**", ""]
    md += [f"- **{n}** — {t}" for n, t in flags] or ["- Sin alertas automáticas."]
    md += ["", "## Datos", "", "```json", json.dumps(rep["checks"], indent=2, ensure_ascii=False), "```", "",
           "> Esto es ayuda, no veredicto. Falta siempre la revisión visual de la superposición, el zoom al 400 %, la prueba a 16 px "
           "y a una tinta (ver `references/04-pruebas-y-qa.md`). Lo que no se ejecutó se declara como NO verificado.", ""]
    (out / "reporte.md").write_text("\n".join(md), encoding="utf-8")
    print(f"{semaforo}  →  {out / 'reporte.md'}")
    for n, t in flags:
        print(f"  [{n}] {t}")


if __name__ == "__main__":
    main()
