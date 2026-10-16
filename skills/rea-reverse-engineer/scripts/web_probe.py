"""web_probe.py — sonda N1 de la skill rea-reverse-engineer: entiende UNA página web renderizada, sin REA y sin instalar nada.

Carga la URL en Chrome/Edge headless (Playwright), toma capturas por ancho, y mide lo que hace falta para
ENTENDER una referencia (diseño, SEO, tecnología, movimiento) sin copiarla:

  python -I web_probe.py https://ejemplo.com --out D:\\proyecto\\referencias\\ejemplo [--widths 1440,390] [--scroll] [--wait 1500]

Salida en --out:  probe.json (todo) · probe.md (resumen legible) · shot-<ancho>.png · rendered.html (DOM final)
Reglas: UNA página por llamada (no rastrea), sin login, sin saltar bloqueos; solo lectura de lo que ve cualquier visitante.
Las capturas hay que MIRARLAS (Read sobre el PNG): los números no sustituyen a la vista.
"""
import argparse, json, os, re, sys, time
from urllib.parse import urlparse

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

PROBE_JS = r"""
() => {
  const q = (s, r = document) => Array.from(r.querySelectorAll(s));
  const txt = e => (e.textContent || '').replace(/\s+/g, ' ').trim();
  const meta = n => { const e = document.querySelector(`meta[name="${n}"],meta[property="${n}"]`); return e ? e.content : null; };
  const vis = e => { const r = e.getBoundingClientRect(); const s = getComputedStyle(e); return r.width > 1 && r.height > 1 && s.visibility !== 'hidden' && s.display !== 'none'; };
  const top = (m, n = 12) => Object.entries(m).sort((a, b) => b[1] - a[1]).slice(0, n);
  const inc = (m, k) => { if (k) m[k] = (m[k] || 0) + 1; };
  const o = {};
  o.url = location.href; o.title = document.title; o.lang = document.documentElement.lang || null;
  o.meta = { description: meta('description'), robots: meta('robots'), viewport: meta('viewport'), generator: meta('generator'),
    'og:title': meta('og:title'), 'og:image': meta('og:image'), 'og:type': meta('og:type'), 'twitter:card': meta('twitter:card'), 'theme-color': meta('theme-color') };
  o.canonical = (document.querySelector('link[rel=canonical]') || {}).href || null;
  o.hreflang = q('link[rel=alternate][hreflang]').map(e => [e.hreflang, e.href]).slice(0, 30);
  o.headings = q('h1,h2,h3').slice(0, 80).map(e => [e.tagName, txt(e).slice(0, 140)]);
  const types = a => Array.isArray(a) ? a.flatMap(types) : (a && typeof a === 'object' ? [a['@type']].flat().concat(a['@graph'] ? types(a['@graph']) : []) : []);
  o.jsonld = q('script[type="application/ld+json"]').flatMap(e => { try { return types(JSON.parse(e.textContent)); } catch (_) { return ['(json inválido)']; } }).filter(Boolean);
  o.textLength = (document.body.innerText || '').length;

  // enlaces
  const host = location.hostname.replace(/^www\./, '');
  const L = { internal: 0, external: 0, nofollow: 0, mailto: 0, tel: 0 };
  q('a[href]').forEach(a => { const h = a.getAttribute('href') || '';
    if (h.startsWith('mailto:')) L.mailto++; else if (h.startsWith('tel:')) L.tel++;
    else { try { const u = new URL(h, location.href); (u.hostname.replace(/^www\./, '') === host ? L.internal++ : L.external++); } catch (_) {} }
    if (/nofollow/.test(a.rel)) L.nofollow++; });
  o.links = L;
  o.nav = q('nav a, header a').filter(vis).slice(0, 24).map(a => txt(a).slice(0, 40)).filter(Boolean);

  // imágenes / medios
  const imgs = q('img'); const fmt = {};
  imgs.forEach(i => inc(fmt, ((i.currentSrc || i.src || '').split('?')[0].match(/\.(avif|webp|png|jpe?g|gif|svg)$/i) || ['', 'otro'])[1].toLowerCase()));
  o.images = { total: imgs.length, sinAlt: imgs.filter(i => !i.hasAttribute('alt')).length, altVacio: imgs.filter(i => i.getAttribute('alt') === '').length,
    lazy: imgs.filter(i => i.loading === 'lazy').length, sobredimensionadas: imgs.filter(i => i.naturalWidth > (i.clientWidth || 1) * 2 && i.clientWidth > 0).length,
    formatos: fmt, picture: q('picture').length, svgInline: q('svg').length, video: q('video').length, iframe: q('iframe').length, canvas: q('canvas').length };

  // tipografía
  const fams = {}; const sizes = {}; const colors = {}; const bgs = {}; const radii = {}; const shadows = {}; const gaps = {};
  const els = q('body *').slice(0, 5000);
  let sticky = 0, snap = 0, backdrop = 0, blend = 0, gridN = 0, flexN = 0, trans = 0, anim = 0;
  els.forEach(e => { const s = getComputedStyle(e); if (!vis(e)) return;
    if (e.childNodes.length && Array.from(e.childNodes).some(n => n.nodeType === 3 && n.textContent.trim())) {
      inc(fams, s.fontFamily.split(',')[0].replace(/["']/g, '').trim()); inc(sizes, s.fontSize); inc(colors, s.color); }
    if (s.backgroundColor && !/rgba\(0, 0, 0, 0\)|transparent/.test(s.backgroundColor)) inc(bgs, s.backgroundColor);
    if (s.borderRadius && s.borderRadius !== '0px') inc(radii, s.borderRadius);
    if (s.boxShadow && s.boxShadow !== 'none') inc(shadows, s.boxShadow.slice(0, 90));
    if (s.position === 'sticky') sticky++; if (s.scrollSnapType && s.scrollSnapType !== 'none') snap++;
    if (s.backdropFilter && s.backdropFilter !== 'none') backdrop++; if (s.mixBlendMode && s.mixBlendMode !== 'normal') blend++;
    if (s.display === 'grid') gridN++; if (s.display === 'flex') flexN++;
    if (s.transitionDuration && !/^0s(, 0s)*$/.test(s.transitionDuration)) trans++;
    if (s.animationName && s.animationName !== 'none') anim++;
    if (s.rowGap && s.rowGap !== 'normal' && s.rowGap !== '0px') inc(gaps, s.rowGap); });
  o.tokens = { fuentes: top(fams, 6), tamanos: top(sizes, 14), colorTexto: top(colors, 8), fondos: top(bgs, 10), radios: top(radii, 8), sombras: top(shadows, 5), gaps: top(gaps, 10) };
  const style = sel => { const e = q(sel).find(vis); if (!e) return null; const s = getComputedStyle(e);
    return { fuente: s.fontFamily.split(',')[0].replace(/["']/g, '').trim(), tam: s.fontSize, peso: s.fontWeight, interlineado: s.lineHeight, tracking: s.letterSpacing, color: s.color, transform: s.textTransform, texto: txt(e).slice(0, 60) }; };
  o.escalaTipografica = {}; ['h1', 'h2', 'h3', 'p', 'a', 'button', 'nav a', 'li', 'small'].forEach(s => { o.escalaTipografica[s] = style(s); });
  o.fuentesCargadas = Array.from(document.fonts).filter(f => f.status === 'loaded').map(f => f.family.replace(/["']/g, '') + ' ' + f.weight + (f.style !== 'normal' ? ' ' + f.style : '')).slice(0, 30);

  // variables CSS (solo hojas accesibles) y @keyframes
  const vars = {}; const kf = [];
  Array.from(document.styleSheets).forEach(sh => { let rules; try { rules = sh.cssRules; } catch (_) { return; }
    Array.from(rules || []).forEach(r => { if (r.type === 7) kf.push(r.name);
      if (r.style && /^(:root|html|body)$/.test(r.selectorText || '')) Array.from(r.style).filter(p => p.startsWith('--')).forEach(p => { if (Object.keys(vars).length < 160) vars[p] = r.style.getPropertyValue(p).trim().slice(0, 60); }); }); });
  o.variablesCss = vars; o.keyframes = Array.from(new Set(kf)).slice(0, 40);
  o.hojasCss = { total: document.styleSheets.length, inaccesibles: Array.from(document.styleSheets).filter(sh => { try { sh.cssRules; return false; } catch (_) { return true; } }).length };

  // layout
  const maxw = {}; q('body *').slice(0, 3000).forEach(e => { const s = getComputedStyle(e); if (s.maxWidth !== 'none' && e.getBoundingClientRect().width > 500) inc(maxw, s.maxWidth); });
  o.layout = { anchoMaxContenedor: top(maxw, 5), scrollHeight: document.documentElement.scrollHeight, grid: gridN, flex: flexN, sticky, scrollSnap: snap };
  o.secciones = q('main > *, body > section, body > div > section, section').filter(vis).slice(0, 40).map(e => {
    const r = e.getBoundingClientRect(); const s = getComputedStyle(e);
    return { tag: e.tagName.toLowerCase(), id: e.id || null, clase: (e.className && e.className.baseVal === undefined ? String(e.className) : '').slice(0, 50), alto: Math.round(r.height), fondo: s.backgroundColor, h: (e.querySelector('h1,h2,h3') ? txt(e.querySelector('h1,h2,h3')).slice(0, 60) : ''), texto: txt(e).slice(0, 70) }; });

  // movimiento
  const W = window; const lib = {
    gsap: !!W.gsap, ScrollTrigger: !!W.ScrollTrigger, Lenis: !!W.Lenis || !!document.querySelector('.lenis'), locomotive: !!document.querySelector('[data-scroll-container]'),
    AOS: !!W.AOS || !!document.querySelector('[data-aos]'), Swiper: !!W.Swiper || !!document.querySelector('.swiper'), Splide: !!document.querySelector('.splide'),
    three: !!W.THREE, canvasWebGL: q('canvas').length > 0, lottie: !!W.lottie || !!document.querySelector('lottie-player,dotlottie-player'), framerMotion: !!document.querySelector('[data-framer-name],[style*="--framer"]'),
    webflowIX: !!W.Webflow, barba: !!W.barba, anime: !!W.anime, jquery: !!W.jQuery };
  o.movimiento = { librerias: Object.keys(lib).filter(k => lib[k]), animacionesWebAnimations: (document.getAnimations ? document.getAnimations().length : null),
    elementosConTransition: trans, elementosConAnimation: anim, backdropFilter: backdrop, mixBlend: blend, prefersReducedMotion: Array.from(document.styleSheets).some(sh => { try { return Array.from(sh.cssRules).some(r => r.media && /prefers-reduced-motion/.test(r.media.mediaText)); } catch (_) { return false; } }) };

  // tecnología (huellas, no certezas)
  const html = document.documentElement.outerHTML; const fp = [];
  const t = (n, c) => { if (c) fp.push(n); };
  t('Next.js', W.__NEXT_DATA__ || /_next\/static/.test(html)); t('Nuxt', W.__NUXT__ || /_nuxt\//.test(html)); t('Astro', /\/_astro\//.test(html) || !!document.querySelector('astro-island'));
  t('React', !!document.querySelector('[data-reactroot]') || !!W.__REACT_DEVTOOLS_GLOBAL_HOOK__); t('Vue', !!W.__VUE__ || !!document.querySelector('[data-v-app]')); t('Svelte', /svelte-/.test(html));
  t('módulos ES con bundle en /assets (Vite/TanStack, probable)', /\/assets\/[^"]+\.js/.test(html) && !!document.querySelector('script[type=module]')); t('WordPress', /wp-content|wp-includes/.test(html)); t('Elementor', /elementor/.test(html));
  t('Divi', /et-boc|et_pb_/.test(html)); t('Bricks', /brxe-|bricks-/.test(html)); t('Webflow', /webflow/i.test(html) && (W.Webflow || /\.webflow\.(com|io)|data-wf-/.test(html)));
  t('Wix', /wixstatic|wix-/.test(html)); t('Squarespace', /squarespace/.test(html)); t('Shopify', W.Shopify || /cdn\.shopify\.com/.test(html)); t('Framer', /framerusercontent|framer\.com/.test(html));
  t('GoHighLevel/LeadConnector', /leadconnectorhq|msgsndr|gohighlevel|vibepreview/.test(html)); t('Odoo', /odoo|o_website/.test(html) && !!document.querySelector('#wrapwrap, .o_website_page'));
  t('Tailwind (probable)', /class="[^"]*\b(flex|grid|px-\d|py-\d|text-(sm|lg|xl)|bg-\w+-\d{3})\b/.test(html)); t('Bootstrap', /bootstrap/.test(html) && !!document.querySelector('.container, .row'));
  o.tecnologia = fp;
  const sc = q('script[src]').map(s => s.src); o.scripts = { total: q('script').length, externos: sc.length, inline: q('script:not([src])').length, lista: sc.slice(0, 40) };

  // formularios y accesibilidad rápida
  o.formularios = { forms: q('form').length, inputs: q('input,select,textarea').length, botones: q('button,[role=button],.btn').filter(vis).slice(0, 20).map(b => txt(b).slice(0, 30)).filter(Boolean) };
  o.a11y = { h1: q('h1').length, enlacesSinTexto: q('a').filter(a => !txt(a) && !a.getAttribute('aria-label') && !a.querySelector('img[alt]')).length, botonesSinNombre: q('button').filter(b => !txt(b) && !b.getAttribute('aria-label')).length,
    inputsSinEtiqueta: q('input:not([type=hidden]):not([type=submit]),select,textarea').filter(i => !i.getAttribute('aria-label') && !(i.id && document.querySelector(`label[for="${i.id}"]`)) && !i.closest('label')).length, landmarks: q('header,nav,main,footer,aside').map(e => e.tagName.toLowerCase()) };
  return o;
}
"""

