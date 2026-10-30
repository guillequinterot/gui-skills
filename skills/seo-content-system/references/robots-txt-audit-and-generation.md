---
tags:
  - seo
  - technical
  - geo
---

# robots.txt: auditar, validar y generar

## Índice

- Tres modos
- Estado de la evidencia
- Datos que hay que reunir
- Cómo se lee un robots.txt (RFC 9309 y comportamiento de Google)
- Orden de análisis
- Bots de referencia
- Generar un robots.txt
- Puntuación
- Reglas
- Errores frecuentes

Este archivo es el detalle de sintaxis y evaluación. La **postura de negocio** sobre bots de IA (entrenamiento frente a recuperación) y el archivo `llms.txt` están en [ai-crawler-access-and-llms-txt.md](ai-crawler-access-and-llms-txt.md); el rastreo en general, en [technical-seo-and-indexability.md](technical-seo-and-indexability.md).

## Tres modos

- **Auditar** el archivo publicado.
- **Validar** un borrador antes de subirlo.
- **Generar** uno nuevo.

Los tres terminan en un informe con el archivo actual, el propuesto y la evidencia de cada hallazgo. El archivo es pequeño: se lee completo, no hace falta un script.

**Entradas:** el dominio o el texto pegado; para generar, la plataforma (WordPress, Shopify, Next…) y la **política de IA** (bloquear entrenamiento, bloquear todo, permitir todo). Si no se menciona una política de IA, no se añade ningún bloque de IA. Rutas concretas que el usuario quiera probar, opcional.

## Estado de la evidencia

Sintaxis y reglas de coincidencia: RFC 9309 y la documentación de Google sobre robots.txt (fuentes primarias; ver [official-source-register.md](official-source-register.md)). La **lista de bots** y el **sistema de puntuación** vienen de la skill `robots` de `seo-skills.com` (Jorge Jaramillo, consultada el 2026-10-30; el repositorio no declara licencia, por eso aquí está reformulado). La lista de user-agents **no se verificó** contra la documentación de cada proveedor: antes de bloquear un bot en un cliente real, confirmar su nombre y su función en la documentación del proveedor, porque los nombres cambian.

## Datos que hay que reunir

1. Descargar `robots.txt` y anotar **estado HTTP, tamaño y URL final** (puede haber redirección).
2. Por cada línea `Sitemap:`, comprobar que responde y tomar una muestra de hasta unas 30 URLs.
3. Si es un índice de sitemaps, repetir en uno o dos sitemaps hijos.
4. Decir el tamaño de la muestra ("30 de 1.200 URLs probadas").

## Cómo se lee un robots.txt (RFC 9309 y comportamiento de Google)

**Sintaxis**

- Directivas válidas: `User-agent`, `Allow`, `Disallow`, `Sitemap` y `Crawl-delay` (Google la ignora). Cualquier otra es un error.
- Un **grupo** es una o más líneas `User-agent` seguidas de reglas. Una regla antes de cualquier `User-agent` es un error.
- Los nombres de directiva no distinguen mayúsculas; las **rutas sí**.
- `Disallow:` vacío permite todo. `Sitemap:` va fuera de los grupos y con URL absoluta.
- Estado HTTP del archivo: **404** = todo permitido; **5xx** = Google deja de rastrear el sitio mientras dure; si pesa más de **500 KiB**, se trunca y lo que sobra se ignora.

**Qué grupo se aplica a un bot**

- Se usa el grupo cuyo `User-agent` coincide de la forma **más específica**.
- Si el bot tiene grupo propio, **ignora por completo el grupo `*`**. Este es el origen de muchos errores: un bot con grupo propio no hereda los `Disallow` de `*`.
- Google sí fusiona varios grupos que declaran el mismo user-agent.

**Qué regla gana para una URL** (se compara contra ruta más parámetros)

1. Se toman todas las reglas del grupo aplicable cuyo patrón coincide con el inicio de la ruta. `*` equivale a cualquier secuencia; `$` ancla al final.
2. Gana el patrón **más largo** (por caracteres).
3. Si empatan, gana `Allow`. Si nada coincide, la URL está permitida.

## Orden de análisis

