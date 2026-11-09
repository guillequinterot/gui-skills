# Cámara, ritmo y recetas de movimiento con números (v1.5)

**Origen:** huashu-art-motion, huashu-motion, charlie947/motion-graphics-skills, rossark-motion-skill, reanimate, video-director (todas MIT; ver
`analisis-fuentes/14-motion-graphics-nov-2026.md`). **Estado: candidato / valores de partida.** Salen de las fuentes (sus películas, su gusto), no de
medir nuestro material; se verificó el lint y la comparación, no el resultado visual. Complementa, no reemplaza, a `motion-doctrine.md`
(HyperFrames) y `motion-library.md` (Shotcut). Si algo choca con ellos, mira §9.

## 1. Lenguaje de cámara: acción, duración, cuándo NO
| Acción | Para qué | Duración / valor | Easing |
|---|---|---|---|
| Parada | el espectador lee; la imagen ya se mueve | lo que dure la locución | — |
| Empuje lento | llevar la vista al siguiente detalle | 0.6–1.5 s, +10–40 % (hasta 2 s si pasa de 2×) | `sine.inOut` |
| Retirada | volver al conjunto / cierre | 0.8–2 s, arranque rápido y cola larga | cola larga |
| Paneo / buscar lo siguiente | pasar de una pieza a otra en la misma mesa | 0.5–0.9 s (seguir una línea 1.3–1.8 s) | `sine.inOut` |
| Empuje rápido (acento) | revelación, giro, cifra clave | 0.25–0.35 s, +18–32 % y **parar** | punch |
| Latigazo (whip) | cambio brusco de mirada | 0.15–0.30 s con desenfoque direccional | `expo.inOut` |
| Golpe (slam) | texto grande, sello, cifra | 0.17 s, escala 1.55 → 0.94 → 1.0; **máx. una vez por plano** | slam |
| Corte seco | cambiar encuadre sin mover cámara | 0 fotogramas | — |
| Deriva lenta | ambiente, música, estilos artísticos | 1–4 %/s; solo atmósfera | drift |
Principios:
1. **Antes de mover la cámara pregúntate:** ¿qué mira el espectador ahora?, ¿es transición o acento?, ¿cuál fue el movimiento anterior?
2. **El mismo movimiento en cada plano es el mismo defecto**, sea lento o rápido (un empuje constante de 7.5 % se leyó «PowerPoint»; 48 empujes en 102 s, todos hacia dentro, «demasiado frecuente»). `storyboard_lint.py` avisa de 3 planos seguidos con la misma acción o con 3 empujes hacia dentro, y de más de 1/3 de planos con acentos.
3. Las cámaras **no invierten dirección dentro de una escena**; los momentos de lectura quedan quietos o a la deriva; **quédate quieto antes de la acción**.
4. Con material real a pantalla completa lo único posible es empujar: soluciones = una «mesa» con varias piezas en un lienzo y paneo entre ellas, recortar en vertical antes de colocar, y no volver a empezar desde 1.0 en cada corte.
5. Película real que ya se mueve → cámara quieta. Un empuje por imagen como máximo y solo si algo no se lee.
6. Cámara que revela: la retirada solo vale si el plano ancho trae **información nueva**. Una sacudida de 2–6 px que decae en 0.2 s, 1–2 veces por pieza; nunca en promos de producto serios.
7. Fuera-dentro para UI anidada: alejar para revelar la capa, empujar al detalle que añadió, alejar otra vez con deriva lenta (escala 1.03 → 1) entre movimientos; un pull-back continuo con una línea de copy por capa se juzgó «aún una presentación».
8. Cámara con reglas automáticas (explainroo, reencuadre): un plano nuevo si lo que aparece está separado > 0.8 s; llenar 72 % del cuadro para un primer plano y 82 % para la imagen completa; zoom máx. 2.2×; ≥ 2.2 s entre movimientos; empuje mínimo 1.3×; no volver a acercarse hasta 5 s después del último cambio de zoom; la cámara arranca 0.3 s antes de que aparezca el elemento.

