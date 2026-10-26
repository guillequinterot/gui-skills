#!/usr/bin/env python3
"""slop_lint: detector de SÍNTOMAS de contenido hecho con IA sin criterio. Es una AYUDA, no un juez.

Qué hace: busca (1) restos objetivos (marcadores de posición, frases de chatbot, enlaces con utm_*), (2) síntomas de
contenido, lenguaje y formato descritos en fuentes (nivel «fuente») y (3) observaciones sin fuente, sobre todo en español
(nivel «candidato»). Ningún síntoma prueba que un texto sea de IA ni que sea malo: sirve para encontrar qué falta debajo
(sustancia, fuente, revisión). NO calcula «porcentaje de IA» y NO sugiere sinónimos.

Con --semaforo da además una luz PROVISIONAL (rojo/amarillo/verde) por párrafo, con su evidencia, según los criterios de
references/06-semaforo-por-parrafo.md. El detector ve pistas (restos, síntomas, anclajes concretos), no novedad ni verdad:
quien revisa decide el color final leyendo cada párrafo con las cinco preguntas.

Uso:
    python -I slop_lint.py <archivo.md|.txt|.html> [--idioma es|en|auto] [--json] [--ignorar id1,id2] [--semaforo]
Salida: 0 sin restos objetivos; 1 si hay restos objetivos (fallo de proceso); 2 error de uso.
Sin dependencias (solo la biblioteca estándar).
"""
from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from pathlib import Path

