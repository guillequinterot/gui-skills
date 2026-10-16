# Análisis: github.com/VideoZero/skills

Nota de verificación: WebFetch pasa el contenido por un modelo pequeño. Los archivos se pidieron vía raw.githubusercontent.com, pero lo recibido son resúmenes/paráfrasis; la tabla de timing (animation-basics) y los nombres de easing (TWEENING.md) parecen literales, el resto NO está verificado literalmente. No se leyeron agent-client.ts, agent-plugin.ts, LAYOUT, TRANSFORMS, SETUP, SOUNDS, FILTERS, GRADIENTS, SVG, ICONS, LATEX, PRESENTATION_MODE.

## 1. Qué es
- Repo de skills para **Motion Canvas** (framework TypeScript de motion graphics programáticos en canvas 2D, escenas con generadores `function*`). NO edita video existente: genera animaciones estructuradas (explainers, diagramas, infografías) desde código.
- Herramienta objetivo: Motion Canvas + editor en navegador (Vite). No toca Shotcut/ffmpeg/CapCut/Premiere/AE; usa ffmpeg solo como exportador a MP4.
- Descripción oficial: "skills for agentic video generation for structured visuals based on MotionCanvas".
- Licencia Apache-2.0. ~67 estrellas, creado 2026-03-18, último push 2026-08-11 (activo), 1 issue abierto. Instalación: `npx skills add videozero/skills`.

## 2. Estructura
```
animation-basics/SKILL.md            (2.8 KB: principios + tabla de timing)
motion-canvas/SKILL.md               (9.4 KB: núcleo)
motion-canvas/references/*.md        (18 refs: CAMERA, EFFECTS, FILTERS, FLOW_CONTROL, GRADIENTS, ICONS,
                                      LATEX, LAYOUT, MEDIA, PRESENTATION_MODE, RENDERING, SETUP, SOUNDS,
                                      SPRINGS, SVG, TRANSFORMS, TWEENING, TXT)
motion-canvas-agent/SKILL.md         (7 KB) + assets/agent-client.ts, agent-plugin.ts (~11 KB c/u)
```
- Frontmatter mínimo: `name` + `description` (la description incluye el disparador "Use when building or editing Motion Canvas scenes"). Sin campos extra.
- Patrón: SKILL.md corto + carpeta `references/` con un tema por archivo (progressive disclosure) + assets de código copiables. Muy replicable.
- Tres skills por rol: conocimiento del framework, principios de animación (independiente de herramienta), control por agente.

## 3. Técnicas de animación (lo aplicable)
Lo transferible a cualquier herramienta es sobre todo `animation-basics/SKILL.md`.

**Tabla de timing (animation-basics):**
| Tipo | Easing | Duración |
|---|---|---|
| Entrada | ease-out | 0.3-0.5 s |
| Salida | ease-in | 0.2-0.3 s |
| Cambio en sitio | ease-in-out | 0.3-0.8 s |
| Énfasis | ease-out con overshoot | 0.2-0.3 s |
| Stagger | - | 40-80 ms (palabras), 100-150 ms (elementos) |

Reglas: nunca fade solo (combinar opacidad con movimiento); un ease-in-out rápido permite cambiar icono/SVG en el 50 %; arcos para movimiento con gravedad; ease in/out salvo en impactos (sin ease-in en colisión); texto en pantalla hasta 3x el tiempo de leerlo en voz alta; anticipación antes de la acción; follow-through/overlap con retrasos según peso; exageración mayor cuanto más rápido el movimiento; staging: una sola cosa compite por la atención.

**Easing (references/TWEENING.md):** linear; familias Sine, Quad, Cubic, Quart, Expo, Circ, Back (overshoot), Elastic, Bounce, cada una In/Out/InOut. Utilidades: `map`, `clamp`, `remap`, `clampRemap`, `Color.lerp`, `Vector2.lerp`, `Vector2.arcLerp(start,end,t,radius)`. Tween encadenado `.to().to().back()`.

**Springs (SPRINGS.md):** física de Hooke con `{mass, stiffness, damping}` (ej. 1/100/10). Presets: Plop (entrada con rebote), Smooth (sin rebote), Beat (énfasis rítmico), Bounce, Swing, Jump, Strike. Más masa = más lento; más stiffness = más rápido; menos damping = más rebote.

