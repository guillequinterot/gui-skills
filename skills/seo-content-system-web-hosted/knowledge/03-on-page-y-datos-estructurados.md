<!-- GENERADO por tools/build_hosted.py desde skills/seo-content-system (v1.5.0, huella dd19e06bf59f). NO EDITAR A MANO: cambia la skill o hosted-src/ y regenera con `python tools/build_hosted.py`. -->

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



## Ampliación [ClickUp 2]: reglas por cliente y sobre-optimización

- **Longitudes: regla por cliente.** Los rangos de otros documentos (title ≈ 30-60, meta ≈ 120-160) son valores por defecto. Cuando el cliente fije los suyos, manda su regla: un caso real trabajó con **58 caracteres para el title y 140 para la meta description** («más que optimizar, ajustar a la extensión»). Registrar la regla del cliente en el HANDOFF del proyecto.
- **Sobre-optimización.** Fijar un máximo de repeticiones de la keyword exacta por documento y tratar como alarma casos como una keyword repetida ~30 veces. Variar con naturalidad (ver principios 6, 7 y 11 de `SKILL.md`).
- **H2 en páginas de programa o de servicio:** el valor para el usuario (qué aprenderá, resultados, convenios) va antes que «desde dónde estudiar» o «dónde estamos». Los H2 internos pueden ser más cortos que los H2 de SEO cuando los títulos largos se ven mal (compromiso SEO/UX).
- No tocar el nombre oficial de un producto o programa; revisar la nomenclatura con el cliente. Un H1 duplicado se corrige **a nivel de plantilla**, no página a página.
- **H2 en forma de pregunta** para landings de servicio, ciudad o industria (lista de 21 variantes usada como plantilla) más los módulos a añadir (instituciones, ciudades). «Humanizar» una landing: texto natural en el idioma de la audiencia, sin rebuscar, con enlaces, módulos y FAQs hiperpersonalizadas.
- **Taxonomías y categorías del blog:** plantilla única de archivo administrable, tarjetas, paginación y mensaje de vacío estándar. Si se dejan indexables categorías vacías, marcarlo como **riesgo de contenido delgado** y documentar el motivo y la alternativa (`noindex` hasta tener entradas). Verificar en el código fuente, no en el inspector.
- **SEO + CRO en on-page:** CTA claro por tipo de página, banners de conversión, página de gracias para medir y mapas de calor sobre las transaccionales prioritarias.


## Procedimiento de redacción (SEO Skills, 2026-10-30)
Para producir title y metadescripción de forma repetible (tres opciones, conteo de caracteres, reglas de puntuación, límites por tanda y salida estructurada), ver [title-and-description-generation.md](title-and-description-generation.md). Ojo con los rangos: uno es el de **auditoría** (title 30 a 60, descripción 70 a 160) y otro el de **redacción** (title 45 a 55, descripción 150 a 160, nunca más de 165). La regla del cliente manda sobre ambos.

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



## Ampliación [ClickUp 2]: reglas de archivo y flujo con diseño

- **Imagen destacada de artículo:** `.webp`, **menos de 100 kB**, nombre en minúscula **sin tildes, `ñ`, símbolos ni espacios**, palabras separadas por guion medio y **nombre = nombre del artículo**. Se entrega con un enlace en una columna de la hoja para que SEO la implemente.
- **Nombrar las imágenes con keywords de SEO desde el diseño** (prototipo): exportar por página y mantener un manual de medidas de imágenes. Para banners por programa o producto, nombrar el archivo con el nombre exacto del programa para que front lo exporte sin renombrar.
- Antes de reemplazar una imagen de más de 100 kB, dejar el `alt` asociado en el mismo documento de trabajo.
- Fotos de proyectos anteriores o de archivo: aclararlo en el pie de foto y en el `alt`.
- Banners CTA genéricos en el blog para que el equipo de contenido no tenga que cambiarlos; el CTA aparece dos veces en el artículo (tras un H2 relevante y al final). Si una portada debe parecer del público objetivo, usar fotografía sin diseño superpuesto.



