"""build_import_html.py — junta varios HTML de UNA página cada uno en un solo HTML multipágina listo para importar a Canva.

Uso:
  python -I build_import_html.py --out combinado.html [--root carpeta] A=a.html B=b.html C=c.html

Qué hace por cada archivo (clave K = letra de la opción):
  1. Toma su <style> y su <div class="page" ...>.
  2. Prefija todos los selectores con `.optK` (sin choques de ids/clases entre páginas).
  3. Reemplaza `.center{left:50%;transform:translateX(-50%)}` por `left:Npx` explícito en cada elemento .center
     (calculado con su width). El importador no se fía de los transforms.
  4. Añade la clase optK a la página y la deja con data-document-role="page".
Si tu HTML ya es multipágina y ya está escopado (como diplomas-v2-20x14.html), NO hace falta este script.
Después: `lint_html_for_canva.py combinado.html`.
"""
import argparse, os, re


def prefix_css(css, k):
    out = []
    for sel, body in re.findall(r"([^{}]+)\{([^{}]*)\}", css):
        new = []
        for s in [x.strip() for x in sel.split(",") if x.strip()]:
            if s in ("html", "body", "html,body"):
                continue
            if s == ":root": new.append(f".opt{k}")
            elif s == "*": new.append(f".opt{k} *")
            elif s == ".page": new.append(f".page.opt{k}")
            else: new.append(f".opt{k} {s}")
        if new:
            out.append(",".join(new) + "{" + body + "}")
    return "\n".join(out)


def center_fix(css, page, page_w):
    css = css.replace(".center{left:50%;transform:translateX(-50%);text-align:center}", ".center{text-align:center}")

    def fix_rule(m):
        sel, body = m.group(1), m.group(2)
        if "translateX(-50%)" in body or "left:50%" in body:
            w = re.search(r"(?:^|;)width:(\d+)px", body)
            if w:
                left = (page_w - int(w.group(1))) // 2
                body = re.sub(r"left:50%;?", "", body)
                body = re.sub(r"transform:translateX\(-50%\);?", "", body)
                body = f"left:{left}px;" + body
        return sel + "{" + body + "}"
    css = re.sub(r"([^{}]+)\{([^{}]*)\}", fix_rule, css)
    for cid in re.findall(r'class="layer center" id="(\w+)"', page):
        m = re.search(r"#" + cid + r"\{([^{}]*)\}", css)
        w = re.search(r"(?:^|;)width:(\d+)px", m.group(1)) if m else None
        if not w:
            raise SystemExit(f"#{cid} tiene clase center pero no width en el CSS")
        if "left:" not in m.group(1):
            css = css.replace("#" + cid + "{", "#" + cid + "{left:" + str((page_w - int(w.group(1))) // 2) + "px;", 1)
    return css


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", required=True); ap.add_argument("--root", default=".")
    ap.add_argument("--page-w", type=int, default=2000, help="ancho de página en px (para centrar)")
    ap.add_argument("pairs", nargs="+", help="K=archivo.html")
    a = ap.parse_args()
    pages, styles, fonts, title = [], [], "", "Diseños"
    for pair in a.pairs:
        k, f = pair.split("=", 1)
        s = open(os.path.join(a.root, f), encoding="utf-8").read()
        css = re.search(r"<style>(.*?)</style>", s, re.S).group(1)
        page = re.search(r'(<div class="page".*?</div>\s*)</body>', s, re.S).group(1)
        css = center_fix(css, page, a.page_w)
        page = page.replace('class="page"', f'class="page opt{k}"', 1)
        if 'data-document-role="page"' not in page:
            page = page.replace(f'class="page opt{k}"', f'class="page opt{k}" data-document-role="page"', 1)
        pages.append(page); styles.append(prefix_css(css, k))
        if not fonts:
            m = re.search(r'(<link rel="preconnect".*?rel="stylesheet">)', s, re.S)
            fonts = m.group(1) if m else ""
    html = f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width={a.page_w}">
<title>{title}</title>
{fonts}
<style>
  *{{box-sizing:border-box;margin:0;padding:0}}
  html,body{{margin:0;background:#fff}}
  .layer{{position:absolute}}
{chr(10).join(styles)}
</style>
</head>
<body>
{chr(10).join(pages)}
</body>
</html>
"""
    open(a.out, "w", encoding="utf-8").write(html)
    print("OK", a.out, len(html), "bytes,", len(pages), "páginas")


if __name__ == "__main__":
    main()