# (id, familia, nivel, idioma, patrón, mensaje corto, arreglo)
O, F, C = "objetivo", "fuente", "candidato"
REGLAS: list[tuple[str, str, str, str, str, str, str]] = [
    # --- restos objetivos -------------------------------------------------------------------------------------
    ("marcador", "restos", O, "both", r"\[(insert|insertar|inserta|your|tu|nombre|empresa|company|link|enlace)[^\]\n]{0,40}\](?!\()|(?-i:(?<!\w)TODO(?!\w))|lorem ipsum|\{\{[^}\n]+\}\}|(?-i:(?<!\w)XXX(?!\w))|\[(cita|fuente|source|citation)( requerida| needed)?\](?!\()",
     "marcador de posición sin completar", "Completar o quitar"),
    ("chatbot-es", "restos", O, "es", r"como (un )?modelo de lenguaje|espero que (esto|esta respuesta|te) (te )?(ayude|sirva)|(claro|por supuesto)[,!]? (aqu[ií]|a continuaci[oó]n)|aqu[ií] tienes|¿(te gustar[ií]a|quieres) que (te )?(ampl[ií]e|expanda|profundice)",
     "frase dirigida al usuario del chatbot", "Borrar y revisar que no queden más"),
    ("chatbot-en", "restos", O, "en", r"as an ai( language model)?|i hope this helps|certainly[!,] here|here(?:'s| is) (a|an|the) (revised|draft|summary)|let me know if you (need|would like)|great question",
     "frase dirigida al usuario del chatbot", "Borrar y revisar que no queden más"),
    ("utm", "restos", O, "both", r"[?&]utm_[a-z]+=|utm_source=",
     "enlace con parámetros de seguimiento (suele venir de un chatbot)", "Abrir la fuente real y limpiar el enlace"),
    # --- contenido ----------------------------------------------------------------------------------------------
    ("importancia-en", "contenido", F, "en", r"\bplays? an? (vital|crucial|pivotal|key|significant|important) role\b|\bstands? as a testament\b|\bpivotal\b|\bin today'?s (fast-paced|digital|ever-changing)\b",
     "importancia inflada sin hecho concreto", "Sustituir por el hecho: qué pasó, cuándo, qué se midió"),
    ("importancia-es", "contenido", C, "es", r"juega(n)? un papel (fundamental|crucial|clave|vital|esencial|importante)|se erige como|es (un )?testimonio de|(un )?papel (fundamental|crucial) en",
     "importancia inflada sin hecho concreto", "Sustituir por el hecho: qué pasó, cuándo, qué se midió"),
    ("promocional", "contenido", F, "both", r"\b(breathtaking|game-?changer|revolutionary|cutting-edge|state-of-the-art|world-class|innovador(a)?|revolucionari[oa]|de vanguardia|l[ií]der en|soluci[oó]n integral)\b",
     "tono promocional: el adjetivo sustituye a la prueba", "Poner la prueba o quitar la frase"),
    ("atribucion-vaga-es", "contenido", F, "es", r"\b(los |muchos |varios |diversos )?(expertos|estudios|especialistas|investigaciones|analistas)( coinciden| se[ñn]alan| afirman| demuestran| indican| han (demostrado|mostrado))\b|\bseg[uú]n (los )?(expertos|estudios)\b",
     "atribución vaga sin fuente", "Citar el estudio o la persona con enlace, o eliminar"),
    ("atribucion-vaga-en", "contenido", F, "en", r"\b(experts|studies|research|analysts) (say|agree|show|suggest|indicate)\b|\baccording to (experts|studies)\b",
     "atribución vaga sin fuente", "Citar el estudio o la persona con enlace, o eliminar"),
    ("seccion-relleno", "contenido", F, "both", r"^#{1,6}\s*(challenges and future (prospects|outlook)|desaf[ií]os y perspectivas( futuras)?|el futuro de |perspectivas futuras)",
     "sección de relleno de plantilla", "Borrar o sustituir por el siguiente paso útil"),
    ("meta-anuncio", "contenido", C, "es", r"(en esta gu[ií]a|en este art[ií]culo|a continuaci[oó]n) (vamos a|veremos|te (voy a )?mostrar|exploraremos|descubrir[aá]s)",
     "meta-anuncio en vez de entrar al contenido", "Empezar por el dato o el problema"),
    # --- lenguaje -----------------------------------------------------------------------------------------------
    ("vocabulario-en", "lenguaje", F, "en", r"\bdelv(e|es|ed|ing)\b|\bshowcas(e|es|ed|ing)\b|\bintricate\b|\bnotably\b",
     "vocabulario típico de modelos (la lista cambia con cada generación)", "Si la palabra es la exacta, se queda; si es adorno, decir la cosa"),
    ("vocabulario-es", "lenguaje", C, "es", r"\b(sum[eé]rge?te|ad[eé]ntrate|desbloque(a|ar|ando)|tapiz|panorama (digital|actual|competitivo)|en el (mundo|entorno) (actual|digital|moderno)|hoy en d[ií]a|en el vertiginoso|sin duda alguna|navegar por el complejo)\b",
     "vocabulario de moda sin información", "Empezar por el dato o el problema"),
    ("sirve-como", "lenguaje", F, "both", r"\bserves? as\b|\bsirve como\b|\bcuenta con\b",
     "«sirve como / cuenta con» en vez de «es / tiene»", "Usar el verbo simple"),
    ("no-solo-sino", "lenguaje", F, "both", r"\bnot (just|only) [^.\n]{1,80}?,? but (also )?|\bno (solo|sólo) [^.\n]{1,90}?,? sino (tambi[eé]n|adem[aá]s)",
     "contraste «no solo X sino Y» (revisar si se repite sin contraste real)", "Reservarlo para cuando haya un contraste de verdad"),
    ("muletilla-editorial", "lenguaje", F, "both", r"\bit'?s (important|worth) (to note|noting)\b|\bes (importante|fundamental) (destacar|se[ñn]alar|mencionar|resaltar|tener en cuenta)( que)?\b|\bcabe (destacar|se[ñn]alar|mencionar|resaltar)\b",
     "muletilla editorial", "Quitar y decir directamente lo importante"),
    ("cierre-resumen", "lenguaje", F, "both", r"^(in summary|in conclusion|overall|en resumen|en conclusi[oó]n|para concluir|en definitiva)\b[,:]?",
     "cierre que repite lo dicho", "Cerrar con la acción siguiente"),
]
MARCAS_PROPIAS = r"\b(por ejemplo|en mi experiencia|en un proyecto|en un caso|caso real|lo comprob[eé]|lo med[ií]|medimos|en este (mismo )?sitio|en mis proyectos|for example|in my experience|in one project|we measured|i measured)\b"
CIFRA = r"\d[\d.,]*\s?(%|USD|COP|EUR|€|\$)|\$\s?\d"
CTA = r"^\W*(desc[aá]rga|suscr[ií]be|cont[aá]cta|escr[ií]be|reserva|solicita|agenda|compra|pru[eé]ba|reg[ií]strate|download|subscribe|contact|book|sign up|try)"
LUZ = {"rojo": "🔴", "amarillo": "🟡", "verde": "🟢"}
CONECTORES = r"\b(adem[aá]s|asimismo|por otro lado|por otra parte|moreover|furthermore|additionally)\b"
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿]")
FAMILIAS = {"restos": "Restos objetivos", "contenido": "Contenido", "lenguaje": "Lenguaje", "formato": "Formato", "ritmo": "Ritmo y concreción"}


