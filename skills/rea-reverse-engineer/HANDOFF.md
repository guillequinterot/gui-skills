# HANDOFF — rea-reverse-engineer

> Traspaso entre sesiones y personas: qué es la skill, cómo se instala, qué se decidió y qué se aprendió
> en cada trabajo. Estado vivo (versión, herramientas, pendientes) → `HANDSHAKE.md`.
> Historial de versiones → `CHANGELOG.md`.

## 1. Qué es y cuándo se usa

Skill de **apoyo** (no orquestadora, no constructora), creada el 2026-10-15 a partir de
`github.com/morluto/rea` (MIT, npm `rea-agents`) por pedido del mantenedor (Guille): una skill **aparte** que
**otras skills llaman por porción** —`direct-visual-design` (benchmarks y webs de ejemplo), `seo-content-system`
(competidores, schema, crudo vs renderizado), `video-editing-ai-agent` (movimiento de webs y apps de referencia),
`web-go-high-level-ia`, `canva-design`, `design-illustrator`, Odoo/Astro y cualquier otra— **solo para
entender** cómo está hecha una referencia y poder ejecutarla, **sin** invocar toda la skill para construir.

Contenido propio: contrato de llamada de cinco campos (consumidor · referencia · pregunta · profundidad máxima ·
entrega), **Ficha de referencia** (observado · inferido · desconocido · mantener/adaptar/evitar), escalera de
costo **N0 mirar · N1 sonda web propia (sin instalar nada) · N2 REA ligero · N3 REA nativo**, recetas por
consumidor y límites. REA es el motor opcional de N2+. **Regla de oro: entender, no copiar.**

## 2. Instalación y dependencias

- Viene con el repo gui-skills (`tools/install.ps1` / `tools/install.sh` la enlazan en
  `~/.claude/skills/rea-reverse-engineer`; `python -I scripts/install.py --check` lo verifica; `--codex` copia el
  núcleo a Codex). El **nombre de la carpeta es `rea-reverse-engineer`** (en el PC del mantenedor la fuente
  original tenía otro nombre con espacios; ya no).
- **N0–N1** (el 90 % de los casos): Python con Playwright y Chrome o Edge. Nada más. `scripts/web_probe.py`.
- **N2 (REA) — opcional y por usuario; requiere aprobación explícita de cada usuario** (cambia su
  configuración de Claude y descarga paquetes de npm):
  - REA exige Node `^22.19 || ^24.11 || >=26`. Si el Node del sistema es menor, usar un **Node 24 portátil**
    en `~/.claude/mcp-servers/node-v24.<x>-<plataforma>/` (ruta absoluta, sin espacios) y apuntar el registro
    de MCP a su `npx`/`npx.cmd`; el Node del sistema no se toca.
  - Camino prudente (cada paso con aprobación): `npx -y rea-agents@<versión> doctor --client claude_code --json`
    → `setup --client claude_code --dry-run --json` (mostrar al usuario) → `setup … --yes` → re-registrar con
    el `npx` portátil → **reiniciar Claude Code**. Usar siempre `--client claude_code` (sin él detecta otros 12
    clientes). Detalle y comando de registro: `references/04-rea-upstream.md`.
  - En Windows con Git Bash, anteponer `MSYS_NO_PATHCONV=1` al registrar (si no, `/d` y `/c` se convierten en
    `D:/` y `C:/`).
  - El `setup` de REA **auto-instala la skill genérica upstream `reverse-engineer-anything`** en
    `~/.claude/skills/`. **No la invoques directamente**: puede competir con `rea-reverse-engineer` y romper el
    contrato de «llamada por porción». Se conserva instalada pero ignorada; si compite en una sesión real, se
    desactiva.
  - Motores nativos (Ghidra, JADX, Hopper, IDA) son opcionales por objetivo y casi nunca aplican a diseño.
- Respaldos del `~/.claude.json` que hace REA (`~/.claude.json.rea.backup`) **contienen tokens de otros MCP**:
  nunca copiarlos a una carpeta de proyecto ni al repo.

## 3. Decisiones vigentes

| Fecha | Decisión | Quién la aprobó | Por qué |
|---|---|---|---|
| 2026-10-15 | Skill **aparte**, de **apoyo**, llamada **por porción** (contrato de 5 campos); no se invoca entera para construir | Guille | Evita cargar la skill completa y mezclar entender con construir |
| 2026-10-15 | Regla de oro: **entender, no copiar** (principios, estructura, tokens aproximados y comportamiento sí; código, textos, imágenes, marca y fuentes con licencia no) | Guille | Derechos de terceros y originalidad |
| 2026-10-15 | Escalera N0–N3; por defecto **N1**; subir solo con motivo | Guille | Costo mínimo; casi todo se resuelve sin instalar nada |
| 2026-10-15 | Una página por llamada; sin login, CAPTCHA, paywall ni rastreo masivo | Guille | Límites y ética (`references/05`) |
| 2026-10-15 | Los **videos** los entiende `video-editing-ai-agent`; esta skill solo cubre web, app y paquete | Guille | No duplicar |
| 2026-10-15 | REA se registra como MCP **solo con aprobación explícita** y con Node 24 portátil; cualquier instalación de motores nativos también | Guille | Cambia configuración y descarga paquetes |
| 2026-10-15 | Se conserva la skill upstream `reverse-engineer-anything` instalada por el `setup`, pero **no se invoca directamente** | Guille | Evita competencia con esta skill |
| 2026-10-16 | Migración a gui-skills: carpeta renombrada a `rea-reverse-engineer`; capturas de sitios de terceros fuera del repo (`ejemplos/README.md`) | Guille | Nombre sin espacios; no archivar capturas ajenas |