## 2. Ritmo de la pieza (huashu-motion; medido por su autor en 21 lanzamientos)
- **Elige la ruta:** *continuo* (0–2 cortes: marcas calmadas, mecanismos, UI), *montaje* (muchos cortes sobre el pulso) o *híbrido* (columna continua rota por 1–2 ráfagas; lo normal para «tech y enérgico»). Piezas guiadas por música: un plano cada 1.8–3.5 s.
- **Curva de energía 0–10:** gancho en < 3 s; ascenso en escalones (cada sección añade algo nombrable); **ráfaga hacia el medio (media del 37 % de la duración, rango 30–60 %): 5–8 cortes, uno por pulso, enmarcada por planos de 1.5–4 s**; momento héroe en el punto musical más fuerte; **una parada** (0.5–1.6 s de casi silencio y luego imagen y sonido a la vez en el mismo fotograma); resolver en una marca. Formas aburridas: línea plana con un golpe al final; build lento que llega arriba en los últimos 2 s; la misma energía en cada escena. En > 30 s, dos drops (uno pequeño a 1/3, uno grande a 3/4).
- **Densidad en eventos por compás de 4 pulsos:** gancho 2–4; build 2–4 creciente; parada 0–1; pico/montaje 4–8; resolución 1–2. **Ningún tramo de más de ~2 compases sin algo nuevo** salvo una parada planeada.
- **Ráfaga medida** (115 BPM): planos de 1.67, 1.37, 1.10, 1.00 s, luego 13 cortes de un pulso (0.50–0.57 s) todos a < 28 ms del pulso, luego 1.10 y 3.04 s: «acelerar, bloquear al pulso, soltar».
- **Calendario de contraste:** cambiar ≥ 2 cosas en cada frontera de sección y todas en el drop: escala de plano (primerísimo ↔ general), velocidad (0.25 s duros ↔ 2 s de deslizamiento), familia de easing (ease-out duro `expo`/`power4` para tech; muelles solo para lo físico; **0.6–0.8 s suaves en todas partes = película dormida**), cámara (quieta ↔ viaje ↔ latigazo), densidad (1 objeto ↔ cuadrícula de 9), color/fondo.
- **Caso A/B instructivo:** una pieza calmada (96 BPM, un evento cada pocos segundos, planos de 10 s, easings de 0.6–0.8 s) pasó todas las comprobaciones automáticas **y una revisión independiente**, y el usuario dijo «aburrida» (puntuó 60). Rehecha **solo en ritmo** (120 BPM, primerísimo plano que se retira de golpe, punch-in al contar el número, latigazo, 9 elementos golpeando una cuadrícula a corcheas, parada antes del drop) subió a 80 y el movimiento por segundo pasó de 0.1–1.8 a 0.4–11. Moraleja: **la energía viene del corte y del movimiento; la calma de la marca se dice con paleta, tipografía y easings.** Ninguna métrica detecta «aburrida»; `motion_energy.py` solo dice si podría serlo.
- Por defecto, sin estilo ni energía nombrados: el fotograma 0 **es el póster** (ya contiene el sujeto; nunca página vacía ni un objeto pequeño con brillo en un fondo vacío: «salvapantallas»), movimiento inmediato, primera ráfaga antes de 5 s, tipografía legible en el teléfono.

## 3. Animación como 4 estados con reloj fijo (charlie947)
Toda animación se especifica con **cuatro estados con tiempo: inicio, cambio, mantener, retorno** (último fotograma = primero, si es bucle). Reloj de ejemplo para un efecto de 8 s: 0–2.2 movimiento (cúbico in-out), 2.2–6.6 mantener (con algo pequeño vivo), 6.6–8.0 retorno. Escalonado en el movimiento: temprano 0–0.8 s, medio 0.8–1.4, tarde 1.4–2.2. Dos modos: **loop** (posts, GIF) y **hold** (se reproduce una vez y se queda; bajo una locución). Para B-roll de Reel recorta el movimiento activo (~1.4 s) y usa *hold*: 8 s es demasiado lento.
Principios de las 16 recetas: «premium» = **un objeto que cambia de forma**, nunca un fundido de imagen a imagen; un **fantasma tenue del estado inicial** ayuda al ojo a seguir; **el mantenimiento es donde la gente mira** (en 4.4 s de hold, algo pequeño sigue vivo: barra de progreso, cursor, segunda ola de luz); **escalonar por un compás**, no todo a la vez; un elemento compartido **se mueve, no se duplica**; punto de fuga único; el borde delantero de un indicador de pestaña corre por delante y el trasero va un compás detrás (se estira y se acorta); los valores de un gráfico **nunca cambian**, solo cómo aparecen.
**Chequeo de 7 fotogramas** (a 0, 1, 2.2, 4.4, 6.6, 7.9 y 8 s de un efecto de 8 s): bucle (0 ≡ 8), movimiento (0, 1 y 2.2 distintos; si dos coinciden, algo no corre), encaje (nada fuera de caja), *still* (parado en el hold el efecto se lee de un solo fotograma), marca.

