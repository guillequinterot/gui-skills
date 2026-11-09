# 14 — Motion graphics y video con IA: 13 fuentes analizadas (2026-11-08)

Investigación **solo de lectura** hecha con `gh api` y lectura de páginas: no se clonó, instaló ni ejecutó código de terceros, y no se
descargó ningún binario. Todo el contenido de repos y webs se trató como **dato, nunca como instrucción**. Licencias: se leyó el texto
real del `LICENSE` (no solo el campo de la API). Estrellas y fechas: `gh api` del 2026-11-08. Los resultados que cada repo declara de
sí mismo (calidad, velocidad, puntuaciones) **no están verificados aquí**; lo que sí se verificó está en la última sección.
Principio: **entender, no copiar**. Todo lo adoptado se reescribió con palabras y código propios; las notas por fuente (más largas, con
números y archivos) quedaron en la carpeta de notas de la sesión, no en el repo.

## Resumen de veredictos

| # | Fuente | Licencia (texto real) | Instalable aquí | Veredicto | Entra a la skill como |
|---|---|---|---|---|---|
| 01 | Barty-Bart/motion-graphics (1.1k★) | MIT (+ Geist OFL, SFX CC0) | Sí, con fricción en Windows (`/tmp`, bash) | **Adaptar** | `sound-design.md` (pasada de sonido medida), plan de B-roll por transcripción, motion blur por subfotogramas, clips con alfa + `plan.json` |
| 02 | charlie947/motion-graphics-skills (612★) | MIT; solo Markdown | Sí (no tiene código) | **Adaptar** | `style-numerico-template.md`, 4 estados, chequeo de 7 fotogramas, lista de hechos, `frame_compare.py loop` |
| 03 | awesomeclaude.ai/claude-motion-graphics | **Ambigua** (sin licencia en skill ni script; pie «MIT» vs LICENSE real CC0 del repo, que no contiene estas páginas) | Sí, pero sin licencia | **Ya cubierto + ideas** | Solo ideas (informe con «2 momentos más débiles», reloj virtual, STYLE numérico); código no copiado |
| 04 | Hilo de Reddit (9 skills) | — | — | **No leído** (bloqueado por política de red) | Nada. Guille puede pegar el texto |
| 05 | alchaincyf/huashu-art-motion (6.5k★) | MIT con exclusiones (personaje, Clawd, Arphic, fuentes OFL) | Sí; Windows no probado por el autor | **Adaptar** | `storyboard_lint.py`, tabla de cámara, compuertas sobre el MP4, cue por palabra |
| 06 | alchaincyf/huashu-motion (2.5k★) | MIT; **GSAP aparte («no charge», no vale para editores competidores)**; firma «Made with…» por defecto; solo macOS | No recomendado | **Adaptar ideas** | Hoja de ritmo, calendario de contraste, trampas de GSAP, revisión «¿dónde se aplana?» |
| 07 | Leonxlnx/earshot (4.3k★) | MIT | Sí (uv + 1.1 GB de modelos opcionales) | **Adaptar** | `sync_audit.py`, `sound-design.md` |
| 08 | NiazMorshed2007/reanimate (1.4k★) | MIT (activos de sitios de terceros excluidos) | **No en Windows** (rutas sin `.exe`, bash, Metal) | **Adaptar** | `frame_compare.py`, `recrear-referencia.md` |
| 09 | vincentsch/explainroo (1.1k★) | MIT (+ misaki Apache-2.0 en un módulo) | Sí en teoría (CI en Windows); ~400 MB de modelos | **Adaptar** | `align_script.py`, sintaxis de guion, caché por hash |
| 10 | rossark0/rossark-motion-skill (755★) | MIT | Plantillas solo RN/SwiftUI/macOS | **Adaptar poco** | `flow()`, capa ociosa, follow-through, tablas de duración |
| 11 | win4r/video-director (402★) | MIT | Scripts Python + ffmpeg (sin probar en Windows) | **Adaptar** | Plan como fuente única, validador, compuerta del gancho, crítico «rechaza por defecto», ficha de arreglo |
| 12 | talsiach/take-one (237★) | MIT; **anidoodle Apache-2.0**; nombre/logo excluidos; **enlaces de afiliado** | No (solo macOS) | **Adaptar ideas** | `concept-check`, «qué es verdad hoy», verificación de cortes de voz, auditoría de texto |
| 13 | shreyaskarnik/argo (153★) | MIT (+ shaders de terceros) | **No en Windows** (CI ubuntu); `argo add` sin verificación de integridad; 704 MB | **Adaptar ideas** | `narracion-y-demos.md` (voz primero, manifiesto, zoom como metadato) |

