# HANDOFF — seo-content-system

> Traspaso entre sesiones y personas: qué es la skill, cómo se instala, qué se decidió y qué se aprendió
> en cada trabajo. Estado vivo (versión, herramientas, pendientes) → `HANDSHAKE.md`.

## 1. Qué es y cuándo se usa

Sistema editorial y de medición para SEO, AEO y GEO: investigación de demanda, estrategia y arquitectura,
briefs, redacción, on-page, técnico, local, programático, búsqueda social, entidad, medición y
actualización. Se usa **antes** de escribir, planificar, auditar u optimizar cualquier contenido.

Relación con otras skills del repo:

- **`web-go-high-level-ia`** es su sub-skill para el SEO que se implementa dentro del constructor de IA de
  GoHighLevel (esta skill decide qué se escribe y se indexa; aquella, cómo se construye y se transfiere).
- **`rea-reverse-engineer`** es skill de apoyo: entiende cómo está construida una página de referencia o de un
  competidor (HTML crudo frente a renderizado, schema, outline). Se llama por porción.
- **`direct-visual-design`** fija la dirección visual; esta skill, lo que se escribe y se indexa en cada página.
- **`seo-content-system-web-hosted`** es una **versión generada** de esta skill para Claude.ai / ChatGPT sin
  sistema de archivos (`tools/build_hosted.py`); nunca se edita a mano.
- `screaming-frog-seo` (skill externa, opcional, **no incluida en gui-skills**): si la tienes con su MCP, es la
  fuente de datos reales de crawl para los modos `technical`/`audit`; si no, se pide una exportación CSV/XLSX.

## 2. Instalación y dependencias

- Viene con el repo gui-skills (`tools/install.ps1` / `tools/install.sh`); no se copia a mano. `scripts/install.py`
  es solo un ayudante para Codex / Antigravity / instalaciones por proyecto (enlaces desde el repo).
- Python 3.9 o superior, solo biblioteca estándar. Sin red, `research_update.py` informa el error de cada
  fuente y sigue.
- **Obsidian es opcional.** Si se usa: clave `obsidian_vault` (y opcionalmente `obsidian_seo_folder`,
  `obsidian_projects_folder`, `obsidian_registry_note`) en `~/.gui-skills/config.json`, o la clave heredada
  `vault` de `~/.seo-content-system.json`, o la variable `SEO_OBSIDIAN_VAULT`. Para que el agente lea y escriba
  la bóveda hace falta además el MCP de Obsidian (ver `references/platform-installation-and-sync.md`).
- Sin bóveda, la memoria vive en `memoria/` dentro de la skill y el estado del recopilador en
  `~/.gui-skills/seo-research-state.json`.
- Datos reales (Search Console, GA4, Clarity) solo si el usuario los conecta; la skill nunca finge acceso.

## 3. Decisiones vigentes

| Fecha | Decisión | Quién la aprobó | Por qué |
|---|---|---|---|
| 2026-07-23 | Separar la recopilación automática de novedades de la promoción de reglas: el script recopila, el agente verifica y solo se promueve tras repetición, contraste o validación | guille | Evitar convertir una observación o una noticia en regla; protocolo de actualización |
| 2026-07-23 | Mantener intención de búsqueda y etapa del journey como campos independientes en briefs y estrategia | guille | La intención describe la búsqueda actual; el journey, la relación con la decisión o la marca |
| 2026-07-23 | La skill es la primera capa obligatoria para todo trabajo de contenido (SEO, AEO, GEO, briefs, metadata, arquitectura, medición, actualización) | guille | Instrucción del mantenedor al montar el sistema |
| 2026-08-25 | Paso 0 obligatorio «memoria primero»: leer antes de producir cualquier salida; si no es accesible, decirlo y marcar la salida como no contrastada; nunca simular la consulta (hasta 2026-10-16 la memoria era solo la bóveda de Obsidian; hoy es HANDOFF/HANDSHAKE + `memoria/` y, opcional, la bóveda) | guille | Evitar que el modelo trabaje de memoria entrenada cuando existe contexto más actual |
| 2026-08-25 | Prohibida la ingeniería lingüística forzada dentro del texto (densidades objetivo, sinónimos inyectados, anáforas obligatorias, conectores por cuota) | guille | Experimento de 90 días de la agencia del mantenedor: lenguaje natural 118 citaciones frente a 9 del optimizado (evidencia direccional, n=2 sitios, un sector, un idioma, datos de Copilot) |
| 2026-08-25 | Preferir páginas agrupadoras por tipología frente a microURLs por keyword aislada | guille | El agrupador concentró más del 50 % de las citaciones del experimento y un caso de escala mostró magnitud parecida (dominio con autoridad previa, no replicable de inmediato) |
| 2026-08-25 | Incorporar entidad/Wikidata (con advertencia de notabilidad y sin ediciones promocionales), comunidades LATAM con identidad declarada y YouTube como superficies; añadir los modos `geo` y `entity` y distinguir entrenamiento de recuperación | guille | Cambios 3 a 7 de la actualización GEO; no asumir que Reddit/Quora son el canal principal en LATAM sin verificar |
| 2026-08-25 | Las cifras de terceros sobre Reddit, Wikipedia o YouTube se citan siempre con fuente, fecha y condición de estudio externo | guille | Son correlacionales y volátiles |
| 2026-08-25 | Sin campo `tags` en el frontmatter de `SKILL.md` | guille | El validador de skills solo admite `name`, `description`, `license`, `metadata` y `allowed-tools` |
| 2026-08-26 | Versión web hosted = 10 documentos temáticos + instrucciones de proyecto + memoria sin Obsidian, **generada por script** y regenerada ante cambios significativos; `keyword-research-ia-local-desktop.md` queda fuera por ser específico de entorno con acceso local | guille | Límites prácticos de archivos de conocimiento en Claude Projects y Custom GPT; mantener dos versiones a mano las desincroniza |
| 2026-08-26 | Puente de datos en el entorno hosted: procesos locales exportan Search Console/GA4/Bing a Google Sheets y el Project/GPT lee el Sheet por el conector de Drive | guille | Ni Claude.ai ni ChatGPT tienen conector nativo de esas fuentes |
| 2026-10-13 | `web-go-high-level-ia` es sub-skill de esta skill para el SEO dentro del constructor de IA de GoHighLevel | guille | Separar qué se escribe/indexa de cómo se construye y transfiere |
| 2026-10-15 | `rea-reverse-engineer` es skill de apoyo (llamada por porción, nivel N1 por defecto) para entender competidores y referencias; una correlación con una página no se convierte en regla | guille | Ver cómo está construido un competidor sin copiarlo |
| 2026-10-16 | El repo gui-skills es la fuente canónica; Obsidian pasa a ser opcional (Paso 0 lee HANDOFF/HANDSHAKE y `memoria/`; los scripts caen a `memoria/` si no hay bóveda); `install.py` ya no refresca desde la bóveda; `screaming-frog-seo` pasa a ser skill opcional no incluida | guille | Compartir la skill con personas que no usan Obsidian y eliminar copias desfasadas |

