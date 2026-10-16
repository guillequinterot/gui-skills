# Oficio de edición: proceso, reglas duras, cortes, EDL y memoria

Incorporado en v1.1.0 desde `browser-use/video-use` (MIT, leído en crudo el 2026-09-21; ver `NOTICE.md`), adaptado a Shotcut + ffmpeg en Windows. Lo que aquí dice "regla dura" es de **corrección de producción**; todo lo demás es criterio artístico (ejemplos trabajados, no mandatos).

## Principios
1. **Razona desde la transcripción + imagen bajo demanda.** El único artefacto derivado que vale la pena es la transcripción empaquetada por frases (`takes_packed.md`, `scripts/pack_transcripts.py`). Muletillas, repeticiones y tomas se deciden al momento de editar.
2. **Audio primero, la imagen sigue.** Los candidatos de corte salen de límites de palabra y huecos de silencio; `timeline_view.py` solo en puntos de decisión (no como barrido).
3. **Preguntar → confirmar → ejecutar → iterar → persistir.** No toques el corte hasta que el usuario apruebe el plan en lenguaje llano.
4. **Generaliza.** No supongas qué tipo de video es: mira el material, pregunta, luego edita.
5. **Verifica tu propia salida antes de mostrarla** (autoexamen, `self_eval.py`).
6. **Inventa técnicas si el material lo pide** (split-screen, PiP, L/J-cuts, speed ramps, freeze frames, match cuts): Shotcut y ffmpeg pueden con ellas.

## Reglas duras (corrección, no gusto) y cómo se cumplen aquí
| # | Regla | En Shotcut/MLT | En ffmpeg |
|---|---|---|---|
| 1 | Subtítulos al FINAL de la cadena (después de todo overlay) | Pista de texto/subtítulos por ENCIMA de las demás pistas | `overlay` de subtítulos/PNG en la última etapa |
| 2 | Extraer por segmento + concatenar sin recodificar (no un filtergraph gigante) | No aplica (el proyecto compone en el render) | segmento a segmento (`-c copy` en el concat) |
| 3 | Fundido de audio de **30 ms** en cada borde de corte | `edl_to_shotcut.py --audio-fade-ms 30` (keyframes de `volume_db`, interpolación **linear**) | `afade=t=in:st=0:d=0.03,afade=t=out:st={dur-0.03}:d=0.03` |
| 4 | Overlays con `setpts=PTS-STARTPTS+T/TB` | El clip en su posición de timeline ya empieza en su frame 0 | así, o `overlay=enable='between(t,a,b)'` |
| 5 | Subtítulos en tiempos de la **línea de salida**: `t_out = word.start - seg_start + seg_offset` | `frame = start_frame + (t_src*fps - in_frame)` (ver `caption_words.py`) | igual, en el SRT maestro |
| 6 | Nunca cortar dentro de una palabra | usar límites de palabra de la transcripción | idem |
| 7 | Padding en cada borde de corte: **30–200 ms** (ej.: 50 ms antes / 80 ms después); Whisper/Scribe se desvían 50–100 ms | `edl_to_shotcut.py --pad-in/--pad-out` | idem |
| 8 | Transcripción palabra a palabra literal (no modo SRT/frase: pierde huecos y muletillas) | `transcribe_words.py` | idem |
| 9 | Cachear transcripciones por fuente; no re-transcribir salvo que el archivo cambie | guardar `words.json` junto a las fuentes | idem |
| 10 | Varias animaciones ⇒ subagentes en PARALELO (nunca secuenciales) | `assets/animation-slot-brief-template.md` | idem |
| 11 | Confirmar la estrategia antes de ejecutar | plan corto aprobado | idem |
| 12 | Salidas de sesión en `<carpeta_proyecto>/edit/`; nunca dentro de la carpeta de la skill | idem | idem |

Nota: video-use recomienda transcripción hospedada (ElevenLabs Scribe) por su fidelidad literal; nuestra skill usa **faster-whisper local** por privacidad/coste. Whisper normaliza algunas muletillas y desplaza inicios tras silencios largos (corregir con la envolvente de energía). Scribe solo con permiso explícito (sube audio a un tercero y cuesta dinero).

## Estructura de carpetas de trabajo
```
<proyecto>/
├── fuentes (intactas)
├── video-handoff.md            ← traspaso + memoria por sesión (ver handoff-handshake.md)
├── handshake.json
└── edit/
    ├── transcripts/words_<clip>.json   ← caché (regla 9)
    ├── takes_packed.md                 ← lectura principal
    ├── edl.json                        ← decisiones de corte
    ├── animations/slot_<id>/           ← fuente + render + razonamiento por animación
    ├── verify/                         ← PNG de autoexamen
    └── final / preview (exportaciones)
```

