# Doctrina de movimiento para piezas animadas (v1.3)

Fuente: skills `motion-doctrine`, `cut-the-curve`, `embedded-captions` y `talking-head-recut` de **HyperFrames** (HeyGen, Apache-2.0; ver `NOTICE.md`), leídas en crudo el 2026-10-15. **Reglas reescritas con nuestras palabras** y contrastadas con `motion-library.md`; los números son los que ellos publican. Alcance: piezas **compuestas** (motion graphics, animación de ilustraciones, tarjetas sobre un talking head), no el montaje de metraje en bruto. Estado: **primera validación hecha** con la animación de banco-pruebas-video (`references/engine-hyperframes.md`): los efectos anclados a palabras y los tiempos funcionan; **cut-the-curve no sirve tal cual para páginas ilustradas a sangre completa** (deja un fotograma atenuado con franja oscura) y **el *push* de la sección 7 lo corrige (medido)**.

## 1. Compatibilidad con `motion-library.md` (leer antes de aplicar)
| Tema | HyperFrames | Nuestra biblioteca | Qué hacer |
|---|---|---|---|
| Transición entre escenas | Prohíbe el crossfade; corte con **portador visible** en movimiento (cursor, contenedor, marca, grupo de palabras) | Dissolve/luma 8–14 f es "seguro" en talking head | **Convivir**: dissolve sigue valiendo para metraje real; en piezas compuestas usar corte con movimiento |
| Movimiento "ocioso" | Prohíbe respirar/flotar/brillo pulsante en bucle | Permite creep de zoom lento (~+4 %/s, tope +9 %) | **No chocan**: el creep es cámara con intención; lo prohibido son bucles decorativos. Si una escena sobra, se añade historia, no movimiento |
| Rebote | Prohíbe `bounce.out` y `elastic.out`; `back.out` 1.4–1.7 sí | "Pop" 0.78→1.12→1.0 y spring de énfasis | `back.out` ≈ nuestro pop; **evitar rebote tipo pelota y elástico** |
| Dirección | Un sentido dominante para toda la pieza (por defecto izquierda) | "Mantener dirección" en transiciones | **Adoptar** la versión de ellos: una dirección por pieza |
| Entrada | ≤ ~800 ms, salida ≈ 75 % | Entrada 0.3–0.5 s, salida 0.2–0.3 s | Los nuestros son más cortos y siguen valiendo; los de ellos son el **tope** |
| Escalonado | Total ≤ 500 ms | Palabras 40–80 ms, elementos 100–150 ms | Compatibles; sumar y no pasar de 500 ms |

## 2. Reglas de costura (corte entre escenas)
1. **Mismo eje, mismo sentido**: x sigue en x, y en y, Z en Z. Nunca espejar. En Z el signo del cambio de escala marca la dirección: crecer = empujar, encoger = tirar; empujar con empujar, tirar con tirar.
2. **Cortar en pleno movimiento** en ambos lados: no asentarse antes del corte ni arrancar desde reposo después.
3. **Velocidad igualada** con curvas espejo: salida `power4.in`, entrada `power4.out`; la entrada recoge al menos el 50 % del recorrido teórico. **Nunca `.inOut` a ambos lados de un corte.**
4. Un lado visible por fotograma (sin solape); el contenedor raíz **opaco** para que no parpadee en blanco.
5. Máximo **2–3 tipos de transición** por pieza, repetidos (la repetición crea lenguaje).
6. Registrar cada costura en un **ledger** (`ledger.json`: tiempo de corte, vector de salida y de entrada con eje y signo, selectores, técnica) y verificar antes de renderizar: la salida sigue moviéndose en el corte, la entrada viene en vuelo, dirección medida = dirección anotada, velocidades parecidas (aviso), cero solape, continuidad del portador.

