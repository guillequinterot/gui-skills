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

