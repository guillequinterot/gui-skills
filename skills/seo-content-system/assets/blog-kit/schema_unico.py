# -*- coding: utf-8 -*-
"""Constructor del schema de un artículo en UN solo bloque JSON-LD con @graph (regla obligatoria de seo-content-system).

Idea: el schema del artículo es un dato DERIVADO de lo que el lector ve. Nunca se escribe a mano ni en bloques sueltos por tipo.
  * FAQPage  <- los H3 que terminan en «?» dentro del H2 de preguntas frecuentes.
  * VideoObject <- el video incrustado (ID de YouTube + datos en meta.json: titulo, descripcion, fecha, duracion ISO 8601).
Cada nodo lleva un @id propio ({url}#faq, {url}#video) y `isPartOf` -> {url}#webpage, que es el WebPage que ya emite el plugin de SEO
(Rank Math, Yoast…). No se duplican Organization, WebSite, WebPage, BreadcrumbList, Person ni Article: los emite el plugin.

Uso:
    from schema_unico import unificar_schema
    cuerpo = unificar_schema(cuerpo, "https://ejemplo.com/mi-articulo/", meta.get("video"))   # idempotente: llamar en cada publicación

Ajustes por proyecto: TITULO_FAQ (el texto del H2), IDIOMA y, si el sitio no tiene plugin de SEO que emita schema, añadir a
`schema_unico()` los nodos Organization, WebSite, WebPage, BreadcrumbList, Person y Article dentro del mismo @graph.
Para que la PÁGINA FINAL tenga un solo script (el del plugin de SEO + este), usar `wordpress-schema-unico.php` en el mismo kit.
Verificación: `python scripts/check_schema_single_block.py <archivo.html> --cuerpo` (fuente) y `... <URL pública>` (página en vivo)."""
import html as ih
import json
import re

TITULO_FAQ = "Preguntas frecuentes"
IDIOMA = "es"
ATRIBUTO = 'data-schema="unico"'
RE_SCHEMA = re.compile(r'<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>.*?</script>', re.S | re.I)


def _texto(fragmento: str) -> str:
    return ih.unescape(re.sub(r"<[^>]+>", "", fragmento)).strip()


def nodo_faq(cuerpo: str, url: str):
    m0 = re.search(rf"<h2[^>]*>\s*{re.escape(TITULO_FAQ)}\s*</h2>", cuerpo)
    if not m0:
        return None
    fin = cuerpo.find("<h2", m0.end())
    seccion = cuerpo[m0.start(): fin if fin > 0 else len(cuerpo)]
    preguntas = [
        {"@type": "Question", "name": _texto(q), "acceptedAnswer": {"@type": "Answer", "text": _texto(a)}}
        for q, a in re.findall(r"<h3[^>]*>(.*?)</h3>\s*(<p>.*?</p>)", seccion, flags=re.S)
    ]
    if not preguntas:
        return None
    return {"@type": "FAQPage", "@id": f"{url}#faq", "isPartOf": {"@id": f"{url}#webpage"}, "inLanguage": IDIOMA, "mainEntity": preguntas}


def nodo_video(v: dict, url: str):
    vid = v["id"]
    return {"@type": "VideoObject", "@id": f"{url}#video", "isPartOf": {"@id": f"{url}#webpage"}, "name": v["titulo"],
            "description": v["descripcion"], "thumbnailUrl": [f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg"], "uploadDate": v["fecha"],
            "duration": v["duracion"], "embedUrl": f"https://www.youtube-nocookie.com/embed/{vid}",
            "contentUrl": f"https://www.youtube.com/watch?v={vid}", "inLanguage": IDIOMA}


def schema_unico(cuerpo: str, url: str, video: dict | None = None) -> str:
    nodos = [n for n in (nodo_faq(cuerpo, url), nodo_video(video, url) if video and video.get("id") else None) if n]
    if not nodos:
        return ""
    return f'<script type="application/ld+json" {ATRIBUTO}>' + json.dumps({"@context": "https://schema.org", "@graph": nodos}, ensure_ascii=False) + "</script>"


def quitar_schema(cuerpo: str) -> str:
    return RE_SCHEMA.sub("", cuerpo).rstrip() + "\n"


def unificar_schema(cuerpo: str, url: str, video: dict | None = None) -> str:
    """Quita todo bloque JSON-LD del cuerpo y deja exactamente uno (o ninguno si no hay FAQ ni video)."""
    return quitar_schema(cuerpo) + schema_unico(cuerpo, url, video)
