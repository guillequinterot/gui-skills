# Producir una pieza desde cero (v1.3)

Para cuando se pide **crear** una pieza (explainer, motion graphic, animación de ilustraciones, tarjetas, montaje de escenas) y no solo editar un metraje que ya existe. Adaptado, **reescrito y reducido** de los procesos de HyperFrames (HeyGen, Apache-2.0; `NOTICE.md`): el router `hyperframes`, `references/{brief-contract,intent-interview,pitch-round,production-loop,review-loop,storyboard-format,subagent-dispatch}`, los agentes `motion-graphics/agents/{director,builder,finalize}` y `general-video`. Leídos en crudo el 2026-10-16 (commit `490ecaf`). El motor técnico (HyperFrames o Shotcut) se elige aparte (`SKILL.md`, "Elección de motor"); este documento es el **proceso**.

> Estado: **validado con una pieza propia completa** (Reel «caso-reel-01», 2026-10-16: brief → storyboard → HyperFrames → verificación; modo autónomo, ruta `musica-al-compas`). Resultados de los pendientes en la sección 10. **Sin probar aún**: ruta con voz narrada (carve), subtítulos con `hf_captions.py`, ronda de propuestas con el usuario, subagentes.

## 0. Antes de planear una pieza nueva (v1.4)
1. Lee `references/errores-conocidos-y-aciertos.md` (cada línea cuesta un re-render si se ignora).
2. `python scripts/save_approved.py suggest --route R --format F --tag T`: si hay un video **aprobado** parecido, `recipe ID` da su estructura, receta, lo bueno y lo malo. Es una **recomendación con origen conocido**; el brief actual manda y lo «sin decidir» no es preferencia.
3. Pide **de una vez** lo que falta y suele llegar tarde: CTA y datos de contacto (si la marca ya tiene un cierre, su captura), idioma, si se muestra la dirección. Mide la música (`beat_grid.py`) antes del primer render.

## 1. Empezar por el estado del proyecto (la primera fila que coincida)
| Estado | Acción |
|---|---|
| Existe `BRIEF.md` | Léelo y ejecútalo. No repitas preguntas ya respondidas. |
| No hay brief, pero sí `STORYBOARD.md` o `video-handoff.md` | Reanuda desde los archivos y las preferencias registradas. Si no puedes deducir qué se hacía, haz **una** pregunta de ruta. |
| Edición puntual en un proyecto existente | Hazla, conserva lo demás y repite las comprobaciones afectadas. No reabras el descubrimiento. |
| Creación nueva | Entrevista de intención (sección 4) y ruta (sección 3). |

## 2. Ruta por **entregable**, no por una palabra suelta
| Entregable pedido | Camino en nuestra skill |
|---|---|
| Subtítulos sobre metraje existente, sin tocar el metraje | `captions-subtitles.md` (Shotcut/ffmpeg) o `hf_captions.py` si la pieza es de HyperFrames |
| Tarjetas/gráficos sobre un talking head sin tocar el metraje | `motion-doctrine.md` §5 (HyperFrames o Shotcut) |
| Video guiado por una pista de música (cortes al compás) | Solo con detección de compás real (`audio-mix.md`, "Sincronía con música"); la música manda el ritmo |
| Unidad corta (< ~10 s), sin narración, el movimiento es el mensaje (título animado, cifra, gráfico, logo) | HyperFrames, con `motion-doctrine.md` |
| Explicar un tema con visuales inventados, sin sitio ni producto que capturar | Explainer: `story-design.md` |
| Cualquier otro (varias escenas, loops, remix de metraje, tarjetas de título) | Pieza general: HyperFrames si es animación compuesta; Shotcut/ffmpeg si el cliente debe editar el proyecto |

Ambigüedades frecuentes: un título animado corto sin narración es motion graphic; un título estático, una secuencia narrada o un montaje largo es pieza general. Retemporizar, reordenar, recolorear o reencuadrar metraje es **edición a medida**. Una música sirve de ruta solo si su compás impulsa la pieza; usada de fondo no cambia la ruta. Los flujos narrativos especializados rinden hasta ~3 min y mejor entre 30 y 90 s.

## 3. Elegir una vez y no volver
La ruta se decide **una vez** en la entrevista y queda escrita en `BRIEF.md`; ninguna fase posterior reabre la pregunta "¿qué se había pedido?": se responde leyendo el brief.