Veredicto «adaptar» = se toma la idea o el número, con atribución, y se reimplementa. Ninguna fuente se **instaló**.

## 01 · Barty-Bart/motion-graphics
- **Qué es:** 6 skills con código real (motor `motion.js`, `render.js`, scripts de ffmpeg y librosa): B-roll de motion graphics sincronizado con las palabras de un video hablado, separación de objetos con SAM 2.1, 3 explainers de producto y una pasada de sonido con biblioteca de 103 SFX CC0.
- **Licencia:** MIT estándar «2026 Bart» más notas (Geist OFL, iconos Lucide ISC). El campo de la API dice `NOASSERTION` por esas notas. Se puede copiar con aviso.
- **Aporta:** contrato de página `seek(t)` pura (ya lo tiene HyperFrames), **motion blur real con 4 subfotogramas a 180° (`tmix` + `select`)** y modo borrador a 30 fps con varios procesos; **plan de B-roll en tabla aprobado antes de programar** con la regla cutaway / panel transparente / nada (no cortar en el gancho ni en líneas emocionales, ≥ 2 s de cara entre cutaways); detección automática de secciones `full / pip / black` y de la caja del hablante; entrega `.mov` ProRes 4444 con alfa + `plan.json` + `TIMING.md`; **pasada de sonido medida**: lista de cues, mapa cue → categoría con offsets, rejilla de bombos < 120 Hz, mezcla medida sobre el MP4; cumplimiento de licencias de audio (preguntar dónde se publica, abrir la licencia vigente de cada fuente, `CREDITS.txt`).
- **Banderas:** `eval()` sobre la salida de ffprobe, `/tmp`, `curl` de URLs del manifest; contradicción interna (los explainers sintetizan música con osciladores y la skill de sonido lo prohíbe). No se copia `sound_pass.py`.
- **No vale la pena:** `object-separation` (SAM 2 en CPU: ~30 min por 10 s), los 3 explainers como plantillas, el motor `motion.js` con su estética.

## 02 · charlie947/motion-graphics-skills
- **Qué es:** 15 skills solo en Markdown (sin motor): marca para movimiento, briefs, efectos, exportación a Reel. Su valor es **proceso y lecciones**.
- **Licencia:** MIT estándar. Pide un enlace al newsletter del autor (petición, no condición). Dos `.zip` de `downloads/` sin abrir.
- **Aporta:** `brand.md` + `MOTION.md` generado solo desde fotogramas, con **«ASK ME» donde no se sabe** y 5 «nunca»; «el archivo fija el aspecto, no la ambición»; animación especificada con **4 estados cronometrados** (inicio, cambio, mantener, retorno) y reloj fijo; **chequeo de 7 fotogramas** con criterios; regla anti-falso-positivo del autoexamen («informa solo lo que observes»); **lista de hechos aprobada** y distinción resultado / objetivo / dato ilustrativo; **medición de bucles**: costura (último vs primer fotograma) y excursión (máxima diferencia contra el fotograma 0); exportación a Reel verificable con `ffprobe` (H.264, `yuv420p`, rango `tv`, BT.709, zona segura).
- **Banderas:** dependen de «Claude Motion» / «Opus 5.5»; `title-sequence-3d` copió texto de `vox-explainer`; cifras de audiencia no verificables. Las skills de producto imitan estéticas de marcas (Apple, Vox): tomar la técnica, no el trade dress.

