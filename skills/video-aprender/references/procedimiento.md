# Procedimiento de video-aprender

Sub-skill de `video-editing-ai-agent`. Herramientas: `video_aprender.py` (la llamada única), `slides_extract.py` (estados estables de la pantalla), `fetch_reference.py` (descarga con protecciones), `frame_probe.py` (ampliar o recortar un fotograma), `save_learning.py` (biblioteca de aprendizajes), `vad_segments.py`, `video_understand.py`. Todo en `<repo>/skills/video-editing-ai-agent/scripts/` (si la skill está instalada por enlace, también en `~/.claude/skills/video-editing-ai-agent/scripts/`).

## 0. Por qué este método (qué puede y qué no puede Claude con un video)
| Se puede | Cómo | No se puede |
|---|---|---|
| Entender lo **dicho** | transcripción local con tiempos por palabra (Whisper `small`, VAD de Silero) | oír tono, ironía, dudas, música; distinguir **quién** habla |
| Entender lo **mostrado** | cada **estado estable** de la pantalla como imagen de 1280 px (diapositiva, pizarra, ecuación, código, hoja de cálculo) | ver movimiento o una animación entre dos estados |
| **Unirlos** | alineación palabra por palabra: lo dicho mientras cada estado estaba en pantalla (con 3 s de adelanto, porque se habla antes de escribir) | saber qué señalaba el instructor con el cursor o la mano |
| **Verificar** | recalcular ecuaciones y cifras con Python con los números del propio video | verificar hechos externos sin una fuente |
Claude no ve fotogramas "en vivo": lee imágenes puntuales. Por eso el detector extrae **estados estables** (cuando la pantalla cambió y ya se quedó quieta) y no fotogramas a intervalos fijos.

## 1. Preparar
1. **Objetivo** en una frase (qué se quiere aprender o ejecutar). Es el `--goal` y manda sobre todo lo demás: decide qué se lee con detalle.
2. **Elegir carpeta de salida** dentro del proyecto: `<proyecto>/referencias/<nombre>` (reunión: `reunion-<fecha>`). Si no hay proyecto: una carpeta temporal en `<carpeta-del-proyecto>` y, si el usuario usa Obsidian, una nota candidata en su bandeja de entrada.
3. **Tramos de un link largo:** `--section INICIO-FIN` descarga solo ese tramo, pero **descargar un tramo del medio o del final puede quedarse colgado sin avisar** (visto: 18 min con 1 s de CPU). El script tiene un tiempo límite (`--fetch-timeout`, 600 s) y, si vence, cierra todo el árbol de procesos y hace el **plan B**: baja el video completo y recorta el tramo en local (`tramo_INICIO-FIN.mp4`). **Los minutos de `contenido.md` son siempre los de la clase ORIGINAL**, no los del recorte (si no, citarías un minuto equivocado).
4. **Avisar del tiempo** (la transcripción es ~1× el tiempo del audio con `small`) y lanzar **en segundo plano** si pasa de unos minutos. Opciones: `--rapido` (beam 1: más rápido, algo menos preciso), `--section INICIO-FIN` (un tramo), `--lang es|en` (evita la detección de idioma y reduce errores), `--model` (solo `small` está en caché local; otros modelos exigen descargarlos: pedir permiso).
5. **Confidencialidad**: una grabación de cliente no sale de la máquina (`references/reuniones.md`).

