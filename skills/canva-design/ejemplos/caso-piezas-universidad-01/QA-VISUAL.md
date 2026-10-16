# QA visual por programa, contra su línea gráfica (plantilla del caso `caso-piezas-universidad-01`)

> Se hace **después de la fase de imágenes (stock/IA)** y **antes de subir a Canva**. Nada se monta en Canva hasta que cada programa esté **aprobado por el usuario** en la tabla de estado. En el caso original: **36 programas** (1–32: 2 diseños × Post/Historia/Banner = 6 piezas; 33–36: carruseles de 4 láminas × 2 diseños = 8 láminas; algunos programas con solo un diseño por falta de copy).
> Cómo: abrir cada `NN-slug/previews/00-resumen.jpg` (y los PNG por pieza a tamaño real; en los carruseles `00-resumen-carrusel.jpg`) tras regenerar y renderizar (`bash herramientas/rerender_all.sh [carpetas]`) y comparar **pieza por pieza** con la referencia gráfica del programa (material del kit de marca del cliente y su documento de línea gráfica). Para cada programa se rellena una fila; el usuario aprueba al final.

## Checklist por pieza (todo debe cumplirse)
1. **Línea gráfica del programa**: paleta (colores dominantes y acento) fiel a su familia; estilo (foto / recorte / panel / degradado) reconocible como ese programa y **distinto** de otros programas.
2. **c1 ≠ c2**: imágenes **distintas** entre los dos diseños y composición distinta (overlay / split / claro-oscuro), pero misma línea.
3. **Texto = copy de la hoja, literal** (sin emojis, sin etiquetas añadidas, sin WhatsApp/correo). Automático: `python -I herramientas/qa_copy_check.py` (→ `QA-COPY.md`; revisar a mano las diferencias que liste: son falsos positivos por saltos de línea o anomalías ya conocidas del copy).
4. **Marca**: barra de sede + lockup correcto (blanco sobre color / negro sobre claro), sin deformar, con área de protección; CTA en el color institucional (anotar las excepciones aprobadas); una sola familia tipográfica con Regular/Bold/Italic.
5. **Legibilidad**: contraste del texto sobre foto/color (mínimo AA; titular ≥ 3:1, texto ≥ 4,5:1), nada de texto sobre rostros u objetos clave, sin solapes ni cortes, chips sin partir mal, CTA que no se funde con el fondo.
6. **Imágenes**: nítidas a tamaño real (sobre todo **Historia**: ¿hay que subir resolución?), sin texto/logos horneados, sin personas generadas con IA sin aprobación del usuario, sujeto bien recortado en cada formato (post / historia / banner), sin bordes/halos en recortes.
7. **Formatos**: Post 1080×1080 · Historia 1080×1920 (**nada importante en los 250 px superiores/inferiores**) · Banner 1200×628 · Carrusel 1080×1350; capas con `data-layer` y nombre de página `N-F-slug-<marca>-cX[-L]`.
8. **Técnico**: lint de Canva 0 errores (`rerender_all.sh` lo corre), pesos de imagen razonables (< ~5 MB c/u para subir a Canva).
9. **Imágenes repetidas entre programas**: ninguna escena igual en dos programas de la misma familia.

## Estado por programa (rellenar durante el QA; ✅ aprobado · 🟡 con observaciones · ⬜ pendiente)

Una fila por programa. Ejemplo del formato (las filas reales del caso, con nombres de programas del cliente, no están en el repo):

| N | Programa | Imágenes (Fase 2) | QA visual | Aprobado por el usuario | Observaciones |
|---|----------|:---:|:---:|:---:|---------------|
| 1 | Programa modelo | ✅ | ✅ | ✅ | modelo aprobado; recheck tras la fase de imágenes |
| 2 | Programa con CTA largo | ⬜ | ⬜ | ⬜ | CTA largo |
| 3 | Programa con un solo diseño | ⬜ | ⬜ | ⬜ | solo c1 (copy 2 vacío) |

## Compuerta para pasar a Canva
Todas las filas con **QA ✅ y Aprobado ✅**, `QA-COPY.md` sin diferencias reales, lint 0 errores, nombres de página correctos y **orden de montaje definido** (tandas de 9 programas = partes 1/4…4/4 del Canva del usuario). Entonces sí: fase de montaje en Canva (`../../references/08-montaje-multipieza-y-fuentes.md`).
