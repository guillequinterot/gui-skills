# TRATAMIENTO: <nombre de la pieza>

<!--
Una hoja, escrita en los primeros minutos, ANTES de construir: la idea, el guion, las elecciones y el plan de planos.
Cómo se usa: references/direccion-y-revision.md §2. Estructura tomada de `cinetic` (Leonxlnx, MIT), reescrita. Copia a la carpeta del
proyecto, rellena cada <…> y borra los comentarios. Si algo no se sabe, escribe «ASK ME» y pregúntalo; no lo inventes.
Una pieza con la marca ya definida: manda la marca (colores, tipografía, tono); anota abajo, en «Prohibiciones de la marca», lo que trae.
-->

**Formato:** `<ancho>x<alto>@<fps>, <duración> s, <lanzamiento | actualización | producto | bucle | sting | recorrido>, audio: <música (título, licencia) + efectos | silencio | voz>` · **Motor:** <HyperFrames | Shotcut | ffmpeg>
**Nombre:** <el del producto, como se escribe> · **Producto:** <qué es y qué hace, en palabras llanas> · **Quién ve y dónde:** <p. ej. ingenieros, sin sonido, en un feed>
**Supuestos:** <lo que se dedujo y no se dijo> · **Aportado:** <kit de marca | clip de referencia | fotos | metraje | nada>
**Prohibiciones de la marca / lo que la marca trae:** <…>

## 0. Idea
- **Frase de la idea:** En esta pieza, <algo que solo tiene este producto> se convierte en <lo que la imagen hace con ello>.
- **Prueba del competidor:** con <el competidor más cercano> en la frase, <falla porque … | sigue siendo cierta → reescribir>.
- **Acción central:** <la entrada> se convierte en <la salida>, mostrado **literal** en el primer plano de imagen, en pasos visibles (<metraje o foto real de la persona que da la entrada, luego la interfaz del producto>).

## 0b. Guion
Palabras que un desconocido entiende **sin sonido**: qué es antes de 3 s, luego una cosa concreta que hace por línea, luego el nombre y qué hacer. 1–5 palabras por línea (2–7 como máximo), una afirmación cada una, una línea en pantalla a la vez.

| # | Papel | Línea | Palabras | En (s) |
|---|---|---|---|---|
| 1 | qué es | <[Nombre] convierte [entrada] en [salida]. / [Nombre] es un [categoría llana] para [quién].> | <2–7> | <≤ 1> |
| 2 | hace | <una cosa concreta, con verbo> | | |
| 3 | hace | | | |
| 4 | cierre | <el nombre y qué hacer: «[Nombre] ya está disponible.», una URL> | | |

Comprobación: `python scripts/storyboard_lint.py plan.md --script guion.txt` sin ROJOS y, leído el guion, otra persona dice qué es, qué hace y qué hacer.

## 1. Elecciones (una de cada; ninguna igual a las 3 últimas piezas: `python scripts/save_approved.py suggest …`)
| Casilla | Elección | Por qué le va a este producto |
|---|---|---|
| Voz del texto (una cara tipográfica) | <construir | desenfoque | tinta | …> | |
| Énfasis | <color en la palabra clave (por defecto) | ninguno | la única firma> | |
| Movimientos (2–3) | | |
| **Firma** (el plano que se recuerda) | <…> en el plano <#> | |
| Costuras (2–3 tipos) | <salida-entrada | cambio de texto | corte por coincidencia | corte de velocidad | desenfoque | zoom | elemento compartido> | |
| Familia de fondo | | |
| Cierre | <elemento | insignia | palabra> | |
| Marcas de terceros | <en la línea | alrededor | pared | ninguna> | |

## 2. Plan de planos
`T` = una línea sola, centrada, sobre fondo limpio (0.5–2.3 s). `A` = el producto actuando a cuadro completo, sin frase encima (1–3.5 s). `T+A` solo donde la línea nombra lo que hace la imagen (≤ 40 % de los planos). Cada `A` nombra **el cambio visible que demuestra la línea anterior**; una línea que ningún `A` demuestra se corta.