SCROLL_JS = """async () => { const h = () => document.documentElement.scrollHeight; let y = 0;
  while (y < h()) { window.scrollTo(0, y); y += Math.round(innerHeight * 0.8); await new Promise(r => setTimeout(r, 180)); }
  window.scrollTo(0, 0); await new Promise(r => setTimeout(r, 300)); }"""


def raw_vs_rendered(url, ua, rendered):
    """Compara el HTML crudo (lo que ve un rastreador sin JS) con el DOM final."""
    try:
        import requests
        r = requests.get(url, headers={"User-Agent": ua}, timeout=20)
        raw = r.content.decode('utf-8', 'replace')
    except Exception as e:
        return {"error": str(e)[:160]}
    g = lambda pat, s: len(re.findall(pat, s, re.I))
    title = re.search(r"<title[^>]*>(.*?)</title>", raw, re.I | re.S)
    plain = re.sub(r"<script.*?</script>|<style.*?</style>|<[^>]+>", " ", raw, flags=re.S | re.I)
    plain = re.sub(r"\s+", " ", plain).strip()
    return {"status": r.status_code, "bytes": len(raw), "title_crudo": (title.group(1).strip()[:120] if title else None),
            "h1_crudo": g(r"<h1\b", raw), "h1_renderizado": rendered.get("a11y", {}).get("h1"),
            "jsonld_crudo": g(r'application/ld\+json', raw), "jsonld_renderizado": len(rendered.get("jsonld", [])),
            "texto_crudo": len(plain), "texto_renderizado": rendered.get("textLength"),
            "depende_de_js": len(plain) < 0.4 * max(1, rendered.get("textLength") or 1)}


