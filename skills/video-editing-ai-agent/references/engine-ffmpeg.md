# Motor ffmpeg

Binario: usa el de Shotcut (`%LOCALAPPDATA%\Programs\Shotcut\ffmpeg.exe`, n8.1.2) o uno del PATH. **Ejecuta `scripts/handshake.py`**: informa qué filtros existen. En el build de Shotcut faltan `drawtext`, `ass` y `subtitles` (sin libass/freetype) → texto con PNG.

## Reglas duras (de video-use, verificadas en Windows)
- Extrae cada segmento y concatena; evita un solo filtergraph gigante con múltiples recodificaciones.
- Un solo fps/tamaño/códec/samplerate antes de concatenar sin recodificar: `fps=30,format=yuv420p`, `libx264 -crf 18 -preset medium`, `aac 192k -ar 48000`, `-movflags +faststart`.
- Fades de audio de 30 ms en cada corte (`afade=t=in:d=0.03,afade=t=out:st=<dur-0.03>:d=0.03`).
- Overlays: `setpts=PTS-STARTPTS+<t>/TB` y `overlay=enable='between(t,a,b)'`. Subtítulos/texto AL FINAL de la cadena.
- Fuente vertical: `scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920`.
- Rotación: MLT/ffmpeg autorrotan por metadata; si mides, `ffprobe` da ancho×alto sin rotar (probar `side_data`).
- Rutas Windows en filtros: escapa `C:\` como `C\:/`. Preferir PNG/archivos relativos.

## Zoom / Ken Burns sin temblor
Preescala a 2× y usa `zoompan` con `d=1` sobre video, easing smoothstep por frame (`on`, N = frames del clip):
```
scale=2160:3840:flags=lanczos,zoompan=z='A+(B-A)*(on/(N-1))*(on/(N-1))*(3-2*on/(N-1))':x='iw/2-iw/zoom/2':y='(ih-ih/zoom)*0.22':d=1:s=1080x1920:fps=30
```
(A=zoom inicial, B=final, y=0.22 ancla la cabeza arriba). Stills: preescalar y `zoompan=z='zoom+0.002':...:d=300`. Aplica `unsharp=5:5:0.6` tras escalar mucho (fuentes de baja resolución quedan suaves; dilo al usuario).

## Transiciones
`xfade=transition=smoothleft|smoothup|fade|dissolve:duration=0.25–0.35:offset=<fin_clip_anterior−duración>`; audio con `acrossfade=d=<igual>:c1=tri:c2=tri`. **No usar `zoomin`** (pixelado). Offsets acumulados: `off_k = suma(len) − k·dur`.

## Texto y subtítulos (sin drawtext)
1. Renderiza cada frase/palabra como PNG RGBA 1080×1920 con Pillow (`ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf")`, `stroke_width` 8, sombra desplazada).
2. Entrada cada PNG como `-loop 1 -framerate 30 -t <dur> -i cap.png`.
3. `format=rgba,fade=t=in:st=0:d=0.12:alpha=1,fade=t=out:st=<dur-0.1>:d=0.1:alpha=1,setpts=PTS+<start>/TB` y `overlay=eof_action=pass:format=auto`.
Si el ffmpeg del PATH sí tiene libass, se puede usar ASS (`\fad`, `\t()`, `\fscx/\fscy` para pop-in) — verificar con el handshake.

## Color y audio
- Grade base: `eq=contrast=1.05:saturation=1.1`. Presets (video-use): subtle `eq=contrast=1.03:saturation=0.98`; warm_cinematic `eq=contrast=1.12:brightness=-0.02:saturation=0.88,colorbalance=...`. Probar tonos de piel.
- Loudnorm redes: `loudnorm=I=-14:TP=-1.5:LRA=11` (dos pasadas, `linear=true`); voz+música para Reels a −16…−14 LUFS.
- `highpass=f=80` limpia graves de viento. Reducción de ruido: `arnndn` requiere modelo `.rnnn` (no viene); en Shotcut usar el filtro `rnnoise`.

## Análisis rápido
- Duración/streams: `ffprobe -v error -show_entries format=duration,size:stream=codec_name,width,height -of compact <f>`.
- Silencios (`silencedetect=noise=-38dB:d=0.12`), loudness (`ebur128=peak=true`), negros (`blackdetect=d=0.5:pix_th=0.10`), freeze (`freezedetect`).
- Contact sheet: `-vf "fps=1,scale=270:-1,tile=6x2"`; frames sueltos con `-ss <t> -frames:v 1`.
- Windows/PowerShell: sin heredocs; escribe scripts `.py` a archivo y ejecútalos.

## Añadido en v1.1 (de video-use, MIT)
- **FPS exacto**: usa `avg_frame_rate` (fallback `r_frame_rate`) como racional (`30000/1001`), no redondeado. Un solo fps/tamaño/códec antes de concatenar sin recodificar.
- **Vertical con rotación**: `ffprobe -show_entries stream=width,height:stream_side_data=rotation`; si la rotación es 90/270 intercambia ancho/alto antes de decidir el eje de escala (`scale=-2:1920` vertical, `scale=1920:-2` horizontal).
- **HDR (PQ/HLG)**: si `color_transfer` es `smpte2084` o `arib-std-b67`, antepon el tonemap para salir en Rec.709 SDR (si no, se ve sobresaturado en redes): `zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p` (requiere `zscale`; verifica con el handshake). En Shotcut: `diagnose_color_workflow` y `set_color_workflow`.
- **Niveles de calidad**: final `libx264 -preset fast -crf 20`, preview `-preset medium -crf 22`, borrador `-preset ultrafast -crf 28`; composición final `-crf 18` con `-c:a copy`. Audio siempre `aac 192k -ar 48000`, `-movflags +faststart`.
- **Loudness**: `scripts/loudnorm_audio.py` (dos pasadas, `-c:v copy`); objetivo redes −14 LUFS/TP −1.0 (`--social`) o nuestro −16/−1.5 por defecto.
- **Color por clip**: `scripts/grade.py` (`--analyze`, `--preset`, `--auto`). Aplicar por segmento en la extracción, no tras concatenar.
- **Análisis visual**: `scripts/timeline_view.py` (tira + onda), `scripts/self_eval.py` (autoexamen).
