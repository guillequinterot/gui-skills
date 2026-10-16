---
name: seo-content-system
description: Investiga, planifica, redacta, optimiza, audita, mide y actualiza contenido para SEO, AEO, GEO, búsqueda social, SEO local y SEO programático. Usar cuando el agente deba trabajar con intención de búsqueda, customer journey, keywords, arquitectura de contenidos, briefs, artículos, landing pages, metatítulos, metadescripciones, slugs, imágenes, enlazado interno, schema, GA4, Search Console, Clarity, fuentes, contenido natural en español, medición posterior o novedades de buscadores. Usar también para visibilidad y citación ante inteligencia artificial (GEO, LLMs, ChatGPT, Copilot, Perplexity, Gemini), páginas agrupadoras, entidades y grafos de conocimiento (Wikidata, sameAs, tripletas semánticas), diversificación de canales, SEO en YouTube y presencia en comunidades como Reddit o Quora. Antes de producir cualquier salida lee la memoria de la skill (HANDSHAKE/HANDOFF del repo gui-skills y, si el usuario usa Obsidian, su bóveda) y registra aprendizajes de proyectos sin convertir observaciones no verificadas en reglas.
---

# SEO Content System

## Protocolo gui-skills (obligatorio)

Esta skill vive en el repo **gui-skills** y sigue [`shared/protocolo-skill.md`](../../shared/protocolo-skill.md):

1. **Paso 0 — cada vez que uses la skill:** corre `python <repo>/tools/check_update.py --quiet --pull`.
   `ACTUALIZADA n` → díselo al usuario en una línea y **vuelve a leer este `SKILL.md`** antes de seguir;
   `CAMBIOS_LOCALES` → avisa y no actualices; `SIN_RED` / `SIN_CREDENCIAL` → sigue con la copia local y dilo.
   Si avisa de aportes sin publicar, corre `python <repo>/tools/publish_job.py --reintentar` (preaprobado).
   Luego lee `HANDSHAKE.md` y el "Registro de trabajos" de `HANDOFF.md`.
2. **Privacidad:** en el repo los clientes solo se nombran con un código `caso-<tipo>-<NN>`; nunca
   nombres, marcas, dominios, correos, rutas personales ni credenciales.
3. **Paso final — obligatorio y preaprobado** (trabajo terminado y aprobado por el usuario; no pidas permiso):
   (1) `python <repo>/tools/log_job.py --skill seo-content-system ...` por cada skill que intervino (qué se hizo, qué
   salió bien, qué salió mal, incidencias); (2) actualiza `HANDSHAKE.md` si cambió el estado vivo;
   (3) publica con `python <repo>/tools/publish_job.py --tema <caso-o-tema>` (rama + push + PR; el mantenedor
   puede añadir `--merge`); (4) dile al usuario el resultado (`PR_CREADO <url>` / `PUBLICADO <url>` /
   `PENDIENTE` / `BLOQUEADO`). Obsidian es opcional: si el usuario lo tiene, registra también allí.

`<repo>` = `repo_path` de `~/.gui-skills/config.json`, o dos carpetas arriba de esta skill.

Trabajar como un sistema editorial y de medición, no como un generador de texto basado únicamente en keywords.

## Paso 0 obligatorio: leer la memoria antes de actuar

Esta skill no se ejecuta desde memoria del modelo. Siempre que se invoque —de forma explícita por el usuario o de forma automática al detectar una tarea de contenido— **el primer acto es leer la memoria**, no redactar ni planificar.

Antes de producir cualquier salida:

1. Cumplir el Protocolo gui-skills de arriba (`check_update.py --quiet --pull` en cada uso de la skill), y leer [`HANDSHAKE.md`](HANDSHAKE.md) (estado vivo, herramientas verificadas, pendientes) y el "Registro de trabajos" de [`HANDOFF.md`](HANDOFF.md) (decisiones vigentes y lecciones de casos anteriores).
2. Revisar la memoria de la propia skill por tema (no entera): `memoria/aprendizaje/inbox/` (candidatos aún sin validar), `memoria/decisiones/` (cambios aprobados) y `memoria/fuentes/` (fuentes ya evaluadas) antes de afirmar datos, cifras o reglas SEO.
3. **Si el usuario usa Obsidian** (clave `obsidian_vault` en `~/.gui-skills/config.json`, la clave heredada `vault` en `~/.seo-content-system.json` o el MCP de Obsidian responde): consultar además la carpeta de esta skill en su bóveda (`06_Aprendizaje/`, `08_Fuentes/`, `09_Proyectos/`, ver [memory-integration.md](references/memory-integration.md)) y la nota madre del proyecto en la carpeta de proyectos que indique `obsidian_projects_folder`. Sin Obsidian, este punto se salta sin más.
4. Si el trabajo pertenece a un proyecto del usuario, abrir su brief o nota de proyecto (en la carpeta del proyecto del usuario, nunca dentro del repo).