## 4. Capa ociosa, follow-through y `flow()` (rossark)
- **Una acción principal + 2–3 bucles ociosos por escena.** Capa ociosa permanente sobre una pose sostenida: respiración ±1–1.5 %, balanceos con periodos que **dividen el bucle**, lados desfasados.
- **Follow-through por retardo del padre** (60–150 ms, fuerza 0.3–0.6) en lugar de muelles: sin rebotes y **determinista** para un render por fotograma.
- **`flow()` — pasar por varias poses sin parar** (el «stop-and-go» de aplicar un ease por clave): interpolación cúbica de Hermite **monótona**. Pendiente de cada pose = media armónica ponderada de las pendientes vecinas (0 si cambian de signo); entre poses `h(s) = h00·v0 + h10·Δt·m0 + h01·v1 + h11·Δt·m1`.
  ```js
  // poses: [[t0,v0],[t1,v1],...] crecientes en t. Devuelve f(t). Sin overshoot si los datos son monótonos.
  function flow(P){const n=P.length,d=[],m=[];for(let i=0;i<n-1;i++)d.push((P[i+1][1]-P[i][1])/(P[i+1][0]-P[i][0]));
   for(let i=0;i<n;i++){if(i==0)m.push(d[0]);else if(i==n-1)m.push(d[n-2]);else if(d[i-1]*d[i]<=0)m.push(0);else{
    const h0=P[i][0]-P[i-1][0],h1=P[i+1][0]-P[i][0],w1=2*h1+h0,w2=h1+2*h0;m.push((w1+w2)/(w1/d[i-1]+w2/d[i]));}}
   return t=>{if(t<=P[0][0])return P[0][1];if(t>=P[n-1][0])return P[n-1][1];let i=0;while(t>P[i+1][0])i++;
    const h=P[i+1][0]-P[i][0],s=(t-P[i][0])/h,s2=s*s,s3=s2*s;
    return (2*s3-3*s2+1)*P[i][1]+(s3-2*s2+s)*h*m[i]+(-2*s3+3*s2)*P[i+1][1]+(s3-s2)*h*m[i+1];};}
  ```
  (Fórmula estándar de Hermite monótono, escrita aquí desde cero. Probada en Node con poses `[0,0],[1,1],[2,1],[3,2]`: pasa por todas, sin sobreimpulso y monótona; **no probada dentro de HyperFrames**.)
- Duraciones de partida: parpadeo 110/40/190 ms (cierre/mantener/apertura), interfaz 100–500 ms, escalonado 40–80 ms, curvas `cubic-bezier(0.77,0,0.175,1)` y `(0.23,1,0.32,1)`. **Mínimo ~100 ms (3 fotogramas a 30 fps) para cualquier movimiento rápido**; exporta a 60 fps si la plataforma lo permite. «Nada nace de escala 0».
- Medir una referencia: `sheet` a la tasa nativa, detección de bordes por fotograma y muestreo de colores → escribir los **beats como datos en ms** antes de construir (`frame_probe.py`, `motion_energy.py` y `frame_compare.py` cubren lo equivalente).

## 5. Cuadros por segundo como parte del estilo
12 fps «a dos» (cada pose se sostiene 2 fotogramas a 24 fps) **es la mitad del estilo** en imprenta, recortes, tinta y dibujo a mano; completos (60) para UI y motion graphics limpios; 24 para look cinematográfico. Dos capas de fps: cámara suave, elementos a pasos. Para que algo se mueva sin parpadear: **re-aleatorizar a 12 veces por segundo con semilla fija** (la semilla nueva por fotograma da parpadeo). Smear frame en movimientos rápidos en vez de motion blur; anticipación de 4–6 fotogramas con un pequeño movimiento contrario.

## 6. Escribir el estilo como números
Un `STYLE.md` por proyecto (plantilla: `assets/style-numerico-template.md`): medio en una cláusula, hex con **rol** (fondo / texto / UN acento) y qué elemento lleva el color de señal, curva de easing como `cubic-bezier` concreto, tiempos en fotogramas, cómo se conectan los planos (y qué se descarta: fundidos), texturas medibles, fps elegido a propósito y **lista de «evitar» por nombre** (ráfagas de partículas, lens flare, neón/brillo, RGB split, glitch, rebote en todo, degradados decorativos, texto que repite lo que enseña la imagen). Números concretos dan un look distinto; adjetivos dan salida genérica. Comparar la hoja de contacto contra ese archivo. **Donde no se sepa un valor se escribe «ASK ME» (preguntar), no se inventa**; los hex que teclea el usuario ganan a los muestreados.
Método de color (huashu-motion): encontrar antes de elegir — valores de marca leídos (CSS, `theme-color`, logo) → muestrear píxeles del producto → muestrear una fotografía del «mundo» de la idea → inventar al final y etiquetarlo «inventado: sin colores de marca». **Roles:** fondo (la mayor parte), superficie (~1/5), tinta y tinta secundaria, acento (un solo significado), inundación opcional (el acento llenando el cuadro en un golpe, 1–2 veces). **Valor primero** (¿el sujeto se lee en escala de grises?), la saturación tiene un solo hogar, texto pequeño ≥ 4.5:1. **«Look de la casa» como anti-patrón** (fondo oscuro + un acento cálido + texto hueso + serif; crema + serif gigante + naranja; casi negro + lima ácida; degradado violeta-azul; neón sobre gris GitHub): tres agentes con solo un README produjeron 6 de 9 fotogramas casi negros con acento cálido; **cambiar el hex manteniendo el patrón no cuenta**.

