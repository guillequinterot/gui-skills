#!/usr/bin/env python3
"""Validador "listo para Figma" del método HTML -> Figma de Guille.

Revisa que paddings, margins y gaps sean múltiplos de 4 y avisa de overflow
hidden/clip. Dos modos:

  estático  (por defecto, solo librería estándar)
      Lee <style> e atributos style="" de .html/.htm/.astro/.vue y archivos .css.
      Resuelve var(--x) con las custom properties encontradas en los mismos
      archivos (pasa tokens.css junto a los componentes). rem -> x16 px.
      calc()/clamp()/min()/max() y em/%/vw se reportan como "revisar", no como error.

  --render  (opcional, requiere Playwright + Chrome instalado)
      Abre el HTML a 1920 px de ancho y mide valores computados reales:
      espaciados no múltiplos de 4, padding superior/inferior de las secciones
      de contenido (esperado 80; header/nav/menú, hero y footer exentos del 80/80
      pero no del múltiplo de 4), borde izquierdo del contenido (esperado 240),
      scroll horizontal y elementos con overflow hidden/clip.

Uso:
  python -I validate_figma_ready.py pagina.html
  python -I validate_figma_ready.py src/styles/tokens.css src/components/**/*.astro
  python -I validate_figma_ready.py pagina.html --render
  python -I validate_figma_ready.py http://127.0.0.1:8080/ --render
  Opciones: --json, --max N (líneas por sección del informe), --section-pad 80,
            --side-pad 240, --width 1920

Código de salida: 0 sin errores, 1 con errores (avisos no cambian el código).
"""

from __future__ import annotations

import argparse
import glob
import json
import re
import sys
from pathlib import Path

SPACING_PROPS = (
    "padding", "padding-top", "padding-right", "padding-bottom", "padding-left",
    "padding-inline", "padding-block", "padding-inline-start", "padding-inline-end",
    "padding-block-start", "padding-block-end",
    "margin", "margin-top", "margin-right", "margin-bottom", "margin-left",
    "margin-inline", "margin-block", "margin-inline-start", "margin-inline-end",
    "margin-block-start", "margin-block-end",
    "gap", "row-gap", "column-gap", "grid-gap", "grid-row-gap", "grid-column-gap",
)
SPACING_RE = re.compile(
    r"(?<![\w-])(" + "|".join(re.escape(p) for p in sorted(SPACING_PROPS, key=len, reverse=True)) + r")\s*:\s*([^;}\"']+)",
    re.I,
)
CUSTOM_PROP_RE = re.compile(r"(--[\w-]+)\s*:\s*([^;}]+)")
DATA_URI_RE = re.compile(r"data:[a-z]+/[a-z0-9.+-]+;base64,[A-Za-z0-9+/=\s]+", re.I)
STYLE_BLOCK_RE = re.compile(r"<style[^>]*>(.*?)</style>", re.S | re.I)
STYLE_ATTR_RE = re.compile(r"style\s*=\s*(\"([^\"]*)\"|'([^']*)')", re.I)
OVERFLOW_RE = re.compile(r"overflow(?:-x|-y)?\s*:\s*(hidden|clip)", re.I)
COMMENT_RE = re.compile(r"/\*.*?\*/", re.S)


def blank_keep_lines(text: str, pattern: re.Pattern) -> str:
    """Sustituye coincidencias por espacios conservando saltos de línea (para números de línea)."""
    return pattern.sub(lambda m: re.sub(r"[^\n]", " ", m.group(0)), text)


def collect_sources(paths: list[str]) -> list[Path]:
    out: list[Path] = []
    for p in paths:
        matches = glob.glob(p, recursive=True) or [p]
        for m in matches:
            mp = Path(m)
            if mp.is_dir():
                for ext in ("*.html", "*.htm", "*.astro", "*.vue", "*.css"):
                    out.extend(sorted(mp.rglob(ext)))
            elif mp.is_file():
                out.append(mp)
    seen, uniq = set(), []
    for f in out:
        k = str(f.resolve())
        if k not in seen and "node_modules" not in f.parts:
            seen.add(k)
            uniq.append(f)
    return uniq


def css_chunks(path: Path):
    """Devuelve (texto_css, desplazamiento_de_línea, origen) por cada bloque CSS del archivo."""
    raw = path.read_text(encoding="utf-8", errors="replace")
    raw = blank_keep_lines(raw, DATA_URI_RE)
    if path.suffix.lower() == ".css":
        yield blank_keep_lines(raw, COMMENT_RE), 0, "css"
        return
    for m in STYLE_BLOCK_RE.finditer(raw):
        line0 = raw.count("\n", 0, m.start(1))
        yield blank_keep_lines(m.group(1), COMMENT_RE), line0, "<style>"
    for m in STYLE_ATTR_RE.finditer(raw):
        body = m.group(2) if m.group(2) is not None else m.group(3)
        line0 = raw.count("\n", 0, m.start())
        yield body, line0, 'style=""'


