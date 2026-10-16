---
name: rea-reverse-engineer
description: Skill propia de APOYO para entender cómo está hecha una referencia antes de construir algo parecido (comprensión, no copia). Otras skills la llaman, solo por la porción que necesitan, para desmontar una web, benchmark, competidor, app, plugin, paquete JS/Electron, captura de red o animación web, y devuelve una Ficha de referencia (observado, inferido, desconocido, mantener/adaptar/evitar). Escalera de costo: mirar, sonda web propia sin instalar nada y REA (morluto/rea) solo si la pregunta lo exige. La usan direct-visual-design, seo-content-system, video-editing-ai-agent y cualquier otra; o el usuario: "analiza esta web", "cómo hace esto", "benchmark", "desmonta", "ingeniería inversa", "qué tecnología usa", "REA". No construye ni copia código, textos o imágenes ajenos.
---

# REA — Reverse Engineer Anything (sub-skill de apoyo y transversal)

## Protocolo gui-skills (obligatorio)

Esta skill vive en el repo **gui-skills** y sigue [`shared/protocolo-skill.md`](../../shared/protocolo-skill.md):

1. **Paso 0 — cada vez que uses la skill:** corre `python <repo>/tools/check_update.py --quiet --pull`.
   `ACTUALIZADA n` → díselo al usuario en una línea y **vuelve a leer este `SKILL.md`** antes de seguir;
   `CAMBIOS_LOCALES` → avisa y no actualices; `SIN_RED` / `SIN_CREDENCIAL` → sigue con la copia local y dilo.
   Si avisa de aportes sin publicar, corre `python <repo>/tools/publish_job.py --reintentar` (preaprobado).
   Luego lee `HANDSHAKE.md` y el "Registro de trabajos" de `HANDOFF.md`.
2. **Privacidad:** en el repo los clientes solo se nombran con un código `caso-<tipo>-<NN>`; nunca
   nombres, marcas, dominios, correos, rutas personales ni credenciales.
3. **Paso final — obligatorio y preaprobado** (trabajo terminado y aprobado por el usuario; no pidas permiso):
   (1) `python <repo>/tools/log_job.py --skill rea-reverse-engineer ...` por cada skill que intervino (qué se hizo, qué
   salió bien, qué salió mal, incidencias); (2) actualiza `HANDSHAKE.md` si cambió el estado vivo;
   (3) publica con `python <repo>/tools/publish_job.py --tema <caso-o-tema>` (rama + push + PR; si eres el
   mantenedor, tu aporte se integra solo); (4) dile al usuario el resultado (`PR_CREADO <url>` / `PUBLICADO <url>` /
   `PENDIENTE` / `BLOQUEADO`). Obsidian es opcional: si el usuario lo tiene, registra también allí.

`<repo>` = `repo_path` de `~/.gui-skills/config.json`, o dos carpetas arriba de esta skill.

**Estatus (decisión del mantenedor, 2026-10-15):** skill propia aparte, **llamada por otras skills** (diseño, SEO, video y cualquier otra) cuando necesitan **entender** una referencia. No es orquestadora ni constructora: **mira, mide y explica**; quien la llamó decide qué construir y con qué proceso. Si el usuario la nombra directamente, se aplica igual: entrega una ficha y se detiene.

Upstream: **REA** (`github.com/morluto/rea`, MIT, npm `rea-agents`, sitio rea.tools). Esta skill es la capa propia: contrato de llamada, escalera de profundidad, sonda web sin instalar nada, recetas por consumidor y límites. Detalle de REA en [04](references/04-rea-upstream.md).

## Regla de oro

> **Entender, no copiar.** La salida es una **Ficha de referencia** (observado · inferido · desconocido · mantener/adaptar/evitar). Se reconstruye con los activos, textos y código propios del proyecto, nunca con los del tercero.

## Cómo la llama otra skill (contrato mínimo, ver [01](references/01-contrato-y-ficha.md))

Cinco campos; si faltan, se asumen y se declaran:

| Campo | Ejemplo |
|---|---|
| **consumidor** | `direct-visual-design`, `seo-content-system`, `video-editing-ai-agent`, … |
| **referencia** | URL, archivo, app, captura, paquete |
| **pregunta** | «¿cómo resuelve el hero y el scroll?», «¿qué schema y qué estructura de H2 usa?» |
| **profundidad máxima** | N0–N3 (por defecto **N1**) |
| **entrega** | resumen ≤ 1 página al consumidor + ficha completa guardada en la carpeta del proyecto |

**No se carga toda la skill:** leer este archivo, [01](references/01-contrato-y-ficha.md) y **solo** la receta de [03](references/03-recetas-por-consumidor.md) del consumidor; [02](references/02-escalera-y-sondas.md) y [04](references/04-rea-upstream.md) únicamente al subir de nivel.

## Escalera de profundidad (subir solo si la pregunta lo exige)

| Nivel | Qué es | Costo | Herramienta |
|---|---|---|---|
| **N0 Mirar** | Captura, imagen, página abierta, lectura del texto | mínimo | Read sobre PNG, navegador del panel, WebFetch |
| **N1 Sonda web** | Página renderizada: estructura, tipografía, color, espaciado, movimiento, SEO, tecnología, red | bajo, **sin instalar nada** | `python -I scripts/web_probe.py <url> --out <carpeta>` + mirar las capturas |
| **N2 REA ligero** | Scripts y módulos reales, source maps, rutas, red capturada, listeners, escenario con acciones, paquetes JS/Electron | medio; necesita REA (registrado, pendiente de reinicio y prueba) | `analyze_javascript_application`, `inspect_web_page`, `capture_browser_scenario`, `export_web_scripts`, `compare_web_captures` |
| **N3 REA nativo** | Binarios, APK, .NET, firmware, WASM, SQLite, pcap | alto; motores externos (Ghidra, JADX…) | Ver [04](references/04-rea-upstream.md) |

Casi toda referencia de diseño/SEO/video se resuelve en **N0–N1**. N2 es para «¿cómo logra este efecto/animación/flujo?» cuando el DOM no basta; N3 casi nunca aplica a diseño.

## Reglas duras

1. **Entender, no copiar** (regla de oro). Principios, estructura, tokens aproximados y comportamiento sí; código, textos, imágenes, marca y fuentes con licencia, no.
2. **Observado ≠ inferido ≠ desconocido**, siempre rotulado. Una huella de tecnología es un indicio; un valor computado no es el sistema de diseño original.
3. **Mirar, no solo medir:** leer los PNG de la sonda antes de concluir (a 1440 y 390).
4. **Una página por llamada**, sin login, sin saltar bloqueos ni CAPTCHA, sin rastreo masivo. Acceso solo a lo que ve cualquier visitante o a lo que el usuario es dueño o está autorizado a examinar.
5. **REA (N2) es opcional y por usuario.** En el PC del mantenedor está registrado como MCP `rea` desde 2026-10-15 (con su aprobación) usando un **Node 24 portátil** en `~/.claude/mcp-servers/node-v24.<x>-<plataforma>/` (REA exige Node ≥ 22.19; el Node del sistema no se toca). Su `initialize` + `tools/list` (207 herramientas) se verificaron por stdio, y el servidor **conectó en una sesión de Claude Code el 2026-10-16**; **aún no se ha ejecutado ninguna herramienta de análisis real**. Si las herramientas `mcp__rea__*` no aparecen, N2 no está disponible: seguir con N0–N1 y avisarlo. **Registrar el MCP o instalar motores nativos requiere aprobación explícita de cada usuario** (cambia su configuración de Claude y descarga paquetes de npm). N0–N1 funcionan sin él. Ver [04](references/04-rea-upstream.md) (sección «Instalación y estado») y `HANDSHAKE.md`.
6. **Subir de nivel con motivo:** decir qué pregunta no cerró el nivel anterior. No repetir una captura idéntica.
7. Los **videos** los entiende `video-editing-ai-agent` (`video_understand.py`, `frame_probe.py`, `fetch_reference.py`); esta skill solo aporta lo que no es video (web, app, paquete). No duplicar.
8. Guardar la ficha en la carpeta del proyecto (`referencias/`), nunca suelta; anotar en las notas del proyecto lo que cambie decisiones (y en Obsidian, si el usuario lo usa).
9. Credenciales y tokens: nunca en fichas ni notas.
10. **Skill upstream que puede competir:** el `setup` de REA auto-instala la skill genérica `reverse-engineer-anything` en `~/.claude/skills/`. **No la invoques directamente**: el contrato de «llamada por porción» y los límites de esta skill mandan; esa otra solo describe la operación de las herramientas de REA y, si aparece activada por su cuenta, se ignora y se avisa al usuario.

