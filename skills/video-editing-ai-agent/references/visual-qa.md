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

## Compuertas v1.5 (de video-director, huashu-art-motion, take-one, reanimate, awesomeclaude; candidato: umbrales sin calibrar con nuestro material)
**Antes de renderizar**
- `python scripts/storyboard_lint.py plan.md` (plan sin defectos mecánicos) y, si hay guion, `python scripts/align_script.py guion.txt words.json` (`matchRate` ≥ 0.85).
- **Hoja de contacto obligatoria** (1 fotograma por segundo o por beat, 4×3) y **leerla con el visor de imágenes**: texto solapado o cortado, texto con menos de ~0.3 s por palabra (mín. 1 s), tiempo muerto, fuente de reserva, ilegible a tamaño de teléfono, fotogramas negros. Para el gancho: una tira de 0–3 s cada 0.5 s a 360 px de ancho (la prueba «sin sonido»).
- **Determinismo** (si la pieza se genera por código): dibujar ~12 fotogramas hacia adelante en una página fría y luego en reversa en caliente; deben salir iguales (si no, nombra el fotograma que envenena a otro: «dibujar X primero cambia Y»). Con `hyperframes check`/`snapshot` ya hay una parte; esto es la prueba de orden.
- **Validar los validadores:** cada comprobación automática debe **fallar a propósito al menos una vez** con una entrada rota; un «todo verde» de un chequeo que no se ejecutó (p. ej. un QA que nunca corrió el código de las transiciones) es peor que no tener chequeo.
**Sobre el MP4 renderizado** (fotogramas de 96×54 en gris, baratos; `self_eval.py`, `motion_energy.py` y `cut_dip.py` ya cubren parte)
- **Fotograma 0** plano o negro = defecto (es el póster). Tramos **congelados** ≥ 1.0 s (cambio medio < 0.25/255) = cada uno debe ser una pausa diseñada. **Flashes** de un fotograma y **pops** (un fotograma salta y vuelve: diferencia con ambos vecinos > 3× y > 2/255 y los vecinos se parecen entre sí) = defecto; cortes detectados contra los planeados (≤ 1 fotograma de error). **Costura de bucle** con `frame_compare.py loop`. **Pendiente:** no hay aún un script de pops/flashes (se escriben a partir de `motion_energy.py`).
- **Volumen y sincronía:** `python scripts/sync_audit.py pieza.mp4 --cues cues.json` (`sound-design.md`). Primer sonido a los ~0.13 s en los films profesionales medidos; sin huecos > 0.04 s salvo silencio deliberado.
- **Texto** (guía; con HyperFrames lo hace `hyperframes check`): pequeño = sostenido ≥ 0.6 s con altura < 3.3 % del alto (< 4.3 % = aviso, ≈ 36/46 px a 1080p); relámpago = tarjeta ≥ 3.5 % del alto en pantalla menos de 0.4 s + 0.2 s por palabra; cortado por el borde ≥ 0.8 s; texto pequeño fijo en una esquina ≥ 6 s; dos textos distintos superpuestos ≥ 0.3 s; `NaN`, `undefined`, `Infinity` o `[object Object]` visibles = error; texto sobre una cara. Gancho ≥ 84 px y llamada a la acción ≥ 48 px a 1080 px de lado corto, contraste 7:1.
- **Movimiento rápido** (huashu-art-motion, calibrado por su autor con 13 videos, «no hay contraejemplos», no demostrado): fracción de fotogramas con cambio medio ≥ 9/255 entre vecinos dentro de un plano: < 0.035 rojo, < 0.06 amarillo. Y **las métricas de quietud nunca deben ser puerta** (un explainer bueno tiene mucha quietud): solo admite lo que separa limpiamente positivos de negativos o hechos duros (plano vacío ≥ 0.3 s, fondo azul-violeta ≥ 30 % de los fotogramas).
**Revisión independiente (refuerzo del patrón de arriba)**
- El revisor es un agente **nuevo, sin el contexto de quien construyó**; recibe el encargo, el MP4 final, el plan, la **tabla de procedencia del texto en pantalla** (sin ella toma frases oficiales por «inventadas») y los hechos a verificar. Si falta un insumo, marca «no verificable».
- **Rechaza por defecto.** Debe (1) decir el mensaje de la pieza **solo con fotogramas**, (2) puntuar 1–10 con evidencia (fotograma/instante) en: gancho · claridad · legibilidad · calidad del movimiento · ritmo y variedad · composición y look · continuidad · verdad · sincronía del sonido, (3) listar defectos P0/P1/P2 con síntoma, mecanismo probable y arreglo medible, (4) decir «entregar» o «una pasada más» y señalar el plano más débil. **Barra: todos ≥ 8 y ningún P0**; se arreglan los ≤ 7, no se toca lo ≥ 9; una sola ronda de arreglos por defecto (máx. 3 de la regla general).
- **Siempre responde: «¿en qué segmento empieza a distraerse y dónde se aplana?»**: una revisión solo de acierto/error no detecta «aburrida».
- **La autoevaluación infla ~10 puntos** (hasta 17): manda la puntuación independiente, y si discrepan manda la más baja. El informe va atado al **hash (SHA) del archivo final**. Una comprobación parcial no se declara revisión completa (solo capturas ≠ movimiento revisado; solo métricas de audio ≠ escuchado). Un ejemplo que el usuario rechazó se convierte en caso de regresión técnica.
- Anti-falsos positivos (de la segunda pasada de un autoexamen): «informa **solo** los problemas que observes; si no hay, dilo y no inventes una revisión».
