"""extraer_modulo.py — saca HTML y CSS REALES de los componentes de un proyecto para la biblioteca de módulos.

  from extraer_modulo import configurar, elemento, css_del_modulo, a_texto, variables_usadas, raiz_vars

HTML: lee las páginas generadas (salida de la compilación) y devuelve el elemento, con su contenido, cuya clase coincide.
CSS : lee las hojas fuente y devuelve las reglas cuyo selector EMPIEZA por una clase del módulo (también sus elementos y
      modificadores BEM: .x, .x__y, .x--z), incluidas las de @media/@supports, y las variables --x que esas reglas usan.
      Las reglas de contexto (`.otra-seccion .x`) se descartan a propósito: son una diferencia entre contextos, no el módulo.
Solo lectura: no modifica nada del proyecto.
Límites: no resuelve @import ni preprocesadores (Sass, PostCSS anidado); lee CSS plano. Un componente que compone a otro
      (una tarjeta con botón) necesita pasar las clases del otro en `clases` o la vista previa sale sin su estilo.
"""
import os
import re
from html.parser import HTMLParser

DIST = None      # carpeta con las páginas generadas (p. ej. dist/)
ESTILOS = None   # carpeta con las hojas CSS fuente
ARCHIVOS_CSS = ()  # nombres de los CSS a leer dentro de ESTILOS (p. ("global.css", "base.css"))


def configurar(dist, estilos, archivos_css):
    """Indica dónde están las páginas generadas y los CSS del proyecto."""
    global DIST, ESTILOS, ARCHIVOS_CSS
    DIST, ESTILOS, ARCHIVOS_CSS = dist, estilos, tuple(archivos_css)
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}


class Nodo:
    def __init__(self, tag, attrs, padre=None):
        self.tag, self.attrs, self.padre, self.hijos = tag, attrs, padre, []

    def clases(self):
        return (dict(self.attrs).get("class") or "").split()