## Enrutamiento

| Necesidad | Archivo |
|---|---|
| Contrato de llamada y formato de la ficha | [01-contrato-y-ficha.md](references/01-contrato-y-ficha.md) · plantilla `templates/ficha-referencia.md` |
| Niveles, sonda web, navegador del panel vs Chrome, cuándo subir | [02-escalera-y-sondas.md](references/02-escalera-y-sondas.md) |
| Qué preguntar y entregar según quién llama (diseño, SEO, video, GHL, Canva, Illustrator, Odoo/Astro, desarrollo) | [03-recetas-por-consumidor.md](references/03-recetas-por-consumidor.md) |
| REA: qué es, tabla objetivo→herramienta, instalación, límites en Windows | [04-rea-upstream.md](references/04-rea-upstream.md) |
| Legalidad, privacidad, qué no hacer con lo entendido | [05-limites-y-etica.md](references/05-limites-y-etica.md) |

| Script (`python -I`) | Para qué |
|---|---|
| `scripts/web_probe.py` | Sonda N1 de una URL: capturas, estructura, tokens, movimiento, SEO, tecnología, red, crudo vs renderizado |
| `scripts/handshake.py` | Preflight: Node, REA, navegador, Playwright, enrutamiento en otras skills |
| `scripts/install.py` | Comprobar que la instalación enlaza al repo (`--check`); copiar el núcleo sin enlaces (`--copy`) o a Codex (`--codex`) |

## Integración

- **direct-visual-design:** referencias y benchmarks → esta skill entrega la ficha; la principal aplica *mantener/adaptar/evitar* y construye. Cuando la referencia ya está en N0 (imagen), no se llama.
- **seo-content-system:** competidores/SERP → estructura, schema, rendered vs crudo, enlazado, tecnología.
- **video-editing-ai-agent:** apps y webs animadas de referencia (movimiento, easing, secuencia); el video como tal lo analiza su propio flujo.
- **Resto** (`web-go-high-level-ia`, `canva-design`, `design-illustrator`, Odoo, Astro, desarrollo de plugins): misma ficha, receta en [03](references/03-recetas-por-consumidor.md).
- **Memoria:** el repo (`HANDOFF.md`/`HANDSHAKE.md` de esta skill) es la memoria principal; si el usuario usa Obsidian, además la nota del proyecto (continuidad) y su registro de herramientas.

## Base de conocimiento

Fuente canónica: `<repo>/skills/rea-reverse-engineer/` (instalada como enlace en `~/.claude/skills/rea-reverse-engineer`; `scripts/install.py --check` lo verifica; para Codex, `--codex` copia el núcleo). Núcleo: `SKILL.md`, `references/`, `scripts/`, `templates/`. Solo en el repo: `HANDOFF.md`, `HANDSHAKE.md`, `CHANGELOG.md`, `memoria/`, `proyectos/`, `conocimiento/`, `ejemplos/`. Aprendizajes nuevos → `memoria/inbox-aprendizajes.md`; se promueven con aprobación o repetición.

## Estado

**v1.0.1 (2026-10-15; migrada a gui-skills 2026-10-16).** Sonda N1 probada en una web pública de referencia (el sitio de REA). REA (rea-agents 6.5.0): registrado como MCP en el PC del mantenedor (Node 24 portátil), `initialize` y `tools/list` verificados (207 herramientas) y servidor conectado en una sesión de Claude Code (2026-10-16); **ninguna herramienta de análisis ejecutada aún**. Además `setup` instaló la skill upstream `reverse-engineer-anything` (ver regla 10). Estado vivo: `HANDSHAKE.md`; historia y decisiones: `HANDOFF.md`.