La memoria (HANDOFF/HANDSHAKE, `memoria/` y, si existe, la bóveda) es la versión actual del conocimiento; el modelo entrenado es la versión vieja. Cuando ambos difieran, **gana la memoria**, salvo que la instrucción presente del usuario, el brief activo o una fuente primaria digan otra cosa.

Si la memoria no es accesible (sin red y sin copia local, bóveda configurada pero inexistente, MCP de Obsidian caído), **decirlo explícitamente** y continuar marcando la salida como *no contrastada con memoria de largo plazo*. Nunca simular que se consultó.

Al cerrar el trabajo, devolver lo aprendido a la memoria según el "Paso final" del protocolo y la sección "Memoria: repo primero, Obsidian opcional" de más abajo.

## Principios obligatorios

1. Comprender primero el negocio, la audiencia, la consulta, la intención y la etapa del recorrido.
2. Separar hechos, inferencias, hipótesis, recomendaciones y decisiones.
3. Priorizar datos propios, documentación oficial, fuentes primarias e investigación académica.
4. No fingir acceso a GA4, Search Console, Clarity, CMS, SERP ni herramientas de keywords.
5. No convertir correlaciones, experimentos o consejos de terceros en reglas universales.
6. Escribir con naturalidad porque el significado y la progresión son claros; no introducir errores para “parecer humano”.
7. Optimizar sin forzar la gramática ni repetir keywords mecánicamente.
8. Mantener visible y útil el contenido descrito por datos estructurados.
9. No cambiar una URL publicada sin evaluar redirección, enlaces, sitemap, canonicals e impacto.
10. No reescribir las reglas estables de la skill a partir de una sola sesión.
11. No aplicar ingeniería lingüística forzada dentro de un texto (densidades léxicas objetivo, sinónimos inyectados, anáforas nominales obligatorias, conectores puestos por cuota). La evidencia disponible indica que **penaliza** la citación en IA. Ver [ai-citation-and-geo-playbook.md](references/ai-citation-and-geo-playbook.md).
12. Distinguir siempre **entrenamiento** (pesos del modelo, lento, umbral de corpus) de **recuperación** (RAG/búsqueda en vivo, inmediata). Casi todo el SEO accionable hoy opera sobre recuperación; no prometer efectos de entrenamiento.
13. Optimizar la **entidad y su ecosistema** (agrupadores, presencia multiplataforma, grafo de conocimiento), no la página aislada. Ver [entity-presence-and-knowledge-graph.md](references/entity-presence-and-knowledge-graph.md).

## Flujo maestro

### 1. Clasificar la tarea

Elegir uno o varios modos:

- `research`: investigar demanda, SERP, fuentes, entidades y competidores.
- `strategy`: construir mapa de temas, intención, journey, arquitectura y prioridades.
- `brief`: preparar un brief verificable antes de redactar.
- `write`: crear o reescribir contenido.
- `on-page`: optimizar títulos, metadescripciones, encabezados, URLs, imágenes y enlaces.
- `technical`: revisar rastreo, indexación, canonicals, rendimiento, renderizado y schema.
- `local`: trabajar entidades, sedes, GBP y necesidades geográficas reales.
- `programmatic`: diseñar páginas escalables con datos y utilidad diferenciada.
- `social-search`: adaptar contenido a descubrimiento en plataformas sociales y video.
- `geo`: trabajar visibilidad y citación ante sistemas de inteligencia artificial (agrupadores, ecosistema, formatos).
- `keyword-research`: recopilar, ampliar, validar, agrupar, mapear, priorizar y medir consultas con datos verificables y asistencia de IA.
- `entity`: construir o corregir la entidad y su presencia en grafos de conocimiento (Wikidata, `sameAs`, perfiles).
- `measure`: analizar Search Console, GA4, Clarity y conversiones.
- `update`: actualizar contenido o revisar novedades SEO.
- `learn`: registrar un aprendizaje del trabajo para revisión posterior.

