---
tags:
  - seo
  - geo
  - schema
---

# Schema markup priorizado para citación en IA

## Índice

- Principio
- Estado de la evidencia
- Por qué JSON-LD sin excepción
- Los seis tipos a priorizar
- FAQPage tras el retiro del rich result (7 de mayo de 2026)
- HowTo tras el retiro del rich result (septiembre de 2023)
- `@graph`: conectar las entidades en un solo grafo
- Validación
- Errores frecuentes
- Lista de revisión

## Principio

El Schema markup no crea señales por sí solo (ver [structured-data-and-search-features.md](structured-data-and-search-features.md)): **traduce** las señales que ya existen —un caso de éxito, un artículo, la vocería de una persona— a un formato que un sistema de recuperación puede interpretar sin ambigüedad. Una señal que el modelo no entiende bien cuenta menos dentro de la Densidad de Señales (ver [signal-density-methodology-and-kpi.md](signal-density-methodology-and-kpi.md)). El schema es el empaque técnico de la evidencia, no la evidencia misma.

## Estado de la evidencia

| Afirmación | Estado | Origen |
|---|---|---|
| JSON-LD es el formato recomendado por Google y por los principales sistemas de IA | Confirmado, práctica estándar de la industria | Documentación de Google, consistente con lo ya registrado en `structured-data-and-search-features.md` |
| Google retiró el rich result de FAQPage por completo, incluidos gobierno y salud, el 7 de mayo de 2026 | **Verificado de forma independiente** | Múltiples reportes SEO del sector, mayo 2026 (ver fuentes al final) |
| Google descontinuó el rich result visual de HowTo desde septiembre de 2023 | Confirmado, hecho ya conocido de la industria | Anuncio de Google, 2023 |
| Los seis tipos de schema (Organization, Article, FAQPage, HowTo, Service, Person) son los que conviene priorizar para construir entidad ante LLMs, en ese orden | **Opinión editorial de Los Creativos**, framework propio sin benchmark publicado | Los Creativos — declaraciones atribuidas a Sebastián Londoño, Fabio Araujo, David Martínez Mata, Eddie Vélez Benjumea |
| `@graph` con `@id` mejora la legibilidad del grafo de entidad para un LLM | Práctica técnica estándar de JSON-LD (Schema.org lo documenta), la aplicación estratégica a GEO es interpretación de Los Creativos | Schema.org (técnica) + Los Creativos (aplicación) |

Las citas de personas con nombre (Sebastián Londoño, Fabio Araujo, David Martínez Mata, Eddie Vélez Benjumea, Juan David Uribe) son **opinión experta de agencia**, útiles como criterio editorial pero no como estudio independiente. Citarlas como tales si se reutilizan con un cliente.

## Por qué JSON-LD sin excepción

Microdata y RDFa mezclan el marcado dentro del HTML visible; JSON-LD vive en un bloque `<script type="application/ld+json">` separado del contenido, normalmente en el `<head>`. Ventaja operativa concreta: un cambio de texto no arriesga romper el marcado, y viceversa — el redactor y el desarrollador trabajan sin pisarse. Válido para cualquier plataforma (WordPress, Drupal, Shopify, VTEX, desarrollo a medida).

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Tu Empresa",
  "url": "https://tuempresa.com"
}
</script>
```

## Los seis tipos a priorizar

Cada tipo corresponde a uno o más tipos de señal de `signal-density-methodology-and-kpi.md`:

### 1. Organization — señal estructural

La "tarjeta de presentación" de la entidad. Sin ella, un modelo arma la identidad de la marca a partir de fragmentos sueltos. Propiedades clave: `name`, `logo`, `url`, `description`, y sobre todo **`sameAs`** apuntando a LinkedIn corporativo, perfiles verificados y directorios — cada enlace es una confirmación cruzada de identidad (ver `entity-presence-and-knowledge-graph.md`). Colocar en todas las páginas del sitio, no solo en el inicio: un modelo puede entrar por cualquier URL.

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Tu Empresa",
  "url": "https://tuempresa.com",
  "logo": "https://tuempresa.com/logo.png",
  "description": "Descripción breve de tu actividad principal",
  "sameAs": [
    "https://www.linkedin.com/company/tuempresa",
    "https://www.wikidata.org/wiki/tu-entidad"
  ]
}
```

