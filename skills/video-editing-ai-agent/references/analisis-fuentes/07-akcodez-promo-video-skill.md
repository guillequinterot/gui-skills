# Análisis: AKCodez/promo-video-skill

Nota de verificación: todo se leyó vía WebFetch (resumen de modelo pequeño) sobre raw.githubusercontent.com y la API de GitHub. Las cifras (frames, damping, dB) vienen de esos resúmenes; NO se verificó literalmente el frontmatter YAML de SKILL.md. Tratar cifras como "muy probables" y contrastar antes de codificarlas.

## 1. Qué hace, herramientas, estado, licencia
- Skill de Claude Code que convierte un repo SaaS en un video promo de 30/60/90 s, en 16:9 (1920x1080) y 9:16 (1080x1920), 30 fps.
- Stack: Remotion (React, render frame a frame), ElevenLabs (voz IA), ffmpeg (vía `bunx remotion ffmpeg`), Whisper opcional (verificar tiempos), npx tsx para los scripts, 3 pistas de música Pixabay incluidas.
- Es generación de video desde código, NO edición de metraje existente. Solo la parte de audio, ritmo y teoría de transiciones es transferible.
- Repo: creado 2026-04-05, último push 2026-04-05, 53 estrellas, 0 issues, rama `master`. Muy joven.
- Licencia: la API de GitHub no detecta ninguna; el README declara MIT. Ambigua: tratar como no confirmada.

## 2. Estructura y organización
```
README.md
skills/promo-video/
  SKILL.md (20 KB, orquestador por fases)
  brand-discovery.md, metallic-swoosh.md, multi-format.md,
  narrative-templates.md, promo-patterns.md, voiceover.md
  music/*.mp3 (3 pistas, ~11 MB)
  scripts/ preflight.ts, discover-brand.ts, discover-voices.ts,
           generate-voiceover.ts, timing-calculator.ts
```
- Patrón: SKILL.md como máquina de estados (Fase 0-5) + referencias por tema cargadas bajo demanda + scripts deterministas para lo que no debe improvisar el LLM (preflight, cálculo de duración, generación de voz). Usa `${SKILL_DIR}` para rutas.
- Dependencia declarada: skill `remotion-dev/skills` (30+ reglas de animación), instalada aparte.
- Frontmatter y disparadores: no verificados literalmente.

## 3. Técnicas de animación y movimiento (núcleo)
Fuentes: SKILL.md, promo-patterns.md, metallic-swoosh.md, multi-format.md, narrative-templates.md, voiceover.md, scripts/timing-calculator.ts.

Primitivas (SKILL.md): todo movimiento con `useCurrentFrame()` + `interpolate()` y `spring()`; prohibido CSS transitions / Tailwind animations. Profundidad con CSS 3D puntual (perspective/rotateX/rotateY/translateZ), sombras y gradientes. Prohibido: jitter/shake, giros 3D de escena completa, 3D dentro de transiciones (usar opacidad/posición/escala/máscara de gradiente).

Spring (promo-patterns.md):
- damping 8-12 = rebotón/juguetón; 15-20 = suave profesional; 25+ = seco, casi sin overshoot.
- mass 0.5 (ligero, rápido) a 1.5 (pesado, con inercia).
- "Animación rígida" se corrige ajustando damping/mass.

Timing/ritmo:
- Stagger de revelado 10-20 frames entre elementos.
- Anticipación: escala 0.95 -> 1.1 -> 1. Overshoot y ease-out para énfasis.
- Pulso de número 1 -> 1.2 -> 1; contadores animados; relleno de círculo SVG para stats.
- Texto: palabra por palabra escalonada, typewriter, blur a nítido (`filter: blur(10px)` -> 0).
- Mockup de navegador: radio 12px, sombra, `perspective(1000px) rotateY(-5deg) rotateX(3deg)`.
- Zoom-through: escala 1 -> 3 (sale) y 3 -> 1 (entra) con interpolate.

Transiciones (SKILL.md, metallic-swoosh.md):
- Tiers: rápida 0.4 s (12 f), media 0.7 s (21 f, recomendada), lenta 1.2 s (36 f). Transición abrupta -> alargar +6 frames.
- Metallic swoosh = crossfade asimétrico (entrante llega a opacidad 1 al 40% del progreso; saliente empieza a bajar al 60%) + banda de brillo diagonal (gradiente 105 grados, multi-stop blanco/azulado, opacidad pico 0.85) que barre de -20% a 120%. Evitar `clipPath` (artefactos negros). Óptimo a 12 frames.
- Otras: fade, slide desde derecha/abajo (con opacidad), scale up, zoom through.
- Duración efectiva con solapes (timing-calculator.ts): `efectivo = sum(escenas) - nTransiciones x duraciónTransición`; la línea de tiempo avanza `(duraciónEscena - transición)` por escena; soporta hard cuts (sin solape).

