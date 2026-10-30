---
tags:
  - seo
---

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