## 4. El encargo (brief) y cómo se pregunta
Plantilla: `assets/brief-template.md`.

**Campos** (pregunta solo los que cambian el resultado; lo inferido se declara, no se pregunta):
| Campo | Regla |
|---|---|
| `destino` | Se infiere de la petición; solo se pregunta si cambia formato o composición. |
| `aspecto` | Se deriva del destino y se dice: feed social 1080×1080; TikTok/Reels/Shorts 1080×1920; YouTube/web/escritorio 1920×1080 (en las pruebas de banco-pruebas-video se usó 1080×1170 para respetar las ilustraciones). |
| `duración` | La recomienda la skill con su razón, según el material. |
| `idioma` | El del usuario; se declara. |
| `público` | Se infiere si está claro; si otra respuesta cambiaría la historia, se pregunta. |
| `mensaje` | **Una** frase. Se deriva y se repite ("Este video le dice a [público] que [mensaje]"). No se hace storyboard hasta que esté claro. |
| `ángulo` | Forma de la historia propia de la ruta; se recomienda uno con razón. |
| `narración` | sí / mínima / no. |

**Forma de ejecución** (dos preguntas **independientes**; nunca se fusionan en un solo menú):
- `flujo`: **automático** (la skill ejecuta de punta a punta) o **compañero** (se construye en conversación, con todo el arsenal sobre la mesa).
- `storyboard`: **sí** (plan en chat + bocetos + construcción, cada pase revisado) o **no** (un video terminado a partir del brief confirmado).
- Modo derivado: compañero → *colaborativo*; automático + storyboard sí → *colaborativo*; automático + storyboard no → *autónomo*. El usuario nunca elige la etiqueta del modo.
- Señales que fijan `automático + sin storyboard`: "hazlo tú", "sorpréndeme", "no preguntes", "solo constrúyelo". Un "listo" o "va" en un punto de control acepta **solo ese punto**; no cambia el modo. Pedir un storyboard fija `storyboard: sí`.

**Puertas**
| Puerta | Colaborativo | Autónomo |
|---|---|---|
| Preferencias (preset, voz, estilo de subtítulos) | Preguntar cuando la ruta lo marque como necesario | Decidir y decirlo con una razón de una línea |
| Puntos de control (plan, bocetos, revisión previa a exportar) | Preguntar y esperar | Publicar el mismo resumen y seguir |
| Calidad (`check`, selftest, comprobaciones de la ruta) | Ejecutar; parar en errores | Ejecutar; parar en errores |
| Ambigüedad de ruta | Resolver explícitamente | Igual |
| Credencial no disponible | Mostrar el estado y esperar | Mostrar el estado y seguir por un proveedor local; si no existe, **informar el bloqueo, no omitir la capacidad en silencio** |
**Exportar el video final sigue requiriendo la petición del usuario en ambos modos** (regla de la skill). Autónomo no es silencioso: cada decisión sustituye a una pregunta con su razón, y la entrega incluye el archivo, la duración real y una hoja de contacto.

**Protocolo de preguntas**
1. Solo campos sin responder que cambien el resultado. 2. **Una pregunta por mensaje**, esperando la respuesta. 3. La opción recomendada va primero, con su razón; las listas sirven en campos factuales (destino, duración, idioma); un campo **creativo** (mensaje, ángulo, tono) se pregunta de forma abierta, anclada a lo ya dicho, porque una lista dirige la respuesta. 4. Inferir no es responder. 5. Anunciar las preguntas diferidas antes de empezar. 6. Antes del resumen, **una comprobación de integración**: buscar la consecuencia que las respuestas juntas crean y ninguna mostraba (p. ej. vertical de 90 s con un concepto cargado de gráficos = gráficos ilegibles en un teléfono) y proponer el ajuste. 7. El resumen separa **lo dicho** de **lo inferido o por defecto**, con su razón en ambos. 8. **Corregir no es confirmar**: tras un cambio se presenta de nuevo el resumen.
Memoria: solo se recuerdan valores **confirmados** por el usuario (`video-handoff.md` del proyecto, la nota del proyecto si el usuario usa Obsidian, o el HANDOFF de la skill); un valor recordado es una **recomendación** que nombra su origen, nunca una orden.