## Auditoría de imágenes con umbrales (SEO Skills, 2026-10-30)

Complementa la sección "Rendimiento" con una revisión ordenada y una puntuación. Origen: skill `seo-images` de Jorge Jaramillo (`github.com/jorgejaramillo/seoskills`), reformulada; el repositorio no declara licencia. Los números son **orientativos**; **manda la regla del cliente y la de Guille de ≤100 KB para la imagen destacada** (ver arriba), que es más estricta que la referencia de la fuente para el hero.

### Datos: qué hace falta extraer
- Peso y tipo **reales** de cada imagen (petición `HEAD`), no solo el HTML. Una lectura de la página convertida a texto pierde `alt`, `loading`, `srcset` y `<picture>`; usar el HTML real.
- Las imágenes cargadas por CSS (`background-image`) no aparecen en la extracción: si el hero parece venir de CSS, decirlo en el informe.
- Candidata a LCP por página: la primera imagen de contenido fuera de cabecera y navegación. **Confirmar a mano** que sea realmente la principal.

### Revisión en ocho puntos
1. **Alt:** describe la imagen y mide de 10 a 125 caracteres, sin relleno de keywords. Decorativas: `alt=""`. Proponer alt concretos para las que no lo tienen, mirando el contexto.
2. **Imagen LCP:** sin `loading="lazy"`, con `fetchpriority="high"`, con dimensiones y formato moderno.
3. **Peso (referencia):** miniaturas menos de 50 KB · contenido menos de 100 KB · hero hasta 200 KB según la fuente (en esta skill, ≤100 KB para la destacada). **Crítico** por encima de 500 KB.
4. **Formato:** JPG o PNG a WebP o AVIF (`<picture>` con alternativa si hace falta); SVG para logos e iconos. El ahorro de WebP frente a JPG es aproximado (25 a 35 %): decirlo así, sin prometer segundos de LCP.
5. **CLS:** `width` y `height` (o `aspect-ratio`) en todas.
6. **Responsive:** `srcset` y `sizes` en las de más de 400 px de ancho.
7. **Carga diferida:** `loading="lazy"` y `decoding="async"` bajo el pliegue.
8. **Nombre de archivo:** descriptivo, en minúsculas y con guiones (no `IMG_1234.jpg`).

Las correcciones de marcado se entregan como **antes y después**.

### Puntuación (valores iniciales)
Parte de 100 y resta: −20 si la imagen LCP tiene carga diferida · −15 si más del 30 % no tiene dimensiones · −10 si más del 20 % no tiene alt · −10 si hay imágenes de más de 500 KB · −5 si más del 50 % está en formato antiguo · −5 sin `srcset` en las grandes · −3 por nombres genéricos. Mínimo 0. Si se integra en una auditoría general, ver [audit-scoring-and-weights.md](audit-scoring-and-weights.md).

---

## Fuente original: `title-and-description-generation.md`

# Procedimiento para escribir title y metadescripción

## Índice

- Cuándo se usa
- Estado de la evidencia
- Entradas
- Title: pasos y reglas
- Metadescripción: pasos y reglas
- Tandas de páginas
- Patrones por tipo de página
- Formato de salida
- Lista de revisión

Complementa [on-page-metadata-and-urls.md](on-page-metadata-and-urls.md) (qué es un buen title y una buena metadescripción) con **cómo producirlos de forma repetible**, sobre todo en lotes. Úsalo cuando una auditoría ([audit-scoring-and-weights.md](audit-scoring-and-weights.md)) marque títulos o descripciones ausentes, fuera de rango o duplicados, o cuando se pida "escribe el title / sugiere metadescripciones / mejora este title".

## Estado de la evidencia

