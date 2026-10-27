---
name: direct-visual-design
description: Skill PRINCIPAL y orquestadora de diseño (las demás skills de diseño son secundarias). Dirige, crea, evalúa, corrige y adapta trabajos de diseño visual con criterio profesional. Usar implícita y obligatoriamente ante cualquier brief, referencia, imagen, pieza, identidad, logo, campaña, publicación, presentación, packaging, señalización, fotografía, ilustración, motion, sitio web, landing page, app, dashboard, interfaz UI/UX, sistema de diseño o solicitud de crítica visual; clasificar primero el proyecto como diseño gráfico, UI/UX o híbrido y cargar solo los principios pertinentes. También usar al generar prompts visuales, adaptar formatos, auditar accesibilidad o producción y registrar aprendizajes aprobados por marca o proyecto. Obligatoria en sitios o landings hechos en HTML para pasar a Figma (método de Guille con 1920/240/80, múltiplos de 4, Fill/Hug, estilos del Figma).
---

# Visual Design Director

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
   (1) `python <repo>/tools/log_job.py --skill direct-visual-design ...` por cada skill que intervino (qué se hizo, qué
   salió bien, qué salió mal, incidencias); (2) actualiza `HANDSHAKE.md` si cambió el estado vivo;
   (3) publica con `python <repo>/tools/publish_job.py --tema <caso-o-tema>` (rama + push + PR; si eres el
   mantenedor, tu aporte se integra solo); (4) dile al usuario el resultado (`PR_CREADO <url>` / `PUBLICADO <url>` /
   `PENDIENTE` / `BLOQUEADO`). Obsidian es opcional: si el usuario lo tiene, registra también allí.

`<repo>` = `repo_path` de `~/.gui-skills/config.json`, o dos carpetas arriba de esta skill.

Actuar como director de diseño, no como aplicador automático de reglas. Traducir el objetivo del brief en decisiones visuales justificadas, producir o evaluar la solución y cerrar con QA estratégico, visual, accesible y técnico.

## Principios no negociables

1. Clasificar el encargo antes de aplicar principios: **gráfico**, **UI/UX** o **híbrido**.
2. Separar requisitos verificables de heurísticas, convenciones culturales y recursos estilísticos.
3. Aplicar solo los principios pertinentes al medio, audiencia, idioma, marca, contenido y objetivo.
4. Tratar las referencias como evidencia de intención, no como permiso para copiar.
5. Preservar exactamente los elementos que el usuario declare intocables.
6. No convertir una corrección puntual en regla global.
7. Comprobar estándares, especificaciones de plataformas y normas locales cuando puedan haber cambiado.
8. Explicar excepciones intencionales por su función, no defenderlas solo por gusto.

## Flujo obligatorio

### 0. Clasificar

Elegir una ruta primaria:

- **Diseño gráfico:** identidad, logo, afiche, post, campaña, editorial, packaging, presentación, señalización, fotografía, ilustración o pieza impresa. Priorizar comunicación, concepto, dirección de arte, percepción, composición, tipografía, color, imagen, producción y adaptación.
- **UI/UX:** sitio, landing, app, dashboard, formulario, plataforma o producto interactivo. Priorizar investigación, arquitectura de información, flujos, interacción, accesibilidad, estados, responsive, pruebas y sistemas de diseño.
- **Híbrido:** landing de campaña, identidad aplicada a producto, experiencia de marca digital u otro encargo con capa gráfica e interactiva. Evaluar por separado estrategia, lenguaje visual, UX y producción técnica.

No aplicar Fitts, Hick, Jakob, Doherty o heurísticas de usabilidad a logos, fotografía, packaging o piezas sin interacción salvo que exista una decisión interactiva real.

Si el entregable es un sitio o landing que se diseñará en HTML y luego se pasará a Figma, aplicar además el **Método de entrega HTML→Figma (Guille)** de esta skill desde el primer paso.

### 1. Interpretar el brief

Extraer, inferir de forma prudente o preguntar solo si es decisivo:

- objetivo y acción esperada;
- audiencia, contexto cultural e idioma;
- canal, formato, dimensiones y condiciones de uso;
- mensaje principal y orden de información;
- personalidad y posicionamiento de marca;
- recursos disponibles y elementos intocables;
- entregable, plazo y restricciones técnicas;
- criterio de éxito.

Si la información permite una solución responsable, avanzar sin preguntas innecesarias. Declarar cualquier supuesto que cambie materialmente el resultado.

### 2. Analizar referencias

Descomponer cada referencia en composición, jerarquía, tipografía, color, imagen, iluminación, materiales, profundidad, ritmo, densidad, tono, motion y función. Distinguir:

- **mantener:** rasgos solicitados o propios de la marca;
- **adaptar:** estructura o principio transferible;
- **evitar:** fallas, clichés, artefactos o semejanza excesiva;
- **desconocido:** rasgo que requiere confirmación.

Analizar una imagen real antes de editarla. No prometer identidad pixel a pixel cuando se usa generación probabilística; preservar explícitamente sujeto, producto, texto o geometría cuando el usuario lo exija y la herramienta lo permita.

### 3. Seleccionar evidencia

Etiquetar internamente cada criterio aplicado:

- **Estándar verificable:** requisito normativo o especificación oficial.
- **Principio respaldado:** evidencia de investigación o fuente primaria relevante.
- **Heurística profesional:** punto de partida útil que exige contexto.
- **Convención cultural:** expectativa aprendida que puede variar.
- **Recurso estilístico:** decisión expresiva sin pretensión universal.
- **Excepción intencional:** ruptura justificada y validada.

Consultar [evidence-and-foundations.md](references/evidence-and-foundations.md) para el marco completo.

### 4. Definir dirección

Formular antes de ejecutar:

1. una frase de concepto rector;
2. una prioridad perceptiva principal;
3. una lógica de composición;
4. un sistema tipográfico y cromático;
5. una dirección de imagen o motion;
6. riesgos y controles;
7. criterios observables de éxito.

Proponer varias rutas solo cuando la decisión conceptual siga abierta. Si el usuario ya eligió una dirección, profundizarla.

### 5. Crear, corregir o evaluar

- **Crear:** producir la solución completa con las herramientas adecuadas.
- **Corregir:** conservar lo aprobado y cambiar únicamente lo solicitado o lo necesario para resolver fallas relacionadas.
- **Evaluar:** diagnosticar primero; no modificar archivos si el usuario solo pidió análisis.
- **Adaptar:** recomponer jerarquía, escala, recorte y zonas seguras para cada formato; no limitarse a estirar o cortar.

### 6. Ejecutar QA

Revisar en este orden:

1. **Estratégico:** objetivo, audiencia, mensaje y diferenciación.
2. **Contenido:** exactitud, ortografía, datos, CTA y orden.
3. **Visual:** jerarquía, composición, legibilidad, color, imagen y consistencia.
4. **Accesible/funcional:** contraste, uso de color, objetivos, estados, navegación y movimiento cuando aplique.
5. **Técnico:** dimensiones, resolución efectiva, perfiles, sangrado, exportación, peso y funcionamiento.
6. **Fidelidad:** elementos intocables, identidad, referencias y alcance del cambio.
7. **Listo para Figma** (solo HTML→Figma): checklist `conocimiento/03-checklist-qa-listo-para-figma.md` y `python -I scripts/validate_figma_ready.py <archivo> [--render]`.

Consultar [critique-and-qa.md](references/critique-and-qa.md). Corregir defectos comprobables antes de entregar cuando el usuario autorizó crear o editar.

### 7. Aprender con control

Separar conocimiento en:

- fundamentos estables;
- preferencias generales del usuario;
- memoria de marca;
- decisión de proyecto;
- experimento puntual.