## 5. Ronda de propuestas (solo si el encargo está sin formar)
Un encargo está **sin formar** si da un tema pero ninguna toma sobre él ("un video sobre el lanzamiento"). Antes de cualquier concepto, pregunta qué imagina ya el usuario; una idea previa entra a la ronda como una propuesta más y no la desplaza ninguna generada.
- **Puerta interna (siempre, nunca se muestra):** responde con precisión cuatro preguntas — ¿cómo es el mundo visual del tema?, ¿cómo se ve la emoción buscada como un cuadro? (el anhelo es espacio vacío que el espectador quiere llenar; la urgencia es compresión; el asombro es un elemento demasiado grande para el cuadro), ¿qué exige la superficie donde se verá?, ¿cómo se ven todos los demás videos del tema? (eso es el anti-patrón).
- **Cinco conceptos, uno por camino:** el mundo del tema · la emoción · el público (cumplir o romper su expectativa) · el anti-patrón invertido · un formato inusual (una carta, una cuenta regresiva, una receta, una portada, un mapa). Estima la probabilidad de que un modelo lo generaría por defecto: **al menos dos deben quedar por debajo de 0.10**; si los cinco superan 0.10, todos son la mediana y se empieza de nuevo. Comprueba siluetas: dos conceptos con la misma silueta son uno.
- **Presentación:** cada propuesta en tres líneas (concepto en una frase, su mundo visual, su gancho de apertura); las **cinco antes** de recomendar una (recomendar primero ancla todo lo demás); mezclar es una respuesta válida; **una sola ronda**. Las probabilidades nunca llegan al usuario.
- **Autónomo:** la puerta se corre igual, internamente, y el aviso nombra la dirección elegida y la típica que se dejó atrás. Es donde más peligra la mediana: nadie está para decir "esto se parece a todos".
- **"No sé nada de video":** un mapa de 2–3 superficies de decisión donde su opinión sí cambia el resultado (dónde se verá, cuánto dura, cómo debe sentirse), con 2–4 opciones en lenguaje llano y una por defecto marcada.

## 6. Ciclo de producción (dependencias, no pasos numerados)
El orden entre etapas independientes es libre (el audio se genera mientras se construyen las escenas); dentro de una cadena de dependencia no.
| Etapa | Necesita | Produce |
|---|---|---|
| Recursos | el plan aprobado | bloques/recursos instalados **una vez, antes de cualquier trabajo en paralelo**; recursos del usuario preparados; logos e imágenes resueltos |
| Audio | texto de narración; el estado de ánimo de la música | voz + **tiempos por palabra** + música + efectos; **si hay música bajo una voz, se hace el carve** (`audio-mix.md`) antes de verificar: un duck solo no es una mezcla terminada |
| Escenas | especificación de diseño + el plan (+ el boceto confirmado) | cada escena como archivo propio, marcada `animated` en el storyboard al aterrizar |
| Sincronía de duración | tiempos por palabra + escenas | duraciones ajustadas al largo **real** de la voz (lo real gana; las escenas mudas conservan su estimación) |
| Ensamblaje | escenas | la composición principal, con las escenas como sub-composiciones |
| Transiciones | el ensamblaje | las costuras (`motion-doctrine.md`) |
| Subtítulos | tiempos por palabra | la pista de subtítulos (`hf_captions.py`) |
| Verificar | todo lo anterior | `check` sin hallazgos + hoja de contacto en los puntos medios de cada escena + `selftest.py` si se tocaron scripts |
| Entregar | verificación aprobada | **vista final** → con aprobación, exportar → ofrecer congelar la receta |

**Economía de ejecución (medida por HyperFrames):**
- Las generaciones externas (voz, imágenes, música) son trabajo independiente: lanza **a la vez** las que ya tienen su prompt y solapa la espera con otro trabajo. Tres imágenes una tras otra cuestan ~3× el tiempo de lanzarlas juntas.
- **Adjuntar una imagen a mitad de sesión reprecia todo el contexto** (invalida la caché del prompt). Agrupa las revisiones visuales: **una hoja de contacto vale más que N fotogramas sueltos**, y se hacen en las fronteras de fase, no a mitad de construcción. Esto es coherente con `video-comprehension.md`: primero texto, después una hoja por tramo, al final sondas puntuales.

