# Subtítulos y texto en pantalla

## Fuente de texto
Copy/guion oficial del cliente (hoja o brief) MANDA sobre la transcripción; la transcripción solo da los tiempos. Corrige palabras mal oídas ("Tired" vs "tire").

## Tiempos por palabra
`python scripts/transcribe_words.py <video> --lang en --model small` → JSON `{clip: [{s,e,w}]}` (faster-whisper local, sin subir audio).
- Whisper pone el inicio de la primera palabra tras un silencio en 0.0 → corrige con `silencedetect=noise=-38dB:d=0.12` (inicio real = `silence_end`).
- Convierte a tiempo global: `t_global = t_clip + offset_clip_en_timeline` (en Shotcut el clip derecho de una transición empieza en su `start_frame`, con su origen en source frame 0).
- `frame = round(t·fps)`.

## Estilos usados/validados
| Estilo | Motor | Resultado |
|---|---|---|
| Frases con borde negro | PNG+overlay (ffmpeg) | Legible; no editable en Shotcut |
| Pista SRT burn-in | Shotcut `set_subtitle_track` | Editable, estático, borde limitado |
| Clip de texto por frase (pop+fade) | Shotcut `add_generator text` | Editable + animado; borde máx 3 px → usar banda oscura |
| **Palabra por palabra** (elegido por el cliente) | Shotcut, 1 clip/palabra, `scripts/caption_words.py` | "Más cool"; fusionar palabras cortas si parpadean |

## Legibilidad
- Zona segura Reels/TikTok/Shorts: no bajar de ~y=1500/1920 ni subir de ~y=250 (UI de la app). Texto centrado en y≈0.68 de la altura.
- Banda `#a6000000` (65 %) + `pad 26` da lectura sobre fondo claro/oscuro; bajar a ~45 % si se ve pesada.
- Palabras muy cortas (the/of/and) en pantalla 0.2–0.4 s parpadean: unirlas a la siguiente ("the space") si el cliente lo pide.
- Mayúsculas solo en el hook; frases en minúsculas normales.
- Chunking clásico (video-use): 2 palabras por bloque cortando en puntuación, o 4–7 palabras "natural sentence"; máx 4 palabras/30 caracteres por línea (super-video-maker); corte si hay hueco de voz >0.7 s.

## ASS (solo si el ffmpeg tiene libass)
`Alignment=2,MarginV=90,Outline=4-5,Shadow=1-2`, palabra activa amarilla `&H0000FFFF`, pop-in `{\fad(120,80)\t(0,180,\fscx104\fscy104)\t(180,360,\fscx100\fscy100)}`. Rutas `C\:/...`.

## Idioma y CTA
Copy en el idioma de la campaña (caso-video-02: inglés). Teléfonos: oficina primero, luego asesor (regla del cliente). Pantalla final con espacio de lectura ≥3.5–4 s, jerarquía: llamado → teléfono destacado → oficina.

## Reglas de control de calidad (v1.3, de `embedded-captions` de HyperFrames, Apache-2.0)
Verificar antes de dar por buenos unos subtítulos animados:
- Cada rótulo **≥ 0.5 s** en pantalla (los más cortos no se leen; ver también "palabras muy cortas").
- Tiempos de palabra dentro de **±80 ms** de la transcripción; la ventana de cada grupo contiene todas sus palabras.
- Agrupar **2–5 palabras** por línea, cortando en cláusulas (no en medio de una frase).
- Contraste legible (WCAG). Texto claro sobre fondo con luminancia 60–180 necesita velo/banda; por encima de 180 usar texto opaco.
- Nada se sale del cuadro. Si hay un rótulo "grande detrás del sujeto", dejar al menos el 30 % de la cara libre en cada ventana de 0.3 s y separar estos efectos ≥ 0.6 s (solo para los picos de énfasis).
- **Rechazar o avisar** antes de subtitular un clip con: varios hablantes, cortes duros, audio casi mudo, subtítulos ya quemados o transcripción ilegible. Esto se comprueba con `video_understand.py` (planos, `speech_ratio`, segmentos sospechosos) y `vad_segments.py`.
- Alineación fina: `vad_segments.py --words words.json --key clip.mp4` lista las palabras de Whisper sin voz debajo (alucinación o mal tiempo).

## Generador para HyperFrames (v1.3)
`python scripts/hf_captions.py words.json --key clip.mp4 [--offset s] [--fps 30] -o captions` agrupa las palabras con las reglas anteriores (cláusulas repartidas en grupos **equilibrados** de 2–5 palabras, sin palabras huérfanas; ≥ 0.5 s; sin solapes; tiempos de las palabras cuantizados a 1/fps) y escribe `captions.json` y `captions-snippet.html` (los `<div>` + el código GSAP `fromTo`/corte para pegar en `index.html`). Probado con las 111 palabras de banco-pruebas-video (30 rótulos de 2–5 palabras, 0 solapes, 0 rótulos < 0.5 s) y con una prueba de reglas en `selftest.py`; **el render con estos rótulos aún no se ha probado** (pendiente del video desde cero). Antes de generar, corrige el **texto** de las palabras con el copy oficial (no sus tiempos); el inicio de la primera palabra tras un silencio largo suele venir en 0.0 (ver arriba). También hay bloques `caption-*` en el catálogo de HyperFrames (`engine-hyperframes.md`, "Reutilizar antes de construir").

## Subtítulos desde el guion (v1.5)
Si hay un guion hablado, **no subtitules lo que oyó Whisper**: `python scripts/align_script.py guion.txt words.json --srt guion.srt` pone el texto del guion con los tiempos por palabra de Whisper y reporta `matchRate` (detalle en `references/narracion-y-demos.md` §2). Reglas del SRT que aplica (de explainroo): corte por puntuación final, pausa > 0.6 s o duración > 6 s; ≤ 42 caracteres por línea con 2 líneas balanceadas (cortando tras puntuación si ambos lados ≥ 12 caracteres); el cue termina 0.25 s después de la última palabra; 1–4 palabras por subtítulo en vertical, con una entrada de ~6 fotogramas de overshoot de escala (fuente: awesomeclaude, sin probar); máx. ~3.5 palabras/s y mín. max(1.8 s, hablado + 0.6 s) (video-director). Estas cifras se suman a las reglas de control de calidad de arriba; no las reemplazan.
