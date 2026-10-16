---
name: design-illustrator
description: Skill propia y OBLIGATORIA para llevar un diseño HTML a Adobe Illustrator como archivo editable y limpio (.ai, PDF editable, base para EPS). Es sub-skill de direct-visual-design, que la llama cuando el entregable vive en Illustrator, pero si el usuario pide algo de Illustrator, .ai, EPS o PDF editable, o la nombra, esta skill manda y su proceso no se salta. Resuelve los defectos del PDF de Chromium al abrirlo en Illustrator, a saber, texto roto en una letra por objeto (deja cada línea en un texto y cada párrafo en UNA caja de texto de área con ancho de columna, sin separación silábica y con Tamaño automático), máscaras de recorte sin sentido y trazados invisibles que quedan como basura, páginas en blanco por fallos de pegado. Incluye preflight, exportación PDF a tamaño exacto, un maestro con una mesa de trabajo por lámina, limpieza de recortes, auditoría y verificación píxel a píxel. Usar ante Illustrator, .ai, EPS, PDF editable, vectores, manuales de marca o láminas que se editarán en Illustrator.
---

# Design Illustrator — sub-skill propia de `direct-visual-design`

## Protocolo gui-skills (obligatorio)

Esta skill vive en el repo **gui-skills** y sigue [`shared/protocolo-skill.md`](../../shared/protocolo-skill.md):

1. **Paso 0 — al día:** corre `python <repo>/tools/check_update.py --quiet`; si sale `ATRASADA`, ofrece
   `git pull` antes de seguir. Luego lee `HANDSHAKE.md` y el "Registro de trabajos" de `HANDOFF.md`.
2. **Privacidad:** en el repo los clientes solo se nombran con un código `caso-<tipo>-<NN>`; nunca
   nombres, marcas, dominios, correos, rutas personales ni credenciales.
3. **Paso final — memoria:** al cerrar un trabajo bien implementado, registra siempre la entrada con
   `python <repo>/tools/log_job.py --skill design-illustrator ...` (qué se hizo, qué salió bien, qué salió mal,
   incidencias). Obsidian es opcional: si el usuario lo tiene, registra también allí.

`<repo>` = `repo_path` de `~/.gui-skills/config.json`, o dos carpetas arriba de esta skill.

**Estatus (decisión del usuario, 2026-10-11):** `direct-visual-design` sigue siendo la skill principal y orquestadora de diseño; esta es su **sub-skill propia para todo lo que viva en Illustrator** (igual que `canva-design` para Canva). Cuando el usuario pide algo de Illustrator / `.ai` / EPS / PDF editable, o nombra esta skill, **su proceso es OBLIGATORIO y completo**. Precedencia: instrucción actual del usuario > brief/marca del proyecto > esta skill > heurísticas de otras skills secundarias (si una contradice este proceso, gana este proceso).

Reparto: `direct-visual-design` clasifica, analiza referencias, fija dirección y hace el QA de diseño; **`design-illustrator` decide cómo se exporta, se limpia y se verifica en Illustrator**. Si se invoca sola, aplica igualmente los principios de la principal.

## Regla de oro

> **Diseñar en HTML (Illustrator-ready) → aprobar → PDF vectorial a tamaño exacto → reconstruir el texto (línea → párrafo) → maestro con una mesa de trabajo por lámina → limpiar recortes → texto de área en automático → auditar y verificar contra el original.**
> **Nunca entregar el PDF crudo de Chromium:** al abrirlo en Illustrator cada letra es un texto suelto (489 objetos en una sola lámina) y hay cientos de máscaras de recorte sin sentido.

## Qué debe cumplir SIEMPRE el archivo entregado (criterio de aceptación)

1. **Cada palabra vive dentro de su caja de texto.** Títulos y etiquetas de una línea = un texto de punto. **Cada párrafo = UNA caja de texto de área** (texto corrido) con el ancho de la columna del HTML, el mismo interlineado, interletraje y alineación, y el **mismo ajuste de líneas que el navegador**. Cero «una letra por objeto».
2. **Separación silábica desactivada** en los párrafos (Illustrator parte «es-pecialista» por defecto; el navegador no).
3. **«Tamaño automático» activado en todos los textos de área**: la caja se ajusta a su texto y crece o encoge sola al editar.
4. **Recortes (clipping masks) solo si el diseño los pide.** Ninguno que no recorte nada, ninguno vacío, y **al soltar un recorte se borra su trazado** (si no, queda como objeto invisible = basura). Cero trazados sin relleno ni trazo, cero grupos vacíos.
5. **Fuente real** (no sustituida), tamaños y colores idénticos al HTML; nada de texto desbordado u oculto.
6. **Idéntico al original:** verificado píxel a píxel y letra a letra contra el render del HTML (`verify_fidelity.py`) y con `ai_audit.ps1`.
7. Una mesa de trabajo por lámina, nombrada (`p01`…), tamaño exacto en pt (1 px = 1 pt).

## Flujo obligatorio (detalle en [01-pipeline](references/01-pipeline-html-a-illustrator.md))

