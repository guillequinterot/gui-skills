<!-- GENERADO por tools/build_hosted.py desde skills/seo-content-system (v1.2.0, huella 679129108509). NO EDITAR A MANO: cambia la skill o hosted-src/ y regenera con `python tools/build_hosted.py`. -->

# SEO técnico y acceso de bots de IA

Rastreo, indexación, canonicals, renderizado, rendimiento, y la capa específica de bots de entrenamiento/recuperación de IA (robots.txt, llms.txt).

---

## Fuente original: `technical-seo-and-indexability.md`

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

---

## Fuente original: `technical-seo-lineamientos-generales.md`

# Lineamientos de SEO Técnico, Indexación y Resultados Enriquecidos

> Documento marco aportado por el mantenedor de la skill el 2026-08-12, incorporado como referencia estable de la skill `seo-content-system`. Es un documento marco y guía técnica general de estándares SEO diseñada para su implementación en cualquier sitio web o e-commerce. Se conserva verbatim como fuente de reglas técnicas; para aplicarlo a un proyecto concreto, cruzar con [technical-seo-and-indexability.md](technical-seo-and-indexability.md), [on-page-metadata-and-urls.md](on-page-metadata-and-urls.md), [image-seo-and-accessibility.md](image-seo-and-accessibility.md) y [structured-data-and-search-features.md](structured-data-and-search-features.md), que cubren el mismo terreno con más contexto editorial. Primera aplicación real: `caso-web-biotech-01` (ver el registro de trabajos de `HANDOFF.md`).

Este manual establece los criterios de rastreabilidad, indexabilidad, arquitectura de información, rendimiento (Performance), internacionalización y marcado de datos estructurados para maximizar la visibilidad orgánica en buscadores y la generación de resultados enriquecidos (Rich Results).

## 1. Lineamientos Técnicos para la Creación de URLs y Arquitectura de Información

### 1.1. Sintaxis, Formato y Buenas Prácticas de Estructura

