# HANDOFF — design-logo-vector

> Traspaso entre sesiones y personas: qué es la skill, cómo se instala, qué se decidió y qué se aprendió
> en cada trabajo. Estado vivo (versión, herramientas, pendientes) → `HANDSHAKE.md`. Historial de cambios → `CHANGELOG.md`.

## 1. Qué es y cuándo se usa

Skill **propia** del mantenedor, **sub-skill de `direct-visual-design`** (la principal/orquestadora de diseño), hermana de `canva-design` y `design-illustrator`. Cubre todo lo que sea **un logo o un vectorizado**: crear (brief → conceptos → checkpoint → kit), vectorizar un raster a SVG limpio y suave, criticar/rediseñar, entregar variantes y animar (traspaso). Nace el 2026-10-31 de cinco repos públicos que el mantenedor pidió integrar (ver `CREDITOS.md`): dos skills de diseño de logos, dos de vectorizado/animación de logos y una lista de skills.

**Receta corta:** preflight (`handshake.py`, derechos del logo) → modo → *crear*: brief → conceptos → 3 en SVG negro → pruebas → **checkpoint** → kit | *vectorizar*: medir → escalera de complejidad → ajuste con superposición (≤ 10 iteraciones) → `verificar_vectorizado.py` → entrega con residuos declarados.

## 2. Instalación y dependencias

- Viene con el repo gui-skills (`tools/install.ps1` / `tools/install.sh`); el instalador enlaza `~/.claude/skills/design-logo-vector` al clon. No se copia a mano.
- Python 3.9+ con **Pillow** y **numpy** (obligatorios); Chrome o Edge instalado (render de SVG/HTML, superposición, hojas de prueba). Opcionales no usados por defecto: OpenCV, potrace, vtracer, Inkscape, cairosvg.
- Los scripts de `scripts/vendor/` son de terceros (MIT), **sin modificar**, con su LICENSE; origen y commit en `scripts/vendor/UPSTREAM.md`. Los propios son `scripts/handshake.py` y `scripts/verificar_vectorizado.py`.
- **No incluido a propósito:** la biblioteca de 1.400+ logos de `logo-design-skill` (marcas registradas de terceros), `search_library.py`/`build_catalog.py`, el generador de showcases con la API de Gemini de `logo-generator-skill` (sin licencia declarada; dependía de una clave de API) y los scripts de animación de `pixel2motion`.

| Ruta | Contenido |
|---|---|
| `SKILL.md`, `references/` (6), `templates/` (3) | Núcleo |
| `scripts/handshake.py`, `scripts/verificar_vectorizado.py` | Herramientas propias |
| `scripts/vendor/` | Scripts MIT de terceros + `UPSTREAM.md` |
| `HANDOFF.md`, `HANDSHAKE.md`, `CHANGELOG.md`, `CREDITOS.md` | Estado y atribución |
| `memoria/` | `inbox-aprendizajes.md`, `preferencias-logo-aprobadas.md` |
| `ejemplos/README.md` | Caso sintético de verificación (sin material de clientes) |

## 3. Decisiones vigentes

| Fecha | Decisión | Quién la aprobó | Por qué |
|---|---|---|---|
| 2026-10-31 | Crear `design-logo-vector` como sub-skill de `direct-visual-design` para logos y vectorizado | Guillermo Quintero | Pedido explícito con cinco repos de referencia |
| 2026-10-31 | Reexpresar el método con palabras propias; vendorizar solo scripts MIT sin modificar, con licencia al lado | Claude (propuesta) — a confirmar | Convención del repo: no copiar texto de terceros; los scripts MIT probados evitan reescribir y re-depurar |
| 2026-10-31 | No incluir la biblioteca de logos de terceros ni el generador con API de Gemini | Claude (propuesta) — a confirmar | Marcas registradas ajenas; licencia no declarada y dependencia de clave de API |
| 2026-10-31 | Checkpoint de conceptos obligatorio antes del kit; vía rápida por defecto | Heredado del método de `logo-design-skill` | El kit es la mayor parte del trabajo y solo tiene sentido sobre una idea aprobada |
| 2026-10-31 | Suavidad y estructura mandan sobre el IoU; sin umbral global | Heredado del método de `pixel2svg-html` | Un IoU alto no esconde mala artesanía vectorial |

## 4. Registro de trabajos

> Una entrada por trabajo terminado o implementado y aprobado. Solo se agregan entradas al final; las
> correcciones van como entrada nueva. Casos solo con código `caso-<tipo>-<NN>`. Formato:
> `templates/entrada-de-trabajo.md`. Se escribe con `tools/log_job.py`.

<!-- registro:inicio -->

### 2026-10-31 · banco-pruebas-logo-vector · guille

- **Qué se hizo:** Creación de la sub-skill a partir de 5 repos de referencia: método reexpresado en 6 referencias, 13 scripts MIT vendorizados sin modificar, handshake.py y verificar_vectorizado.py propios; integrada en direct-visual-design y README.
- **Salió bien:** Cadena completa de vectorizado, hoja de conceptos, variantes, set web y tablero verificados en Windows con Chrome headless sobre un logo sintético; el semáforo distingue trazo por píxeles (ROJO) de un SVG dibujado con arcos (VERDE) aunque ambos tengan IoU alto.
- **Salió mal / incidencia:** Sin caso real todavía; fit_ribbon_centerline.py, la ruta con IA y el traspaso de animación sin probar. Incidencia: svg_path_audit.py aproxima los arcos SVG con rectas y da avisos de unión falsos; el envoltorio los omite si el trazado usa arcos. render_overlay.py suelto necesita CHROME_BIN en Windows.
- **Regla candidata:** ninguna
- **Herramientas:** Python 3.12, Pillow, numpy, Chrome headless

<!-- registro:fin -->

## 5. Reglas candidatas (sin aprobar)

| Regla | Visto en (casos) | Estado |
|---|---|---|
| Un SVG de logo con > 40 segmentos rectos y 0 curvas se trata como trazo por píxeles (ROJO en `verificar_vectorizado.py`) | prueba sintética (2026-10-31) | Heurística propia, sin probar en un caso real |
