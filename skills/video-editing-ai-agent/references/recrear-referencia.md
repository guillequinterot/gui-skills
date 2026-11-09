# Recrear una animación de referencia y comprobar que coincide (v1.5)

**Origen:** reanimate (MIT), charlie947/reference-to-motion (MIT), huashu-art-motion `breakdown` (MIT). Entender, no copiar: de una referencia
se toma **ritmo, cambios y la idea**; jamás logo, copy, colores ni personajes ajenos. Esta guía completa a `video-comprehension.md` (entender un video)
y a `rea-reverse-engineer` (entender una web/app): aquí se trata de **construir algo propio que se mueva igual** y **medirlo**.
**Estado: candidato.** `scripts/frame_compare.py` está probado con material sintético; el bucle completo no se ha corrido con una pieza real.

## 1. MOVES vs LOOK (separar antes de pedir nada)
- **MOVES** = lo que se toma de un video de referencia: ritmo, cuánto dura cada plano, cómo una escena se convierte en la siguiente, la idea única.
- **LOOK** = lo que se toma de una web/marca/moodboard: colores, fuentes, sensación.
- Desglose en 5 líneas de la referencia (sirve también al modo `estilo` de `video-aprender`):
  1. **Pace** — cuánto dura cada plano (medir con `video_understand.py`/`motion_energy.py`, no a ojo).
  2. **Change** — cómo una escena pasa a la siguiente (corte, empuje, forma que crece…; `cut_dip.py` mide el hueco).
  3. **Type** — tamaño, peso, cómo llegan las palabras.
  4. **Colour & light** — hex muestreados (los tecleados por el usuario ganan a los muestreados de un JPEG, que «derivan unos puntos»).
  5. **La única idea** que sostiene todo.
- Salida: un prompt/plan de < 300 palabras con escenas `rango en segundos · NOMBRE · qué se ve · texto entre comillas`, que **sumen exactamente la duración**. No inventar números.

## 2. El bucle (máx. 5 rondas)
**grabar la referencia → especificar → construir → volver a grabar el clon con EXACTAMENTE la misma configuración → comparar → corregir lo más grande.**
1. **Configuración fija** (la misma en ambos lados): resolución, fps, recorte, disparador, duración. Si la referencia es un video ajeno: recortar cursor y marco del navegador; un GIF tiene el tiempo cuantizado ±1 fotograma; en pantallas Retina convertir píxeles (`distancia_css = distancia_video × ancho_viewport / ancho_recorte`).
2. **Especificar con números** (tabla): elemento · propiedad · de→a · inicio ms · duración ms · easing · escalonado · fuente del número. Orden de preferencia de fuentes: una declaración exacta (CSS/WAAPI, si la referencia es web: `rea-reverse-engineer` N1) > medición > lectura de fotogramas.
   Lectura manual: `inicio = primer_fotograma_con_cambio / fps`; `duración = (último − primero + 1) / fps`; ease-out si ya cubrió > 50 % de la distancia a 1/3 de la duración, ease-in si < 25 %.
3. **Construir** (HyperFrames o lo que corresponda; ver `engine-hyperframes.md`) y **volver a renderizar con la misma configuración**.
4. **Comparar** con `frame_compare.py` y **mirar la hoja de contacto con el visor de imágenes en cada ronda** (los números no bastan).
5. **Corregir lo más grande primero** y registrar qué cambió. Tras 5 rondas sin progreso en una fila: parar y reportar con números y motivo. **No bajar umbrales en silencio** para «pasar».

