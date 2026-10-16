# CHANGELOG — design-illustrator

## 2026-10-16 — Migración al repo gui-skills (anonimizada)

- Fuente del mantenedor y copia instalada reconciliadas: **idénticas** en los 20 archivos del núcleo (`SKILL.md`, `references/`, `scripts/`); la fuente aportaba además `HANDOFF.md`, `HANDSHAKE.md`, `CHANGELOG.md`, `conocimiento/`, `memoria/`, `proyectos/` y `ejemplos/`.
- Bloque **Protocolo gui-skills** insertado tras el título de `SKILL.md`; "Integración con Obsidian" pasa a "Memoria, Obsidian y otras skills" (Obsidian opcional).
- **Renombrado interno al anonimizar:** las funciones de la biblioteca ExtendScript llevaban el nombre del cliente como prefijo (`<prefijo>FixText`, `<prefijo>MergeParagraphs`, `<prefijo>CollectLines`, `<prefijo>CleanClips`, `<prefijo>AuditClips`, …) y las variables `<PREFIJO>_PARAS` / `<PREFIJO>_BREAK`. Ahora son `aiFixText`, `aiMergeParagraphs`, `aiCollectLines`, `aiCleanClips`, `aiAuditClips`, … y `AI_PARAS` / `AI_BREAK`, de forma coherente en `ai_fix_text.jsx`, `ai_clean.jsx` y todos los `.ps1`. La lógica no cambia.
- `scripts/install.py` detecta que la skill está instalada por enlace al repo y no copia.
- Anonimizado: cliente → `caso-manual-marca-01` (la referencia del caso, la ficha de `proyectos/` y la carpeta de `ejemplos/` se renombraron con el código); rutas del proyecto y de la carpeta temporal → `<carpeta-del-proyecto>` / `$env:TEMP`; `mcp_probe.py` lee el token de `ILLUSTRATOR_MCP_TOKEN` o de un archivo local fuera del repo.
- Fuera del repo: `_respaldo/`. `HANDOFF.md` y `HANDSHAKE.md` reestructurados con la plantilla de gui-skills; el Registro de trabajos se sembró con 1 entrada.


## 2026-10-11 — v1.0.0 (creación, caso `caso-manual-marca-01`: manual de marca)

Origen: petición del usuario tras exportar el manual de caso-manual-marca-01 (46 láminas HTML) a Illustrator: «creemos una subskill de direct-visual-design… design-illustrator… que cree un PDF editable para Illustrator… con los textos en su caja, sin clipping masks sin sentido ni basura, con el text area en automático… con handoff y handshake… y graba el MCP de Illustrator».

### Añadido
- `SKILL.md` (criterio de aceptación, flujo, 12 reglas duras), `references/01…06`.
- `scripts/`: `handshake.py`, `export_pdf.py`, `extract_paragraphs.py`, `ai_pipeline.ps1`, `ai_fix_text.jsx`, `ai_clean.jsx`, `ai_clean_clips.ps1`, `ai_autosize_text.ps1`, `ai_audit.ps1`, `ai_repair_page.ps1`, `ai_merge_open.ps1`, `verify_fidelity.py`, `install.py` (generalizados desde los scripts del proyecto caso-manual-marca-01: parámetros `-Root`, `-Master`, `-OutDir`, tamaño).
- `HANDOFF.md`, `HANDSHAKE.md`, `memoria/`, `proyectos/` (ficha caso-manual-marca-01), `conocimiento/`, `ejemplos/caso-manual-marca-01/` (herramientas originales de la sesión).
- Integración: fila en `direct-visual-design/SKILL.md`, sección en `~/.claude/CLAUDE.md`, alta en el registro de skills del vault del mantenedor (auditoría y matriz de skills).
- MCP de Illustrator registrado en Claude Code (`claude mcp add … --scope user illustrator`); sin respuesta del servidor.

### Cambios respecto a los scripts del proyecto
- `ai_pipeline.ps1` ahora incluye la **limpieza de recortes** al final y **no cierra documentos** (la versión anterior cerraba los abiertos al inicio).
- `ai_clean.jsx` generaliza la limpieza: el redibujado del asa de la bolsa ya no está dentro del script (se reporta como «necesario»).
- `ai_autosize_text.ps1` automatiza el clic en el cuadro (antes manual): búsqueda de la ventana con timeout, clics proporcionales, detección de la casilla por las esquinas (la palomita blanca confundía a la detección por el centro).
- `handshake.py` pregunta por COM si la fuente está disponible en Illustrator (Poppins venía de Adobe Fonts y no había archivos).
- Todos los `.ps1` guardados con BOM UTF-8.

### Verificado
Prueba de los scripts generalizados con 3 láminas del manual (`-OutDir export\illustrator-prueba`, borrada después), auditoría del documento real, y clic automático de «Tamaño automático» en un documento de prueba (3 cajas ajustadas).