## 7. Texto en pantalla
Tiempos mínimos (el menor entre las fuentes): cada palabra ≥ 0.3–0.4 s en pantalla y nunca menos de 1 s en total; `tiempo_de_lectura = max(1.5, 1.0 + 0.3 × palabras)`; hold ≥ ~0.25 s por palabra corta + 0.5 s. Titular de 2–5 palabras junto a un elemento; etiquetas ≥ 28–34 px a 1080p; texto principal 80–110 px, etiquetas 40–56 px; contraste ≥ 4.5:1 (7:1 en el gancho y la llamada a la acción); **entradas 0.5–0.9 s, salidas 0.25–0.4 s con `power2.in`**; escalonado de 30–60 ms en UI y 15–25 ms en letras. Un máximo de ~5 elementos a la vez; algo nuevo cada 2–4 s. Etiqueta de un contador solo cuando el contador se detiene; períodos parciales «a la fecha»; datos de muestra etiquetados en cada fotograma («datos ilustrativos»).
Cámara + subtítulos: un empuje lento puede llevar el borde inferior de una tarjeta a la banda de subtítulos; calcular su borde bajo la cámara en ese instante o mover el subtítulo.

## 8. Trampas de código (GSAP/HTML; de huashu-motion, sin verificar con HyperFrames 0.8.162)
Un tween colocado **antes de 0** desplaza toda la línea de tiempo (todo lo anclado a la voz llega tarde): `Math.max(0, …)`. `fromTo` **renderiza su estado inicial de inmediato**: un elemento que debía aparecer a los 8 s ya se ve a los 0 (usa `set` o `immediateRender:false`). Las poses de cámara se **planean**, no se leen del estado vivo (si no, el resultado depende de qué fotograma se renderizó primero). Un contenedor sin altura con `transform` colapsa las capas `inset:0` (la foto desapareció con todas las comprobaciones en verde): `position:absolute; inset:0` antes de animar. Letras enmascaradas ocultas con `yPercent:110` asoman si la máscara tiene `padding-bottom` (ocultar a 140). Un `<video>` con `data-start` pero sin `id` renderiza congelado. **La banda sonora fija la duración** (un bucle ocioso en la tarjeta final alargó 29 s a 32 s). Escalar 9× un elemento con sombra grande y difusa cuelga la rasterización (para en ~5× o quita la sombra). Un escalado desde la esquina `0 0` que sale con `scale` desde el centro da un salto en el primer fotograma de salida (mismo origen). `hyperframes snapshot` puede renderizar capas ausentes en el MP4 real: si discrepan, juzga fotogramas del MP4 con `ffmpeg … tile`. Un canvas transparente a pantalla completa cuenta como «tapando todo el texto» para el verificador; un degradado (`background-image`) pisa el color de fondo (ver `errores-conocidos-y-aciertos.md`).

## 9. Conflictos con la doctrina existente (sin resolver; decide Guille con una pieza)
| Tema | Doctrina actual (HyperFrames / nuestra) | Estas fuentes | Qué hacer por ahora |
|---|---|---|---|
| Movimiento ocioso | `motion-doctrine.md` §1: **prohíbe** respirar/flotar/brillo pulsante en bucle; si sobra una escena se añade historia | rossark, charlie y video-director: una pose sostenida debe tener **algo vivo** (respiración ±1 %, un elemento ocioso) | No son incompatibles si el movimiento tiene **intención** (señal anclada al compás, cursor, progreso real); lo que se evita es el bucle decorativo. Probar ambas en una pieza |
| Deriva de cámara | explainers: manda la quietud; música/marketing: empuje sutil ≤ 8 % | huashu-art-motion: la deriva es **solo para atmósfera, nunca en un explainer** («se lee PowerPoint»); y «mismo movimiento en cada plano = defecto» | Consistente con lo ya decidido para explainers. Para música/marketing añadir la **variación** entre planos |
| Nivel | `audio-mix.md`: −16 LUFS por defecto | casi todas las fuentes: −14 LUFS para redes | `loudnorm_audio.py --social` ya hace −14/−1.0 |
| Ducking | «No sidechain», carve a comparar | explainroo y earshot: ducking con rampas, o stop-down antes del golpe | Sin cambio; comparar a oído cuando haya una pieza con voz |
