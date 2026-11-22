# <Producto>: kit de video

<!--
Para una película de producto hecha desde el propio código/diseño del producto (`production-workflow.md` §12). Estructura de `product-film`
(Rieranthony, MIT), reescrita. La hoja se llena DESPUÉS del descubrimiento y de la entrevista, con lo que el usuario eligió. Cada regla lleva su
fuente (archivo y línea, o la URL de la landing): lo que no tenga fuente se marca «ASK ME». Si esta hoja y las reglas del repo del producto
discrepan, manda el repo. Nunca traigas reglas de otro producto.
-->

Fuentes: <URL de la landing>, <ruta del sistema de diseño>, <archivos de reglas>, notas del dueño del producto.

## El encargo (de la entrevista)
- Dónde se ve: <bucle de landing mudo | redes con sonido | lanzamiento o demo con sonido>. Formato: <16:9 | 9:16 | 1:1>. Duración: <s>.
- Música: <pista y licencia | silencio>. Debe mostrar: <funciones, con sus nombres de producto>.
- Ingredientes elegidos: <elemento de marca: animación del logo / mascota / marca de palabra / solo interfaz> · <palabras: frases grandes / pies / ninguna> · <traslados: elemento que viaja / una cámara grande / cortes al compás> · <extras: cursores, logos de socios, momentos de prueba, textura>.
- Final: <eslogan, llamada a la acción, URL>.

## Reglas duras (cada una con su fuente)
- Mayúsculas y minúsculas: <…> (fuente)
- Tipografía: <estilos; dónde se permite la monoespaciada> (fuente)
- Esquinas: <token de radio> (fuente)
- Superficies: fondo `<token>`; otras superficies **solo donde el producto las tiene**: <cuáles> (fuente)
- Bordes y sombras: <lo que hace el producto> (fuente)
- Texto: <guiones, nivel de lectura, palabras prohibidas> (fuente)

## Encuadre (<ancho>x<alto>, <fps> fps, <oscuro|claro>)
- Encuadre: <sangre completa | el propio del producto>. Palabras: <estilo, peso, tamaño, acento>. Escenas: solo el texto de la interfaz salvo que se hayan elegido pies; contenido legible a 100 px de los bordes.

## Color (en hex todo lo que se anima)
| Token | Valor | Uso |
|---|---|---|
| fondo | | |
| primer plano | | |
| apagado | | |
| superficie | | solo donde el producto muestra una |
| borde | | solo donde el producto usa uno |
| acento | | |
| estados (bien / aviso / fallo) | | del producto |

## Elementos propios del producto
| Elemento | Aspecto | Fuente | En el video |
|---|---|---|---|
| Botones (y su estado de carga) | | | **conserva su ancho** mientras carga |
| Marcadores o insignias | | | |
| Cargador | | | dibujado por fotograma, no con su propio reloj |
| Iconos de marcas y socios | | | junto a sus nombres |
| Textura o patrón (si lo hay) | | | tranquila detrás de la interfaz |

## Logo y elemento de marca
- Logo (ruta SVG o componente) y su animación: <se dibuja solo / se revela / ninguna>. Mascota: solo si el producto la tiene **y** el usuario la eligió. Nunca: <lo que está fuera de la marca>.

## Componentes
| Necesidad | Componente (ruta) | En el video: importar / gemelo / redibujar, y por qué |
|---|---|---|
| | | un componente que corre su propio reloj (animaciones por librería, `requestAnimationFrame`, un spinner, keyframes CSS, video, shaders, imágenes que cargan solas) **se redibuja como gemelo guiado por el tiempo** |

## Movimiento
- Resortes y curvas del producto: <valores>. Traslados elegidos y sus reglas.

## Afirmaciones (honestas)
- Lo que el producto hace (se puede mostrar): <…> · Lo que nunca hace (no se muestra): <…> · Frases aprobadas: <…> · Palabras que evitar: <…>
- Solo se muestran resultados y cifras que el producto da de verdad (sus datos de demostración, los de la landing). Sin garantías.
