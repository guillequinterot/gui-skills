---
name: video-aprender
description: Sub-skill de video-editing-ai-agent para APRENDER de un video y EJECUTAR a partir de lo aprendido. El usuario da un link o un archivo (una clase con ecuaciones o pizarra, una reunión grabada con un cliente, un video de referencia) y dice «léelo», «analízalo», «aprende de esto» o «qué se acordó»; la skill lo descarga si es link, transcribe el audio en local, extrae cada estado estable de la pantalla (diapositivas, ecuaciones, pizarra, hojas de cálculo), alinea lo que se dijo con lo que se mostró, verifica las ecuaciones recalculándolas, saca decisiones, cambios solicitados y pendientes con cita y minuto, y propone un plan de ejecución que NO ejecuta sin confirmación. Tres modos: contenido (clases, tutoriales, finanzas), reunión (acuerdos y cambios del cliente) y estilo (ritmo, gancho y voz de un video de referencia). Usar ante «video-aprender», «aprende de este video», «analiza esta reunión/clase/grabación», «te mando un link/video para que lo entiendas», «qué dijeron/mostraron», «sácame los pendientes/acuerdos de la reunión», «entiende las fórmulas del video», «qué puedo aprender de este video de referencia».
---

# video-aprender

## Protocolo gui-skills (obligatorio)

Esta skill vive en el repo **gui-skills** y sigue [`shared/protocolo-skill.md`](../../shared/protocolo-skill.md):

1. **Paso 0 — cada vez que uses la skill:** corre `python <repo>/tools/check_update.py --quiet --pull`.
   `ACTUALIZADA n` → díselo al usuario en una línea y **vuelve a leer este `SKILL.md`** antes de seguir;
   `CAMBIOS_LOCALES` → avisa y no actualices; `SIN_RED` / `SIN_CREDENCIAL` → sigue con la copia local y dilo.
   Si avisa de aportes sin publicar, corre `python <repo>/tools/publish_job.py --reintentar` (preaprobado).
   Luego lee `HANDSHAKE.md` y el "Registro de trabajos" de `HANDOFF.md`.
2. **Privacidad:** en el repo los clientes solo se nombran con un código `caso-<tipo>-<NN>`; nunca
   nombres, marcas, dominios, correos, rutas personales ni credenciales.
3. **Paso final — obligatorio y preaprobado** (trabajo terminado y aprobado por el usuario; no pidas permiso):
   (1) `python <repo>/tools/log_job.py --skill video-aprender ...` por cada skill que intervino (qué se hizo, qué
   salió bien, qué salió mal, incidencias); (2) actualiza `HANDSHAKE.md` si cambió el estado vivo;
   (3) publica con `python <repo>/tools/publish_job.py --tema <caso-o-tema>` (rama + push + PR; el mantenedor
   puede añadir `--merge`); (4) dile al usuario el resultado (`PR_CREADO <url>` / `PUBLICADO <url>` /
   `PENDIENTE` / `BLOQUEADO`). Obsidian es opcional: si el usuario lo tiene, registra también allí.

`<repo>` = `repo_path` de `~/.gui-skills/config.json`, o dos carpetas arriba de esta skill.

Sub-skill de **`video-editing-ai-agent`** (decisión del mantenedor, 2026-10-16). Esa skill aporta las herramientas; esta aporta el **proceso de aprender y ejecutar**. No duplica scripts: todos viven en `video-editing-ai-agent/scripts/`.

- Scripts: `<repo>/skills/video-editing-ai-agent/scripts/` (si la skill está instalada por enlace en `~/.claude/skills/`, `~/.claude/skills/video-editing-ai-agent/scripts/` apunta al mismo lugar). En este archivo `<scripts>` = esa carpeta.
- Procedimiento completo: `references/procedimiento.md` (léelo antes de la primera ejecución de la sesión). Ecuaciones: `references/ecuaciones.md`. Reuniones: `references/reuniones.md`.

## Qué eres en este modo
**No ves ni oyes video**: lees **texto** (la transcripción) e **imágenes** (los estados estables de la pantalla). Por eso el método es: transcribir en local → extraer cada estado estable de la pantalla → alinear palabra por palabra → leer las imágenes en orden → **verificar** lo que se pueda recalcular → concluir con evidencia → proponer, y solo tras confirmación, ejecutar. Lo que no se pueda ver u oír se declara, no se inventa.

