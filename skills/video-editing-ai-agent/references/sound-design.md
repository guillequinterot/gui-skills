# Sonido de una pieza: efectos, cues, sincronía y nivel (v1.5)

**Origen:** earshot, Barty-Bart/motion-graphics, huashu-motion, explainroo, video-director (todas MIT; análisis y veredictos en
`analisis-fuentes/14-motion-graphics-nov-2026.md`). Las ideas se reescribieron; no se copió código. **Estado: candidato.** Lo único
verificado aquí es `scripts/sync_audit.py` con audio sintético; los números de abajo son de las fuentes y no están calibrados con
material de Guille. Lo que ya existe y sigue mandando: `audio-mix.md` (voz, música, carve, `loudnorm_audio.py`, `beat_grid.py`).

## 0. Regla madre: Claude no oye
No se dice «suena bien». Se **mide** (sincronía, volumen, pico, qué tapa a qué) y se entregan **5 instantes** para que una persona
los escuche con audífonos. `sync_audit.py` ya imprime «PARA ESCUCHAR CON AUDÍFONOS». Un análisis multimodal «de oído» de una
música se equivocó en BPM, número de notas y tiempos de efectos (huashu-art-motion): cualquier cifra «oída» se valida con un detector.

## 1. Lista de cues (se calcula, no se teclea)
- Un `cues.json` con `[{"t": 2.0, "type": "scene_cut", "id": "…"}]` (o `"f": 75` + `fps`). **Los tiempos salen del código de la imagen**
  (etiquetas de la línea de tiempo, el plan, los cortes detectados), no de una lista escrita a mano: los tiempos tecleados cayeron 8–11
  fotogramas fuera en earshot.
- Si no hay plan: `python scripts/sync_audit.py pieza.mp4 --cuts` usa como cues los **cortes de imagen detectados** en el propio video.
- ids estables tipo `acto:cosa:n` permiten filtrar reglas por tipo y regenerar el número si cambia el origen.

## 2. Gramática imagen → sonido (qué merece un efecto)
| Imagen | Sonido | Nota |
|---|---|---|
| Cursor, hover, scroll, barra de progreso | **nada** | ~75 % del tecleo en pantalla de los films profesionales medidos es silencioso |
| Clic | UN clic (presionar y soltar 60–110 ms después, suelta 0–3 dB más baja) | el clic suena 10–30 ms **antes** del hundimiento visible |
| Tarjeta o chip que aparece | pop suave al ~50 % de su recorrido; en una racha, +1…+3 semitonos por elemento | ponlo en el fotograma de **aterrizaje**, no al inicio del movimiento (con `back.out` llega al ~45 % de la duración; con `expo.out`, la mayor parte del recorrido está en el 30 % inicial) |
| Contador | un tick en el valor final (~8 dB bajo la música) | no un tick por dígito |
| Movimiento de cámara grande | whoosh con el ápice en el pico de velocidad, que empieza 100–450 ms antes | ~2 por pieza |
| Corte duro | **nada**, salvo en un tiempo fuerte | un whoosh por cada corte es la huella más repetida de «hecho con IA» |
| Tensión | riser que **termina** 30–250 ms antes del golpe | |
| Revelación / momento héroe | el golpe de la música en su tiempo fuerte (+ impacto, el sonido más fuerte de la pieza, al 30–60 % de la duración en los films medidos) | un impacto y un chime como máximo |
| Logo final | la música para en una línea de compás, 0.2–0.7 s de casi silencio y UNA nota suave | el logo 8–20 dB bajo el pico; cola de 0.5–2.5 s |
Densidad orientativa: 8–15 golpes por 30 s; una pieza sin una parada de silencio antes de su momento más fuerte «se lee plana».

## 3. Colocación: offsets y separación (valores de partida, medidos en films de lanzamiento por una fuente)
- Offset del sonido respecto del cue (negativo = sonido adelantado): tap −60 ms, knock −40, clic −11, pop +4, pop-in +30, pico de whoosh +37, pico de swell +42.
- Separación mínima entre golpes del mismo rol: ticks 66 ms, teclas 87, pops 114, impactos 100–159.
- Si el efecto empieza en la muestra 0, fade de ~25 ms. Un sonido por cue y **varía la toma** dentro de la categoría (nunca la misma muestra dos veces seguidas; jitter de intervalos ±15–25 % en tecleo): evita el efecto «ametralladora».
- Ganancia de cada efecto **relativa a la cama de música**: 3–10 dB sobre ella (no un nivel fijo); los efectos de apoyo 0.08–0.2 de ganancia y el héroe 0.25–0.35.
- **Stop-down en vez de ducking por efecto:** la música baja 6–12 dB durante 0.3–0.5 s **antes** de un golpe grande y vuelve en el golpe. Bajar la música bajo cada efecto es lo que se oye «ducking». (No contradice `audio-mix.md`: eso habla de la voz; aquí de efectos.)
- **Tolerancia perceptual** (cita de la fuente): se detecta un sonido 45 ms antes o 125 ms después de la imagen; el acento de los films profesionales cae entre −45 y +75 ms (mediana +8). Regla práctica: se acepta hasta 1 fotograma de adelanto; **nunca 2 o más de retraso**. `sync_audit.py` usa −45/+75 ms.

