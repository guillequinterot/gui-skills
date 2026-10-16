# CHANGELOG — canva-design

## 2026-10-16 — Migración al repo gui-skills (anonimizada)

- Fuente del mantenedor y copia instalada reconciliadas: **idénticas** en los 21 archivos del núcleo (`SKILL.md`, `references/`, `scripts/`, `templates/`); la fuente aportaba además `HANDOFF.md`, `HANDSHAKE.md`, `CHANGELOG.md`, `conocimiento/`, `memoria/`, `proyectos/` y `ejemplos/`. La copia instalada solo traía un `__pycache__` (excluido).
- Bloque **Protocolo gui-skills** insertado tras el título de `SKILL.md`; "Integración con Obsidian" pasa a "Memoria, Obsidian y otras skills" (Obsidian opcional).
- `scripts/temp_host.sh` y `scripts/handshake.py` ya no llevan IP, usuario, puerto, dominio ni ruta de llave del mantenedor: leen `CANVA_TMP_*` o las claves `canva_tmp_*` de `~/.gui-skills/config.json` y se niegan a subir sin ellas. `scripts/install.py` detecta que la skill está instalada por enlace al repo y no copia.
- Anonimizado: clientes → códigos (`caso-diplomas-01`, `caso-piezas-universidad-01`); la referencia 07, las fichas de `proyectos/` y las carpetas de `ejemplos/` se renombraron con el código de caso; enlaces e ids de Canva quitados.
- Fuera del repo: `_respaldo/` y todo el material con marca de cliente en `ejemplos/` (HTML, assets, logos, previews, exportaciones, configs y textos por programa). Quedan `ejemplos/caso-diplomas-01/` (README con la especificación de capas, y `bake.py`/`streak.py` anonimizados) y `ejemplos/caso-piezas-universidad-01/` (README, QA, notas del montaje y las herramientas genéricas del motor, renombradas).
- `HANDOFF.md` y `HANDSHAKE.md` reestructurados con la plantilla de gui-skills; el Registro de trabajos se sembró con 4 entradas.


## 2026-10-09 — v1.1.2 (solo ejemplo caso-piezas-universidad-01; el núcleo instalado no cambia)

Origen: Fase 2 del proyecto caso-piezas-universidad-01 (imágenes del diseño 2 de 34 programas con stock de Magnific).

### Añadido en `ejemplos/caso-piezas-universidad-01/herramientas/`
- **Convención de imágenes por diseño en el motor** (`motor_series.py`): `assets/img-c2-fondo.jpg` tiene prioridad; en layouts `split` recorta la foto a la franja visible (`strip_fit`) y descarta la persona heredada; foco opcional por formato con `img-c2-foco.json`.
- `place_c2.py` (nuevo; no incluido en el repo por depender de los módulos por programa): coloca la imagen, regenera con el módulo correcto del programa y renderiza (usa Git Bash, no WSL).
- Opt-in de la convención en los módulos por programa y en el del carrusel (fondo/banda); esos módulos llevan el copy del cliente y no están en el repo.
- Respaldos de la versión anterior: en el PC del mantenedor (no están en el repo).

### Verificado
34 diseños 2 renderizados y mirados (post/historia/banner o carrusel); 100 HTML con lint 0 errores; `qa_copy_check.py` sin diferencias nuevas.

## 2026-10-09 — v1.1.1 (solo ejemplo caso-piezas-universidad-01; el núcleo instalado no cambia)

### Añadido
- `ejemplos/caso-piezas-universidad-01/herramientas/motor_series.py`: opción **`strip_fit`** (opt-in por variante) para layouts `split`: recorta la foto a la franja visible en vez de a la página completa, de modo que `focus` encuadre al sujeto. Un módulo por programa la usa en el diseño 2 de un programa junto con `person=False`. Respaldo previo: en el PC del mantenedor.
- `memoria/inbox-aprendizajes.md`: 2 candidatos (franja `split`; coste de Magnific stock y límites del stock para gente local). Sin promover.
- Verificación al retomar: `install.py --check` = 21 archivos, 0 diferencias; `handshake.py` 15/15.

## 2026-10-09 — v1.1.0 (caso caso-piezas-universidad-01: producción en serie y montaje multipieza)

Origen: proyecto caso-piezas-universidad-01 (36 programas × 2 diseños × 3 formatos). Petición del usuario: actualizar y reinstalar la skill con todas las incidencias y hallazgos («el diseño quedó super genial»).

### Añadido
- `references/08-montaje-multipieza-y-fuentes.md`: estrategia para producir en serie (motor + config por programa), importación de varias páginas de **tamaños mixtos** en un solo HTML, flujo B (marcadores en vez de `<img>` + `update_fill` + `crop_media`), `merge-designs` (una operación por llamada, orden invertido y `move_pages`, `delete_pages`), títulos de página = `data-label`, uso de `copy-design` para probar, lectura barata de títulos, export a tamaño nativo, costes, y el **hallazgo de la fuente de marca** (el importador no aplica la fuente de marca; 15 pruebas) con opciones.
- `scripts/prepare_multipage_import.py` (nuevo, probado con las 3 HTML del programa 1: 6 páginas, 18 marcadores, lint 0 errores).
- `ejemplos/caso-piezas-universidad-01/` (motor de diseño, configs, extractor de imágenes de `.ai`, render, notas del montaje, previews y exportaciones; en el repo solo las herramientas genéricas y las notas) y `proyectos/caso-piezas-universidad-01.md` (ficha: Canva, decisiones).
- Reglas 13–16 en `SKILL.md`; filas A11/A12/B11–B14 y herramientas (`copy-design`, `merge-designs`, `read-design`, `export-design`, `list-brand-kits`) en `references/02`; sección «Variante multipieza» en `01`; sección C2 en `06`; sección «Bug corregido» en `03`.