## 4. Registro de trabajos

> Una entrada por trabajo terminado o implementado y aprobado. Solo se agregan entradas al final; las
> correcciones van como entrada nueva. Casos solo con código `caso-<tipo>-<NN>`. Formato:
> `templates/entrada-de-trabajo.md`. Se escribe con `tools/log_job.py`.

<!-- registro:inicio -->

### 2026-10-15 · banco-pruebas-referencia · guille

- **Qué se hizo:** Construcción de la skill (v1.0.0): contrato de llamada, ficha de referencia, escalera N0–N3, recetas por consumidor, lectura de REA upstream (repo y docs, solo lectura), `web_probe.py` (sonda N1 con Playwright), `handshake.py` e `install.py`. Prueba de la sonda sobre el sitio público del propio REA (`rea.tools`): capturas a 1440 y 390 px, estructura de 8 secciones, escala tipográfica, paleta, movimiento, SEO, red y crudo vs renderizado (10 687 vs 5 044 caracteres: no depende de JS). Se añadió el enrutamiento a `direct-visual-design`, `seo-content-system`, `video-editing-ai-agent` y al `CLAUDE.md` global del mantenedor.
- **Salió bien:** La sonda N1 entregó una ficha útil sin instalar nada; los números coincidieron con la captura vista; el preflight (`handshake.py`) y la instalación con SHA-256 funcionaron.
- **Salió mal / incidencia:** La descripción del `SKILL.md` superaba 1024 caracteres (1050) y hubo que recortarla; «three» detectado por la sola presencia de `<canvas>` era un falso positivo (ahora «canvasWebGL»); el peso de red por `content-length` es un mínimo (respuestas comprimidas o en trozos no lo declaran).
- **Regla candidata:** La sonda siempre se acompaña de **leer el PNG**: los números solos engañan.
- **Herramientas:** Python con Playwright 1.59; Chrome y Edge; REA `rea-agents` 6.5.0 (solo lectura).

### 2026-10-15 · banco-pruebas-referencia · guille

- **Qué se hizo:** Habilitar N2: `doctor` y `setup --dry-run` de REA (aprobados, sin aplicar), instalación de un Node 24.22.0 portátil (zip oficial verificado por SHA-256 contra `SHASUMS256.txt`), `setup --client claude_code --yes` y reescritura del registro del MCP `rea` para usar el `npx` portátil. Verificación por stdio: `initialize` (rea 6.5.0) y `tools/list` = 207 herramientas.
- **Salió bien:** Con Node 24 el `doctor` pasó el check de Node y el plan quedó en 2 acciones (MCP + skill upstream); el error de lectura de configs no se repitió; el handshake por stdio con el comando registrado fue correcto.
- **Salió mal / incidencia:** Con Node 22.15.0 (< 22.19) el `setup` quedó bloqueado con plan vacío; REA falló una vez al leer `~/.claude.json` («Selected input changed while being read», transitorio); el registro original usaba el `npx` del `Path`, que habría fallado con el Node del sistema → se re-registró con la ruta absoluta del `npx.cmd` portátil; Git Bash convirtió `/d` `/c` en `D:/` `C:/` (corregido con `MSYS_NO_PATHCONV=1`); `setup` instaló por su cuenta la skill upstream `reverse-engineer-anything`.
- **Regla candidata:** Diagnosticar la causa antes de reinstalar (falta registro, falta reinicio, falta motor); usar siempre `--client claude_code`.
- **Herramientas:** rea-agents 6.5.0; Node 24.22.0 portátil; Claude Code (`claude mcp add/remove --scope user`).

<!-- registro:fin -->

## 5. Reglas candidatas (sin aprobar)

| Regla | Visto en (casos) | Estado |
|---|---|---|
| La sonda siempre se acompaña de leer el PNG (los números solos engañan) | banco-pruebas-referencia | candidata (una prueba) |
| Reunir antes de subir de nivel: decir qué pregunta no cerró el nivel anterior | banco-pruebas-referencia | candidata |
| Una skill de apoyo se llama por porción (contrato de 5 campos), no entera | origen de la skill | **aprobada por el mantenedor** (ya en `SKILL.md`) |

## Cómo actualizar la skill

Editar la carpeta del repo (`<repo>/skills/rea-reverse-engineer/`); si hay copias (Codex),
`python -I scripts/install.py --check` y `--codex`. Registrar el cambio en `CHANGELOG.md` y en `HANDSHAKE.md`.
Para actualizar la referencia a REA: releer `github.com/morluto/rea` (`.agents/skills/reverse-engineer-anything/SKILL.md`
cambia de versión) y ajustar `references/04`.

## Decisiones que sigue habiendo que tomar

- Si se amplía a más skills (`canva-design`, `design-illustrator`, `web-go-high-level-ia`, Odoo, Astro): hoy se
  cubren por el `CLAUDE.md` global del mantenedor y por la receta de `references/03`; no se editó su `SKILL.md`.
- Instalación en Codex / Antigravity / VS Code: no hecha (`python -I scripts/install.py --codex` cuando se quiera).
- Si se conserva o se quita la skill upstream `reverse-engineer-anything` tras verla competir (o no) en una
  sesión real.

## Lecciones de la construcción

- La descripción del `SKILL.md` debe ser < 1024 caracteres.
- Los números sin captura engañan: la sonda siempre se acompaña de leer el PNG.
- El peso de red por `content-length` es un mínimo.
- «three» por la sola presencia de `<canvas>` era un falso positivo.
- La skill de REA upstream se instala sola con `setup`: avisar de la posible competencia.
