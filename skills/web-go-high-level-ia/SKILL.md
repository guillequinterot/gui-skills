---
name: web-go-high-level-ia
description: Skill propia y OBLIGATORIA para construir un sitio web dentro del constructor de IA de GoHighLevel (AI Studio / «Vibe», TanStack Start + React + Tailwind v4) a partir de un diseño aprobado en HTML, y mantenerlo bajo control. Es sub-skill de direct-visual-design (diseño y QA visual) y de seo-content-system (title, meta, H1, alt, schema, noindex, enlazado). Cubre el proceso completo: UI kit y Home en HTML → «partes» de ≤ 50 000 caracteres que se pegan al chat del constructor (solo admite imágenes y texto) → auditoría del código que generó la IA → edición local con chequeo de tipos → pegado manual por portapapeles en el editor de código + «Guardar» → imágenes por Medios (el CDN renombra los archivos; emparejar por SHA-256) → AGENTS.md y README.md vivos (handoff + handshake dentro del proyecto) para que la IA del constructor no pierda el hilo. Incluye el registro de incidencias (choque de .container con Tailwind, rutas relativas de imagen, CDN que renombra, ctrl+S que escribe una «s», botón Publicar, portapapeles pisado). Usar ante GoHighLevel AI Studio, vibepreview, constructor de IA de GHL, «el builder», AGENTS.md del constructor, Medios/CDN filesafe, o cualquier web hecha con la IA de GoHighLevel.
---

# Web en GoHighLevel AI Studio — sub-skill de `direct-visual-design` y de `seo-content-system`

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
   (1) `python <repo>/tools/log_job.py --skill web-go-high-level-ia ...` por cada skill que intervino (qué se hizo, qué
   salió bien, qué salió mal, incidencias); (2) actualiza `HANDSHAKE.md` si cambió el estado vivo;
   (3) publica con `python <repo>/tools/publish_job.py --tema <caso-o-tema>` (rama + push + PR; el mantenedor
   puede añadir `--merge`); (4) dile al usuario el resultado (`PR_CREADO <url>` / `PUBLICADO <url>` /
   `PENDIENTE` / `BLOQUEADO`). Obsidian es opcional: si el usuario lo tiene, registra también allí.

`<repo>` = `repo_path` de `~/.gui-skills/config.json`, o dos carpetas arriba de esta skill.

**Estatus (decisión del usuario, 2026-10-13):** es sub-skill propia de **`direct-visual-design`** (la principal clasifica, fija la dirección visual y hace el QA de diseño) y de **`seo-content-system`** (todo lo de SEO/AEO de cada página). Cuando el usuario trabaja una web en el constructor de IA de GoHighLevel o nombra esta skill, **su proceso es OBLIGATORIO y completo**. Precedencia: instrucción actual del usuario > brief/marca del proyecto > esta skill > heurísticas de otras skills.

Reparto: `direct-visual-design` decide **cómo se ve** (HTML aprobado, kit, marca); `seo-content-system` decide **cómo se escribe y se indexa**; **esta skill decide cómo se construye, se controla y se transfiere dentro del constructor de GHL**. Si se invoca sola, aplica igualmente los principios de las dos.

## Regla de oro

> **Diseño aprobado en HTML → partes de texto para el constructor → auditar el código que la IA generó → corregir en local (tipos estrictos + servidor local) → pegar a mano en el editor + «Guardar» → verificar en la vista previa → dejar AGENTS.md y README.md vivos para que nadie pierda el hilo.**
> El constructor **no deja subir archivos al proyecto**: solo imágenes (≤ 5) y texto (≤ 50 000 caracteres por mensaje) en el chat, y edición de código a mano. Todo el proceso está pensado para ese cuello de botella.

## Qué debe cumplir SIEMPRE el proyecto entregado (criterio de aceptación)

1. **La Home (y cada página) se ve idéntica al HTML aprobado**: misma estructura, textos literales, alturas y espaciados (probado con capturas contra el original).
2. **Estructura común en `__root.tsx`** (header, menú móvil, footer, flotantes, 404/error en español); cada ruta solo trae su contenido y su `head()`.
3. **Estilos de marca en un CSS propio** (`src/<proyecto>.css`; ver el caso `caso-web-universidad-01`), sin clases que choquen con Tailwind (`container`, `hidden`, `flex`…); sin utilidades de Tailwind ni shadcn en páginas de marca.
4. **Datos en un solo módulo** (`src/lib/*-data.ts`): listados del cliente, enlaces, IDs de CRM, `img()` con base única y `IMG_URLS`.
5. **SEO por ruta** (`title`, `description`, canonical, og:*, un `h1`, schema, `noindex` mientras sea provisional) — ver [06](references/06-seo-en-ghl-ai-studio.md).
6. **`AGENTS.md` y `README.md` presentes y vivos**: reglas + memoria del proyecto; la IA del constructor los lee antes y los actualiza al terminar ([03](references/03-agents-md-y-readme-vivos.md)).
7. **Chequeo de tipos estricto limpio** (salvo los errores de `routeTree.gen.ts` desactualizado en local) y la vista previa responde 200 en todas las rutas.
8. **Imágenes conectadas** con el mapa archivo→URL verificado byte a byte ([05](references/05-imagenes-medios-cdn.md)).
9. Nada inventado: cifras, enlaces, testimonios o promesas; lo pendiente del cliente queda con marcador visible y anotado en el README.

## Flujo obligatorio (detalle en [01-proceso](references/01-proceso-completo.md))