## 3. Recetas con números (resolución de referencia 1920 px de ancho; escalar proporcionalmente)
| Receta | Parámetros |
|---|---|
| **Cut the curve** (corte por defecto) | Recorrido ≈ 230 px (~12 % del ancho, nunca fuera de cuadro); salida 0.2–0.4 s y entrada ≥ igual; total ≈ 0.6 s; la salida se desvanece al 25–30 % del recorrido; desenfoque opcional 8–10 px |
| **Zoom-through** (empuje, solo titulares) | Salida escala 1→1.2 (`power3.in`, 0.2 s) con desenfoque 0→10 px; **corte duro en el pico de desenfoque**; entrada 0.75→1 (`expo.out`, 0.5 s); nunca se ven dos textos a la vez |
| **Zoom-through inverso** (tirar, solo llegadas) | Salida 1→0.8 (~0.2 s), entrada 1.25→1 (~0.5 s), total ≈ 0.7 s |
| **Desenfoque** | Texto: pico 10 px; cuadro completo: 18–20 px; desenfocar el contenedor, no a los hijos; mismo pico en ambos lados |
| **Waterfall de palabras** (costura a nivel de palabra) | ±230 px; salida 0.34 s `power4.in`; fundido de palabra 0.18 s; escalonado +0.022 s; entrada 0.3 s `power4.out` desde opacidad 0.35; huecos de 0.05 s que se reducen ×0.84 por palabra |
| **Rack-focus** | Curvas `power2`; el saliente se mantiene opaco hasta el corte; corte en el pico de desenfoque 8–12 px (máx. 16–18); escala ≈ 1.06; **como mucho una vez cada ~8 s**, en giros de la historia |
| **Entrada en cascada** | Desplazamiento en Y: ancla 60–80 px, normal 40–50 px, ligero 30–48 px; duración 0.16–0.20 / 0.13–0.16 / 0.10–0.13 s; solape de 1–2 fotogramas; `power4.out`; opacidad binaria |
| **Nudge** (deslizar un grupo) | Rampa `power3.in`: 10 % de distancia en 20 % del tiempo; ráfaga lineal: 65 % en 18 %; cola `power4.out`: 25 % en 62 % (≥ 3× la rampa) |

## 4. Tiempos y orden
- Pausa de **0.3–0.75 s** entre una acción y su resultado. El efecto empieza **en el mismo fotograma que su causa**.
- Elementos parecidos comparten una sola curva y una sola duración.
- Cada fase entre entrada y salida lleva movimiento sostenido de alguna clase: revelado por etapas, cámara con intención, interfaz secuenciada, secuencias animadas o acción guiada por cursor.
- Tiempos de escena = **marcas de palabra reales** de la voz (`transcribe_words.py`), no estimaciones. Si se regenera la voz o se edita el primer/último segundo de una escena, **repetir la verificación**.
- Estado inicial de cada elemento: invisible (`autoAlpha: 0`) y `data-start` igual al instante del corte, para que no aparezca antes de tiempo.
- Cuantizar todos los tiempos a **1/fps**.

## 5. Gráficos o tarjetas sobre un talking head (`talking-head-recut`)
El metraje se entrega **intacto**; solo se superponen tarjetas con tiempo.
- Número de tarjetas = `max(5, round(duración / (ritmo base × multiplicador de densidad)))`. Ritmo base: < 60 s → 6–8 s; 1–3 min → 8–12 s; 3–10 min → 12–20 s; 10–30 min → 20–35 s; > 30 min → 30–60 s. Densidad alta ×0.7, media ×1.0, baja ×1.5.
- Tarjeta > 8 s necesita movimiento extra; > 15 s, un bloque de datos o revelado en varios pasos.
- Formato recomendado según el origen: ancho/alto ≥ 1.5 → 16:9; ≤ 0.7 → 9:16; entre medias → 4:5. Texto vertical = tamaño horizontal × 1.3 (titulares 88–132 px), relleno lateral 24–36 px.
- Entrada 0.4 s, salida 0.35 s, reencuadres 0.5–0.7 s. Mirar el **fotograma "héroe"** de cada tarjeta antes del render completo.
- Corregir errores de la transcripción **solo en el texto** de cada palabra; no tocar `start`/`end`. Recortar el final de cada tarjeta a la duración del medio (si no, la cola sale negra).
- Recodificar la fuente con intervalo de fotogramas clave = fps (`-g 30` a 30 fps) para que las búsquedas del renderizador no congelen la imagen. **[no verificado con Shotcut]**