## 03 · awesomeclaude.ai/claude-motion-graphics (y subpáginas)
- **Qué es:** página de guía con **una** skill de 6 pasos, un script de render con reloj virtual, 17 recetas de estilo con números, 9 consejos para escribir estilos y un constructor de prompts. No cataloga skills de terceros.
- **Licencia:** ambigua. Ni la skill ni el script traen licencia; el pie dice «MIT» pero el `LICENSE` real de `webfuse-com/awesome-claude` es **CC0** y ese repo no contiene estas páginas. → Solo ideas; nada copiado literal.
- **Aporta (ya cubierto en su mayoría):** hoja de contactos obligatoria antes del render, informe final con **los 2 momentos más débiles**, `STYLE.md` numérico, lista «evitar por nombre», reloj virtual (`performance.now`, `Date`, `requestAnimationFrame` y animaciones CSS controlados por quien renderiza), «etiquetar BT.709», motion blur barato (capturar a 240 fps y promediar de 4 en 4).
- **No vale la pena:** estadísticas de costos y «703 prompts» (autodeclaradas, sin fuente); el render script como motor de producción (secuencial, sin audio).
- **Candidatos para otra ronda** (los cita la página; MIT; **no leídos a fondo**): `lemomo-ai/lemo-opuscar` (13.7k★, 66 estilos), `Vincentwei1021/mg-styles-15` (3.3k★).

## 04 · Hilo de Reddit «9 Claude skills for motion design / animation»
**No se pudo leer.** `curl`, `old.reddit.com`, WebFetch, el navegador integrado y la búsqueda fallaron por una política de red; no se intentó eludirla. Por eso la lista de 9 skills no se infirió de ningún lado: se usó la lista de repos que dio Guille (fuentes 05–13). Si Guille pega el texto del hilo (post y comentarios), se puede revisar y añadir aquí.

## 05 · alchaincyf/huashu-art-motion
- **Qué es:** video «pintado en código» (Canvas/SVG/Three) renderizado cuadro a cuadro: 36 estilos artísticos, 9 gramáticas de explainer parametrizables por JSON, película larga, QA y entrega con puertas automáticas. Documentación casi toda en chino.
- **Licencia:** MIT sobre código y documentación. **Excluidos:** la imagen del autor, Clawd (propiedad de Anthropic), datos de trazos Arphic y fuentes con su propia OFL. No se copia nada de esos activos.
- **Aporta:** **tabla de planos con lint mecánico antes de escribir código** (objeto = sustantivo, acción = verbo, texto en pantalla corto, planos de 2–6 s, texto dominante ≤ 30 %, primer y último plano no de texto); **tabla de acciones de cámara con duraciones y cuándo NO usarlas**, y la regla «el mismo movimiento en cada plano es el mismo defecto»; puertas medibles sobre el MP4 (fracción de fotogramas con movimiento rápido, plano vacío, % de fondo azul-violeta) donde `deliver.py` no copia si hay rojo; **cue por palabra, no por segundo**; revisión independiente donde manda la puntuación más baja (la autoevaluación infla ~10 puntos); **«validar los validadores»** (cada comprobación debe fallar a propósito al menos una vez).
- **Cuidado:** los umbrales vienen de **13 videos** del propio autor (gusto personal). Dice textualmente que no es demostrado. Tratar como punto de partida. 17 de sus recetas de estilo están marcadas «sin validar».
- **No vale la pena:** los estilos pictóricos, las películas largas de «mismo escenario, estilos distintos», la voz con Volcengine.

