---
name: design-logo-vector
description: Skill propia y OBLIGATORIA para crear, rediseñar, criticar y entregar logos y marcas, y para vectorizar un logo raster (PNG/JPG/captura) a SVG limpio, suave y editable. Es sub-skill de direct-visual-design, que la llama cuando el entregable es un logo, un isotipo, un wordmark, un ícono de app/favicon o un vectorizado; si el usuario pide un logo o vectorizar algo, o la nombra, esta skill manda y su proceso no se salta. Cubre brief y mapa de palabras, conceptos en SVG construidos con geometría, vectorizado con escalera de complejidad (primitivas antes que trazo automático), superposición e IoU solo como diagnóstico, auditoría de curvas, pruebas (16 px, una tinta, invertido, estantería de competidores), checkpoint de conceptos antes del kit, variantes, favicon/ícono de app, guía de uso y entrega. Usar ante logo, logotipo, isotipo, wordmark, monograma, símbolo, ícono, favicon, vectorizar, trazar, convertir a SVG, redibujar un logo, rediseño o refresh de marca.
---

# Design Logo Vector — sub-skill propia de `direct-visual-design`

## Protocolo gui-skills (obligatorio)

Esta skill vive en el repo **gui-skills** y sigue [`shared/protocolo-skill.md`](../../shared/protocolo-skill.md):

1. **Paso 0 — cada vez que uses la skill:** corre `python <repo>/tools/check_update.py --quiet --pull`.
   `ACTUALIZADA n` → díselo al usuario en una línea y **vuelve a leer este `SKILL.md`** antes de seguir;
   `CAMBIOS_LOCALES` → avisa y no actualices; `SIN_RED` / `SIN_CREDENCIAL` → sigue con la copia local y dilo.
   Si avisa de aportes sin publicar, corre `python <repo>/tools/publish_job.py --reintentar` (preaprobado).
   Luego lee `HANDSHAKE.md` y el "Registro de trabajos" de `HANDOFF.md`.
2. **Privacidad:** en el repo los clientes solo se nombran con un código `caso-<tipo>-<NN>`; nunca
   nombres, marcas, dominios, correos, rutas personales ni credenciales. Los logos de clientes (originales,
   vectorizados, tableros) viven en la carpeta del proyecto del usuario, **no** en el repo.
3. **Paso final — obligatorio y preaprobado** (trabajo terminado y aprobado por el usuario; no pidas permiso):
   (1) `python <repo>/tools/log_job.py --skill design-logo-vector ...` por cada skill que intervino (qué se hizo, qué
   salió bien, qué salió mal, incidencias); (2) actualiza `HANDSHAKE.md` si cambió el estado vivo;
   (3) publica con `python <repo>/tools/publish_job.py --tema <caso-o-tema>` (rama + push + PR; si eres el
   mantenedor, tu aporte se integra solo); (4) dile al usuario el resultado (`PR_CREADO <url>` / `PUBLICADO <url>` /
   `PENDIENTE` / `BLOQUEADO`). Obsidian es opcional: si el usuario lo tiene, registra también allí.

`<repo>` = `repo_path` de `~/.gui-skills/config.json`, o dos carpetas arriba de esta skill.

**Estatus (decisión del usuario, 2026-10-31):** `direct-visual-design` sigue siendo la skill principal y orquestadora; esta es su **sub-skill propia para todo lo que sea un logo o un vectorizado**. `direct-visual-design` clasifica, fija la dirección de marca y hace el QA de diseño; **`design-logo-vector` decide cómo se concibe, se dibuja en SVG, se vectoriza, se prueba y se entrega la marca.** Si se invoca sola, aplica igualmente los principios de la principal (clasificar; referencias: mantener/adaptar/evitar; QA estratégico→técnico). Precedencia: instrucción actual > brief del proyecto > memoria aprobada > heurísticas de esta skill.

Un logo es un **identificador, no una explicación**: una marca simple, distintiva y pertinente que funciona a 16 px y en un edificio, a una tinta, durante años. El trabajo es encontrar **una** idea clara, construirla con oficio, probar que funciona y presentarla para que se juzgue con los criterios correctos.

## Elegir el modo

| El usuario quiere… | Modo | Empieza por |
|---|---|---|
| Un logo nuevo (desde un brief) | **crear** | `references/02-crear-logo.md` |
| Convertir un logo raster en vector (PNG/JPG/captura/foto de un logo) | **vectorizar** | `references/03-vectorizar-raster.md` |
| Opinión sobre un logo, o modernizarlo / hacer un refresh | **criticar / rediseñar** | `references/04-pruebas-y-qa.md` §4 y `references/02-crear-logo.md` §8 |
| Variantes, favicon, ícono de app, tablero, guía de uso | **entregar** | `references/05-entrega-y-kit.md` |
| Animar un logo ya vectorizado | **animar** (entrega a otra skill) | `references/06-animar-y-rutas.md` §1 |