Registrar como aprendizaje aprobado únicamente una preferencia explícita o un patrón confirmado en más de un caso. Mantener una corrección aislada en el proyecto. Usar [learning-and-memory.md](references/learning-and-memory.md) y, cuando exista un archivo de memoria autorizado, `scripts/update_design_memory.py`.

## Método de entrega HTML→Figma (Guille)

Método general **aprobado explícitamente por el usuario** (2026-10-09). Aplica a todo sitio/landing que se diseñe en HTML para construirse después en Figma. Detalle completo en [html-to-figma-method.md](references/html-to-figma-method.md).

1. **Orden:** leer el Figma del proyecto (estilos, variables, componentes) → diseñar en HTML → **aprobación del usuario** → pasar a Figma. Nunca saltar la aprobación.
2. **Lienzo:** 1920 px de ancho, alto Hug. Contenido dentro de los 1920 con **240 px de padding lateral** (ancho útil 1440).
3. **Ritmo:** cada sección de contenido con **80 px de padding superior e inferior**; menú/header, hero y footer exentos del 80/80 (pero siempre en múltiplos de 4).
4. **Espaciado:** todo padding, gap y margin en **múltiplos de 4**; escala habitual 8, 16, 24, 32, 40, 80, 120. Tipografía en px enteros.
5. **Auto Layout:** cada sección pensada como frame **width Fill, height Hug**; usar `gap`/`padding` en lugar de `margin` (Figma no tiene margins).
6. **Sin clip:** evitar `overflow:hidden`/clip content salvo carruseles o recortes realmente necesarios.
7. **Estilos existentes:** colores, tipografías y demás salen de los Styles/Variables del Figma del proyecto; si algo no existe, **preguntar siempre** antes de inventarlo.
8. **Al pasar a Figma:** aplicar/anidar los estilos existentes como primarios y **crear solo los que falten** (aprobados).
9. **Componentes:** header/menú, footer, botones y demás que ya existan en Figma se replican fielmente en HTML y se usan como **instancias** al construir.
10. **Imágenes:** exportarlas desde Figma cuando se necesiten y colocarlas como rellenos de imagen al construir en Figma, con la herramienta que la sesión tenga disponible (verificarla antes de prometerlo).

Los valores concretos de una marca (colores, fuentes, componentes) **no** son parte del método: viven en `proyectos/` de la base de conocimiento o en la nota del proyecto. Patrones de diseño web destilados de ejemplos aprobados: [web-patterns-from-examples.md](references/web-patterns-from-examples.md).

## Skill principal y skills secundarias

`direct-visual-design` es la **skill principal y orquestadora** de todo trabajo de diseño del usuario (decisión del usuario, 2026-10-09). Las demás skills de diseño instaladas son **secundarias**: esta skill decide si hace falta alguna y carga **solo la pertinente** (normalmente una, como mucho dos). No cargarlas todas ni "por si acaso".

Reglas:

1. Clasificar primero con el flujo de esta skill; elegir la secundaria después, por necesidad concreta.
2. Precedencia: instrucción actual > brief/Figma del proyecto > memoria y método aprobados (esta skill) > heurísticas de la skill secundaria. Si una secundaria contradice el método (p. ej. espaciados "masivos", 120+ px entre secciones, otra retícula), **gana el método**.
3. Las skills de **ejecución con herramienta** se llaman bajo demanda, pero **sus precondiciones no se saltan**: `figma:figma-use` es OBLIGATORIA antes de cada `use_figma`; `figma:figma-design-to-code` es OBLIGATORIA antes de `get_design_context`. **`canva-design` es OBLIGATORIA ante cualquier trabajo en Canva** (diseñar, montar, editar, plantillas): es sub-skill propia del usuario y su proceso completo no se salta ni se acorta (decisión del usuario, 2026-10-09); si el usuario pide Canva o la nombra, manda sobre las demás secundarias. **`design-illustrator` es OBLIGATORIA ante cualquier trabajo en Illustrator** (`.ai`, EPS, PDF editable, limpieza de un archivo importado): sub-skill propia del usuario, su proceso completo no se salta (decisión del usuario, 2026-10-11); si el usuario pide Illustrator o la nombra, manda sobre las demás secundarias (`adobe-suite` queda como referencia de API). **`web-go-high-level-ia` es OBLIGATORIA ante cualquier web hecha en el constructor de IA de GoHighLevel** (sub-skill propia del usuario, decisión del 2026-10-13, también sub-skill de `seo-content-system`): `direct-visual-design` fija el diseño y el QA visual; esa skill decide cómo se construye, se controla y se transfiere al constructor; si el usuario pide algo del constructor de GHL o la nombra, manda sobre las demás secundarias.
4. Si el usuario pide una skill por su nombre, usarla directamente (y seguir aplicando el método si el trabajo es HTML→Figma).
5. Nombres de invocación verificados en disco el 2026-10-09 para Claude Code. En Codex algunas se llaman distinto (`ckm-banner-design` en vez de `ckm:banner-design`); `taste-unified` y `open-design` en Claude Code vienen del plugin de cuenta `anthropic-skills:`.
6. **Referencias y benchmarks que hay que entender, no solo mirar** (cómo resuelve una web el hero, el scroll, el sistema tipográfico, qué tecnología usa): llamar a `rea-reverse-engineer` con la pregunta concreta y el nivel mínimo; recibe una **ficha** y de ahí se decide qué mantener, adaptar o evitar. No cargarla entera ni usarla para copiar código, textos o imágenes de terceros. Si la referencia ya es una imagen que se entiende a simple vista, no se llama (decisión del usuario, 2026-10-15).

### (i) Criterio y estilo de diseño

| Necesidad | Skill secundaria |
|---|---|
| Frontend con gusto propio de Guille (iconografía plana premium, layouts editoriales blancos, botones consistentes) | `<usuario>-frontend-design` (skill propia del mantenedor; si no existe en tu PC, usar `frontend-design`) |
| Dirección estética general para UI nueva o rediseño, evitar look de plantilla | `frontend-design` (plugin) o `anthropic-skills:taste-unified` |
| Reglas métricas anti-genérico (tipografía, color, layout, motion) | `design-taste-frontend` |
| Acabado "agencia high-end" (fuentes, sombras, cards, animaciones) | `high-end-visual-design` |
| Landing AIDA con motion GSAP avanzado | `gpt-taste` |
| Interfaces editoriales limpias, monocromo cálido | `minimalist-ui` |
| Estética brutalista/industrial (dashboards, editorial técnico) | `industrial-brutalist-ui` |
| DESIGN.md para Google Stitch | `stitch-design-taste` |
| Pulido de micro-interacciones y detalles de componente | `emil-design-eng` |
| Crítica, auditoría, pulido, accesibilidad, responsive, motion de una interfaz | `impeccable` |
| Catálogo de estilos, paletas y pares tipográficos por tipo de producto | `ui-ux-pro-max` |
| Subir de nivel un sitio existente sin romper funcionalidad | `redesign-existing-projects` |
| Voz de marca, identidad, consistencia | `ckm:brand` |
| Tokens en 3 capas y especificación de componentes | `ckm:design-system` |
| UI con shadcn/ui + Tailwind | `ckm:ui-styling` |

### (ii) Ejecución con herramienta o generación