## 06 · alchaincyf/huashu-motion
- **Qué es:** skill + CLI `om` para películas de lanzamiento como código editable, con editor en el navegador. Mismo autor que la 05; HyperFrames fue **eliminado** de ese proyecto el 2026-10-18 y sustituido por motor propio.
- **Licencia:** MIT propia. **GSAP (licencia «no charge» de GreenSock)**: prohibido en herramientas que compitan con Webflow; **firma «Made with huashu-motion» activada por defecto** en los últimos 1.2 s; muestras de instrumentos y modelos de voz se descargan aparte; solo probado en macOS.
- **Aporta:** **hoja de ritmo con números medidos en 21 lanzamientos** (gancho en < 3 s, ráfaga de 5–8 cortes hacia el 37 % de la duración, una parada, densidad en eventos por compás), **calendario de contraste** (cambiar ≥ 2 cosas en cada frontera de sección), caso A/B donde una pieza que pasaba todas las comprobaciones se rechazó por «aburrida» (la energía viene del corte y del movimiento, la calma de la marca se dice en paleta y easings); bucle de comentarios (comentar sobre un fotograma, el agente edita lo mínimo y dice qué lectura tomó); **trampas de GSAP** (tween antes de 0 desplaza toda la línea de tiempo, `fromTo` renderiza ya su estado inicial, contenedor sin altura que colapsa capas, banda sonora fija la duración); método de color por roles y «look de la casa» como anti-patrón; revisión que **siempre responde «¿en qué segmento empieza a distraerse?»**, con tabla de procedencia del texto en pantalla.
- **No vale la pena:** el motor propio, el Studio, la música en notación ABC sintetizada (contradice nuestra regla de audio), la firma por defecto, el empaquetado de talking-head salvo la idea de anclar a palabras reales.

## 07 · Leonxlnx/earshot
- **Qué es:** «oídos» para agentes: audio → evidencia legible (eventos, secciones, loudness, rejilla de beats, **sincronía contra los cortes y cues de la imagen**) y un banco de 252 SFX sintetizados; skill `real-sound` con 10 pasos y puertas de calidad.
- **Licencia:** MIT. Modelos CLAP y AST con sus licencias (Apache-2.0 / BSD-3). No contiene audio ni video.
- **Aporta (sin modelos):** detector de golpes (flujo espectral en log-mel a 5 ms + umbral robusto con mediana/MAD + afinado del ataque en envolvente de 1 ms); **sincronía = offset del golpe respecto del cue, comparado siempre con la probabilidad «por azar»** (ventana −45/+75 ms); detector de cortes por diferencia de fotogramas grises de 96×54; tabla de **offsets por tipo de efecto** (clic −11 ms, pico de whoosh +37 ms…); **«stop-down»** (la música baja 6–12 dB durante 0.3–0.5 s antes de un golpe grande en vez de agacharse bajo cada efecto); gramática imagen → sonido (cursor y scroll = nada; corte duro = nada; revelación = el golpe de la música en su tiempo fuerte); lista de «cheap tells».
- **Honestidad del autor:** el etiquetado de eventos en mezclas densas acierta ~50 % (25 % bajo música); su prueba ciega de «realness» dio 8/15 (azar). Los rangos de su scorecard salen de 7 films.
- **No vale la pena:** CLAP/AST (1.1 GB, 20–40 s por llamada), `forge` y `fit` (Goodhart declarado), `earshot llm` (sube audio a Google), el scorecard de 7 films.

## 08 · NiazMorshed2007/reanimate
- **Qué es:** recrea animaciones web: graba la referencia con reloj virtual, mide movimiento y easing, implementa, vuelve a grabar **igual** y compara cuadro a cuadro, 2–5 rondas.
- **Licencia:** MIT sobre el código. `site/public/examples/` contiene recreaciones de sitios de marcas (shaders, imágenes, fuentes): **no copiar nada de ahí**.
- **Aporta:** la métrica **no es SSIM ni PSNR** sino fracción de píxeles distintos (`pixelmatch`) + **curva de actividad** (cambio entre fotogramas consecutivos) + **ventana de movimiento** (primer/último fotograma activo y pico) → error de tiempo en segundos, independiente de colores y texto; autoalineación de ±15 fotogramas; aviso cuando referencia y clon se capturaron con configuración distinta; suelo de ruido (referencia contra sí misma); ajuste de easing contra ~22 curvas con RMSE; hoja «referencia | clon | diferencia».
- **No vale la pena:** el trazador WebGL, los 18 clones, la parte de implementar en React/Framer. **No funciona en Windows tal cual.** Con video natural conviene SSIM o la curva de actividad, no solo `pixelmatch`.