0. **Preflight:** `python -I scripts/handshake.py` (Windows + COM, Illustrator, fuente disponible en Illustrator, librerías, estado del MCP). Leer la nota del proyecto (en el vault de Obsidian, si el usuario lo usa) y `proyectos/`.
1. **HTML Illustrator-ready** ([03](references/03-html-illustrator-ready.md)): una lámina por archivo, tamaño fijo, texto real en bloques simples, sin `overflow:hidden`/sombras/filtros/gradientes/transform. Validar y **mostrar al usuario; esperar aprobación**.
2. **Exportar:** `export_pdf.py` (PDF a W×H pt, texto vivo) + `extract_paragraphs.py` (qué líneas forman cada párrafo).
3. **Construir el maestro:** `ai_pipeline.ps1 -Root <proyecto>` (letras → líneas → párrafos en texto de área → pegar en su mesa de trabajo → limpiar recortes → guardar `.ai` + PDF editable). **Avisar al usuario antes de lanzarlo** (Illustrator trabaja ~15 min; guardar sus documentos).
4. **Tamaño automático:** `ai_autosize_text.ps1` (no hay API: hace el clic en el cuadro de Illustrator; el ratón se mueve ~10 s).
5. **Verificar:** `verify_fidelity.py` (píxeles + caracteres) y `ai_audit.ps1` (textos, fuentes, desbordes, recortes). Reparar láminas con `ai_repair_page.ps1`. **Mirar** las láminas, no fiarse solo de los números.
6. **Entregar y registrar:** rutas de los archivos, qué se verificó y qué no; HANDOFF del proyecto; registrar el trabajo con el Paso final del protocolo (HANDOFF §4 de la skill) y, si hay Obsidian, la nota del proyecto y el registro de la skill; `memoria/inbox-aprendizajes.md`.

## Reglas duras

1. El HTML es la fuente de verdad; **Illustrator se construye desde él**, no al revés. Cambios de diseño → HTML → regenerar (no retocar a mano salvo orden del usuario).
2. **Backup antes de limpiar o modificar** un `.ai` del usuario (`backups/` del proyecto).
3. **No cerrar ni sobrescribir documentos abiertos del usuario.** Los scripts crean un maestro nuevo y no cierran nada. **Nunca terminar el proceso de Illustrator sin permiso expreso.** Illustrator (Beta) puede cerrarse solo en corridas largas y se pierde lo no guardado: avisar y guardar antes.
4. **Los recortes que sí recortan no se borran en silencio:** `aiCleanClips` los devuelve en `necesarios` (lámina, tamaño, cuánto sobresale). Decidir: rehacerlos con geometría real (p. ej. un borde redondeado recortado en 3 trozos = un arco abierto con trazo) o conservarlos si el diseño lo pide (foto recortada, máscara de forma).
5. **Solo texto de área si el ajuste de líneas coincide con el del navegador**; si no coincide, se deja como líneas sueltas y se informa. Nunca forzar.
6. **«Tamaño automático» y la unión de párrafos se repiten tras rehacer una lámina** (`ai_repair_page.ps1` devuelve la lámina sin la casilla).
7. **Fuente:** debe estar disponible en Illustrator (instalada o Adobe Fonts). Sin ella se sustituye al abrir. Comprobar con `handshake.py`.
8. **Control de Illustrator = COM (`Illustrator.Application`) + ExtendScript**, verificado. El **MCP de Illustrator** (`localhost:18412`) está registrado pero **a 2026-10-11 acepta la conexión y no responde**; no depender de él ([04](references/04-control-de-illustrator-com-y-mcp.md)).
9. **Credenciales:** el token del MCP nunca va en archivos de la skill ni en notas; vive en la configuración de usuario de Claude (`~/.claude.json`) o en una variable de entorno. Se obtiene del panel «MCP y herramientas» de Illustrator.
10. **Verificar siempre** (píxeles + caracteres + auditoría) y mirar las láminas; decir con franqueza qué no se verificó. No declarar «listo» solo porque el script no dio error.
11. No inventar contenido ni «arreglar» el texto del cliente al exportar: el texto sale tal cual está en el HTML.
12. PDF/AI en **RGB**. Para imprenta (CMYK, sangrado) es un paso aparte y se pide al usuario.

## Qué NO hacer

- No abrir los PDF de `export/pdf` (crudos) para trabajar: son un intermedio.
- No usar `Ctrl+Shift+O` ni «soltar máscara» a mano como método: deja trazados invisibles.
- No lanzar dos procesos de Illustrator a la vez (COM los serializa y se mezclan las ventanas activas).
- No usar `app.userInteractionLevel = DONTDISPLAYALERTS` al abrir cuadros de diálogo (no se muestran).
- No asumir que `anchor` de un texto es escribible (es de solo lectura): se mueve con `translate`.
- No mezclar con el flujo HTML→Figma ni con Canva: son entregas distintas; si el usuario pide varias, tratarlas por separado.

## Enrutamiento de referencias y scripts

