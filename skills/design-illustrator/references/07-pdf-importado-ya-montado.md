# 07 · PDF ya abierto y montado (planos, láminas, CAD) — arreglo en sitio

Caso modelo: `caso-planos-01` (8 láminas de 36 × 24 in, PDF exportado desde Illustrator y abierto en Illustrator para editar). Distinto del flujo HTML → PDF de Chromium (01-06): aquí **no hay HTML ni DOM**, el documento llega con **grupos anidados**, fotos recortadas a propósito y textos de otro autor. Por eso no se usa `ai_pipeline.ps1` ni `ai_fix_text.jsx` (sacan todo a la raíz y rompen el apilado): se usan las versiones «en sitio».

## Qué traía el documento

| Síntoma | Cifras del caso |
|---|---|
| Texto partido en trozos y letras sueltas («oposed SQ. F») | 1 939 textos de punto, 868 de 1 carácter, 0 de área |
| Máscaras de recorte | 318 (155 sin efecto, 163 que «recortan»), anidadas hasta 9 niveles |
| Recortes que parecían necesarios y no lo eran | 22 grupos enteros ocultos (restos de copiar y pegar) + recortes de foto duplicados dentro de otro recorte |
| Texto que se sale de la página y el PDF lo corta | un bloque legal de 8 líneas, 55–65 pt por fuera del borde derecho, en cada lámina |

## Receta (orden fijo)

0. «Guardar como» una versión nueva (`…-limpio.ai`) y copiar el original a `backups/`. El original no se toca.
1. `scripts/ai_fix_pdf_import.ps1 -Dry` (solo cuenta) y luego sin `-Dry`. Ejecuta, en este orden:
   - `ai_fix_text_inplace.jsx` — une trozos de la misma línea (mismo contenedor, línea base, tamaño y escala; la fuente y el color pueden cambiar por trozo, p. ej. la ligadura «fi» en otra fuente). **Valida** el ancho (12 %, el resto lo absorbe el tracking) y, si no cuadra, no une. El texto nuevo nace en el mismo grupo y en la misma posición de apilado.
   - `ai_clean_deep.jsx` — recortes con **límite visible efectivo** (un grupo recortado mide recorte ∩ contenido): suelta de dentro hacia fuera los que no recortan nada visible, aparta a la capa oculta `_fuera-de-mesa (oculto)` lo que el recorte esconde por completo (no se borra) y deja solo los que recortan de verdad (fotos). Devuelve `necesarios` con lámina, tamaño y cuánto sobresale.
   - `ai_merge_paragraphs_infer.jsx` — infiere párrafos (mismo borde izquierdo, estilo e interlineado constante 0,9–1,5 em; salto de párrafo donde la palabra siguiente habría cabido) y los une en un texto de área **solo si sus líneas son idénticas a las originales**.
2. **Texto que se sale de la página** (lo que `necesarios` lista con `sobresale` y no es una foto): no se resuelve solo. Se junta en un texto de área dentro del margen, con el tamaño más grande que no choque con lo de abajo (en el caso: 19,6 → 17,2 pt, de 8 a 9 líneas), y **se le dice al usuario**: es una decisión de diseño. Script del caso: `ai_reflow_legal.jsx`, en la carpeta del proyecto (a medida, no genérico).
3. Repetir `ai_fix_pdf_import.ps1`: los recortes de página se sueltan solos (ya nada sobresale). Debe quedar idempotente (0 cambios).
4. `ai_autosize_text.ps1` (mueve el ratón ~10 s: avisar). Guardar.
5. Verificar: (a) conteos (textos, de 1 carácter, recortes visibles, trazados invisibles); (b) **texto**: extraer con PyMuPDF el texto de cada página del PDF original y el de cada mesa de trabajo (sin espacios, NFKC) y comparar multiconjuntos de caracteres: no puede faltar ninguno, solo puede sobrar lo que el PDF tenía cortado; (c) **render**: exportar cada mesa de trabajo (PNG, 40 %) antes y después, comparar píxeles y mirar a pantalla completa junto al PDF.

## Resultado del caso

Textos 1 939 → 534 visibles (508 de punto + 26 de área); recortes 318 → 21 (todos de foto); 0 trazados invisibles; 22 grupos ocultos apartados; 8 bloques legales dentro de la página; 0 caracteres perdidos (27 por lámina recuperados del texto que el PDF cortaba). Los scripts tardan segundos; lo lento es exportar a PNG el documento original (~2–3 min las 8 mesas).

## Trampas aprendidas (ver también 02, filas 24–31)

- `doc.pathItems.rectangle(…)` y `doc.textFrames.areaText(…)` fallan con «Target layer cannot be modified» si la **capa activa** es la oculta o bloqueada que crea la limpieza: crear con `doc.activeLayer.pathItems.rectangle(…)` y fijar `doc.activeLayer` antes.
- Leer `tf.textRange.characterAttributes` **antes** de recorrer `tf.textRange.characters[...]` invalida el rango («illegal text range»): leer los atributos del conjunto después y envolver la lectura del último carácter en `try`.
- El `geometricBounds` de un grupo con recorte no es fiable para decidir si el recorte sobra: calcular el límite visible efectivo a mano (`aiCD_eff`).
- La altura de un texto de área recién creado es la del rectángulo: ajustarla (`textPath.height`, `textPath.top`) antes de decidir si un recorte de página sobra; «Tamaño automático» llega después y es un clic.
- Un PDF puede traer el mismo texto dos veces (una copia con la ligadura como carácter privado y otra por trozos): no se toca, se informa.