## 09 · vincentsch/explainroo
- **Qué es:** explainers narrados desde un `script.md` y un `scenes.js`: voz local Kokoro, Whisper local que anota cuándo se dice cada palabra, render en Chrome, subtítulos y capítulos.
- **Licencia:** MIT. Un módulo de fonemas adaptado de misaki es Apache-2.0 (conservar su aviso si se copia). Pide conservar su marca de agua (petición, no condición).
- **Aporta:** **voz por frases → Whisper sobre cada frase → alineación por programación dinámica contra el guion**, con `matchRate` como control; reglas de normalización de cifras; sintaxis de guion `[#marca]`, `[pause s]`, `{mostrado|hablado}`; **caché por hash** de (texto, voz, velocidad, modelos); línea de tiempo con `lead / hold / pace`; ducking −8 dB con ataque 0.2 s y suelta 0.5 s; **`verify` que vuelve a reconocer el habla sobre la mezcla final** y avisa si la música tapa la voz; subtítulos `.srt` desde los tiempos por palabra.
- **Pesos:** ~400 MB de modelos; Kokoro en español solo tiene 3 voces y necesita espeak-ng (**no se escuchó**).
- **No vale la pena:** el motor canvas «dibujado a mano», ElevenLabs/OpenRouter desde su herramienta, `capture` de sitios ajenos.

## 10 · rossark0/rossark-motion-skill
- **Qué es:** método de movimiento para SVG y personajes en React Native y SwiftUI, con 3 herramientas de medición con ffmpeg (`track_edges.py`, `sheet.sh`, `sample_colors.py`). Repo de un mes, sin tests.
- **Licencia:** MIT.
- **Aporta:** `flow()` (interpolación cúbica de Hermite monótona para pasar por poses sin parar), **capa ociosa permanente** (respiración ±1–1.5 %, balanceos con periodos que dividen el bucle), **follow-through por retardo del padre de 60–150 ms** en vez de muelles (determinista), tablas de duración (parpadeo 110/40/190 ms, interfaz 100–500 ms, escalonado 40–80 ms), mínimo ~100 ms para movimientos rápidos, checklist de «vida» de 9 puntos.
- **No vale la pena:** plantillas RN/SwiftUI y el render de macOS 14+.

## 11 · win4r/video-director
- **Qué es:** skill de dirección y verificación (no generador) para videos hechos como código: flujo por fases con compuertas, 13 principios, dos scripts de QA (`check_timeline.py`, `qa_video.py`), 3 evaluaciones.
- **Licencia:** MIT. Python + ffmpeg, sin red; CI solo en Linux.
- **Aporta:** **`timeline.json` como fuente única de verdad** y un validador previo a todo render (huecos entre escenas, beats fuera de rango, **texto de gancho legible antes de 3 s**, términos dichos y mostrados); compuerta del gancho medida en el MP4; definición operativa de «silencio» (≥ 0.4 s, ≥ 15 dB bajo el percentil 90 y bajo −30 dBFS); detectores de «pops» y flashes de un fotograma, congelados, fotograma 0 plano, costura de bucle, sobre fotogramas de 96×54; **crítico de contexto limpio que rechaza por defecto** (barra de 8/10 en cada eje, una sola ronda de arreglos); **ficha de arreglo** (diagnóstico, alcance, qué conservar, atajos prohibidos, prueba de que lo demás queda idéntico); informe de entrega que separa medido de visto/oído; registro `DECISION: … porque …` en modo autónomo.
- **Cuidado:** umbrales (84/48 px, 7:1, −14 LUFS) son defaults del autor; las evaluaciones son de una sola ejecución. No edita metraje real.