## 4. Registro de trabajos

> Una entrada por trabajo terminado o implementado y aprobado. Solo se agregan entradas al final; las
> correcciones van como entrada nueva. Casos solo con código `caso-<tipo>-<NN>`. Formato:
> `templates/entrada-de-trabajo.md`. Se escribe con `tools/log_job.py`.

<!-- registro:inicio -->

### 2026-07-23 · caso-mantenimiento-01 · guille

- **Qué se hizo:** Creación del sistema: skill v1.0/1.1 con modos de trabajo, 28 referencias, plantillas, scripts de aprendizaje y de investigación periódica, y la memoria viva en una bóveda de Obsidian (inicio, conocimiento, investigación, estrategia, producción, medición, aprendizaje, plantillas, fuentes, proyectos). Primer «Estado SEO» de la investigación periódica y primeras dos decisiones (recopilar vs. promover; intención y journey separados).
- **Salió bien:** Separar lo estable (procedimiento y referencias en la skill) de lo extenso (memoria fuera de la skill); la regla «el recopilador no convierte novedades en verdad».
- **Salió mal / incidencia:** Nada relevante en este alta; la dependencia total de la bóveda se resolvió después (2026-10-16).
- **Regla candidata:** ninguna
- **Herramientas:** Python 3 (biblioteca estándar), MCP de Obsidian, scheduler del sistema

### 2026-08-12 · caso-web-biotech-01 · guille

- **Qué se hizo:** El mantenedor aportó un documento marco de SEO técnico, indexación y resultados enriquecidos (URLs, hreflang, home, fichas de producto, rendimiento, schema, checklist de auditoría) y se incorporó verbatim como `references/technical-seo-lineamientos-generales.md`; su primera aplicación real fue este proyecto web.
- **Salió bien:** Conservar el documento tal cual como fuente de reglas técnicas y cruzarlo con las referencias editoriales que cubren el mismo terreno con más contexto.
- **Salió mal / incidencia:** Nada relevante.
- **Regla candidata:** ninguna
- **Herramientas:** Markdown; auditoría contra la checklist del propio documento

### 2026-08-25 · caso-mantenimiento-02 · guille

- **Qué se hizo:** Actualización GEO con siete cambios a partir del experimento de 90 días de la agencia del mantenedor (artículo público del 2026-08-24 y resumen de 15 láminas): regla «memoria primero», prohibición de la ingeniería lingüística forzada, comunidades (Reddit/Quora, LATAM), diversificación de canales y YouTube, tripletas semánticas, Wikidata y grafo de conocimiento, y agrupadores; se añadieron los modos `geo` y `entity` y las referencias `ai-citation-and-geo-playbook`, `entity-presence-and-knowledge-graph`, `channel-diversification-and-youtube-seo`, `community-search-reddit-quora` y `editorial-pattern-long-form`. Se generó además el adaptador para asistentes web (`WEB-ASSISTANT-PROMPT.md`) y el manifiesto 1.1.0.
- **Salió bien:** Editar la fuente canónica y dividir en referencias temáticas con ciclos de revisión distintos; validar la skill con el validador de skills en UTF-8.
- **Salió mal / incidencia:** (1) La copia instalada tenía la línea sobre `screaming-frog-seo` que no existía en la fuente canónica: se portó antes de refrescar para no perderla. (2) El validador de skills rechazó `tags` en el frontmatter: se retiró. (3) La copia operativa de Codex estaba retrasada respecto a la fuente: se actualizó.
- **Regla candidata:** Antes de refrescar una copia instalada, comparar contra la fuente canónica y portar lo que solo exista en la copia (hoy no aplica: la instalación es por enlaces).
- **Herramientas:** Obsidian, `quick_validate.py` de skills, instalador por copia (retirado)

### 2026-08-26 · caso-mantenimiento-03 · guille

