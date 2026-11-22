# Dirigir una pieza y revisarla por lentes (v1.6; de `cinetic`, con apoyo de `product-film`; todo **candidato** hasta probarlo con una pieza real)

Fuente principal: `Leonxlnx/cinetic` (MIT, leído en crudo el 2026-11-14; `references/analisis-fuentes/15-cinetic-productfilm-htmldemo-nov-2026.md` dice qué se tomó y qué no). Aquí está la parte que **no existía** en la skill: un plan de tiempo con porcentajes, un tratamiento que prueba la idea antes de construir, un estándar con números, y una revisión en dos pasadas con lentes y un **refutador**. Lo que ya existía (plan en tabla, `storyboard_lint.py`, revisor independiente, rúbrica de 7 ejes) sigue valiendo: esto se apoya en ello, no lo sustituye (`production-workflow.md` §11, `visual-qa.md`).

**Cuándo:** lanzamientos, piezas de producto o de función, videos de «ya salió la versión X», bucles de landing, recorridos de interfaz, stings de logo, de 3 a 60 s. Para un Reel de testimonios o un corte de metraje real no hace falta: usa `edit-craft.md`.

**Qué NO se adopta** (es el gusto de la casa de cinetic, no verdad): su lista de prohibiciones de estilo (sin serifas ni cursiva, sin naranja/beige/morado, sin vidrio, sin emojis), «nunca música generada», «un solo tipo de letra», «−14 LUFS». **Manda la marca** del proyecto y el criterio de Guille (`direct-visual-design`); si una regla de abajo choca con la marca, gana la marca y se anota en el encargo.

## 1. Plan de tiempo con porcentajes (la pieza completa existe pronto; cada mirada posterior se recorta de ella)
Un render es lento; lo que ahorra tiempo es tener **todo el film temprano** y mirarlo muchas veces barato. Con un presupuesto dado (si no hay, 90 min para una pieza de 15–30 s):
| Hito | % | Qué existe al terminar |
|---|---|---|
| Encargo, tratamiento, guion que pasa `storyboard_lint.py`, **música elegida y ajustada** | 15 | La imagen se corta **a la música**; no se mira nunca una pieza sin su sonido. |
| **El final primero**, en fotogramas fijos | 25 | El cierre (la marca, el nombre, el dato) se lee. Es también el póster. |
| **Borrador completo** (mitad de resolución, 30 fps, codificación rápida, con el sonido de ese momento) + su hoja de contacto | 45 | Se ve todo el arco. |
| Sonido definitivo, **una ronda de revisión** (§4), correcciones, borrador otra vez | 45–70 | Lo que falla una compuerta se corrige; una segunda ronda solo si una compuerta sigue fallando (tope: 3, regla ya vigente). |
| Render final | 70 | Si no alcanza el tiempo, se entrega el borrador escalado **diciéndolo**; no se entrega una pieza cortada. |
Si hay horas de sobra (modo largo): pulir **cada escena en su propia pasada** contra los números de su receta, con fotogramas fijos al lado, en vez de una pasada sobre toda la pieza.
Una compuerta que cuesta más de 5 min en una pieza de 30 s es **consultiva**, no obligatoria.

## 2. Tratamiento de una página (`assets/tratamiento-template.md`; se escribe en los primeros minutos, antes de construir)
Añade a lo que ya pide `production-workflow.md` §11.4 tres cosas de cinetic:
1. **Frase de la idea:** «En esta pieza, *algo que solo tiene este producto* se convierte en *lo que hace la imagen con ello*». **Prueba del competidor:** pon el nombre del competidor más cercano en la frase; si sigue siendo cierta, la idea es genérica: se reescribe.
2. **Acción central** literal en el **primer plano de imagen**: la entrada se convierte en la salida **en pasos visibles** (nunca un corte de «la petición» al «resultado terminado»); si la entrada es humana, una persona real la da (metraje o foto, no dibujo).
3. **Plan de planos T/A:** `T` = una línea sola, centrada, sobre fondo limpio (0.5–2.3 s); `A` = el producto actuando a cuadro completo, sin frase encima (1–3.5 s); `T+A` solo donde la línea nombra lo que hace la imagen (≤ 40 % de los planos). Cada `A` declara **el cambio visible que demuestra la línea anterior**; **una línea que ningún `A` demuestra se corta**.
El guion: palabras que un desconocido entiende **sin sonido** (qué es antes de 3 s, una cosa concreta que hace por línea, el nombre y qué hacer al final).