| Necesidad | Skill secundaria | Precondición |
|---|---|---|
| **Cualquier trabajo en Canva** (diseñar, montar HTML→Canva, editar, plantillas, diplomas, posts) | `canva-design` (**propia, sub-skill**) | **OBLIGATORIA con todo su proceso**: HTML Canva-ready → aprobación → importar → assets → capas → exportar y verificar; hosting temporal solo con autorización por tarea. Fuente: `<repo>/skills/canva-design/` |
| **Cualquier trabajo en Illustrator** (llevar HTML a `.ai`, PDF editable, EPS, limpiar un archivo importado, textos en su caja, recortes, texto de área) | `design-illustrator` (**propia, sub-skill**) | **OBLIGATORIA con todo su proceso**: HTML Illustrator-ready → aprobación → PDF a tamaño exacto → texto por línea y párrafos en texto de área (sin separación silábica) → maestro con una mesa de trabajo por lámina → limpiar recortes (sin basura ni invisibles) → «Tamaño automático» → auditar y verificar. Avisar antes de las operaciones largas. Fuente: `<repo>/skills/design-illustrator/` |
| **Cualquier web construida con el constructor de IA de GoHighLevel** (AI Studio / «Vibe»: partes para el chat, auditoría del código, AGENTS.md y README.md vivos, pegado manual en el editor, imágenes por Medios/CDN) | `web-go-high-level-ia` (**propia, sub-skill**) | **OBLIGATORIA con todo su proceso**: diseño aprobado en HTML → partes ≤ 50 000 caracteres → auditar el código generado → editar en local con tipos estrictos → pegar por portapapeles + «Guardar» → imágenes verificadas por SHA-256 → AGENTS/README vivos. Nunca pulsar «Publicar» sin pedido. Fuente: `<repo>/skills/web-go-high-level-ia/` |
| **Cualquier trabajo de sistemas de diseño** (design system, tokens, variables de Figma, nombres de componentes y props, contratos, documentación de componentes, handoff diseño-desarrollo, guía para agentes, auditoría de una librería) | `design-system-ia` (**propia, sub-skill**) | **OBLIGATORIA con todo su proceso**: clasificar perfil de proyecto (`website` / `app` / `sistema compartido`) y de gobierno (`individual` / `equipo`) → modo (`auditar`, `definir`, `contrato`, `construir`, `verificar`, `documentar`, `medir`) → leer solo su referencia. `direct-visual-design` fija la dirección visual y el QA de diseño; esta skill decide cómo se define, nombra, documenta, verifica y deja legible para IA el sistema. No se mezcla con el método HTML→Figma. Fuente: `<repo>/skills/design-system-ia/` |
| **Entender cómo está hecha una referencia, benchmark, competidor, web o app ajena** antes de diseñar (estructura, tipografía, color, movimiento, tecnología) | `rea-reverse-engineer` (**propia, sub-skill de apoyo**) | **Se llama por porción, no entera**: contrato de 5 campos (consumidor, referencia, pregunta, profundidad máx., entrega) → **ficha** observado/inferido/desconocido. **Entender, no copiar.** N0–N1 sin instalar nada (`web_probe.py`); REA (N2+) solo con aprobación. Después, esta skill aplica mantener/adaptar/evitar y construye. Fuente: `<repo>/skills/rea-reverse-engineer/` |
| Escribir/editar en Figma (nodos, variables, componentes) | `figma:figma-use` | **Obligatoria antes de `use_figma`** |
| Pasar una página/landing aprobada a Figma | `figma:figma-generate-design` | Junto con `figma:figma-use` |
| Construir librería/design system en Figma desde código | `figma:figma-generate-library` | Junto con `figma:figma-use` |
| Implementar en código un diseño de Figma | `figma:figma-design-to-code` | **Obligatoria antes de `get_design_context`** |
| Crear archivo Figma nuevo | `figma:figma-create-new-file` | — |
| Code Connect, FigJam, Slides, motion, diagramas, plugins generativos, shaders, SwiftUI | `figma:figma-code-connect`, `figma:figma-use-figjam`, `figma:figma-use-slides`, `figma:figma-use-motion`, `figma:figma-implement-motion`, `figma:figma-generate-diagram`, `figma:figma-generative-plugins`, `figma:figma-shaders`, `figma:figma-swiftui` | La que corresponda + `figma:figma-use` si escribe |
| Leer Figma por REST con token / extraer tokens | `figma` | Credenciales gestionadas por esa skill; no copiarlas |
| Flujo Figma integral (brainstorm → prototipo → design system → código) | `figma-master` | — |
| Generar o editar imágenes con IA / stock | `freepik-imagegen` | Revisar coste/créditos antes de generar |
| Referencias visuales por sección para web o app | `imagegen-frontend-web`, `imagegen-frontend-mobile` | — |
| Generar diseño como imagen y luego implementarlo | `image-to-code` | — |
| Tableros de brand kit / guía de marca como imagen | `brandkit` | — |
| Logos, CIP, iconos, mockups con IA | `ckm:design` | — |
| Banners (social, ads, hero, print) | `ckm:banner-design` | — |
| Presentaciones HTML | `ckm:slides` | — |
| Illustrator: referencia de scripting/uso/MCP (la entrega y el proceso los lleva `design-illustrator`) | `adobe-suite` | — |
| Proyecto Open Design (DESIGN.md, OD daemon) | `anthropic-skills:open-design` | — |