- **Qué se hizo:** Versión web hosted: 10 documentos temáticos de conocimiento (consolidando las referencias), instrucciones de proyecto adaptadas de `SKILL.md`, archivo de memoria sin Obsidian y guía de instalación para Claude.ai (Project) y ChatGPT (Custom GPT/Project). Se definió el puente de Search Console/GA4/Bing por Google Sheets.
- **Salió bien:** Consolidar por tema (en vez de subir ~34 archivos sueltos) y generar la carpeta con un script en lugar de editarla a mano.
- **Salió mal / incidencia:** La instantánea quedó desfasada de la fuente (le faltaba la línea de `screaming-frog-seo` en `topical-map-and-content-architecture`) porque no existía un generador versionado; desde 2026-10-16 se regenera con `tools/build_hosted.py`.
- **Regla candidata:** Todo artefacto derivado se genera con script y lleva un `--check` que detecta si está desfasado.
- **Herramientas:** script de consolidación (hoy `tools/build_hosted.py`), Claude.ai Projects, ChatGPT Projects/GPTs

### 2026-08-26 · caso-mantenimiento-04 · guille

- **Qué se hizo:** Incorporación de referencias nuevas como candidatos de aprendizaje y luego como referencias: acceso de bots de IA (entrenamiento frente a recuperación, `robots.txt`, `llms.txt`), cadencia del keyword research (fundacional, revisión del mapa, minería de oportunidad), mapa temático (3 niveles y filtro de 4 dimensiones), metodología de Densidad de Señales (taxonomía, KPI beta, roadmap 30-60-90), schema priorizado para citación en IA (seis tipos, `@graph`, retiro de los rich results de FAQPage y HowTo), patrón de automatización de keywords de oportunidad (IA + Search Console + CMS) y las dos rutas de keyword research asistido (local y alojada).
- **Salió bien:** Registrar cada aporte como candidato con su fuente antes de convertirlo en referencia; etiquetar siempre el estado de la evidencia (propia, primaria, tercero, hipótesis).
- **Salió mal / incidencia:** Se descartó una técnica (enmascarar enlaces con JavaScript en lugar de `nofollow`) por obsoleta; quedó registrada como descartada.
- **Regla candidata:** ninguna
- **Herramientas:** `capture_learning.py`, fuentes primarias de Google y publicaciones de la agencia

### 2026-09-20 · caso-migracion-01 · guille

- **Qué se hizo:** Migración de dominio de un sitio WordPress con Bricks (23 artículos): auditoría del enlazado interno, medición de Search Console cruzando página y consulta, y refuerzo de la entidad con los identificadores del registro mercantil en los términos y en el schema `Organization`.
- **Salió bien:** (1) El bloque «Artículos relacionados» sin taxonomía devolvía siempre los 3 posts más recientes; se sustituyó por grupos temáticos definidos a mano y relleno con pilares, sin crear etiquetas públicas (huérfanas 5 a 1, concentración máxima 23 a 10, alcanzables desde la home 20/33 a 32/33). (2) Cruzar `query` + `page` desmontó una hipótesis propia: el 68 % de las impresiones de la página estrella estaba anonimizado. (3) Un mu-plugin con el filtro `rank_math/json_ld` añadió `legalName`, `taxID` y `foundingDate`, que el plugin SEO no ofrece.
- **Salió mal / incidencia:** Se presentó como demostrado que ampliar la cobertura léxica sube posiciones durante tres documentos, sin haber calculado el porcentaje anonimizado; la página con cobertura completa seguía en posición 23. Sin resultado de posicionamiento aún (el dominio cambió el día anterior).
- **Regla candidata:** (a) Antes de atribuir un enlazado interno pobre a falta de enlaces editoriales, auditar la consulta del bloque de relacionados y medir la **distribución** de entrantes, no la media. (b) Nunca atribuir el rendimiento de una página a las consultas visibles sin calcular `anonimizado % = 1 − (impresiones query+page ÷ impresiones page)`; por encima de ~30 % la inferencia no es defendible. (c) Sustituir «empresa legalmente constituida» por identificadores verificables, con consistencia carácter por carácter entre términos y schema. Las tres: un solo sitio, sin repetir.
- **Herramientas:** WordPress + Bricks, RankMath, Search Console API, crawl propio del grafo de enlaces

### 2026-09-21 · caso-local-rotulos-01 · guille

- **Qué se hizo:** Auditoría SEO de un sitio de rótulos comerciales con páginas servicio-ciudad en serie (WordPress + Elementor): triage de 36 problemas de Screaming Frog verificados contra la fuente de verdad (`_elementor_data` por REST) y medición del texto exclusivo frente al de plantilla en 51 páginas.
- **Salió bien:** Abrir los ítems en vez de fiarse del recuento (de 36 problemas: 21 reales, 2 de servidor, 1 sin verificar, 2 informativos, 10 artefactos); medir entre páginas (0 % de texto exclusivo en servicio-ciudad; una FAQ de otro servicio copiada en 47 de 51 páginas); cruzar con demanda propia y con la SERP.
- **Salió mal / incidencia:** Descarté «errores ortográficos en 250/250 páginas» como falso positivo sin abrir un solo error; al exportar los 3.009 casos aparecieron defectos reales (caracteres corruptos en el consentimiento de un formulario, entidades HTML doble-escapadas, una errata en un titular). La SERP se midió con un proxy (DuckDuckGo/Bing) porque Google bloqueó y no se eludió.
- **Regla candidata:** (a) Un «falso positivo» sin abrir es una suposición: un filtro que marca casi el 100 % de las páginas es ruido o defecto de plantilla, y se distingue abriendo ítems, ordenados por baja frecuencia. (b) Medir el texto exclusivo (nombres de ciudad neutralizados) antes de publicar páginas locales en serie; «cero impresiones» en un borrador no prueba falta de demanda. Un solo sitio, sin repetir.
- **Herramientas:** Screaming Frog (skill externa `screaming-frog-seo`), REST de WordPress, Search Console

### 2026-10-03 · caso-home-01 · guille

