---
tags:
  - seo
---

# SEO técnico e indexabilidad

## Índice

- Modelo de diagnóstico
- Rastreo
- Indexación
- Canonicals
- Renderizado
- Rendimiento
- Internacionalización
- Despliegues

## Modelo de diagnóstico

Separar:

1. Descubrimiento.
2. Rastreo.
3. Renderizado.
4. Indexación.
5. Selección de canonical.
6. Clasificación.
7. Presentación en resultados.

No atribuir un problema de ranking a indexación sin evidencia.

## Rastreo

Revisar:

- Robots.txt.
- Respuestas HTTP.
- Sitemaps.
- Enlaces internos.
- Facetas y parámetros.
- Cadenas y bucles.
- Logs cuando existan.
- Bloqueos de CDN o firewall.

Robots.txt controla rastreo, no garantiza desindexación.

Para la capa específica de bots de IA (distinción entrenamiento vs. recuperación, user-agents concretos como GPTBot/ClaudeBot/PerplexityBot/OAI-SearchBot/Google-Extended, y el estándar `llms.txt`), ver [ai-crawler-access-and-llms-txt.md](ai-crawler-access-and-llms-txt.md) — es habitual que un firewall o plugin de seguridad heredado bloquee estos bots sin que nadie lo note.

## Indexación

Verificar:

- `noindex`.
- Canonical.
- Duplicación.
- Contenido disponible en HTML.
- Calidad y utilidad.
- Estado en Search Console.
- Sitemap.
- Soft 404.
- Acceso móvil.

## Canonicals

Una canonical es una señal. Mantener coherencia entre:

- Canonical declarada.
- Redirecciones.
- Enlaces internos.
- Sitemap.
- Hreflang.
- Contenido.

No canonicalizar páginas con intención distinta solo porque comparten texto.

## Renderizado

Comprobar que:

- El contenido esencial aparezca sin interacción.
- Los enlaces sean rastreables.
- Metadata y canonicals sean estables.
- La hidratación no borre contenido.
- Los errores JS no oculten páginas.

Preferir la solución técnica más simple que preserve funcionalidad.

## Rendimiento

Core Web Vitals y experiencia importan, pero no reducir todo el SEO a una puntuación. Diagnosticar LCP, INP y CLS con datos de campo cuando existan.

## Internacionalización

Revisar:

- URLs por idioma o región.
- Hreflang recíproco.
- Canonicals compatibles.
- Contenido realmente localizado.
- Selector accesible.
- Redirecciones no intrusivas.

## Despliegues

Antes y después:

- Guardar línea base.
- Probar entorno.
- Verificar códigos.
- Rastrear muestra.
- Revisar metadata.
- Confirmar sitemap.
- Supervisar Search Console, logs y conversiones.



## Ampliación [ClickUp 2]: casos de indexación y lanzamiento

- **Página subida como código a mano y que no se indexa:** montarla **dentro del CMS** para que entre al sitemap y a los módulos. Checklist previa a publicar una página fuera del CMS: ¿entra al sitemap?, ¿noindex o robots?, ¿canonical?, ¿se solicitó la indexación?, ¿la puede administrar el equipo?
- **SPA y render:** validar con «ver código fuente» y no con el inspector; **404 real frente a soft-404**; quitar el noindex de producción el día de salida. Checklist completa en [launch-checklist-new-site.md](launch-checklist-new-site.md).
- **Categorías de blog vacías indexables:** riesgo de contenido delgado; documentar el criterio. Ver [on-page-metadata-and-urls.md](on-page-metadata-and-urls.md).
- **Rendimiento:** una sola pasada no es concluyente (tres como mínimo); los datos de campo tardan ~28 días en reflejar un cambio; **servidor primero** (hosting → caché → base de datos) antes de optimizar imágenes y CLS. Orden de ataque y esqueleto del plan en [ecommerce-seo-multicountry.md](ecommerce-seo-multicountry.md).
- **Seguridad e i18n:** cabeceras (CSP primero en Report-Only, HSTS, `X-Content-Type-Options`, `X-Frame-Options`), protección XSS/CSRF, librerías sin vulnerabilidades conocidas, `<html lang>` correcto por idioma y `hreflang` para evitar duplicados entre idiomas.
- **Sitemap y robots** (tarea corta): solo páginas esenciales indexables, actualización automática, enviar a Search Console y revisar el informe de estado, robots que controle lo no relevante y declare el sitemap.
- Trampas de medición y de WordPress con constructores visuales: [measurement-traps-and-diagnosis.md](measurement-traps-and-diagnosis.md) y [wordpress-technical-audit-checklist.md](wordpress-technical-audit-checklist.md).


## Detalle por tema (SEO Skills, 2026-10-30)
- Sintaxis, coincidencia de reglas, auditoría y generación de `robots.txt`: [robots-txt-audit-and-generation.md](robots-txt-audit-and-generation.md).
- HTML renderizado para sitios con JavaScript y comparación con el HTML inicial: [rendered-html-crawl.md](rendered-html-crawl.md).
- Auditoría general con categorías, pesos y puntuación: [audit-scoring-and-weights.md](audit-scoring-and-weights.md).
