"""site_seo_gate.py: puerta SEO de un sitio de servicios sobre una carpeta de build (HTML estatico) y, opcionalmente, en vivo.

Nace de la auditoria de un sitio sano tecnicamente que no posicionaba (ver references/service-site-seo-gate.md).
Un linter que solo comprueba que la keyword principal sea unica como cadena exacta NO detecta canibalizacion: este script
marca los pares de paginas que comparten la frase raiz del titulo o del H1, las aperturas casi iguales, las paginas de
servicio delgadas, el lang/hreflang inconsistente, las imagenes sin atributo alt y el host que no redirige.

Uso (solo lectura, solo biblioteca estandar):
  python -I site_seo_gate.py <carpeta-dist> [--min-palabras 800] [--umbral-apertura 0.4] [--prefijo-servicio servicios,services] [--json]
  python -I site_seo_gate.py --live https://ejemplo.com [--ruta /blog/]
  (se pueden combinar ambos)
Salida 0 si no hay FALLOS; 1 si los hay. Los AVISOS son candidatos a verificar con Search Console, no hallazgos confirmados.
"""
import argparse
import http.client
import json
import os
import re
import sys
import unicodedata
from html.parser import HTMLParser
from urllib.parse import urlsplit

STOP = set("""a al algo ante con contra cual cuando de del desde donde e el ella ellos en entre es esa ese esta este esto la las le les lo los
mas me mi mis mucho muy no nos o para pero por que se si sin sobre su sus te tu tus un una uno unos y ya como cada otra otro""".split())
GENERICAS = set("clave claves guia ideas decisiones paso pasos tips mejor mejores manera forma".split())  # palabras de relleno que no definen una busqueda
LEGALES = ("privacy", "terms", "data-policy", "privacidad", "terminos", "politica", "cookies", "legal")
SECCIONES_SERVICIO = {
    "para quien es": r"para qui[eé]n",
    "que incluye": r"qu[eé] incluye|incluye",
    "proceso": r"proceso|c[oó]mo trabajo|c[oó]mo funciona",
    "preguntas frecuentes": r"preguntas|faq",
    "caso o prueba": r"caso|proyecto|resultado|portafolio",
}


