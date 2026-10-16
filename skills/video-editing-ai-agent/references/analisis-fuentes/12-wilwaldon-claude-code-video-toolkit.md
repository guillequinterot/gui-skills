# Análisis: wilwaldon/Claude-Code-Video-Toolkit

Fuente verificada: API de GitHub (árbol + metadatos) y README crudo (raw.githubusercontent.com). Complemento: README de digitalsamba/claude-code-video-toolkit (leído vía WebFetch, resumen de modelo pequeño, NO literal).

## 1. Qué es, estado, licencia
- NO es un toolkit con código: el árbol del repo contiene UN solo archivo, `README.md` (10 KB). Es una lista curada ("awesome list") de skills/MCP/plugins de video para Claude Code. No hay SKILL.md, scripts, referencias ni ejemplos propios.
- Cubre: Remotion (React->MP4), Manim (animación matemática), Playwright MCP `--save-video` (grabación de pantalla), Youtube-clipper-skill (yt-dlp + ffmpeg + subtítulos bilingües), FFmpeg (snippets), y el proyecto digitalsamba/claude-code-video-toolkit.
- Nada sobre Shotcut, MLT, CapCut, Canva, Premiere o After Effects.
- Actividad: creado y último push 2026-02-26 (mismo día, un solo commit aparente); 83 estrellas, 12 forks, 0 issues.
- Licencia: la API dice "ninguna" (sin archivo LICENSE); el README declara MIT. Inconsistente -> tratar como sin licencia formal.

## 2. Estructura y organización de skills
- Del repo wilwaldon: solo README con secciones (Remotion, Manim, Screen recording, YouTube clipping, FFmpeg, stacks recomendados, tabla resumen, contribución).
- No hay frontmatter/disparadores que analizar aquí. Lo único aprovechable es el mapa del repo hermano digitalsamba (no verificado literal): `.claude/` (skills + slash commands `/video`, `/record-demo`, `/brand`, `/contribute`), `lib/` (componentes, transiciones, tema), `tools/` (CLI Python), `templates/`, `brands/`, `examples/`, `projects/` (git-ignored).

## 3. Técnicas de animación y movimiento (lo importante)
Contenido muy pobre: el README NO documenta easing, curvas, Ken Burns, keyframes ni parámetros de spring.
- Primitivas mencionadas (solo nombres, README): `useCurrentFrame()`, `interpolate()`, `spring()`, `<Sequence>`, `<Composition>` de Remotion. Idea transferible: animación = función pura del número de frame (progreso = frame/duración) -> interpolar + easing. Aplicable a MLT (keyframes de `affine`/`rect` con interpolación) pero sin fórmulas en el repo.
- Transiciones (digitalsamba, no literal): 7 personalizadas (glitch, RGB split, zoom blur, light leak, clock wipe, pixelate, checkerboard) + 4 oficiales Remotion (slide, fade, wipe, flip). Útil como catálogo de nombres para mapear a MLT (luma/wipe, `affine`, `lumakey`) y ffmpeg `xfade` (p. ej. fade, wipeleft, slideleft, pixelize, radial=clock wipe).
- Subtítulos (Youtube-clipper, README): quemado con libass y "estilo personalizable"; no hay animación de texto documentada. Ruta ffmpeg: filtro `subtitles`/ASS.
- Ritmo/cortes: solo "capítulos semánticos de 2-5 min" en clipper; cortes con ffmpeg "frame-accurate" (sin comando literal).
- Comandos ffmpeg literales verificados (README):
  - Normalizar a 1080p30 con letterbox: `-vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps=30" -c:v libx264 -crf 18 -preset slow -movflags faststart`.
  - Preview web: `-c:v libx264 -crf 28 -preset fast -c:a aac -b:a 96k`.
  - GIF->MP4: `-pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" -movflags faststart` (par forzado para yuv420p).
  Estos son lo único copiable directamente.

## 4. Flujo de trabajo, handoff, estado, logs
- Del repo hermano digitalsamba (no literal): ciclo de vida planning -> assets -> review -> audio -> editing -> rendering -> complete; `project.json` por proyecto (escenas, estado de audio, historial de trabajo) y `CLAUDE.md` autogenerado por proyecto para continuidad entre sesiones. Este es el patrón de handoff más útil: estado en archivo máquina-legible + resumen humano regenerado.
- Clipper: pipeline de 7 pasos con selección humana de capítulos (punto de aprobación).
- wilwaldon: sin logs ni handoff propios.

## 5. Reutilizar / descartar / riesgos
Reutilizar:
- Los 3 comandos ffmpeg (normalización, preview, gif->mp4).
- Patrón `project.json` + `CLAUDE.md` autogenerado + fases con estado, adaptado a tu handshake/logs (añadir campo por herramienta: shotcut/ffmpeg/capcut...).
- Catálogo de transiciones como vocabulario para mapear a xfade/MLT.
- Punto de aprobación humano antes de cortes/renderizado.
Descartar:
- Remotion/Manim/Playwright: otro paradigma (código->render), no editan timelines de Shotcut/CapCut.
- Este repo como fuente de técnicas de movimiento: no las tiene. Buscar en Remotion docs, docs de MLT (`affine`, keyframes, easing en `mlt_animation`) y ffmpeg (`zoompan`, `xfade`).
Riesgos:
- Licencia ambigua (README MIT vs. API none); repo de un día, poco mantenimiento probado.
- Instalar `npx skills add ...` / `npx @playwright/mcp@latest` ejecuta código de terceros sin fijar versión (cadena de suministro).
- Instrucciones de instalación orientadas a macOS (`brew`); en Windows requerir ffmpeg con libass, yt-dlp y pysrt manualmente; los bucles `for` del README son bash (usar Git Bash o reescribir en PowerShell).
- Menos de 1 hora de contenido útil: no sobrevalorar.