### 2. Article — señal semántica y de autoridad

Confirma que un texto es contenido editorial completo, con autor y fecha identificables — no una página genérica. `author` conecta con un `Person` propio; `publisher` conecta con `Organization`, cerrando el círculo autor → marca. Actualizar `dateModified` cada vez que se revisa una pieza: es una señal barata de vigencia que casi nadie mantiene.

### 3. FAQPage — ver sección dedicada abajo

### 4. HowTo — ver sección dedicada abajo

### 5. Service — señal semántica orientada a B2B

Traduce lenguaje de marketing ambiguo ("soluciones integrales") en una oferta concreta que un sistema puede citar. `provider` conecta con `Organization`, `areaServed` define cobertura geográfica, `serviceType` nombra la categoría exacta. Un bloque por servicio, nunca uno genérico que cubre toda la oferta.

### 6. Person — señal de autoridad (vocería)

Convierte la vocería real (conferencias, entrevistas, publicaciones) de fundadores, directivos o especialistas en una entidad legible. Debe enlazarse desde `Article.author` y llevar `sameAs` hacia el perfil de LinkedIn. Cuando varios artículos llevan la firma de la misma persona con `Person` bien marcado, el patrón de autoría repetida refuerza tanto al autor como a la organización.

```json
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "Nombre del Experto",
  "jobTitle": "Cargo",
  "worksFor": { "@type": "Organization", "name": "Tu Empresa" },
  "sameAs": ["https://www.linkedin.com/in/perfil"]
}
```

## FAQPage tras el retiro del rich result (7 de mayo de 2026)

Cronología verificada: Google restringió el rich result de FAQ casi exclusivamente a sitios de gobierno y salud en agosto de 2023, y **lo retiró por completo, incluida esa excepción, el 7 de mayo de 2026**. Soporte en el reporte de Search Console y en Rich Results Test se retira en junio de 2026; en la API de Search Console, en agosto de 2026.

Esto es un retiro del **resultado visual**, no del vocabulario: `FAQPage` sigue siendo un tipo válido de Schema.org, Google sigue interpretándolo para entender la página (sin usarlo como fuente de despliegue visual), y sistemas distintos a la búsqueda de Google (ChatGPT, Claude, Perplexity) pueden seguir aprovechando esa estructura para construir sus propias respuestas.

Regla operativa: marcar solo preguntas que existen **visibles** en la página. Nunca usar `FAQPage` con fines promocionales o para preguntas no publicadas — Google lo señala explícitamente como mal uso, y la discrepancia entre marcado y contenido visible genera desconfianza en cualquier sistema que la detecte.

## HowTo tras el retiro del rich result (septiembre de 2023)

Google descontinuó el resultado visual de HowTo (pasos numerados con imágenes) desde septiembre de 2023, primero en móvil y luego en escritorio. Igual que con FAQPage, el retiro es del rich result, no de la utilidad estructural: una secuencia de pasos bien marcada facilita que un sistema conversacional cite un paso puntual sin tener que extraerlo de un párrafo largo.

Tres reglas de implementación:

1. Dividir el proceso en pasos genuinos e independientes — nunca un paso gigante que mezcla varias acciones.
2. Cada paso con nombre corto y texto explicativo autocontenido.
3. El orden del código debe coincidir exactamente con el orden visible; una discrepancia confunde al sistema que interpreta la secuencia.

## `@graph`: conectar las entidades en un solo grafo

En vez de dejar `Organization`, `Article` y `Person` como bloques sueltos, `@graph` los agrupa en un solo bloque JSON-LD con referencias cruzadas vía `@id`. Un `Article` puede apuntar directamente al `Person` de su autor, que a su vez apunta al `Organization` de la empresa — una red de entidades que un sistema puede recorrer, en vez de piezas aisladas que debe intentar relacionar por su cuenta.

```json
{
  "@context": "https://schema.org",
  "@graph": [
    { "@type": "Organization", "@id": "https://tuempresa.com/#organization", "name": "Tu Empresa" },
    { "@type": "Person", "@id": "https://tuempresa.com/#autor", "name": "Nombre del Experto",
      "worksFor": { "@id": "https://tuempresa.com/#organization" } },
    { "@type": "Article", "headline": "Título del Artículo",
      "author": { "@id": "https://tuempresa.com/#autor" },
      "publisher": { "@id": "https://tuempresa.com/#organization" } }
  ]
}
```