0. **Preflight:** `python -I scripts/handshake.py` (Node, Chrome para Claude in Chrome y capturas headless, carpetas). Leer la ficha del proyecto en `proyectos/` y, si usas Obsidian, la nota del proyecto.
1. **Diseño y contenido:** UI kit + páginas en HTML con `direct-visual-design` y `seo-content-system`. Aprobación del usuario antes de pasar al constructor.
2. **Partes para el constructor:** `scripts/make_partes.py` (configuración JSON, ver `ejemplos/caso-web-universidad-01/partes.ejemplo.json`) → PARTE-1…5 (≤ 50 000 caracteres, contiguas y verificadas), imágenes de referencia (≤ 5), carpeta de imágenes aparte ([02](references/02-partes-para-el-constructor.md)).
3. **Construcción por la IA** y primera revisión visual en la vista previa. Corregir con ajustes cortos (uno por mensaje).
4. **Auditar el código generado:** descargar el proyecto («Descargar base de código»), leer cada archivo propio, listar hallazgos ([01](references/01-proceso-completo.md) §4).
5. **Editar en local** (copia de respaldo primero), `tsc --noEmit` en una copia con `npm i`, servidor local y capturas con Chrome headless (`scripts/cshot.sh`; Edge falla si el usuario lo tiene abierto, 07 F8).
6. **Transferir:** portapapeles + editor + «Guardar», un archivo a la vez, verificando pestaña y primera línea antes de guardar ([04](references/04-transferencia-editor-portapapeles.md)). **Nunca pulsar «Publicar» sin pedido del usuario.**
7. **Imágenes:** carpeta de la entrega → Medios → «Insertar enlaces» → la IA actualiza `IMG_URLS`; contrastar con `match_cdn.py`.
8. **Verificar en la vista previa real** (rutas, h1, secciones, imágenes rotas, consola) y **registrar**: README del proyecto, entrada del registro de trabajos en el `HANDOFF.md` de la skill (`tools/log_job.py`), `HANDSHAKE.md` si cambió el estado, `memoria/inbox-aprendizajes.md` y, si usas Obsidian, la nota del proyecto.

## Reglas duras

1. **No pulsar «Publicar»** ni cambiar ajustes de la cuenta/proyecto sin permiso expreso del usuario. Tras «Guardar» la vista puede pasar a «Vista previa» y el botón de esa esquina pasa a ser «Publicar»: comprobar con captura antes de cada clic en esa zona.
2. **Backup antes de editar:** copia del original del builder en la carpeta del proyecto (`_backup-original`). El historial git está conectado al constructor: **no reescribir historial publicado**.
3. **No tocar** `routeTree.gen.ts`, `.env`, `vite.config.ts`, `start.ts`, `server.ts`, `integrations/supabase/*`, `.vibe/`. No instalar dependencias sin necesidad y aviso.
4. **Un archivo a la vez** en el editor: verificar el nombre de la pestaña **y** la primera línea pegada antes de «Guardar». Re-copiar al portapapeles justo antes de pegar (el constructor puede pisarlo).
5. **No usar Ctrl+S** (escribe una «s»). Guardar solo con el botón «Guardar».
6. **Imágenes siempre por `img()`**; el CDN renombra los archivos y no se puede cambiar: la relación nombre→URL vive solo en `IMG_URLS`. Contrastar por SHA-256, no por aspecto.
7. **No inventar contenido ni «arreglar» el texto del cliente**; lo pendiente se marca con `.placeholder` y se anota.
8. **Lo aprobado no se rediseña** sin pedido. Los cambios de diseño se hacen en el HTML fuente y luego se regeneran/pegan.
9. **La IA del constructor se gobierna con `AGENTS.md`** (reglas) y **`README.md`** (estado). Una tarea no está terminada hasta que el README refleja lo hecho.
10. **Verificar siempre** (tipos, rutas, capturas, consola) y decir con franqueza qué no se verificó. No declarar «listo» porque la compilación no falle.
11. **Credenciales:** los IDs de seguimiento del proyecto ya viven en el código del cliente; nunca copiar tokens/API keys a notas ni a la skill. `.env` no se lee ni se pega.
12. **Avisar** antes de operaciones largas (npm install ~5 min, esperas del constructor, recargas del panel ~20 s).

## Qué NO hacer

- No intentar subir archivos al proyecto por el chat (solo acepta imágenes) ni por la API de GHL (no crea páginas).
- No pegar contenido grande en el chat del constructor si se puede editar el archivo directamente en el editor.
- No dejar el shell (header/footer) repetido en cada página: va en `__root.tsx`.
- No usar `<a href>` para rutas internas existentes (usar `<Link>`); no dejar rutas de imagen relativas (`imagenes/…`) que fallan en rutas anidadas.
- No fiarse de `get_page_text` para leer el código del editor: es un iframe de otro origen. Descargar el código o ver capturas.
- No usar Arc para controlar con Claude in Chrome: solo funciona en Chrome.
- No confiar en capturas del navegador integrado cuando el panel está oculto: usar Chrome headless (`scripts/cshot.sh`).

## Dónde mirar

- Proceso: [01](references/01-proceso-completo.md) · partes: [02](references/02-partes-para-el-constructor.md) · AGENTS/README: [03](references/03-agents-md-y-readme-vivos.md) · transferencia: [04](references/04-transferencia-editor-portapapeles.md) · imágenes: [05](references/05-imagenes-medios-cdn.md) · SEO: [06](references/06-seo-en-ghl-ai-studio.md) · **incidencias: [07](references/07-incidencias-y-soluciones.md)** · caso: [08](references/08-caso-web-universidad-01.md).
- Estado, decisiones y registro de trabajos: `HANDOFF.md` · preflight, herramientas verificadas y límites: `HANDSHAKE.md` · historial: `CHANGELOG.md` · patrones de código sanitizados: `ejemplos/caso-web-universidad-01/`.