def build_vars(files: list[Path]) -> dict[str, str]:
    vars_: dict[str, str] = {}
    for f in files:
        for css, _, _ in css_chunks(f):
            for name, val in CUSTOM_PROP_RE.findall(css):
                vars_.setdefault(name, val.strip())
    return vars_


def resolve(value: str, vars_: dict[str, str], depth: int = 0) -> str:
    if depth > 12:
        return value

    def rep(m):
        name, fallback = m.group(1), m.group(2)
        if name in vars_:
            return resolve(vars_[name], vars_, depth + 1)
        return fallback.strip() if fallback else m.group(0)

    return re.sub(r"var\(\s*(--[\w-]+)\s*(?:,\s*([^()]*))?\)", rep, value)


def split_tokens(value: str) -> list[str]:
    toks, depth, cur = [], 0, ""
    for ch in value:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch.isspace() and depth == 0:
            if cur:
                toks.append(cur)
            cur = ""
        else:
            cur += ch
    if cur:
        toks.append(cur)
    return toks


def classify(token: str):
    """-> ('ok'|'error'|'revisar'|'skip', px o None)"""
    t = token.strip().rstrip(",").replace("!important", "")
    if not t or t in ("0", "auto", "inherit", "initial", "unset", "normal", "revert"):
        return "skip", None
    if t.lower().startswith(("calc(", "clamp(", "min(", "max(", "var(")):
        return "revisar", None
    m = re.fullmatch(r"(-?\d*\.?\d+)(px|rem)?", t, re.I)
    if m:
        n = float(m.group(1)) * (16 if (m.group(2) or "").lower() == "rem" else 1)
        if n == 0:
            return "skip", 0.0
        if not m.group(2) and n != 0:
            return "revisar", n  # número sin unidad
        if abs(n) <= 1:
            return "revisar", n  # hairline / patrón visually-hidden (margin:-1px)
        return ("ok" if abs(n) % 4 == 0 else "error"), n
    return "revisar", None  # em, %, vw, ch, etc.


def static_check(files: list[Path]) -> dict:
    vars_ = build_vars(files)
    errors, review, overflow = [], [], []
    checked = 0
    for f in files:
        for css, line0, origin in css_chunks(f):
            for m in SPACING_RE.finditer(css):
                prop, raw_val = m.group(1).lower(), m.group(2).strip()
                if raw_val.startswith("--"):
                    continue
                val = resolve(raw_val, vars_)
                line = line0 + css.count("\n", 0, m.start()) + 1
                for tok in split_tokens(val):
                    kind, px = classify(tok)
                    if kind == "skip":
                        continue
                    checked += 1
                    rec = {"file": str(f), "line": line, "origin": origin, "prop": prop,
                           "value": raw_val, "resolved": val if val != raw_val else None, "token": tok, "px": px}
                    if kind == "error":
                        errors.append(rec)
                    elif kind == "revisar":
                        review.append(rec)
            for m in OVERFLOW_RE.finditer(css):
                line = line0 + css.count("\n", 0, m.start()) + 1
                overflow.append({"file": str(f), "line": line, "origin": origin, "value": m.group(0)})
    return {"mode": "static", "files": [str(f) for f in files], "checked": checked,
            "errors": errors, "review": review, "overflow": overflow, "vars_resolved": len(vars_)}