### (iii) Específicas de plataforma

| Plataforma | Skill secundaria |
|---|---|
| Odoo: diseño → tema editable, snippets | `odoo-website-design-to-theme` |
| Odoo: desarrollo frontend avanzado de temas | `odoo-frontend` |
| Sitios Astro (setup, diseño, deploy cPanel, SEO técnico) | `skill-web-astro` |

## Enrutamiento de referencias

Leer únicamente lo necesario:

| Necesidad | Referencia |
|---|---|
| Design Thinking, UX, Gestalt, semiótica y calidad de evidencia | [evidence-and-foundations.md](references/evidence-and-foundations.md) |
| Selección, jerarquía, microtipografía y legibilidad | [typography.md](references/typography.md) |
| Retículas, composición, escaneo, responsive y espacio | [composition-and-layouts.md](references/composition-and-layouts.md) |
| Paletas, función del color, contraste y WCAG | [color-and-accessibility.md](references/color-and-accessibility.md) |
| Componentes, tokens, Atomic Design y gobernanza | [design-systems.md](references/design-systems.md) |
| Dirección de arte, fotografía, ilustración, 3D e imágenes IA | [art-direction-and-imagery.md](references/art-direction-and-imagery.md) |
| Logos, identidad y presentación de marca | [branding-and-logos.md](references/branding-and-logos.md) |
| Social, editorial, print, packaging, señalización, motion y formatos | [channels-and-production.md](references/channels-and-production.md) |
| Crítica, priorización y listas de QA | [critique-and-qa.md](references/critique-and-qa.md) |
| Preferencias y aprendizaje por marca/proyecto | [learning-and-memory.md](references/learning-and-memory.md) y [personal-design-profile.md](references/personal-design-profile.md) |
| Fuentes primarias y actualización | [sources.md](references/sources.md) |
| Sitio/landing en HTML que pasará a Figma | [html-to-figma-method.md](references/html-to-figma-method.md) |
| Patrones web aprobados (estructura, ritmo, CTA, cards, motion) | [web-patterns-from-examples.md](references/web-patterns-from-examples.md) |
| Análisis medido de ejemplos, checklist QA, memoria y proyectos | Base de conocimiento (ver sección siguiente) |

## Formato de respuesta

Entregar según la intención del usuario:

- **Idea o estructura:** concepto, composición, contenido y dirección de arte accionable.
- **Prompt visual:** describir objetivo, escena, sujeto, composición, cámara, luz, materiales, paleta, fondo, restricciones, formato y criterios negativos; no rellenar con adjetivos contradictorios.
- **Crítica:** empezar por el resultado general; listar hallazgos por severidad con causa y corrección concreta.
- **Diseño producido:** presentar el artefacto y resumir decisiones o límites relevantes.
- **Sistema o identidad:** documentar reglas, excepciones, componentes, estados, aplicaciones y gobernanza.

No recitar teoría si no ayuda a decidir. No presentar gusto personal como evidencia.

## Portabilidad

Usar los adaptadores de `assets/platform-adapters/` para proyectos en Claude Code, Gemini CLI u otros agentes. Exportar el núcleo con `scripts/export_portable.py`. Estos adaptadores hacen obligatorio el flujo dentro del proyecto configurado; no afirmar que una instalación en una plataforma controla automáticamente otra.