- **Qué se hizo:** Optimización técnica del rendimiento de un sitio Astro SSG: servicio de imágenes (sharp) con tope de calidad ≤ 72 y de 100 KB por variante, y una sola hoja CSS.
- **Salió bien:** Las imágenes bajaron de 31 a 11 MB; con un solo CSS (`cssCodeSplit: false`) el Lighthouse móvil subió de 89 a 96 en producto y de 91 a 98 en contacto.
- **Salió mal / incidencia:** `inlineStylesheets: always` empeoró el TBT (+170 a +500 ms); el LCP simulado de Lighthouse varía ~1 s entre corridas según la carga de la máquina.
- **Regla candidata:** Medir Lighthouse varias veces antes de comparar y no inlinear todo el CSS por defecto. Una sola sesión, un solo sitio.
- **Herramientas:** Astro, sharp, Lighthouse

### 2026-10-13 · caso-mantenimiento-05 · guille

- **Qué se hizo:** Integración de `web-go-high-level-ia` como sub-skill de esta skill: sección en `SKILL.md` sobre el SEO que se implementa dentro del constructor de IA de GoHighLevel (`head()` por ruta, un `h1`, `noindex` provisional, `alt` + `width/height` con CDN que renombra archivos, `og:image` absoluta, medición por `data-track`).
- **Salió bien:** Dejar clara la frontera: esta skill decide qué se escribe y se indexa, la sub-skill cómo se construye y se transfiere.
- **Salió mal / incidencia:** Nada relevante.
- **Regla candidata:** ninguna
- **Herramientas:** `web-go-high-level-ia`

### 2026-10-15 · caso-mantenimiento-06 · guille

- **Qué se hizo:** Integración de `rea-reverse-engineer` como skill de apoyo para entender competidores y referencias (outline, title/meta/canonical/hreflang, tipos de JSON-LD, HTML crudo frente a renderizado, peso, terceros), nivel N1 por defecto.
- **Salió bien:** Contrato claro: devuelve una ficha observado / inferido / desconocido y no sustituye a Screaming Frog ni a las fuentes primarias.
- **Salió mal / incidencia:** Nada relevante.
- **Regla candidata:** ninguna
- **Herramientas:** `rea-reverse-engineer` (`scripts/web_probe.py`)

### 2026-10-16 · caso-mantenimiento-07 · guille

- **Qué se hizo:** Migración de la skill al repo gui-skills como fuente canónica: Obsidian pasa a ser opcional (Paso 0 lee HANDOFF/HANDSHAKE y `memoria/`; scripts con respaldo a `memoria/`), `install.py` deja de refrescar desde la bóveda y pasa a crear enlaces, `screaming-frog-seo` queda como skill opcional, se anonimizó el contenido y se creó `hosted-src/` con `tools/build_hosted.py` para generar la versión web.
- **Salió bien:** Los scripts funcionan sin bóveda (probados con un HOME temporal) y con bóveda (de prueba); `capture_learning.py` se niega a escribir en el repo texto con términos de la lista privada, correos o rutas personales.
- **Salió mal / incidencia:** El paquete `seo-content-system.skill` de la fuente estaba desfasado (9 archivos distintos de las carpetas) y no se migró. La fuente y la copia instalada coincidían en todos los archivos de texto.
- **Regla candidata:** Un paquete empaquetado (`.skill`, `.zip`) no se versiona junto a sus fuentes: se genera al publicar.
- **Herramientas:** Python 3.12, `tools/build_hosted.py`

### 2026-10-22 · caso-local-rotulos-01 · guille

- **Qué se hizo:** Reducción de pSEO local por filtro geográfico: 18 páginas de 12 ciudades fuera del radio de servicio (>140 mi de la base) redirigidas con 301 por snippet template_redirect (ciudad -> hub de ubicaciones, hija -> página de servicio equivalente), pasadas a borrador, 16 borradores sobrantes a papelera con respaldo, hub de ubicaciones depurado. Sitemap de páginas 70 -> 52.
- **Salió bien:** Kit preparado semanas antes en modo dry con CSV de impresiones, enlaces entrantes y destino; verificación en vivo 18/18 301 antes de pasar a borrador; destinos comprobados 200; sitemap y llms.txt revisados después.
- **Salió mal / incidencia:** El modo de papelera recalculó la lista tras el paso a borrador y envió también las 18 páginas recién retiradas; se restauró al minuto con su slug original. Incidencia: Kits con varios pasos que recalculan el estado vivo: un paso posterior puede reclasificar lo que cambió el anterior. Excluir siempre lo tocado por pasos previos (archivo de estado).
- **Regla candidata:** En retiradas por 301 + borrador, la redirección debe ir por ruta (template_redirect) y no depender de que la página exista; verificar 301 en vivo antes de despublicar.
- **Herramientas:** WordPress REST, Code Snippets REST, Yoast sitemap, curl

### 2026-10-22 · caso-local-rotulos-01 · guille

- **Qué se hizo:** Enlazado interno ciudad -> hijas ciudad x servicio: línea de enlaces con ancla descriptiva en el hero de 6 páginas de ciudad (8 enlaces de contenido), verificada en público; línea base de Search Console guardada para medir a 2/4/8 semanas.
- **Salió bien:** Widget clonado del párrafo vecino para heredar estilo; script idempotente con respaldo y reversión; descubierto que el endpoint REST de caché de Elementor equivale a regenerar y permite verificar en público sin intervención.
- **Salió mal / incidencia:** nada relevante
- **Regla candidata:** Tras editar _elementor_data por API, limpiar la caché con DELETE elementor/v1/cache antes de verificar el HTML público (sin ella el público sigue con la versión vieja).
- **Herramientas:** no indicadas

### 2026-10-22 · caso-local-rotulos-01 · guille