- **Caracteres Permitidos:** Utilizar exclusivamente letras minúsculas (a-z), números (0-9) y guiones medios (-) como separador de palabras.
- **Caracteres Prohibidos:** Queda estrictamente prohibido el uso de mayúsculas, guiones bajos (_), espacios, acentos, tildes, la letra 'ñ' y símbolos especiales (&, %, $, #, ?, !, @).
- **Longitud y Concisión:** Mantener la URL por debajo de los 75-80 caracteres. Eliminar palabras vacías (*stop words*) e identificadores dinámicos que no aporten valor semántico.
- **Etiquetas de Enlace Interno:** Todos los enlaces deben utilizar la etiqueta HTML `<a href="URL">` explícita con un texto de ancla (*anchor text*) descriptivo. Evitar enlaces dinámicos controlados por eventos de JavaScript (ej. `onclick` o `javascript:void(0)`) que impidan el rastreo del bot.

### 1.2. Arquitectura de Información Jerárquica Recomendada

La estructura del sitio debe seguir una lógica piramidal limpia de máximo 3 o 4 niveles de profundidad desde la raíz:

```
Raíz (Home):           https://www.dominio.com/
Categoría Principal:   https://www.dominio.com/categoria-principal/
Subcategoría:          https://www.dominio.com/categoria-principal/subcategoria/
Página Final / PDP:    https://www.dominio.com/categoria-principal/subcategoria/nombre-producto-o-articulo
```

### 1.3. Canonicalización, Protocolo Seguro y Directivas del Servidor

- **Etiqueta Canónica Absoluta:** Toda página indexable debe incorporar en el `<head>` su versión canónica apuntando a la URL final con protocolo seguro HTTPS: `<link rel="canonical" href="https://www.dominio.com/categoria/pagina-ejemplo" />`
- **Redirecciones 301 Permanentes:**
  - Forzar redirección 301 de la versión HTTP hacia la versión HTTPS.
  - Forzar redirección 301 entre versiones con www y sin www para consolidar una sola versión maestra.
  - Implementar redirecciones 301 en caso de cambios de ruta o eliminación permanente de contenidos.
- **Prevención de Contenido Mixto (Mixed Content):** Cargar absolutamente todos los recursos estáticos (imágenes, fuentes, scripts, hojas de estilo) bajo el protocolo HTTPS.
- **Gestión de Parámetros de URL:** Bloquear parámetros de búsqueda interna, filtros o ordenamientos mediante el archivo robots.txt o etiquetado canónico para preservar el presupuesto de rastreo (*Crawl Budget*).

### 1.4. Tabla Comparativa General de Sintaxis de URLs

| Criterio | Estándar SEO Recomendado | Mala Práctica a Evitar |
| :---- | :---- | :---- |
| Formatos y Separadores | /calzado-deportivo-running | /Calzado_Deportivo_Running/ |
| Parámetros Dinámicos | /portatiles-gaming/laptops | /index.php?cat=45&item=98342 |
| Caracteres Especiales | /camisas-diseno-urbano | /camisas-diseño-urbano! |
| Profundidad de Niveles | /tecnologia/smartphones/modelo-x | /v2/items/cat/sub/prod/id/99/modelo-x |

## 2. Configuración Multi-idioma e Internacionalización (`hreflang`)

Cuando un sitio web opera en múltiples idiomas o regiones geográficas, es obligatorio utilizar la anotación `rel="alternate" hreflang="..."` para indicar al buscador la versión lingüística correspondiente y evitar penalizaciones por contenido duplicado.

### 2.1. Reglas Técnicas de Implementación

- **Reciprocidad Obligatoria:** Cada versión lingüística debe enlazar de forma bidireccional a todas las demás versiones del mismo contenido.
- **Formato de Códigos:** Utilizar el código de idioma ISO 639-1 (ej. es, en) combinado opcionalmente con el código de región ISO 3166-1 Alpha-2 (ej. es-CO, es-ES, en-US).
- **Fallback Global (x-default):** Incluir una etiqueta con el atributo `hreflang="x-default"` que dirija a la versión genérica o de aterrizaje internacional para usuarios que no coincidan con ningún idioma especificado.
- **Ubicación:** Implementar directamente en el `<head>` HTML de cada documento o dentro del Sitemap XML.

### 2.2. Plantilla de Código HTML para Multi-idioma

```html
<!-- Insertar en el <head> de todas las variantes de la página -->
<link rel="alternate" hreflang="es" href="https://www.dominio.com/es/pagina" />
<link rel="alternate" hreflang="es-CO" href="https://www.dominio.com/es-co/pagina" />
<link rel="alternate" hreflang="en" href="https://www.dominio.com/en/page" />
<link rel="alternate" hreflang="x-default" href="https://www.dominio.com/pagina" />
```

**Nota de aplicación:** solo aplica a sitios con más de una variante de idioma/región publicada. Un sitio de un solo idioma/país no necesita hreflang — no fabricar variantes para "cumplir" esta regla.

## 3. Lineamientos Técnicos para la Página Principal (Home)

### 3.1. Meta Etiquetas y Estructura Semántica HTML5

- **Meta Title:** Incluir el nombre de la marca y la propuesta principal de valor (50–60 caracteres). `<title>Nombre de Marca | Descripción de Propuesta de Valor</title>`
- **Meta Description:** Resumen persuasivo que incluya llamada a la acción implícita (140–155 caracteres). `<meta name="description" content="Descripción optimizada del sitio web para atraer clics orgánicos desde la SERP." />`
- **Directivas Robots:** `<meta name="robots" content="index, follow, max-image-preview:large" />`
- **Estructura Semántica HTML5:**
  - Usar etiquetas contenedoras semánticas: `<header>`, `<nav>`, `<main>`, `<section>`, `<article>` y `<footer>`.
  - El menú principal debe ser renderizado dentro de la etiqueta `<nav>` utilizando listas no ordenadas (`<ul><li><a href="...">Texto</a></li></ul>`).
  - **Jerarquía de Encabezados:** Debe existir **un único H1 por página** que resuma el propósito del sitio, seguido de H2s para secciones clave y H3s para bloques secundarios.
- **Marcado de Redes Sociales (Open Graph y Twitter Cards):**
  ```html
  <meta property="og:title" content="Título del Sitio Web" />
  <meta property="og:description" content="Descripción del sitio para redes sociales." />
  <meta property="og:image" content="https://www.dominio.com/assets/og-image.jpg" />
  <meta property="og:url" content="https://www.dominio.com/" />
  <meta name="twitter:card" content="summary_large_image" />
  ```

### 3.2. Schema Markup en JSON-LD para la Home

Integrar los esquemas globales de entidad de negocio (Organization) y funcionalidad del sitio (WebSite con caja de búsqueda):

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "https://www.dominio.com/#organization",
      "name": "Nombre de la Empresa",
      "url": "https://www.dominio.com/",
      "logo": {
        "@type": "ImageObject",
        "url": "https://www.dominio.com/assets/logo.png"
      },
      "sameAs": [
        "https://www.facebook.com/empresa",
        "https://www.instagram.com/empresa"
      ]
    },
    {
      "@type": "WebSite",
      "@id": "https://www.dominio.com/#website",
      "url": "https://www.dominio.com/",
      "name": "Nombre de la Marca",
      "publisher": { "@id": "https://www.dominio.com/#organization" },
      "potentialAction": {
        "@type": "SearchAction",
        "target": "https://www.dominio.com/buscar?q={search_term_string}",
        "query-input": "required name=search_term_string"
      }
    }
  ]
}
```

**Nota de aplicación:** el bloque `potentialAction`/`SearchAction` solo debe incluirse si el sitio tiene una búsqueda interna real en esa URL — no inventar un endpoint de búsqueda que no existe.

## 4. Lineamientos Técnicos para Páginas de Producto (PDP) y Fichas de Contenido

### 4.1. Meta Datos y Jerarquía

- **Title Tag:** `[Nombre del Producto/Artículo] - [Atributo/Variante] | [Nombre de Marca]`
- **Meta Description:** Incluir beneficios, características técnicas, disponibilidad y llamada a la acción.
- **H1 de Contenido:** Coincidir con la denominación oficial del producto o título de la entrada.

### 4.2. Protocolo para Optimización Multimedia (Peso, Formato y Rendimiento)

- **Límites de Peso de Archivos:**
  - Imágenes principales / Banners de cabecera (Hero Images): **< 100 KB – 150 KB**.
  - Imágenes de producto o contenido general: **< 70 KB – 100 KB**.
  - Miniaturas (Thumbnails) e iconos: **< 30 KB**.
- **Formatos de Nueva Generación:** Servir imágenes obligatoriamente en formatos de alta compresión **WebP** o **AVIF**.
- **Texto Alternativo (Alt Text):** Toda etiqueta `<img>` debe incluir un texto alternativo descriptivo y relevante: `alt="Descripción del producto o contenido de la imagen"`
- **Dimensiones Estáticas en HTML:** Definir siempre los atributos `width` y `height` explícitos para prevenir desplazamientos de diseño y proteger el indicador CLS.
- **Directivas de Carga Diferida (Lazy Loading) y Prioridad:**
  - Imagen principal (Hero / Above-the-fold): Usar `loading="eager" fetchpriority="high"` para maximizar la métrica LCP.
  - Imágenes secundarias o bajo la línea de visión (Below-the-fold): Usar `loading="lazy" decoding="async"`.

### 4.3. Schema Markup de Producto (JSON-LD)

```json
{
  "@context": "https://schema.org/",
  "@type": "Product",
  "name": "Nombre del Producto",
  "image": [
    "https://www.dominio.com/images/producto-1x1.jpg",
    "https://www.dominio.com/images/producto-4x3.jpg"
  ],
  "description": "Descripción técnica detallada del producto.",
  "sku": "SKU-12345",
  "mpn": "987654",
  "brand": { "@type": "Brand", "name": "Nombre de la Marca" },
  "review": {
    "@type": "Review",
    "reviewRating": { "@type": "Rating", "ratingValue": "5", "bestRating": "5" },
    "author": { "@type": "Person", "name": "Nombre de Usuario" }
  },
  "aggregateRating": { "@type": "AggregateRating", "ratingValue": "4.8", "reviewCount": "50" },
  "offers": {
    "@type": "Offer",
    "url": "https://www.dominio.com/categoria/subcategoria/nombre-producto",
    "priceCurrency": "USD",
    "price": "99.99",
    "priceValidUntil": "2026-12-31",
    "itemCondition": "https://schema.org/NewCondition",
    "availability": "https://schema.org/InStock",
    "seller": { "@type": "Organization", "name": "Nombre de la Marca" }
  }
}
```

**Nota de aplicación:** `review`/`aggregateRating` solo si existen reseñas reales verificables — nunca inventar calificaciones o conteos de reseñas para calificar a rich results. `price`/`availability` deben reflejar el precio y estado real del catálogo (ver [source-verification-and-evidence.md](source-verification-and-evidence.md)).

## 5. Rendimiento Técnico (Performance), Renderizado y Core Web Vitals

- **Renderización Server-Side (SSR / SSG):** En plataformas desarrolladas con librerías JavaScript (React, Vue, Angular, Next.js), priorizar Server-Side Rendering (SSR) o Static Site Generation (SSG) para que los motores de búsqueda rastreen el código HTML renderizado sin depender de la ejecución en el cliente.
- **Metas Core Web Vitals (Objetivos Oficiales de Google):**
  - **LCP (Largest Contentful Paint):** < 2.5 segundos.
  - **INP (Interaction to Next Paint):** < 200 milisegundos.
  - **CLS (Cumulative Layout Shift):** < 0.1.
- **Optimización de Scripts y Estilos:**
  - Minificar y comprimir archivos HTML, CSS y JavaScript.
  - Cargar scripts no críticos con los atributos `defer` o `async`.
  - Evitar la carga de hojas de estilo o bibliotecas JavaScript en páginas donde no sean utilizadas.
- **Políticas de Caché y CDN:** Configurar encabezados `Cache-Control` de larga duración para archivos estáticos y distribuir la carga del servidor mediante una red de CDN (Cloudflare, Fastly, AWS CloudFront).
- **Experiencia de Usuario (UX) Móvil:** No desplegar popups, interstitials o ventanas emergentes intrusivas que bloqueen la lectura del contenido principal en navegadores móviles.

## 6. Marcado Semántico Adicional para Resultados Enriquecidos (Rich Results)

### 6.1. Marcado de Preguntas Frecuentes (FAQPage Schema)

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "¿Pregunta frecuente del usuario?",
    "acceptedAnswer": { "@type": "Answer", "text": "Respuesta clara, concisa y estructurada para el usuario." }
  }]
}
```