## Flujo (siempre en este orden)
1. **Qué quiere aprender o ejecutar.** Si no lo dijo, **una** pregunta. Para una **reunión**, recuerda que es confidencial: todo se procesa **en local** (Whisper local; nada se sube a ningún servicio) y los archivos quedan en la carpeta del proyecto.
2. **Elegir modo** (`--modo`): `contenido` (clase, tutorial, ecuaciones, pizarra, hoja de cálculo), `reunion` (acuerdos y cambios), `estilo` (cómo está hecho un video: ritmo, gancho, voz).
3. **Una sola llamada** (link o archivo; **varios links → `aprender_lote.py`**, ver abajo):
```bash
python "<scripts>/video_aprender.py" FUENTE --modo contenido --goal "qué quiero aprender" [--lang es] [--section 0-600] [--rapido] [--glosario trading] -o <carpeta del proyecto>/referencias/<nombre>
```
   - Un **link** se baja con `fetch_reference.py` y sus protecciones (un video por llamada, sin cookies salvo que el sitio las pida, registro en `fetch-log.jsonl`). **Requiere autorización explícita de cada usuario** para instalar yt-dlp y, solo si el sitio pide sesión, usar las cookies del navegador; el mantenedor la tiene concedida en su PC. Si eres otra persona, pídela en el chat la primera vez (ver `video-editing-ai-agent/references/fetch-reference.md`).
   - **Tiempo:** la transcripción corre a ~1× el tiempo del audio en esta CPU (modelo `small`): una reunión de 1 h tarda ~1 h. Avísalo **antes**, lánzala **en segundo plano** y ofrece `--rapido` (menos precisión) o `--section` (empezar por un tramo). El avance se guarda cada minuto y se reutiliza si se interrumpe.
   - **Link largo:** si pides un tramo (`--section`) y la descarga se cuelga, el script cancela y baja el video completo (plan B); avísalo, puede pesar >100 MB. Los minutos que reporta son los de la clase original.
   - **Clase en un video de aula (cámara con el profesor y el público) con archivo de diapositivas:** añade `--slides diapositivas.pdf --sin-pantalla`. **Pídele al usuario el archivo original**: del video de aula las ecuaciones no se leen (medido: 480p, diapositiva de ~190 px). Sin el archivo, solo se obtiene lo que el profesor **dice**.
   - **Varios links (reels, clases, un curso):** `python <scripts>/aprender_lote.py fuentes.txt -o <proyecto>/investigacion/<fecha_tema> --goal "..." --glosario <dominio> [--rapido] --prefijo reel` → una carpeta por fuente + `lote-resumen.md`; uno tras otro con pausa, **reanudable** (salta lo ya hecho), un fallo no detiene el lote. Lánzalo **en segundo plano** y avisa el tiempo (≈ 1 min de pared por minuto de audio; 11 reels = 26 min).
   - **Glosario de dominio (`--glosario trading`):** el vocabulario va al reconocedor como `hotwords` (actúa en todas las ventanas de 30 s) y se corrigen en `contenido.md` los errores de oído **ya vistos** (`assets/glosarios/<nombre>.json`; el crudo queda en `transcripcion.json`). Para otro dominio, crea otro JSON **solo con errores reales observados**.
   - **Pantalla sin estados estables** (una persona a cámara, o una **cámara filmando un monitor** con manos delante: casi todos los reels de Instagram): el script lo detecta (< 4 estados) y hace solo el **muestreo de fotogramas**: fotogramas repartidos (el más nítido de ±0.5 s) + uno donde la voz señala la pantalla («podemos ver», «miren»…) y una **hoja de contacto** `pantalla/muestreo/hoja.jpg`: mira **la hoja primero** (todo de un vistazo) y abre a resolución completa solo el fotograma de la cifra que necesites (`ffmpeg -ss T -i video -frames:v 1`).
   - **Instagram (público): funciona sin cookies** (`fetch_reference.py info/video` y `video_aprender.py URL`), ofrece hasta 1440×2560; **siempre con `-o <carpeta del proyecto>`** (si no, la salida por defecto es la carpeta actual y, si estás dentro de la skill, el script se niega).
   - **`--rapido`** ahorra ~18 % (reel de 63 s: 47.4 s → 38.9 s) con 98.8 % de coincidencia de palabras: úsalo para **explorar y en lotes**; con cifras o nombres propios que importen, el modo normal + glosario.