## 2. La llamada única
```bash
python video_aprender.py FUENTE --modo contenido|reunion|estilo --goal "..." -o <carpeta> [--lang ..] [--section a-b] [--rapido] [--sin-pantalla] [--max-slides 40] [--sens 1.0]
```
Produce en `<carpeta>`: `transcripcion.json` (con avance parcial y caché), `pantalla/slides/*.jpg` y `pantalla/overview/*.png`, `contenido.md` (evidencia cruda), `analisis.md` (plantilla por completar). En modo estilo: `mapa/`, `metricas.json`, `ficha-aprendizaje.md`.
- **Video de aula con cámara(s) + archivo de diapositivas**: añade `--slides archivo.pdf --sin-pantalla`. Se renderiza cada página (1280 px), se lee su texto y se **propone** en qué tramo de la voz se explicó cada una (alineación monótona por palabras distintivas, **heurística**). **Cómo decide (calibrado con 3 tramos de una clase real):** una ventana de voz de 30 s cuenta como evidencia con ≥ 3 palabras en común con una página (puntaje idf ≥ 6). **Ninguna ventana aislada separa la explicación real de una charla ajena** (puntajes de hasta 20 en charla ajena, de 8 en explicación real), pero **la secuencia sí**: cuando el profesor explica el PDF, las mejores páginas de cada ventana caen juntas (3, 5, 9, 5, 5, 9, 3); cuando habla de otra cosa saltan por todo el documento (37, 8, 34, 36, 35, 19…). Por eso hay una **puerta de coherencia**: se piden ≥ 4 ventanas con evidencia (y al menos la mitad de las que tienen voz) y ≥ 70 % de ellas dentro de una banda del ~15 % del PDF alrededor de la página mediana; si no, **no se asigna nada** y `contenido.md` dice por qué (también delata un PDF equivocado). Pasada la puerta, una programación dinámica monótona propone las páginas y solo se muestran las de evidencia **media o alta**. **No afirmes «en el minuto X explicó la página N» sin contrastarlo.**
- **Cámara fija con la pantalla en un rincón** (trípode, sin cambios de ángulo): `--roi x,y,w,h` (fracciones 0–1; mira un fotograma para decidirlo) vigila solo la pantalla proyectada. No sirve en producciones con varias cámaras o zoom, ni si la pantalla ocupa pocos píxeles.
- `--sens` > 1 detecta cambios más pequeños (una línea nueva en la pizarra); < 1 solo cambios grandes. El umbral por defecto (0.7 % de los bloques de 8×8) detecta una línea corta de texto nueva y no confunde una diapositiva estática muy comprimida con un cambio.
- Si salen **muy pocas capturas** en un video largo, el script avisa: probablemente es cámara de personas (sin estados estables). Usa `--sens 2` o el modo estilo.
- Si hay **más de `--max-slides`** estados, sube el umbral solo y lo avisa; para no perder detalle, analiza por tramos (`--section`).

## 3. Leer (orden y presupuesto)
1. `contenido.md` completo (texto: barato). Fíjate en el aviso de segmentos **descartados** (ruido o alucinación) y **dudosos** (baja confianza): los dudosos se conservan marcados; contrástalos con la imagen.
2. **Cada imagen de `pantalla/slides/` en orden** (~1.5–2.5k tokens cada una). No abras las `overview` salvo para orientarte: son 2×2 a 780 px de ancho y **no sirven para leer ecuaciones**.
3. **Detalle solo donde importa:** recorte ampliado con `frame_probe.py --at T --crop x,y,w,h --scale 2`; una ráfaga con `--span` si el instructor **dibuja** (para ver el orden en que escribe).
4. Agrupa las revisiones visuales (adjuntar imágenes encarece el contexto): una pasada por las diapositivas, no una imagen suelta cada vez.

## 4. Verificar y completar `analisis.md`
- Contenido: sigue `analisis.md` sección por sección. **Cada afirmación** lleva su cita (`#07 · 12:41` o `[12:41] "frase"`) y su tipo: **[visto] · [dicho] · [verificado] · [inferido] · [no sé]**.
- Ecuaciones y cifras: `references/ecuaciones.md` (transcribir → variables y unidades → recalcular con Python → casos límite → comparar con lo dicho).
- Reunión: `references/reuniones.md` (decisiones, cambios solicitados con cita y minuto, pendientes, cifras a confirmar, plan de ejecución).
- Discrepancias entre voz, imagen y cálculo: **se reportan**; la imagen manda sobre el audio para símbolos y cifras.
- Lo que no se pudo verificar se lista al final (sección 9), sin suavizarlo.

## 5. Aprender (lo que queda después)
- **Entender**: mapa de conceptos en el orden en que el instructor los construye; qué depende de qué.
- **Aplicar**: ejemplos resueltos reproducidos con los números del video y recalculados; ejercicios propios con solución recalculada (si se pidió material de estudio).
- **Recordar**: aprendizajes de **método o de estilo** (cómo explica, cómo estructura, qué ritmo usa) con `save_learning.py add ...`. Un aprendizaje de **una sola fuente es un candidato**: se promueve únicamente con la cita textual del usuario o al repetirse en ≥ 3 fuentes distintas (el script lo exige). Los conocimientos de **contenido** (por ejemplo la fórmula de la anualidad) van a la nota de estudio del proyecto o a Obsidian, no a la biblioteca de aprendizajes.

