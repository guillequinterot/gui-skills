"""lint_html_for_canva.py — revisa un HTML de diseño ANTES de importarlo a Canva.

Uso:  python -I lint_html_for_canva.py <archivo.html> [--w 2000 --h 1400]

Detecta lo que el importador de Canva (import-design-from-url) pierde o rompe, según lo
aprendido en el caso `caso-diplomas-01` (2026-10-08). Salida: ERROR (arréglalo), AVISO (decide), INFO (plan).
Código de salida 1 si hay ERROR.
"""
import argparse, re, sys, os

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html"); ap.add_argument("--w", type=int); ap.add_argument("--h", type=int)
    a = ap.parse_args()
    s = open(a.html, encoding="utf-8").read()
    base = os.path.dirname(os.path.abspath(a.html))
    css = " ".join(re.findall(r"<style>(.*?)</style>", s, re.S))
    body = s[s.find("<body"):] if "<body" in s else s
    err, warn, info = [], [], []

    pages = re.findall(r'<div[^>]*data-document-role="page"[^>]*>', s)
    if not pages:
        err.append('ninguna página tiene data-document-role="page" (el importador no sabrá dónde cortar páginas)')
    else:
        info.append(f"{len(pages)} página(s) con data-document-role=page")
    if re.search(r"<div[^>]*data-document-role=\"page\"[^>]*>(?:(?!</div>).)*<div[^>]*data-document-role=\"page\"", s, re.S) and False:
        pass

    m = re.search(r"\.page\s*\{[^}]*width:\s*(\d+)px[^}]*height:\s*(\d+)px", css) or re.search(r"\.page\s*\{[^}]*height:\s*(\d+)px[^}]*width:\s*(\d+)px", css)
    if m:
        w, h = int(m.group(1)), int(m.group(2))
        info.append(f"tamaño de página en CSS: {w} x {h} px")
        if a.w and (w != a.w or h != a.h):
            err.append(f"la página mide {w}x{h} y esperabas {a.w}x{a.h}")
    else:
        warn.append("no encontré `.page{width:..px;height:..px}` en el CSS (¿tamaño por otra vía?)")

    if re.search(r"(?<![-\w])transform\s*:", css):
        err.append("usa `transform:` (p. ej. translateX(-50%) para centrar). Calcula `left` explícito: el importador no garantiza transforms.")
    if re.search(r"gradient\(", css):
        err.append("usa gradientes CSS. Hornea el fondo a imagen (bake_assets.py vignette / canvas-bg) y colócalo como imagen.")
    if re.search(r"background(-image)?\s*:[^;}]*url\(", css):
        err.append("usa `background:url()`. Las imágenes de fondo no se importan: usa <img> + insert_fill/update_fill.")
    for prop in ("box-shadow", "filter", "backdrop-filter", "mix-blend-mode", "clip-path", "mask"):
        if re.search(prop + r"\s*:", css):
            warn.append(f"usa `{prop}`: no se importa fielmente; hornéalo en el asset.")
    if re.search(r"(?<![-\w])border\s*:[^;}]*\d", css) or re.search(r"border-(top|left|right|bottom)\s*:", css):
        warn.append("usa `border`: Canva lo importa como 4 rectángulos finos (sin esquinas redondeadas). Para marcos redondeados borra los 4 e inserta `insert_shape` con path.")
    if re.search(r"overflow\s*:\s*hidden", css):
        info.append("hay overflow:hidden (normal en .page); los elementos fuera de la página se recortan en Canva igual.")
    if re.search(r"text-transform\s*:\s*uppercase", css):
        warn.append("usa text-transform:uppercase. Se conserva en elementos simples, pero se pierde si el texto tiene hijos con otro estilo (<i>, <b>): escribe esos textos ya en mayúsculas o corrige con find_and_replace_text.")
    if re.search(r"<(i|b|span|em|strong)[^>]*>", body):
        info.append("hay texto con estilos mixtos (<i>/<b>/<span>): se importa como regiones de un mismo cuadro; revisa tamaño de la 1.ª región (bug conocido).")
    if not re.search(r"position\s*:\s*absolute", css):
        warn.append("ningún `position:absolute`: el diseño no está en capas posicionadas; el importador puede reflujar.")
    if re.search(r"display\s*:\s*(flex|grid)", css.replace("body{display:flex", "")):
        warn.append("usa flex/grid dentro de la página: mejor posiciones absolutas para fidelidad exacta.")

    vars_ = dict(re.findall(r"(--[\w-]+)\s*:\s*([^;}]+)", css))
    fam = set()
    for f in re.findall(r"font-family\s*:\s*([^;}]+)", css):
        m = re.match(r"\s*var\((--[\w-]+)\)", f)
        fam.add((vars_.get(m.group(1), f) if m else f).strip())
    info.append("tipografías: " + "; ".join(sorted(fam)))

    imgs = re.findall(r'<img[^>]*src="([^"]+)"', body)
    if imgs:
        info.append(f"{len(imgs)} <img> (NO se importan: súbelas con upload-asset-from-url y colócalas con insert_fill):")
        for src in sorted(set(imgs)):
            p = os.path.join(base, src)
            sz = f"{os.path.getsize(p)/1024:.0f} KB" if os.path.exists(p) else "NO EXISTE"
            info.append(f"    - {src} ({sz})")
            if not os.path.exists(p): err.append(f"asset inexistente: {src}")

    ids = re.findall(r'class="layer[^"]*"[^>]*data-layer="([^"]+)"', body)
    if not ids:
        warn.append("sin data-layer: ponle nombre a cada capa (ayuda a localizar elementos en Canva).")
    if "&nbsp;" not in body and re.search(r"trazo a trazo", body):
        pass

    for t, items in (("ERROR", err), ("AVISO", warn), ("INFO", info)):
        for i in items:
            print(f"[{t}] {i}")
    print(f"\nResumen: {len(err)} error(es), {len(warn)} aviso(s).")
    sys.exit(1 if err else 0)


if __name__ == "__main__":
    main()