- **Qué se hizo:** Enlazado interno hub-and-spoke: bloque de lectura relacionada (título + lista de enlaces) en 18 páginas de servicio/ciudad/home hacia 21 posts (42 enlaces, 2 páginas por post, anclas descriptivas) y enlace de vuelta a su servicio en los 6 posts que no lo tenían.
- **Salió bien:** Medición previa del estado real (15 de 21 posts ya enlazaban) evitó duplicar enlaces; una página piloto con revisión visual antes de aplicar al resto; scripts idempotentes con respaldo; verificación en público 42/42 tras limpiar caché de Elementor por API.
- **Salió mal / incidencia:** La primera comprobación pública usó un patrón de URL equivocado (los posts viven en /blog/) y dio 18 falsos fallos; se corrigió el chequeo, no las páginas.
- **Regla candidata:** Al verificar enlaces nuevos, derivar el patrón de URL de los permalinks reales (posts bajo /blog/) y comprobar primero una página a mano antes de automatizar el chequeo.
- **Herramientas:** no indicadas

### 2026-10-22 · caso-local-rotulos-01 · guille

- **Qué se hizo:** Unificación de perfiles sociales (entidad de marca): corregidos en Elementor (bloques de datos estructurados LocalBusiness, iconos y plantillas) y en los ajustes del plugin SEO (sameAs de Organization) a las cuentas oficiales confirmadas por el cliente; verificado en 11 páginas públicas.
- **Salió bien:** Escaneo previo de todo el contenido y del sameAs público para saber qué estaba mal y dónde; validación de JSON antes de escribir evitó guardar un bloque roto; verificación final por páginas.
- **Salió mal / incidencia:** Al probar el endpoint de perfiles sociales del plugin SEO con solo la red a cambiar, se reinició el resto de redes; se restauró en segundos con la lista completa. Incidencia: El endpoint de configuración de perfiles sociales del plugin SEO reemplaza lo no enviado: enviar siempre la lista completa y comprobar el sameAs público antes y después.
- **Regla candidata:** Antes de escribir ajustes globales del plugin SEO por API, tomar foto del sameAs público y enviar el conjunto completo, no solo el campo a corregir.
- **Herramientas:** no indicadas

### 2026-10-23 · banco-pruebas-actualizacion-v1-5-0 · guille

- **Qué se hizo:** Cierre y publicacion del borrador v1.5.0: segunda y tercera pasada de ClickUp/Obsidian/Drive/Sheets integradas, 5 referencias nuevas y 18 ampliadas con secciones [ClickUp 2]/[Sheets 2]/[Drive 2], 16 plantillas nuevas, hosted regenerada, y resueltas las decisiones pendientes de Guille (tope de imagen unificado a <=100KB en drive-deliverables-and-guidelines.md, rutas personales de HANDOFF/HANDSHAKE marcadas como excepcion con privacy-scan: ignore, rangos de title/meta confirmados sin conflicto).
- **Salió bien:** privacy_scan, build_hosted --check y editorial_lint quedaron limpios antes de publicar; las decisiones ambiguas se resolvieron con Guille antes de tocar texto en vez de asumirlas.
- **Salió mal / incidencia:** El trabajo quedo repartido en varias sesiones sin commit durante dias (1.3/1.4/1.5), lo que acumulo 92 archivos sin guardar y obligo a reconstruir el contexto de las decisiones pendientes desde el HANDOFF.
- **Regla candidata:** Cuando una actualizacion de skill deja pendientes de decision explicitos en el HANDOFF, resolverlos y registrarlos en una entrada propia antes de log_job/publish_job, nunca asumirlos ni publicarlos en silencio.
- **Herramientas:** no indicadas

<!-- registro:fin -->

## 5. Reglas candidatas (sin aprobar)

| Regla | Visto en (casos) | Estado |
|---|---|---|
| Auditar la consulta del bloque «relacionados» y medir la distribución de enlaces entrantes (no la media) antes de culpar a la falta de enlaces editoriales | caso-migracion-01 | candidata: un solo caso, sin resultado de posicionamiento; revisar 2026-12-20 |
| No atribuir el rendimiento de una página a sus consultas visibles sin calcular el % anonimizado (por encima de ~30 % no es defendible) | caso-migracion-01, caso-local-rotulos-01 | candidata: se repitió el método en dos sitios; falta contrastar en un sitio de mayor volumen; revisar 2026-12-20 |
| Identificadores del registro mercantil (razón social, NIT, fecha, representante) en términos y schema `Organization`, consistentes carácter por carácter | caso-migracion-01 | candidata: sin medir; repetir en otro proyecto del sector antes de promover; revisar 2026-11-20 |
| Un «falso positivo» sin abrir es una suposición: abrir los ítems de los filtros que marcan casi todas las páginas | caso-local-rotulos-01 | candidata: una auditoría; revisar 2026-12-21 |
| Medir el texto exclusivo antes de publicar páginas locales en serie | caso-local-rotulos-01 | candidata: un sitio, SERP por proxy; revisar 2026-12-21 |
| Tope de 100 KB por variante de imagen y un solo CSS mejoran el Lighthouse móvil en Astro; no inlinear todo el CSS | caso-home-01 | candidata: una sesión, un sitio; revisar 2026-11-02 |
| Con la keyword ya en slug, title y H1 y aun así en posición 25-31, reescribir títulos no mueve la posición: el cuello de botella es profundidad y autoridad | caso-migracion-01, caso-local-rotulos-01 | candidata: coincide en dos sitios; sin medir resultado |
| En retiradas por 301 + borrador, la redirección debe ir por ruta (template_redirect) y no depender de que la página exista; verificar 301 en vivo antes de despublicar. | caso-local-rotulos-01 | candidata |
| Tras editar _elementor_data por API, limpiar la caché con DELETE elementor/v1/cache antes de verificar el HTML público (sin ella el público sigue con la versión vieja). | caso-local-rotulos-01 | candidata |
| Al verificar enlaces nuevos, derivar el patrón de URL de los permalinks reales (posts bajo /blog/) y comprobar primero una página a mano antes de automatizar el chequeo. | caso-local-rotulos-01 | candidata |
| Antes de escribir ajustes globales del plugin SEO por API, tomar foto del sameAs público y enviar el conjunto completo, no solo el campo a corregir. | caso-local-rotulos-01 | candidata |
| Cuando una actualizacion de skill deja pendientes de decision explicitos en el HANDOFF, resolverlos y registrarlos en una entrada propia antes de log_job/publish_job, nunca asumirlos ni publicarlos en silencio. | banco-pruebas-actualizacion-v1-5-0 | candidata |

