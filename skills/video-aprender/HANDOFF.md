# HANDOFF — video-aprender

> Traspaso entre sesiones y personas: qué es la skill, cómo se instala, qué se decidió y qué se aprendió
> en cada trabajo. Estado vivo (versión, herramientas, pendientes) → `HANDSHAKE.md`.
> Historial técnico de los scripts (que viven en otra skill) → `../video-editing-ai-agent/logs/UPDATE-LOG.md`.

## 1. Qué es y cuándo se usa

**Sub-skill de `video-editing-ai-agent`** (decisión del mantenedor, 2026-10-16). Esa skill aporta las
herramientas (los scripts viven en `../video-editing-ai-agent/scripts/`: `video_aprender.py`,
`aprender_lote.py`, `slides_extract.py`, `save_learning.py`, `fetch_reference.py`, `frame_probe.py`,
`video_understand.py`, `vad_segments.py`); **esta** aporta el **proceso de aprender y ejecutar**:

1. el usuario da un link o un archivo (una clase con ecuaciones o pizarra, una reunión grabada con un cliente,
   un video de referencia) y dice «léelo», «analízalo», «aprende de esto» o «qué se acordó»;
2. se descarga (si es link), se transcribe en **local** (Whisper), se extrae cada estado estable de la pantalla,
   se alinea lo dicho con lo mostrado y se **verifica recalculando** toda ecuación o cifra;
3. se concluye con evidencia (frase + minuto + tipo: visto/dicho/verificado/inferido/no sé);
4. se propone un **plan de ejecución que NO se ejecuta sin confirmación del usuario**.

Tres modos: `contenido` (clases, tutoriales, finanzas), `reunion` (acuerdos y cambios del cliente) y `estilo`
(ritmo, gancho y voz de un video de referencia). No ve ni oye video: lee texto e imágenes.

No es: la skill de edición (eso es `video-editing-ai-agent`), ni una herramienta de asesoría financiera, ni
una forma de reutilizar contenido ajeno (análisis y referencia, no copia).

## 2. Instalación y dependencias

- Viene con el repo gui-skills (`tools/install.ps1` / `tools/install.sh` la enlazan en `~/.claude/skills/`).
  **Requiere que `video-editing-ai-agent` esté instalada** (comparte scripts, glosarios y plantillas).
- Dependencias externas: las de `video-editing-ai-agent` (Python ≥ 3.10, `faster-whisper`, `pillow`, `numpy`,
  ffmpeg; `yt-dlp` para links; PyMuPDF opcional para `--slides`). Ver `../video-editing-ai-agent/HANDOFF.md` §2.
- Todo se procesa **en local**: ni audio ni video se suben a ningún servicio (tampoco `video_analyze` /
  `media_summarize` sin permiso explícito). Una reunión con un cliente es confidencial: los archivos quedan en la
  carpeta del proyecto del usuario, **nunca** en el repo.
- **Descarga con yt-dlp y cookies:** requiere autorización explícita de cada usuario; el mantenedor la tiene
  concedida en su PC. Las protecciones de `fetch_reference.py` (un video por llamada, sin cookies por defecto,
  salida solo en la carpeta del proyecto con `-o`, `fetch-log.jsonl`) valen siempre.

## 3. Decisiones vigentes

| Fecha | Decisión | Quién la aprobó | Por qué |
|---|---|---|---|
| 2026-10-15 | Sub-skill propia, no un modo escondido de la skill de video: «aprender de un link o archivo y ejecutar tras confirmación» | Guille | Es un proceso distinto de editar; los scripts se comparten, el proceso no |
| 2026-10-15 | **Ejecutar solo tras confirmación**, acción por acción o en bloque; una aprobación general cubre lo listado, no lo que aparezca después | Guille | Lo aprendido puede estar mal oído o mal leído |
| 2026-10-15 | Una ecuación o cifra no está entendida hasta estar **transcrita y recalculada con Python**; si voz e imagen discrepan, manda la imagen | Guille (por evidencia) | Whisper confunde cifras, nombres propios y siglas |
| 2026-10-15 | Un aprendizaje de **una sola fuente es un candidato**; se promueve con la cita del usuario o al repetirse en ≥ 3 fuentes distintas (`save_learning.py` lo exige) | Guille | Evitar convertir una observación en regla |
| 2026-10-16 | Contenido de captación comercial = **pistas, no evidencia**; varias piezas de una misma cuenta = **una** fuente | Guille (por evidencia) | Un reel afirmó algo falso (0.99^100 = 37 %) |
| 2026-10-16 | **Glosarios de dominio** (`--glosario`) como `hotwords` del reconocedor y corrección solo de errores **ya vistos**; `initial_prompt` no sirve | Guille (por evidencia) | `initial_prompt` solo actúa en la 1.ª ventana de 30 s |
| 2026-10-16 | Pantalla sin estados estables (cámara filmando un monitor): **muestreo de fotogramas** con hoja de contacto; mirar la hoja primero | Guille (por evidencia) | El detector dio 0–3 estados en reels con 6 gráficos |
| 2026-10-16 | Sin asesoría financiera personalizada: se explican conceptos y se calcula con los números del usuario | Guille | No somos asesor |
| 2026-10-16 | Antes de volcar ideas a un proyecto de destino, leer **su** plantilla y reglas; si tiene handshake controlado, se deja una **propuesta** y no se edita | Guille | Respetar el flujo del proyecto de destino |

## 4. Registro de trabajos