## 3. Estándar con números (candidato; umbrales de cinetic, **sin calibrar con nuestro material**)
| Regla | Número | Cómo se mide hoy |
|---|---|---|
| Líneas cortas y claras | 1–5 palabras (2–7 como máximo); 0.3–1.5 palabras de titular por segundo | `storyboard_lint.py --max-text-words`, a mano |
| Qué es el producto | en palabras llanas antes de 3 s; primera línea antes de 1 s | hoja de contacto de 0–3 s (`visual-qa.md`) |
| Texto escaso | sin texto en ≥ 15 % de los fotogramas; ≤ 2 bloques de texto a la vez fuera de un plano de producto | a ojo sobre la hoja |
| Línea o imagen | ≥ 2 planos solo-texto; `T+A` ≤ 40 % de los planos | `storyboard_lint.py` (tabla) |
| Frase centrada (16:9) | centro entre 35 y 65 % del alto, centrada ≥ 80 % del tiempo; nunca pegada a la izquierda arriba o abajo salvo sobre imagen a sangre | a ojo; **vertical: manda la zona segura** (`captions-subtitles.md`, `errores-conocidos…` §1) |
| Movimiento | nada quieto > 0.8 s fuera del cierre | `motion_energy.py`, `glitch_scan.py` (congelados) |
| Costuras | todo corte duro lleva algo (desenfoque, ancla, arrastre, objeto que cruza); ≤ 10 % de cortes «desnudos»; 2–3 tipos de costura, ninguno > 40 % | `cut_dip.py` mide el hueco; el resto a ojo |
| Una cara tipográfica | una familia y su «voz» que rota (construir, desenfocar-entrar, tinta; nunca dos líneas seguidas iguales), énfasis en ≤ 2 líneas | a ojo |
| Cierre | centrado, construido con el último elemento, 2–3 s, el nombre una vez y el dato debajo; la marca es la real | a ojo + `verify_entrega.py` |
| Pieza propia | fondo, voz, firma y cierre distintos de las 3 últimas piezas | `save_approved.py suggest` (la biblioteca) |
**Conflicto sin resolver:** cinetic masteriza a **−14 LUFS** (feed) y nuestra skill a **~−16** (`audio-mix.md`). Se decide por destino con Guille; `verify_entrega.py --lufs` mide cualquiera de los dos.