## 2026-10-23 · Actualización a 1.3.0
- Se instala seo-content-system 1.3.0 (marcas [ClickUp], [Obsidian], [Sheets] y [Drive]): nuevas referencias, plantillas en assets/templates y docs/CAMBIOS.md + docs/INVESTIGACION-CLICKUP-SEO.md.
- Respaldo de 1.2.0: D:\guille-diseno\skills\_respaldos\seo-content-system-v1.2.0-2026-10-23. <!-- privacy-scan: ignore -->
- Plantillas de proyecto: D:\guille-diseno\skills\seo-plantillas-proyecto. <!-- privacy-scan: ignore -->


## 2026-10-23 · Actualización a 1.4.0
- Revisión externa de solo lectura de la skill completa; informe fuera del repo (carpeta de revisiones del usuario).
- Aplicado: principios 18-20 (retiro de datos, roadmap como «próximamente», schema sin marcadores, sin `Offer` vacío, sin duplicar el grafo de Rank Math); paso 2 (investigar carpeta y sitio antes de preguntar); paso 8 (higiene de archivos en PowerShell, YMYL); editorial-quality-gates §8-10; schema-markup-for-ai-citation (productos sin precio, plugins SEO y ajustes globales); structured-data (validación); technical-audit-by-finding (riesgo y ámbito, entrega completa con brief por hallazgo); task-brief y audit-findings-matrix.csv con riesgo, ámbito, reversión, verificación y brief; notas en technical-seo-guidelines y drive-deliverables; manifest 1.4.0.
- Pendiente de decisión de guille: rutas personales en la entrada 1.3.0 (bloquean privacy_scan), regenerar versión hosted (knowledge-map sin las plantillas nuevas), tope de imagen 100 KB frente a 150 KB, unificar rangos de title/meta y escalas de prioridad/estado, flag `--sin-chequeo-privacidad` de capture_learning.py, script nuevo de chequeo de entregables, fusiones y borrados propuestos. No se hizo commit.

## 2026-10-23 · Limpieza de menciones de credenciales
- Se retiraron de la documentación de la skill y del paquete de investigación las frases que describían dónde había credenciales en texto plano; se sustituyeron por un hallazgo genérico (usar gestor de contraseñas, nunca copiarlas a entregables). Re-escaneo sin valores. No se hizo commit.


## 2026-10-23 · Segunda pasada ClickUp + Obsidian + Drive (versión 1.5.0, borrador sin commit)

**Qué se hizo**
- Sobre la 1.4.0 se hizo una segunda lectura de ClickUp con 6 agentes de solo lectura por bloques de listas (agencia propia, clientes recurrentes, B2B/logística, educación, contrato por fases y e-commerce, plantillas GDD y Docs). **Todos quedaron parciales:** el conector de ClickUp tiene un tope de 1.000 llamadas/día para todo el workspace y se agotó a mitad de la lectura (se reinicia unas 15 h después).
- Se leyeron además 5 notas de Obsidian que habían quedado pendientes (modelo de priorización, checklist de publicación, flujo editorial, diagnóstico de caídas, prompt de auditoría con rastreador para WordPress + Elementor).
- Se lanzaron 2 agentes de lectura de Drive/Sheets/Docs/Slides con los enlaces que dejaron los agentes de ClickUp. **No se sabe si terminaron** cuando se cortó la sesión: sus salidas esperadas son `drive-A.md` y `drive-B.md` (ver «Dónde está todo»). No están integradas.

**Referencias nuevas (en `references/`)**: `contract-phases-and-scope-control.md`, `launch-checklist-new-site.md`, `ecommerce-seo-multicountry.md`, `education-program-seo.md`, `measurement-traps-and-diagnosis.md`.

**Referencias ampliadas con una sección `[ClickUp 2]` al final**: `clickup-task-operating-model`, `agency-operating-methodology`, `deindexing-procedure`, `technical-audit-by-finding`, `migration-redirects-and-validation`, `on-page-metadata-and-urls`, `editorial-quality-gates` (§11), `image-seo-and-accessibility`, `analytics-search-console-and-decisions`, `keyword-research-cadence-and-triggers`, `programmatic-and-local-seo`, `internal-linking-and-conversion-paths`, `growth-driven-design-gdd`, `onboarding-and-initial-audit`, `technical-seo-and-indexability`, `editorial-pattern-long-form`, `entity-presence-and-knowledge-graph`, `wordpress-technical-audit-checklist` (trampas de Elementor).
También: `SKILL.md` (versión 1.5.0, principios 21 y 22, índice), `hosted-src/knowledge-map.json` (5 fuentes nuevas) y, fuera del repo, `seo-plantillas-proyecto/AGENTS.md` (ruteo a v1.5.0 y reglas 5-7).