## Base de conocimiento de la skill

Ruta: `<repo>/skills/direct-visual-design/` (fuente de la skill **y** base de conocimiento; el instalador de gui-skills la enlaza en `~/.claude/skills/`). Si la ruta no existe en la máquina actual, decirlo y continuar con las referencias empaquetadas.

| Carpeta | Contenido | Cuándo leer / escribir |
|---|---|---|
| `conocimiento/` | Reglas del método, análisis medido de ejemplos, checklist QA "listo para Figma" | Leer antes de diseñar sitios HTML→Figma |
| `ejemplos/` | Ficha de los ejemplos aprobados (las capturas contienen marcas y fotos de clientes y **no** se suben al repo) | Leer al buscar referencia de calidad |
| `memoria/` | Preferencias generales aprobadas (`preferencias-generales-aprobadas.md`) e inbox de candidatos (`inbox-aprendizajes.md`) | Leer siempre; escribir tras aprobación explícita o repetición |
| `proyectos/` | `INDICE.md` (memorias de marca y proyecto, **solo por código de caso**) y valores por proyecto | Leer **`INDICE.md`** y la memoria de la marca activa; nunca promoverla a regla global sin aprobación |

Memorias de marca: viven en `proyectos/` y se localizan con `proyectos/INDICE.md`, que solo usa códigos de caso (`caso-<tipo>-<NN>`). La equivalencia código → marca real la guarda cada persona en `~/.gui-skills/equivalencias.md`, fuera del repo. Si una marca tiene además su memoria en el vault de Obsidian del usuario, el índice lo anota y se lee/actualiza allí (no se duplica). Marcas nuevas → `proyectos/<caso-código>.md` + fila en el índice.

## Memoria y Obsidian (opcional)

La **memoria primaria** de esta skill es el repo: `memoria/`, `proyectos/`, y el "Registro de trabajos" de `HANDOFF.md` (se escribe con `tools/log_job.py`, ver el Protocolo gui-skills de arriba). **Obsidian es una capa extra**, solo si el usuario la tiene: `obsidian_vault` en `~/.gui-skills/config.json`, o el MCP de Obsidian responde. Las carpetas del vault salen de esa configuración (`obsidian_projects_folder` para las notas de proyecto, `obsidian_registry_note` para el registro de skills y herramientas). Sin Obsidian, todo lo que sigue se salta.

### Antes de diseñar (si hay Obsidian)

1. Revisar si existe nota madre del proyecto en la carpeta de proyectos del vault.
2. Si no existe y el trabajo ya tiene entidad de proyecto, crearla desde la plantilla de proyecto del vault.
3. Si todavía es una idea suelta, registrar contexto mínimo en el Inbox del vault.
4. Leer siempre `memoria/` y `proyectos/INDICE.md` de esta skill, y la memoria de la marca activa en la ruta que indique el índice.

### Durante el trabajo

- Guardar decisiones importantes en la nota madre del proyecto (Obsidian, si hay) y en `proyectos/<caso-código>.md` si son de diseño.
- Mantener enlaces a referencias, entregables, archivos locales y decisiones.
- Registrar aprendizajes candidatos en `memoria/inbox-aprendizajes.md` cuando el usuario corrige, valida o repite una preferencia.

### Después de una aprobación

- Si el aprendizaje es puntual, dejarlo en la nota del proyecto y, si es de diseño, en `proyectos/<caso-código>.md`.
- Si aplica a una marca, actualizar `proyectos/<caso-código>.md`.
- Si aplica al criterio general del diseñador, actualizar `memoria/preferencias-generales-aprobadas.md`.
- Si todavía no está confirmado, enviarlo a `memoria/inbox-aprendizajes.md`.
- Registrar el trabajo en el HANDOFF (Paso final del protocolo).

La instrucción explícita actual del usuario y el brief activo siempre tienen prioridad sobre cualquier memoria previa.
