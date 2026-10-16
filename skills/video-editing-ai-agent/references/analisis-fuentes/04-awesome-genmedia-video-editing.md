# Análisis: awesome-genmedia/skills -> video-editing/SKILL.md

Verificación: el SKILL.md se leyó CRUDO (curl a raw.githubusercontent.com, ~9.5 KB, ruta real `.agents/skills/video-editing/SKILL.md`; `video-editing/SKILL.md` resuelve al mismo contenido). README y árbol vía WebFetch (resumen, no literal). Metadatos del repo vía API de GitHub (literal).

## 1. Qué hace, herramientas, estado, licencia
- Es un WRAPPER DE API CLOUD, no una skill de edición local. Todo pasa por each::sense (each::labs): un POST a `https://eachsense-agent.core.eachlabs.run/v1/chat/completions` (formato OpenAI, header `X-API-Key: $EACHLABS_API_KEY`, modelo `eachsense/beta`). El video se pasa como `image_url` con URL pública; máx. 4 "imágenes" por request; `stream` true/false.
- No usa ffmpeg, MLT, Shotcut, CapCut, Premiere ni After Effects. No hay scripts ni carpeta de referencias; el único archivo es el SKILL.md.
- Repo: 562 skills de medios generativos (14 core, 117 por categoría, 431 por modelo). Creado 2026-03-22, último push 2026-03-22 (mismo día), 32 estrellas: repo joven, marketing de un proveedor. Licencia MIT (API de GitHub, literal).
- Requiere cuenta y clave de pago de eachlabs.ai.

## 2. Estructura y organización
- Frontmatter: `name: video-editing`, `description` larga con "Use for:" y "Triggers:" (edit video, color grade, speed change, trim video, slow motion, timelapse, video style, video enhance, post production...), `allowed-tools: Bash(curl *), WebFetch`.
- Cuerpo: Quick Start (curl, OpenAI SDK Python, con imagen de referencia, streaming) -> tabla de 8 capacidades -> Prompt Tips -> 5 ejemplos curl -> tabla de presets de color -> Common Pitfalls -> Related Skills (enlaces relativos a video-generation, image-editing, sound-effects, music-generation) -> Documentación.
- El repo replica la skill vía symlinks en ~19 carpetas de agentes (.claude, .kiro, .goose, .continue, etc.): patrón multi-plataforma útil (una fuente en `.agents/skills/`, symlinks a cada agente). En Windows los symlinks requieren modo desarrollador/admin: riesgo.
- Instalación: `/plugin install awesome-genmedia` o `npx skills add awesome-genmedia/skills@<skill>`.

## 3. TÉCNICAS DE ANIMACIÓN Y MOVIMIENTO (SKILL.md)
Resultado honesto: el archivo NO contiene técnicas técnicas reutilizables de movimiento. Todo son prompts en lenguaje natural delegados a un modelo remoto. Sin easing, sin keyframes, sin comandos ffmpeg, sin fórmulas ni duraciones parametrizadas.
- Easing/curvas: ausente. Solo la mención "speed ramping" sin parámetros.
- Zoom/Ken Burns: solo un ejemplo verbal ("quick zoom-in effect at the beginning for engagement") en el reformateo 16:9 -> 9:16; sin duración ni escala.
- Transiciones: solo "smooth fade-in at start and fade-out at end", sin duración.
- Texto/subtítulos animados: no cubierto (solo un sello de fecha VHS "08/15/1994" pedido por prompt).
- Ritmo/cortes: solo "Expecting frame-accurate cuts from natural language: include timestamps"; ejemplo de slow-mo "0:02 a 0:04 y volver a velocidad normal"; "0.5x" y "0.25x con interpolación de fotogramas".
- Único valor concreto aprovechable: vocabulario de looks (tabla de 8 presets: Teal & Orange, Film Noir, Vintage Film, Neon Cyberpunk, Pastel Dream, Documentary, Golden Hour, Nordic Minimal) y plantillas de descripción de look (Kodak Portra 400: desaturar ligeramente, highlights cálidos, negros elevados, grano; Blade Runner 2049: sombras azul profundo, highlights ámbar). Sirven como briefs de color, que luego se traducen a filtros MLT/ffmpeg (curves, colorbalance, eq, noise) por nuestra cuenta; el repo no da esa traducción.
- Conversión a vertical 9:16 "manteniendo sujeto centrado": concepto útil (reframe), pero sin comando (en ffmpeg sería crop=ih*9/16:ih + scale; esto es conocimiento propio, no del repo).

## 4. Flujo de trabajo, handoff, estado, logs
- Ninguno. Flujo de una sola llamada, sin estado, sin manifiestos, sin logs, sin verificación de resultado ni manejo de errores/polling. Sin handoff entre herramientas.
- Buenas prácticas cualitativas aprovechables: (a) describir el look objetivo concreto, no "que se vea cool"; (b) dar timestamps para edits temporales; (c) aplicar ediciones por etapas, no todas a la vez; (d) la calidad de la fuente limita mejoras; (e) usar imagen de referencia de estilo (ese patrón de "reference frame" es reutilizable como paso de QA/matching de color).
- Enlaces "Related Skills" muestran composición modular (edición + SFX + música + imagen), buen patrón de routing.

## 5. Reutilizar / descartar / riesgos
Reutilizar:
- Estructura de frontmatter con triggers explícitos y `allowed-tools` restringido.
- Tabla de 8 categorías de edición como taxonomía de intents (color, velocidad, estilo, mejora, recorte, efectos, formato, transiciones) para el router de la skill.
- Tabla de presets de color como catálogo de looks (mapear cada uno a parámetros ffmpeg/MLT propios).
- Sección "Common Pitfalls" como base de guardarraíles; patrón de symlinks multi-agente; enlaces a skills relacionadas.
Descartar:
- Todo el backend each::sense (cloud, de pago, opaco, no determinista, sin frame-accuracy). Incompatible con edición reproducible en Shotcut/ffmpeg.
- Style transfer generativo (Ghibli, VHS) como núcleo; solo opcional futuro.
Riesgos:
- Seguridad/privacidad: sube el video a un tercero (URL pública) y requiere API key; mala fit para material de cliente (caso-video-02). Nunca pegar la clave en archivos.
- Dependencia: proveedor nuevo (repo de 1 día de vida, `eachsense/beta`), API puede cambiar; la URL del video debe ser pública (en Windows local no hay hosting).
- Windows: symlinks del repo; comandos curl con comillas y `$EACHLABS_API_KEY` requieren adaptación en PowerShell.
- Conclusión: baja utilidad para nuestra skill; las técnicas de animación (easing, Ken Burns, subtítulos animados) deben buscarse en otras fuentes (MLT/ffmpeg/Shotcut docs, animate_clip del shotcut-mcp).