def quitar_frontmatter(texto: str) -> tuple[str, int]:
    m = re.match(r"^---\r?\n.*?\r?\n---\r?\n", texto, re.S)
    if not m:
        return texto, 0
    return texto[m.end():], texto[: m.end()].count("\n")


def detectar_idioma(texto: str) -> str:
    t = texto.lower()
    es = len(re.findall(r"\b(el|la|de|que|y|en|los|las|para|con|una|por)\b", t))
    en = len(re.findall(r"\b(the|and|of|to|in|is|for|with|that|this|are)\b", t))
    return "es" if es >= en else "en"


def analizar(texto: str, idioma: str = "auto", ignorar: set[str] | None = None, con_semaforo: bool = False) -> dict:
    ignorar = ignorar or set()
    cuerpo, desfase = quitar_frontmatter(texto)
    cuerpo = re.sub(r"<!--.*?-->", lambda m: "\n" * m.group(0).count("\n"), cuerpo, flags=re.S)
    idioma = detectar_idioma(cuerpo) if idioma == "auto" else idioma
    palabras = len(re.findall(r"\w+", cuerpo))
    hallazgos: list[dict] = []

    def linea(pos: int) -> int:
        return desfase + cuerpo.count("\n", 0, pos) + 1

    def add(id_, familia, nivel, mensaje, arreglo, linea_=None, ejemplo=""):
        if id_ in ignorar:
            return
        hallazgos.append({"id": id_, "familia": familia, "nivel": nivel, "mensaje": mensaje, "arreglo": arreglo, "linea": linea_, "ejemplo": ejemplo.strip()[:110]})

    # mención vs uso: una frase entre «» o “” se cita como ejemplo, no se usa; los restos objetivos se buscan siempre
    sin_citas = re.sub(r"«[^»\n]{0,240}»|“[^”\n]{0,240}”", lambda m: " " * len(m.group(0)), cuerpo)
    for id_, familia, nivel, lang, patron, mensaje, arreglo in REGLAS:
        if lang not in ("both", idioma):
            continue
        base = cuerpo if nivel == O else sin_citas
        for m in re.finditer(patron, base, re.I | re.M):
            add(id_, familia, nivel, mensaje, arreglo, linea(m.start()), cuerpo[max(0, m.start() - 20): m.end() + 30].replace("\n", " "))

    parrafos = [p.strip() for p in re.split(r"\n\s*\n", cuerpo) if p.strip() and not p.lstrip().startswith(("#", "|", "```", "---"))]
    enlaces_ext = len(re.findall(r"https?://", cuerpo))

    # formato -------------------------------------------------------------------------------------------------
    negritas = len(re.findall(r"\*\*[^*\n]{2,80}\*\*", cuerpo))
    if palabras and negritas / palabras * 1000 > 18:
        add("exceso-negritas", "formato", F, f"{negritas} negritas en {palabras} palabras", "Dejar en negrita solo lo que alguien buscaría al escanear")
    encabezado_en_linea = len(re.findall(r"^\s*[-*]\s+\*\*[^*\n]{2,40}[:.]?\*\*[:.]?\s", cuerpo, re.M))
    if encabezado_en_linea >= 5:
        add("lista-encabezada", "formato", F, f"{encabezado_en_linea} viñetas con encabezado en negrita", "Pasar a prosa o a una lista corta con criterio")
    niveles = [len(m.group(1)) for m in re.finditer(r"^(#{1,6})\s+\S", cuerpo, re.M)]
    for a, b in zip(niveles, niveles[1:]):
        if b - a > 1:
            add("nivel-saltado", "formato", F, f"salto de título H{a} → H{b}", "Respetar la jerarquía de títulos")
            break
    for m in re.finditer(r"^(#{1,6})\s+(.+)$", cuerpo, re.M):
        titulo = m.group(2)
        if EMOJI.search(titulo):
            add("emoji-titulo", "formato", F, "emoji en un título", "Quitar", linea(m.start()), titulo)
        palabras_t = [w for w in re.findall(r"[A-Za-zÁÉÍÓÚÑáéíóúñ]+", titulo)[1:] if len(w) > 3]
        if idioma == "es" and len(palabras_t) >= 3 and sum(w[0].isupper() for w in palabras_t) >= len(palabras_t) - 0 and len(palabras_t) >= 3:
            add("titulo-mayusculas", "formato", C, "título con mayúscula en cada palabra (en español se escribe como oración)", "Capitalizar como oración", linea(m.start()), titulo)

    # ritmo y concreción ------------------------------------------------------------------------------------------
    tern = sum(1 for p in parrafos if re.search(r"\b\w+, \w+(?: \w+)?,? (y|e|and) \w+", p))
    if len(parrafos) >= 8 and tern / len(parrafos) > 0.45:
        add("triadas", "lenguaje", F, f"enumeraciones de tres elementos en {tern} de {len(parrafos)} párrafos", "Decir los elementos que de verdad hay (a veces son dos o cuatro)")
    conect = len(re.findall(CONECTORES, cuerpo, re.I))
    if palabras and conect / palabras * 1000 > 6:
        add("conectores", "lenguaje", C, f"{conect} conectores de ensayo en {palabras} palabras", "Dejar que el orden de las ideas haga el trabajo")
    frases = [len(re.findall(r"\w+", f)) for f in re.split(r"(?<=[.!?])\s+", re.sub(r"[#>*`|_\[\]]", " ", cuerpo)) if len(re.findall(r"\w+", f)) >= 3]
    if len(frases) >= 15 and statistics.mean(frases) and statistics.pstdev(frases) / statistics.mean(frases) < 0.35:
        add("ritmo-uniforme", "ritmo", C, "frases de longitud muy parecida", "Solo importa si además falta sustancia; no se «mezcla» por sistema")
    aperturas = [re.match(r"\W*(\w+)", p).group(1).lower() for p in parrafos if re.match(r"\W*(\w+)", p)]
    racha = 1
    for a, b in zip(aperturas, aperturas[1:]):
        racha = racha + 1 if a == b else 1
        if racha >= 4:
            add("aperturas-repetidas", "ritmo", C, f"4 párrafos seguidos empiezan por «{a}»", "Variar según lo que dice cada párrafo")
            break
    cifras = len(re.findall(CIFRA, cuerpo))
    if cifras >= 3 and enlaces_ext == 0:
        add("cifras-sin-fuente", "contenido", C, f"{cifras} cifras y ningún enlace a fuente", "Fuente abierta con fecha para cada cifra o quitarla")
    marcas_propias = len(re.findall(MARCAS_PROPIAS, cuerpo, re.I))
    anclas = cifras + marcas_propias + len(re.findall(r"\b\d+[.,]\d+\b", cuerpo)) + enlaces_ext
    if palabras >= 600 and anclas / palabras * 1000 < 2.0:
        add("baja-concrecion", "ritmo", C, f"pocos anclajes concretos (cifras, ejemplos, fuentes): {anclas} en {palabras} palabras", "Añadir un ejemplo propio, un dato con fuente o una experiencia real; si no existe, recortar")

    res = {"idioma": idioma, "palabras": palabras, "hallazgos": hallazgos}
    if con_semaforo:
        res["semaforo"] = semaforo(cuerpo, desfase, hallazgos)
    return res