Un encargo mezcla modos con frecuencia (p. ej. "rediséñalo y dame el SVG"): encadénalos en este orden → criticar → crear → vectorizar/dibujar → probar → entregar.

## Antes de tocar nada (preflight)

1. `python -I <skill>/scripts/handshake.py` → Python, Pillow/numpy, navegador headless (Chrome/Edge). En Windows usa `python`, no `python3`.
2. **Derechos:** ¿el logo que vas a vectorizar es del usuario o de su cliente? Se vectoriza el logo **propio** (o con autorización del titular). No se calca, redibuja ni "inspira de cerca" la marca de un tercero para reutilizarla. Dilo si dudas.
3. Carpeta del proyecto: todo el material (original, SVG, renders, verificación, entregables) va en la carpeta del proyecto del usuario, no en el repo ni en `/tmp`. Guarda cada iteración con versión (`concepto-a-v1.svg`, `-v2.svg`), no sobrescribas.
4. Si hay Obsidian, ubica la nota madre del proyecto (ver `direct-visual-design`). Memoria de marca: `proyectos/INDICE.md` de `direct-visual-design`.

## Flujo por modo (resumen; el detalle está en las referencias)

### Crear
Descubrimiento → **brief** → investigar la categoría y sus clichés → **mapa de palabras** → 8–12 conceptos de una frase → elegir y construir **3** en SVG (negro sobre blanco, sin color todavía) → **probar y refinar al menos dos vueltas** → **CHECKPOINT: mostrar los conceptos, recomendar y parar** → solo si el usuario elige y dice sí: kit completo.

El checkpoint no se salta salvo que el usuario diga expresamente "no preguntes, entrégalo todo". El kit es la mayor parte del trabajo y solo tiene sentido sobre una idea aprobada.

### Vectorizar
Medir el original → elegir el **nivel más bajo de la escalera de complejidad** que explique la marca (1 primitivas · 2 compuestos · 3 pocas curvas · 4 contorno suavizado · 5 trazo automático solo como medida) → SVG con ids semánticos por parte → superponer sobre el original → iterar (**una** cosa por iteración, **máximo 10**) → verificar → entregar con las diferencias dichas con honestidad.

**La suavidad y la estructura mandan sobre el IoU.** Un SVG con IoU de 0,99 pero bordes en escalera o decenas de nodos de un trazador automático **falla**. El IoU se reporta siempre, pero no es una compuerta con umbral fijo.

### Criticar / rediseñar
Diagnosticar primero (¿qué identifica, qué estorba, qué se debe conservar?). Un refresh conserva el reconocimiento; un rebrand lo reemplaza: decide cuál es y dilo. No modificar archivos si solo se pidió análisis.

### Entregar
Variantes (negro, blanco, una tinta de marca, cuadrada, favicon, ícono de app), PNG a los tamaños pedidos, set de web (`favicon.ico`, manifest, snippet `<head>`), guía de uso de una página y, si se pide, tablero de presentación con mockups del sector. Para `.ai`/EPS/PDF editable → **`design-illustrator`**.

## Herramientas (todas con Python y Chrome headless; sin servicios de pago)

| Script | Para qué |
|---|---|
| `scripts/handshake.py` | Verifica entorno local (Python, Pillow, numpy, Chrome). Corre al empezar. |
| `scripts/verificar_vectorizado.py` | **Reporte con semáforo** de un SVG: IoU/superposición contra el original, uniones de curvas, principios de logo. `python -I verificar_vectorizado.py logo.svg --source original.png --out-dir verificacion` |
| `scripts/vendor/pixel2svg-html/` | Medida y trazo inicial (`raster_logo_trace.py`), superposición e IoU (`render_overlay.py`), auditoría Bézier (`svg_path_audit.py`), cintas de ancho variable (`fit_ribbon_centerline.py`), tira de progreso, HTML con JS (`svg_to_js_html.py`) |
| `scripts/vendor/logo-design-skill/` | `svg_audit.py` (auditoría de logo), `concept_sheet.py` (hoja de conceptos del checkpoint), `preview_sheet.py` (hoja de pruebas), `presentation_board.py` (tablero), `render_png.py`, `export_variants.py` (variantes + favicon/ícono) |

Los scripts de `vendor/` son de terceros (MIT), sin modificar y con su licencia al lado; el origen y el commit están en `scripts/vendor/UPSTREAM.md` y los créditos en `CREDITOS.md`. En Windows, si un script de `vendor/` no encuentra el navegador, exporta `CHROME_BIN` (lo imprime `handshake.py`). **Mira siempre tu trabajo**: renderiza el SVG a PNG y ábrelo; dibujar SVG sin verlo es dibujar a ciegas.