## 6. Puerta antes de renderizar (patrón de HyperFrames)
Verificar **antes** de gastar un render: estructura/lint, desbordes del cuadro, contraste, costuras (ledger), y un fotograma suelto por escena (`snapshot`). Nuestro `self_eval.py` verifica **después**; esta puerta es el complemento.

## 7. Páginas a sangre completa: push (validado en banco-pruebas-video v2, 2026-10-15)
`cut-the-curve` asume elementos sueltos sobre un fondo común. Con **páginas ilustradas completas** deja un hueco oscuro y un fotograma atenuado. Para ese caso:
- **Push**: ambas páginas **en contacto** (sin hueco ni solape), misma curva y misma velocidad, sentido dominante (izquierda), **recorrido = ancho completo** (1080 px), **0.60 s centrado en el corte narrativo**. La página saliente va de `x:0` a `x:-W` y la entrante de `x:W` a `x:0`.
- Una **sola curva continua** `power3.inOut` por transición: el pico de velocidad cae justo en el corte. (Excepción deliberada a "no `.inOut` en un corte": aquí no hay dos tweens separados.)
- **Sin cambio de opacidad.** Cada escena debe existir 0.30 s antes y 0.30 s después de su corte (`data-start`/`data-duration` ampliados) para que ambas convivan durante el empuje.
- La cámara (empuje lento de escala) sigue **continua a través del push**, sin reiniciarse.
- **Medido** con `scripts/cut_dip.py` en los mismos cortes: hueco máximo **19.8 % / 16.7 % del ancho (v1) → 0 % (v2)**; el bajón de brillo mínimo pasó de 0.40 / 0.34 a 0.73 / 0.85 (el resto es la diferencia real de brillo entre páginas). Lo que **no** se puede juzgar con fotogramas: la sensación de movimiento; hay que verlo en el video.

## 8. Principios de composición para video (de `motion-principles` y `video-composition`, HyperFrames)
**Guardrails** (los modelos los violan por defecto):
- No uses **la misma curva en todos los tweens**: máximo 2 tweens independientes con la misma curva en una escena (varía las curvas como varías los pesos de una tipografía). No la misma **velocidad** en todo: la escena más lenta debe ser ~3× más lenta que la más rápida. No entres todo desde la **misma dirección** (varía: izquierda, derecha, escala, solo opacidad, espaciado de letras). No el mismo **escalonado** en cada escena. No un zoom ambiente en cada escena (elige: paneo lento, rotación sutil, empuje de escala, cambio de color o **nada**; la quietud tras el movimiento es poderosa). **No empieces en t = 0**: desplaza la primera animación 0.1–0.3 s (cero retraso se siente como un corte).
- **La curva es la emoción, la transición es el verbo:** `expo.out` = seguro; `sine.inOut` = soñador; `elastic.out` = juguetón. Dirección (no opcional): `.out` para lo que **entra** (arranca rápido y frena; responde), `.in` para lo que **sale** (arranca lento y acelera), `.inOut` para lo que se mueve entre posiciones. Se confunden constantemente.
- **La velocidad comunica peso:** rápido 0.15–0.3 s (energía, urgencia); medio 0.3–0.5 s (profesional, la mayoría); lento 0.5–0.8 s (gravedad, lujo); muy lento 0.8–2.0 s (cinematográfico, emocional).
- **Estructura de escena — construir / respirar / resolver:** construir (0–30 %: los elementos entran, escalonados, no todos a la vez) · respirar (30–70 %: el contenido visible, vivo con UN solo movimiento ambiente) · resolver (70–100 %: salida o final decidido; **las salidas son más rápidas que las entradas**: una tarjeta tarda 0.4 s en aparecer y 0.25 s en desaparecer).
- **Las transiciones son significado:** fundido cruzado = "esto continúa"; corte seco = "despierta" / disrupción; disolución lenta = "déjate llevar". Se suele fundir todo: usa cortes secos para disrupciones y cambios de registro.
- **La coreografía es jerarquía:** lo que se mueve primero se percibe como lo más importante; escalona por importancia, no por orden del DOM; solapa las entradas (no esperes a que termine la anterior); **escalonado total < 500 ms** sin importar cuántos elementos.
- **Composición de video (los cuadros no son páginas web):** al menos **dos puntos focales** por escena (el ojo necesita adónde viajar; nunca un solo bloque de texto flotando en el vacío) · **llena el cuadro** (texto principal al 60–80 % del ancho) · **tres capas mínimas** (fondo con tratamiento, contenido, acentos como divisores, etiquetas, barras de datos) · el fondo no está vacío (resplandores radiales, tipografía enorme y tenue que se sale del cuadro, paneles con borde, filetes; un negro puro `#000` se lee como "no cargó nada") · **ancla a los bordes** (centrado y flotando es un patrón web) · cuadros divididos y diseños por zonas · elementos estructurales (filetes, divisores, paneles; animan bien con `scaleX` de 0) · **una línea conectora (rayo, riel, subrayado) debe poder nombrar su ancla de inicio, su ancla final —elementos reales— y su trabajo; si el cuadro puede perderla sin perder significado, es decoración: córtala**.
- **Escala para video (referencia 1920 px de ancho):** titulares 64–120 px · cuerpo 28–42 px · etiquetas 18–24 px · opacidad decorativa 12–25 % (por debajo de 10 % es invisible) · bordes 2–4 px · relleno 60–140 px. Un `font-size` menor de 24 px exige justificación.
- **Color:** mate está bien, plano no: cada escena necesita al menos un color que atraiga el ojo; el acento visible (15–25 % para atmósfera, saturación plena en lo focal); en fondos claros usa bordes más fuertes y acentos plenos y añade textura para evitar "diapositiva en blanco"; **no uses degradados lineales de pantalla completa sobre fondo oscuro: se ven bandas con la compresión H.264** (usa radial, sólido o sólido + brillo localizado); tiñe los neutros hacia el matiz de marca (el gris muerto parece sin diseñar).
- **Los recursos y el diseño de marca** los decide `direct-visual-design`; esto solo ajusta su aplicación a video (tamaños, opacidades, grosores): el color de marca es sagrado, la aplicación es tuya.