def parrafos_con_linea(cuerpo: str, desfase: int) -> list[dict]:
    """Bloques de líneas seguidas, sin títulos, tablas ni código, con su rango de líneas (contando el frontmatter)."""
    out = []
    en_codigo = False
    for m in re.finditer(r"(?:[^\n]*\S[^\n]*(?:\n|$))+", cuerpo):
        ini = desfase + cuerpo.count("\n", 0, m.start()) + 1
        lineas = m.group(0).rstrip("\n").split("\n")
        tras_titulo = False
        while lineas and re.match(r"\s*#{1,6}\s", lineas[0]):
            lineas.pop(0)
            ini += 1
            tras_titulo = True
        if not lineas or len(re.findall(r"\w+", " ".join(lineas))) < 3:
            continue
        primera = lineas[0].lstrip()
        if primera.startswith("```"):
            en_codigo = not en_codigo
            continue
        if en_codigo or primera.startswith(("|", "---", "<")):
            continue
        out.append({"inicio": ini, "fin": ini + len(lineas) - 1, "texto": "\n".join(lineas).strip(), "tras_titulo": tras_titulo,
                    "lista": all(re.match(r"\s*([-*+]|\d+[.)])\s", x) for x in lineas)})
    return out


def _palabras_contenido(t: str) -> set[str]:
    return {w for w in re.findall(r"[a-záéíóúñü]{5,}", t.lower())}