def sin_acentos(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def palabras(s):
    return re.findall(r"[a-z0-9ñ]+", sin_acentos(s.lower()))


def tronco(w):
    if len(w) > 4 and w.endswith("s"):
        w = w[:-1]
    return w[:5]


class Pagina(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.meta = ""
        self.robots = ""
        self.canonical = ""
        self.lang = ""
        self.hreflang = []
        self.h1 = []
        self.encabezados = []
        self.imgs = []
        self.navs = []
        self.main_txt = []
        self.cuerpo_txt = []
        self._pila = []
        self._en = {"title": False, "main": 0, "nav": 0, "header": 0, "footer": 0, "script": 0, "style": 0, "li": 0}
        self._h = None
        self._h_txt = []
        self._cont = []  # contenedores a/button abiertos

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.lang = a.get("lang", "")
        elif tag == "title":
            self._en["title"] = True
        elif tag == "meta":
            n = (a.get("name") or "").lower()
            if n == "description":
                self.meta = a.get("content", "")
            elif n == "robots":
                self.robots = (a.get("content") or "").lower()
        elif tag == "link":
            rel = (a.get("rel") or "").lower()
            if rel == "canonical":
                self.canonical = a.get("href", "")
            elif rel == "alternate" and a.get("hreflang"):
                self.hreflang.append(a["hreflang"])
        elif tag in ("script", "style", "main", "nav", "header", "footer", "li"):
            self._en[tag] += 1
            if tag == "nav":
                self.navs.append({"enlaces": 0, "en_lista": 0, "donde": "nav"})
            if tag == "footer":
                self.navs.append({"enlaces": 0, "en_lista": 0, "donde": "footer"})
        elif tag in ("h1", "h2", "h3"):
            self._h, self._h_txt = tag, []
        if tag in ("a", "button"):
            self._cont.append({"aria": bool((a.get("aria-label") or "").strip()), "texto": 0, "imgs": []})
            if tag == "a" and self.navs and (self._en["nav"] or self._en["footer"]):
                self.navs[-1]["enlaces"] += 1
                if self._en["li"]:
                    self.navs[-1]["en_lista"] += 1
        if tag == "img":
            im = {"alt": a.get("alt"), "src": a.get("src", ""), "etiquetada": False}
            self.imgs.append(im)
            if self._cont:
                self._cont[-1]["imgs"].append(im)

    def handle_endtag(self, tag):
        if tag == "title":
            self._en["title"] = False
        elif tag in ("script", "style", "main", "nav", "header", "footer", "li") and self._en[tag]:
            self._en[tag] -= 1
        elif tag == self._h:
            t = re.sub(r"\s+", " ", "".join(self._h_txt)).strip()
            (self.h1 if tag == "h1" else self.encabezados).append(t if tag == "h1" else t)
            self._h = None
        if tag in ("a", "button") and self._cont:
            c = self._cont.pop()
            for im in c["imgs"]:
                im["etiquetada"] = c["aria"] or c["texto"] > 0

    def handle_data(self, data):
        if self._en["title"]:
            self.title += data
            return
        if self._en["script"] or self._en["style"]:
            return
        if self._h:
            self._h_txt.append(data)
        if self._cont:
            self._cont[-1]["texto"] += len(data.strip())
        if self._en["main"]:
            self.main_txt.append(data)
        if not (self._en["nav"] or self._en["header"] or self._en["footer"]):
            self.cuerpo_txt.append(data)

    def texto(self):
        t = " ".join(self.main_txt) if self.main_txt else " ".join(self.cuerpo_txt)
        return re.sub(r"\s+", " ", t).strip()


def url_de(raiz, archivo):
    rel = os.path.relpath(archivo, raiz).replace(os.sep, "/")
    if rel.endswith("index.html"):
        rel = rel[: -len("index.html")]
    return "/" + rel.lstrip("/")


def leer_paginas(raiz):
    pags = {}
    for d, _, fs in os.walk(raiz):
        for f in fs:
            if f != "index.html":  # los archivos sueltos (verificacion de propiedad, 404) no son paginas de contenido
                continue
            p = Pagina()
            p.feed(open(os.path.join(d, f), encoding="utf-8", errors="ignore").read())
            p.title = re.sub(r"\s+", " ", p.title).strip()
            pags[url_de(raiz, os.path.join(d, f))] = p
    return pags


def frase_raiz(titulo, ignorar):
    cabeza = re.split(r"\s[|\-–—]\s", titulo)[0]
    toks = [tronco(w) for w in palabras(cabeza) if w not in STOP and w not in ignorar and w not in GENERICAS and not w.isdigit()]
    return {frozenset(par) for par in zip(toks, toks[1:])}, cabeza


def similitud(a, b, n=3):
    def sh(t):
        w = palabras(t)[:60]
        return {tuple(w[i:i + n]) for i in range(max(0, len(w) - n + 1))}
    x, y = sh(a), sh(b)
    return len(x & y) / len(x | y) if x and y else 0.0


def revisar_estatico(raiz, a):
    fallos, avisos, info = [], [], []
    pags = leer_paginas(raiz)
    indexables = {u: p for u, p in pags.items() if "noindex" not in p.robots}
    ignorar = {w for x in (a.ignorar or "").split(",") for w in palabras(x)}
    prefijos = tuple("/" + x.strip("/ ") + "/" for x in a.prefijo_servicio.split(",") if x.strip())

    # 1) basicos por pagina y duplicados
    for campo, etiqueta in (("title", "titulo"), ("meta", "meta description")):
        vistos = {}
        for u, p in indexables.items():
            v = getattr(p, campo).strip()
            if not v:
                fallos.append(f"{u}: {etiqueta} vacio")
            vistos.setdefault(v, []).append(u)
        for v, us in vistos.items():
            if v and len(us) > 1:
                fallos.append(f"{etiqueta} duplicado en {', '.join(us)}")
    for u, p in indexables.items():
        if len(p.h1) != 1:
            fallos.append(f"{u}: {len(p.h1)} H1 (debe haber uno)")
        elif re.search(r"\s[,.;:]", p.h1[0]):
            avisos.append(f"{u}: el H1 tiene un espacio antes de un signo de puntuacion: «{p.h1[0][:70]}»")
        if not p.canonical:
            fallos.append(f"{u}: sin canonica")
        if not p.lang:
            fallos.append(f"{u}: <html> sin lang")

    # 2) imagenes: sin atributo alt = fallo; alt vacio solo es correcto si es decorativa o esta etiquetada
    decorativas = []
    for u, p in indexables.items():
        for im in p.imgs:
            if im["alt"] is None:
                fallos.append(f"{u}: imagen sin atributo alt ({im['src'][:60]})")
            elif im["alt"].strip() == "" and not im["etiquetada"] and re.search(r"logo|marca|icono", im["src"], re.I):
                avisos.append(f"{u}: posible logo con alt vacio y sin texto o aria-label alrededor ({im['src'][:60]})")
            elif im["alt"].strip() == "" and im["etiquetada"]:
                decorativas.append(u)

    if decorativas:
        info.append(f"{len(decorativas)} imagenes con alt vacio dentro de un enlace o boton con texto o aria-label en {len(set(decorativas))} paginas: correcto (decorativas); los rastreadores las cuentan como «sin alt»")
    # 3) menu y pie en listas
    sin_lista = {}
    for u, p in indexables.items():
        for nv in p.navs:
            if nv["enlaces"] >= 6 and nv["en_lista"] < nv["enlaces"]:
                sin_lista.setdefault(nv["donde"], set()).add(u)
    for donde, us in sin_lista.items():
        avisos.append(f"los enlaces del {donde} no estan dentro de ul/ol en {len(us)} paginas (plantilla: se corrige una vez, ej. {sorted(us)[0]})")

    # 4) lang y hreflang coherentes
    langs = {}
    for u, p in indexables.items():
        langs.setdefault(p.lang, []).append(u)
    if len(langs) > 1:
        avisos.append("lang inconsistente: " + "; ".join(f"«{k}»: {len(v)} paginas ({', '.join(v[:3])}{'…' if len(v) > 3 else ''})" for k, v in langs.items()))
    hl = {}
    for u, p in indexables.items():
        for h in p.hreflang:
            hl.setdefault(h, []).append(u)
    if len(hl) > 1:
        avisos.append("hreflang inconsistente: " + "; ".join(f"«{k}»: {len(v)} paginas" for k, v in hl.items()) + " (en un sitio de un solo idioma, el mismo valor en todas las plantillas o ninguno)")

    # 5) canibalizacion por frase raiz (titulo y H1)
    h1s = {}
    for u, p in indexables.items():
        if p.h1:
            h1s.setdefault(p.h1[0].strip().lower(), []).append(u)
    for h, us in h1s.items():
        if len(us) > 1:
            fallos.append(f"H1 duplicado «{h[:60]}» en {', '.join(us)}")
    for fuente, getter in (("titulo", lambda p: p.title),):
        pares = {}
        cabezas = {}
        for u, p in indexables.items():
            fr, cab = frase_raiz(getter(p), ignorar)
            cabezas[u] = cab
            for par in fr:
                pares.setdefault(par, []).append(u)
        for par, us in sorted(pares.items(), key=lambda x: -len(x[1])):
            if len(us) > 1:
                avisos.append(f"CANDIDATO a canibalizacion en el {fuente}: frase «{' '.join(sorted(par))}» (troncos) compartida por " + "; ".join(f"{u} («{cabezas[u][:50]}»)" for u in us))

    # 6) aperturas casi iguales
    urls = sorted(indexables)
    for i, u in enumerate(urls):
        for v in urls[i + 1:]:
            ta, tb = indexables[u].texto(), indexables[v].texto()
            if len(ta.split()) < 30 or len(tb.split()) < 30:
                continue
            s = similitud(ta, tb)
            if s >= a.umbral_apertura:
                avisos.append(f"CANDIDATO: aperturas parecidas ({s:.2f}) entre {u} y {v}: cada pagina debe abrir con una respuesta propia")

    # 7) paginas de servicio delgadas y secciones que faltan
    for u, p in indexables.items():
        if prefijos and u.startswith(prefijos) and u.count("/") >= 3:
            n = len(p.texto().split())
            if n < a.min_palabras:
                avisos.append(f"{u}: pagina de servicio delgada ({n} palabras; minimo orientativo {a.min_palabras})")
            enc = " ".join(p.encabezados).lower()
            faltan = [k for k, rx in SECCIONES_SERVICIO.items() if not re.search(rx, enc)]
            if faltan:
                avisos.append(f"{u}: faltan secciones de servicio por encabezado: {', '.join(faltan)}")

    # 8) sitemap y legales
    sm = os.path.join(raiz, "sitemap.xml")
    if os.path.exists(sm):
        x = open(sm, encoding="utf-8", errors="ignore").read()
        en_sm = {urlsplit(l).path for l in re.findall(r"<loc>(.*?)</loc>", x)}
        for u in indexables:
            if u not in en_sm and "noindex" not in indexables[u].robots and not u.endswith(".html"):
                avisos.append(f"{u}: indexable y fuera del sitemap")
        for u in en_sm:
            if u in pags and "noindex" in pags[u].robots:
                fallos.append(f"{u}: esta en el sitemap pero es noindex")
        fechas = re.findall(r"<lastmod>(.*?)</lastmod>", x)
        if len(fechas) > 3 and len(set(fechas)) == 1:
            avisos.append("todos los lastmod del sitemap tienen la misma fecha: probablemente no reflejan cambios reales de contenido")
    for u, p in indexables.items():
        if any(k in u for k in LEGALES):
            info.append(f"{u}: pagina legal indexable (decidir si se indexa o se pone noindex; no necesita prioridad alta en el sitemap)")
    return {"paginas": len(pags), "indexables": len(indexables), "fallos": fallos, "avisos": avisos, "info": info}


def pedir(url, sin_tls=False, resolver=None):
    s = urlsplit(url)
    host = s.hostname
    destino = (resolver or (host, s.port))
    if s.scheme == "https" and not sin_tls:
        c = http.client.HTTPSConnection(destino[0], destino[1] or 443, timeout=25)
    else:
        c = http.client.HTTPConnection(destino[0], destino[1] or 80, timeout=25)
    ruta = (s.path or "/") + ("?" + s.query if s.query else "")
    c.request("GET", ruta, headers={"Host": s.netloc, "User-Agent": "Mozilla/5.0 site-seo-gate (solo lectura)"})
    r = c.getresponse()
    r.read()
    return r.status, r.getheader("Location") or ""


def revisar_host(base, ruta, sin_tls=False, resolver=None):
    """Las cuatro variantes (http/https x con/sin www) deben terminar en un solo 301 hacia la canonica, conservando ruta y consulta."""
    b = urlsplit(base)
    apex = b.hostname[4:] if b.hostname.startswith("www.") else b.hostname
    canon = f"https://{apex}{ruta}"
    fallos, ok = [], []
    variantes = [f"https://{apex}{ruta}", f"http://{apex}{ruta}", f"http://www.{apex}{ruta}", f"https://www.{apex}{ruta}"]
    for v in variantes:
        try:
            st, loc = pedir(v, sin_tls, resolver)
        except Exception as e:  # red o TLS
            fallos.append(f"{v}: no se pudo consultar ({str(e)[:70]})")
            continue
        if v == canon:
            (ok if st == 200 else fallos).append(f"{v}: {st} (la canonica debe responder 200)" if st != 200 else f"{v}: 200 (canonica)")
        elif st in (301, 308) and loc.rstrip("/") == canon.rstrip("/"):
            ok.append(f"{v}: {st} -> {loc} (un solo salto)")
        elif st in (301, 308):
            fallos.append(f"{v}: {st} -> {loc} (no llega a la canonica {canon} en un salto; puede ser una cadena)")
        elif st in (302, 303, 307):
            fallos.append(f"{v}: redireccion temporal {st} -> {loc} (debe ser 301)")
        else:
            fallos.append(f"{v}: responde {st} en lugar de redirigir con 301 a {canon}")
    return {"canonica": canon, "ok": ok, "fallos": fallos}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dist", nargs="?", help="carpeta del build (HTML estatico)")
    ap.add_argument("--live", help="URL canonica del sitio, p. ej. https://ejemplo.com (solo lectura)")
    ap.add_argument("--ruta", default="/", help="ruta interior para la prueba en vivo (por defecto /)")
    ap.add_argument("--min-palabras", type=int, default=800)
    ap.add_argument("--umbral-apertura", type=float, default=0.4)
    ap.add_argument("--prefijo-servicio", default="servicios,services")
    ap.add_argument("--ignorar", default="", help="palabras a ignorar en la frase raiz, separadas por comas (pais, marca)")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--sin-tls", action="store_true", help="solo pruebas: trata https como http")
    ap.add_argument("--resolver", help="solo pruebas: ip:puerto al que conectar siempre")
    a = ap.parse_args(argv)
    if not a.dist and not a.live:
        ap.error("indica una carpeta de build o --live")
    out = {}
    if a.dist:
        out["estatico"] = revisar_estatico(a.dist, a)
    if a.live:
        a.ruta = "/" + a.ruta.lstrip("/")  # acepta «blog/» (en Git Bash, «/blog/» se convierte en una ruta de Windows: usa MSYS_NO_PATHCONV=1 o escribe «blog/»)
        res = None
        if a.resolver:
            h, p = a.resolver.split(":")
            res = (h, int(p))
        out["host"] = revisar_host(a.live, a.ruta, a.sin_tls, res)
    nf = sum(len(v.get("fallos", [])) for v in out.values())
    if a.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        e = out.get("estatico")
        if e:
            print(f"Paginas: {e['paginas']} ({e['indexables']} indexables)")
            for t, k in (("FALLOS", "fallos"), ("AVISOS (candidatos a verificar)", "avisos"), ("INFO", "info")):
                print(f"\n{t} ({len(e[k])})")
                for x in e[k]:
                    print("  -", x)
        h = out.get("host")
        if h:
            print(f"\nHOST canonico {h['canonica']}")
            for x in h["ok"]:
                print("  OK   ", x)
            for x in h["fallos"]:
                print("  FALLA", x)
        print("\nRESULTADO:", "SIN FALLOS" if nf == 0 else f"{nf} fallo(s)")
    return 1 if nf else 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
