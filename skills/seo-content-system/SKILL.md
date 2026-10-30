---
name: seo-content-system
description: Investiga, planifica, redacta, optimiza, audita, mide y actualiza contenido para SEO, AEO, GEO, búsqueda social, SEO local y SEO programático. Usar cuando el agente deba trabajar con intención de búsqueda, customer journey, keywords, arquitectura de contenidos, briefs, artículos, landing pages, metatítulos, metadescripciones, slugs, imágenes, enlazado interno, schema, GA4, Search Console, Clarity, fuentes, contenido natural en español, medición posterior o novedades de buscadores. Usar también para visibilidad y citación ante inteligencia artificial (GEO, LLMs, ChatGPT, Copilot, Perplexity, Gemini), páginas agrupadoras, entidades y grafos de conocimiento (Wikidata, sameAs, tripletas semánticas), diversificación de canales, SEO en YouTube y presencia en comunidades como Reddit o Quora. Antes de producir cualquier salida lee la memoria de la skill (HANDSHAKE/HANDOFF del repo gui-skills y, si el usuario usa Obsidian, su bóveda) y registra aprendizajes sin volver reglas lo no verificado.
---

# SEO Content System

> Versión 1.7.0 (sobre la 1.6.0: **metodología de SEO Skills integrada**, marcada **[SEO Skills 2026-10]**: auditoría con puntuación, robots.txt (RFC 9309 y 22 bots), HTML renderizado, procedimiento para title y metadescripción, umbrales de imágenes, auditoría del grafo de enlaces y mapa de clústeres frente al sitio; corrige además el ejemplo de `Allow: /` por bot de IA; ver `docs/CAMBIOS.md`). En la 1.6.0 (sobre la 1.5.0: **puerta SEO para sitios de servicios y páginas nuevas**, marcada **[Auditoría 2026-10]**, derivada de una auditoría real: principios 23 a 27, modo `gate`, referencia `service-site-seo-gate.md` y script `site_seo_gate.py`; ver `docs/CAMBIOS.md`). En la 1.5.0 (sobre la 1.4.0: segunda pasada por ClickUp, Obsidian y Drive, marcada **[ClickUp 2]**: contrato por fases y control de alcance, lanzamiento de sitio nuevo, e-commerce multipaís, SEO de oferta académica, trampas de medición y diagnóstico de caídas, criterio de hecho por hallazgo; ver `docs/CAMBIOS.md`). En la 1.4.0: higiene de archivos, retiro de datos, schema con Rank Math y sin precio, riesgo de ajustes globales, matriz con brief por hallazgo, YMYL. En la 1.3.0, Las marcas **[ClickUp]**, **[Obsidian]**, **[Sheets]** y **[Drive]** señalan lo que se añadió sobre la 1.2.0, a partir de la metodología interna de la agencia (anonimizada), de la bóveda del usuario, de 18 libros de Google Sheets del equipo y de Docs, Slides y .xlsx de su Drive (solo estructura). Todo lo que no lleva marca sigue igual. Detalle en [`docs/CAMBIOS.md`](docs/CAMBIOS.md).

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
   (3) publica con `python <repo>/tools/publish_job.py --tema <caso-o-tema>` (rama + push + PR; si eres el
   mantenedor, tu aporte se integra solo); (4) dile al usuario el resultado (`PR_CREADO <url>` / `PUBLICADO <url>` /
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
14. **[ClickUp]** No tocar el sitio en vivo (publicar, redirigir, cambiar robots, noindex, sitemap, plantillas o GBP) sin **aprobación escrita** del responsable o del cliente. Hasta tenerla, se entrega una propuesta.
15. **[ClickUp]** Cada hallazgo es una unidad de trabajo con origen, prioridad, número de URLs afectadas, qué se espera, criterio de hecho y responsable (o "por definir"). Ver [technical-audit-by-finding.md](references/technical-audit-by-finding.md).
16. **[ClickUp]** Priorizar las ganancias tempranas: primero lo que se corrige sin crear páginas nuevas, después lo que requiere desarrollo o contenido nuevo.
17. **[ClickUp]** Los KPI son parámetros de gestión, no garantías. Toda solicitud se compara con el alcance acordado y, si no está cubierta, se marca *fuera de alcance* antes de ejecutarla.
18. Cuando se retira un dato (precios, una plataforma, un producto, una sede, una cifra), buscarlo en **todos** los entregables y en el sitio: textos, titles y metas, schema, alt, FAQs, `llms.txt`, plantillas, CSV de seguimiento y briefs. El criterio de hecho incluye esa búsqueda con 0 resultados.
19. Los productos o funciones del roadmap solo aparecen como «próximamente»: sin fecha (salvo aprobación escrita), sin precio, sin CTA de compra, sin schema de producto u oferta y sin FAQs que los den por disponibles.
20. En schema, nunca marcadores (`[PENDIENTE]`, `TBD`, `XXX`) dentro de un campo: si el dato no existe, se omite el campo. Producto sin precio público: solo `SoftwareApplication`, nunca `Offer` vacío ni `price` 0. Si Rank Math (o Yoast) ya genera `#organization`/`#website`/`#webpage`, no duplicarlos con bloques manuales. Ver [schema-markup-for-ai-citation.md](references/schema-markup-for-ai-citation.md).
21. **[ClickUp 2]** Medir, no estimar: en Search Console las dimensiones `page` y `query` no son comparables (calcular el % anonimizado), se mide la **distribución** del enlazado y no la media, y una caída de tráfico no se atribuye a una actualización sin descartar medición, estacionalidad y cambios propios. Ver [measurement-traps-and-diagnosis.md](references/measurement-traps-and-diagnosis.md).
22. **[ClickUp 2]** Todo hallazgo y toda tarea llevan **criterio de hecho verificable** y se cierran con una re-medición o re-auditoría; el estado «en revisión» no equivale a hecho. Nunca inflar horas, cifras ni resultados en un informe: se reporta el tiempo real.
23. **[Auditoría 2026-10]** Se nombra cada página por **cómo se busca**, no por cómo la llama el negocio. El menú puede conservar la palabra de la oferta; el título SEO y el H1 siguen la búsqueda. Sin datos de demanda se escribe «sin datos»: no se inventa un volumen. Ver [service-site-seo-gate.md](references/service-site-seo-gate.md).
24. **[Auditoría 2026-10]** Una **frase raíz** y una **intención** por URL. La unicidad de la keyword como cadena exacta **no detecta canibalización** (tres páginas con «diseño web» en el título pasan ese linter). Artículo y servicio no atacan la misma intención: el artículo toma la informativa y enlaza al servicio con anchor descriptivo en el primer tercio. Dos servicios casi iguales se fusionan o se diferencian: decisión del dueño.
25. **[Auditoría 2026-10]** Un servicio no se publica sin su **estructura mínima** (problema, para quién y para quién no, qué incluye y qué no, proceso, plazos, precio o rango, objeciones) y sin **al menos un caso propio** de ese servicio. Una página de servicio más delgada que el artículo que la rodea pierde la búsqueda comercial. Nunca se rellena: lo que no se sabe se pide al dueño.
26. **[Auditoría 2026-10]** El **host canónico se resuelve en el servidor**: las cuatro variantes (`http`/`https` × con/sin `www`) terminan en **un solo salto 301**, con ruta y consulta conservadas. La etiqueta `canonical` mitiga, no sustituye. Se verifica en vivo con `scripts/site_seo_gate.py --live`.
27. **[Auditoría 2026-10]** Antes de escribir «no hay datos» se prueban **todas** las rutas de acceso disponibles (cuenta del dueño, cuenta de servicio, exportaciones). La indexación no se infiere con `site:` en un buscador que no es Google. Todo cambio de título en una URL indexada lleva fecha, línea base y medición a los 14 y 28 días.

## Flujo maestro

### 0. Situar la tarea en la fase del servicio [ClickUp]

Fases: Fase inicial (onboarding, accesos, auditoría, KWR, competidores, OKR, roadmap) → Operación mensual (sprints, contenido, correcciones, informe) → Expansión o mercados → Dependencias del cliente → Control de alcance. Para sitios nuevos o rediseños por etapas, usar GDD (Estrategia → Launchpad de PAI → Mejoras continuas). Leer [agency-operating-methodology.md](references/agency-operating-methodology.md), [onboarding-and-initial-audit.md](references/onboarding-and-initial-audit.md) y [growth-driven-design-gdd.md](references/growth-driven-design-gdd.md).

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
- `onboarding` **[ClickUp]**: kickoff, auditoría inicial en 3 pasos, cuatro tipos de KWR, competidores en 7 pasos y OKR. Ver [onboarding-and-initial-audit.md](references/onboarding-and-initial-audit.md).
- `audit` **[ClickUp]**: auditoría técnica por hallazgo, con matriz de entendimiento. Ver [technical-audit-by-finding.md](references/technical-audit-by-finding.md), [wordpress-technical-audit-checklist.md](references/wordpress-technical-audit-checklist.md) y la plantilla [audit-understanding-matrix.md](assets/templates/audit-understanding-matrix.md).
- `gate` **[Auditoría 2026-10]**: puerta SEO para sitios de servicios y páginas nuevas (nombre por búsqueda, frase raíz e intención únicas, estructura mínima del servicio, caso propio, host canónico, lang/hreflang, alt, medición). Ver [service-site-seo-gate.md](references/service-site-seo-gate.md) y `scripts/site_seo_gate.py`.
- `migration` **[ClickUp]**: comparar desarrollo con producción, plan de redirecciones, reporte post-migración, mapa de 404 y validación de implementaciones. Ver [migration-redirects-and-validation.md](references/migration-redirects-and-validation.md).
- `deindex` **[ClickUp]**: retirada controlada del índice con `X-Robots-Tag`. Ver [deindexing-procedure.md](references/deindexing-procedure.md).
- `report` **[ClickUp]** (submodo de `measure`): informe mensual o trimestral antes/después. Plantilla: [seo-report.md](assets/templates/seo-report.md).

### 2. Establecer evidencia disponible

Declarar cuál escenario aplica:

- Acceso directo a datos o conectores.
- Archivos exportados, capturas o reportes.
- Investigación web verificable.
- Información aportada por el usuario.
- Proyecto nuevo sin datos propios.

Antes de pedir datos al usuario, agotar lo disponible: la carpeta del proyecto completa (briefs, entregables previos, CSV, exportaciones, `AGENTS.md`/README, actas) y el sitio público (home, servicios, legales, footer, schema y `sameAs` actuales, sitemap, robots, `llms.txt`). Preguntar solo lo que no se encontró, en una sola lista y diciendo dónde se buscó; si aun así falta información crítica, avanzar con supuestos etiquetados.

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

Leer [on-page-metadata-and-urls.md](references/on-page-metadata-and-urls.md), [title-and-description-generation.md](references/title-and-description-generation.md) **[SEO Skills 2026-10]** (cómo producir title y metadescripción), [image-seo-and-accessibility.md](references/image-seo-and-accessibility.md) y [structured-data-and-search-features.md](references/structured-data-and-search-features.md).

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

**[ClickUp]** Cada informe compara el antes y el después de cada implementación (con su fecha de despliegue) y cuenta cuántos artículos están publicados, cuántos en el sitemap y cuántos indexados. Hay que avisar de que la indexación puede tardar de 2 a 3 meses. El dashboard mínimo tiene tres secciones: adquisición e interacción (GA4), visibilidad (impresiones, posición, keywords en GSC) y salud del sitio (Core Web Vitals). Plantilla: [seo-report.md](assets/templates/seo-report.md).

### 8. Control de calidad

Ejecutar cinco pasadas:

1. Semántica.
2. Referencial.
3. Léxica.
4. Estilística.
5. Pragmática y SEO.

Usar `scripts/editorial_lint.py` como detector, no como sustituto del juicio editorial.

**[Auditoría 2026-10] Sitios de servicios y páginas nuevas:** antes de publicar, ejecutar `python scripts/site_seo_gate.py <build> --ignorar "<país>,<marca>"` (candidatos a canibalización por frase raíz, aperturas casi iguales, servicios delgados, `lang`/`hreflang`, `alt`, menú sin listas) y `python scripts/site_seo_gate.py --live https://<dominio> --ruta blog/` (las cuatro variantes del host). Los avisos son **candidatos** que se confirman con Search Console; los fallos bloquean. Checklist de 10 puntos en [service-site-seo-gate.md](references/service-site-seo-gate.md). Leer [editorial-quality-gates.md](references/editorial-quality-gates.md).

**Puerta anti-slop (obligatoria antes de entregar o publicar contenido hecho o asistido con IA):** pasar la skill `contenido-sin-slop` (propósito para el lector, sustancia propia, procedencia y revisión humana, nada inventado; su detector `slop_lint.py` solo como ayuda). Si la pieza no pasa, se reescribe con sustancia o se descarta; no se rellena un calendario con contenido genérico.

**Reglas de redacción de artículos de blog (pedidas por el usuario el 2026-10-26):** leer [blog-article-writing-rules.md](references/blog-article-writing-rules.md) antes de escribir o mejorar un artículo. En corto: comillas rectas dobles; título con número real y año cuando el contenido es una lista; un dato verificado con fuente por cada consejo (nunca inventado); un solo bloque JSON-LD con `@graph` y `@id`; foco local con ciudades e industrias reales; estructura escaneable (tabla resumen y tabla de datos con fuente); voces reales citadas con nombre, cargo y enlace (solo con permiso y frase textual); y 2 o 3 citas cortas de libros consultados de forma legítima, con su fuente completa.

Higiene de archivos (sección 8 de editorial-quality-gates): en PowerShell no escribir Markdown, HTML ni JSON con cadenas o here-strings de comillas dobles; usar Python o `[IO.File]::WriteAllText` con UTF-8 sin BOM, y validar que no haya bytes NUL antes de entregar.

Temas YMYL (finanzas, trading, salud): no prometer ganancias ni resultados y poner avisos de riesgo visibles (sección 10 de editorial-quality-gates).

**[ClickUp]** Revisión de compliance: quitar promesas que la marca no puede sostener (resultados, salarios, garantías) y términos rebuscados o en inglés que no aporten. Cada landing debe tener enlaces al home y a uno o dos servicios relacionados, y FAQs basadas en experiencia real o en consultas de GSC.

### 9. Entregar como tarea [ClickUp]

Toda acción que pase a otra persona se redacta con [task-brief.md](assets/templates/task-brief.md): Contexto/Origen · Qué se espera · Qué NO hacer · Criterio de hecho · Cómo entregar · Qué necesitamos del cliente · Esfuerzo/Impacto · Responsable. La estructura de tarea madre (entregable) con subtareas (trabajo, QA y "Ajustes · Ronda N"), los estados y los niveles de servicio están en [clickup-task-operating-model.md](references/clickup-task-operating-model.md). La skill redacta las tareas, pero **no las crea ni las mueve** en el gestor de proyectos sin una instrucción explícita.

### Link building, local y programático [ClickUp]

- **PR/backlinks:** a partir de cada nota de prensa sobre la marca, un artículo resumen de 600–800 palabras en estilo periodístico. Nombra el medio, explica por qué hablan de la marca y qué impacto tiene, y enlaza al home, a la nota original y a uno o dos servicios. Después, una versión de 400–500 palabras para el newsletter de LinkedIn y una actualización en GBP.
- **Local:** ficha de GBP por país o sede (nombre correcto, fotos, ciudades de cobertura enlazadas a landings geolocalizadas) y publicaciones periódicas.
- **Programático:** plantilla → contenido → diseño → despliegue → canonical → solicitud de indexación → medición. No se construye hasta que el cliente apruebe la visual.

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

`web-go-high-level-ia` es sub-skill propia de esta skill (y de `direct-visual-design`) para todo SEO que se **implementa dentro del constructor de IA de GoHighLevel** (AI Studio, TanStack Start): `head()` por ruta (title, description, canonical, og:*, schema JSON-LD), un solo `h1`, `noindex` mientras una página sea provisional, enlazado interno con `<Link>`, `alt` + `width/height` en imágenes (el CDN de Medios **renombra los archivos**: el nombre del archivo servido no aporta señal), `og:image` absoluta, medición por `data-track`. Esta skill decide **qué se escribe y se indexa**; `web-go-high-level-ia` decide **cómo se construye y transfiere** (ver `references/06-seo-en-ghl-ai-studio.md` de la skill externa `web-go-high-level-ia`). Cuando el trabajo SEO vaya a vivir en una web de GHL AI Studio, cargar también esa skill. Vive en este mismo repo: `skills/web-go-high-level-ia/`.

## Sub-skill de apoyo: entender competidores y referencias

`rea-reverse-engineer` es skill propia de **apoyo** (decisión del usuario, 2026-10-15) para **entender cómo está construida** una página de referencia o de un competidor: outline H1–H3, title/meta/canonical/hreflang, tipos de JSON-LD, enlaces, imágenes, **HTML crudo frente a renderizado** (qué entiende un rastreador sin JS), peso, terceros y tecnología. Se llama por porción (contrato en su `SKILL.md`), nivel N1 (`scripts/web_probe.py` de la skill externa `rea-reverse-engineer`, sin instalar nada) y devuelve una ficha con observado/inferido/desconocido. No sustituye a `screaming-frog-seo` (rastreo de sitio; skill opcional, no incluida en gui-skills) ni a las fuentes primarias, y **una correlación con una página no se convierte en regla**: los candidatos van a `memoria/aprendizaje/inbox/` (o `06_Aprendizaje/Inbox/` si usas Obsidian). Vive en este mismo repo: `skills/rea-reverse-engineer/`.

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

### Operación de agencia [ClickUp]

- Metodología operativa (fases, cadencia, contenido, link building, roles, migración): [agency-operating-methodology.md](references/agency-operating-methodology.md)
- Onboarding, auditoría inicial, KWR y competidores: [onboarding-and-initial-audit.md](references/onboarding-and-initial-audit.md)
- Growth-Driven Design (PAI/PMI/PBI y dashboard): [growth-driven-design-gdd.md](references/growth-driven-design-gdd.md)
- Modelo de tareas, estados, campos y alcance: [clickup-task-operating-model.md](references/clickup-task-operating-model.md)
- Auditoría técnica por hallazgo: [technical-audit-by-finding.md](references/technical-audit-by-finding.md)
- **[SEO Skills 2026-10]** Auditoría general con categorías, pesos y puntuación: [audit-scoring-and-weights.md](references/audit-scoring-and-weights.md)
- **[SEO Skills 2026-10]** robots.txt (auditar, validar, generar; RFC 9309; bots de referencia): [robots-txt-audit-and-generation.md](references/robots-txt-audit-and-generation.md)
- **[SEO Skills 2026-10]** Rastreo con HTML renderizado para sitios con JavaScript: [rendered-html-crawl.md](references/rendered-html-crawl.md)
- **[Auditoría 2026-10]** Puerta SEO para sitios de servicios y páginas nuevas (ocho causas raíz, spam de enlaces, checklist de 10 puntos): [service-site-seo-gate.md](references/service-site-seo-gate.md); script `scripts/site_seo_gate.py` con sus pruebas `scripts/test_site_seo_gate.py`.
- Checklist WordPress + servidor: [wordpress-technical-audit-checklist.md](references/wordpress-technical-audit-checklist.md)
- Migración, redirecciones y validación: [migration-redirects-and-validation.md](references/migration-redirects-and-validation.md)
- Desindexación controlada: [deindexing-procedure.md](references/deindexing-procedure.md)
- **[ClickUp 2]** Contrato por fases, campos de alcance, bolsa, solicitudes y higiene de tareas: [contract-phases-and-scope-control.md](references/contract-phases-and-scope-control.md)
- **[ClickUp 2]** Lanzamiento de un sitio nuevo (React/SPA, MVP estático, auditoría en stage, plan de medición): [launch-checklist-new-site.md](references/launch-checklist-new-site.md)
- **[ClickUp 2]** E-commerce multipaís (hallazgos de Shopify, programático, FAQ de producto, plan de rendimiento): [ecommerce-seo-multicountry.md](references/ecommerce-seo-multicountry.md)
- **[ClickUp 2]** Oferta académica (programa como unidad, ficha de acción, schema, QA, rediseño): [education-program-seo.md](references/education-program-seo.md)
- **[ClickUp 2]** Trampas de medición, enlazado, diagnóstico de caídas, priorización y regla de bloqueo: [measurement-traps-and-diagnosis.md](references/measurement-traps-and-diagnosis.md)
- Plantillas: [task-brief.md](assets/templates/task-brief.md), [seo-report.md](assets/templates/seo-report.md), [audit-understanding-matrix.md](assets/templates/audit-understanding-matrix.md)

#### Plantillas de hoja de cálculo [Sheets]
Reconstruidas de 18 libros reales del equipo (solo estructura). Detalle en `references/sheets-workbook-templates.md`.
- Auditoría: `assets/templates/audit-findings-matrix.csv` (matriz maestra *Nombre del problema · Tipo · Prioridad · Área · Status · N.º URLs · % · Descripción · Cómo solucionar · Pestaña · Validación*) + `assets/templates/audit-finding-tab.csv` (una pestaña por hallazgo con propuesta, `=LEN()` e Implementado).
- Vocabularios: Tipo `Problema/Aviso/Oportunidad`; Prioridad `Alta/Media/Baja`; Área `SEO/Front/Cliente/QA/UX`; Status `Pendiente → En implementación → Realizado` (`Cliente` = bloqueado por el cliente).
- Migración: `assets/templates/migration-checklist.csv`, `assets/templates/redirect-map.csv`, `assets/templates/404-triage.csv`.
- Contenido: `assets/templates/keyword-content-calendar.csv`, `assets/templates/keyword-research-terms.csv`, `assets/templates/content-architecture-map.csv`.
- Gestión: `assets/templates/seo-work-plan.csv`, `assets/templates/pending-tracker.csv`, `assets/templates/implementation-tracker.csv`, `assets/templates/traffic-opportunity-model.csv`.
- Regla: nunca escribir ni copiar credenciales en hojas de insumos; solo "acceso concedido sí/no".

#### Entregables y lineamientos de Drive [Drive]
Reconstruidos de Docs, Slides y .xlsx del equipo (solo estructura). Detalle en `references/drive-deliverables-and-guidelines.md`.
- Informe mensual: `assets/templates/seo-performance-report-deck.md` (GSC + GA4 por propiedad, top 10 páginas, consultas de marca y sin marca, blog y conclusiones con titular-conclusión).
- Reuniones: `assets/templates/audit-review-minutes.md`, `assets/templates/sprint-meeting-memo.md`.
- Lineamientos para desarrollo: `assets/templates/technical-seo-guidelines.md`. FAQs: `assets/templates/faq-optimization-proposal.md`.
- Propuesta técnica comercial: `assets/templates/technical-proposal-deck.md` (caso de desindexación de PDFs).
- Contenido con experto: `assets/templates/sme-interview-guide.md` (5 salidas), `assets/templates/eeat-gameplan.csv`, `assets/templates/kwr-program-clusters.csv`.
- Local: `assets/templates/gbp-audit.csv`.

#### Plantillas de la segunda pasada [ClickUp 2] [Sheets 2]
Solo estructura; detalle en `references/sheets-workbook-templates.md` §10 y `references/drive-deliverables-and-guidelines.md` §12.
- GDD y lanzamiento: `assets/templates/gdd-task-brief.md`, `assets/templates/gdd-time-estimates.csv`, `assets/templates/client-content-review-checklist.md`, `assets/templates/pre-launch-audit-checklist.md`, `assets/templates/landing-technical-sheet.md`.
- Programático: `assets/templates/programmatic-landing-inventory.csv`, `assets/templates/programmatic-input-matrix.csv`.
- Oferta académica y producto: `assets/templates/program-approval-matrix.csv`, `assets/templates/program-data-sheet.csv`, `assets/templates/product-input-matrix.csv`, `assets/templates/consolidation-canonical-redirect.csv`.
- Enlazado, competencia y operación: `assets/templates/internal-linking-matrix.csv`, `assets/templates/competitor-matrix.csv`, `assets/templates/client-intake-matrix.csv`, `assets/templates/monthly-request-log.csv`, `assets/templates/ad-copy-by-angle.csv`.


## GEO y visibilidad ante inteligencia artificial

- Citación en IA, agrupadores y lenguaje natural vs. optimizado (experimento Los Creativos, 90 días): [ai-citation-and-geo-playbook.md](references/ai-citation-and-geo-playbook.md)
- Entidad, grafo de conocimiento, Wikidata y tripletas semánticas: [entity-presence-and-knowledge-graph.md](references/entity-presence-and-knowledge-graph.md)
- Metodología de Densidad de Señales: taxonomía de señales, KPI (Beta) y roadmap 30-60-90 (framework propio Los Creativos): [signal-density-methodology-and-kpi.md](references/signal-density-methodology-and-kpi.md)
- Schema markup priorizado para citación en IA (JSON-LD, seis tipos clave, `@graph`, FAQPage/HowTo tras el retiro de sus rich results): [schema-markup-for-ai-citation.md](references/schema-markup-for-ai-citation.md)
- Acceso de bots de IA: robots.txt, `llms.txt` y verificación (entrenamiento vs. recuperación): [ai-crawler-access-and-llms-txt.md](references/ai-crawler-access-and-llms-txt.md)
- Diversificación de canales y SEO en YouTube: [channel-diversification-and-youtube-seo.md](references/channel-diversification-and-youtube-seo.md)
- Búsqueda en comunidades (Reddit y Quora, enfoque LATAM): [community-search-reddit-quora.md](references/community-search-reddit-quora.md)
- Patrón editorial de artículo largo con autoridad (modelo Los Creativos): [editorial-pattern-long-form.md](references/editorial-pattern-long-form.md)
## Obsidian (opcional)

**[Obsidian]** En la bóveda del usuario, la carpeta de esta skill sigue la estructura `00_Inicio`, `01_Conocimiento`, `02_Investigacion`, `03_Estrategia` (modelo de priorización), `04_Produccion` (flujo editorial y checklist de publicación), `05_Medicion` (diagnóstico de caídas), `06_Aprendizaje`, `08_Fuentes` y `09_Proyectos`. Hay además una nota *Puente SEO contenido y diseño*: cuando el trabajo incluya landings, UI copy, imágenes, piezas sociales o conversión, se carga también `direct-visual-design`. Las fuentes guardadas en `08_Fuentes` llevan **jerarquía de evidencia** (dato editorial de agencia frente a hecho confirmado con fuente primaria); hay que respetarla al citar.

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