## 4. Revisión en dos pasadas (la imagen sola primero) + lentes + refutador
**Pasada 1 — la imagen sola.** Con la hoja de contacto abierta y **las palabras tapadas** (lee solo los planos de imagen), escribe **una línea por plano `A`**: qué hace el producto en él, y si **se lee** (sí / en parte / no). Meta: todos se leen al menos en parte y la mitad con claridad. Un plano que dice «no pasa nada» recibe una acción del producto (un clic, un resultado que aparece, un objeto que se transforma) **antes** de añadirle una palabra.
Dos pruebas sobre la hoja, antes de la lista (de `references/review-loop.md` de cinetic §1):
- **La frase en cadena.** Escribe la pieza ya cortada como **una línea**: «A se convierte en B se convierte en C…», con la forma del elemento en cada tile («la petición escrita se convierte en la página, el botón de la página en la etiqueta *en vivo*, la etiqueta en el primer registro, los registros en la cifra, la cifra en la marca»). Cada «luego» entre dos tiles es una **unión por diseñar** (un corte donde el elemento debería crecer, encogerse, hincharse y cambiar, volar o ampliarse); una pieza que necesita «y además» son **dos piezas**: corta una.
- **Las palabras tapadas.** Tapa el texto en seis fotogramas (uno por acto y el cierre) y pregunta: ¿cuál es la única acción y qué caso la recorre (la misma petición, los mismos nombres y cifras)? Si un desconocido no puede decirlo, la imagen no lo cuenta: el texto propio del producto y el elemento llevan el medio, las líneas solo prometen y afirman.
**Lo que un crítico a ciegas encuentra primero** (cada uno con sus fotogramas): la acción principal del producto saltada (un corte de la petición a un resultado terminado) o su salida desnuda; **datos que se contradicen al pausar** (la tarjeta más nueva delante con la hora más vieja; una cuenta y un total que no pueden ser ciertos a la vez); un nombre sobre la cara de otra persona o una cara para dos personas; el mismo recurso tipográfico en cada línea (mismo tamaño, misma construcción, el acento siempre en la última palabra); texto que no se lee sobre su fondo; un corte que cambia de sujeto mientras aún está nítido, o un fundido cruzado de dos escenas; un cuadro vacío o detenido; la tarjeta final que se va del centro hasta el último fotograma; un mundo que es una sola foto quieta o una mancha; la música cortada al final.
**Pasada 2 — la lista, un sí o un no con fotogramas** (§3). Un «no» es **P0** en el gancho, la acción central, el cierre o una prohibición de la marca; **P1** en el resto. Después: **los 3 segundos más débiles** y por qué.
**Prioridades ancladas:** **P0** se ve en un momento clave o rompe la historia; **P1** se nota viendo la pieza con normalidad (incluye un pop de un fotograma sobre una zona grande); **P2** solo se ve al pausar.
**Reglas del revisor:** como máximo **10 cambios**, ordenados por impacto por minuto de arreglo; cada uno **concreto** (archivo, constante, valores: «`CUE.entrada: compás 5 tiempo 2 → tiempo 1`», no «mejora el ritmo»); **nunca proponer añadir texto** (sí cortar una línea, reescribir una vaga con palabras llanas, o darle a un plano quieto la acción del producto); no listar lo que está bien ni lo ya arreglado. Las imágenes cuestan: lee la hoja y recorta o saca un fotograma solo para confirmar.
**Lentes opcionales** (`assets/critics/`; se entregan a un subagente con los campos rellenos, o se siguen a mano; devuelven JSON con la misma forma, así que se pueden juntar): `director.md` (la pasada de arriba), `forense.md` (las banderas de los scripts: ¿real, **diseñada** —se declara— o falso positivo?), `sincronia-sonido.md`, `detalle.md` (par fotograma a fotograma contra una referencia o contra la ronda aprobada). Se usan cuando el usuario pide una revisión más profunda o una compuerta sigue fallando en su área.
**El refutador** (`assets/critics/refutador.md`) — **lo nuevo de verdad:** antes de gastar tiempo en arreglar, un revisor distinto **intenta tumbar cada P0/P1** como si fuera una afirmación, no un hecho: mira los fotogramas, mira el código que el arreglo nombra, lo mira **a velocidad normal** (un defecto de un fotograma sobre una zona pequeña dentro de un movimiento rápido suele ser invisible). Rechaza si la afirmación es falsa, exagerada, invisible a velocidad normal fuera de un momento clave, ya arreglada o si el arreglo empeoraría la pieza. **Excepciones:** una **prohibición de la marca** nunca se rebaja por breve o pequeña; las **comprobaciones de texto** (cuántas palabras por fotograma, cuánto se lee) se verifican contando en las hojas, no «a ojo y a velocidad», porque quien ya conoce el texto lo lee siempre. Si el problema es real pero el arreglo es malo, se queda el problema con un arreglo mejor. Esto mata los falsos positivos y evita rondas de «arreglo» de cosas que no estaban rotas.
**Cuidado heredado de `visual-qa.md`:** la autoevaluación infla; manda la puntuación independiente; el informe va atado al hash del archivo.
**Cuándo se entrega:** sin ningún P0 abierto y con la lista en «sí» (o respondida por escrito); tope de **3 rondas** (5 si el usuario pidió la revisión larga). Cuando varias lentes puntúan una misma dimensión, **manda la más baja**, y una dimensión con un P0 verificado abierto no pasa de 3 sobre 5. **En la entrega se dice con claridad qué cambiarías todavía.** Las compuertas de cinetic que premian «su» gramática (una puntuación de gramática de la casa) son **solo consultivas**: miden su gusto, no el de la pieza.

