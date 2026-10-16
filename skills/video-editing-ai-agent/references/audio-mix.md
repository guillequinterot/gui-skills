# Audio: voz, música, mezcla

## Reglas
- Voz manda. Música 10–14 dB por debajo de la voz mientras se habla; puede subir en la pantalla final sin voz. Programa −16…−14 LUFS, pico verdadero ≤ −1.5 dBFS.
- No sidechain (bombea); usa automatización de volumen o EQ estático (voz: −6 dB a 1.8 kHz en la música, −2 dB a 350 Hz).
- Fades de audio 30 ms en cortes; música con fundido de entrada corto y salida de 1.3–3 s.
- Música de stock: **no existe en Magnific/Freepik** (sin audio en el catálogo). El usuario aporta el archivo o aprueba explícitamente audio generado por IA (Gemini/Magnific).
- Medir siempre; no adivinar.

## caso-video-02 Reel #02 (referencia real)
- Voz cruda: −22.9 / −27.3 LUFS → +5 dB (picos −7…−10 dBFS, sin distorsión).
- Música `Open_Floor_Plan.mp3` (66.9 s): energía por segundo por RMS; tramo 0:00–0:17 (intro suave 0–8 s, groove desde ~8 s). Keyframes de `volume_db`: 0:−14, 60:−12, 200:−12, 250:−17, 375:−17, 405:−7, 465:−7, 504:−50.
- Resultado medido: habla −19.0 LUFS (mezcla), final −19.2 LUFS, pico −2.4 dBFS. (Algo bajo para Reels; subir mezcla +3–4 dB si se pide.)
- Denoise RNNoise 0.9: pausas −2.5 dB, nivel típico −3 dB, voz −0.6 dB (`p10` por ventanas de 50 ms).

## Prompt de música (entregar SIEMPRE con cada video, antes de exportar)
Al terminar de armar un video, calcula la duración real (frames/fps) y da al usuario un prompt para generar la música (Gemini u otro). Pide `duración + 0.5–1 s` (se recorta y se hace fundido); indica la estructura por tiempos según el montaje (cambios de escena, revelado, CTA). Plantilla:
```
Create a <N>-second instrumental background track for a <plataforma> video from a home painting company (<marca>).
Style: <estilo>, <BPM>, major key, warm and confident. No vocals, no spoken words, no risers or cymbal crashes.
Structure (<N> s total, sync to the edit):
- 0:00–<t1>: <sección 1: p. ej. calm, sparse, leaves room for narration/visual>
- <t1>: <momento clave: p. ej. gentle lift at the before→after reveal>
- <t1>–<t2>: <sección 2>
- <t2>–<N>: <cierre/CTA: resolves warmly, clean final note, no long reverb tail>
Mix: leave headroom, keep mid frequencies uncluttered, background level under <voz/sin voz>. Stereo, one continuous track, loop-free.
```
Sin voz en el video (carrusel/before-after): la música puede llevar más presencia (−12…−8 dB en la mezcla); con voz, 10–14 dB bajo la voz.

## Limpieza de voz
- Shotcut: `rnnoise` (mix 0.6–1.0; 0.9 conserva naturalidad). Filtro propio (link/filter): `add_filter service:rnnoise`.
- ffmpeg: `highpass=f=80`; `afftdn=nr=12:nf=-40` como alternativa si `arnndn` no tiene modelo.
- Ruido puntual (auto pasando) no se elimina del todo.

## Medición
```
ffmpeg -i f.mp4 -vn -af ebur128=peak=true -f null -          # LUFS integrado y picos
ffmpeg -ss A -t D -i f.mp4 -vn -af ebur128=peak=true -f null -   # por tramos
```
Estimación voz vs música: mide clip solo (sin música) y la mezcla; la diferencia da la separación aproximada. Para percentiles de ruido: decodificar a s16le mono 16 kHz y calcular RMS por ventanas de 50 ms con numpy (p10 ≈ suelo de ruido).

## Sincronía con música
**Antes de anclar nada a un compás, ajusta la rejilla con `python scripts/beat_grid.py musica.mp3 [--end 31]`** (periodo y fase sobre los golpes graves reales; 122.0 BPM en la pista de prueba). La autocorrelación gruesa (un lag entero = 23 ms) dio 123 BPM y desplazó los cortes hasta **0.2 s a los 60 tiempos**; `hyperframes beats` da ~122 BPM pero con ~45 ms de latencia y la lista empieza en el segundo tiempo. El script solo mide el compás: **confirma a oído** (o con un golpe visual en un tiempo fuerte) antes de dar la sincronía por buena; anticipar el efecto visual ~0.1 s se siente «en sincronía». Verificación en la salida: el salto de amplitud en los cortes de `self_eval.py` sube de ×0.4–0.8 (cortes fuera de golpe) a ×3–5 (en el golpe); no es un clic.

Beat: `librosa.beat.beat_track(tightness=400)` y ajuste por mínimos cuadrados `t_i=t0+i·T`; `beatF(n)=round((BEAT0+OFFSET+n·T)·fps)`; tolerancia ±3 frames. AAC 48 kHz añade ~1.28 f de latencia a 30 fps (priming ~2048 muestras).

## Entrega
Versión con y sin música si el cliente puede querer cambiarla. Nombres: `..._musica.mp4`, `..._sin-musica.mp4`.

