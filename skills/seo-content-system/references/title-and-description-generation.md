---
tags:
  - seo
  - on-page
---

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