| # | Tiempo | Tipo | Línea o imagen | El cambio visible (A) | Costura de entrada | Sonido |
|---|---|---|---|---|---|---|
| 1 | 0:00–0:01.5 | T | <línea 1> | – | – | <la intro de la pista> |
| 2 | 0:01.5–0:04.0 | A | <la acción central> | <entrada → salida> | | |
| … | | | | | | |
| n | | cierre | marca centrada construida con <el último elemento>, el dato debajo | – | | <un golpe; el final resuena> |

Para pasarlo a `storyboard_lint.py`, copia las columnas a `assets/plan-tabla-template.md` (tiempo | objeto | acción | cámara | texto).

## 3. Fotograma final (el póster)
<El cierre como imagen fija: el fondo, la marca (la real o la construida con el último elemento), el nombre una vez, el dato debajo.>

## 4. Compuerta antes de construir (marca lo que se cumple; lo que no, se corrige aquí, no en el render)
- [ ] frases centradas en la banda media (16:9) o dentro de la zona segura (vertical); ninguna pegada a la izquierda arriba o abajo
- [ ] ≥ 2 planos solo-texto; `T+A` ≤ 40 %; la primera línea antes de 1 s; cada `A` muestra al producto haciendo la cosa
- [ ] una voz de texto; énfasis en ≤ 2 líneas; sin caja ni marcador salvo la firma
- [ ] todo corte duro lleva una costura; ≤ 10 % desnudos; el cierre centrado y construido con el último elemento, 2–3 s
- [ ] palabras reales (ni barras grises ni «lorem»), marcas de terceros vigentes
- [ ] fondo, voz, firma y cierre distintos de las 3 últimas piezas
- [ ] poco texto: sin texto en < 15 % de los fotogramas; ≤ 2 bloques a la vez
- [ ] premium, no solo limpio: profundidad y luz con motivo, tipografía héroe a 6–9 % del alto, la firma aterriza
- [ ] ninguna prohibición de la marca; las excepciones que la marca trae están arriba

---

# Ejemplo (ficticio; bórralo en tu copia): Cuadre, una app que concilia pagos con facturas

**Formato:** `1920x1080@30, 20 s, lanzamiento, audio: pista con licencia (96 BPM) + efectos` · **Motor:** HyperFrames
**Nombre:** Cuadre · **Producto:** una app que empareja cada pago del banco con su factura y deja a la vista solo lo que no cuadra · **Quién ve y dónde:** dueños de pequeños negocios, sin sonido, en un feed

## 0. Idea
- **Frase de la idea:** En esta pieza, los 412 movimientos del mes se convierten en una columna de pagos que encuentran su factura y dejan solo tres filas rojas.
- **Prueba del competidor:** con una hoja de cálculo en la frase falla: la hoja no empareja, solo lista.
- **Acción central:** el extracto del banco (una lista larga) se convierte en pares pago-factura que se unen uno a uno, en el primer plano de imagen (la pantalla real de la app).

## 0b. Guion
| # | Papel | Línea | Palabras | En (s) |
|---|---|---|---|---|
| 1 | qué es | Cuadre empareja tus pagos con tus facturas. | 7 | 0.4 |
| 2 | hace | Lee 412 movimientos del banco. | 5 | 4.0 |
| 3 | hace | Une cada pago con su factura. | 6 | 8.0 |
| 4 | hace | Solo ves lo que no cuadra. | 6 | 12.0 |
| 5 | cierre | Pruébalo gratis en cuadre.app. | 5 | 17.0 |

## 2. Plan de planos (extracto)
| # | Tiempo | Tipo | Línea o imagen | El cambio visible | Costura | Sonido |
|---|---|---|---|---|---|---|
| 1 | 0:00–0:01.8 | T | Cuadre empareja tus pagos con tus facturas. | – | – | la intro |
| 2 | 0:01.8–0:04.0 | A | el extracto entra | la lista corre hasta el final y el contador marca 412 | corte por coincidencia | tics con el desplazamiento |
| 5 | 0:08.0–0:11.0 | A | la firma | cada pago vuela a su factura y se apaga; quedan tres filas rojas | corte por coincidencia | un golpe en la entrada de la pista |
| 8 | 0:16.0–0:20.0 | cierre | la última fila roja se encoge hasta la marca; «cuadre» sale; la URL debajo | – | elemento compartido | un golpe; el final resuena |
