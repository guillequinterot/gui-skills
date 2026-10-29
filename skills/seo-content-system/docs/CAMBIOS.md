# CAMBIOS v1.5.0 → v1.6.0 (2026-10-29)

Origen: una auditoría real (`caso-seo-sitio-servicios-01`) de un sitio de servicios técnicamente sano (rendimiento 97 a 100, schema rico, 0 enlaces rotos) que no posicionaba. El linter del proyecto pasaba con 0 fallos y 0 avisos: la causa estaba en lo que ese linter **no** comprobaba.

- **Nueva referencia `references/service-site-seo-gate.md`:** ocho causas raíz (nombre por jerga interna y no por búsqueda; varias páginas con la misma frase raíz; servicios delgados frente a artículos; falta de un caso del servicio que se vende; clusters de un solo artículo; host canónico sin 301 en `https://www`; `lang`/`hreflang` y `alt` mal tratados; medición y autoridad), triage del spam de enlaces entrantes, checklist de 10 puntos antes de publicar y lista de lo que no se hace (fusionar servicios o redirigir sin el dueño, reverificar volúmenes de pago, «arreglar» falsos positivos).
- **Nuevo script `scripts/site_seo_gate.py`** (solo biblioteca estándar, solo lectura) y **`scripts/test_site_seo_gate.py`** (16 comprobaciones, sin red externa): candidatos a canibalización por frase raíz del título, aperturas casi iguales, servicios delgados y secciones que faltan, `lang`/`hreflang` inconsistentes, imágenes sin atributo `alt` (distingue `alt=""` correcto de un logo sin etiqueta), menú y pie sin listas, sitemap, y `--live` con las cuatro variantes del host. Probado contra el sitio de la auditoría: reproduce la canibalización del título entre servicios, el artículo frente al servicio y el `https://www` que responde 200.
- **SKILL.md:** versión 1.6.0; principios 23 a 27 (nombrar por la búsqueda; una frase raíz y una intención por URL; estructura mínima y un caso propio por servicio; host canónico en el servidor; probar todas las rutas de acceso antes de decir «no hay datos», no inferir indexación con `site:`, y cambios de título con fecha y línea base); modo `gate`; la puerta se ejecuta en el control de calidad (paso 8) de los sitios de servicios.
- **hosted-src/knowledge-map.json:** la referencia nueva entra en el documento técnico de la versión web (regenerada con `tools/build_hosted.py`).

# Correcciones v1.5.0 (2026-10-23)

- `SKILL.md`: descripción ≤1024 caracteres; rutas de skills externas explícitas.
- `keyword-research-ia-local-desktop.md`: retirada referencia a archivo inexistente.
- `INVESTIGACION-CLICKUP-SEO.md`, `sheets-workbook-templates.md`, `HANDOFF.md`: hallazgos de seguridad en forma genérica.

# CAMBIOS v1.4.0 → v1.5.0 (2026-10-23, borrador sin publicar)

- **Nuevas referencias [ClickUp 2]:** `contract-phases-and-scope-control.md` (carpeta de contrato de 5 listas, campos de alcance, reglas de conteo y bolsa, tarea madre de landing con 9 subtareas, matriz de solicitudes, convergencia entre cuentas, higiene de tareas), `launch-checklist-new-site.md` (checklist de 12 secciones para React/SPA, plan de medición, MVP estático, auditoría en stage), `ecommerce-seo-multicountry.md` (hallazgos de Shopify, arquitectura multipaís, programático de e-commerce, plan de rendimiento y seguridad de 20 tareas), `education-program-seo.md` (programa como unidad, ficha de acción, schema de programa, gate de QA, rediseño), `measurement-traps-and-diagnosis.md` (page frente a query, distribución del enlazado, diagnóstico de caídas, priorización, regla de bloqueo; origen Obsidian).
- **Ampliadas (sección `[ClickUp 2]` al final):** clickup-task-operating-model, agency-operating-methodology, deindexing-procedure, technical-audit-by-finding (criterio de hecho por tipo), migration-redirects-and-validation (secuencia de 15 pasos, 404 en 301/410), on-page-metadata-and-urls (regla por cliente 58/140, sobre-optimización), editorial-quality-gates §11, image-seo-and-accessibility, analytics-search-console-and-decisions, keyword-research-cadence-and-triggers, programmatic-and-local-seo (publicación escalonada, GBP), internal-linking-and-conversion-paths, growth-driven-design-gdd, onboarding-and-initial-audit, technical-seo-and-indexability, editorial-pattern-long-form, entity-presence-and-knowledge-graph, wordpress-technical-audit-checklist (trampas de Elementor Pro).
- **SKILL.md:** versión 1.5.0, principios 21 (medir, no estimar) y 22 (criterio de hecho; no inflar horas), índice con las cinco referencias nuevas.
- **hosted-src/knowledge-map.json:** añade las cinco referencias nuevas.
- **Fuera del repo:** `seo-plantillas-proyecto/AGENTS.md` con el ruteo de la v1.5.0 y reglas 5-7.
- **[Sheets 2] / [Drive 2]:** `references/sheets-workbook-templates.md` §10 (libros de SEO programático, auditoría con clasificación por impacto, matriz de insumos, KWR de prospecto, oferta académica, linkbuilding / enlazado / competencia, plan editorial de autoridad, e-commerce multiidioma, operación recurrente, re-auditoría) y `references/drive-deliverables-and-guidelines.md` §12 (convenciones de entrega).
- **Plantillas nuevas en `assets/templates/` (16):** `gdd-task-brief.md`, `client-content-review-checklist.md`, `pre-launch-audit-checklist.md`, `landing-technical-sheet.md` y los CSV `gdd-time-estimates`, `programmatic-landing-inventory`, `programmatic-input-matrix`, `program-approval-matrix`, `program-data-sheet`, `product-input-matrix`, `consolidation-canonical-redirect`, `internal-linking-matrix`, `competitor-matrix`, `client-intake-matrix`, `monthly-request-log`, `ad-copy-by-angle`. Listadas en `SKILL.md`.
- **docs/INVESTIGACION-CLICKUP-SEO.md:** §23 (segunda pasada y sus límites).
- **Límites:** cobertura de ClickUp parcial por el tope diario del conector (listas pendientes registradas fuera del repo); los agentes de Drive/Sheets se detuvieron antes de cerrar y su material se integró desde notas de estructura; lo derivado solo de títulos de tarea está marcado como tal. Ver HANDOFF.