### 6.2. Marcado de Migas de Pan (BreadcrumbList Schema)

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Inicio", "item": "https://www.dominio.com/" },
    { "@type": "ListItem", "position": 2, "name": "Categoría", "item": "https://www.dominio.com/categoria/" }
  ]
}
```

### 6.3. Esquemas Adicionales (Artículos, Recetas, Video)

- **Article / BlogPosting:** Obligatorio para publicaciones de blogs o contenidos informativos.
- **VideoObject:** Obligatorio para páginas que incluyan reproducciones de video integradas.
- **Recipe:** Para sitios dedicados al sector gastronómico o nutricional.

## 7. Matriz y Checklist Integral de Auditoría SEO Técnico

| Categoría | Ítem de Auditoría / Verificación | Requisito Estándar Aceptable |
| :---- | :---- | :---- |
| Indexabilidad y Servidor | Archivo robots.txt | Configurado correctamente bloqueando entornos de prueba/QA y enlaces dinámicos sin bloquear archivos CSS/JS. |
| Indexabilidad y Servidor | Redirecciones 301 | HTTP a HTTPS y no-www a www totalmente unificadas hacia una única versión. |
| Indexabilidad y Servidor | Estado del Sitemap XML | Libre de errores, incluye solo URLs con respuesta HTTP 200 OK y etiquetas canónicas. |
| Indexabilidad y Servidor | Detección de Enlaces 404 | Sin páginas rotas o enlaces internos huérfanos. |
| Indexabilidad y Servidor | Renderizado (SSR) | Contenido principal renderizado en el servidor y accesible desde el código fuente sin depender de JS. |
| Meta Data y Contenido | Meta Título y Descripción | Únicos por cada URL del sitio, respetando límites de caracteres y palabras clave prioritarias. |
| Meta Data y Contenido | Internacionalización (hreflang) | Anotaciones recíprocas configuradas para todos los idiomas/regiones con versión x-default. |
| Meta Data y Contenido | OpenGraph & Twitter Cards | Etiquetas declaradas para la previsualización de enlaces en plataformas sociales. |
| Seguimiento e Identificación | Herramientas de Analítica | Etiquetas de Google Search Console, Google Analytics 4 y Google Tag Manager instaladas sin conflictos. |
| Rendimiento (Performance) | Optimización de Imágenes | Formato WebP/AVIF, peso <150KB, atributo alt presente y dimensiones físicas definidas en el código HTML. |
| Rendimiento (Performance) | Core Web Vitals & Cargas | Métricas en rango verde (LCP <2.5s, INP <200ms, CLS <0.1). Scripts con atributos defer/async y CDN activo. |
| HTML5 y Semántica | Navegación y Encabezados | Uso de `<nav>` para menús, listas no ordenadas en footers y exactamente un H1 por URL. |
| Datos Estructurados (Schema) | Validación de JSON-LD | Implementación de esquemas Organization, WebSite, Product, BreadcrumbList y FAQPage sin advertencias técnicas. |

---

## Fuente original: `ai-crawler-access-and-llms-txt.md`

# Acceso de bots de IA: robots.txt, llms.txt y verificación

## Índice

- Principio
- Estado de la evidencia
- Bots de entrenamiento vs. bots de recuperación
- Auditar y configurar robots.txt
- El archivo llms.txt
- Cómo verificar que la configuración funciona en la práctica
- Errores frecuentes
- Lista de revisión

## Principio

Ninguna estrategia de contenido, Densidad de Señales o schema markup produce efecto si la infraestructura técnica bloquea el acceso de los bots de IA desde el origen. Esta es la capa que se revisa **antes** de cualquier trabajo editorial: de nada sirve construir señales si la puerta técnica está cerrada. Complementa el rastreo genérico ya cubierto en [technical-seo-and-indexability.md](technical-seo-and-indexability.md) con la capa específica de bots de IA, que ese archivo no distingue.

## Estado de la evidencia

| Afirmación | Estado | Origen |
|---|---|---|
| Existen bots de IA diferenciados por función (entrenamiento vs. recuperación) con nombres de user-agent específicos | Confirmado, documentado por los propios proveedores (OpenAI, Anthropic, Google) | Documentación pública de cada proveedor |
| Bloquear un bot de entrenamiento tiene efecto retardado (meses); bloquear uno de recuperación tiene efecto inmediato | Consistente con cómo funcionan ambos mecanismos (ver distinción entrenamiento/recuperación en [ai-citation-and-geo-playbook.md](ai-citation-and-geo-playbook.md)) | Framework Los Creativos, coherente con arquitectura conocida de los sistemas |
| `llms.txt` es un estándar propuesto por Jeremy Howard en 2024 | Confirmado, es un hecho verificable de la comunidad técnica | Propuesta pública de Jeremy Howard, 2024 |
| Adopción de `llms.txt` cercana al 10% entre sitios corporativos | **Cifra sin fuente identificable** citada por el artículo como "estimaciones recientes del sector" | Los Creativos, sin cita primaria — tratar como estimación no verificada |
| Casos y cifras de bloqueo (340 intentos de GPTBot, "casi la mitad de las empresas auditadas bloquean algún bot sin saberlo") | Anécdota/caso ilustrativo y cifra de la propia cartera de clientes de Los Creativos | Los Creativos, dato interno no auditable externamente |

## Bots de entrenamiento vs. bots de recuperación

Distinción operativa central, ya alineada con "entrenamiento vs. recuperación" de `ai-citation-and-geo-playbook.md`:

**Bots de entrenamiento** (rastrean para incorporar contenido en versiones futuras de un modelo; efecto retardado, medido en meses):
- `GPTBot` (OpenAI)
- `ClaudeBot` (Anthropic)
- `Google-Extended` (Google)

**Bots de recuperación** (rastrean en vivo para construir la respuesta que alguien recibe en el momento; efecto inmediato):
- `OAI-SearchBot` (OpenAI)
- `PerplexityBot` (Perplexity)
- `ChatGPT-User` (agente de usuario cuando una persona pide a ChatGPT que visite una URL)

**Postura por tipo de negocio (criterio, no regla universal):** una empresa cuyo contenido *es* el producto (medio, proveedor de datos) puede considerar bloquear bots de entrenamiento mientras deja abiertos los de recuperación, protegiendo propiedad intelectual sin perder visibilidad conversacional. Una empresa que vende productos o servicios normalmente gana más dejando ambos grupos sin restricción, porque su objetivo es visibilidad máxima, no protección editorial.

Decisión de bloqueo/apertura: corresponde a marketing (qué bots importan para el objetivo de negocio) y a tecnología (ejecutar la configuración) en conjunto — nunca delegada por completo a un solo equipo, y nunca heredada sin revisión de una plantilla o plugin de seguridad configurado por defecto.

## Auditar y configurar robots.txt

`robots.txt` vive en `tudominio.com/robots.txt` desde 1994. Es una solicitud, no una barrera técnica absoluta — pero los rastreadores serios de OpenAI, Anthropic y Google la respetan.

**Paso 1 — Auditar la configuración actual.** Abrir `tudominio.com/robots.txt` y revisar línea por línea. Buscar directivas genéricas tipo `User-agent: *` seguidas de `Disallow: /` heredadas de plantillas o plugins de seguridad — bloquean todo tráfico automatizado sin distinguir bots de IA legítimos de scrapers maliciosos.

**Paso 2 — Definir postura explícita por grupo de bots**, nunca dejarlo en una directiva genérica ambigua. Ejemplo para maximizar visibilidad (empresa que vende productos/servicios):

```text
User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: OAI-SearchBot
Allow: /
```

**Paso 3 — Mantener rutas sensibles bloqueadas para todos los bots por igual** (paneles administrativos, áreas de cliente, contenido interno) — abrir la puerta a la IA no implica exponer lo que ninguna audiencia externa debería consultar.

**Paso 4 — Referenciar el sitemap dentro del mismo archivo**: `Sitemap: https://tudominio.com/sitemap.xml`. Confirmar que esa URL responde 200, no 404.

