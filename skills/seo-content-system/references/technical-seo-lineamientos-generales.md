---
tags:
  - seo
---

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