def semaforo(cuerpo: str, desfase: int, hallazgos: list[dict]) -> dict:
    """Luz PROVISIONAL por párrafo. Criterios en references/06-semaforo-por-parrafo.md; el color final lo decide quien revisa."""
    ps = parrafos_con_linea(cuerpo, desfase)
    usados: set[int] = set()
    for i, p in enumerate(ps):
        t = p["texto"]
        p["indice"] = i + 1
        p["palabras"] = len(re.findall(r"\w+", t))
        propios = [h for h in hallazgos if h["linea"] and p["inicio"] <= h["linea"] <= p["fin"]]
        usados.update(id(h) for h in propios)
        objetivos = [h for h in propios if h["nivel"] == O]
        sintomas = {h["id"]: h for h in propios if h["nivel"] != O and h["familia"] in ("contenido", "lenguaje")}
        cifras = len(re.findall(CIFRA, t))
        urls = len(re.findall(r"https?://", t))
        fuertes = cifras + urls + len(re.findall(MARCAS_PROPIAS, t, re.I)) + len(re.findall(r"\b\d+[.,]\d+\b|\b(?:19|20)\d{2}\b", t))
        nombres = 0
        for fr in re.split(r"(?<=[.!?])\s+", t):
            nombres += len([w for w in re.findall(r"\b[A-ZÁÉÍÓÚÑ][a-záéíóúñ]{2,}\b", fr)[1:]])
        if p["lista"]:
            tipo = "lista"
        elif re.search(CTA, t, re.I) and p["palabras"] <= 40:
            tipo = "CTA"
        elif p["palabras"] <= 25 and not p["tras_titulo"]:
            tipo = "transición"
        elif p["tras_titulo"]:
            tipo = "apertura"
        elif cifras:
            tipo = "dato"
        elif re.search(MARCAS_PROPIAS, t, re.I):
            tipo = "ejemplo"
        else:
            tipo = "sin clasificar"
        if i == 0:
            tipo = "apertura" if tipo in ("sin clasificar", "dato", "ejemplo") else tipo
        motivos: list[str] = []
        faltas: list[str] = []
        notas: list[str] = []
        if objetivos:
            luz = "rojo"
            motivos += [f"resto objetivo: {h['mensaje']} → «{h['ejemplo']}»" for h in objetivos[:3]]
            faltas.append("completar o quitar el resto objetivo")
        elif len(sintomas) >= 2 and fuertes == 0 and p["palabras"] >= 20:
            luz = "rojo"
            motivos.append("posible P1+P2 (ni nuevo ni propio): " + "; ".join(h["mensaje"] for h in sintomas.values()) + " y ningún anclaje concreto")
            faltas.append("un dato con fuente, un ejemplo propio o una posición; si no existe, borrar el párrafo")
        elif any(k.startswith("atribucion-vaga") for k in sintomas):
            luz = "amarillo"
            motivos.append("P3: atribución vaga sin fuente")
            faltas.append("citar el estudio o la persona con enlace, o quitar la afirmación")
        elif cifras and urls == 0 and not (re.search(r"\b(source|fuente|datos de)\b", t, re.I) or re.search(r"\b(seg[uú]n|according to)\s+(?:(?:el|la|los|las)\s+)?(?:(?i:informe|estudio|gu[ií]a|documentaci[oó]n)|(?-i:[A-ZÁÉÍÓÚÑ]))", t, re.I)):
            luz = "amarillo"
            motivos.append(f"P3: {cifras} cifra(s) sin fuente cercana")
            faltas.append("fuente abierta con fecha para cada cifra, o quitarla")
        elif sintomas and fuertes == 0:
            luz = "amarillo"
            motivos.append("síntoma sin sustancia que lo sostenga: " + "; ".join(h["mensaje"] for h in sintomas.values()))
            faltas.append("; ".join(sorted({h["arreglo"] for h in sintomas.values()})))
        elif p["palabras"] >= 60 and fuertes == 0 and nombres < 2 and tipo not in ("transición", "CTA"):
            luz = "amarillo"
            motivos.append("pista P1/P2: sin cifra, ejemplo, fuente ni nombre propio en ≥ 60 palabras")
            faltas.append("comprobar con las cinco preguntas; añadir un dato, ejemplo o experiencia propia, o recortar")
        else:
            luz = "verde"
        if sintomas and luz == "verde":
            notas.append("síntoma aislado con anclajes (no cambia la luz): " + "; ".join(h["mensaje"] for h in sintomas.values()))
        if p["palabras"] > 120:
            notas.append("pista de legibilidad: más de 120 palabras")
        p.update({"tipo": tipo, "luz": luz, "motivos": motivos, "falta": faltas, "notas": notas, "anclajes": fuertes})
    for i, a in enumerate(ps):
        ca = _palabras_contenido(a["texto"])
        for j in range(i + 1, len(ps)):
            cb = _palabras_contenido(ps[j]["texto"])
            if len(ca) >= 8 and len(cb) >= 8 and len(ca & cb) / len(ca | cb) >= 0.55:
                a["notas"].append(f"posible redundancia con ¶{ps[j]['indice']}")
                ps[j]["notas"].append(f"posible redundancia con ¶{a['indice']}")
    n = len(ps)
    rojos = sum(p["luz"] == "rojo" for p in ps)
    amarillos = sum(p["luz"] == "amarillo" for p in ps)
    con_resto = any(h["nivel"] == O for h in hallazgos)
    if n == 0:
        luz_doc, decision = "amarillo", "Sin párrafos que evaluar."
    elif con_resto or rojos / n >= 1 / 3:
        luz_doc, decision = "rojo", "Rehacer o descartar"
    elif rojos or amarillos / n > 0.25:
        luz_doc, decision = "amarillo", "Reescribir los párrafos marcados y volver a pasar solo esos"
    else:
        luz_doc, decision = "verde", "Publicar si pasan propósito, procedencia y promesa (se evalúan a mano)"
    de_pieza = [h for h in hallazgos if id(h) not in usados]
    return {"documento": {"luz": luz_doc, "decision": decision, "parrafos": n, "rojos": rojos, "amarillos": amarillos, "verdes": n - rojos - amarillos},
            "parrafos": [{k: p[k] for k in ("indice", "inicio", "fin", "palabras", "tipo", "luz", "motivos", "falta", "notas", "anclajes")} | {"extracto": re.sub(r"\s+", " ", p["texto"])[:80]} for p in ps],
            "de_la_pieza": de_pieza}


