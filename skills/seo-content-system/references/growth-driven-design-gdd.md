# Growth-Driven Design (GDD) aplicado a SEO [ClickUp]

Origen: el Doc interno "Diseñando sitios web SEO / GDD" y las listas de la plantilla GDD, anonimizados. Se usa cuando un sitio nuevo o un rediseño se lanza por etapas en vez de hacerse de una vez.

## Entendimiento del negocio
- Ventas entrega el cliente a operaciones con el contexto comercial.
- Se reúnen los accesos y se hace el benchmark UX, la auditoría del sitio actual y el análisis de competidores (ver `onboarding-and-initial-audit.md`).

## Etapa 1 · Estrategia
- KWR, user persona y **arquitectura de información por intención** (ver `search-intent-and-customer-journey.md` y `topical-map-and-content-architecture.md`).
- Las páginas se clasifican por impacto:
  - **PAI**: páginas de alto impacto (home, servicios principales, conversión).
  - **PMI**: páginas de impacto medio.
  - **PBI**: páginas de bajo impacto.

## Etapa 2 · Launchpad
- Se lanzan **solo las PAI**, optimizadas (on-page, schema, medición), con un dashboard que tiene tres secciones:
  1. **Adquisición e interacción** (GA4).
  2. **Visibilidad**: impresiones, posición media y keywords (GSC).
  3. **Salud del sitio**: Core Web Vitals.
- El cliente aprueba por escrito antes de publicar (principio 14).

## Etapa 3 · Mejoras continuas
- Con los datos del dashboard se mejoran las PAI (CTR, contenido, conversión) y luego se construyen las PMI y después las PBI.
- Cada mejora se trata como un experimento: hipótesis, cambio, fecha de despliegue y medición antes/después (ver `analytics-search-console-and-decisions.md`).

## Roles
Gestor GDD (dueño del proceso), UX, UI, front y SEO. El SEO participa desde la estrategia, no al final.

## Regla
El sitio no se da por "terminado" al lanzarse. El Launchpad es el mínimo que mide, y el crecimiento se decide con datos.


## Ampliación [ClickUp 2]: detalle de las listas de la plantilla

Origen: lectura de las listas de la plantilla GDD y de su versión ligera (anonimizado). Las tareas de la plantilla son un **esqueleto** (objetivo, insumos con «insertar enlace», ubicación del entregable y «cargar el tiempo»); no traen campos personalizados, criterio de hecho ni prioridad, y solo el dashboard tiene un checklist real. Las horas de la plantilla (2022) son orden de magnitud, no resultados.

- **Secuencia con dependencias en Estrategia:** persona y journey dependen del KWR; los metadatos van **después** del contenido aprobado; el wireframe, después del contenido.
- **Clasificación funcional de URLs:** navegación · conversión · interacción; las URLs de mayor interacción alimentan la arquitectura y el plan de redirecciones.
- **Contenido del cliente:** taller de inducción al equipo de contenido + tres talleres de revisión + cuatro criterios de revisión (encabezados, caracteres por módulo, keywords, narrativa frente al objetivo del módulo).
- **Prototipo para desarrollo:** imágenes nombradas con keywords desde el diseño, exportación por página y activos descargables.
- **Auditoría en stage** antes del lanzamiento, en tres frentes (SEO, UX, Front), con la verificación de que la analítica está conectada. Ver [launch-checklist-new-site.md](launch-checklist-new-site.md).
- **Mejoras continuas en cinco pasos:** línea base de métricas → cinco tareas de implementación por rol → scorecard → reporte. El UX audita Clarity en esta fase.
- **Dashboard:** objetivos del cliente → GA → GSC → Core Web Vitals; duplicar la plantilla, vincular GA4/GSC/ads y dar dos capacitaciones al cierre.
- **Handoff de operaciones (versión ligera):** una lista propia; las tres tareas de accesos e insumos quedan fundidas en una; tarea «Cliente - tiempo de entrega de insumos» como marcador del retraso del cliente; kick-off de socialización y cronograma GDD.
- Plantillas posibles (aún no creadas): brief de tarea GDD, tabla de estimaciones, checklist de revisión del contenido del cliente y checklist de auditoría previa en tres frentes.