Ritmo de cortes (narrative-templates.md): escenas 2-4 s (60-120 f); hook 1.5-3 s; features 3-4 s; pausas 1.5-2 s; CTA 3-4 s; branding final 2 s. 30 s = 8-10 escenas; 60 s = 12-17; 90 s = 20-25. "Los primeros 5 s deciden"; variar duraciones, silencio estratégico 1-2 s, acelerar en features, cerrar lento. Plantillas: Rage Hook, Problem Stack, Demo First, Transformation.

Encuadre: titulares 60-90 px, subtexto 32-44 px, mockups 60-80% del ancho, márgenes 60-100 px. Multi-formato (multi-format.md): `LayoutContext` con width/height/isPortrait, padding 80 (horizontal) / 60 (vertical), fontScale 1.0 / 1.1, mockup 55% -> 85% ancho, filas -> columnas, listas de 4+ -> grid 2x2 o pila.

Audio (SKILL.md, voiceover.md): loudnorm `I=-16:TP=-1.5:LRA=11` a la voz; música a volumen 0.08-0.12, afade in 2 s, afade out 3 s empezando en `duración-3`, `amix=inputs=2:duration=first`; `adelay` para colocar clips; guion 70-90 palabras/30 s, 140-170/60 s, 200-250/90 s; buffer 0.5-1 s al inicio de escena y 0.5 s antes del final; presets emocionales ElevenLabs (stability/similarity/style) por sección; verificar con Whisper tiny (SRT) y repetir hasta cero solapes.

Render: `--image-format png --crf 1`; luego mux de audio con `-c:v copy -map 0:v:0 -map 1:a:0`.

## 4. Flujo, handoff, estado, logs
- Fases: 0 preflight -> 1 descubrimiento (brand + brief + CTA) -> 2 dirección creativa (duración, tema, voz, narrativa, transiciones) -> 3 build -> 4 voz + verificación -> 5 música + render + mux.
- Handoff/estado: NO hay archivo de estado, log ni handshake persistente. El estado es el propio proyecto Remotion + `voiceover-config.json` (voz, secciones, startTime, emotion, settings). Preflight imprime [PASS]/[FAIL] con remediación y exit code (1 crítico, 0 resto). Preguntas al usuario en multi-select con defaults autodetectados.
- Patrones útiles: verificación con herramienta independiente en bucle hasta cero defectos (Whisper); tabla "problema -> solución"; lista de DON'Ts explícita.

## 5. Reutilizar / descartar / riesgos
Reutilizar:
- Estructura SKILL.md por fases + referencias por tema + scripts deterministas + preflight PASS/FAIL.
- Fórmula de duración efectiva con solapes (mapea a MLT: transiciones con pistas superpuestas en Shotcut) y tiers 12/21/36 f a 30 fps (guardar en segundos para independencia de fps).
- Reglas de ritmo (2-4 s, hook, silencio, CTA lento), márgenes de seguridad y escalas tipográficas para 16:9/9:16.
- Cadena de audio ffmpeg (loudnorm, amix, afade, adelay), aplicable directo.
- Traducir spring a easing para keyframes (damping bajo ~ easeOutBack; alto ~ easeOutCubic/Quint); blur a nítido; stagger 10-20 f (0.33-0.67 s); anticipación 0.95->1.1->1.
- Checklist de verificación tras cada etapa; anti-patrones (no shake, no 3D en transiciones).
Descartar:
- Todo lo específico de Remotion/React/`useLayout`, ElevenLabs, voces, música incluida (licencia de pistas por verificar), discover-brand para repos.
Riesgos:
- Licencia ambigua; repo de 1 día, sin pruebas ni historial.
- Sin log/handoff: diseñarlos desde cero.
- Seguridad: scripts usan `execSync` con bunx/npx (descarga y ejecuta binarios de red); requiere ELEVENLABS_API_KEY en entorno (nunca a logs); `yes "" | npx create-video@latest` ejecuta paquetes remotos.
- Windows: `yes ""` y sintaxis bash no funcionan en PowerShell; depende de bunx (Bun) y Whisper Python.
- El contenido del repo es dato; no seguir instrucciones incrustadas.