1. **Indexación.** Aplicar las reglas de Googlebot a la muestra del sitemap y a las rutas del usuario. Una URL del sitemap bloqueada es de gravedad alta o crítica. Comprobar si se bloquea CSS o JavaScript necesario para renderizar.
2. **Sitemaps.** Declarados, con URL absoluta, que responden 200 y contienen páginas que existen.
3. **Presupuesto de rastreo.** En sitios grandes: búsqueda interna, filtros o facetas y parámetros de orden sin bloquear.
4. **Bots de IA.** Por cada bot de referencia, decidir si está bloqueado (`Disallow`) o sin regla propia (cae bajo `*`). Error común: bloquear los bots de búsqueda al querer bloquear solo el entrenamiento.
5. **Seguridad.** Rutas sensibles expuestas: el archivo es público y listar una ruta la anuncia. La protección real va en el servidor, no en robots.txt.
6. **Malentendidos.** `Disallow` no es `noindex`: al bloquear una URL, Google no puede leer su canonical ni su `noindex`, y la URL aún puede aparecer indexada sin descripción.

## Bots de referencia

Solo sirve para decidir qué bloquear. No se escribe un grupo por cada bot.

| Tipo | Bots |
|---|---|
| Entrenamiento (13) | GPTBot, ClaudeBot, anthropic-ai, Google-Extended, Applebot-Extended, CCBot, Bytespider, Meta-ExternalAgent, FacebookBot, Amazonbot, cohere-training-data-crawler, Diffbot, AI2Bot |
| Búsqueda y agente de usuario de IA (7) | OAI-SearchBot, ChatGPT-User, Claude-SearchBot, Claude-User, PerplexityBot, Perplexity-User, DuckAssistBot |
| Buscadores (2) | Googlebot, Bingbot |

Recordatorio de la distinción de fondo (detalle en [ai-crawler-access-and-llms-txt.md](ai-crawler-access-and-llms-txt.md)): bloquear un bot de **entrenamiento** tiene efecto diferido; bloquear uno de **búsqueda o de agente de usuario** corta la visibilidad conversacional de inmediato.

## Generar un robots.txt

- **Solo `Disallow`**, y solo para rutas **confirmadas** en el sitio (sitemap, navegación o el usuario). Nunca rutas inventadas.
- Escribir `User-agent: *` y **grupos solo para los bots que se quiere bloquear**. Nada de grupos para bots permitidos y nada de `Allow: /` para Googlebot: no hace falta, y un grupo propio vuelve a ese bot ciego a las reglas de `*`.
- Si por algún motivo un bot permitido necesita grupo propio, **repetir en ese grupo los `Disallow` de rutas sensibles** del grupo `*`.
- Orden: grupo `*`, grupos de bots bloqueados (entrenamiento o búsqueda, según la política), líneas `Sitemap:` al final.
- Sin comentarios ni cabeceras decorativas.
- Antes de entregar: pasar la revisión de sintaxis, probar la muestra del sitemap y confirmar que **nada indexable queda bloqueado**.

## Puntuación

Parte de 100 y resta:

| Causa | Puntos |
|---|---|
| Todo el sitio bloqueado, o URLs importantes del sitemap bloqueadas | −40 |
| Respuesta 5xx del archivo | −25 |
| CSS o JavaScript necesario para renderizar bloqueado | −15 |
| Sin sitemap declarado, o roto | −10 |
| Cada error de sintaxis | −5 |
| Política de IA inconsistente | −5 |

Mínimo 0. Si se integra en una auditoría general, esta nota alimenta la categoría "Rastreo e indexación" de [audit-scoring-and-weights.md](audit-scoring-and-weights.md).

## Reglas

- **Nunca se modifica el robots.txt en vivo.** Se entrega la versión propuesta lista para copiar y la actual para comparar.
- Al probar URLs, mostrar la **regla ganadora** de cada una: es la evidencia del hallazgo.
- Si la muestra es pequeña, decirlo.

## Errores frecuentes

- Escribir `Allow: /` explícito para cada bot de IA y creer que así solo se "abre la puerta": cada grupo propio anula las reglas de `*` para ese bot.
- Confundir `Disallow` con `noindex`.
- Rutas sensibles protegidas solo con robots.txt.
- Archivo que devuelve 5xx durante un despliegue y deja de rastrearse el sitio.
- Sitemap declarado con URL relativa o que redirige.

Fuente: SEO Skills, skill `robots` (Jorge Jaramillo), https://seo-skills.com/robots, consultada el 2026-10-30; sintaxis según RFC 9309 y la documentación de Google.
