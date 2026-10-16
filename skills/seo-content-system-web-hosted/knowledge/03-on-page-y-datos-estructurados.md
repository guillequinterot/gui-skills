<!-- GENERADO por tools/build_hosted.py desde skills/seo-content-system (v1.2.0, huella a9679cd8226a). NO EDITAR A MANO: cambia la skill o hosted-src/ y regenera con `python tools/build_hosted.py`. -->

# On-page, imágenes y datos estructurados

Metadatos, URLs, SEO de imágenes, y priorización de Schema markup orientada tanto a Google como a citación en sistemas de IA.

---

## Fuente original: `on-page-metadata-and-urls.md`

# SEO on-page, metadatos y URLs

## Índice

- Paquete por página
- Title
- Metadescripción
- H1 y encabezados
- Slugs
- Cambios de URL
- QA

## Paquete por página

Entregar cuando aplique:

```text
URL:
Keyword e intención:
Title:
Metadescripción:
H1:
Slug:
H2/H3:
Canonical:
Robots:
Enlaces:
Imágenes:
Schema:
CTA:
KPI:
```

## Title

Crear un title:

- Único.
- Descriptivo.
- Coherente con la página.
- Diferenciado de otras URLs.
- Natural.
- Con marca cuando aporte reconocimiento.

Usar 50–60 caracteres como referencia editorial, no como garantía. Los buscadores pueden construir otro title link.

Evitar:

- Repetición de keywords.
- Titles idénticos en muchas páginas.
- Promesas ausentes del contenido.
- Plantillas que ocultan el tema.

## Metadescripción

Resumir el valor real de la página. Incluir detalles concretos, intención y diferenciador. Un rango de 140–160 caracteres puede ayudar a editar, pero no garantiza el fragmento mostrado.

No:

- Duplicar descripciones.
- Rellenar con listas de keywords.
- Inventar precios, ubicaciones o beneficios.
- Repetir el title sin ampliar.

## H1 y encabezados

Usar un H1 principal que describa la página. No es obligatorio que sea idéntico al title. Mantener una jerarquía semántica y no elegir niveles por tamaño visual.

## Slugs

Preferir:

- Minúsculas.
- Guiones.
- Brevedad suficiente.
- Palabras descriptivas.
- Estabilidad.

Evitar fechas innecesarias, parámetros indexables sin control, stopwords acumuladas y keyword stuffing.

## Cambios de URL

Antes de cambiar una URL existente:

1. Verificar tráfico, enlaces, rankings y uso externo.
2. Definir destino equivalente.
3. Crear redirección 301.
4. Actualizar enlaces internos, canonical, hreflang y sitemap.
5. Probar códigos y cadenas.
6. Supervisar Search Console y logs.

No redirigir muchas páginas diferentes a una home genérica.

## QA

- Title y H1 representan el contenido.
- Metadescripción no promete de más.
- Slug coincide con la arquitectura.
- Canonical es correcto.
- La página puede indexarse si debe.
- No existe duplicación evitable.

---

## Fuente original: `image-seo-and-accessibility.md`

# SEO de imágenes y accesibilidad

## Índice

- Elementos distintos
- Texto alternativo
- Imágenes enlazadas
- Archivo y contexto
- Rendimiento
- Entregable

## Elementos distintos

- **Nombre de archivo:** organización y descripción técnica.
- **Alt:** alternativa textual según función y contexto.
- **Caption:** contexto visible adicional.
- **Título de biblioteca:** organización en el CMS.
- **Atributo HTML `title`:** información complementaria opcional.

No rellenar todos por rutina ni copiar la misma frase.

## Texto alternativo

### Informativa

Describir la información necesaria para comprender la imagen dentro del contexto.

### Decorativa

Usar `alt=""` para permitir que la tecnología asistiva la ignore.

### Funcional

Describir la acción o destino, no la apariencia del botón.

### Compleja

Ofrecer un resumen en el alt y una explicación extensa próxima o enlazada para gráficos, diagramas y mapas.

Evitar:

- “Imagen de” salvo que el tipo de recurso sea relevante.
- Keyword stuffing.
- Detalles visuales que no cambian significado.
- Dejar vacío el alt de una imagen funcional.
- Usar `title` como sustituto.

## Imágenes enlazadas

El alt puede funcionar como texto de enlace. Debe describir el destino o la acción cuando la imagen es el único contenido del enlace.

