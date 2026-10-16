# CHANGELOG — direct-visual-design

## 2026-10-09 (4) — Enlace con la sub-skill propia `canva-design`

- `SKILL.md`: fila **«Cualquier trabajo en Canva → `canva-design`»** en la tabla (ii) y precondición en la regla 3 (obligatoria, proceso completo; manda sobre otras secundarias cuando se pide Canva). Descripción del frontmatter **sin cambios** (887 caracteres).
- Instalado solo en Claude Code (`~/.claude/skills/direct-visual-design/SKILL.md` = fuente). **Codex NO actualizado** (no tiene `canva-design` ni el conector Canva): su copia queda sin la fila hasta decidir lo contrario.
- Respaldo del `SKILL.md` anterior: guardado en el PC del mantenedor (`_respaldo/` de `canva-design`; no está en el repo).
- Detalle y motivos: `<repo>/skills/canva-design/HANDOFF.md`.

## 2026-10-09 (3) — Cierre: documentación final y decisiones de proyecto caso-landing-industrial-01

- `HANDOFF.md` y `HANDSHAKE.md` reescritos como documentos autosuficientes: instalación y hashes (manifiesto `467dd50aaa1057e0` en fuente, Claude y Codex), respaldos y reversión, tabla de jerarquía, textos listos para `~/.codex/AGENTS.md` y `~/.gemini/GEMINI.md` (no aplicados), criterio de memoria, capacidades verificadas/no verificadas, decisiones pendientes y "Siguiente paso recomendado".
- `proyectos/caso-landing-industrial-01.md`: decisiones de proyecto (footer de la agrupadora en HTML real, no imagen; imágenes de bloque UI = referencia visual), paint style `Surface` `#F1F1F1` y fills duplicados en el Figma (`primary`, `Secondary`, `Primary 2`, `Typography`, `grayscale#5` ×2). Solo proyecto, no regla general.
- `proyectos/INDICE.md`: descripción de la fila caso-landing-industrial-01.
- Sin cambios en el núcleo instalado (no requiere reinstalar).

## 2026-10-09 (2) — Instalación, skill principal y ajustes aprobados

### Añadido
- `SKILL.md`: sección **"Skill principal y skills secundarias"** con tabla de enrutamiento en 3 grupos (criterio/estilo, ejecución con herramienta con sus precondiciones, plataforma); nombres verificados en disco. Descripción: "Skill PRINCIPAL y orquestadora de diseño".
- `proyectos/INDICE.md`: índice de memorias de marca con su ruta (las de Obsidian no se movieron); la skill lo lee antes de trabajar para una marca.

### Cambiado
- Regla 80/80 limitada a secciones de contenido; menú/header, hero y footer exentos (siempre múltiplos de 4) en SKILL.md, método, checklist, reglas y validador (`role` por sección: header/hero/footer/content).
- `memoria/`: los 7 candidatos pasan a `preferencias-generales-aprobadas.md` como "aprobado explícitamente por el usuario, 2026-10-09"; inbox vacío con historial.
- `conocimiento/01-reglas-metodo-html-figma.md`: reglas derivadas pasan a aprobadas.
- Descripción del frontmatter acortada a 887 caracteres (límite 1024) y sin `": "` que rompía el YAML.

### Instalado / sincronizado
- Núcleo instalado en `~/.claude/skills` y `~/.codex/skills` (24 archivos, verificados por hash).
- Vault privado del mantenedor: espejo `98-skill-source/` y zip actualizados (hoy reemplazados por el repo gui-skills).
- `~/.claude/CLAUDE.md`: sección "Direct visual design" (skill principal, secundarias vía tabla, precondiciones Figma, base de conocimiento). Respaldo en `_respaldo/`.

## 2026-10-09 — Método HTML→Figma de Guille + base de conocimiento propia (sin instalar)

Trabajo hecho sobre la copia en `<repo>/skills/direct-visual-design/`. Las instalaciones de `~/.claude/skills` y `~/.codex/skills` **no se tocaron**.

### Añadido
- `SKILL.md`: sección **"Método de entrega HTML→Figma (Guille)"** (10 reglas), paso de QA 7 "Listo para Figma", disparador en la descripción, 3 filas nuevas en el enrutamiento, sección **"Base de conocimiento de la skill"**.
- `references/html-to-figma-method.md`: método completo (orden, lienzo, espaciado, equivalencias CSS ↔ Auto Layout, estilos, componentes, imágenes, paso a Figma, qué no hacer, precedencia).
- `references/web-patterns-from-examples.md`: patrones destilados de los dos ejemplos aprobados.
- `scripts/validate_figma_ready.py`: validador (modo estático con librería estándar; modo `--render` con Playwright). Probado con ambos ejemplos.
- `conocimiento/` (README, reglas del método, análisis medido de ejemplos, checklist QA).
- `ejemplos/` (5 capturas a 1920 px + README; las capturas no están en el repo).
- `memoria/` (preferencias generales aprobadas — heredadas + método nuevo; inbox de candidatos).
- `proyectos/` (README con plantilla; `caso-landing-industrial-01.md` como ejemplo de valores de proyecto).
- `_respaldo/original-instalado-2026-07-23/`: copia intacta de la versión instalada.
- `HANDOFF.md`, `HANDSHAKE.md`, este `CHANGELOG.md`.

### Cambiado
- `SKILL.md` → "Integracion obligatoria con Obsidian": la memoria de diseño pasa de `Obsidian/.../04-memoria/` a `memoria/` y `proyectos/` de esta carpeta; Obsidian sigue como centro de mando de proyectos y enlaza la base vía nota puntero. Las memorias de marca heredadas se leen en Obsidian hasta migrarlas.
- `references/learning-and-memory.md` §5: nueva ruta de memoria y ejemplo de `update_design_memory.py --file`.
- `references/personal-design-profile.md`: bloque "Método web aprobado (2026-10-09)".
- `references/critique-and-qa.md`: bloque "HTML que pasará a Figma".

### Sin cambios
`agents/openai.yaml`, `assets/`, `scripts/export_portable.py`, `scripts/update_design_memory.py` y el resto de `references/`.

## 2026-07-22/23 — Versión instalada previa

Instalada en Claude y Codex (idénticas byte a byte). Fuente en el vault `98-skill-source/` y zip `diseno-multimedia/skill/direct-visual-design-codex-claude.zip` (ver diferencias en `HANDSHAKE.md`).