Procedimiento tomado de las skills `title-generator` y `description-generator` de `seo-skills.com` (Jorge Jaramillo, consultadas el 2026-10-30; sin licencia declarada, por eso está reformulado). Los rangos de caracteres y las reglas de puntuación son **criterio editorial de esos autores para español de Colombia**, no una regla de Google: los buscadores pueden mostrar otro título y otro fragmento. **La regla del cliente manda** sobre los valores de aquí (ver el rango de [on-page-metadata-and-urls.md](on-page-metadata-and-urls.md) y la nota "Longitudes: regla por cliente"). Los ejemplos de marca de las fuentes (una cadena de farmacias) no se incluyen.

Resumen de rangos para no confundirlos:

| Qué | Para **detectar** el problema (auditoría) | Para **redactar** |
|---|---|---|
| Title | 30 a 60 caracteres | 45 a 55 |
| Metadescripción | 70 a 160 caracteres | 150 a 160, nunca más de 165 |

## Entradas

- **Consulta principal** (obligatoria): el término tal como lo busca la gente. Si falta, se infiere del slug, del H1 o del title actual y **se avisa** en las alertas.
- **Contexto** (opcional): tipo de página, marca o sitio, público, atributos reales (material, tamaño, ciudad, planes, medios de pago) y el title o la descripción actuales.
- **Title** (solo para la descripción): la descripción debe **añadir** información, no repetirlo ni parafrasearlo.
- **Descripciones existentes** (opcional, en lotes): las de otras URLs del mismo sitio, para no duplicar.
- **Número de opciones:** tres por defecto.

## Title: pasos y reglas

**Pasos**

1. Fijar la consulta como la busca la gente.
2. Identificar el tipo de página y elegir un patrón (tabla más abajo).
3. Escribir las opciones con **estructuras distintas**, cada una con la consulta al inicio.
4. **Contar caracteres** (con espacios y signos) y reescribir toda opción fuera de 45 a 55. No cortar a mitad de palabra ni rellenar con palabras vacías.
5. Pasar la lista de revisión.
6. Elegir la mejor como recomendada.

**Reglas de forma**

- Frase natural y completa, no una lista de palabras clave.
- Consulta principal primero; después un complemento (público, uso, opciones, lugar).
- Evitar separadores `|` y `–`. Se admiten dos puntos con moderación y **como único signo de ese tipo** en el title.
- Mayúscula normal: solo la inicial y los nombres propios (ver [spanish-style-and-capitalization.md](spanish-style-and-capitalization.md)). Nada de mayúscula en cada palabra ni de todo en mayúsculas.
- Sin emojis ni símbolos decorativos. Ortografía y tildes correctas; signo de apertura en las preguntas.

**Reglas de contenido**

- Sin exageración ni sensacionalismo, y sin prometer lo que la página no cumple.
- La consulta aparece **una vez**, en su forma natural.
- Específico del tema de la página.
- Una razón para hacer clic (beneficio, uso, público, dato verificable), **solo con datos que vengan del contexto**.

## Metadescripción: pasos y reglas

**Pasos**

1. Fijar la consulta.
2. Leer el title e identificar qué deja fuera.
3. Identificar el tipo de página y la propuesta de valor con el contexto.
4. Escribir las opciones, cada una con estructura distinta y la consulta cerca del inicio.
5. Contar caracteres: **150 a 160, tope duro de 165**. No rellenar con adjetivos ni cortar a mitad de palabra.
6. Pasar la lista de revisión y comparar contra el title y contra las descripciones existentes.
7. Marcar la recomendada.

**Reglas**

- La consulta aparece **una vez**, de forma natural, cerca del inicio.
- Describir **solo lo que la página ofrece**, con datos del contexto. Una idea de valor principal y una de apoyo.
- Llamada a la acción opcional, corta y tranquila: sin urgencia, sin presión, sin signos de exclamación repetidos.
- Una o dos oraciones completas. Sin listas de palabras clave, separadores `|` o `–`, emojis, mayúsculas sostenidas ni superlativos.
- **Única por URL:** refleja su marca, categoría o variantes. No copiar ni parafrasear el title. Sin menús, avisos legales, nombres de sección ni fichas técnicas pegadas.
- Si no se puede escribir una opción sin inventar datos, **se omite y se explica en las alertas**: es preferible a una descripción falsa.