## 4. Medir la sincronía: `scripts/sync_audit.py`
```
python scripts/sync_audit.py pieza.mp4 --cues cues.json [--fps 30] [--early 45 --late 75] [--lufs -16] [--json salida.json]
```
Detecta los golpes del **audio ya mezclado** (flujo espectral con umbral robusto y afinado del ataque en envolvente de 1 ms), mide el
offset de cada cue y lo compara con el **azar**: la fracción del tiempo que quedaría cubierta por algún golpe con esa tolerancia. Con
música densa el azar sube (un film profesional medido: 81 % de acierto frente a 86 % de azar, o sea, nada) y entonces una sincronía alta
**no demuestra nada**: mira el offset de cada cue. Un offset mediano constante > 30 ms es un **retardo fijo** (códec AAC ≈ 1.3 fotogramas a 30 fps, o la colocación): se corrige con una constante, no moviendo cue por cue.
Mide también el MP4 entregado (LUFS y pico). **Límites:** el golpe de un efecto bajo música densa puede quedar tapado (el detector ve la mezcla); no sabe QUÉ suena; verificado solo con ruido sintético.

## 5. Nivel y master (objetivos; ver `audio-mix.md` para el flujo)
- Esta skill: −16 LUFS ±1, pico ≤ −1.0…−1.5 dBTP (`loudnorm_audio.py`). Las fuentes usan −14 LUFS para redes (X, Reels) y −16 para web/diapositivas: **pasar `--social`** cuando el destino normaliza a −14.
- Mide siempre el **MP4 entregado**, no el WAV intermedio. En clips cortos el valor de `loudnorm` puede discrepar de BS.1770: confirma con `ebur128=peak=true`. Seis de siete films profesionales medidos pasaban de −1 dBTP tras el AAC: **deja margen** (apunta a −1.5…−2 dBTP antes de codificar).
- Silencio (definición operativa): ≥ 0.4 s con nivel RMS (ventana de 100 ms) ≥ 15 dB bajo el percentil 90 de la pieza **y** bajo −30 dBFS. Un silencio planeado debe ser realmente silencioso; antes del golpe más fuerte debe haber uno en los 4 s previos.
- Voz y música: la voz ~10–12 dB sobre la música; **que la música no tape la voz** se comprueba volviendo a reconocer el habla sobre la mezcla final (explainroo avisa si el acierto cae < 0.8 por escena): `video_understand.py`/`transcribe_words.py` sobre el MP4 mezclado y comparar con el guion con `align_script.py`.
- Medias de banda 120 Hz–2 kHz dentro de ~6 dB: comprobación barata de que una mezcla no quedó «demasiado grave» sin escucharla.

## 6. Efectos: de dónde salen (decisión pendiente)
- **No se sintetiza música ni efectos con osciladores** como estándar (las fuentes mismas se contradicen: los explainers de una la sintetizan y su skill de sonido lo prohíbe por sonar «a pitidos»). Efectos y música: archivos del usuario, audio aprobado generado por IA (`audio-mix.md`) o una biblioteca **CC0** con su `LICENSES.md`.
- La biblioteca CC0 de Barty-Bart (103 OGG normalizados a −3 dBFS de pico, 12 categorías, `manifest.json` con `alt_categories`) es MIT/CC0 y reutilizable **con aviso**, pero **no está en la skill**: su peso y atribuciones se deciden con Guille antes de copiarla.
- **Licencias de audio, antes de entregar:** preguntar dónde se publica (YouTube, redes, anuncios, TV, juego, plantilla); abrir la licencia VIGENTE de cada fuente; música «no confirmada» hasta que el usuario la confirme; entregar un `CREDITS.txt`. Reglas de las fuentes (verifícalas, cambian): CC0 sin atribución; CC-BY pide crédito; CC-BY-NC nunca en uso comercial; Mixkit no permite redistribuir el archivo suelto ni dentro de una plantilla y su música no vale para TV/radio/juegos; YouTube Audio Library solo para YouTube.

## 7. «Cheap tells» (checklist de QA de audio)
Bips sintéticos; una sola muestra repetida; whoosh en cada corte; boom en cada logo; reverb en sonidos pequeños; tono aleatorio en el tecleo; cobertura parcial (solo algunos cortes con sonido); clics en los cortes; música cortada a media nota; bucle de ambiente audible; logo más fuerte que el golpe principal; final que se corta en vez de dejar cola.

## 8. Sin probar (anotado para no perderlo)
Ajuste de la música a compases por programación dinámica (mover el inicio para que los cortes caigan en el pulso: búsqueda de offset en pasos de 5 ms que minimiza el error corte-a-beat); verificación de la rejilla con el contenido < 120 Hz (`beat_grid.py` ya ajusta sobre graves; criterios de la fuente: ≥ 98 % de beats casan, error medio < 10 ms, deriva < 5 ms); re-ajustar la rejilla sobre el **audio renderizado** para medir el retardo del códec; comprobación de enmascaramiento de voz por stems (voz ≥ 3 dB sobre el resto entre 500 Hz y 4 kHz en ≥ 80 % de sus segundos activos); mono downmix aparte.