### 2. Establecer evidencia disponible

Declarar cuál escenario aplica:

- Acceso directo a datos o conectores.
- Archivos exportados, capturas o reportes.
- Investigación web verificable.
- Información aportada por el usuario.
- Proyecto nuevo sin datos propios.

Si falta información crítica, pedirla o avanzar con supuestos etiquetados.

### 3. Definir la unidad de trabajo

Registrar como mínimo:

```text
Objetivo del negocio:
Audiencia:
País e idioma:
Página o activo:
Consulta o keyword principal:
Intención principal:
Intención secundaria:
Componente local:
Etapa del journey:
Necesidad:
Nivel de conocimiento:
Objeción:
Acción siguiente:
CTA:
KPI:
Fuentes disponibles:
```

Leer [search-intent-and-customer-journey.md](references/search-intent-and-customer-journey.md) y [keyword-research-and-query-mapping.md](references/keyword-research-and-query-mapping.md) para investigación, mapeo y priorización.

### 3.5 Seleccionar la ruta de keyword research

Antes de investigar keywords, comprobar capacidades reales de la sesión.

- Si existe acceso autorizado al sistema de archivos, procesos locales, Obsidian, exportaciones locales o MCP local, leer [keyword-research-ia-local-desktop.md](references/keyword-research-ia-local-desktop.md).
- Si la ejecución ocurre en ChatGPT.com, Claude.ai u otro entorno alojado sin acceso al equipo, leer [keyword-research-ia-web-hosted.md](references/keyword-research-ia-web-hosted.md).
- Si las capacidades son mixtas, usar la ruta local solo para recursos comprobados y aplicar la ruta web como fallback para lo demás.
- No afirmar acceso a una herramienta, cuenta, archivo, API, CMS, Sheet, bóveda o rastreador hasta comprobarlo.
- Para la frecuencia con la que repetir cada tipo de keyword research y qué eventos deben adelantar una revisión, leer [keyword-research-cadence-and-triggers.md](references/keyword-research-cadence-and-triggers.md).

### 4. Construir significado y arquitectura

Definir:

- Respuesta central.
- Preguntas secundarias plausibles.
- Entidades y relaciones.
- Evidencia necesaria.
- Orden lógico.
- Profundidad adecuada.
- Enlaces internos.
- Siguiente paso de conversión.

No afirmar que un mapa de subconsultas reproduce exactamente el funcionamiento interno de un buscador o una LLM.

Decidir además si la pieza debe ser un **agrupador** (una URL que resuelve varias sub-consultas por tipología de contenido) o una página específica. Ante duda, agrupar: la evidencia disponible indica que los agrupadores concentran la citación en IA y las microURLs por keyword aislada casi no se citan.

Definir la **ficha de entidad** antes de redactar cuando la pieza deba reforzar una marca, persona o producto.

Leer [semantic-writing-and-meaning.md](references/semantic-writing-and-meaning.md), [content-brief-and-architecture.md](references/content-brief-and-architecture.md) y [internal-linking-and-conversion-paths.md](references/internal-linking-and-conversion-paths.md). Para agrupadores y entidad, leer [ai-citation-and-geo-playbook.md](references/ai-citation-and-geo-playbook.md) y [entity-presence-and-knowledge-graph.md](references/entity-presence-and-knowledge-graph.md).

### 5. Redactar

Escribir primero para resolver la necesidad real. Presentar pronto la respuesta cuando la intención lo favorezca; no imponer BLUF ni un número fijo de palabras.

Aplicar:

- Precisión semántica.
- Referentes claros.
- Progresión temática.
- Ritmo variable.
- Vocabulario compatible con la marca y el país.
- Ejemplos y datos verificables.
- Persuasión proporcional a la etapa del journey.

No aplicar reglas lingüísticas por cuota: nada de densidades léxicas objetivo, sinónimos inyectados, prohibición de pronombres ni conectores puestos para cumplir una proporción. Corregir el enunciado que de verdad es ambiguo, no todos por sistema. La evidencia disponible indica que el texto forzado pierde citaciones frente al texto natural de experto.

Anclar la autoría real —persona nombrada, credenciales, perfil verificable— desde el inicio de la pieza cuando el formato lo permita.