# CAMBIOS v1.3.0 → v1.4.0 (2026-10-23)

- **SKILL.md:** versión 1.4.0; paso 2 «investigar antes de preguntar»; principios 18-20; paso 8 con higiene de archivos y YMYL; enlace corregido a `docs/CAMBIOS.md`.
- **references/editorial-quality-gates.md:** secciones 8 (higiene de archivos y retiro de datos), 9 (roadmap) y 10 (YMYL).
- **references/schema-markup-for-ai-citation.md:** productos y software sin precio; plugins SEO que ya generan el grafo (Rank Math, ajustes globales); errores frecuentes ampliados.
- **references/structured-data-and-search-features.md:** validación sin marcadores, sin `Offer` vacío y sin nodos duplicados.
- **references/technical-audit-by-finding.md:** riesgo y ámbito (ajuste global de schema nunca Bajo); entrega completa con un brief por hallazgo.
- **assets/templates/task-brief.md:** riesgo/ámbito, reversión y verificación.
- **assets/templates/audit-findings-matrix.csv:** columnas Riesgo, Ámbito, Criterio de hecho, Reversión y Brief (link) al final (las fórmulas existentes no cambian).
- **assets/templates/technical-seo-guidelines.md** y **references/drive-deliverables-and-guidelines.md:** salvedades de Rank Math y de productos sin precio.
- **assets/system-manifest.json:** 1.4.0. HANDOFF y HANDSHAKE con entrada fechada.

# CAMBIOS v1.2.0 → v1.3.0 (borrador para revisión)

`seo-content-system-v2/` es una **copia completa y funcional**: el original entero, con 76 archivos, más las mejoras. No es un overlay. El original no se modificó.

## Modificado
- **SKILL.md.** Solo hay añadidos, marcados **[ClickUp]** o **[Obsidian]**; no se borró ninguna línea del original.
  - Cabecera de versión 1.3.0.
  - Principios 14–17: aprobación escrita antes de tocar el sitio en vivo, cada hallazgo como unidad de trabajo, ganancias tempranas primero, y KPI como parámetros de gestión con control de alcance.
  - Paso 0: situar la tarea en la fase del servicio y en GDD.
  - Modos nuevos: `onboarding`, `audit`, `migration`, `deindex` y `report`.
  - Paso 7: informe antes/después y dashboard de tres secciones.
  - Paso 8: revisión de compliance y de landings.
  - Paso 9 nuevo: entregar como tarea.
  - Sección de link building PR, local y programático.
  - Índice "Operación de agencia" dentro de las referencias.
  - Bloque [Obsidian] sobre la estructura de la bóveda, la nota puente con diseño y la jerarquía de evidencia.
- **`assets/system-manifest.json`** y **HANDSHAKE.md:** versión 1.3.0.
- **`references/technical-seo-lineamientos-generales.md`:** el tope de peso de imagen queda unificado en **≤ 100 KB**. Antes decía "100–150 KB" y "<150KB", lo que chocaba con la auditoría por hallazgo de ClickUp y con la decisión del HANDOFF de 100 KB por variante.
- **`references/keyword-research-ia-local-desktop.md`** y **`-web-hosted.md`:** se corrigieron 4 enlaces que estaban rotos en el original, porque apuntaban a `references/...` desde dentro de `references/`.
- **`references/agency-operating-methodology.md`** y **`technical-audit-by-finding.md`:** se actualizaron los recuentos y se añadieron referencias cruzadas.
- **`hosted-src/knowledge-map.json`:** se añadieron las 9 fuentes nuevas para que `build_hosted.py` las incluya.