## Enrutamiento: qué otra skill entra y cuándo

| Necesidad | Skill |
|---|---|
| Dirección de marca, estrategia, QA de diseño general | `direct-visual-design` (principal) y su `references/branding-and-logos.md` |
| Llevar el logo a `.ai`, EPS, PDF editable | `design-illustrator` (obligatoria; este SVG es su insumo) |
| Montar el logo en Canva | `canva-design` (obligatoria) |
| Subir símbolos a Figma / librería | `figma:figma-use` (obligatoria antes de `use_figma`) |
| Conceptos generados con IA como imagen (para luego vectorizar) | `freepik-imagegen` (revisar créditos antes) o `ckm:design`; el resultado entra aquí como **raster que se vectoriza o se redibuja**, no se entrega tal cual |
| Tokens de color / tipografía del sistema de marca | `design-system-ia` |
| Entender cómo está hecha una referencia (no copiarla) | `rea-reverse-engineer` (por porción) |
| Logo animado / intro / reveal | `video-editing-ai-agent` (HyperFrames) — ver `references/06` |

## Reglas que no se rompen

1. **Una idea, explicable en una frase.** Si necesita un párrafo, no se lee de un vistazo.
2. **Negro primero, color después.** El color provoca debates de gusto antes de que la forma esté resuelta.
3. **Construir, no trazar.** Primitivas, arcos y pocas curvas con ángulos limpios (0/15/30/45/60/90°). El trazo automático es una **medida**, nunca el arte final.
4. **Sin `<text>` vivo, sin rasters incrustados, sin filtros ni máscaras** en un SVG final. Las letras de un logotipo van como contornos (o se declara que se asumió una fuente y que falta convertirla). Excepción de exploración: marcar el `<text>` como provisional.
5. **Probar antes de mostrar:** 16 px, una tinta, invertido, silueta/entrecerrar los ojos, espejo y giro de 180°, estantería de competidores. Lo que no se probó se declara "no verificado".
6. **Texto del cliente literal** (nombre, escritura exacta). Las incoherencias se señalan, no se corrigen en silencio.
7. **Licencias:** la fuente usada debe permitir uso en logo; una búsqueda preliminar de semejanza no sustituye una revisión marcaria profesional. Dilo.
8. **No inventar capacidades:** no prometer pixel a pixel con generación probabilística, ni que "quedó vectorizado" sin haber superpuesto y mirado el resultado.
9. **No convertir una corrección puntual en regla global.** Aprendizajes: `memoria/inbox-aprendizajes.md` → `memoria/preferencias-logo-aprobadas.md` solo tras aprobación o repetición.

## Señales de alarma (arreglar antes de mostrar)

- Literalidad de clip-art (un diente para un dentista) o cliché de categoría sin giro propio.
- Iniciales en una fuente de serie sin modificar; sans geométrica en peso por defecto sin nada propio.
- Más de tres colores sin razón conceptual; degradados o sombras para rescatar una forma débil.
- Detalles menores a ~1/48 de la marca, líneas de pelo, huecos que se cierran al reducir.
- Ángulos casi limpios (13,4° en vez de 15°), curvas con nodos de más, grosores inconsistentes.
- En un vectorizado: bordes en escalera al ampliar, cientos de nodos, centro/escala/hueco distintos al original.
- Se parece a un logo existente. Si se siente familiar y no es tuyo, es de otro.

## Referencias (leer solo la que toca)

| Archivo | Cuándo |
|---|---|
| `references/01-contrato-y-alcance.md` | Contrato de entrada/salida, qué entrega cada modo, qué NO hace esta skill |
| `references/02-crear-logo.md` | Brief, mapa de palabras, tipos de marca, conceptos, construcción en SVG, checkpoint, rediseño |
| `references/03-vectorizar-raster.md` | Escalera de complejidad, ajuste, compuertas, cintas, wordmarks, comandos |
| `references/04-pruebas-y-qa.md` | Pruebas, optical corrections, criterios de aceptación, crítica con tarjeta de puntaje |
| `references/05-entrega-y-kit.md` | Variantes, tamaños mínimos, favicon/ícono, guía de uso, tablero, entrega |
| `references/06-animar-y-rutas.md` | Logo animado (traspaso), rutas con IA, Illustrator/Canva/Figma |
| `templates/` | `guia-de-uso-logo.md` (guía de una página), `presentation-spec.example.json` (tablero), `brief-logo.md` |
| `CREDITOS.md` | Fuentes y licencias de las ideas y los scripts incorporados |