**Control de flujo (FLOW_CONTROL.md):** `all` (paralelo), `chain` (secuencia), `sequence(0.1, ...)` (stagger), `delay`, `loop`. Sirve como vocabulario para planificar capas y offsets en cualquier timeline.

**Cámara (CAMERA.md):** `zoom()` (no scale), pan por `position.x/y`, `rotation`, `centerOn(nodo|[x,y], t)`, `followCurve(path, t)`, multicámara/PiP con `Camera.Stage`. Equivale conceptualmente a zoom/pan/Ken Burns, pero NO da fórmulas numéricas de Ken Burns (habrá que definirlas nosotros, p.ej. escala 1.0 a 1.1-1.2 con ease-in-out; no es del repo).

**Texto (TXT.md):** tween del `text` (efecto máquina de escribir/morph), texto ligado a señal contador, animar fontSize/fill en sincronía. No hay subtítulos animados palabra a palabra ni karaoke; solo la regla de stagger 40-80 ms por palabra.

**Transiciones:** SKILL.md menciona slideTransition, fadeTransition, zoomInTransition, zoomOutTransition (sin parámetros leídos).

**Otros:** morph de paths, filtros animables (blur, brightness, contrast, saturate, hue...), gradientes, iconos Iconify animados, `waitUntil(evento)` para sincronizar con eventos (útil para audio), `Video.seek/play/playbackRate`. Render: 720p/1080p/4K/cuadrado/vertical 1080x1920, 30 o 60 fps, fondo transparente con `view.fill(null)`.

No hay nada sobre ritmo de cortes de edición, J/L-cuts ni beat-sync (salvo el preset Beat spring).

## 4. Flujo, handoff, estado, logs
- motion-canvas-agent: cliente HTTP (curl) -> plugin de Vite -> WebSocket -> cliente en navegador (Player/Renderer). API en `localhost:9000/__agent/`.
- Endpoints: `/status` (`{connected, frame, duration, fps, paused, sceneName, errors}`), `/seek`, `/play`, `/pause`, `/next-frame`, `/prev-frame`, `/screenshot`, `/screenshot-base64`, `/scene-graph`, `/scenes`, `/threads`, `/settings/size`, `/settings/rendering-fps`, `/render`, `/render/abort`, `/errors`, `/clear-errors`.
- Patrones reutilizables: (a) handshake por `/status` antes de operar; (b) respuestas `{ok, ...}`; (c) bucle editar -> seek a frame -> screenshot -> revisar -> corregir; (d) cola de errores consultable y limpiable; (e) inspección estructural (scene graph) para validar.
- Seguridad: bind a localhost; nombres de screenshot sanitizados y confinados a `screenshotDir`; texto del scene graph sin caracteres de control, recortado a 100 caracteres y tratado como no confiable.
- No hay handoff entre sesiones/herramientas ni logs de actualización.

## 5. Reutilizar / descartar / riesgos
Reutilizar:
- Tabla de timing y principios (animation-basics) como referencia `motion-principles.md`; traducir easings a Shotcut/MLT (keyframes smooth/ease) y ffmpeg (expresiones).
- Vocabulario chain/all/sequence/delay/loop para planes de edición agnósticos de herramienta.
- Presets de springs como catálogo semántico (entrada con rebote, suave, énfasis) mapeado a curvas por herramienta.
- Estructura SKILL.md + references temáticas; frontmatter name/description con "Use when".
- Handshake `/status`, respuestas `{ok}`, verificación por frame/screenshot, cola de errores: análogos a `shotcut_status`, `render_preview`, `validate_project`.
- Sanitización de rutas y texto no confiable.

Descartar: todo lo específico de Motion Canvas (generadores TS, signals, JSX, Vite, Iconify, LaTeX, presentation mode). No sirve para editar video existente.

Riesgos: (1) requiere Node, Vite y navegador abierto; la API HTTP no tiene auth (solo localhost); (2) instrucciones de ffmpeg con brew/apt: ajustar a Windows; (3) `npx skills add` instala código de terceros: revisar antes; (4) contenido verificado solo parcialmente por resúmenes; leer raw con curl antes de citar fórmulas; (5) faltan fórmulas de Ken Burns, subtítulos animados y ritmo de cortes: buscar en otros repos.