def md(p, widths):
    L = []
    a = L.append
    a(f"# Sonda N1 · {p['url']}\n")
    a(f"- Título: {p['title']!r} · lang: {p['lang']} · canonical: {p['canonical']}")
    a(f"- Meta: description={'sí' if p['meta'].get('description') else 'NO'} · robots={p['meta'].get('robots')} · og:image={'sí' if p['meta'].get('og:image') else 'no'} · generator={p['meta'].get('generator')}")
    a(f"- Tecnología (huellas, no certezas): {', '.join(p['tecnologia']) or 'sin huellas claras'}")
    a(f"- Capturas: {', '.join('shot-%d.png' % w for w in widths)} — **mírelas** antes de concluir.\n")
    a("## Estructura")
    a(f"- Alto de página: {p['layout']['scrollHeight']} px · secciones detectadas: {len(p['secciones'])} · ancho máx. de contenedor: {p['layout']['anchoMaxContenedor']}")
    for i, s in enumerate(p['secciones'][:25], 1):
        a(f"  {i}. <{s['tag']}{'#' + s['id'] if s['id'] else ''}> {s['alto']}px · fondo {s['fondo']} · «{s['h'] or s['texto'][:50]}»")
    a("\n## Titulares")
    for t, x in p['headings'][:30]:
        a(f"- {t}: {x}")
    a("\n## Diseño medido")
    tk = p['tokens']
    a(f"- Fuentes: {tk['fuentes']} · cargadas: {p['fuentesCargadas'][:8]}")
    a(f"- Tamaños más usados: {tk['tamanos'][:8]}")
    a(f"- Colores de texto: {tk['colorTexto'][:5]} · fondos: {tk['fondos'][:6]}")
    a(f"- Radios: {tk['radios'][:5]} · gaps: {tk['gaps'][:6]} · sombras: {tk['sombras'][:3]}")
    a("- Escala tipográfica (primer elemento visible):")
    for k, v in p['escalaTipografica'].items():
        if v:
            a(f"  - {k}: {v['fuente']} {v['tam']}/{v['interlineado']} peso {v['peso']} tracking {v['tracking']} {v['color']} «{v['texto']}»")
    a(f"- Variables CSS en :root: {len(p['variablesCss'])} (hojas inaccesibles: {p['hojasCss']['inaccesibles']}/{p['hojasCss']['total']})")
    a("\n## Movimiento")
    m = p['movimiento']
    a(f"- Librerías: {m['librerias'] or 'ninguna detectada'} · animaciones activas: {m['animacionesWebAnimations']} · con transition: {m['elementosConTransition']} · con animation: {m['elementosConAnimation']} · @keyframes: {p['keyframes'][:10]}")
    a(f"- sticky: {p['layout']['sticky']} · scroll-snap: {p['layout']['scrollSnap']} · backdrop-filter: {m['backdropFilter']} · blend: {m['mixBlend']} · respeta prefers-reduced-motion: {m['prefersReducedMotion']}")
    a("\n## SEO / contenido")
    im = p['images']
    a(f"- Enlaces: {p['links']} · imágenes: {im['total']} (sin alt: {im['sinAlt']}, lazy: {im['lazy']}, sobredimensionadas: {im['sobredimensionadas']}, formatos {im['formatos']})")
    a(f"- JSON-LD: {sorted(set(p['jsonld'])) or 'ninguno'} · hreflang: {len(p['hreflang'])} · texto visible: {p['textLength']} caracteres")
    rv = p.get('crudoVsRenderizado', {})
    a(f"- Crudo vs renderizado: {rv}")
    a(f"- Accesibilidad rápida: {p['a11y']}")
    a("\n## Red")
    n = p['red']
    a(f"- Peticiones: {n['total']} · por tipo: {n['porTipo']} · terceros: {n['terceros'][:15]}")
    a(f"- Peso (solo respuestas que declaran content-length; las comprimidas/en trozos no cuentan, es un mínimo): {n['kb']} KB · errores de consola: {len(n['consola'])} {n['consola'][:3]} · fallos de red: {n['fallos'][:3]}")
    a(f"- Scripts: {p['scripts']['externos']} externos / {p['scripts']['inline']} inline")
    a("\n## Límites de esta sonda\n- Una sola página, sin sesión, estado inicial. No prueba hovers, menús ni flujos (eso es `capture_browser_scenario` de REA o una sesión con el navegador).\n- Las huellas de tecnología son indicios. Los tokens son valores computados de lo renderizado, no el sistema de diseño original.\n- Nada de esto autoriza copiar código, textos ni imágenes de terceros.")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--out", default=None)
    ap.add_argument("--widths", default="1440,390")
    ap.add_argument("--scroll", action="store_true", help="desplazar la página para activar carga diferida")
    ap.add_argument("--wait", type=int, default=1500, help="ms de espera tras cargar")
    ap.add_argument("--browser", default="chrome", help="canal: chrome | msedge")
    a = ap.parse_args()
    u = urlparse(a.url)
    if u.scheme not in ("http", "https"):
        sys.exit("Solo http/https.")
    out = a.out or os.path.join(os.getcwd(), "_rea", re.sub(r"[^a-z0-9.-]", "_", u.netloc.lower()))
    os.makedirs(out, exist_ok=True)
    widths = [int(x) for x in a.widths.split(",") if x.strip()]
    from playwright.sync_api import sync_playwright

    reqs, fails, cons = [], [], []
    with sync_playwright() as pw:
        try:
            br = pw.chromium.launch(channel=a.browser, headless=True)
        except Exception:
            br = pw.chromium.launch(channel="msedge", headless=True)
        ua = None
        probe = None
        for w in widths:
            ctx = br.new_context(viewport={"width": w, "height": 900}, device_scale_factor=1, locale="es-CO" if w > 600 else "es-CO")
            pg = ctx.new_page()
            ua = pg.evaluate("navigator.userAgent")
            if w == widths[0]:
                pg.on("response", lambda r: reqs.append((r.url, r.request.resource_type, r.status, r.headers.get("content-length"))))
                pg.on("requestfailed", lambda r: fails.append(r.url[:140]))
                pg.on("console", lambda m: cons.append(m.text[:160]) if m.type == "error" else None)
            try:
                pg.goto(a.url, wait_until="networkidle", timeout=45000)
            except Exception:
                pg.goto(a.url, wait_until="domcontentloaded", timeout=45000)
            pg.wait_for_timeout(a.wait)
            if a.scroll:
                pg.evaluate(SCROLL_JS)
            if w == widths[0]:
                probe = pg.evaluate(PROBE_JS)
                with open(os.path.join(out, "rendered.html"), "w", encoding="utf-8") as f:
                    f.write(pg.content())
            pg.screenshot(path=os.path.join(out, f"shot-{w}.png"), full_page=True)
            ctx.close()
        br.close()

    host = u.hostname.replace("www.", "")
    third = {}
    for url, rt, st, cl in reqs:
        h = urlparse(url).hostname or ""
        if h and not h.endswith(host):
            third[h] = third.get(h, 0) + 1
    bytype = {}
    for _, rt, _, _ in reqs:
        bytype[rt] = bytype.get(rt, 0) + 1
    probe["red"] = {"total": len(reqs), "porTipo": bytype, "terceros": sorted(third.items(), key=lambda x: -x[1]),
                    "kb": round(sum(int(c) for *_, c in reqs if c and c.isdigit()) / 1024), "consola": cons[:20], "fallos": fails[:20],
                    "errores_http": [(x[0][:100], x[2]) for x in reqs if x[2] >= 400][:10]}
    probe["crudoVsRenderizado"] = raw_vs_rendered(a.url, ua or "Mozilla/5.0", probe)
    probe["_meta"] = {"sonda": "web_probe.py", "fecha": time.strftime("%Y-%m-%d %H:%M"), "anchos": widths, "scroll": a.scroll}
    with open(os.path.join(out, "probe.json"), "w", encoding="utf-8") as f:
        json.dump(probe, f, ensure_ascii=False, indent=1)
    with open(os.path.join(out, "probe.md"), "w", encoding="utf-8") as f:
        f.write(md(probe, widths))
    print(f"OK · {out}\n  probe.md · probe.json · rendered.html · " + " · ".join(f"shot-{w}.png" for w in widths))


if __name__ == "__main__":
    main()