## 6. Ejecutar (siempre con confirmación)
1. Presenta el **plan de ejecución** (`analisis.md` §8): cada acción, la evidencia que la origina, su riesgo y reversibilidad, y si necesita un permiso aparte.
2. **Espera la confirmación del usuario.** Una aprobación general ("sí, hazlo") cubre lo listado, no lo que aparezca después.
3. Ejecuta con las puertas normales de cada herramienta: copia de respaldo antes de modificar, el flujo de la skill que corresponda (`direct-visual-design`, `video-editing-ai-agent`, `seo-content-system`…), y **permiso explícito aparte** para enviar mensajes o correos, publicar, invitar, crear tareas o editar documentos compartidos.
4. **Registrar** (decisiones, qué se hizo, qué quedó pendiente) en `video-handoff.md` del proyecto y en el «Registro de trabajos» del `HANDOFF.md` de esta skill (Paso final del protocolo, `tools/log_job.py`); si el usuario usa Obsidian, también en la nota de su proyecto y, si cambió una skill o herramienta, en su registro de skills.
5. Entregar con **cada cambio ligado a su cita** y la lista de lo no verificado.

## 7. Errores que esta sub-skill ya cometió y corrigió al probarse (no repetir)
- Detectar planos por **color** no sirve para pizarra o diapositivas (cambian ~1 % de los píxeles): se usa comparación por **bloques de 8×8** contra la última captura y se captura solo cuando la pantalla **ya se quedó quieta**.
- Contar píxeles sueltos con un umbral bajo mete ruido de compresión; con bloques, una diapositiva estática muy comprimida da **1 solo estado**.
- **Descartar** una frase real porque el reconocimiento dudaba perdía contenido: ahora se descarta solo lo claramente falso (sin voz o alucinación típica) y lo dudoso se **conserva marcado**.
- Alinear por **frase** metía en un solo tramo frases que cruzaban varias diapositivas: ahora se alinea por **palabra** (`… palabra palabra …`).
- Whisper estira el final de la última frase más allá del audio real: la voz se acota a la duración del video.
- **Imprimir un título de video con un carácter raro** (`：`, el dos puntos de ancho completo que yt-dlp pone en los nombres para Windows) por una tubería reventaba con `UnicodeEncodeError` (cp1252) **después** de descargar bien: ahora `_common.py` sustituye lo no codificable.
- **Normalizar la puntuación de cada ventana contra su mejor página** daba «confianza 1.0» a una coincidencia de una sola palabra: la evidencia debe ser **absoluta** (≥ 3 palabras distintivas), no relativa.
- Un `ffmpeg` hijo se quedaba **huérfano** (2294 s de CPU) cuando el selftest cancelaba por tiempo a su proceso padre: ahora se cierra todo el árbol (`taskkill /T`).
- **Minutos del recorte frente a minutos de la clase:** en un tramo descargado por URL los tiempos salían relativos al recorte (0:00 = minuto 9:00 de la clase) sin decirlo. Ahora todo `contenido.md` usa el reloj de la clase original y lo declara en la cabecera.
- **Palabras comunes ("down", "price", "since", "years") daban evidencia «media»** en una charla sin relación con las diapositivas. Endurecer la palabra «distintiva» (solo las de pocas páginas) **mató también los verdaderos positivos** (en la parte conceptual, «asset» y «cashflows» están en muchas diapositivas): ni un umbral fijo ni uno relativo servían; lo que discrimina es la **coherencia de la secuencia**.
- **La banda de coherencia fija (±6 páginas) cubría TODO un PDF de 8 páginas** y la prueba dura (coincidencias fuertes pero saltando por el documento) lo dejó pasar: la banda escala con el tamaño del PDF.
- El marcado de «dudoso» **no es infalible**: en una prueba sintética una frase claramente mal transcrita no quedó marcada. Contrastar siempre con la imagen.