**Lo que NO se hizo (siguiente sesión)**
1. **Integrar Drive/Sheets:** leer `drive-A.md` y `drive-B.md` (si existen) y pasar lo nuevo a `sheets-workbook-templates.md`, `drive-deliverables-and-guidelines.md` y `assets/templates/` (sección E de cada digest trae las acciones «añadir X a Y»).
2. **Cobertura de ClickUp pendiente:** ver `_revisiones/pendientes-clickup-segunda-pasada-2026-10-23.md` (IDs de lista y método). Repartir el cupo: no lanzar 6 agentes a la vez; ≈150 llamadas por lista.
3. **Anexar a `docs/INVESTIGACION-CLICKUP-SEO.md` el §23** (resumen de esta pasada y sus límites) y la entrada 1.5.0 en `docs/CAMBIOS.md` (la entrada ya está redactada abajo en el HANDSHAKE; falta pasarla a CAMBIOS si no quedó).
4. **Validar:** todos los enlaces `references/…` y `assets/…` de `SKILL.md` y de las referencias existen; `python scripts/editorial_lint.py --help`; JSON válidos (`system-manifest.json`, `knowledge-map.json`); búsqueda de privacidad (sin nombres de cliente, dominios, personas, correos, IDs ni credenciales) en los 5 archivos nuevos y en las secciones `[ClickUp 2]`.
5. **Regenerar la versión hosted:** `python <repo>/tools/build_hosted.py` y luego `--check`.
6. **Sincronizar copias:** el clon del repo es la fuente canónica y va por delante de `D:\guille-diseno\skills\seo-content-system-1.4.0` (esa carpeta es una copia de distribución). Pasar el clon a esa carpeta y renombrarla a 1.5.0 si Guille lo aprueba. <!-- privacy-scan: ignore -->
7. **Decisión de Guille antes de publicar:** el clon tiene ~51 archivos sin commit (trabajo 1.3/1.4 sin revisar + esta pasada). No se hizo pull ni commit. Resolver los pendientes de revisión que ya figuraban en HANDSHAKE (rutas personales de la entrada 1.3.0 que bloquean `privacy_scan`, tope de imagen 100 KB frente a 150 KB, rangos de title/meta, etc.). Luego `log_job.py` y `publish_job.py`. <!-- privacy-scan: ignore -->
8. **Registrar en Obsidian** (nota del proyecto y `Auditoría de skills y plugins.md`): el MCP de Obsidian expiró en esta sesión (CONNECT_TIMEOUT); si no responde, escribir directo en la bóveda `D:\guille-diseno\Obsidian`. <!-- privacy-scan: ignore -->