Estructura recomendada: `[consulta y qué ofrece]. [detalle que suma: opciones, atributos, medios de pago, público]. [llamada a la acción corta, opcional].`

## Tandas de páginas

- **Primero el title y después la descripción**, nunca al revés: la descripción toma el title recomendado como entrada.
- Una llamada por página, en el mismo orden para ambos; cada title y cada descripción recomendados pasan al contexto de las siguientes.
- Cada title es único y estructuralmente distinto de los demás.
- Como máximo **1 de cada 5** titles usa dos puntos.
- Ninguna estructura se repite en más de **2 de cada 5** titles de la tanda.
- Variar el arranque: consulta + "para", + "en", + un verbo, o + coma y descripción.
- Comparar los titles lado a lado antes de entregar y reescribir los que se parezcan.
- Si la marca va al final, hacerlo en **menos de 1 de cada 3**.

## Patrones por tipo de página

| Tipo | Patrón de title |
|---|---|
| Marca o catálogo | `[Marca] [tipo de producto] para [uso]` |
| Marca con verbo | `[Marca] ofrece / reúne [productos]` |
| Producto | `[Nombre], [qué es o para qué sirve]` |
| Categoría | `[consulta] para [necesidad] en [tipo o presentación]` |
| Categoría con sitio | `[consulta] [complemento] en [sitio]` |
| Categoría en dos frases | `[consulta]. [complemento útil]` |
| Artículo en forma de pregunta | `¿[pregunta]?: [enfoque]` |
| Listado | `[consulta] en [tamaños o presentaciones]` |
| Herramienta | `[Nombre], el [tipo de herramienta] de [tema] en [país]` |

## Formato de salida

Cuando el procedimiento lo ejecuta una persona o un agente que alimenta una hoja o un script, devolver solo JSON válido, sin texto adicional:

```json
{
  "consulta": "…",
  "opciones": [
    {"title": "…", "caracteres": 52, "enfoque": "máximo 12 palabras"}
  ],
  "recomendado": 0,
  "alertas": []
}
```

Para descripciones, el campo `title` se llama `description` y `caracteres` está entre 150 y 160 (tolerancia hasta 165). `recomendado` es el índice desde 0. `alertas` recoge datos que faltan, consulta inferida u opciones que no llegaron a la longitud sin inventar contenido; queda vacía si no hay nada.

Si el cliente pide una hoja, trasladar este JSON a las columnas de la plantilla `assets/templates/content-architecture-map.csv` (que ya lleva caracteres restantes).

## Lista de revisión

Title:

- Entre 45 y 55 caracteres exactos (o el rango del cliente).
- Consulta al inicio y una sola vez.
- Se lee como una frase; sin `|`, `–`, emojis ni símbolos.
- Mayúsculas correctas; ortografía y tildes.
- Nada sensacionalista ni sin respaldo; específico y con una razón para hacer clic.
- No duplica el title de otra página.

Metadescripción:

- Entre 150 y 160 caracteres, nunca más de 165.
- Consulta al inicio, una vez; nada inventado.
- Una propuesta de valor concreta; llamada a la acción tranquila, si la hay.
- Oraciones completas, sin símbolos prohibidos, sin exageración.
- Distinta del title y de las descripciones de otras URLs.

Fuentes: SEO Skills, skills `title-generator` y `description-generator` (Jorge Jaramillo), https://seo-skills.com/title-generator y https://seo-skills.com/description-generator, consultadas el 2026-10-30.

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
- Ausencia de reseñas, precios o disponibilidad inventados (sin precio público: nada de `Offer` vacío ni `price` 0).
- Ningún marcador (`[PENDIENTE]`, `TBD`, `XXX`) dentro de un valor: si falta el dato, se omite el campo.
- Sin nodos duplicados con los que ya genera el plugin SEO (Rank Math: `#organization`, `#website`, `#webpage`); ver `schema-markup-for-ai-citation.md`.

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