## 7b. Errores del 2.º uso real (11 reels de Instagram, 2026-10-16): no repetir
- **`fetch_reference.py` desde la carpeta de la skill**: se negó («no se escribe dentro de la carpeta de la skill») porque el `-o` por defecto es la carpeta ACTUAL. Siempre `-o <proyecto>/referencias`; el mensaje ahora lo dice.
- **El detector de estados estables dio 0 estados en 8 de 11 reels** y 1–3 en los demás aunque 6 de ellos muestran gráficos y fórmulas: la cámara filma un monitor con manos delante (el movimiento medio es 24.6/255, mucho más que un cambio de diapositiva). Se perdía todo lo visual. Solución: **muestreo de fotogramas** automático (hoja de contacto + más nítido de ±0.5 s + fotogramas donde la voz señala la pantalla).
- **Whisper `small` desconoce la jerga**: `Garche`/`Garch` (GARCH), `Horst` (Hurst), `Finvert`/`Fimber` (FinBERT), `esoblos`/`soblogos` (stop loss), `shared ratio` (Sharpe), `Cuckoo` (QQQ), `tripela barrera`, `heteroseasticidad`, `baptism` (backtest). Con `hotwords` (vocabulario del dominio) «GARCH» salió bien las 9 veces; el resto se corrige con el glosario. **`initial_prompt` no sirve** aquí: con `condition_on_previous_text=False` solo actúa en la primera ventana de 30 s.
- **Cifras dichas ≠ cifras vistas**: la voz y la imagen discreparon (barra del 51 % que parecía 52 %; «10×» y «14×» que en pantalla eran otras razones). **Manda la imagen**; una cifra hablada sin respaldo visual queda [dicho], no [verificado].
- **El contenido de captación miente por omisión**: una frase del reel («100 pérdidas seguidas al 1 % queman la cuenta») era falsa al recalcularla (0.99^100 = 37 %). Recalcular **todo** lo recalculable antes de tomar una idea.
- **Un reel citando literatura real no valida el reel** (López de Prado, Engle…): sirve de pista de dónde leer; la evidencia es el paper o nuestros datos.
- **Volcar ideas con tu formato** en un proyecto que ya tiene plantilla y reglas (hipótesis con código propio, entornos separados, «solo investigación»; en un proyecto con flujo de propuestas, se propone y no se edita): lee primero la plantilla del destino. Un handshake controlado (como el del proyecto caso-trading-01) **no se edita a mano**.
- **Procesar 11 videos a mano uno a uno** habría costado 11 llamadas y esperas: `aprender_lote.py` (reanudable, resumen, pausa entre peticiones).

## 8. Validación realizada (2026-10-15/16)
| Prueba | Resultado |
|---|---|
| Pizarra sintética (diapositivas + una línea de ecuación nueva cada 3 s) | **6 de 6 estados**; una diapositiva estática muy comprimida da **1 solo** (sin falsos positivos); `--roi` vigila solo la región pedida (5 estados donde hay texto, 1 donde no hay nada) |
| Clase sintética con voz (SAPI) | transcripción fiel; alineación **por palabra** de lo dicho con cada diapositiva |
| **Clase real MIT 15.401 «Ses 2: Present Value Relations I»** (YouTube, canal oficial de MIT OpenCourseWare, CC BY-NC-SA; primeros 8 min, descargados con `fetch_reference.py` desde el enlace) | descarga + transcripción local: **1216 palabras, 181 palabras/min, transcripción fiel** (apertura de la clase, una subasta y la actualidad financiera de 2008; **todavía sin ecuaciones**). Detección de pantalla: **2 estados** con el cuadro completo y 9 con `--roi`, **pero los 9 eran la misma carátula** desde distintos ángulos de cámara → **la detección de diapositivas no es fiable en un video de aula** (límite documentado arriba). YouTube ofrece esta clase **como máximo a 640×480**: las ecuaciones proyectadas no son legibles en ninguna herramienta |
| Misma clase + **PDF oficial de las diapositivas** (37 páginas, capa de texto) | las páginas 23 y 25 se leen **perfectamente**; sus ecuaciones y las 60 celdas de la tabla de factores de anualidad quedaron **verificadas con Python** (ver `ecuaciones.md`). Alineación: **prueba negativa** (8 min sin relación con las diapositivas) → **0 asignaciones** (una primera versión asignó 6 páginas con «confianza 1.0»: era falsa confianza). **Positiva real** (minutos 26–34): coherencia 0.91, **páginas 3, 5 y 9** propuestas (la 5 con evidencia alta: a las 31:00 el profesor dice literalmente «basic building blocks», que es el texto de la diapositiva 5); es una propuesta **conservadora** (no asigna las páginas 4 y 6–8, que seguramente también se explicaron). **Límite de la calibración:** 3 tramos de una sola clase; con otro material los umbrales podrían necesitar ajuste |
| **2.º uso real: 11 reels de Instagram sobre trading** (25 min de audio, `aprender_lote.py`, sin cookies) | 11/11 procesados en **26.2 min** (77–180 s por reel); 4 de ellos con voz = 1.0× el audio; transcripciones fieles salvo jerga; 0–3 estados estables (cámara filmando monitor) → muestreo de fotogramas; 6 gráficos/fórmulas leídos del fotograma y **recalculados** con Python (GARCH, triple barrera, Sharpe deflactado, probabilidad de stop por régimen); 1 afirmación del reel refutada con cálculo. `--rapido`: −18 % de tiempo, 98.8 % de coincidencia. Glosario + `hotwords`: «Garche»→«GARCH» natural |
| Modo estilo con un enlace real (*Big Buck Bunny*, 10 min) | 144 planos, 14.4 cortes/min, ficha prellenada; 4.5 min de punta a punta |