**Paso 5 — Validar tras cada cambio**: herramientas de verificación de robots.txt (Search Console y equivalentes) confirman sintaxis; revisar logs de servidor durante dos o tres semanas después del ajuste para confirmar que la actividad de los bots relevantes efectivamente cambió.

## El archivo llms.txt

Estándar propuesto por Jeremy Howard en 2024: un archivo Markdown simple en la raíz del dominio (`tudominio.com/llms.txt`) que entrega a un modelo una lista curada de las páginas más relevantes del sitio, sin que tenga que interpretar HTML completo con menús, banners y elementos decorativos. Ejemplo público: `https://loscreativos.co/llms.txt`. Vercel también publica el suyo.

Contenido básico: nombre de la empresa, descripción breve, enlaces organizados a las secciones más importantes (casos de éxito, servicios principales, contenido educativo destacado).

**No reemplaza nada, complementa:** `robots.txt` abre la puerta de acceso; `llms.txt` orienta la atención una vez adentro; el schema markup (ver [schema-markup-for-ai-citation.md](schema-markup-for-ai-citation.md)) confirma el significado exacto de cada pieza. Los tres trabajan juntos.

La cifra de adopción ("~10% de sitios corporativos") no tiene fuente primaria identificable en el artículo — tratarla como estimación de sector sin verificar, útil para argumentar oportunidad temprana pero no para citar como dato duro frente a un cliente.