Leer [natural-writing-and-robotic-patterns.md](references/natural-writing-and-robotic-patterns.md), [spanish-style-and-capitalization.md](references/spanish-style-and-capitalization.md) y [brand-voice-and-language-variants.md](references/brand-voice-and-language-variants.md). Para artículos largos de investigación o agrupadores extensos, leer [editorial-pattern-long-form.md](references/editorial-pattern-long-form.md).

### 6. Entregar el paquete SEO

Cuando aplique, incluir:

- Keyword, intención y journey.
- Title SEO.
- Metadescripción.
- H1 y estructura H2/H3.
- Slug.
- Enlaces internos de entrada y salida.
- Anchor texts.
- Nombres de archivo, alt y captions de imágenes.
- Schema recomendado con límites.
- Fuentes y afirmaciones verificadas.
- CTA y KPI.
- Plan de medición.
- Rol de la URL en el ecosistema: agrupador o página específica, y a qué agrupador pertenece.
- Ficha de entidad e identificadores (`sameAs`, Wikidata si aplica, perfiles de autor).
- Autoría real, con credenciales y perfil verificable.
- Formatos complementarios previstos (video, audio, PDF) y su enlace de vuelta.
- Estado de evidencia de cada afirmación: dato propio, fuente primaria, estudio de terceros o hipótesis.

Leer [on-page-metadata-and-urls.md](references/on-page-metadata-and-urls.md), [image-seo-and-accessibility.md](references/image-seo-and-accessibility.md) y [structured-data-and-search-features.md](references/structured-data-and-search-features.md).

### 7. Medir y decidir

Relacionar:

```text
Search Console: visibilidad, consultas, páginas, CTR, posición e indexación
GA4: sesiones, interacción, eventos y conversiones
Clarity u otra evidencia UX: scroll, clics y fricciones
Negocio: leads, ventas, calidad y valor
```

Comparar periodos equivalentes, estacionalidad, despliegues y actualizaciones conocidas. No concluir con muestras insuficientes.

Leer [analytics-search-console-and-decisions.md](references/analytics-search-console-and-decisions.md) y [conversion-and-content-performance.md](references/conversion-and-content-performance.md).

### 8. Control de calidad

Ejecutar cinco pasadas:

1. Semántica.
2. Referencial.
3. Léxica.
4. Estilística.
5. Pragmática y SEO.

Usar `scripts/editorial_lint.py` como detector, no como sustituto del juicio editorial. Leer [editorial-quality-gates.md](references/editorial-quality-gates.md).

## Aprendizaje y actualización

### Aprendizaje durante el trabajo

Cuando un proyecto produzca una observación reutilizable:

1. Registrar el contexto, evidencia, resultado, límites y fecha.
2. Guardarla como `candidata`, no como regla.
3. Evitar información sensible, credenciales o datos personales.
4. Promoverla solo después de repetición, contraste o validación.

Para dejarla como candidata en la memoria (carpeta `memoria/aprendizaje/inbox/` de la skill, o la bóveda si está configurada), ejecutar:

```bash
python scripts/capture_learning.py --title "Título" --summary "Hallazgo" \
  --evidence "Evidencia" --status candidate
```

Funciona sin bóveda. Para los casos terminados se usa además `tools/log_job.py` (Paso final del protocolo). Los casos se nombran solo con código (`caso-<tipo>-<NN>`); el script se niega a escribir en el repo si el texto contiene un término de la lista privada del usuario.

### Investigación periódica

Ejecutar `scripts/research_update.py` para revisar las fuentes configuradas y crear un informe fechado (en `memoria/novedades/` o en la bóveda si está configurada). El script recopila cambios; el agente debe verificar el contenido antes de modificar recomendaciones.

Leer [update-governance-and-research.md](references/update-governance-and-research.md). Instalar la periodicidad con `scripts/scheduler.py` únicamente cuando el usuario lo solicite y después de confirmar rutas.

## Memoria: repo primero, Obsidian opcional

La memoria de largo plazo vive en el repo (HANDOFF/HANDSHAKE y la carpeta `memoria/` de esta skill). Obsidian es un complemento opcional para quien ya lo usa:

| Qué | Dentro del repo (siempre) | En la bóveda (solo si está configurada) |
|---|---|---|
| Aprendizajes sin validar | `memoria/aprendizaje/inbox/` | `06_Aprendizaje/Inbox/` |
| Decisiones aprobadas | `memoria/decisiones/` y HANDOFF §3 | `06_Aprendizaje/Decisiones/` |
| Reportes de novedades | `memoria/novedades/` | `02_Investigacion/Novedades/` |
| Fuentes evaluadas | `memoria/fuentes/` | `08_Fuentes/` |
| Casos terminados | HANDOFF §4 (registro de trabajos) | `09_Proyectos/` o la carpeta de proyectos del usuario |

No cargar toda la memoria en cada tarea. Buscar por tema y leer solo notas pertinentes. Detalle en [memory-integration.md](references/memory-integration.md).

## Sub-skill: implementación web en el constructor de GoHighLevel

`web-go-high-level-ia` es sub-skill propia de esta skill (y de `direct-visual-design`) para todo SEO que se **implementa dentro del constructor de IA de GoHighLevel** (AI Studio, TanStack Start): `head()` por ruta (title, description, canonical, og:*, schema JSON-LD), un solo `h1`, `noindex` mientras una página sea provisional, enlazado interno con `<Link>`, `alt` + `width/height` en imágenes (el CDN de Medios **renombra los archivos**: el nombre del archivo servido no aporta señal), `og:image` absoluta, medición por `data-track`. Esta skill decide **qué se escribe y se indexa**; `web-go-high-level-ia` decide **cómo se construye y transfiere** (ver su `references/06-seo-en-ghl-ai-studio.md`). Cuando el trabajo SEO vaya a vivir en una web de GHL AI Studio, cargar también esa skill. Vive en este mismo repo: `skills/web-go-high-level-ia/`.

## Sub-skill de apoyo: entender competidores y referencias

`rea-reverse-engineer` es skill propia de **apoyo** (decisión del usuario, 2026-10-15) para **entender cómo está construida** una página de referencia o de un competidor: outline H1–H3, title/meta/canonical/hreflang, tipos de JSON-LD, enlaces, imágenes, **HTML crudo frente a renderizado** (qué entiende un rastreador sin JS), peso, terceros y tecnología. Se llama por porción (contrato en su `SKILL.md`), nivel N1 (`scripts/web_probe.py`, sin instalar nada) y devuelve una ficha con observado/inferido/desconocido. No sustituye a `screaming-frog-seo` (rastreo de sitio; skill opcional, no incluida en gui-skills) ni a las fuentes primarias, y **una correlación con una página no se convierte en regla**: los candidatos van a `memoria/aprendizaje/inbox/` (o `06_Aprendizaje/Inbox/` si usas Obsidian). Vive en este mismo repo: `skills/rea-reverse-engineer/`.

## Compatibilidad

El formato `SKILL.md` es común. La instalación en Claude Code la hace el instalador del repo (`tools/install.ps1` / `tools/install.sh`, por enlaces). Para Codex o Antigravity y para la versión sin sistema de archivos (`skills/seo-content-system-web-hosted/`, generada con `tools/build_hosted.py`), consultar [platform-installation-and-sync.md](references/platform-installation-and-sync.md).

## Referencias por especialidad