## 5. Clases de defecto y su causa habitual (cinetic las tiene medidas; aquí, con el script nuestro que ve cada una)
| Clase | Qué es | Causa habitual | Lo ve… |
|---|---|---|---|
| `pop` / `seam-pop` | cambio de 1–2 fotogramas que el movimiento no explica | una propiedad que salta en un corte; un fundido que colapsa a 1–2 fotogramas | `glitch_scan.py` |
| `stall` | un fotograma repetido dentro de un movimiento | pose de reposo duplicada en un empalme; dos movimientos que llegan a reposo seguidos | `motion_energy.py` |
| `dead-stretch` / `hold` | > 2.5 s sin cambio fuera del cierre | tramo muerto: dale cambio al producto o corta antes | `glitch_scan.py` (congelados), `motion_energy.py` |
| `camera-wander` | la cámara va y vuelve despacio o nunca se asienta | flotación sin motivo: o quieta, o **un** movimiento que arranca, viaja y aterriza | a ojo sobre la hoja |
| `carried-cut` | un corte «de velocidad» que rompe dirección o rapidez | el plano entrante arranca desde reposo o al revés | `cut_dip.py` (parcial) |
| `dissolve` | mezcla de dos imágenes distintas, o fundido a negro antes de los últimos 2 s | fundido cruzado entre escenas: construir una costura con algo que se lleva | `cut_dip.py` |
| `ghost` | una imagen de un fotograma que ningún vecino tiene | `will-change` sobre una capa con desenfoque animado; capa vieja | `glitch_scan.py` |
| `border` | franja de 1–3 px en un borde varios fotogramas | la cámara descubre el borde del escenario; capas sin sobrante | a ojo (recorte con `frame_probe.py --crop`) |
| `judder` | escalones de píxel entero en un movimiento lento | `left/top` fraccionarios con `transform`; el texto que se ajusta a píxel al final de una curva | `frame_probe.py --diff` |
| `sharpness` | un escalón de nitidez en un fotograma | desenfoque CSS animado sobre una capa grande: usa **niveles fijos** de desenfoque | a ojo |
| `banding` | degradados dibujados como escalones de 8 bits | degradados CSS: hornea placas con tramado (dither) | **sin script** (estírale el contraste ×12 a un fotograma con `frame_probe.py`) |
| `smear` | manchas de compresión sobre un campo plano | un tramado de 8 bits que el codificador conservó a medias | **sin script** |
Cuando un script marca algo, decide uno de tres: **real** (se corrige), **diseñado** (se declara: un corte o un congelado que quisiste) o **falso positivo** (se dice por qué en una cláusula). Un número de bandera solo **no es evidencia**: hace falta el fotograma.

## 6. Entrega: verificar decodificando, no leyendo metadatos
`python scripts/verify_entrega.py pieza.mp4 --duration D --bg R,G,B [--bg-at x,y] [--loop] [--probe t:x,y …] [--lufs -16]`: duración al fotograma, etiquetas de color (si el MP4 no trae, **avisa y decodifica asumiendo BT.709 / rango TV**), color real del fondo en el fotograma 0, costura de bucle a resolución completa, color decodificado en un instante (acento, superficie), pico del audio tras el códec (> −1 dBTP avisa). Si el fondo sale **más claro** (`#0a0a0a` → `#171717`), el rango de color se leyó al revés: **se arregla la conversión, nunca los tokens**. Verificado **solo con material sintético** (`selftest.py`).
Orden de cierre: `glitch_scan.py` → `verify_entrega.py` → hoja de contacto leída → refutador sobre los P0/P1 → entrega con lo medido separado de lo visto y de lo no verificado.
