# Narración con tiempos por palabra, guion alineado y demos de producto (v1.5)

**Origen:** explainroo, argo, take-one, huashu-motion (`om voice`), video-director (todas MIT; ver `analisis-fuentes/14-motion-graphics-nov-2026.md`).
**Estado:** `scripts/align_script.py` verificado con datos sintéticos; **ninguna herramienta externa instalada** (ni Kokoro, ni Argo). Lo de §3 y §4 es
guía de diseño, no un flujo probado. Complementa `captions-subtitles.md`, `story-design.md` §9 (guion) y `production-workflow.md`.

## 1. El orden: la voz primero
1. **Escribe el guion hablado** (`story-design.md` §9: ~2–2.5 palabras/s con pausas; frases de 8–18 palabras, una idea por frase; los pronombres se pegan a lo último dicho: tras un inciso, vuelve a nombrar el sujeto). **Cuenta las líneas habladas antes del storyboard**: el guion fija la duración.
2. **Genera o graba la voz y mídela** antes de animar. Los tiempos de palabra **medidos del audio renderizado** son las señales de toda la pieza (cues por palabra, no por segundo).
3. **La imagen sigue a la voz**: la imagen empieza ~0.3 s después de terminar la frase que la nombra; el golpe del momento clave va en la pausa **antes** de la línea que lo nombra; ~200 ms de desfase ya se lee como lag. Para que la entrada de un elemento *asiente* al decir la palabra, ancla el cue ~0.25 s antes de ella; un contador cuenta hasta ~0.35 s después del cue.
4. Si cambia el guion o la voz, se **regenera solo lo que cambió**: caché por hash de (texto de la escena, voz, velocidad, modelo, versión del procedimiento). Una voz de pago (ElevenLabs vía MCP) cuesta créditos: **no regeneres lo que no cambió** (reutilizar la voz de una pieza aprobada costó 0 créditos, ver `errores-conocidos-y-aciertos.md`).
5. Una escena mide `lead` (aire antes de la voz, ~0.35 s) + voz + `hold` (~0.7 s; ~1.4 s en la última); todo ajustado a la rejilla de fotogramas (`round(t·fps)/fps`); un `pace` global (0.7–1.6) escala voz, pausas, animaciones y música a la vez.

## 2. `scripts/align_script.py`: guion + transcripción → tiempos por palabra con control de calidad
```
python scripts/transcribe_words.py voz.wav --lang es --out words.json
python scripts/align_script.py guion.txt words.json --key voz.wav -o guion-words.json --srt guion.srt
```
- **Por qué:** Whisper acierta los tiempos pero **se equivoca en nombres, cifras y siglas**; el guion tiene las palabras correctas y ningún tiempo. El script las une (programación dinámica, distancia de edición) y entrega por cada palabra del guion: texto mostrado, hablado, `s`, `e`, `matched`. El **copy oficial manda** sobre el texto transcrito (`captions-subtitles.md`).
- **Sintaxis del guion:** `[#nombre]` marcador (toma el inicio de la palabra siguiente o el fin de la última), `[pause 0.6]`, `{mostrado|hablado}` cuando lo que se ve difiere de lo que se dice (`{20|veinte}`, `{API|a pe i}`), líneas `> nota` ignoradas. **Escribe las cifras y siglas en su forma hablada** o con `{mostrado|hablado}`: no hay normalización de números en español.
- **Control de calidad:** `matchRate` (fracción de palabras habladas confirmadas por el oído). **< 0.85 = revisa guion o audio** (~90 % es normal; **< 0.5: archivo equivocado**). Las no confirmadas tienen tiempo **interpolado, no medido**. Una palabra de varias partes solo cuenta como confirmada si se oyeron todas. Una palabra > 1.2 s suele ser un tiempo **estirado sobre un silencio** (habla entrecortada): comprobar con la forma de onda (`timeline_view.py`); si el metraje trae subtítulos quemados, esos son el mejor reloj.
- **SRT:** corta por puntuación final, pausa > 0.6 s o duración > 6 s; ≤ 42 caracteres por línea con 2 líneas balanceadas; cue termina 0.25 s después de la última palabra. Reglas de legibilidad: `captions-subtitles.md`.
- **Límites:** verificado solo con datos sintéticos; el idioma importa (acentos se pliegan, no hay lematización); un guion muy distinto del audio no se «arregla», se detecta (`matchRate` bajo).

## 3. Verificar las líneas cortadas (take-one `vo.py`) y la mezcla final
- **Voz hecha de varias tomas o cortada de un archivo largo:** corta de silencio a silencio (`vad_segments.py`), **transcribe cada línea cortada** y compárala con el guion antes de renderizar. Cada línea con ~0.6 s de relleno de silencio; en inglés palabra por palabra, en CJK similitud ≥ 0.92.
- **Sobre la mezcla final** (voz + música): vuelve a reconocer el habla y compara con el guion; un acierto que cae < 0.8 por escena (o < 0.85 global) significa que **la música tapa la voz** (`sound-design.md` §5).
- Si la voz es de una herramienta TTS: se vio en una pieza real que **un dominio con guion se leyó como la palabra «guion»**: no escribas direcciones web en el texto hablado; usa `{mostrado|hablado}` con la forma hablada.

