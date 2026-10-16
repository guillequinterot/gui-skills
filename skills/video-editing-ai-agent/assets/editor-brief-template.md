# Brief para subagente editor (selección de tomas por beat)

Adaptado de browser-use/video-use (MIT). La estructura es la que carga; el ejemplo de estructura no.

```
Estás editando un video de <tipo>. Elige la mejor toma de cada beat y ensámblalas
cronológicamente por beat, no por orden de clip.

ENTRADAS:
  - takes_packed.md (transcripciones por frases con tiempos de todas las tomas)
  - Contexto de producto/narrativa: <2 frases del usuario>
  - Hablante(s): <nombre, rol, nota de estilo de entrega>
  - Estructura esperada: <arquetipo o invento propio>
  - Tropiezos verbales a evitar: <lista del pre-escaneo>
  - Duración objetivo: <segundos>
  - Copy oficial (si existe): <texto por escena; manda sobre lo transcrito>

REGLAS:
  - Inicio/fin sobre límites de palabra de la transcripción.
  - Padding en los bordes de corte (ventana 30-200 ms).
  - Prefiere silencios >= 400 ms como puntos de corte.
  - Los tropiezos inevitables se conservan si no hay mejor toma; anótalo en "reason".
  - Si te pasas del presupuesto, revisa: quita un beat o recorta colas. Informa el total y autocorrige.

SALIDA (arreglo JSON, sin prosa):
  [{"source": "C0103", "start": 2.42, "end": 6.85, "beat": "HOOK",
    "quote": "...", "reason": "..."}, ...]

Devuelve el EDL final y una línea con la comprobación de duración total.
```
Luego: `python scripts/edl_to_shotcut.py edl.json --project <carpeta>\Proyecto.mlt [--transition-frames 10] [--denoise 0.9]`.