| Necesidad | Archivo |
|---|---|
| Proceso completo paso a paso (la receta) | [01-pipeline-html-a-illustrator.md](references/01-pipeline-html-a-illustrator.md) |
| Catálogo de defectos y su solución (texto, recortes, pegado, cuadros, fuentes) | [02-defectos-y-soluciones.md](references/02-defectos-y-soluciones.md) |
| Cómo escribir el HTML para que salga bien | [03-html-illustrator-ready.md](references/03-html-illustrator-ready.md) |
| COM, ExtendScript, MCP de Illustrator (registro en Claude/Codex), trucos y límites | [04-control-de-illustrator-com-y-mcp.md](references/04-control-de-illustrator-com-y-mcp.md) |
| QA y verificación | [05-qa-verificacion.md](references/05-qa-verificacion.md) |
| Caso modelo (`caso-manual-marca-01`: manual de marca, 46 láminas) | [06-caso-manual-marca-01.md](references/06-caso-manual-marca-01.md) |

| Script | Para qué |
|---|---|
| `scripts/handshake.py` | Preflight local (solo lectura) |
| `scripts/export_pdf.py` | HTML → PDF a tamaño exacto en pt, texto vivo (intermedio) |
| `scripts/extract_paragraphs.py` | Bloques de varias líneas del DOM → JSON |
| `scripts/ai_pipeline.ps1` | **El proceso:** PDFs → maestro `.ai` + PDF editable (letras→líneas→párrafos, pegado con reintento, limpieza de recortes) |
| `scripts/ai_fix_text.jsx` | Biblioteca ExtendScript: `aiFixText`, `aiMergeParagraphs`, `aiCollectLines` |
| `scripts/ai_clean.jsx` / `ai_clean_clips.ps1` | Limpieza de recortes (biblioteca / sobre el documento activo, con `-AuditOnly`) |
| `scripts/ai_autosize_text.ps1` | «Tamaño automático» en todos los textos de área (clic automatizado) |
| `scripts/ai_audit.ps1` | Auditoría de solo lectura (textos, fuentes, desbordes, recortes) |
| `scripts/ai_repair_page.ps1` | Rehace y vuelve a pegar UNA lámina |
| `scripts/ai_merge_open.ps1` | Une párrafos dentro de un documento ya abierto |
| `scripts/verify_fidelity.py` | Original vs maestro: píxeles y caracteres |
| `scripts/install.py` | Instalar por copia / verificar el núcleo (en gui-skills lo instala el instalador del repo con un enlace; este script detecta el enlace y no copia) |

## Base de conocimiento de la skill

Ruta: `<repo>/skills/design-illustrator/` (el instalador de gui-skills la enlaza en `~/.claude/skills/`; si no existe en la máquina actual, decirlo y usar las referencias empaquetadas).

| Carpeta | Contenido | ¿Se instala? |
|---|---|---|
| `SKILL.md`, `references/`, `scripts/` | Núcleo | Sí |
| `HANDOFF.md`, `HANDSHAKE.md`, `CHANGELOG.md` | Decisiones y registro de trabajos, estado vivo y capacidades verificadas, historial | Se leen en el Paso 0 |
| `ejemplos/caso-manual-marca-01/` | Herramientas originales de la sesión (clics, auditorías, pruebas del MCP) y su README | Solo lectura |
| `proyectos/` | Ficha por caso con Illustrator, solo con código (`caso-manual-marca-01.md`) + `INDICE.md` | Leer antes de trabajar para una marca |
| `memoria/` | Preferencias aprobadas e inbox de aprendizajes | Leer siempre |
| `conocimiento/` | Notas de apoyo | Opcional |

Antes de trabajar para una marca: leer `proyectos/INDICE.md` y su ficha. Aprendizajes nuevos → `memoria/inbox-aprendizajes.md`; promoverlos solo con aprobación explícita o repetición.

## Memoria, Obsidian y otras skills

- **Memoria primaria = el repo:** HANDOFF §4 (Registro de trabajos), `memoria/` y `proyectos/`. **Obsidian es una capa opcional**: solo si el usuario la tiene (`obsidian_vault` en `~/.gui-skills/config.json` o el MCP de Obsidian responde) se actualiza además la nota madre del proyecto (`obsidian_projects_folder`) y, si cambió la herramienta, la nota de registro de skills (`obsidian_registry_note`). Sin Obsidian, se salta.
- Dirección de arte, tipografía, color y QA estratégico: `direct-visual-design`. Canva: `canva-design`. Figma: método HTML→Figma de la principal.
- `adobe-suite` (referencia de ExtendScript e Illustrator MCP) puede consultarse para la API; **el proceso manda esta skill**.

## Estado y portabilidad

**v1.0.0 (2026-10-11).** Instalada en Claude Code por enlace desde el repo (`~/.claude/skills/design-illustrator`). Codex/Antigravity/VS Code: **no instalada ni verificada**. Estado vivo y siguientes pasos: `HANDOFF.md` y `HANDSHAKE.md`.
