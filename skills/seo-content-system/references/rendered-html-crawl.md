---
tags:
  - seo
  - technical
---

# Rastreo con HTML renderizado

## Índice

- Cuándo hace falta
- Estado de la evidencia
- Entradas y reglas
- Dos formas de rastrear
- Qué se mide
- Qué se analiza
- Límites

Complementa [technical-seo-and-indexability.md](technical-seo-and-indexability.md) (sección "Renderizado") con un procedimiento concreto para obtener el HTML **después** de ejecutar JavaScript. Las herramientas de rastreo ya instaladas (Screaming Frog con renderizado, o `web_probe.py` de la skill `rea-reverse-engineer`) cubren el mismo propósito; este archivo describe la alternativa con Cloudflare Browser Rendering.

## Cuándo hace falta

| Sitio | Qué usar |
|---|---|
| Con mucho JavaScript (SPA, Angular, Next.js sin renderizado en servidor) | **Obligatorio** el HTML renderizado antes de auditar |
| Estático o WordPress | Basta la extracción por HTTP |
| Hay duda de si el contenido depende de JavaScript | Extraer **las dos versiones** y comparar `title`, H1 y enlaces entre HTML inicial y renderizado |

Si el H1, el contenido o los enlaces solo existen en el HTML renderizado, el riesgo es de renderizado: Google puede tardar en ver ese contenido o no verlo, y otros rastreadores (muchos bots de IA no ejecutan JavaScript) no lo verán.

## Estado de la evidencia

Procedimiento tomado de la skill `crawler` de `seo-skills.com` (Jorge Jaramillo, consultada el 2026-10-30; repositorio sin licencia declarada, por eso está reformulado). **No se ha probado en este entorno** (ver `HANDSHAKE.md`). Las rutas de la API de Cloudflare y los permisos del token cambian: antes de usarlo, leer la documentación vigente de Cloudflare Browser Rendering.

## Entradas y reglas

**Entradas:** URL de partida; una sola URL o varias (con límite de páginas, por defecto 10, y fuente de descubrimiento: `sitemaps`, `links` o `all`); credenciales de cuenta y token de Cloudflare con permiso de edición sobre Browser Rendering.

**Reglas**

- **El token nunca aparece** en un comando, un archivo, un informe ni el chat. Se carga solo desde un archivo `.env` fuera del repositorio.
- Se guarda **HTML, no Markdown**: el HTML es la fuente de verdad.
- Se respeta robots.txt y las protecciones anti-bot. Si el sitio bloquea el rastreador, se informa; no se intenta evadir.
- Revisar los límites del plan gratuito antes de un rastreo grande.
- Los resultados de un rastreo masivo permanecen en Cloudflare unos 14 días: si el trabajo terminó, la descarga se puede repetir con el mismo identificador de trabajo.

## Dos formas de rastrear

**Una URL o unas pocas:** una llamada por URL que devuelve el HTML ya renderizado. Conviene rechazar imágenes, vídeo, fuentes y hojas de estilo (más rápido), esperar a que la red se calme y poner un tiempo máximo (unos 30 segundos). Si la respuesta es un error, anotarlo y seguir. Mantener un manifiesto con URL, estado y archivo.

**Varias URLs:** trabajo asíncrono.

1. **Iniciar** con un límite, la fuente de descubrimiento, formato HTML y renderizado activado (con renderizado desactivado es más rápido y sirve para sitios estáticos).
2. **Esperar** consultando el estado cada unos 10 segundos hasta que deje de estar "en curso". Estados finales: completado, con error, cancelado por límites, cancelado por tiempo.
3. **Descargar** por páginas con cursor (necesario por encima de unos 10 MB), separar un `.html` por URL, armar el manifiesto y contar por estado.

Después, extraer las métricas del directorio de salida con el mismo extractor que usan las demás auditorías, para que alimente la auditoría general ([audit-scoring-and-weights.md](audit-scoring-and-weights.md)), el enlazado ([internal-linking-and-conversion-paths.md](internal-linking-and-conversion-paths.md)) y las imágenes ([image-seo-and-accessibility.md](image-seo-and-accessibility.md)).

## Qué se mide

| Indicador | Cómo se lee |
|---|---|
| Páginas descargadas | Cobertura del rastreo |
| Errores 4xx y 5xx | Hallazgos de estado |
| URLs no descargadas (omitidas, bloqueadas, canceladas) | Cruzar con robots.txt ([robots-txt-audit-and-generation.md](robots-txt-audit-and-generation.md)) |
| Promedio de palabras | Contexto |
| Contenido delgado (menos de 300 palabras) | Estado según el porcentaje de páginas afectadas |
| Páginas sin H1 tras renderizar | Pista: si no está en el HTML renderizado, tampoco lo ve Google |

Estados para contenido delgado y H1 ausente: **bueno** si ninguna página está afectada, **aviso** si menos del 30 % de las páginas, **malo** en cualquier otro caso.

También sirve una tabla de páginas rastreadas (URL, estado, título, palabras, enlaces internos) ordenada por número de palabras.

## Qué se analiza

- Páginas con error o vacías tras renderizar (sin título o sin H1): contenido que depende de JavaScript y falla.
- Contenido que **solo aparece al renderizar**, al comparar con la extracción por HTTP.
- Secciones del sitio que no aparecen en el rastreo (bloqueadas, sin enlazar o fuera del sitemap).
- URLs bloqueadas por robots.txt.

## Límites

Esta herramienta mide **cobertura**, no calidad: por eso **no asigna puntuación**. Una cobertura completa no dice que el contenido sea bueno, y una cobertura baja puede deberse al plan, al límite o a un bloqueo del sitio. Documentar siempre cuál fue la causa antes de sacar conclusiones.

Fuente: SEO Skills, skill `crawler` (Jorge Jaramillo), https://seo-skills.com/crawler, consultada el 2026-10-30.