> Una entrada por trabajo terminado o implementado y aprobado. Solo se agregan entradas al final; las
> correcciones van como entrada nueva. Casos solo con código `caso-<tipo>-<NN>`. Formato:
> `templates/entrada-de-trabajo.md`. Se escribe con `tools/log_job.py`.

<!-- registro:inicio -->

### 2026-10-15 · banco-pruebas-video · guille

- **Qué se hizo:** Creación y primeras pruebas de la sub-skill: `video_aprender.py` (3 modos), `slides_extract.py` (estados estables de pantalla/pizarra por bloques 8×8, `--roi`), `save_learning.py` y plantillas de análisis. Pruebas con una pizarra sintética, una clase sintética con voz, el modo estilo sobre un video público de 10 min (144 planos, 4.5 min de punta a punta) y una **clase pública real de MIT OpenCourseWare** (8 min, descargada desde el enlace; 1216 palabras, 181 palabras/min) con el PDF oficial de diapositivas: ecuaciones de dos páginas y las 60 celdas de una tabla de factores verificadas con Python.
- **Salió bien:** Transcripción fiel de la clase real; pizarra sintética 6/6 estados sin falsos positivos en una diapositiva estática muy comprimida; alineación con el PDF: prueba negativa → 0 asignaciones y prueba positiva (minutos 26–34) con coherencia 0.91 y 3 páginas propuestas; selftest 26/26.
- **Salió mal / incidencia:** Seis fallos reales hallados con datos reales: (1) un título con dos puntos de ancho completo reventaba al imprimirse por una tubería cp1252; (2) la descarga por TRAMO de yt-dlp + ffmpeg se colgaba 18 min → tiempo límite + plan B (video completo y recorte local); (3) los minutos de un tramo salían relativos al recorte; (4) la alineación con PDF daba confianza 1.0 por una coincidencia suelta; (5) endurecer la palabra distintiva mató también los positivos reales (lo que discrimina es la puerta de coherencia de la secuencia); (6) la banda de coherencia fija de 6 páginas cubría todo un PDF de 8 (ahora escala con su tamaño); además un ffmpeg hijo quedaba huérfano al cancelar por tiempo (`taskkill /T`). La **detección de diapositivas no es fiable en un video de aula** (cámaras, 480p, diapositiva de ~190 px): hace falta el archivo original.
- **Regla candidata:** Para una clase en video de aula, pedir el archivo de diapositivas y usar `--slides … --sin-pantalla`.
- **Herramientas:** faster-whisper 1.2.1 (`small`, CPU, ≈ 1–1.5× el tiempo real); PyMuPDF 1.27; yt-dlp 2026.08.19; ffmpeg n8.1.2.

### 2026-10-16 · caso-aprendizaje-reels-01 · guille

- **Qué se hizo:** 2.º uso real: 11 reels públicos de Instagram sobre ML y cuantitativo para trading (25 min de audio) en un lote reanudable (`aprender_lote.py`, sin cookies, 26.2 min). 6 gráficos/fórmulas leídos de fotogramas y recalculados con Python (GARCH, triple barrera, Sharpe deflactado, probabilidad de stop por régimen); verificación en `verificacion_calculos`. Las ideas se registraron como hipótesis de solo investigación en los proyectos de trading del usuario (`caso-trading-01`), como propuesta y sin tocar su handshake controlado. Resultado: v1.4 de los scripts (lote, glosario `trading`, muestreo de fotogramas automático, `--rapido`).
- **Salió bien:** Instagram público sin cookies 11/11; `--rapido` −18 % con 98.8 % de coincidencia de palabras; glosario + `hotwords`: «GARCH» natural las 9 veces (antes «Garche»); 16 fotogramas de un reel mostraron todos sus gráficos; cifras leídas del fotograma y recalculadas (σ² = 0.8160 frente a 0.8159 en pantalla; vida media 73.4 días; SR* 0.52–3.86 según N); una afirmación del reel refutada por cálculo.
- **Salió mal / incidencia:** El detector de estados estables dio 0 estados en 8 de 11 reels y 1–3 en los demás (cámara filmando un monitor con manos delante); Whisper `small` desconoce la jerga (`Garche`, `Horst`, `Finvert`, `esoblos`, `shared ratio`, `Cuckoo`, `baptism`…); voz e imagen discreparon en cifras (51 % visto frente a 52 % oído); `fetch_reference.py` desde la carpeta de la skill se negó a escribir (el `-o` por defecto es la carpeta actual).
- **Regla candidata:** Clasificar la fuente antes de aprender (captación = pistas, una cuenta = una fuente); lanzar el lote en segundo plano y avisar el tiempo antes (≈ 1 min de pared por minuto de audio).
- **Herramientas:** yt-dlp 2026.08.19; faster-whisper 1.2.1 (`hotwords`); ffmpeg n8.1.2; Pillow; numpy.

<!-- registro:fin -->

## 5. Reglas candidatas (sin aprobar)

| Regla | Visto en (casos) | Estado |
|---|---|---|
| Procesar 2 reels en paralelo no gana tiempo en 4 núcleos | caso-aprendizaje-reels-01 | sospecha, no medida |
| Cuándo conviene el modelo `medium` en vez de `small` + glosario | caso-aprendizaje-reels-01 | sin medir |
| Hotwords con vocabulario largo podrían sesgar la transcripción de una charla ajena al dominio | caso-aprendizaje-reels-01 | no observado ni medido |
| Extraer automáticamente las cifras de un gráfico (OCR) en vez de leerlas a mano | caso-aprendizaje-reels-01 | idea |
| Umbrales de alineación con PDF (calibrados con 3 tramos de una sola clase) | banco-pruebas-video | por recalibrar con más clases |