## Proceso (9 pasos)
1. **Inventario**: `ffprobe` de cada fuente; `transcribe_words.py`; `pack_transcripts.py`; una o dos `timeline_view` de primera impresión.
2. **Pre-escaneo de problemas**: una pasada por `takes_packed.md` anotando tropiezos verbales, errores evidentes y frases a evitar (alimenta el brief del editor).
3. **Conversar**: describe lo que ves y pregunta según el material: tipo de contenido, duración/formato, dirección estética/marca, ritmo, momentos a conservar o cortar, animación, color, subtítulos. Sin lista fija.
4. **Proponer estrategia** (4–8 frases: forma, tomas elegidas, dirección de cortes, animación, color, subtítulos, duración estimada) y **esperar confirmación**.
5. **Ejecutar**: EDL → `edl_to_shotcut.py` (o proyecto manual) → animaciones/textos → color por clip → audio.
6. **Preview** (contact sheet o render de borrador).
7. **Autoexamen antes de mostrar**: `self_eval.py` sobre la SALIDA renderizada (cortes ±1.5 s, primeros/últimos 2 s, 2–3 puntos medios; duración vs EDL; picos/LUFS; clics de audio; negros/congelados). Si algo falla → corregir → re-renderizar → re-evaluar. **Máximo 3 pasadas**; si persiste, avisa al usuario en vez de entrar en bucle.
8. **Iterar y persistir**: feedback en lenguaje natural sin re-transcribir; render final a petición; actualizar `video-handoff.md`.
9. **Cierre**: prompt de música con duración real (si hay música), log de la skill si aprendiste algo, entrada en el «Registro de trabajos» del HANDOFF de la skill (y nota en Obsidian si el usuario lo usa).

## Oficio de cortes
- **Audio primero.** Candidatos: límites de palabra y silencios. Silencios ≥400 ms = cortes más limpios; frases de 150–400 ms = usables con revisión visual; <150 ms = inseguros (a mitad de frase).
- **Preserva picos**: risas, remates, énfasis; extiende más allá del remate para incluir la reacción (la risa ES el golpe).
- **Relevos entre hablantes**: 400–600 ms de aire (menos si es rápido, más si es cinematográfico).
- **Eventos de audio** `(risas)`, `(aplausos)`: marcan beats; extiende más allá.
- **Nunca razones audio y video por separado**: cada corte debe funcionar en ambas pistas.
- Padding ejemplo: 50 ms antes de la primera palabra conservada y 80 ms después (30–50 ms energía de montaje; 100–200 ms cine/documental).

## Transcripción empaquetada
`pack_transcripts.py words.json -o takes_packed.md` → una línea por frase: `[002.52-005.36] texto`, rompiendo en huecos ≥0.5 s o puntuación final. Da precisión de palabra con ~1/10 de tokens del JSON crudo.

## Brief para el subagente editor (selección de tomas)
Plantilla en `assets/editor-brief-template.md`. Estructura de carga: entradas (takes_packed.md, contexto narrativo de 2 frases, hablantes, estructura esperada, tropiezos a evitar, duración objetivo) + reglas (límites de palabra, padding, silencios ≥400 ms, tropiezos inevitables se conservan si no hay mejor toma, presupuesto de tiempo) + salida (JSON de EDL, sin prosa).
**Arquetipos** (elige, adapta o inventa): lanzamiento/demo HOOK→PROBLEM→SOLUTION→BENEFIT→EXAMPLE→CTA · tutorial INTRO→SETUP→STEPS→GOTCHAS→RECAP · entrevista (PREGUNTA→RESPUESTA→SEGUIMIENTO)* · viaje/evento LLEGADA→MOMENTOS→CALMA→SALIDA · documental TESIS→EVIDENCIA→CONTRAPUNTO→CONCLUSIÓN · música INTRO→VERSO→CORO→PUENTE→OUTRO · anuncio corto de Meta (nuestro caso): HOOK→ESCENA 1→ESCENA 2→CTA.

## EDL (contrato de traspaso)
`assets/edl-schema.json` (compatible con el formato de video-use: `sources`, `ranges[{source,start,end,beat,quote,reason}]`, `grade`, `overlays`, `subtitles`, `total_duration_s`). `grade` = nombre de preset, cadena ffmpeg cruda o `auto`. Rutas relativas se resuelven respecto a la carpeta del EDL.