def _rangos(nums: list[int]) -> str:
    out, i = [], 0
    while i < len(nums):
        j = i
        while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1:
            j += 1
        out.append(f"¶{nums[i]}" if i == j else f"¶{nums[i]}-¶{nums[j]}")
        i = j + 1
    return ", ".join(out)


def informe_semaforo(res: dict) -> str:
    s = res["semaforo"]
    d = s["documento"]
    L = [f"slop_lint --semaforo · {res['palabras']} palabras · idioma {res['idioma']}  (luces PROVISIONALES: decide quien revisa)", "",
         f"DOCUMENTO: {LUZ[d['luz']]} {d['luz'].upper()} — {d['decision']}",
         f"  {d['parrafos']} párrafos: {d['rojos']} rojos, {d['amarillos']} amarillos, {d['verdes']} verdes", ""]
    for p in s["parrafos"]:
        if p["luz"] == "verde":
            continue
        L.append(f"¶{p['indice']}  líneas {p['inicio']}-{p['fin']}  {p['tipo']}?  {LUZ[p['luz']]} {p['luz'].upper()}  ({p['palabras']} palabras)")
        L.append(f"    «{p['extracto']}…»")
        L += [f"    · {m}" for m in p["motivos"]]
        L += [f"    falta: {f}" for f in p["falta"]]
        L += [f"    nota: {n}" for n in p["notas"]]
        L.append("")
    verdes = [p for p in s["parrafos"] if p["luz"] == "verde"]
    if verdes:
        L.append("VERDES: " + _rangos([p["indice"] for p in verdes]) + "  → léelos igual con las cinco preguntas (novedad, especificidad, respaldo, lo propio, función)")
        for p in verdes:
            for n in p["notas"]:
                L.append(f"    ¶{p['indice']} nota: {n}")
        L.append("")
    if s["de_la_pieza"]:
        L.append("DE LA PIEZA ENTERA (no de un párrafo):")
        porid: dict[str, list[dict]] = {}
        for x in s["de_la_pieza"]:
            porid.setdefault(x["id"], []).append(x)
        for xs in porid.values():
            L.append(f"  [{xs[0]['nivel']}] {xs[0]['mensaje']} ×{len(xs)}  → {xs[0]['arreglo']}")
        L.append("")
    L.append("Se evalúan a mano, no los ve el detector: propósito, procedencia y revisión humana, promesa cumplida, hechos verdaderos.")
    return "\n".join(L)