## Archivo y contexto

Usar nombres legibles:

```text
auditoria-seo-search-console.webp
```

No:

```text
IMG_00492-final-final2.webp
seo-seo-agencia-seo-medellin.webp
```

Colocar la imagen cerca del texto relacionado. Mantener consistencia entre alt, caption y contexto sin duplicación innecesaria.

## Rendimiento

Evaluar:

- Dimensiones reales.
- Formato.
- Compresión.
- `srcset` y `sizes`.
- Lazy loading fuera del viewport.
- Reserva de espacio para evitar desplazamientos.
- Prioridad de la imagen principal.
- Sitemap de imágenes cuando sea pertinente.

No degradar la calidad esencial ni cargar imágenes críticas demasiado tarde.

## Entregable

| Archivo | Función | Alt | Caption | Title HTML | Página |
|---|---|---|---|---|---|
| nombre.webp | Informativa | Texto contextual | Opcional | Omitir salvo necesidad | URL |

---

## Fuente original: `structured-data-and-search-features.md`

# Datos estructurados y funciones de búsqueda

## Índice

- Principio
- Selección
- Limitaciones
- Validación
- Cambios
- Lista de control

## Principio

El schema describe entidades y contenido visibles. No crea por sí solo autoridad, calidad ni derecho a un resultado enriquecido.

## Selección

Secuencia:

```text
Contenido visible
→ tipo real de entidad
→ documentación actual
→ propiedades aplicables
→ marcado
→ validación
→ seguimiento
```

Usar Schema.org para vocabulario y la documentación del buscador para compatibilidad de funciones.

## Limitaciones

- No existe un schema especial obligatorio para AI Overviews o AI Mode.
- `Article` describe autoría, fechas y publicación; no certifica E-E-A-T.
- `FAQPage` puede ser semánticamente válido aunque Google limite su rich result — **retirado por completo el 7 de mayo de 2026**, incluida la excepción que quedaba para sitios de gobierno y salud (verificado externamente, ver fuentes en [schema-markup-for-ai-citation.md](schema-markup-for-ai-citation.md)). El vocabulario sigue siendo válido; lo que desaparece es el despliegue visual en Google, no la utilidad para otros sistemas.
- `HowTo` no debe prometer un rich result que ya no existe (descontinuado desde septiembre de 2023).
- `Speakable` tiene disponibilidad limitada.
- `DefinedTerm` describe conceptos; no garantiza visibilidad especial.

Verificar siempre el estado actual antes de recomendar una implementación. Para priorización de tipos orientada a GEO/citación en LLMs (Organization, Article, FAQPage, HowTo, Service, Person y la técnica `@graph`), ver [schema-markup-for-ai-citation.md](schema-markup-for-ai-citation.md).

## Validación

Comprobar:

- JSON válido.
- Tipo correcto.
- Propiedades requeridas y recomendadas.
- Coincidencia con contenido visible.
- URLs absolutas y canónicas.
- Fechas y zonas horarias.
- Identificadores consistentes.
- Ausencia de reseñas, precios o disponibilidad inventados.

Usar validadores pertinentes y revisar Search Console después del despliegue.

## Cambios

Registrar:

```text
Tipo:
Página:
Motivo:
Documentación consultada:
Fecha:
Resultado esperado:
Resultado observado:
```

No retirar marcado útil solo porque no produce una función visual, si sigue describiendo correctamente la entidad y no causa problemas.

## Lista de control

- ¿Existe contenido visible equivalente?
- ¿El tipo representa la entidad real?
- ¿La función sigue vigente?
- ¿El marcado valida?
- ¿La expectativa se comunicó sin garantías?
- ¿Se medirá el resultado?

---

## Fuente original: `schema-markup-for-ai-citation.md`

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

## Validación

Antes de publicar: Rich Results Test de Google + validador oficial de Schema.org confirman sintaxis. Monitorear Search Console después del despliegue para detectar errores nuevos — revisión recurrente, no evento único. Ver también la sección "Validación" de `structured-data-and-search-features.md`, que ya cubre coincidencia con contenido visible, URLs absolutas y ausencia de datos inventados.

## Errores frecuentes

- Marcar `FAQPage` con preguntas que no están visibles en la página.
- Presentar HowTo o FAQPage como si aún generaran un rich result visual en Google.
- Dejar `Organization` solo en la home en vez de en todas las páginas.
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