## Nuevo [ClickUp]
- `references/onboarding-and-initial-audit.md`: kickoff, auditoría en 3 pasos, matriz de entendimiento, 4 tipos de KWR, competidores en 7 pasos y OKR.
- `references/growth-driven-design-gdd.md`: Estrategia → Launchpad (PAI) → Mejoras continuas (PMI/PBI), con el dashboard.
- `references/clickup-task-operating-model.md`: tarea madre y subtareas, estados, campos, niveles de servicio, alcance, 11 frentes mensuales y patrones recurrentes.
- `references/migration-redirects-and-validation.md`: comparación desarrollo/producción, plan de redirecciones, post-migración, mapa de 404 y validación de implementaciones.
- `references/wordpress-technical-audit-checklist.md`: 12 bloques.
- `references/technical-audit-by-finding.md` y `references/deindexing-procedure.md` (ya estaban en el borrador 1.3, ahora integradas).
- `assets/templates/audit-understanding-matrix.md` (nueva), además de `task-brief.md` y `seo-report.md`.

## Plantillas de proyecto
- `plantillas/AGENTS.md`: la tabla de ruteo apunta a references y templates reales de la v1.3.0, con 19 filas y todas las rutas validadas.

## Validación
- Todos los enlaces y rutas `references/`, `assets/` y `scripts/` de SKILL.md y de las references existen.
- Quedan sin resolver, por diseño, las rutas que viven fuera de la skill: `../../shared/protocolo-skill.md` del repo, y `references/06-seo-en-ghl-ai-studio.md` y `scripts/web_probe.py`, que pertenecen a las skills externas `web-go-high-level-ia` y `rea-reverse-engineer`.
- Los JSON son válidos y `editorial_lint.py --help` responde.
- Revisión de privacidad sin coincidencias en los archivos nuevos: sin clientes, dominios ni personas.

## Pendiente antes de publicar en gui-skills
- Revisión de Guille.
- `tools/build_hosted.py` para regenerar la versión hosted.
- `log_job` / `publish_job`.

## Nuevo [Drive]
Fuente: Docs, Slides y .xlsx del Drive del equipo, leídos en solo lectura el 2026-10-23. Solo se tomó estructura y metodología.
- `references/drive-deliverables-and-guidelines.md` (nuevo): informe mensual GSC+GA4, variante post-migración, acta de auditoría, memoria de sprint, lineamientos técnicos (7 bloques + checklist), propuesta de FAQs, propuesta técnica comercial (desindexación de PDFs), guía de entrevista a experto con 5 salidas, gameplan E-E-A-T trimestral (con las listas de validación reales), KWR por programa, libro de estrategia de cuenta y auditoría de GBP.
- Plantillas nuevas en `assets/templates/`: `seo-performance-report-deck.md`, `audit-review-minutes.md`, `sprint-meeting-memo.md`, `technical-seo-guidelines.md`, `faq-optimization-proposal.md`, `technical-proposal-deck.md`, `sme-interview-guide.md`, `eeat-gameplan.csv`, `kwr-program-clusters.csv`, `gbp-audit.csv`.
- Marcas [Drive] en `SKILL.md` (leyenda y bloque de plantillas) y en `deindexing-procedure`, `technical-seo-lineamientos-generales`, `analytics-search-console-and-decisions`, `keyword-research-and-query-mapping`, `editorial-pattern-long-form` y `programmatic-and-local-seo`. `knowledge-map.json` añade la nueva referencia.

## Nuevo [Sheets]
Todo se reconstruyó de 18 hojas reales, solo con la estructura.
- `references/sheets-workbook-templates.md`: libros de auditoría, migración, 404, KWR, arquitectura, plan, insumos, enlazado y seguimiento por carpeta, con vocabularios y fórmulas.
- 13 plantillas CSV en `assets/templates/`:
  - auditoría: `audit-findings-matrix`, `audit-finding-tab`;
  - migración: `migration-checklist`, `redirect-map`, `404-triage`;
  - contenido: `keyword-content-calendar`, `keyword-research-terms`, `content-architecture-map`;
  - gestión: `seo-work-plan`, `pending-tracker`, `implementation-tracker`, `traffic-opportunity-model`.
- Secciones [Sheets] añadidas en `SKILL.md`, `technical-audit-by-finding.md`, `migration-redirects-and-validation.md`, `onboarding-and-initial-audit.md` y `keyword-research-and-query-mapping.md`.
- `hosted-src/knowledge-map.json` ahora incluye la nueva referencia.
