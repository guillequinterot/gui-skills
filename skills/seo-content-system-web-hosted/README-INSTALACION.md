<!-- GENERADO por tools/build_hosted.py desde skills/seo-content-system (v1.5.0, huella 7ca0efb2c34f). NO EDITAR A MANO: cambia la skill o hosted-src/ y regenera con `python tools/build_hosted.py`. -->
# Instalación de seo-content-system (versión web hosted)

Esta carpeta es la versión de `seo-content-system` (v1.5.0) para **Claude.ai (Project)** y **ChatGPT.com (Custom GPT / Project)** — entornos sin acceso al sistema de archivos, sin MCP local y sin Obsidian.

## Contenido

- `00-instrucciones-del-proyecto.md` — pegar como **instrucciones del Project** (Claude.ai) o **instrucciones del sistema/GPT** (ChatGPT Custom GPT/Project). Es la adaptación de `SKILL.md`. La primera línea es un comentario HTML que avisa de que el archivo es generado: se puede omitir al pegar.
- `knowledge/` — 10 documentos temáticos (consolidados a partir de 67 archivos de la skill) para subir como **archivos de conocimiento** del Project/GPT:

  - `knowledge/01-estrategia-y-arquitectura.md` — Estrategia, arquitectura y keyword research
  - `knowledge/02-redaccion-y-estilo.md` — Redacción, estilo y calidad editorial
  - `knowledge/03-on-page-y-datos-estructurados.md` — On-page, imágenes y datos estructurados
  - `knowledge/04-seo-tecnico.md` — SEO técnico y acceso de bots de IA
  - `knowledge/05-geo-y-citacion-ia.md` — GEO: citación en IA, entidades y densidad de señales
  - `knowledge/06-local-programatico-social.md` — SEO local, programático y social search
  - `knowledge/07-medicion-y-decisiones.md` — Medición, Search Console y decisiones
  - `knowledge/08-fuentes-y-gobernanza.md` — Fuentes, evidencia y gobernanza de actualizaciones
  - `knowledge/09-keyword-research-hosted.md` — Keyword research asistido por IA en entornos alojados
  - `knowledge/11-plantillas.md` — Plantillas de la skill

- `10-memoria-sin-obsidian.md` — cómo esta versión reemplaza el acceso a la memoria de la skill (subida manual de notas).

## Instalar en Claude.ai

1. Crear un **Project** nuevo (o abrir el existente).
2. En **Project instructions**, pegar el contenido de `00-instrucciones-del-proyecto.md`.
3. En **Project knowledge**, subir los 10 archivos de `knowledge/` (y, si quieres, `10-memoria-sin-obsidian.md`).
4. Si vas a leer datos de Sheets o Drive, conectar **Google Workspace** (Drive/Sheets) desde `Connectors` y verificarlo desde el Project.
5. Probar con una consulta pequeña (p. ej. "lee el Sheet X y dime qué columnas tiene") antes de ejecutar un flujo completo.

## Instalar en ChatGPT.com

Dos opciones válidas, según qué tengas disponible en tu plan:

**Opción A — Project (más simple, recomendado si no necesitas un GPT público):**
1. Crear un **Project** en ChatGPT.
2. En las instrucciones del Project, pegar `00-instrucciones-del-proyecto.md`.
3. Subir los 10 archivos de `knowledge/` como archivos del proyecto.
4. Si usas Drive, verificar que el conector de Google Drive esté activo.

**Opción B — Custom GPT (si quieres compartirlo o usar Actions):**
1. Crear un GPT nuevo en el creador de GPTs.
2. En **Instructions**, pegar `00-instrucciones-del-proyecto.md` (recortar si el editor de GPT tiene límite de caracteres más estricto que un Project — en ese caso, dejar los principios y el flujo maestro, y mover el detalle a `knowledge/`).
3. En **Knowledge**, subir los 10 archivos de `knowledge/`.
4. Si más adelante quieres una conexión directa a Search Console/GA4 (no disponible de forma nativa), se necesitaría una **Action** (OpenAPI) apuntando a un servicio propio — no está incluido en este paquete.

## Limitación importante a tener presente

Ni Claude.ai ni ChatGPT.com tienen conector nativo para **Google Search Console**, **GA4** o **Bing Webmaster Tools**. La vía práctica con Drive/Sheets es: procesos locales (con credenciales que viven en tu máquina y nunca se suben a estas plataformas) exportan datos a un Google Sheet, y esta versión hosted lee ese Sheet a través del conector de Drive. Ver `07-medicion-y-decisiones.md` y `09-keyword-research-hosted.md` dentro de `knowledge/`.

## Privacidad

No subas a un Project o GPT compartido nombres de clientes, datos de contacto, credenciales ni exportaciones con datos personales. Para los casos usa un código (`caso-<tipo>-<NN>`).

## Mantenimiento

Esta carpeta es una instantánea **generada** por `tools/build_hosted.py` desde `skills/seo-content-system/` (versión 1.5.0, huella de la fuente `3c20b2d81445`). No se edita a mano:

- Para cambiar una regla, edita la skill (o `hosted-src/` para las partes escritas a mano) y corre `python tools/build_hosted.py`.
- `python tools/build_hosted.py --check` sale con código 1 si lo guardado está desfasado de la skill.
- Tras regenerar, vuelve a subir los archivos cambiados al Project/GPT.