4. **Leer, en este orden:** `contenido.md` (evidencia cruda: lo dicho alineado con cada estado de la pantalla) → **cada imagen** de `pantalla/slides/` (1280 px: se leen ecuaciones; si son pequeñas, `frame_probe.py --at T --crop x,y,w,h --scale 2`).
5. **Verificar** (ecuaciones y cifras): transcribirlas a texto, nombrar variables y unidades, **recalcularlas con Python** con los números del propio video y probar casos límite (`references/ecuaciones.md`). Marcar **[verificado]** solo lo recalculado.
6. **Completar `analisis.md`** (plantilla ya creada junto a la evidencia) citando **minuto y diapositiva** y el tipo de cada afirmación: [visto] · [dicho] · [verificado] · [inferido] · [no sé].
7. **Aprender:** (antes, **clasifica la fuente**: un reel o video de captación comercial —termina con «comenta X para recibir…»— da **pistas, no evidencia**; varias piezas de una misma cuenta = **una** fuente; lo dicho se marca [dicho] hasta recalcularlo o verlo en pantalla). Mapa de conceptos, ejemplos resueltos recalculados, dudas y lo que el video no aclara o contradice. Si pidió material de estudio: resumen, tarjetas, ejercicios con solución recalculada. Los aprendizajes de **estilo o método** que valgan la pena van a `save_learning.py add` (candidato hasta repetirse en ≥ 3 fuentes o ser aprobado por el usuario).
8. **Destino de lo aprendido:** antes de volcar nada, lee **la plantilla y las reglas del proyecto de destino** (p. ej. en un proyecto de trading: su *plantilla obligatoria de hipótesis*, entornos separados y la etiqueta «solo investigación»; en un proyecto con flujo de propuestas, ese protocolo) y registra con ese formato, no con el tuyo. Si el destino es un proyecto con handshake controlado, **no lo edites a mano**: deja una propuesta y avísalo.
9. **Ejecutar:** presenta el **plan de ejecución** (sección 8 de `analisis.md`: acción · evidencia que la origina · riesgo · si necesita permiso) y **espera confirmación**. Solo entonces actúa, con las puertas normales de cada herramienta (copias de respaldo, nada de enviar mensajes o publicar sin permiso explícito) y registra el resultado en `video-handoff.md` del proyecto y en el «Registro de trabajos» del `HANDOFF.md` de esta skill (si el usuario usa Obsidian, también en la nota de su proyecto).

## Reglas duras
- **Evidencia o no se afirma.** Cada decisión, cambio solicitado o cifra lleva la frase y el minuto; si el audio no lo dice, es [ambiguo] y se pregunta.
- **No distingo quién habla** (sin diarización): no atribuyo frases a personas salvo que el audio lo diga o el usuario lo confirme.
- **Una ecuación o cifra no está entendida hasta estar transcrita y recalculada.** Si la transcripción y la imagen discrepan, manda la imagen y se avisa; si no se puede leer, se marca ilegible.
- **No doy asesoría financiera personalizada.** Puedo explicar los conceptos y hacer cálculos con los números que el usuario aporte, pero no recomiendo qué comprar, vender o contratar.
- **Análisis y referencia, no copia:** no se reutilizan recursos, texto ni diseño ajeno; no se republica lo descargado. La licencia declarada del video (`licencia declarada` en la ficha) **no equivale a permiso de uso**.
- Nada se sube a servicios externos de análisis de video (`video_analyze`, `media_summarize`…) sin permiso explícito.
- Lo que no se pudo verificar se lista siempre al final del análisis.

## Qué mide cada modo
| Modo | Produce | Para qué |
|---|---|---|
| `contenido` | `transcripcion.json`, `pantalla/slides/*.jpg`, `contenido.md` (voz alineada por palabra con cada estado de la pantalla), `analisis.md` | entender una clase, tutorial o demostración y poder aplicarla |
| `reunion` | lo mismo + plantilla de decisiones, cambios solicitados con cita y minuto, pendientes y **plan de ejecución a confirmar** | traducir una reunión en cambios concretos sin inventar acuerdos |
| `estilo` | `mapa/` (planos, hojas de contacto), `metricas.json`, `ficha-aprendizaje.md` | aprender el ritmo, el gancho y la voz de un video de referencia |

## Estado y límites conocidos (2026-10-16, actualizado en el 2.º uso real)
- Probado: modo estilo con un archivo local y con un link real (*Big Buck Bunny*, 10 min); detector de pantalla con un video sintético de pizarra (6 de 6 estados, sin falsos positivos en una diapositiva estática muy comprimida; `--roi` y alineación con PDF con pruebas negativas); modo contenido con una clase sintética y con una clase real de MIT OCW (ver `references/procedimiento.md`, «Validación realizada»).
- **Medido con una clase real de MIT** (8 min, desde el enlace): transcripción fiel; detección de diapositivas **no fiable en video de aula** (cámara(s) y 480p) → se resuelve con el PDF original; ecuaciones de ese PDF verificadas con Python. **Probado en el 2.º uso real (11 reels de Instagram, 25 min de audio):** descarga pública sin cookies, transcripción fiel salvo términos técnicos (corregidos con glosario), cifras de gráficos leídas del fotograma y recalculadas (GARCH, triple barrera, Sharpe deflactado); detector de estados estables **no sirve** con una cámara filmando un monitor (0–3 estados en reels con 6 gráficos) → muestreo de fotogramas. **Sin probar:** una reunión real con varias personas, grabaciones de pantalla reales (solo sintéticas), videos de más de 1 h, cookies, TikTok.
- Whisper puede **equivocar cifras, nombres propios y siglas**, y su marca de «dudoso» no es infalible: contrasta siempre con la imagen.