**Dónde está todo**
- Digests anonimizados de ClickUp (carpeta durable, fuera del repo): `D:\guille-diseno\skills\_revisiones\clickup-segunda-pasada\` (`clickup-G1..G6.md`, `clickup-G1..G6-links.txt` sin anonimizar, y `drive-A.md`/`drive-B.md` si llegaron a existir). La sección **H** de cada digest lista las acciones «añadir X a la referencia Y»; las ya aplicadas están en esta entrada; faltan las de menor valor (p. ej. plantillas `gdd-task-brief.md`, `client-content-review-checklist.md`, `pre-launch-audit-checklist.md`, sección de pauta + landing). <!-- privacy-scan: ignore -->
- Pendientes de lectura con IDs: `D:\guille-diseno\skills\_revisiones\pendientes-clickup-segunda-pasada-2026-10-23.md`. <!-- privacy-scan: ignore -->

**Lecciones del proceso**
- La carga masiva de tareas (`task.get_many`) no devuelve descripción (`content` nulo), pero sí `content_size`, checklists, subtareas y adjuntos: sirve para filtrar qué tareas leer a fondo.
- Seis agentes en paralelo agotan el cupo diario del conector antes de terminar; mejor 2-3 agentes con presupuesto explícito.
- Evidencia parcial: lo derivado solo de títulos de tarea se marcó como tal en las referencias.
- Hallazgo de seguridad genérico: nunca guardar credenciales en tareas, documentos ni hojas; usar un gestor de contraseñas, rotar ante cualquier exposición y nunca copiarlas a entregables. Una tarea de informe pide «exagerar» horas (no replicar).

> Actualización de la misma entrada: los agentes de Drive/Sheets sí escribieron salidas (`drive-A.md`, `drive-A-p2.md`, `drive-A-p3.md`, `drive-B.md`, ya copiadas a `_revisiones/clickup-segunda-pasada/`). **No se revisó si están completas ni se integraron**: leer su sección E («NUEVO frente a lo ya cubierto») y su sección F («Límites») antes de aplicar.
> Corrección: el agente de Drive B (`drive-B.md`) fue **detenido antes de terminar**; su digest puede estar incompleto (comprobar si tiene sus secciones E y F). Los de Drive A sí terminaron o dejaron salidas parciales (`drive-A*.md`). Los archivos de Google de los grupos G4-G6 que no se abrieron hay que repetirlos con `clickup-G4/G5/G6-links.txt`.
> Segunda corrección: **los dos agentes de Drive (A y B) fueron detenidos antes de terminar.** Sus archivos (`drive-A.md`, `drive-A-p2.md`, `drive-A-p3.md`, `drive-B.md`, `drive-B-part2.md`, en `_revisiones/clickup-segunda-pasada/`) son **notas incrementales de estructura (sección B), sin las conclusiones E/F ni el cierre**. Úsalos como material en bruto: extraer de ellos lo nuevo frente a `sheets-workbook-templates.md` y `drive-deliverables-and-guidelines.md`, y reabrir con los conectores lo que falte según `clickup-G*-links.txt`.


## 2026-10-23 · Tercera pasada: integración de Drive/Sheets y cierre del borrador 1.5.0

**Qué se hizo**
- **Drive/Sheets integrado.** Los cinco archivos de los agentes de Drive eran notas incrementales de estructura (sin las conclusiones E/F). Se pasó lo nuevo a `references/sheets-workbook-templates.md` §10 (diez bloques) y `references/drive-deliverables-and-guidelines.md` §12. Se retiraron las cifras de clientes (porcentajes de concentración, horas por talla): solo estructura y orden de magnitud.
- **16 plantillas nuevas** en `assets/templates/`: `gdd-task-brief.md`, `client-content-review-checklist.md`, `pre-launch-audit-checklist.md`, `landing-technical-sheet.md` y los CSV `gdd-time-estimates`, `programmatic-landing-inventory`, `programmatic-input-matrix`, `program-approval-matrix`, `program-data-sheet`, `product-input-matrix`, `consolidation-canonical-redirect`, `internal-linking-matrix`, `competitor-matrix`, `client-intake-matrix`, `monthly-request-log`, `ad-copy-by-angle`. Listadas en `SKILL.md`.
- **Sección H de los digests G1-G6:** casi todo estaba ya aplicado. Lo que faltaba se aplicó: las tres plantillas nombradas, `gdd-time-estimates.csv` y una sección «pauta y landing, SEO + CRO y cierre real de entregas» en `conversion-and-content-performance.md`. Las páginas de ranking ya estaban en `editorial-pattern-long-form.md`.
- **Docs:** §23 anexado a `docs/INVESTIGACION-CLICKUP-SEO.md`; la entrada 1.5.0 de `docs/CAMBIOS.md` ya existía y se completó.
- **Hosted:** el `knowledge-map.json` no clasificaba 11 plantillas Markdown (varias de la 1.3/1.4); se añadieron a `11-plantillas.md`. `build_hosted.py` regenerado y `--check` en AL DIA.
- **Validación:** JSON válidos; `editorial_lint.py --help` responde; todos los enlaces `references/`, `assets/` y `scripts/` existen salvo dos que apuntan a skills externas por diseño (`06-seo-en-ghl-ai-studio.md` de `web-go-high-level-ia` y `web_probe.py` de `rea-reverse-engineer`); `privacy_scan` limpio en referencias, plantillas y hosted (solo quedan las rutas personales de HANDOFF/HANDSHAKE).
- **Obsidian:** el MCP no respondió; se registró escribiendo directo en la bóveda (fila en la Auditoría de skills y entrada en la nota del proyecto).

**Lo que NO se hizo**
1. **ClickUp:** el conector seguía en `RATE_LIMIT_EXCEEDED` (1.000/1.000 llamadas, reinicio en unas 14 h), así que no se lanzaron agentes y las listas pendientes siguen igual (archivo de pendientes fuera del repo). Retomar con 2-3 agentes, ≈150 llamadas por lista, empezando por las de prioridad Alta, solo lectura.
2. **Copia de distribución sincronizada** (aprobado por Guille): `robocopy /MIR` del clon a la carpeta antigua y renombrada a `seo-content-system-1.5.0`; diff sin diferencias.
3. **Commit, `log_job` y `publish_job`:** no se ejecutaron. El clon tiene unos 60 archivos sin commit.
4. Los enlaces de Google de los grupos G4-G6 que no se abrieron siguen sin abrir.

**Decisiones de Guille que faltan** (heredadas de la 1.3/1.4): rutas personales de la entrada 1.3.0 y de este HANDOFF/HANDSHAKE que bloquean `privacy_scan`; tope de imagen 100 KB frente a 150 KB; rangos de title/meta y escalas de prioridad/estado; flag `--sin-chequeo-privacidad` de `capture_learning.py`; script de chequeo de entregables; fusiones y borrados propuestos; commit y publicación.

**Lecciones del proceso**
- Un digest cortado (sin secciones E/F) sirve como material en bruto, pero conviene verificar contra lo ya cubierto antes de aplicar: casi toda la sección H de ClickUp ya estaba en la 1.5.0.
- Al clasificar plantillas nuevas hay que actualizar `knowledge-map.json` o `build_hosted.py` falla; hacerlo al crear cada plantilla.

## 2026-10-23 · Correcciones de calidad v1.5.0
- Descripción del frontmatter de `SKILL.md` recortada a ≤1024 caracteres sin quitar disparadores.
- Referencias a archivos de otras skills reescritas indicando la skill externa (`web-go-high-level-ia`, `rea-reverse-engineer`); retirada la mención a un archivo inexistente en `keyword-research-ia-local-desktop.md`.
- Hallazgos de seguridad reescritos en forma genérica (sin ubicaciones). Sin commit.

## 2026-10-23 · Decisiones de Guille antes de publicar v1.5.0
- **Tope de imagen:** confirmado ≤100 KB como regla única. `drive-deliverables-and-guidelines.md` todavía decía "hero 100–150 KB"; corregido a ≤100 KB para que no contradiga `technical-seo-lineamientos-generales.md`.
- **Rutas personales en HANDOFF/HANDSHAKE** (8 hallazgos de `privacy_scan`, rutas de respaldo en el disco de Guille): se publican tal cual — son metadatos de la skill, no datos de cliente.
- **Rangos de title/meta y escalas de prioridad/estado:** sin conflicto real (`on-page-metadata-and-urls.md` ya documenta que la regla del cliente manda sobre los valores por defecto); no requieren cambio.
- **Pendientes de alcance nuevo (quedan para después, sin implementar en esta publicación):** flag `--sin-chequeo-privacidad` en `capture_learning.py`, script de chequeo de entregables, fusiones/borrados de referencias propuestos.
- Con esto, los pendientes heredados de 1.3/1.4/1.5 quedan resueltos o diferidos explícitamente. Lista para `log_job` y `publish_job`.
