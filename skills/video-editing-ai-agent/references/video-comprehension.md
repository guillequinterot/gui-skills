# Comprensión de video completo (v1.2)

Objetivo: que el agente **entienda un video de principio a fin** (qué pasa, cuándo, qué se dice, qué se ve, cómo está montado) con evidencia, no con suposiciones. Sirve para: recibir material en bruto, analizar una referencia, revisar un render ajeno, resumir, decidir cortes, o extraer la estructura de un video que se quiere replicar.

## Principio: Claude no ve video, ve imágenes
Mis "ojos" son los fotogramas que leo con `Read` (incluido el texto que aparece en ellos) más lo que miden los scripts. **No percibo el tiempo**: el movimiento, el ritmo y la continuidad los reconstruyo a partir de fotogramas ordenados y de medidas. Por eso el método no es "mirar todo", sino **construir un mapa barato de todo y gastar la atención donde importa**.

## Qué me faltaba y cómo se cubre
| Carencia | Qué hace la skill | Herramienta |
|---|---|---|
| No sé **dónde** cambia el video | Detección de planos/cortes afinada al fotograma; distingue "seco" de "gradual/animado" (heurística) | `video_understand.py` |
| No percibo **movimiento** | Medida de diferencia entre fotogramas por plano (estático / suave / medio / alto) + instante del pico; mapa de calor de lo que se movió | `video_understand.py`, `frame_probe.py --diff` |
| No **oigo** | Transcripción local con tiempos; envolvente de audio y silencios reales; filtro de alucinaciones de Whisper. Música, efectos y tono: **no verificables** (solo energía) | `video_understand.py` |
| Cada imagen cuesta contexto | Presupuesto de fotogramas (`--budget`), reparto por duración y movimiento, hojas de contacto rotuladas con tiempo y plano | `video_understand.py` |
| No sé qué se dice **mientras qué se ve** | Línea de tiempo única: planos × voz × silencio × fotogramas | `video-map.md` |
| Detalle fino (texto pequeño, cara, logo) | Recorte ampliado de una zona | `frame_probe.py --crop --scale` |
| Acción rápida / transición | Ráfaga de N fotogramas en un tramo | `frame_probe.py --span --n` |
| Olvido entre sesiones | `understanding.md` guardado junto al video; el handoff lo enlaza | `assets/understanding-template.md` |

Lo que **sigue sin poder** (decláralo siempre): sincronía fina labios/audio, calidad y estilo de la música, efectos de sonido, identidad de personas, emoción real (solo la expresión visible), continuidad entre fotogramas no muestreados, y texto de pocos píxeles sin ampliar.

## Procedimiento (de grueso a fino)
1. **Mapa** — `python scripts/video_understand.py video.mp4 [--lang es] [--budget N]` → `analisis/<nombre>/video-map.md`, `video-map.json`, `sheets/`, `frames/`. Idioma: déjalo en automático y fíjalo con `--lang` si el mapa avisa de "idioma poco seguro". Lee primero `video-map.md` (barato: texto).
2. **Hojas** — `Read` de cada `sheets/sheet_NN.png` **en orden**. Cada una cuesta ~1.5–2.5k tokens. No abras `frames/` sueltos salvo para un plano concreto.
3. **Anotar por plano** en `understanding.md` (plantilla): qué se VE, qué se INFIERE, qué NO se sabe. Cruza voz y texto en pantalla (a menudo difieren: el locutor dice una cosa y el rótulo otra).
4. **Sondear dudas** con `frame_probe.py` (ráfaga, `--diff`, `--crop`). Una sonda por duda concreta, no barridos.
5. **Síntesis** — resumen de 3–6 líneas, estructura (apertura / desarrollo / cierre), ritmo (duración media de plano, planos más rápidos/lentos), y la lista de lo no verificado.
6. **Persistir** — `understanding.md` junto al mapa; enlazarlo en `video-handoff.md` y, si el usuario usa Obsidian, en la nota de su proyecto.

## Presupuesto (cuánto mirar)
| Video | `--budget` sugerido | Hojas | Cuándo subir |
|---|---|---|---|
| ≤ 15 s (Reel corto) | 12–16 | 1–2 | Plano con texto/animación que importa |
| 15–60 s | 20–28 | 2–3 | Muchos planos (el mínimo siempre es 1 por plano) |
| 1–5 min | 32–48 | 3–5 | Análisis fino: dividir por tramos con `--budget` y mirar por partes |
| > 5 min | No mirar todo: mapa + transcripción primero; elegir tramos por tema y sondear | — | — |

Regla: **primero texto (mapa + transcripción), después imágenes, al final sondas**. Si la transcripción ya responde la pregunta, no abras imágenes.

