# Migración, redirecciones y validación [ClickUp]

Origen: tareas de migración, de planes de redirección y de auditorías pre/post lanzamiento, anonimizadas. Complementa `technical-seo-and-indexability.md`.

## Antes de migrar
1. **Rastrear el sitio en desarrollo y compararlo con producción**: URLs que desaparecen, cambios de title/H1/canonical, noindex heredado del entorno de pruebas.
2. Hacer el inventario de URLs con valor: clics o impresiones en GSC, enlaces externos, tráfico en GA4.
3. **Plan de redirecciones** en una pestaña del documento de arquitectura: `URL origen · URL destino · Tipo (301) · Motivo · Estado`. Las reglas:
   - redirigir 1:1 al equivalente más cercano y no mandar todo al home;
   - evitar las cadenas;
   - las URLs duplicadas o "de prueba" (`-test`, `-prueba`) se redirigen a la oficial;
   - las URLs que deben salir del índice pero seguir accesibles van con noindex (ver `deindexing-procedure.md`).
4. Hacer la checklist de lanzamiento: redirecciones, GA4, GSC, GTM, HTTPS y cabeceras, nomenclatura de URLs, robots.txt, sitemap y hreflang si aplica.
5. Definir quién implementa y quién aprueba. Nada se toca en vivo sin aprobación escrita (principio 14).

## Después de migrar (las primeras 24–72 h y la primera semana)
- Rastrear el dominio nuevo y dejar un **reporte de incidencias** priorizado (Crítico/Alto/Medio/Bajo).
- Revisar las 404 nuevas y armar el **mapa de redirecciones de 404**.
- Enviar el sitemap nuevo, inspeccionar las URLs clave y vigilar la cobertura en GSC.
- Comparar clics e impresiones antes y después, con la fecha de despliegue anotada.
- Las incidencias técnicas que dejó un proveedor externo se documentan aunque "no sean nuestras", y se resuelven las que estén a nuestro alcance.

## Validar las implementaciones
Después de cada ronda de correcciones, revisar fila por fila la pestaña de incidencias de la auditoría. Las columnas son `Estado (Realizado / En revisión / Pendiente)` y `Observaciones`. Si una corrección falló por falta de contexto, se reescribe la tarea con el criterio de hecho explícito.

## Plantillas [Sheets]
- Checklist de migración por etapa y responsable: `assets/templates/migration-checklist.csv`.
- Mapa de redirecciones: `assets/templates/redirect-map.csv`.
- Triage de 404 en tres pestañas (a redireccionar / redireccionadas / no redireccionables → desindexar): `assets/templates/404-triage.csv`.
- Validación de implementaciones: filtrar `Implementado = FALSE` en `assets/templates/implementation-tracker.csv` y `assets/templates/audit-finding-tab.csv`.


## Ampliación [ClickUp 2]: secuencia real, clasificación de 404 y lanzamiento

Origen: una migración a un sitio nuevo de dos meses, una reestructuración de oferta con 98 páginas y proyectos de e-commerce (anonimizado).

### Secuencia real de una migración (≈15 pasos)
1. Revisión del documento de migración → plan de implementación.
2. **Rastrear el sitio en desarrollo (sandbox) y compararlo con producción** → auditoría de pendientes de migración sobre el sandbox (documento que se debe llenar) → lista de URLs del nodo → verificación.
3. Insumos y tareas posmigración.
4. Implementación, **un hallazgo por tarea**: plan de redirecciones → implementar redirecciones → retirar del sitemap las URLs que ahora redirigen (en cada idioma) → peso y nombre de imágenes → reemplazar imágenes de más de 100 KB con su `alt` asociado → implementar `alt` → meta títulos → metadescripciones y H1 duplicados → migas de pan → revisar el protocolo del sitemap de artículos.
5. Seguimiento: **informe semanal durante el cambio**, auditoría y revisión de optimizaciones, informe de rendimiento orgánico.
6. Dos auditorías posmigración + QA de páginas + validaciones + **auditoría de rutas** (sitemaps, canonical y hreflang por idioma).

### Plan y mapa 301 antes del rediseño
Construir el **mapa 301 antes** de rediseñar, con una matriz por tipo de página (ver `assets/templates/redirect-map.csv`). Auditar además los **enlaces internos y externos propios** que apuntan a URLs que ahora redirigen: corregir el origen, no dejar la redirección como única solución.

### Clasificación de 404
Clasificar en pestañas por tipo (ciudades o países, sin categoría, tema, equipo, generales) y decidir por grupo: **301** (hay destino equivalente) frente a **410** (retiro definitivo), con un instructivo. La mayoría suele redirigirse masivamente a carpetas. **No dejar la tarea en «nuevo» indefinidamente**: en un caso real las tareas de 404 y enlaces rotos de enero nunca se ejecutaron en casi dos años.

### Controles adicionales de QA posmigración
Cabeceras (headers), páginas sin H1, H1 no secuencial, imágenes de más de 100 KB, 404, sitemap + rastreo, caché del servidor, redirecciones por país y manuales de entrega. En e-commerce multipaís: entorno en el dominio nuevo con respaldo, espejo para el segundo país, validaciones técnicas en dos partes y **QA triple**; ver [ecommerce-seo-multicountry.md](ecommerce-seo-multicountry.md).

### Dependencias que bloquean una migración
Acceso al CMS actual cuando lo administra un proveedor (registrar como dependencia del cliente y escalar **antes**), cuenta de Search Console, accesos al servidor y estado de stock o catálogo que decide qué URL sigue viva.

### Sitio nuevo (no migración)
Para un sitio React/SPA, un MVP estático o un lanzamiento por etapas (GDD), usar [launch-checklist-new-site.md](launch-checklist-new-site.md).
