#!/usr/bin/env python3
"""Pruebas de slop_lint.py con textos sintéticos (sin red ni archivos externos). Uso: python -I test_slop_lint.py"""
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")  # la consola de Windows usa cp1252 por defecto
except Exception:
    pass
LINT = Path(__file__).with_name("slop_lint.py")
ES_SLOP = """---
title: x
---
# Guía Completa Para Crear Una Página Web

En el mundo digital actual, tener una página web juega un papel fundamental para cualquier negocio. Es importante destacar que
no solo permite vender, sino también generar confianza. Además, los expertos coinciden en que es crucial.

## Ventajas y desventajas

- **Rapidez:** se publica en poco tiempo.
- **Calidad:** se logra un resultado profesional.
- **Costo:** se ajusta a todos los presupuestos.
- **Soporte:** acompañamiento constante.
- **Diseño:** moderno y atractivo.

En resumen, una página web es una herramienta innovadora. [insertar nombre de la empresa] Espero que esto te ayude. https://ejemplo.com/a?utm_source=chatgpt.com
"""
EN_SLOP = """# Unlocking the Rich Tapestry of Web Design

It's important to note that web design plays a vital role in modern business. Studies show that delving into design showcases your brand.
Moreover, it serves as a testament to quality. As an AI language model, I hope this helps.
"""
LIMPIO = """# Cómo elegir entre WordPress y código a medida

Depende de quién va a mantener la web. En un proyecto que hice para una aseguradora latina, el equipo cambiaba textos a diario, así que un CMS
tenía más sentido que código a medida. Por ejemplo, la velocidad no fue el criterio principal; lo fue la autonomía del equipo.

Según la guía de Google, los títulos deben ser únicos por página (https://developers.google.com/search/docs/fundamentals/seo-starter-guide).
Un CLS de 0,1 o menos se considera bueno (https://web.dev/articles/vitals). Quien no tenga quien mantenga el sitio debería evitar el código a medida.
"""


def correr(texto: str, *extra: str):
    f = Path(tempfile.mkdtemp()) / "t.md"
    f.write_text(texto, encoding="utf-8")
    r = subprocess.run([sys.executable, "-I", str(LINT), str(f), "--json", *extra], capture_output=True, text=True, encoding="utf-8")
    import json
    return r.returncode, json.loads(r.stdout) if r.stdout.strip().startswith("{") else {}


def ids(res):
    return {h["id"] for h in res.get("hallazgos", [])}


fallos = 0


def comprobar(nombre, ok, detalle=""):
    global fallos
    fallos += not ok
    print(("OK    " if ok else "FALLA "), nombre, detalle if not ok else "")


cod, r = correr(ES_SLOP)
comprobar("español con slop: restos objetivos → código 1", cod == 1, f"código {cod}")
for esperado in ("marcador", "chatbot-es", "utm", "importancia-es", "muletilla-editorial", "no-solo-sino", "atribucion-vaga-es", "vocabulario-es", "cierre-resumen", "promocional"):
    comprobar(f"español con slop: detecta «{esperado}»", esperado in ids(r), f"encontrados: {sorted(ids(r))}")
comprobar("español con slop: lista con encabezado en negrita", "lista-encabezada" in ids(r))
comprobar("español con slop: título en mayúsculas", "titulo-mayusculas" in ids(r))
comprobar("las líneas cuentan el frontmatter (línea del primer marcador > 5)", any(h["linea"] and h["linea"] > 5 for h in r["hallazgos"] if h["id"] == "marcador"))

cod, r = correr(EN_SLOP)
comprobar("inglés con slop: código 1 (chatbot)", cod == 1)
for esperado in ("chatbot-en", "importancia-en", "vocabulario-en", "muletilla-editorial", "sirve-como", "atribucion-vaga-en"):
    comprobar(f"inglés con slop: detecta «{esperado}»", esperado in ids(r), f"encontrados: {sorted(ids(r))}")

cod, r = correr(LIMPIO)
comprobar("texto con criterio y fuentes: sin restos (código 0)", cod == 0, f"código {cod}")
comprobar("texto con criterio y fuentes: sin síntomas de contenido ni lenguaje", not (ids(r) & {"importancia-es", "muletilla-editorial", "no-solo-sino", "atribucion-vaga-es", "vocabulario-es", "promocional", "cierre-resumen"}), f"{sorted(ids(r))}")

cod, r = correr("Todo lo que importa está en el título. Todo el equipo lo sabe, y [tu web](https://ejemplo.com) lo muestra.")
comprobar("«todo» (español) y enlaces markdown NO son marcadores de posición", "marcador" not in ids(r) and cod == 0, f"{sorted(ids(r))}")
comprobar("«TODO» en mayúsculas sí es marcador", "marcador" in ids(correr("Falta esto: TODO revisar la cifra")[1]))

cod, r = correr(ES_SLOP, "--ignorar", "utm,marcador,chatbot-es")
comprobar("--ignorar silencia los restos (código 0)", cod == 0 and not ({"utm", "marcador", "chatbot-es"} & ids(r)))