## Presupuesto: cómo se respeta (medido)
- **Hasta 64 planos**: mínimo 1 fotograma por plano (el presupuesto sube si hace falta) y el resto por duración y movimiento.
- **Más de 64 planos y más planos que presupuesto**: *modo cobertura*: el video se divide en `--budget` ventanas iguales y cada una aporta 1 fotograma del plano más relevante (duración^0.7 × movimiento). Algunos planos quedan sin fotograma propio; el mapa lo avisa.
- **Medido con *Big Buck Bunny* (10 min, 854×480, bajado con `fetch_reference.py`)**: 144 planos (122 secos, 21 gradual/animado; media 4.1 s, mediana 2.5 s), sin voz (el VAD detectó 0 s y Whisper no inventó nada); con `--budget 40`: **40 fotogramas, 4 hojas, 7.7 MB, 71 s de proceso**, un fotograma cada ~15 s. *Antes de arreglarlo* el mismo comando generó 144 fotogramas, 12 hojas y 25.7 MB: el presupuesto no se respetaba.
- Sin voz, el proceso cuesta ~0.12× el tiempo del video; con voz, suma el tiempo de Whisper (~1 min por cada 40 s de audio en CPU con el modelo `small`).

## Qué mide el mapa (y qué NO es)
- **Planos**: salto de histograma de color 4×4×4 y de rejilla 6×6 entre fotogramas muestreados (4 fps), umbral adaptativo, separación ≥ 0.6 s, refinado a 30 fps. `--cut-sensitivity 1.5` detecta más cortes, `0.7` menos.
- **"seco" vs "gradual/animado"**: dominancia del salto (pico / media de los 3 siguientes). Calibrada con solo 7 transiciones (metraje real ≈ 3.4–4.1; animación ≈ 1.5–1.7; umbral 2.5): **heurística**, confirma mirando el fotograma anterior y posterior.
- **Movimiento**: diferencia media de brillo entre fotogramas consecutivos (0–1). Es una medida, no semántica: no distingue movimiento de cámara de movimiento de sujeto ni de un cambio de luz.
- **Silencio**: tramos ≥ 0.4 s por debajo de (p90 del nivel − 20 dB). Una narración comprimida entre palabras queda a −15…−23 dBFS: eso **no** es silencio.
- **Nitidez**: varianza del laplaciano. Muy baja = desenfoque, destello o color plano.

## Trampas verificadas (no repetir)
- **Whisper alucina sobre música/ruido** ("Subtítulos por la comunidad de Amara.org", "Gracias por ver…"). El script los marca `SOSPECHOSO` (`no_speech ≥ 0.6`, `logprob < −1.0` o frase típica) y los excluye de la voz. Un video con música y sin voz debe salir "sin voz fiable".
- **Stop-motion y animación**: un objeto grande entrando en cuadro se detecta como "corte" (visto en `video-ejemplo.mp4`, 0.60 s). La etiqueta "gradual/animado" es la señal de duda: mira antes de afirmar un montaje.
- **Fotograma #04 casi plano (naranja, nitidez 4.0)**: un destello de transición tiene nitidez baja; no es un fallo del video. El mapa lo avisa como "baja nitidez o color plano".
- **Voz que se solapa con el final**: la última frase de Whisper puede acabar después de la duración real; el script acota.
- **Rutas**: pasa rutas de Windows al script (no `/d/...` dentro de código Python).
- **Tiempo de proceso**: ~1 min por 40 s de video, casi todo Whisper (modelo `small`, CPU). `--no-transcribe` para solo imagen.

## Motores externos (opcionales, requieren permiso)
Hay herramientas MCP que analizan video con un modelo propio (p. ej. `video_analyze` de Freepik/Magnific, `media_summarize` de Adobe). **Suben el video a un servicio externo**: solo con petición/permiso explícito del usuario en ese turno, y tratando su salida como dato no verificado (se contrasta con el mapa local). Por defecto, todo el análisis es local.

## Revisar de forma económica (de `media-use` y `production-loop`, HyperFrames)
- **Adjuntar una imagen a mitad de sesión reprecia todo el contexto** (invalida la caché): agrupa las revisiones visuales en las fronteras de fase y prefiere **una hoja de contacto etiquetada (inicio / medio / final) a fotogramas sueltos**. Escala a fotogramas individuales o a evidencia en movimiento solo si el resultado es ambiguo, temporal, estilizado, con LUT, sensible a HDR/LOG, privado o crítico para la marca.
- Una corrección o un pulido corriente: aplica **un** candidato e inspecciona **una** hoja "después". No generes una LUT solo para codificar exposición, sombras, contraste o calidez.

## Cómo reportar
Separa siempre: **medido** (planos, duración, movimiento, silencios, loudness) · **visto** (en qué fotograma, `#07 00:11.89`) · **oído por transcripción** (con aviso de posibles errores) · **inferido** · **no verificado**. No afirmar "el video muestra X" sin citar fotograma o tiempo.