def informe(res: dict) -> str:
    h = res["hallazgos"]
    obj = [x for x in h if x["nivel"] == O]
    L = [f"slop_lint · {res['palabras']} palabras · idioma {res['idioma']}", ""]
    if obj:
        L.append(f"RESTOS OBJETIVOS ({len(obj)}) — se corrigen siempre")
        for x in obj:
            L.append(f"  línea {x['linea']}: {x['mensaje']} → «{x['ejemplo']}»")
        L.append("")
    for fam in ("contenido", "lenguaje", "formato", "ritmo"):
        grupo = [x for x in h if x["familia"] == fam]
        if not grupo:
            continue
        L.append(f"{FAMILIAS[fam].upper()} ({len(grupo)})")
        porid: dict[str, list[dict]] = {}
        for x in grupo:
            porid.setdefault(x["id"], []).append(x)
        for id_, xs in porid.items():
            x0 = xs[0]
            L.append(f"  [{x0['nivel']}] {x0['mensaje']} ×{len(xs)}  → {x0['arreglo']}")
            for x in xs[:3]:
                if x["linea"]:
                    L.append(f"      línea {x['linea']}: «{x['ejemplo']}»")
        L.append("")
    if not h:
        L.append("Sin hallazgos. Eso NO prueba que la pieza sea buena: falta pasar la puerta (propósito, sustancia, procedencia).")
    L.append("Recuerda: un síntoma no prueba nada. Pregunta qué falta debajo (hecho, fuente, ejemplo propio, posición) y arréglalo ahí.")
    return "\n".join(L)


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description="Detector de síntomas de slop (ayuda, no juez)")
    ap.add_argument("archivo")
    ap.add_argument("--idioma", default="auto", choices=["auto", "es", "en"])
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--ignorar", default="", help="ids a omitir, separados por comas")
    ap.add_argument("--semaforo", action="store_true", help="luz provisional por párrafo (rojo/amarillo/verde) con evidencia")
    a = ap.parse_args()
    p = Path(a.archivo)
    if not p.exists():
        print(f"No existe {p}", file=sys.stderr)
        return 2
    texto = p.read_text(encoding="utf-8", errors="replace")
    if p.suffix.lower() in (".html", ".htm"):
        texto = re.sub(r"<(script|style|nav|header|footer|aside|form|noscript|svg|button)[^>]*>.*?</\1>", " ", texto, flags=re.S | re.I)
        texto = re.sub(r"</(p|div|li|h[1-6]|section|article)>", "\n\n", texto, flags=re.I)
        texto = re.sub(r"<[^>]+>", " ", texto)
    res = analizar(texto, a.idioma, {x for x in a.ignorar.split(",") if x}, a.semaforo)
    print(json.dumps(res, ensure_ascii=False, indent=2) if a.json else (informe_semaforo(res) if a.semaforo else informe(res)))
    return 1 if any(x["nivel"] == O for x in res["hallazgos"]) else 0


if __name__ == "__main__":
    sys.exit(main())