## Color (cuando se pida o se detecte necesidad)
Razona sobre la imagen: mira un fotograma (`timeline_view`), decide qué falla, ajusta UNA cosa, vuelve a mirar. Modelo mental ASC CDL: `out=(in*slope+offset)^power` (slope=luces, offset=sombras, power=medios). `scripts/grade.py`: presets `subtle`, `neutral_punch`, `warm_cinematic` (creativo, opt-in) y `--analyze/--auto` (corrección acotada ±8 %, sin cambios de color creativos). En Shotcut se aplican como filtros `avfilter.eq/colorbalance/curves` (`grade.py --mlt-ops PRESET`, o `"grade"` en el EDL). En ffmpeg, por clip (regla: no tras concatenar). Prueba tonos de piel antes de ser agresivo. Fuentes HDR (PQ/HLG): tonemap a Rec.709 antes de exportar (ver `engine-ffmpeg.md`).

## Subtítulos: tres dimensiones
**Chunking** (1/2/3 palabras o frase), **caja** (MAYÚSCULAS/Título/natural) y **posición** (margen inferior). Estilos trabajados de video-use: `bold-overlay` (2 palabras, MAYÚSCULAS, cortar en puntuación, blanco con contorno, `MarginV≈35`) para redes rápidas; `natural-sentence` (4–7 palabras, minúsculas, cortar en pausas naturales, `MarginV 60–80`, fuente mayor) para narrativa/educación. Nuestro estilo validado con el cliente: **palabra por palabra** con pop y banda oscura (`captions-subtitles.md`). Reglas: subtítulos al final (1) y tiempos de salida (5).

## Animaciones
La paleta, tipografía y lenguaje visual salen de la conversación/brief de marca (nunca supongas); si el usuario no dio guía, propón una y confirma antes de construir.
- Motores posibles por “slot”: PIL + secuencia PNG + ffmpeg (tarjetas simples, contadores, máquina de escribir), clips de texto de Shotcut con keyframes (nuestro camino por defecto), y —solo si se instalan y se aprueba— HyperFrames (HTML/CSS/GSAP), Remotion (React) o Manim (diagramas). No están instalados aquí.
- **Duraciones (criterio)**: explicación sincronizada a narración 5–7 s (tarjeta simple) / 8–14 s (diagrama); piso ~3 s. Acentos con música/montaje 0.5–2 s. Mantén el último frame ≥1 s antes del corte. Sobre voz en off: duración ≥ narración + 1 s. Nunca reveles dos cosas nuevas a la vez.
- **Payoff**: toma el timestamp de la palabra clave y arranca la animación `reveal_duration` antes para que el fotograma de aterrizaje coincida con la palabra.
- **Easing** (nunca lineal): `ease_out_cubic(t)=1-(1-t)^3` (revelados) y `ease_in_out_cubic` (trazos continuos). En Shotcut: keyframes intermedios (`scripts/ease_keyframes.py`). Texto tipeado: centrar sobre el ancho de la cadena COMPLETA.
- **Brief de subagente de animación** (uno por animación, en paralelo, autocontenido, “no hagas preguntas”): `assets/animation-slot-brief-template.md`. Un subagente = un archivo (nombres únicos).

## Especificación de salida
Igualar la fuente salvo petición. Formatos habituales: `1920×1080@24` cine, `1920×1080@30` pantalla, `1080×1920@30` vertical social (nuestro caso), `3840×2160@24`, `1080×1080@30`. Pregunta qué formato de entrega importa. Usa el fps **exacto** de la fuente (`avg_frame_rate` como racional, p. ej. 30000/1001) y detecta vertical con rotación (side_data). Niveles de calidad: final (crf 18–20), preview (crf 22, más rápido), borrador (crf 28, ultrafast).

## Memoria por sesión (`video-handoff.md`)
Añade un bloque por sesión: **Estrategia** (un párrafo) · **Decisiones** (tomas, cortes, color, animaciones y por qué) · **Registro de razonamiento** (una línea por decisión no obvia) · **Pendiente**. Al arrancar, léelo y resume la última sesión en una frase antes de preguntar si continuar.

## Antipatrones
Formatos jerárquicos precalculados (USABILITY/tono/capas) = sobreingeniería · funciones a mano para puntuar momentos (el modelo elige mejor) · Whisper en modo SRT/frase · quemar subtítulos antes de componer overlays · un solo filtergraph con overlays (doble recodificación) · animación lineal · cortes de audio duros sin fundido · texto tipeado centrado sobre la cadena parcial · subagentes de animación secuenciales · editar sin confirmar estrategia · re-transcribir fuentes ya cacheadas · asumir el tipo de video.