RENDER_JS = r"""
({sectionPad, sidePad}) => {
  const props = ['paddingTop','paddingRight','paddingBottom','paddingLeft','marginTop','marginRight','marginBottom','marginLeft','rowGap','columnGap'];
  const path = el => { const p = []; let e = el; for (let i = 0; e && e !== document.body && i < 3; i++, e = e.parentElement) {
      let s = e.tagName.toLowerCase(); const c = (typeof e.className === 'string' ? e.className.trim().split(/\s+/)[0] : '');
      if (e.id) s += '#' + e.id; else if (c) s += '.' + c; p.unshift(s); } return p.join(' > '); };
  const off = {}; let checked = 0; const overflow = [];
  for (const el of document.querySelectorAll('body *')) {
    const r = el.getBoundingClientRect(); if (!r.width && !r.height) continue;
    const cs = getComputedStyle(el);
    for (const p of props) {
      const n = parseFloat(cs[p]); if (!n || isNaN(n)) continue; checked++;
      const k = Math.round(n * 100) / 100;
      if (Math.abs(k % 4) > 0.01 && Math.abs(Math.abs(k % 4) - 4) > 0.01) {
        const key = p + ' ' + k + 'px'; (off[key] = off[key] || {count: 0, examples: []}).count++;
        if (off[key].examples.length < 3) off[key].examples.push(path(el));
      }
    }
    if (['hidden','clip'].includes(cs.overflow) || ['hidden','clip'].includes(cs.overflowX) || ['hidden','clip'].includes(cs.overflowY))
      if (r.width >= 160 && r.height >= 80 && el.tagName !== 'IMG') overflow.push(path(el));
  }
  // secciones de primer nivel: bloques casi a ancho completo cuyos padres no lo son
  const W = innerWidth; const sections = [];
  for (const el of document.querySelectorAll('section, header, footer, main > *, body > div > div, body > div > div > div')) {
    const r = el.getBoundingClientRect(); if (r.width < W * 0.98 || r.height < 60) continue;
    const parent = el.parentElement; const pr = parent ? parent.getBoundingClientRect() : null;
    const cs = getComputedStyle(el);
    if (sections.some(s => s.el.contains(el))) continue;
    sections.push({el, y: Math.round(r.top + scrollY), h: Math.round(r.height), name: path(el), padT: parseFloat(cs.paddingTop), padB: parseFloat(cs.paddingBottom)});
  }
  if (sections.length < 3) {  // respaldo: contenedor con más hijos a ancho completo (exports con host/runtime)
    let best = null, bestN = 0;
    for (const el of document.querySelectorAll('body, body *')) {
      const n = [...el.children].filter(c => { const r = c.getBoundingClientRect(); return r.width >= W * 0.98 && r.height >= 60; }).length;
      if (n > bestN) { best = el; bestN = n; }
    }
    if (best && bestN >= 3) {
      sections.length = 0;
      for (const el of best.children) {
        const r = el.getBoundingClientRect(); if (r.width < W * 0.98 || r.height < 60) continue;
        const cs = getComputedStyle(el);
        sections.push({el, y: Math.round(r.top + scrollY), h: Math.round(r.height), name: path(el), padT: parseFloat(cs.paddingTop), padB: parseFloat(cs.paddingBottom)});
      }
    }
  }
  // borde izquierdo del contenido: primer texto/heading dentro de cada sección
  // exentos del 80/80 (siguen obligados a múltiplos de 4): header/nav/menú, hero y footer
  const roleOf = (s, i, arr) => {
    const el = s.el; const tag = el.tagName.toLowerCase();
    const ident = ((el.id || '') + ' ' + (typeof el.className === 'string' ? el.className : '')).toLowerCase();
    if (tag === 'header' || tag === 'nav' || /(^|[\s_-])(header|nav|navbar|menu|topbar)([\s_-]|$)/.test(ident)) return 'header';
    if (tag === 'footer' || /(^|[\s_-])footer([\s_-]|$)/.test(ident)) return 'footer';
    if (/(^|[\s_-])hero([\s_-]|$)/.test(ident) || el.querySelector('h1')) return 'hero';
    if (i === arr.length - 1 && s.h < 200) return 'footer';
    return 'content';
  };
  const secOut = sections.map((s, i, arr) => {
    const t = s.el.querySelector('h1, h2, h3, p'); const x = t ? Math.round(t.getBoundingClientRect().left) : null;
    return {name: s.name, y: s.y, h: s.h, padT: s.padT, padB: s.padB, contentLeft: x, role: roleOf(s, i, arr)};
  });
  return {width: W, scrollWidth: document.documentElement.scrollWidth, docHeight: document.documentElement.scrollHeight,
          checked, offenders: Object.entries(off).sort((a, b) => b[1].count - a[1].count).map(([k, v]) => ({key: k, ...v})),
          overflow: [...new Set(overflow)], sections: secOut, sectionPad, sidePad};
}
"""


def render_check(target: str, width: int, section_pad: int, side_pad: int) -> dict:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        raise SystemExit("--render requiere Playwright (pip install playwright) y Chrome instalado.")
    import time
    url = target if re.match(r"^(https?|file)://", target) else Path(target).resolve().as_uri()
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(channel="chrome", headless=True)
        except Exception:
            browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": width, "height": 1080})
        page.goto(url, wait_until="load", timeout=90000)
        time.sleep(1.5)
        h = page.evaluate("document.documentElement.scrollHeight")
        y = 0
        while y < h:  # dispara animaciones de entrada (IntersectionObserver)
            page.evaluate(f"window.scrollTo(0,{y})")
            time.sleep(0.15)
            y += 800
        page.evaluate("window.scrollTo(0,0)")
        time.sleep(0.8)
        data = page.evaluate(RENDER_JS, {"sectionPad": section_pad, "sidePad": side_pad})
        browser.close()
    data["mode"] = "render"
    data["url"] = url
    errs = sum(o["count"] for o in data["offenders"])
    data["errors_count"] = errs
    return data


