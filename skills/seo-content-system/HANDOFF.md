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