## 9. Doctrina del explainer narrado (de `faceless-explainer/motion-language`)
Cuatro reglas "de las que cargan peso" para que una pieza se lea como un explainer serio y no como una presentación hecha por un agente:
1. **Suave gana a rebotón; `power3` es el valor por defecto.** Curvas de cola larga que se asientan con suavidad. Nada de `back.out` / `bounce.out` / `elastic.out` como estilo base: el rebote es el **primer motivo de rechazo** de los usuarios y el agente casi nunca lo acierta (cree que añade énfasis y lo paga con limpieza). El sobreimpulso queda como excepción rara y explícitamente juguetona (un golpe de logo para consumo, una campanada deliberada).
2. **Revelado secuencial en la segunda mitad (~50 % trasero), a la voz.** No vuelques todo en el primer ~25 % de la escena (eso fuerza el aire de diapositiva). Revela cada pieza —una línea, una tarjeta, incluso un h1— **cuando la voz la menciona**, repartiendo los revelados en la mitad final. Menos es más: pocas cosas en pantalla, cada una llegando en su señal, vence a un lienzo lleno que se animó una vez y se congeló. La entrada solo carga lo que la voz dice en t = 0; el resto espera en el timeline su señal hablada.
3. **Sin "respiración perezosa", sin empuje o paneo lento malo en la segunda mitad: "prefiero NINGÚN movimiento a un movimiento MALO".** Escalar tarjetas o texto arriba y abajo en bucle para parecer "vivo" es la señal barata; un paneo o empuje lento sobre elementos en la mitad final **rompe la línea de visión y cansa los ojos**. La solución a ambos es la misma: escalonar los revelados con el guion. Una escena en reposo vence a otra "mantenida viva" con respiración o deriva. **Única "vida" permitida durante una pausa: *jitter* sutil** (oscilación de muy baja amplitud) o interiores SVG que se mueven porque el sujeto hace algo (manecillas, aspas, puntos que pulsan).
4. **Las costuras internas son cortes con velocidad igualada** (§2–§3).
**Reglas de núcleo "seekable" (no negociables):** sin movimiento infinito ni *forever* (cualquier vida es un tween finito durante la pausa, nunca `repeat`/`yoyo`) · sin aleatoriedad ni reloj de pared (cada render idéntico; el escalonado y la variación se derivan del índice del elemento) · las entradas usan `fromTo` (declara el estado inicial para que un salto a t = 0 aterrice bien; nunca dependas de un inicio oculto por CSS) · **sin `transition` ni `@keyframes` de CSS para el movimiento** (corren con el reloj del navegador, no con el de la búsqueda de fotogramas: se desincronizan y parpadean) · entrada + revelado secuencial, **sin salida a mitad del video** (la escena se desmonta con la transición; la salida es solo de la última escena).
**Prohibido (modos de fallo):** *presentación* (todo volcado en el primer 25 %, el contenido entra y se congela, nada llega en su señal) · *vida barata* (respiración circular, empuje lento en la mitad final, muchos elementos flotando por su cuenta) · *rebotón* · todos los elementos entrando a la vez (secuencia o escalonado).