def print_static(r: dict, limit: int) -> None:
    print(f"Modo estático · {len(r['files'])} archivo(s) · {r['vars_resolved']} variables CSS resueltas")
    print(f"Valores de espaciado revisados: {r['checked']}")
    print(f"ERRORES (no múltiplo de 4): {len(r['errors'])}")
    by_val: dict[float, int] = {}
    for e in r["errors"]:
        by_val[e["px"]] = by_val.get(e["px"], 0) + 1
    if by_val:
        print("  Valores problemáticos más frecuentes: " + ", ".join(f"{k:g}px×{v}" for k, v in sorted(by_val.items(), key=lambda kv: -kv[1])[:12]))
    for e in r["errors"][:limit]:
        res = f" -> {e['resolved']}" if e["resolved"] else ""
        print(f"  {Path(e['file']).name}:{e['line']} [{e['origin']}] {e['prop']}: {e['value']}{res}  ({e['token']})")
    if len(r["errors"]) > limit:
        print(f"  … {len(r['errors']) - limit} más (usa --max o --json)")
    print(f"REVISAR a mano (calc/clamp/em/%/vw/sin unidad): {len(r['review'])}")
    for e in r["review"][: min(limit, 8)]:
        print(f"  {Path(e['file']).name}:{e['line']} {e['prop']}: {e['value']}")
    print(f"AVISO overflow hidden/clip: {len(r['overflow'])} (permitido solo en carruseles, máscaras de imagen o donde sea imprescindible)")
    for e in r["overflow"][: min(limit, 8)]:
        print(f"  {Path(e['file']).name}:{e['line']} {e['value']}")


def print_render(r: dict, limit: int) -> None:
    print(f"Modo render · {r['url']}")
    print(f"Ancho de viewport {r['width']} px · scrollWidth {r['scrollWidth']} px · alto {r['docHeight']} px (Hug)")
    if r["scrollWidth"] > r["width"]:
        print("  ERROR: hay scroll horizontal (algo se sale del ancho de diseño).")
    print(f"Valores computados revisados: {r['checked']} · ERRORES (no múltiplo de 4): {r['errors_count']}")
    for o in r["offenders"][:limit]:
        print(f"  {o['key']} ×{o['count']}  ej.: {' | '.join(o['examples'])}")
    print(f"Secciones de primer nivel detectadas: {len(r['sections'])} (esperado padding vertical {r['sectionPad']} en secciones de contenido y contenido en x={r['sidePad']}; header/menú, hero y footer exentos del {r['sectionPad']}/{r['sectionPad']})")
    for s in r["sections"]:
        flags = []
        exempt = s.get("role", "content") != "content"
        if not exempt and (s["padT"] != r["sectionPad"] or s["padB"] != r["sectionPad"]):
            flags.append(f"padding {s['padT']:g}/{s['padB']:g}")
        if exempt:
            pads_ok = all(abs(v) % 4 == 0 for v in (s["padT"], s["padB"]))
            flags.append(f"{s['role']}: exento {r['sectionPad']}/{r['sectionPad']}" + ("" if pads_ok else f"; padding {s['padT']:g}/{s['padB']:g} NO múltiplo de 4"))
        if s["contentLeft"] is not None and s["contentLeft"] != r["sidePad"]:
            flags.append(f"contenido en x={s['contentLeft']}")
        problems = [f for f in flags if "exento" not in f or "NO múltiplo" in f]
        mark = ("AVISO " if problems else "ok · ") + "; ".join(flags) if flags else "ok"
        print(f"  y={s['y']:>5} h={s['h']:>5} {s['name'][:60]:<60} {mark}")
    print(f"AVISO overflow hidden/clip en contenedores: {len(r['overflow'])}")
    for o in r["overflow"][:limit]:
        print(f"  {o}")


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # consola Windows (cp1252)
    except (AttributeError, ValueError):
        pass
    ap = argparse.ArgumentParser(description="Validador 'listo para Figma' (múltiplos de 4, 240/80, sin clip).")
    ap.add_argument("targets", nargs="+", help="Archivos/carpetas/globs, o una URL con --render")
    ap.add_argument("--render", action="store_true", help="Medir valores computados con Playwright a --width px")
    ap.add_argument("--width", type=int, default=1920)
    ap.add_argument("--section-pad", type=int, default=80)
    ap.add_argument("--side-pad", type=int, default=240)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--max", type=int, default=25)
    a = ap.parse_args()

    if a.render:
        r = render_check(a.targets[0], a.width, a.section_pad, a.side_pad)
        print(json.dumps(r, ensure_ascii=False, indent=1)) if a.json else print_render(r, a.max)
        return 1 if r["errors_count"] or r["scrollWidth"] > r["width"] else 0

    files = collect_sources(a.targets)
    if not files:
        raise SystemExit("No se encontraron archivos para revisar.")
    r = static_check(files)
    print(json.dumps(r, ensure_ascii=False, indent=1)) if a.json else print_static(r, a.max)
    return 1 if r["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