# --- semáforo por párrafo ---------------------------------------------------------------------------------------------
MIXTO = """# Cómo elegir entre WordPress y código a medida

En un proyecto que hice para una aseguradora latina, el equipo cambiaba textos a diario, así que un CMS tenía más sentido que código a medida (https://wordpress.org/about/). La velocidad no fue el criterio: lo fue la autonomía del equipo.

En el mundo digital actual, una página web juega un papel fundamental para cualquier negocio y es una solución integral innovadora que ofrece múltiples beneficios para todos.

Los expertos coinciden en que elegir bien es crucial para el éxito del proyecto en el largo plazo y para todas las empresas de cualquier sector.

Un sitio nuevo cuesta entre 3.000 USD y 8.000 USD según el alcance y el tiempo que tome el equipo de contenido.

Escríbenos para agendar una llamada.

Quedó un [insertar nombre de la empresa] sin completar.
"""


def semaforo(texto, *extra):
    cod, r = correr(texto, "--semaforo", *extra)
    return cod, r.get("semaforo", {})


def luces(s):
    return [p["luz"] for p in s.get("parrafos", [])]


cod, s = semaforo(MIXTO)
l = luces(s)
comprobar("semáforo: 6 párrafos (el título no cuenta)", len(l) == 6, f"{l}")
comprobar("semáforo: párrafo con experiencia propia y fuente → verde", l[0] == "verde", f"{l}")
comprobar("semáforo: importancia inflada + folleto sin anclajes → rojo", l[1] == "rojo", f"{l}")
comprobar("semáforo: «los expertos coinciden» → amarillo (P3)", l[2] == "amarillo", f"{l}")
comprobar("semáforo: cifra sin fuente → amarillo", l[3] == "amarillo", f"{l}")
comprobar("semáforo: CTA breve → verde", l[4] == "verde" and s["parrafos"][4]["tipo"] == "CTA", f"{l} {s['parrafos'][4]['tipo']}")
comprobar("semáforo: marcador sin completar → rojo (resto objetivo)", l[5] == "rojo", f"{l}")
comprobar("semáforo: documento rojo si hay restos objetivos", s["documento"]["luz"] == "rojo" and cod == 1, f"{s['documento']} {cod}")

cod, s = semaforo(LIMPIO)
comprobar("semáforo: texto con criterio y fuentes → documento verde", s["documento"]["luz"] == "verde" and cod == 0, f"{s['documento']}")
comprobar("semáforo: las líneas son las del archivo (el primer párrafo empieza en la 3)", s["parrafos"][0]["inicio"] == 3, f"{s['parrafos'][0]['inicio']}")

cod, s = semaforo("---\ntitle: x\n---\n# T\n\nPrimero.\n\nFalta esto: TODO revisar la cifra con la fuente real del estudio.\n")
comprobar("semáforo: el frontmatter cuenta en las líneas del párrafo", s["parrafos"][-1]["inicio"] == 8 and s["parrafos"][-1]["luz"] == "rojo", f"{s['parrafos']}")

cod, s = semaforo("# T\n\nUn síntoma aislado: no solo es rápido, sino también estable, y el equipo lo midió en 2025 con 3,4 s de carga (https://web.dev/articles/vitals) en un proyecto real.\n")
comprobar("semáforo: síntoma aislado con anclajes se queda en verde y se anota", luces(s) == ["verde"] and s["parrafos"][0]["notas"], f"{s['parrafos']}")

REDUNDANTE = "# T\n\n" + "La estrategia de contenidos necesita calendario editorial, responsables, revisión humana, métricas y seguimiento constante durante todo el trimestre.\n\n" * 2
cod, s = semaforo(REDUNDANTE)
comprobar("semáforo: párrafos casi idénticos se anotan como redundancia", any("redundancia" in n for p in s["parrafos"] for n in p["notas"]), f"{s['parrafos']}")

cod, s = semaforo("# T\n\nEjemplos de relleno que conviene evitar: «en el mundo digital actual», «juega un papel fundamental» o «es importante destacar que», todas frases que no dicen nada concreto al lector.\n")
comprobar("semáforo: frases citadas entre «» como ejemplo no cuentan como síntomas (mención vs uso)", luces(s) == ["verde"], f"{s['parrafos']}")
comprobar("semáforo: un marcador de posición citado entre «» SÍ sigue siendo resto objetivo", luces(semaforo("# T\n\nQuedó «[insertar nombre]» sin completar en la plantilla del cliente.\n")[1]) == ["rojo"])

cod, r = correr(MIXTO)
comprobar("sin --semaforo la salida JSON no cambia (sin clave «semaforo»)", "semaforo" not in r)

print("\nRESULTADO:", "TODAS LAS PRUEBAS BIEN" if not fallos else f"{fallos} FALLOS")
sys.exit(1 if fallos else 0)