class Arbol(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.raiz = Nodo("#raiz", [])
        self.actual = self.raiz

    def handle_starttag(self, tag, attrs):
        n = Nodo(tag, attrs, self.actual)
        self.actual.hijos.append(n)
        if tag not in VOID:
            self.actual = n

    def handle_startendtag(self, tag, attrs):
        self.actual.hijos.append(Nodo(tag, attrs, self.actual))

    def handle_endtag(self, tag):
        n = self.actual
        while n is not None and n.tag != tag:
            n = n.padre
        if n is not None and n.padre is not None:
            self.actual = n.padre

    def handle_data(self, data):
        self.actual.hijos.append(data)

    handle_entityref = lambda self, name: self.actual.hijos.append("&%s;" % name)
    handle_charref = lambda self, name: self.actual.hijos.append("&#%s;" % name)


def arbol(ruta):
    a = Arbol()
    a.feed(open(ruta, encoding="utf-8").read())
    return a.raiz


def buscar(nodo, pred):
    for h in nodo.hijos:
        if isinstance(h, Nodo):
            if pred(h):
                yield h
            yield from buscar(h, pred)


def serializar(n, prof=0, quitar_attrs=("data-astro-cid", "srcset", "sizes", "loading", "decoding", "fetchpriority", "data-placement", "data-track")):
    pad = "  " * prof
    if isinstance(n, str):
        t = re.sub(r"\s+", " ", n).strip()
        return pad + t if t else ""
    attrs = ""
    for k, v in n.attrs:
        if k.startswith(quitar_attrs) or k in quitar_attrs:
            continue
        attrs += f' {k}="{v}"' if v is not None else f" {k}"
    if n.tag in VOID:
        return f"{pad}<{n.tag}{attrs}>"
    hijos = [s for s in (serializar(h, prof + 1, quitar_attrs) for h in n.hijos) if s]
    if not hijos:
        return f"{pad}<{n.tag}{attrs}></{n.tag}>"
    if len(hijos) == 1 and not any(isinstance(h, Nodo) for h in n.hijos) and len(hijos[0].strip()) < 90:
        return f"{pad}<{n.tag}{attrs}>{hijos[0].strip()}</{n.tag}>"
    return f"{pad}<{n.tag}{attrs}>\n" + "\n".join(hijos) + f"\n{pad}</{n.tag}>"


def elemento(pagina, clase, indice=0, exacto=None, contiene_texto=None):
    """Devuelve el HTML del elemento n.º `indice` de `pagina` (ruta relativa a dist) con esa clase."""
    raiz = arbol(os.path.join(DIST, pagina))
    def pred(n):
        cl = n.clases()
        if clase not in cl:
            return False
        if exacto is not None and " ".join(cl) != exacto:
            return False
        return True
    res = list(buscar(raiz, pred))
    if contiene_texto:
        res = [r for r in res if contiene_texto in serializar(r)]
    return serializar(res[indice]) if len(res) > indice else None


# ------------------------------------------------------------------ CSS
def partir_reglas(css):
    """Devuelve lista de bloques de primer nivel: (preludio, cuerpo) respetando llaves anidadas y comentarios."""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    salida, i, n = [], 0, len(css)
    while i < n:
        j = css.find("{", i)
        if j < 0:
            break
        pre = css[i:j].strip()
        prof, k = 1, j + 1
        while k < n and prof:
            if css[k] == "{":
                prof += 1
            elif css[k] == "}":
                prof -= 1
            k += 1
        salida.append((pre, css[j + 1:k - 1]))
        i = k
    return salida


def reglas_con_clases(css, clases, inicio=True):
    """Reglas (y @media con reglas) cuyo selector contiene alguna de `clases`.
    inicio=True: solo selectores que EMPIEZAN por una clase del módulo (descarta reglas de contexto como `.otra .clase`)."""
    pre_ = r"^(?::is\()?" if inicio else ""
    pats = [re.compile(pre_ + r"\.%s(?:(?:__|--)[\w-]+)*(?![\w-])" % re.escape(c)) for c in clases]
    def casa(sel):
        return any(p.search(sel) for p in pats)
    def filtrar(bloques):
        out = []
        for pre, cuerpo in bloques:
            if pre.startswith("@media") or pre.startswith("@supports"):
                inner = filtrar(partir_reglas(cuerpo))
                if inner:
                    out.append((pre, inner))
            elif pre.startswith("@"):
                continue
            else:
                sels = [s.strip() for s in pre.split(",") if s.strip()]
                util = [s for s in sels if casa(s)]
                if util:
                    out.append((", ".join(util), cuerpo))
        return out
    return filtrar(partir_reglas(css))


def a_texto(reglas, sangria=""):
    t = []
    for pre, cuerpo in reglas:
        if isinstance(cuerpo, list):
            t.append(f"{sangria}{pre} {{\n{a_texto(cuerpo, sangria + '  ')}\n{sangria}}}")
        else:
            decl = [d.strip() for d in cuerpo.split(";") if d.strip()]
            sels = ",\n".join(sangria + s.strip() for s in pre.split(","))
            t.append(sels + " {\n" + "\n".join(f"{sangria}  {d};" for d in decl) + f"\n{sangria}}}")
    return "\n\n".join(t)


def variables_usadas(texto):
    return sorted(set(re.findall(r"var\((--[\w-]+)", texto)))


def raiz_vars():
    out = {}
    for f in ARCHIVOS_CSS:
        css = re.sub(r"/\*.*?\*/", "", open(os.path.join(ESTILOS, f), encoding="utf-8").read(), flags=re.S)
        for m in re.finditer(r":root\s*\{([^}]*)\}", css):
            for d in re.finditer(r"(--[\w-]+)\s*:\s*([^;]+);", m.group(1)):
                out.setdefault(d.group(1), " ".join(d.group(2).split()))
    return out


def css_del_modulo(clases, inicio=True):
    todo = []
    for f in ARCHIVOS_CSS:
        css = open(os.path.join(ESTILOS, f), encoding="utf-8").read().replace("\r\n", "\n")
        todo += reglas_con_clases(css, clases, inicio)
    return todo