## 12 · talsiach/take-one
- **Qué es:** «estudio» de 12 oficios que genera cortos desde canvas. Skill muy larga (46 KB + ~60 referencias).
- **Licencia:** MIT; archivos adaptados de anidoodle **siguen en Apache-2.0** (con su NOTICE); el nombre y el logo «Take One» **no** están licenciados. **Enlaces de afiliado** del autor (Higgsfield, ElevenLabs) incrustados en las instrucciones: ignorados.
- **Aporta:** compuerta del storyboard antes de construir («sin palabras», página vs. imagen, evento vs. estado); **«qué es verdad hoy»** (verificar cada función/cifra del pedido contra el sitio real antes de construir); **verificación de cortes de voz** (cortar de silencio a silencio, transcribir cada línea cortada y compararla con el guion); auditoría de texto medida (pequeño, relámpago, cortado por el borde, sobre una cara, `NaN`/`undefined` visibles); comprobación de determinismo (dibujar adelante en frío y atrás en caliente, nombrar el fotograma que envenena); revisor nuevo con paquete automático (hojas a 1 fps, cuadrícula por beat, hoja a 360 px) y brief fijo.
- **No vale la pena:** 22 estilos, rutas de pago, pitch de precios, rol de copywriter social, manejar cuentas de terceros con el navegador del usuario.

## 13 · shreyaskarnik/argo
- **Qué es:** demos de producto: un script de Playwright + un manifiesto `.scenes.json` → MP4 narrado (voz local Kokoro, Whisper por palabra, cursor humano, zoom, 16 transiciones de shader).
- **Licencia:** MIT. Shaders de gl-transitions (MIT) y de HyperFrames (Apache-2.0) con licencia propia.
- **Aporta (como patrón, no como herramienta):** **orden «voz primero»** (la voz se genera antes de grabar para que el recorrido espere la duración real de cada línea), manifiesto único con validador que cruza escenas y marcas, clips alineados en su marca con separación mínima de 100 ms, **zoom registrado como metadato y aplicado al exportar con `zoompan`** (así los overlays ya grabados no se escalan raro), **cursor humano determinista** (curva con semilla, 300–1100 ms según distancia, pausa de 350 ms antes del clic), caché por hash, captura sin pérdida con relleno por reloj de pared.
- **Riesgos:** `argo add` baja archivos de terceros cuyos `<script>` se ejecutan dentro de la página grabada y cargan CDN **sin integridad**; no probado en Windows (CI solo en Ubuntu); repo de 704 MB; atado a páginas controlables con Playwright. **No se instala.**

## Lo que hay en común (señal de confianza)
Casi todas las fuentes llegaron por separado a lo mismo, lo que sube la confianza: (1) la pieza es una página cuyo aspecto es **función pura del tiempo**; (2) **plan validado antes de renderizar**; (3) **medir lo que el modelo no puede ver ni oír** (fotogramas pequeños en gris para pops/congelados, ebur128 sobre el MP4 entregado, onsets contra cues); (4) **revisor independiente que rechaza por defecto**; (5) **hechos primero**: nada en pantalla que no esté en una lista aprobada; (6) «aburrida» es el rechazo más común y no lo detecta ninguna métrica.

## Qué se verificó y qué NO
- **Verificado aquí (selftest, material sintético):** `storyboard_lint.py` (plan malo → ROJO, sano → VERDE), `frame_compare.py compare` (clon 0.2 s tarde → error de inicio 0.2 s y desfase óptimo +5 fotogramas; clon idéntico → coincide) y `loop`, `sync_audit.py` (4 golpes sintéticos detectados; offset de +30 ms medido con ±12 ms; cue sin golpe cerca no se da por bueno), `align_script.py` (cifra con `{20|veinte}`, mal oído «pruebda», palabra de más «eh», guion ajeno → `matchRate` < 0.5).
- **NO verificado:** ningún script con material real de un cliente (solo sintético); los umbrales de las fuentes con **nuestro** material (todos son «punto de partida»); `sync_audit.py` con música densa (el azar sube y la sincronía deja de significar algo: el script lo avisa); `frame_compare.py` con video natural (cámara, compresión); que las ideas de motion blur, reloj virtual y clips con alfa funcionen dentro de HyperFrames 0.8.162; ninguna herramienta externa se ejecutó; nada de Kokoro/Argo/earshot/reanimate se instaló; el hilo de Reddit no se leyó.
- **Decisiones de Guille (2026-11-09):** «instalar Kokoro» y «hacer todo» lo pendiente → ver la sección siguiente.