## 3. `scripts/frame_compare.py`
```
python scripts/frame_compare.py compare ref.mp4 clon.mp4 [--fps 25] [--width 320] [--region x,y,w,h] [--max-shift 15] [--fidelity movimiento|pixel] [--sheet hoja.png --every 5] [--json salida.json]
python scripts/frame_compare.py loop bucle.gif [--fps 20]
```
- **Curva de actividad:** % de cambio entre cada fotograma y el anterior, para ambos clips. Resume **tiempo y easing sin importar colores ni texto**: barras iguales = misma curva; un clon «cargado al inicio» frente a una referencia uniforme = easing de salida demasiado fuerte.
- **Ventana de movimiento:** primer y último fotograma con actividad > 0.2 % y fotograma pico; **error de tiempo** = clon − referencia en segundos para inicio, fin, duración y pico.
- **Desfase óptimo:** el desplazamiento (en fotogramas, ±15) que minimiza el desajuste alrededor del movimiento. **Si es grande (> 2 fotogramas), arregla el disparador/retardo del clon; no lo escondas alineando.**
- **Niveles de fidelidad:** `movimiento` (por defecto): error de tiempo ≤ ±0.08 s (2 fotogramas a 25 fps). `pixel`: además media de desajuste ≤ 2 % y ningún fotograma > 5 %. **Umbrales de la fuente, sin calibrar con nuestro material**: di cuáles usaste.
- **Avisos:** otro tamaño → se reescala el clon (con pérdida); mide con el mismo viewport.
- **Suelo de ruido:** compara la referencia contra una segunda captura de sí misma antes de juzgar el clon. Con reloj virtual determinista el suelo es 0 %; con video natural (cámara, compresión) **no persigas el desajuste de píxeles**: confía en la curva de actividad y la ventana de movimiento.
- **`loop`:** *costura* = diferencia media entre el último y el primer fotograma; *excursión* = máxima diferencia contra el fotograma 0. Referencia externa de portadas reales (sin calibrar aquí): costura 0.0–0.3, excursión ≈ 0.7–2.8; excursión ≈ 0 = nada se mueve. **No midas el movimiento en el fotograma de la mitad** (una oscilación vuelve a 0 ahí). Rotar el bucle para que el fotograma 1 sea la imagen terminada si la plataforma muestra el primero como estático. GIF: paleta propia (`palettegen=stats_mode=full` + `paletteuse=dither=none`: el dithering añade parpadeo en imágenes planas); revisar a 240 px de ancho.

## 4. Valores de partida de movimiento (de reanimate; para la tabla del paso 2)
fade-up con escalonado: 500–800 ms, ease-out-expo/quint, escalonado 60–150 ms, elevación 16–48 px · text reveal 600–1000 ms, escalonado 20–50 ms por pieza, con `overflow:hidden` · clip/máscara 800–1200 ms in-out · scale-in desde 0.90–0.96 en 150–250 ms · hover lift 2–8 px en 150–300 ms · marquee lineal con periodo 10–40 s (se mide el **periodo**, no el easing) · parallax con razones 0.2 / 0.5 / 1 · transición de página 300–600 ms con la salida más corta que la entrada · desfase del puntero `x += (objetivo − x)·k`, independiente del fps como `1 − (1 − k)^(dt/16.67)`.
Detalles que rompen el match: `transform-origin`, el orden de transforms, `fill-mode: forwards`, `overflow:hidden`, **fuentes distintas cambian todos los píxeles**, `prefers-reduced-motion`.
Muelles: sobreimpulso ≈ exp(−πζ/√(1−ζ²)) → 10 % ≈ ζ 0.59, 5 % ≈ 0.69, 20 % ≈ 0.46; tiempo de asentamiento ≈ 4/(ζω), ω = √(rigidez/masa). Si el sobreimpulso medido es > 2 %, es muelle/`back`, no bezier.
**Ajuste de easing** (no implementado aquí): probar ~22 curvas con nombre (`0.16,1,0.3,1` expo-out, `0.22,1,0.36,1` quint-out, `0.34,1.56,0.64,1` back-out…) con duración libre entre 1× y 2× la visible, ordenar por RMSE (< 0.03 ajuste bueno, < 0.08 aproximado).

## 5. Qué NO hacer
Copiar activos de un sitio de marca (shaders, imágenes, fuentes) aunque el repo de la técnica los publique «como estudio»; usar la medición para clonar un producto ajeno; ejecutar `--pre-js` o `--assets` de una herramienta externa contra sitios no confiables sin aislamiento. **Reanimate no se instala** (no funciona en Windows tal cual; ver el informe).