## 7. Ciclo de revisión (cuando `storyboard: sí`)
1. **El plan, en el chat.** Escribe las decisiones y la lista de escenas en `STORYBOARD.md` y preséntalo como una **propuesta**: abre repitiendo **"Este video le dice a [público] que [mensaje]"**, y una tabla con una fila por escena: escena · beat (tipo, duración) · en pantalla · por qué (su función en la historia, rastreable hasta el mensaje; **una escena cuyo "por qué" no se rastrea al mensaje se corta, no se decora**). Pregunta dos cosas: (a) ¿se aprueba o qué cambia? y (b) ¿bocetos primero (recomendado) o construir de una vez? Una revisión por respuesta: cambiar una escena aquí cuesta 30 segundos; después de construir, minutos.
2. **Bocetos.** Cada escena como un **cuadro estático, no uno sin estilo**: su diseño en el momento clave, con tipografía y color reales y el texto real colocado donde vivirá, usando bloques simples solo para lo aún no producido. **Sin movimiento** todavía. Se montan en una imagen-tablero (`boards/storyboard.html`), se marca cada escena `built` y se pregunta una sola cosa: ¿se ve bien el tablero o qué escenas cambian? Ante comentarios, se rehacen **solo las escenas nombradas**. Un tablero confirmado también es un buen punto de parada si lo pedido era un storyboard.
3. **Construir sobre lo confirmado.** La composición del boceto ya está aprobada: construir es **vestirla** (diseño completo, recursos, movimiento), nunca redibujarla. Marca cada escena `animated` al aterrizar.
4. **La vista final.** Con las comprobaciones en verde, abre la vista previa **antes** de exportar, en ambos modos: es la única forma de que alguien que solo pidió un video sepa que puede verlo antes. Pregunta una sola cosa: ¿exportar ahora o qué cambia? Exportar solo tras la aprobación.
5. **Receta.** Tras aprobar, ofrece **una vez** congelar la corrida (especificación de diseño, esqueleto del storyboard con la estructura y sin el contenido, esqueleto del brief y los valores confirmados) como una receta con nombre ("la próxima vez di *haz otro <nombre>*"). Aquí: guardarla como nota en Obsidian (`maestro/07 Decisiones` o la nota del proyecto). En autónomo no se pregunta; se menciona en la nota de entrega.

## 8. `STORYBOARD.md`
Plantilla: `assets/storyboard-template.md`. Frontmatter: `formato`, `duración` (expectativa, no un tope), `mensaje`, `arco`, `público`, `modo`. Una sección `## Escena N — Título` por escena con `estado` (`outline` → `built` → `animated`), `src`, `duración`, `transición_de_entrada`, `escena` (una línea de pie de hoja de contacto), `voz` (guía de narración) y el texto libre debajo. `built` es el peldaño medio: el HTML existe y **el diseño está confirmado**, falta el movimiento. Si el plan cambia la duración real, se actualiza el valor.

## 9. Roles: director → constructor → finalizador
Tres roles de una misma corrida; pueden ser **una sola sesión** o subagentes.
- **Director** — convierte el encargo en un **plan tipado** (`shot-plan.json`: categoría, `duración`, `fps`, `lienzo`, `estilo`, `paleta`, `tipografía`, `beats`, necesidades de recursos, `bloque` del catálogo + `personalización`, y el contenido propio de la categoría). No escribe código. Si es ambiguo entre dos categorías, hace **una** pregunta. **Reuso primero:** antes de planear a mano cualquier efecto con nombre ("scanlines", "glitch", "grano", "destello", "confeti") **busca en el catálogo** (`npx hyperframes catalog --query "<el efecto en llano>" --json`, no instala nada ni pide cuenta; una búsqueda de "karaoke word by word captions" devolvió 43 resultados) y construye a mano solo lo que la búsqueda no cubra. Búsquedas de recursos: **dos polos** — atómicas (1–3 palabras) o específicas (5–15); nunca a medias; una consulta específica fallida se descarta, no se ensancha.
- **Constructor** — convierte el plan en una composición renderizable. Contrato en `engine-hyperframes.md`. **Primero el estado final en CSS** (flex + relleno, nunca desplazamientos absolutos en contenedores de contenido; la raíz con tamaño) y después la animación. No exporta.
- **Finalizador** — control de calidad por fotogramas y **una sola pasada de reparación** en el sitio: revisa desbordes, contenido fuera del lienzo, textos que chocan, cuadros vacíos, contenido equivocado y movimiento ilegible; **nunca cambia un `data-duration` fijo** (el tiempo se decide aguas arriba); repite `check` y los fotogramas afectados. **Escala solo si la escena está fundamentalmente mal** (todo el contenido fuera de lugar): vuelve a diseñar y construir, no la fuerza con retoques. Los arreglos pequeños nunca escalan.