### Conflicto con nuestras dos versiones de banco-pruebas-video (decisión pendiente)
Las dos versiones de banco-pruebas-video usaron empuje de cámara continuo (escala 1.0→1.08 y 1.04→1.10) durante páginas con texto: la regla 3 lo desaconseja en la segunda mitad, y para un Ken Burns de ilustración ellos proponen **1.0→1.04 durante el beat**. Nuestra biblioteca (`motion-library.md` §1) recomienda el *creep* de zoom para **metraje real** (+4 %/s, tope +9 %); no coinciden por el tipo de material. Además, su guía de marketing dice lo contrario ("todo elemento decorativo con movimiento ambiente; lo sutil se lee estático a 30 fps"): **depende del género**. Decisión: para explainers y piezas educativas manda la quietud; para marketing y *sizzle*, el movimiento ambiente. Se valida con el video desde cero (`production-workflow.md` §10).

### Decisión parcial tras el video desde cero (2026-10-16)
Para **música y marketing** (pieza al compás): empuje sutil (≤ 8 %) sobre fotos **sí** (sin él el gancho queda congelado: movimiento 0.00–0.03 durante 2 s) y las pausas se llenan con **señales ancladas al compás** (subrayados que barren, derivas lentas, pulsos de escala ≤ 1.04), nunca con respiración en bucle. Para explainers narrados sigue mandando la quietud. La preferencia estética entre con y sin empuje es de Guille y sigue sin decidir (hay dos renders comparables en la carpeta `hyperframes/renders/` del proyecto de caso-reel-01). Detalle y números en `production-workflow.md` §10.

## 10. Vocabulario de primitivas (nombre → receta GSAP; de `motion-vocabulary`)
Usa el nombre en el plan y la receta al construir; "suits" indica el carácter. *Antes de escribir una a mano, busca un bloque equivalente en el catálogo* (`npx hyperframes catalog --query ...`).
| Tipo | Primitiva | Receta (hacia el estado final en CSS) | Carácter |
|---|---|---|---|
| Entrada | `slide_*` | `from({ y:±150 / x:±200, opacity:0, ease:"power4.out" })` | calmo, profesional |
| | `scale_grow` | `from({ scale:0, opacity:0, duration:.6, ease:"power2.out" })` | calmo, suave |
| | `scale_punch` | `from({ scale:.6, opacity:0, ease:"back.out(2.2)" })` | impacto (usar con la excepción de la regla 1) |
| | `fade_in` / `fade_blur` | `from({ opacity:0, duration:.4 })` / `+ filter:"blur(14px)"` | sutil / cinematográfico |
| | `word_reveal` | por palabra `from({opacity:0, y:..}, stagger:.1)` | narrativo |
| | `wave` | por letra `from({y:..}, stagger:{each:.04})` | fluido, musical |
| | `slam` | `from({ y:-300, ease:"power4.out" })` + sacudida al caer | pesado |
| Énfasis | `scale_pulse` | `to({ scale:1.12, yoyo:true, repeat:1, ease:"sine.inOut" })` en el compás | rítmico |
| | `shake` | `to({ keyframes:[{x:-9},{x:9},{x:0}], ease:"none" })` | urgente |
| | `glow` / `color_shift` | `textShadow` / `color` hacia el acento (envolvente ataque–decaimiento–reposo) | importante / dinámico |
| Salida | `fade_out` / `slide_out` / `scale_out` | `to({ opacity:0, duration:.4, ease:"power2.in" })` / `y,x fuera` / `scale:1.06` | cierre / transición |
| Acento | `underline_sweep` · `bar_wipe` · `hold_breath` | `fromTo({scaleX:0},{scaleX:1}, transformOrigin:"left center")` · barra · `to({scale:1.015, ease:"sine.inOut"})` | — |
Elementos de pantalla de interfaz: clic con cursor + onda expansiva, pulsación de botón (compresión y recuperación con resorte), brillo de palabra clave sincronizado a la voz, cámara que sigue al cursor, zoom a un objetivo descentrado, orbitar. Revelado: decodificación por volteo 3D de caracteres, autotrazado de contornos SVG, expansión desde el centro hacia afuera. Marcadores: resaltado, círculo, estallido, garabato. **Heurísticas de piezas cortas con el movimiento como mensaje:** el gancho aterriza en ~0.5 s · **un único motivo dominante** · rompe el patrón si la pieza dura más de ~2.5 s (cambia exactamente una cosa) · la intensidad del efecto iguala la energía · un elemento clave queda legible ≥ ~0.3 s · los beats pueden anticiparse ~0.1 s para sentirse en sincronía.

