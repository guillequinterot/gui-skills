# Obtener material de referencia (yt-dlp) — v1.3

Para **analizar** o tomar como referencia un video de YouTube, TikTok, Instagram u otra plataforma, o para traer material propio. Herramienta: **yt-dlp** (Unlicense) instalada con `pip install "yt-dlp[default]"` (2026.08.19, 2026-10-15) y envuelta en `scripts/fetch_reference.py`. **No se usan scrapers ni descargadores de terceros** (ver `analisis-fuentes/13-herramientas-v1.3-decisiones.md`).

## Autorización (personal de cada usuario)
**Requiere autorización explícita de cada usuario; el mantenedor (Guille) la tiene concedida en su PC desde 2026-10-15** (instalar yt-dlp y usarlo, incluidas las cookies del navegador cuando haga falta, sin pedir aprobación en cada uso mientras sea seguro). Esa autorización **no se hereda**: si eres otra persona, pídela al usuario en el chat la primera vez (qué se instala, que las cookies solo se usan si el sitio pide sesión) y respeta siempre estas protecciones, que el script impone en código:
- Un solo video por llamada, con pausas entre peticiones; nada masivo.
- **Sin cookies por defecto.** Con `--cookies-from-browser` se intenta primero sin ellas y solo se reintenta con cookies si el sitio pide sesión, edad o límite. Las cookies **nunca** se guardan en disco ni se imprimen; el log solo anota "cookies usadas: sí/no" y el navegador.
- Salida siempre en la carpeta del **proyecto** (`<proyecto>/referencias/`), nunca dentro de la skill (el script se niega).
- Cada obtención queda en `fetch-log.jsonl` (URL, título, canal, licencia, qué se bajó, tamaño).
- Uso para análisis y referencia; **no republicar** lo descargado. No se evaden DRM, pagos ni cuentas privadas; si el sitio exige algo más que cookies propias, se informa del fallo.
- Lo que **sí** sigue requiriendo preguntar: algo fuera de lo anterior (descargas masivas, usar la cuenta para acciones —publicar, seguir, comentar—, o cualquier cosa que no sea leer/descargar un video).

## Uso
```bash
python scripts/fetch_reference.py info  URL                    # título, canal, licencia declarada, subtítulos disponibles, resolución
python scripts/fetch_reference.py subs  URL --langs en         # .vtt + transcripción limpia .txt con tiempos
python scripts/fetch_reference.py audio URL --section 0-60     # wav 16 kHz mono listo para transcribe_words.py / vad_segments.py
python scripts/fetch_reference.py video URL --max-height 720 [--section 10-40] -o <proyecto>/referencias
# con cookies solo si hace falta (login, edad, límite):
python scripts/fetch_reference.py video URL --cookies-from-browser firefox
```
Después de bajar: `video_understand.py` para entender el video (mapa + hojas de contacto) y `references/video-comprehension.md`.

## Qué se verificó (2026-10-15, YouTube, *Big Buck Bunny* del canal Blender)
| Modo | Resultado |
|---|---|
| `info` | Título, canal, 597 s, 1920×1080 a 24 fps, subtítulos manuales en/fr y 157 idiomas automáticos |
| `video --section 0-15 --max-height 480` | 15.0 s exactos, 854×480, H.264 + AAC, 1.5 MB, ~18 s |
| `subs --langs en` | `.vtt` (0.00 MB) y `.txt` limpio con tiempos |
| Protecciones | se niega a escribir en la skill (fuente e instalada), rechaza URLs no http(s), registra en `fetch-log.jsonl` |

## Fallos reales encontrados al probar (no repetir)
- `os.path.commonpath` falla si la salida está en otro disco (C: contra D:) → comparar con `try/except ValueError`.
- `--max-downloads 1` hace que yt-dlp termine con **código 101** y, en consultas de metadatos, **aborta antes de imprimir el JSON** → no usarlo en metadatos y tratar 101 como éxito en descargas.
- **YouTube devuelve 429** si se piden subtítulos *auto-traducidos* (p. ej. `es` de un video en inglés): pedir el idioma original o manual, con `--sleep-subtitles`; el script conserva lo que sí se bajó y avisa.
- Whisper/VAD no sirven de nada en un video sin diálogo (los subtítulos de *Big Buck Bunny* son solo efectos "(YAWNS)").

## Instagram (probado 2026-10-16, 11 reels)
- Reels **públicos**: `info` y `video` funcionan **sin cookies**; ofrece hasta 1440×2560 (usar `--max-height 1280` para ~720×1280); el campo duración sale `None` en `info` (se mide al bajar). Un video por llamada con pausa (`aprender_lote.py --pausa 8`). La URL puede llevar parámetros de seguimiento (`?mdxt=…`, `?xtok=…`): se pueden quitar.
- **Siempre `-o <carpeta del proyecto>`**: la salida por defecto es la carpeta actual y dentro de la skill el script se niega.
- Nombre del archivo: `Video by <cuenta> [codigo].mp4` (con corchetes: entrecomillar en shell).

## Límites conocidos (sin probar)
- **Cookies**: implementadas pero **no probadas** (no hizo falta con contenido público). En Windows, Chrome y Edge (v127+) cifran las cookies y yt-dlp suele **no poder leerlas** sin permisos de administrador; **Firefox funciona**. Si falla, el script lo avisa.
- **TikTok**: no probado; suele exigir sesión y cambia a menudo (Instagram público sí funcionó, ver arriba). Si fallan, la alternativa es que el usuario descargue el archivo y lo pase.
- La licencia (`license`) casi nunca viene declarada en YouTube (aquí: "no declarada"); **no equivale a permiso de uso**.