### Decisión tipográfica (usuario, misma fecha)
El cambio de fuente en Canva es **en bloque** (Canva reconoce la fuente de reemplazo y la sustituye en todo el diseño). Regla: una sola familia y pocos estilos (Regular/Bold/Italic); máx. 2 familias con estilos equivalentes si la marca lo exige. Reflejado en `SKILL.md` regla 13, `references/08` §4 y `proyectos/caso-piezas-universidad-01.md`.

### Corregido
- `scripts/temp_host.sh upload` con **varios archivos** subía una carpeta vacía (`"$@"` llegaba a `tar` como un solo argumento). Ahora cada archivo es un argumento propio (admite espacios). Probado con `--dry-run` y sintaxis; la ejecución real se probó en el montaje caso-piezas-universidad-01 con el método manual equivalente. Respaldo del script anterior: en el PC del mantenedor.

### Corrige supuestos anteriores
- «Un diseño de Canva = un solo tamaño»: falso en la cuenta del usuario (diseño `custom` con páginas de tamaños mixtos).
- «Las fuentes de marca se importan si se declara la familia»: falso (solo biblioteca pública).

### Verificado en esta versión (contra Canva real)
`import-design-from-url` con HTML de páginas de tamaños distintos · `merge-designs insert_pages/move_pages/delete_pages` · `copy-design` · `edit-design update_fill + crop_media / insert_fill / delete_element / update_title+commit` · `export-design` PNG a tamaño nativo · `read-design` con `element_ids` ficticio · `resolve-shortlink` · `list-brand-kits`.
### No verificado
Plantilla con cuadros en fuente de marca + relleno por API · `autofill-design`/brand templates · reemplazo de fuente en bloque desde el panel de Canva · límite de páginas por diseño · importación de 9 programas (54 páginas) de una vez · Codex/Antigravity/VS Code.

## 2026-10-09 — Creación de la skill (v1.0.0)

Origen: caso Diplomas caso-diplomas-01 (2026-10-08/09). Petición del usuario: crear una skill con todo el proceso y las decisiones para pasar diseños HTML a Canva, bajo `direct-visual-design` como sub-skill propia, **obligatoria** ante cualquier trabajo de Canva, con carpeta principal `<repo>/skills/canva-design`.

### Añadido
- `SKILL.md` (frontmatter validado, 724 caracteres de descripción), `references/01…07`, `templates/diploma-20x14.template.html`.
- `scripts/`: `handshake.py`, `lint_html_for_canva.py`, `build_import_html.py`, `render_html.sh`, `split_pages.py`, `bake_assets.py` (panel, swoosh, triangles, marble, canvas-bg, vignette, logo), `pdf_pages.py`, `temp_host.sh`, `canva_verify.py`, `install.py`. Probados con los archivos reales del caso.
- `ejemplos/caso-diplomas-01/` (24 MB: HTML v1/v2, assets, previews, exportaciones de Canva, handoff/handshake del proyecto y `scripts-originales/` de la sesión; en el repo solo un README anónimo y los scripts `bake.py` y `streak.py`).
- `proyectos/caso-diplomas-01.md` + `INDICE.md`; `memoria/` (preferencias aprobadas e inbox); `conocimiento/README.md`.
- Pruebas: 6 de 7 assets horneados idénticos byte a byte; lint (v1 con errores esperados, v2 limpio); combinador; render Chrome headless; contraste WCAG calculado (no estimado).

### Integración
- `direct-visual-design/SKILL.md` (fuente e instalado en Claude Code): fila «Cualquier trabajo en Canva → `canva-design`» en la tabla (ii) y precondición en la regla 3. Respaldo del anterior en `_respaldo/`.
- `~/.claude/CLAUDE.md`: sección «Canva design» (respaldo en `_respaldo/`).
- Obsidian: fila en `Auditoría de skills y plugins`, fila en `Matriz multiplataforma de skills`, puntero en `04 Laboratorio de diseno`, nota de proyecto caso-diplomas-01 actualizada.
- Memoria de Claude Code: preferencia «trabajo de Canva → skill canva-design obligatoria».

### Instalado
- `~/.claude/skills/canva-design/` (núcleo, verificado por hash). Codex: no.

### Lecciones consolidadas (de la sesión de origen)
Importador conserva texto pero no imágenes; offset ~0,1 em del numeral; orden de capas; `merge-designs` de una operación; `edit-design` sin fuente/espaciado; escala física; hosting temporal con autorización por tarea; navegador del panel inútil para QA local. Detalle en `references/02` y `07`.