## Segunda ronda (2026-11-09): con la aprobación de Guille
| # | Fuente | Licencia (texto real) | Veredicto | Entra como |
|---|---|---|---|---|
| 14 | lemomo-ai/lemo-opuscar (13.7k★) | MIT en `LICENSE`; el README añade CC BY 4.0 para las películas y fotogramas demo y excluye seis pistas de voz (esa capa no está en `LICENSE`); activos de terceros con licencia propia | **Adaptar ideas** | guardias de render roto, `readcheck` de tiempo de lectura, `rescheck` de resolución, audio tras AAC, medidores sobre el MP4, ficha de estilo de 11 secciones |
| 15 | Vincentwei1021/mg-styles-15 (3.3k★) | MIT (Copyright 2026 Vincentwei1021); archivos de terceros con su licencia; sin fuentes en el repo | **Adaptar ideas** | rúbrica de 7 ejes con escala ancla, prompt de ronda 2, punto de sincronía por tipo de sonido |
- **lemo-opuscar:** 66 estilos como «ficha invariante de 11 secciones + demo separado»; ~17 scripts de chequeo por demo y dos puertas humanas, **sin rúbrica con puntuación**. **No se instala**: `setup.sh` actualiza el repo desde `main` en cada uso (ejecuta código remoto), los prompts están afinados para Opus 5.5, hay demos que son fan films de obras reales y reglas políticas sobre cómo dibujar mapas. No se vio ninguna película: la calidad real no está verificada.
- **mg-styles-15:** es un escaparate con banco de prompts, **no una herramienta**: el «harness» solo renderiza; la medición es un jurado de IA cuyas reseñas no están publicadas (las notas 7.57–8.21 no son evidencia). Repo sin actividad desde el 2026-10-05; `render.mjs` asume macOS; faltan muestras de audio (issues sin respuesta).

### Lo que se hizo con la aprobación de Guille
- **Kokoro instalado y verificado** (`references/narracion-y-demos.md` §4): entorno `~/.gui-skills/kokoro` fuera del repo, `kokoro-onnx` 0.6.1 (MIT), modelos de la release oficial (310 + 26 MB, sha256 anotado). `scripts/voz_local.py`. **No se oyó**: `matchRate` 0.94–0.96 de Whisper sobre la propia voz.
- **Biblioteca CC0 de 109 efectos** copiada a `assets/sfx-cc0/` (2.7 MB; integridad OGG comprobada; cada sonido figura como CC0 1.0 en el `manifest.json` del autor; **no se re-verificó cada página de origen**).
- **`scripts/glitch_scan.py`** (flashes, pops, fotograma 0, congelados, bucle) y **cifras en español** en `align_script.py`.
- **HyperFrames:** `render --format mov` da ProRes 4444 con alfa real (verificado); 240 fps + `tmix` funciona (el efecto visual no se verificó); no hay motion blur nativo.
- **earshot no se instaló:** lo útil (onsets, sincronía contra el azar, cortes por diferencia de fotogramas) ya está reimplementado sin modelos en `sync_audit.py`; sus 1.1 GB de CLAP/AST no aportan a una skill de edición y su propio autor admite que el etiquetado de eventos en mezclas densas acierta ~50 %.
- **No se pudo hacer:** calibrar umbrales con material real (no hay una pieza real a mano en esta sesión), resolver los conflictos con `motion-doctrine.md` (hace falta una pieza), leer el hilo de Reddit (hace falta que Guille pegue el texto).