## Cómo verificar que la configuración funciona en la práctica

- **Logs de servidor, revisión mensual**: filtrar por los user-agents relevantes (`GPTBot`, `ClaudeBot`, `PerplexityBot`, `OAI-SearchBot`) y confirmar si la frecuencia de visitas crece o cae mes a mes.
- **Probar desde ubicaciones distintas**, no solo desde la red de la oficina: reglas de CDN o firewall pueden variar por país de origen de la solicitud.
- **Validar el schema en cada publicación nueva** como paso obligatorio del flujo editorial, no como revisión ocasional.
- **Verificación cualitativa trimestral**: preguntar directamente a ChatGPT, Perplexity y Gemini sobre la categoría de la empresa y confirmar si la marca aparece mencionada.
- **Documentar cada hallazgo** en un reporte compartido entre marketing y tecnología (fecha, bots detectados, errores corregidos, menciones observadas) — evita que el mismo problema se repita sin que nadie recuerde cómo se resolvió antes.

Advertencia operativa: una configuración correcta hoy puede quedar obsoleta sin aviso tras un cambio de plataforma, un plugin nuevo o una actualización de seguridad no coordinada con marketing. La revisión recurrente importa tanto como la configuración inicial.

## Errores frecuentes

- Heredar `Disallow: /` genérico de una plantilla o plugin de seguridad sin revisarlo nunca.
- Delegar la decisión de qué bots permitir exclusivamente a tecnología, sin criterio de negocio de marketing.
- Bloquear bots de IA pensando que son scrapers maliciosos sin verificar el user-agent real.
- Omitir la línea `Sitemap:` dentro de robots.txt.
- Publicar `llms.txt` una sola vez y no mantenerlo sincronizado con contenido nuevo relevante.
- Auditar la configuración una sola vez en vez de revisarla con frecuencia recurrente.
- Presentar la cifra de adopción de `llms.txt` (~10%) como dato verificado con fuente primaria.

## Lista de revisión

- ¿Se revisó robots.txt línea por línea buscando `Disallow: /` heredado?
- ¿Existe una postura explícita y documentada por tipo de bot (entrenamiento vs. recuperación), decidida junto con marketing?
- ¿Las rutas sensibles quedan bloqueadas para todos los bots por igual?
- ¿robots.txt referencia el sitemap y el sitemap responde 200?
- ¿Existe `llms.txt` publicado y actualizado con las secciones más relevantes?
- ¿Se revisan logs de servidor con frecuencia mensual filtrando por los user-agents de IA?
- ¿Se hizo la prueba cualitativa trimestral preguntando directamente a ChatGPT/Perplexity/Gemini?
- ¿Existe un reporte compartido entre marketing y tecnología con la fecha de cada revisión?

Fuente primaria: [Checklist técnico para que los motores de IA puedan rastrear tu sitio](https://loscreativos.co/blog/acciones-para-que-motores-ia-rastreen-sitio-web/) — Los Creativos, 19 de agosto de 2026. Autoría: Juan David Uribe Taquez, con citas de Fabio Araujo, David Martínez Mata y Esteban Ortiz.