- SEO técnico: [technical-seo-and-indexability.md](references/technical-seo-and-indexability.md)
- Lineamientos generales de SEO técnico, indexación y resultados enriquecidos (checklist universal aportada por el usuario): [technical-seo-lineamientos-generales.md](references/technical-seo-lineamientos-generales.md)
- Datos reales de crawl (rastreo, códigos de respuesta, canonicals, enlaces, duplicados, etc.): si tienes la skill **screaming-frog-seo** (opcional; no viene en gui-skills) con su MCP, úsala en lugar de estimar estos datos; si no, pide una exportación CSV/XLSX del rastreo. Aplica al modo `technical`/`audit`, y también al inventario de URLs dentro de `keyword-research` (ver [keyword-research-ia-local-desktop.md](references/keyword-research-ia-local-desktop.md#screaming-frog-en-esta-ruta)) y al mapa temático (asignar URLs existentes en [topical-map-and-content-architecture.md](references/topical-map-and-content-architecture.md)) cuando esa skill y su MCP local estén disponibles.
- Mapa temático y arquitectura de contenido a nivel de sitio: [topical-map-and-content-architecture.md](references/topical-map-and-content-architecture.md)
- Automatización de keywords de oportunidad con IA + Search Console + CMS: [ai-assisted-search-console-workflow.md](references/ai-assisted-search-console-workflow.md)
- Keyword research asistido por IA, entorno local/desktop (Claude Code, Claude Desktop, Codex CLI/IDE, MCP local): [keyword-research-ia-local-desktop.md](references/keyword-research-ia-local-desktop.md)
- Keyword research asistido por IA, entorno alojado (ChatGPT.com, Claude.ai, conectores remotos): [keyword-research-ia-web-hosted.md](references/keyword-research-ia-web-hosted.md)
- Cada cuánto repetir el keyword research y qué eventos adelantan una revisión: [keyword-research-cadence-and-triggers.md](references/keyword-research-cadence-and-triggers.md)
- SEO local y programático: [programmatic-and-local-seo.md](references/programmatic-and-local-seo.md)
- Social SEO: [social-search-and-copywriting.md](references/social-search-and-copywriting.md)
- Evidencia: [source-verification-and-evidence.md](references/source-verification-and-evidence.md)
- Registro oficial: [official-source-register.md](references/official-source-register.md)

### GEO y visibilidad ante inteligencia artificial

- Citación en IA, agrupadores y lenguaje natural vs. optimizado (experimento Los Creativos, 90 días): [ai-citation-and-geo-playbook.md](references/ai-citation-and-geo-playbook.md)
- Entidad, grafo de conocimiento, Wikidata y tripletas semánticas: [entity-presence-and-knowledge-graph.md](references/entity-presence-and-knowledge-graph.md)
- Metodología de Densidad de Señales: taxonomía de señales, KPI (Beta) y roadmap 30-60-90 (framework propio Los Creativos): [signal-density-methodology-and-kpi.md](references/signal-density-methodology-and-kpi.md)
- Schema markup priorizado para citación en IA (JSON-LD, seis tipos clave, `@graph`, FAQPage/HowTo tras el retiro de sus rich results): [schema-markup-for-ai-citation.md](references/schema-markup-for-ai-citation.md)
- Acceso de bots de IA: robots.txt, `llms.txt` y verificación (entrenamiento vs. recuperación): [ai-crawler-access-and-llms-txt.md](references/ai-crawler-access-and-llms-txt.md)
- Diversificación de canales y SEO en YouTube: [channel-diversification-and-youtube-seo.md](references/channel-diversification-and-youtube-seo.md)
- Búsqueda en comunidades (Reddit y Quora, enfoque LATAM): [community-search-reddit-quora.md](references/community-search-reddit-quora.md)
- Patrón editorial de artículo largo con autoridad (modelo Los Creativos): [editorial-pattern-long-form.md](references/editorial-pattern-long-form.md)
## Obsidian (opcional)

Si el usuario tiene una bóveda de Obsidian configurada (`obsidian_vault` y, opcionalmente, `obsidian_projects_folder` y `obsidian_registry_note` en `~/.gui-skills/config.json`), usarla además de la memoria del repo antes, durante y después de escribir, planificar, auditar u optimizar contenido. Sin bóveda, nada de esto aplica y la skill funciona igual.

### Antes de escribir o planificar contenido

1. Revisar si existe nota madre del proyecto en la carpeta de proyectos de la bóveda; si no existe y el trabajo ya tiene entidad de proyecto, crearla desde la plantilla de proyecto del usuario.
2. Consultar el contexto relevante en la carpeta de esta skill en la bóveda (ver [memory-integration.md](references/memory-integration.md)).
3. Revisar fuentes y decisiones aplicables antes de afirmar datos, estrategia o reglas SEO.

### Durante el trabajo

- Guardar briefs, paquetes SEO, decisiones editoriales, fuentes y entregables en la carpeta propia del proyecto del usuario y enlazarlos desde la nota madre.
- Usar `06_Aprendizaje/` para aprendizajes y `08_Fuentes/` para fuentes.

### Después de aprobaciones o resultados

- Si el aprendizaje es puntual, dejarlo en el proyecto.
- Si es reusable pero no validado, guardarlo como candidato (`capture_learning.py`).
- Si está validado, repetido, medido, documentado o aprobado, registrar la decisión antes de promoverlo.

La instrucción actual del usuario, el brief activo, datos propios y fuentes primarias tienen prioridad sobre memoria previa o heurísticas.
