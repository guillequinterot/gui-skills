# HANDOFF — seo-content-system-web-hosted

> **Esta carpeta es GENERADA. No se edita a mano.** Todo lo que no sea este `HANDOFF.md` y `HANDSHAKE.md`
> lo escribe `tools/build_hosted.py`; un cambio a mano se pierde en la siguiente regeneración y hace que
> `python tools/build_hosted.py --check` falle.

## 1. Qué es y cuándo se usa

Port de `seo-content-system` para entornos **sin sistema de archivos ni MCP**: un Project de Claude.ai o un
Custom GPT / Project de ChatGPT. Contiene las instrucciones del proyecto (`00-instrucciones-del-proyecto.md`),
la guía de memoria sin acceso al repo (`10-memoria-sin-obsidian.md`), la guía de instalación
(`README-INSTALACION.md`) y 10 documentos de conocimiento en `knowledge/` que consolidan las referencias de la
skill. No es una skill de Claude Code: no tiene `SKILL.md` ni se instala por enlace.

Cómo se deriva:

- `knowledge/*.md`: concatenación mecánica de archivos de `skills/seo-content-system/` (sin frontmatter), según
  `skills/seo-content-system/hosted-src/knowledge-map.json`.
- `00-…`, `10-…`, `README-INSTALACION.md`: plantillas escritas a mano en `skills/seo-content-system/hosted-src/`
  con marcadores `{{…}}` que rellena el script (versión, huella de la fuente, listas y conteos).
- Cada archivo generado empieza con una cabecera que lo declara generado y da la versión y la huella de la fuente.

## 2. Instalación y dependencias

- Para **usarla**: seguir `README-INSTALACION.md` (pegar las instrucciones en un Project/GPT y subir `knowledge/`).
- Para **regenerarla**: `python tools/build_hosted.py` (solo biblioteca estándar de Python 3.9+). Para comprobar
  que lo guardado está al día: `python tools/build_hosted.py --check` (sale con 1 si está desfasado; úsalo antes
  de cada commit que toque `skills/seo-content-system/`).
- No se instala en `~/.claude/skills`: el instalador de gui-skills la ignora porque no tiene `SKILL.md`.

## 3. Decisiones vigentes

| Fecha | Decisión | Quién la aprobó | Por qué |
|---|---|---|---|
| 2026-08-26 | Consolidar las referencias en 10 documentos temáticos de `knowledge/`; dejar fuera `keyword-research-ia-local-desktop.md` | guille | Límites prácticos de archivos de conocimiento en Claude Projects y Custom GPT; ese documento es específico de un entorno con acceso local |
| 2026-08-26 | Generar la carpeta con script y regenerarla ante cambios significativos de la skill local, en vez de mantener dos versiones a mano | guille | Dos versiones editadas a mano se desincronizan |
| 2026-10-16 | El script vive en el repo (`tools/build_hosted.py`), es determinista y tiene `--check`; las partes escritas a mano pasan a `hosted-src/` de la skill; toda referencia nueva de la skill debe clasificarse en `knowledge-map.json` (incluida o excluida) o el script falla | guille | Que cualquier colaborador pueda regenerar sin depender de un script local perdido, y que nada nuevo se quede fuera sin querer |

## 4. Registro de trabajos

> Una entrada por trabajo terminado o implementado y aprobado. Solo se agregan entradas al final; las
> correcciones van como entrada nueva. Casos solo con código `caso-<tipo>-<NN>`. Formato:
> `templates/entrada-de-trabajo.md`. Se escribe con `tools/log_job.py`.

<!-- registro:inicio -->

### 2026-08-26 · caso-mantenimiento-03 · guille

- **Qué se hizo:** Primera versión hosted de `seo-content-system`: 10 documentos de conocimiento, instrucciones de proyecto adaptadas de `SKILL.md`, archivo de memoria sin Obsidian y guía de instalación para Claude.ai y ChatGPT.
- **Salió bien:** Consolidar por tema en vez de subir ~34 archivos sueltos; el puente de datos por Google Sheets para Search Console/GA4/Bing.
- **Salió mal / incidencia:** La instantánea se generó con un script local que no se versionó y quedó desfasada de la skill (le faltaba una línea sobre `screaming-frog-seo` en el mapa temático).
- **Regla candidata:** Todo artefacto derivado se genera con un script versionado que tenga `--check`.
- **Herramientas:** Claude.ai Projects, ChatGPT Projects/GPTs

### 2026-10-16 · caso-mantenimiento-07 · guille

- **Qué se hizo:** Se escribió `tools/build_hosted.py` (determinista, solo biblioteca estándar, con `--check`) y se regeneró esta carpeta desde la skill ya migrada al repo. Las plantillas escritas a mano (`00-…`, `10-…`, `README-INSTALACION.md`) se movieron a `skills/seo-content-system/hosted-src/` y se anonimizaron.
- **Salió bien:** La instantánea anterior resultó ser una concatenación puramente mecánica (frontmatter fuera, una sección «Fuente original» por archivo), así que el script reproduce su estructura sin pérdida; el contenido solo difiere en lo que cambió la skill (anonimización, memoria en el repo en lugar de Obsidian, `screaming-frog-seo` como opcional).
- **Salió mal / incidencia:** Nada relevante.
- **Regla candidata:** ninguna
- **Herramientas:** Python 3.12, `tools/build_hosted.py`

<!-- registro:fin -->

## 5. Reglas candidatas (sin aprobar)

| Regla | Visto en (casos) | Estado |
|---|---|---|
| Todo artefacto derivado se genera con un script versionado que tenga `--check` | caso-mantenimiento-03 | candidata: un solo caso |