## 4. Voz local (candidato; requiere aprobación de Guille)
**explainroo y argo usan Kokoro (82 M, ONNX, CPU, ~400 MB de modelos)** con Whisper local por frase. Alternativa a ElevenLabs sin créditos ni salida de datos. **No está instalado ni probado.** Antes de proponerlo: instalarlo cuesta ~400 MB y `npm install`; las voces en español son solo 3 (`ef_dora`, `em_alex`, `em_santa`), dependen de espeak-ng y **no se escucharon**; Kokoro no es seguro para llamadas concurrentes (generar en serie). Es una decisión de Guille (voz de la marca ≠ voz del sistema); no se instala sin su sí.
Si algún día se adopta, el patrón útil es: **trocear en frases** (silencio entre frases 0.3 s, entre párrafos 0.55 s), recortar el silencio de cada trozo, **re-transcribir cada trozo en el mismo equipo** y alinear contra el guion como arriba.

## 5. Demos de producto desde un recorrido (patrón de argo; sin instalar nada)
Para una pieza que muestra una **web o app que Guille controla** (no un producto ajeno):
1. **Manifiesto de escenas único** (nombre, texto hablado, voz, velocidad, overlay): se valida **sin ejecutar nada** que cada escena tenga su marca y que los nombres coincidan (mayúsculas incluidas).
2. **Voz primero:** se genera la voz de cada escena y se escribe su duración en un JSON; el recorrido (Playwright o a mano) **espera `duración(escena)`** en vez de pausas fijas; cada clip de voz se coloca en su marca con **separación mínima de 100 ms** entre clips.
3. **Preparar fuera de cámara** (login, tema, navegación), empezar a grabar y **re-anclar el reloj** para que la primera marca caiga en t ≈ 0.
4. **Cursor humano determinista:** curva Bézier con semilla, duración 300–1100 ms según la distancia (`300 + 700·dist/diagonal`), 18–64 pasos, easing in-out, aterrizaje en el padding del elemento (no tapa la etiqueta), **350 ms de pausa antes del clic**, clic con eventos reales (se comprueba que el elemento es accionable). Misma lógica para un cursor dibujado en una pieza HyperFrames: 1.3–1.55× al pasar sobre algo, −15 % al pulsar, onda al clic, **clic y cambio de estado en el mismo fotograma**; mover 0.3–0.8 s, leer 1–2.5 s.
5. **Zoom como metadato:** el recorrido solo **registra** (caja, tiempos) y el zoom se aplica **al exportar** con `zoompan` (con el tiempo por fotograma; `crop` no evalúa w/h por fotograma), después de las transiciones, a la fps de la grabación; así los overlays ya quemados no se escalan raro. Desenfoque de movimiento solo durante la ventana del zoom (`tblend=all_mode=average` con `enable='between(t,…)'`).
6. **Captura sin pérdida con relleno por reloj de pared** (la captura emite fotogramas solo cuando la página cambia: repetir el último para cubrir huecos) y export de calidad en un segundo pase; avisar si el rendimiento cae por debajo del 50 % del fps.
7. **Acabado de export:** etiquetas BT.709 (`scale=out_color_matrix=bt709:out_range=tv`, `-colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv`), `loudnorm` (`sound-design.md` §5), capítulos y `.srt`.
**Riesgos de la herramienta (por eso no se instala):** `argo add` descarga archivos de terceros cuyos `<script>` se ejecutan dentro de la página grabada y cargan CDN sin integridad; los `argo.config.mjs` corren con privilegios completos de Node; CI solo en Ubuntu; repo de 704 MB. Para un producto **ajeno**, no (derechos y términos). Verifica antes de afirmar: **«qué es verdad hoy»** — cada función, cifra y pantalla del pedido se comprueba contra el producto real; lo que no existe se declara «ilustración».

## 6. Edición mínima por comentario (idea de huashu-motion)
En lugar de rehacer la pieza ante un cambio: **variables** para lo que se cambia a menudo (títulos, cifras, colores, pausas), **ids estables** en lo que una persona señala y **etiquetas de escena** en la línea de tiempo; el comentario lleva el instante exacto y el objeto señalado; el agente edita **solo eso**, dice **qué lectura tomó** si era ambiguo («una suposición sin decirlo no funciona»), guarda una nota de una línea («pausa 1.2 → 2.0 s, el resto se corre 0.8 s») y mantiene el historial para deshacer. Una petición de tiempo («mantén un beat más») desplaza lo que viene después y mantiene anclados los eventos posteriores. `production-workflow.md` §11 lo usa como ficha de arreglo.