## 11. Qué costura para qué situación (de `cut-catalog`)
| | Zoom-through | Zoom-through inverso | Cut the curve | Waterfall |
|---|---|---|---|---|
| Alcance | cambio de texto dentro de la escena | beat de llegada / pago | entre escenas | costura texto→texto |
| Eje | Z, hacia el espectador | Z, alejándose | X / Y | X, por palabra |
| Desenfoque pico | 10 px texto / 20 px cuadro | igual | no hace falta | ninguno (el fundido hace el trabajo) |
| Sensación | "avanzar a través de" | "llegar a" | "llevado de lado" | "una ola a través de la costura" |
**Elegir:** una **frase inacabada** (una idea mayor que se construye en varias escenas distintas) → cut-the-curve o waterfall; un **cambio de estado** (pasar a una parte NUEVA del video, típico gancho → contexto) → zoom-through; una **llegada** → inverso. Encadénalos para que las costuras internas se sientan como una cámara moviéndose por el contenido. **Anti-patrones:** dos textos visibles durante un zoom-through · 20 px de desenfoque en texto (las letras se emborronan) · elementos en caminos distintos a ambos lados del corte · desenfoque u opacidad distintos en el fotograma del intercambio · curva suave en la entrada (`power2.out`: la entrada se siente más lenta que la salida) · entradas y salidas totalmente fuera del cuadro · un elemento solo que se desvanece mucho antes de su corte (aire muerto) · zoom-through en texto de cuerpo (a escala 0.75 es ilegible) · escenas sin cut-the-curve (los cortes estáticos parecen diapositivas). *(Los nombres de estas costuras son recetas de construcción internas: no son valores válidos de una transición entre escenas del inyector.)*

## 12. Reglas de construcción en HTML/GSAP que el linter no atrapa (de `motion-principles`)
- **Nunca incrustes una imagen plana**: dale tratamiento de movimiento (inclinación de perspectiva con `transformPerspective: 1200, rotationY: -8` + sombra —no `transform: perspective()` de CSS, GSAP lo pisa—; Ken Burns **1 → 1.04** durante el beat; marco de dispositivo; interfaz flotante a otra profundidad; revelado por desplazamiento).
- **No superpongas tweens de transformación en conflicto sobre el mismo elemento** (una entrada en `y` y un Ken Burns en `scale` simultáneos pueden dejar el elemento invisible sin aviso): combínalos en un `fromTo` o sepáralos entre padre (entrada) e hijo (Ken Burns).
- **Prefiere `fromTo()` a `from()`** dentro de escenas: `from()` escribe el estado inicial al construir la línea de tiempo, antes de que la escena esté activa, y al saltar entre posiciones puede parpadear o saltarse la entrada.
- **Los pulsos ambiente se agregan al `tl`, nunca a un `gsap.to()` suelto** (corre con el reloj de pared: se ve en la vista previa y **no aparece en el render**).
- **Elimina a la fuerza los elementos interiores que salen en el límite de una escena** (un `tl.set()` de duración cero tras su fundido), nunca el contenedor `.clip`.