## Normalización de volumen (v1.1)
`python scripts/loudnorm_audio.py entrada.mp4 [-o salida.mp4] [--target -16] [--tp -1.5] [--social]` — mide (pasada 1) y aplica `loudnorm ... linear=true` (pasada 2) con `-c:v copy` (no toca la imagen), escribe archivo NUEVO y reporta antes/después. Probado: Reel con voz −19.3 → −16.0 LUFS (pico −1.4 dBFS). Úsalo cuando la mezcla quede por debajo de −18 LUFS o el usuario lo pida. Objetivos: −16 LUFS/TP −1.5 por defecto; `--social` = −14/−1.0 (YouTube/Instagram/TikTok). Verifica siempre el resultado impreso.
Fundidos de 30 ms en cortes de audio (regla dura 3): ver `edit-craft.md`.

## Carve: música bajo una voz sin que pierda presencia (v1.3)
**Problema.** Bajar toda la música mientras habla la voz (un *duck*) funciona, pero la música pierde toda su presencia durante la voz en off. La voz no necesita todo el espectro, solo las bandas que ocupa (~250 Hz–2.5 kHz). El **carve** baja *solo esas bandas*, siguiendo a la voz, y deja los graves y los agudos: la música sigue siendo música y la voz sigue siendo inteligible. Idea de `hyperframes-audio` (HeyGen, Apache-2.0); implementación propia con ffmpeg.
```
python scripts/carve_music.py --voice voz.wav --bed musica.mp3 -o mezcla.wav [--strength 0.8] [--bed-offset-db -12] [--bed-only] [--voice-delay 0] [--verify]
```
- Cadena: música → `acrossover` (graves | medios | agudos) → **solo los medios** por `sidechaincompress` con la **voz como llave** (ataque 20 ms, liberación **lenta** 450 ms para que la música no "salte" de golpe al terminar cada palabra) → se suman las tres bandas → nivel de la música igualado a `voz + --bed-offset-db` LUFS → mezcla con la voz → limitador en una pasada aparte.
- `--strength` 0..1 (0.8 por defecto): profundidad buscada = 3 + 12 × strength dB. **Medido** con voz sintética y ruido rosa, `--verify`: a 0.3 → medios −6.6 dB; a 0.8 → −9.4 dB; a 1.0 → −10.2 dB; con graves y agudos en −0.4…−1.1 dB. El recorte real suele ser ~70–100 % del buscado. A 0.5 el recorte empieza a oírse como un efecto y no como "espacio para la voz" (HyperFrames); si la música suena "con muescas" y no solo más baja, baja la fuerza. **Baja la fuerza cuando la música es el protagonista y la voz es escasa.**
- **Siempre sigue a la voz** (no hay modo estático): un recorte fijo adelgaza la música en cada pausa. La voz **nunca** se carva contra sí misma; varias voces se mezclan antes en una sola pista. Obligatorio cuando suena música bajo cualquier voz (narración, entrevista, voz en off); se omite solo si no hay voz (video musical, tarjeta de título, montaje al ritmo de la pista).
- **Trampas reales (ya corregidas en el script, con prueba de regresión):** (1) `sidechaincompress` **se cuelga** si la voz y la música duran distinto (se igualan con `apad`); (2) encadenar `alimiter` justo después de `amix` **se cuelga** en el ffmpeg de Shotcut n8.1.2 (el limitador va en otra pasada); (3) toda llamada a ffmpeg lleva tiempo límite.
- **Qué NO se verifica con medición:** cómo suena. Escúchalo.

### Esto y la regla "No sidechain (bombea)" de arriba
La regla viene de una edición real (caso-video-02): un sidechain de **banda completa** bombea. El carve actúa en **una banda** y con liberación lenta, que es justo lo que HyperFrames diseña para evitarlo; pero **no está validado a oído en nuestras piezas**. Hasta entonces: la regla anterior sigue siendo el valor por defecto y el carve es una **alternativa a comparar** (misma pieza con EQ estático, carve 0.5 y carve 0.8; ver `production-workflow.md` §10). Si Guille prefiere el carve, esta sección sustituye a la regla.
**Diagnóstico de un audio que "suena mal" sin poder escucharlo** (de `hyperframes-audio`): el espectro absoluto de una voz desconocida **no se puede diagnosticar** (los formantes varían ±10 dB y las frases decaen 5–6 dB al terminar: todo parece un defecto y todo es el hablante); **compara contra algo del mismo archivo** — el original limpio o las pausas (lo audible en un hueco es aditivo: ese espectro es el canal, no la voz). Comparar con un espectro medio publicado no funciona. Sin original ni silencio utilizable, un defecto tonal estático está subdeterminado: dilo y ofrece las lecturas posibles en vez de elegir una. Tabla síntoma → arreglo: retumbo → pasaaltos a 80 Hz · retumbante/pecho → recorte en ~200 Hz · apagado/mudo → ~250 Hz · palabras difíciles de entender → realce ~3 kHz o carve de la música · áspero → recorte ~3.2 kHz · algunas palabras mucho más fuertes → compresor · ruido de sala entre frases → puerta · "amateur" a secas → pasaaltos + puerta + compresor + EQ (en ese orden).