**Cuándo despachar subagentes (medido por HyperFrames):** una película de hasta ~6 escenas cortas se construye **más rápido en línea** (5 escenas ≈ 9 min en línea frente a ≈ 21 min empaquetadas). Despacha solo si el plan supera eso o hay escenas pesadas, y entonces: **2–3 escenas por trabajador y todos en una sola ola** (una segunda ola casi duplica la ventana). Reglas del despacho: la solicitud al subagente lleva el **archivo de rol completo** más el contexto de despacho copiado **literal**; el hijo no ve tu conversación ni tu memoria, solo el prompt y los archivos; la espera termina cuando **existe el artefacto esperado en disco**, no cuando llega una notificación; si falta, **se vuelve a despachar una vez** con el mismo prompt más el fallo de la puerta; un tope de concurrencia reduce el paralelismo, **no el trabajo** (olas del tamaño del tope; nunca se descartan ni se funden escenas); con tope 3 y 9 escenas, 3 olas de 3. Sin canal de delegación, se hace en serie en esta sesión trabajando solo desde el paquete.
**En esta skill:** **no se lanzan subagentes salvo que el usuario lo pida o haya un permiso permanente** (regla general del entorno). El orquestador no delega la aprobación ni la exportación.

## 10. Pendientes que debía validar el video desde cero: resultados (2026-10-16)
Pieza de prueba: Reel vertical de 29.7 s para caso-reel-01 (8 fotos + 1 video + una música de 122 BPM, **sin voz**), en la carpeta del proyecto de caso-reel-01 (`<carpeta-del-proyecto>`). Se renderizaron las dos variantes del punto 2 con `--batch`.
| # | Pendiente | Resultado | Estado |
|---|---|---|---|
| 1 | Carve de música frente a «No sidechain» | **No se pudo decidir**: la pieza no lleva voz (el carve se omite por regla). Hace falta una pieza con voz en off y escuchar tres versiones (EQ estático, carve 0.5, carve 0.8). | **abierto** |
| 2 | Empuje lento de cámara | Medido (movimiento medio por fotograma, escala 0–100): **sin empuje el gancho queda congelado** (0.00–0.03 entre 1 y 3 s sobre una foto fija); con empuje 1.0→1.06 sube a 0.3–0.4. En las tarjetas de foto y el paneo (1.0→1.05/1.08) el empuje cambia la imagen 1–6 niveles frente a no usarlo. Lo medido no dice cuál **se ve mejor**: Guille compara `reel_v2_row0` (con) y `reel_v2_row1` (sin). | **provisional**: en música/marketing, empuje sutil (≤ 8 %) sobre fotos; la decisión estética es de Guille |
| 3 | Movimiento ambiente por género | En una pieza al compás las pausas muertas se arreglan con **señales ancladas a un tiempo** (subrayado que barre en el tiempo 2 de cada grupo, deriva lenta de un elemento gráfico, pulso de escala 1.035 de una fila de fotos), no con respiración perezosa: fotogramas casi inmóviles **189 → 82 de 881**; tramos quietos ≥ 0.5 s **2 → 1** (solo el cierre con logo, 1.8 s). | **adoptado para música/marketing** |
| 4 | Subtítulos `hf_captions.py` y catálogo | Subtítulos: **no aplica** (sin voz). Catálogo: `catalog --query "light sweep shine on logo" --json` devolvió 46 bloques sin instalar ni pedir cuenta (`shimmer-sweep`, `light-leak`, `logo-outro`…); **no se instaló ninguno** (la línea gráfica de la marca prohíbe brillos/neón). | subtítulos **abierto**; búsqueda **verificada** |
| 5 | Rebote | No se usó: solo curvas `power3/power4/expo/sine` y un pulso de escala 1.035–1.08 sobre el tiempo. Sin evidencia contra la regla. | se mantiene |
**Además** (no estaba en la lista): `--batch` con variables (`push` 1/0) **funciona**; y la **rejilla de compás hay que ajustarla** (`scripts/beat_grid.py`, `audio-mix.md`): con la autocorrelación gruesa los cortes llegaban hasta 0.2 s antes que los golpes.
