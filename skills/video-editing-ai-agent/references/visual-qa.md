# QA visual y revisión

Objetivo: ver el resultado antes de exportar y no afirmar lo que no se comprobó.

## Herramientas
- Shotcut: `render_contact_sheet` (`frames:[...]`, `columns`, `cell_width`) y `render_preview` (un frame exacto). Sin render completo.
- ffmpeg: `fps=1,scale=270:-1,tile=6x2` o frames sueltos con `-ss`. Une con `hstack`. Los nombres con coma decimal rompen rutas en PowerShell → usa nombres sin puntos (chk_1, chk_4).
- Frames a revisar (probe frames): primeros/últimos 2 s, cada corte ±1.5 s (frame de entrada B+3, mitad, pico del efecto, asentado B+8), 2–3 puntos medios, cada frase/palabra de texto, pantalla final.

## Checklist
1. **Estructura**: duración esperada (ffprobe), resolución, fps, códec (h264/yuv420p), audio presente.
2. **Cortes/transiciones**: sin saltos, sin frames negros (blackdetect), transición no pixelada.
3. **Texto**: dentro de zona segura, ≥56 px, legible sobre fondo claro/oscuro, ortografía = copy oficial, teléfonos correctos y en orden (oficina primero).
4. **Marca**: logo visible pero no invasivo, colores del brief.
5. **Audio**: LUFS y pico medidos; voz por encima de música; sin clipping; fades en bordes.
6. **Sincronía**: palabras/beats ±3–4 frames (solo confirmable oyéndolo → dilo).
7. **Legibilidad de la pantalla final**: ≥3.5 s, espacio entre líneas.

## Revisión independiente (patrón video-shotcraft)
Para entregas importantes, lanza un subagente con contexto limpio que revise con el checklist y evidencia por número de frame (`F2 ✗ frame 340: ...`), separando: correcciones obligatorias, mejoras opcionales, puntos no verificables. Quien edita no se autoaprueba.

## Bucle
Máx. **3 pasadas** de corrección; si persiste, reporta al usuario con el problema concreto. Aprobar UNA sección antes de replicar el patrón.

## Qué reportar (fidelidad)
Verificado con medición ≠ visto en contact sheet ≠ no verificado (movimiento, sincronía fina, sonido). Dilo explícitamente. No decir "quedó genial" sin haberlo visto/medido.

## Herramientas de autoexamen (v1.1)
- `python scripts/self_eval.py salida.mp4 --boundaries 2.7,7.4 --expected-duration 17.2` → duración vs esperada, negros/congelados, LUFS/pico, detección de clics de audio en cada corte y PNG de cada corte (±1.5 s), inicio, final y 3 puntos medios. **Lee los PNG** (Read) buscando: discontinuidad visual, subtítulo tapado por un overlay, overlay desalineado, cambio de color entre tomas. Un "congelado" en una tarjeta final estática es esperado.
- `python scripts/timeline_view.py video.mp4 INICIO FIN [--marks t1,t2] [--words words.json --key clip.mp4 --offset s]` → tira de fotogramas + forma de onda con marcas de corte y rótulos de palabras; útil para decidir un corte o revisar una pausa larga (p. ej. el hueco de ~0.6 s entre frases dentro de una toma).
- Máx. 3 pasadas de corrección; si persisten fallos, informa al usuario.

## Entender antes de revisar (v1.2)
Para un video que no conoces (material en bruto, referencia, render ajeno) usa primero `scripts/video_understand.py` y `scripts/frame_probe.py` (`references/video-comprehension.md`). `timeline_view.py` y `self_eval.py` revisan un tramo/corte ya sabido; el mapa decide **dónde** mirar.
- `python scripts/cut_dip.py video.mp4 --cuts t1,t2 [--window 0.5]` (v1.3) → bajón de brillo y **hueco oscuro** (% del ancho) alrededor de cada corte; para comparar dos versiones de una transición con números. El brillo depende del material: el indicador limpio es el hueco.
