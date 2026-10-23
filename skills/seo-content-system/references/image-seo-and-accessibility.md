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
