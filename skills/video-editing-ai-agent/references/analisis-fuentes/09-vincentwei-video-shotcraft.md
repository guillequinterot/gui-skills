# Análisis: Vincentwei1021/video-shotcraft

Método: SKILL.md, README.md, references/*.md, helpers y demos leídos vía raw.githubusercontent.com con WebFetch. WebFetch devuelve resúmenes de un modelo pequeño, no el texto literal. Los números vienen de esos resúmenes y no están verificados carácter por carácter. Están marcados [~] los que conviene reconfirmar en el raw antes de codificarlos.

## 1. Qué hace, estado, licencia

- Es una skill para Claude Code y Codex que genera videos de producto "cinematográficos" con **Remotion** (React/TypeScript), no con un editor de timeline. No usa Shotcut, MLT ni CapCut como motor. ffmpeg solo se usa para verificar audio y extraer frames.
- Contenido: 157 "shot recipe cards" en 10 categorías, unas 209-214 previews de movimiento, la plantilla ejecutable "Ink Press" (36,2 s, 1920x1080, 10 planos), 5 BGM y 149 SFX en 16 categorías.
- Estado: creado el 19-jul-2026, último push el 9-sep-2026, unas 9.159 estrellas, 832 forks, 6 issues abiertos. Es un repo joven y muy activo, con CI (tsc estricto, vitest, smoke render).
- Licencia: Apache-2.0 para el repo. Remotion tiene licencia propia y puede requerir pago en empresas. Los audios tienen `ATTRIBUTION.md` de 22 KB.
- Los archivos de texto están escritos en chino, con README en EN/CN/JA. Las reglas y las fichas contienen mucho chino.

## 2. Estructura y organización de la skill

Raíz:
- `SKILL.md` (~20 KB): frontmatter con `name` y `description`. Los disparadores son "convertir proyecto web en video de producto", "usa video-shotcraft", nombre de la plantilla Ink Press, o pedir un plano concreto por nombre de ficha.
- `.claude-plugin/plugin.json`, `agents/openai.yaml`: empaquetado para Claude Code y Codex.
- `references/`: `pipeline.md`, `guided-free-creation.md`, `music-beat-sync.md`, `sound-design.md`, `aesthetic-rules.md`, `final-review.md`, `workbench.md`, `jianying-export.md`.
  - `references/shots/<categoría>/*.md`: fichas por plano. Categorías: camera, data, effects, interaction, opening, outro, rhythm, transition, typography, ui-entrance.
  - `references/sequences/`: esqueletos de video completo, con curva de energía.
- `assets/lib/`: componentes TSX para copiar y modificar (PageCam, Caption, FlashCut, ClipCard, DigitRoll, FlatPanel, VerticalTicker) y `helpers/` (motion, camera, shake, rand). Los helpers tienen tests.
- `assets/audio/`: bgm, sfx por categoría, `ATTRIBUTION.md` y un registro de auditoría.
- `assets/scripts/capture-template.mjs`: captura de páginas con navegador headless a 2x, más `layout.json` con las coordenadas.
- `demos/`: TSX de referencia con los valores ya afinados.
- `template/`, `workbench/`, `jianying-export/`, `gallery/`.

Patrones de diseño de la skill:
- **Carga progresiva** con una tabla "cuándo leer qué" al final de SKILL.md.
- Tres modos excluyentes: plantilla directa, creativo autónomo y creación colaborativa.
- **Ficha + demo**: el frontmatter de la ficha describe la semántica, y el TSX del demo guarda los valores realmente afinados. El SKILL.md prohíbe escribir un plano solo con el nombre de la ficha, porque se pierde el ajuste y los "命门" (parámetros críticos).
- `gallery/api/library.json` sirve de índice validable de nombres y `style-key`.

## 3. TÉCNICAS DE ANIMACIÓN Y MOVIMIENTO (núcleo)

### 3.1 Easing y curvas
- Cámara por defecto en `helpers/camera.tsx`: `Easing.bezier(0.4, 0, 0.2, 1)`. En `PageCam.tsx` el valor es `bezier(0.33, 0, 0.15, 1)`. Ambos son ease-in-out suaves con cola larga.
- Impacto y crash zoom (`demos/camera/crash-zoom-punch/CrashZoomReal.tsx`): `bezier(0.55, 0, 0.7, 1)`, es decir, arranque lento y llegada brusca. El desplazamiento del centro usa `Easing.in(quad)`.
- Push-in lento (`demos/camera/tension-camera-moves/SlowPushIn.tsx`): `Easing.in(quad)` sobre escala y viñeta. Se nota poco al principio y mucho al final.
- Portal en profundidad (`shot-transitions.md`): `bezier(0.7, 0, 0.3, 1)`.
- Batch de elementos: entrada acelerada, nunca velocidad constante (R2). Esto es una regla de estilo, sin bezier concreta.
- Rebote y asentamiento (`helpers/motion.ts`): `dampedSettle = exp(-damping*t) * sin(2π*freq*t)` para t>0, con freq≈0,1 ciclos/frame y damping≈0,15/frame. Es una forma cerrada sin estado.
- `velocityAt` usa diferencia central: vx = (x(f+dt) − x(f−dt)) / (2dt), con dt=0,5 frames. Sirve para gobernar stretch o blur según la velocidad. `lagged` devuelve `stateAt(frame − delay)` para follow-through. Todo es función pura del frame.

### 3.2 Zooms, Ken Burns y cámara
- Zoom con impacto (crash zoom): 0-40 f panorámica, 40-46 f empuje de escala 1x a 2,6x, 46-51 f recuperación a 2,45x, 51-120 f hold. Motion blur en 38-48 f con shutter 200° y 20 muestras. Es un patrón útil para un ffmpeg `zoompan` o keyframes en MLT.
- Push-in lento: escala 1,0 a 1,14 en 120 f (4 s a 30 fps), más una viñeta radial `ellipse 62% 55% ... 0→0.95` con opacidad 0 a 0,5 con el mismo easing.
- Cámara 2.5D (`PageCam.tsx`): keyframes `{frame, cx, cy, zoom, rotX/Y/Z}` interpolados entre pares con el bezier por defecto.
  - Modo plano: `translate(960 − cx·zoom, 540 − cy·zoom) scale(zoom)`.
  - Modo 3D: usa CSS `zoom` (no `scale`) para mantener nitidez del texto, con perspectiva 1400 px.
  - DOF: degradado de blur del 45% al 100% de altura.
- Rig 3D (`camera.tsx`): keyframes `{frame, pos[3], look[3], fov?}` con fov por defecto 36 y lerp lineal de pos/look con `t` eased.
- Handheld (`helpers/shake.ts`), literal: `amp*(sin(f*0.31) + 0.6*sin(f*0.83+1.7))` en X y `amp*(sin(f*0.47+0.9) + 0.5*sin(f*1.13+3.1))` en Y, con amp=0,012 por defecto. Usa frecuencias inconmensurables, es determinista y en la Rig atenúa el look un 60%. Regla Q3: sin shake en UI de producto y máximo 0,02 en escenas oscuras tipo documental.

### 3.3 Transiciones (`references/shots/transition/shot-transitions.md`)
- A, flash-cut: destello blanco ±5 f alrededor del corte. `FlashCut.tsx` usa 10 f por defecto con opacidad 0 → 0,85 (pico en el 40%, ~f4) → 0, con un radial-gradient cálido `rgba(255,248,235,.98)`.
- B, túnel oscuro: 8-12 f de push, 4-8 f oscuro y 10-14 f de pull. Escala de fondo 0,6→1 con blur. La dirección se mantiene: si sale por la derecha, entra por la derecha.
- C, traspaso de foco: 10-16 f de crossfade con desfase de 2-4 f. El primer plano pasa de blur 0 a 8 px y el fondo de 8 px a 0.
- D, tarjeta negra: fade de 6-10 f por lado, lineal. Máximo 2 por cada 30 s.
- E1, whip-pan: 20 f de hold, 8 f de latigazo, aterrizaje directo. Velocidad pico ≥300 px/frame. Motion blur shutter 200° y 8 muestras solo sobre el latigazo.
- E2, whip con freno: 70% de la distancia en el 30% del tiempo, más una cola ease-out de 48 f. Tope de 60 f.
- F, portal/wipe: 45 f de escala y fade, con la opacidad del elemento como `1 − t·2.2`. En profundidad son 40 f de expansión más 8 f de asentamiento, con solo 2 capas de parallax (0,08 y 0,3).
- Reglas: un solo tipo de transición por unión (sin apilar), presupuestar los frames de las tomas vecinas, y ≥30 f de hold tras un portal.
- Otras fichas de transición (nombres verificados, sin leer el contenido): card-flip-reveal, circle-match-iris, page-turn-transitions, wipe-transitions, white-flash-logo-simplify-cut, transition-hidden-cut, cube-navigation.

### 3.4 Ritmo y cortes
- Acelerando (`rhythm/beat-cut-moves.md`, estilo A): seis vistas con intervalos 16→12→8→6→4 f, cortes duros a pantalla completa. Cada corte lleva 1 frame de brillo 1,05 y 6% de blanco. El final escala 1→1,06 en 20 f ease-out y luego mantiene 35 f.
- Estilo B "paparazzi": tres destellos blancos con intervalos 22→18 f. La capa blanca baja de 0,95 a 0 en 4 f. Hay shake de ±2 px, retroceso de escala 1,03→1 en 6 f y asentamiento de −16 px. El recorte progresa 1,0x → 2,3x → 4,0x y termina con un hold ≥60 f.
- Speed ramp (`rhythm/speed-ramp-freeze.md`): remapeo `src = interpolate(frame,[0,40,85,135],[0,88,97,207])`. Los tramos rápidos tienen pendiente ≥2, el lento ≈0,2 (contraste ≥10x) y el freeze pendiente 0 sin easing. Los tramos rápidos llevan blur y el lento va nítido. Máximo 2 usos por cada 30 s. Se traduce directamente a `setpts` en ffmpeg o a `timeremap` en MLT.
- Reglas de respiración (SKILL.md y `aesthetic-rules.md`): una técnica de movimiento por plano, acción principal de apertura ≥3 s, hold de marca ≥1 s, hold de 0,5 s tras animaciones por lotes, y ≤3 impactos de pantalla completa por video, separados ≥16 beats.
- Sincronía con la música (`music-beat-sync.md`): `librosa.beat.beat_track(tightness=400, units="time")` y ajuste por mínimos cuadrados de `t_i = t0 + i·T` (BPM = 60/T). Valida la rejilla con un residuo ≤±15 ms y probando 0,5x/1x/2x.
  - Línea de tiempo: `beatF(n) = round((BEAT0 + OFFSET_AUDIO + n·BEAT_INT)·FPS)`. Solo se pasa a frames al final. Los acentos sueltos van sobre transitorios reales.
  - Verificación tras renderizar: extraer el audio con `ffmpeg -i out.mp4 -vn -acodec pcm_s16le` y comparar. Es aceptable un error ≤3 frames e ideal ≤1,5.

### 3.5 Texto animado y subtítulos
- `Caption.tsx`: fade-in de 8 f con `translateY` de 8 px a 0, fade-out de 8 f, interpolación lineal con clamp. El tamaño es de 22 px con letter-spacing de 0,14 em. El propio código reconoce que 22 px incumple la regla Q11.
- Tamaños mínimos (Q11), medidos en píxeles reales de la salida: subtítulo narrativo ≥56 px (≥5,2% de la altura, recomendado 60 px), texto secundario ≥32 px (≥3%).
- Rasterización 3D del texto (Q2): texturas a 2-4x y CSS `zoom` en lugar de `transform: scale`.
- `typography/type-rhythm-sync.md`:
  - Pulso de peso: envolvente `env = (1 − t/10)^0.8` con decay de 10 f, un beat cada 20 f, toggle de font-weight 400↔900 mientras env>0,15, `-webkit-text-stroke: 10px·env` y escala X `1 + 0,08·env` en los acentos.
  - Relleno karaoke: capa base gris y capa activa oscura con `clipPath: inset(0 X% 0 0)`, donde X = (1−p)·100. Pausa de 4-10 f entre palabras y subrayado de 8 px (4 px es insuficiente a 1080p). Hold final ≥20 f.
- `typography/type-entrance-moves.md`:
  - Scramble-decode: 0-20 f con caracteres aleatorios cambiando cada 2 f. El carácter i se fija en `20 + i·6` con un flash invertido de 2 f. Charset A-F 0-9 #$%&, con hash determinista `sin(i*101 + floor(f/2)*7 + 13)`.
  - Letter-drop con física: inicio del carácter i en `10 + i·5`, caída parabólica `y = −DROP + DROP·(t/24)²`, primer rebote con 30% de decaimiento y segundo con 9%, y rotación de ±6°. Reset final de ~6 f. Máximo 2 tipos de entrada de título por pieza.
- Otras fichas de tipografía (solo nombres verificados): marker-underline-title, split-flap-title, gradient-word-sweep, flying-words, glitch-cycle, typewriter-moves, word-relay-*.

### 3.6 Determinismo y audio de apoyo
- Prohibido `Date.now()` y `Math.random()`. El pseudoazar es mulberry32 con semilla por índice.
- Audio (`sound-design.md`): BGM a volumen 0,34 y SFX en 0,2-0,6. Escalera de volumen decreciente, por ejemplo 0,40→0,25 en seis golpes. Alternar dos muestras al repetir.
- Compensación de latencia: AAC 48 kHz añade ~1,28 f a 30 fps (priming de ~2048 muestras). Fórmula `from = frame_objetivo − latencia_pico_archivo − offset_salida`, con la latencia por archivo medida con ffmpeg y correlación cruzada.
- Normalización `loudnorm=I=-16:TP=-1.5` para material por debajo de −12 dB de pico. Las muestras largas necesitan duración explícita.
- Los SFX se anclan con expresiones relativas al frame de cada plano (`SHOTS.x.from + offset`), de modo que siguen a los cambios de montaje.

## 4. Flujo de trabajo, handoff, estado y logs

- Handshake de modo: si el usuario no define el modo, hace una comprobación de producto de solo lectura y recomienda un modo. Luego pide confirmación explícita ("Con base en la revisión, recomiendo el modo X. ¿Continuamos?"). Hay excepciones: si el usuario nombra la plantilla Ink Press o fichas concretas, se salta la pregunta.
- Pipeline de 8 fases (`pipeline.md`), cada una con su entregable:
  0. brief de producto y tabla requisitos→ejecución.
  1. styleframe HTML/CSS y tokens.
  2. mapeo función→plano.
  3. storyboard y timeline por frames.
  4. captura de assets (solo después de aprobar el storyboard).
  5. implementación plano a plano, con un commit y un `remotion still` por plano, archivados en `out/qa/`.
  6. sonido, solo con la imagen ya bloqueada.
  7. revisión independiente y entrega.
- Orden invariante: brief → decisiones → dirección de texto → styleframe → mapeo → storyboard, y nunca implementar un plano antes de fijar la dirección.
- Revisión final independiente (`final-review.md`): la hace un subagente con contexto limpio (quien hace no se autoaprueba). Checklists P/F/V/S/B/D/A y un informe con evidencia por número de frame, por ejemplo `F2 ✗ Frame 340: ...`. Termina con correcciones obligatorias, mejoras opcionales y puntos no verificables.
- Entrega doble: versión con BGM y otra sin BGM, generadas desde la misma línea de tiempo con `--props='{"bgm":false}'`.
- Workbench (`workbench.md`): editor en el navegador (puerto 5198) alimentado por un manifest `src/workbench.ts` con `shots/transitions/captions/overlays/sfx/bgm`. Cada entrada lleva `{id,label,from,duration,component,props,schema}` con un `schema` de campos editables. La tabla de tiempos se define una sola vez y se importa. Los parámetros de ritmo se dejan como constantes para que el usuario no los rompa. `npm run parity` compara píxeles y exige <0,1% de diferencia.
- Handoffs post-entrega, cada uno una sola vez: abrir workbench, crédito al autor (voluntario), envío a showcase, y exportación a CapCut/Jianying (`jianying-export.md`). La exportación:
  - Renderiza una "plate" sin subtítulos ni SFX con `plate=true`.
  - Extrae de las constantes tres tablas (planos, subtítulos, SFX) y monta pistas con `pyJianYingDraft`: un segmento de video por plano, BGM y SFX separados, y dos pistas de texto.
  - Es editable en CapCut la estructura y el texto, pero los movimientos internos de cada plano quedan horneados.
  - Estado de plataformas: Mac verificado con CapCut 11.2, Windows sin verificar.
  - La regla de microsegundos exige redondear cada borde por separado antes de restar.
  - CapCut cifra el borrador de forma irreversible, y hay que cerrar CapCut antes de instalarlo.
- Logs y estado: no hay un log de actualizaciones ni un archivo de estado persistente tipo handshake. El "estado" es el conjunto de entregables por fase, los commits por plano y los still QA. Falta un registro de cambios estructurado, y eso hay que añadirlo en la skill propia.

## 5. Qué reutilizar, descartar y riesgos

Reutilizar (conocimiento, no código):
- Tabla de parámetros de movimiento: bezier, escalas, duraciones en frames (crash zoom, push-in, whip, flash, speed ramp, acelerando 16→12→8→6→4).
- Reglas de respiración: hold de marca ≥1 s, apertura ≥3 s, una técnica por plano, ≤3 impactos de pantalla completa, una transición por unión.
- Tamaños mínimos de texto (56 px y 32 px a 1080p) y verificación en píxeles renderizados.
- Fórmulas de audio: `beatF(n)`, ajuste de rejilla por mínimos cuadrados, latencia de codec, `from = objetivo − pico − offset`, `loudnorm=I=-16:TP=-1.5`, y el chequeo de ±3 frames.
- Patrón "ficha + demo afinado", con parámetros críticos marcados como no negociables.
- Modos con handshake, revisión independiente con informe por frame, entrega con y sin BGM, y la exportación por pistas independientes hacia CapCut como concepto.
- Traducciones a nuestro stack:
  - En Shotcut/MLT, los keyframes con curvas equivalentes van en `affine`/`qtblend` con interpolación smooth, y el speed ramp en `timeremap`.
  - En ffmpeg, `zoompan`/`scale+crop` con expresiones de easing y `setpts` para las rampas.

Descartar:
- Remotion/React/three.js como motor: no encaja con Shotcut/MLT ni con ffmpeg y exige Node 22+ y Chromium.
- El 90% de las demos "SaaS UI" (dashboards, chips, cursores colaborativos) y la captura de páginas web.
- Los 149 SFX y las 5 BGM: pesan cientos de MB en el repo y tienen atribuciones mixtas. Lo aprovechable es la taxonomía de 16 categorías.
- El texto de crédito al autor y la publicación en showcase (son promoción del repo, no de nuestro flujo).

Riesgos:
- Seguridad: la instalación recomienda `npx skills add ...` y clonar con symlink a `~/.claude/skills`. Antes de ejecutar cualquier script (`capture-template.mjs` lanza un navegador headless y abre URLs) conviene revisar el código. La captura de páginas puede exponer datos sensibles, aunque la skill exige anonimizar.
- Dependencias: Remotion tiene licencia propia (uso comercial en empresas). `pyJianYingDraft` es una librería de terceros que toca formatos privados de CapCut y puede romperse con cada versión.
- Windows: el exportador a CapCut para Windows no está probado y depende de rutas y de reiniciar CapCut. Los scripts `.mjs`/`.py` y los symlinks de `public/` requieren permisos de symlink en Windows. Las rutas `~/.claude/skills` hay que mapearlas a `%USERPROFILE%\.claude\skills`.
- Fiabilidad de los datos: mucha documentación está en chino y los números provienen de resúmenes de un modelo pequeño. Los [~] anteriores deberían reconfirmarse en el raw antes de fijarlos como constantes de la skill.
- No se leyeron: las fichas de `references/shots` salvo las citadas, `references/sequences/`, `guided-free-creation.md`, ni `template/TEMPLATE.md`.