## Productos y software sin precio público

Sin precio público, marcar solo `SoftwareApplication` (o `WebApplication`/`MobileApplication`) con `name`, `description`, `applicationCategory`, `operatingSystem`, `url` y `publisher` apuntando al `@id` de la Organization. **Nunca** `offers` vacío, `Offer` sin precio, `price: 0` ni `"0.00"`: comunican «gratis» y es falso. Se renuncia al rich result de software si este exige `offers` o valoración (verificar la documentación vigente de Google): la exactitud manda. `aggregateRating` solo con reseñas reales y visibles. Productos del roadmap: sin schema de producto hasta que estén disponibles.

## Plugins SEO que ya generan el grafo (Rank Math, Yoast)

Rank Math emite un `@graph` con `#organization`, `#website` y `#webpage` (más breadcrumb, imagen principal y autor). No añadir bloques JSON-LD manuales con esas entidades: se duplican nodos con datos divergentes. Para completarlos: 1) usar los ajustes del plugin (Knowledge Graph o Local SEO, perfiles sociales → `sameAs`); 2) para propiedades que no ofrece, usar el filtro `rank_math/json_ld` en un mu-plugin, modificando el nodo existente por su `@id`. Ajustes y filtro son **globales** (afectan a todo el sitio): antes, guardar una foto del JSON-LD público de home, una página y un post; enviar el conjunto completo de campos, no solo el que se corrige; verificar después en las tres plantillas. Por eso un cambio así nunca se clasifica como riesgo Bajo (ver `technical-audit-by-finding.md`).

## Validación

Antes de publicar: Rich Results Test de Google + validador oficial de Schema.org confirman sintaxis. Monitorear Search Console después del despliegue para detectar errores nuevos — revisión recurrente, no evento único. Ver también la sección "Validación" de `structured-data-and-search-features.md`, que ya cubre coincidencia con contenido visible, URLs absolutas y ausencia de datos inventados.

## Errores frecuentes

- Marcar `FAQPage` con preguntas que no están visibles en la página.
- Presentar HowTo o FAQPage como si aún generaran un rich result visual en Google.
- Dejar `Organization` solo en la home en vez de en todas las páginas (si el plugin SEO ya la emite en todo el sitio, no duplicarla a mano).
- Dejar marcadores (`[PENDIENTE]`, `TBD`, `XXX`) dentro de un campo de schema: si el dato no existe, se omite el campo y se anota fuera del JSON-LD.
- Usar `Offer` vacío o `price` 0 para un producto sin precio público.
- Usar un solo bloque `Service` genérico para varios servicios distintos.
- Firmar artículos sin `Person` propio del autor, perdiendo la conexión autor → organización.
- No actualizar `dateModified` al revisar contenido existente.

## Lista de revisión

- ¿El marcado está en JSON-LD, separado del contenido visible?
- ¿`Organization` con `sameAs` está presente en todo el sitio, no solo en la home?
- ¿Cada artículo tiene `Article` conectado a un `Person` de autor real y a `Organization` como publisher?
- ¿Las preguntas marcadas en `FAQPage` existen visibles en la página?
- ¿Los pasos de `HowTo` están en el mismo orden en el código y en pantalla?
- ¿Cada servicio relevante tiene su propio bloque `Service`?
- ¿Se evaluó usar `@graph` para conectar las entidades en vez de dejarlas sueltas?
- ¿Se validó con Rich Results Test / validador de Schema.org antes de publicar?

Fuente primaria: [Schema markup para AI Search: qué datos estructurados priorizar](https://loscreativos.co/blog/schema-markup-para-ai-search-datos-estructurados-priorizar/) — Los Creativos, 19 de agosto de 2026. Autoría: Juan David Uribe Taquez, con citas de Sebastián Londoño, David Martínez Mata, Fabio Araujo y Eddie Vélez Benjumea.

Verificación externa del retiro de FAQPage: [FAQ Rich Results Deprecated: Google's May 2026 Change](https://www.getpassionfruit.com/blog/what-changed-with-google-drops-faq-rich-results-and-what-to-do-now), [Google FAQ Rich Results Removed in 2026](https://seocrawl.ai/blog/faq-structured-data-google-2026).
