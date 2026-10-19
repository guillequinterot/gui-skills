# HANDOFF — direct-visual-design

> Traspaso entre sesiones y personas: qué es la skill, cómo se instala, qué se decidió y qué se aprendió
> en cada trabajo. Estado vivo (versión, herramientas, pendientes) → `HANDSHAKE.md`. Historial de cambios → `CHANGELOG.md`.

## 1. Qué es y cuándo se usa

`direct-visual-design` es la **skill principal y orquestadora de todo trabajo de diseño** (decisión del mantenedor, 2026-10-09): clasifica el encargo (gráfico / UI-UX / híbrido), analiza referencias, fija la dirección, hace el QA y decide qué skill secundaria cargar (normalmente una, como mucho dos). Las skills hermanas de este repo que ella llama son `canva-design` (todo lo que viva en Canva), `design-illustrator` (todo lo que termine en Illustrator), `web-go-high-level-ia` (webs hechas en el constructor de IA de GoHighLevel) y, como apoyo por porción, `rea-reverse-engineer` (entender cómo está hecha una referencia). La llaman otras skills de diseño solo a través de su tabla de enrutamiento (`SKILL.md`, sección "Skill principal y skills secundarias").

Contenido de la carpeta:

| Ruta | Contenido |
|---|---|
| `SKILL.md`, `agents/`, `assets/`, `references/`, `scripts/` | Núcleo de la skill (24 archivos + este protocolo) |
| `conocimiento/` | Reglas del método HTML→Figma, análisis medido de 2 ejemplos, checklist QA "listo para Figma", lecciones técnicas de `use_figma` |
| `ejemplos/` | Ficha de los ejemplos aprobados (las capturas contienen marcas de clientes y no se suben al repo) |
| `memoria/` | `preferencias-generales-aprobadas.md`, `inbox-aprendizajes.md` |
| `proyectos/` | `INDICE.md` (memorias de marca, solo códigos de caso), `caso-landing-industrial-01.md`, plantilla |

**Método HTML→Figma (resumen).** Aprobado como método general el 2026-10-09: primero HTML → aprobación → Figma · 1920 × Hug · 240 px laterales · **80/80 en secciones de contenido** (menú/header y footer exentos; hero exento pendiente de confirmar) · todo espaciado múltiplo de 4 (8/16/24/32/40/80/120) · secciones Fill × Hug · sin clip salvo carruseles o necesidad real · estilos/componentes del Figma del proyecto, preguntar antes de inventar, crear en Figma solo los que falten · imágenes exportadas de/colocadas en Figma. Detalle: `references/html-to-figma-method.md`; checklist: `conocimiento/03-checklist-qa-listo-para-figma.md`; validador: `python -I scripts/validate_figma_ready.py <html|css|carpeta> [--render]`.

## 2. Instalación y dependencias

- Viene con el repo gui-skills (`tools/install.ps1` / `tools/install.sh`); no se copia a mano. El instalador enlaza `~/.claude/skills/direct-visual-design` al clon, así `git pull` actualiza la skill instalada. Frontmatter de `SKILL.md`: YAML válido, `name` + `description` de 887 caracteres (< 1024).
- Dependencias externas: Python 3.10+ (`python -I` para los scripts); `validate_figma_ready.py` en modo `--render` necesita Playwright + Google Chrome instalado; PIL para las hojas de contacto. Las skills secundarias que cite la tabla de enrutamiento son opcionales: se usan si existen en el equipo.
- Servidor MCP oficial de Figma: necesario solo para escribir/leer Figma (`use_figma`, `get_design_context`). El plugin de Figma pide OAuth; no hay credenciales en esta skill.
- Los respaldos previos (`_respaldo/`, versiones antiguas, zips) **no se suben** al repo; siguen en el PC del mantenedor.
- Tras editar la skill: abrir una rama `aporte/<alias>/<tema>` y PR (ver `CONTRIBUTING.md`); no hay copias que sincronizar a mano.
- Portabilidad: `scripts/export_portable.py` exporta el núcleo + adaptadores (`assets/platform-adapters/`) a un proyecto para usarlo desde Claude Code, Gemini CLI u otros agentes; no exporta `conocimiento/`, `memoria/` ni `proyectos/`.

## 3. Decisiones vigentes

| Fecha | Decisión | Quién la aprobó | Por qué |
|---|---|---|---|
| 2026-10-09 | `direct-visual-design` es la skill **principal y orquestadora** de diseño; las demás son secundarias y solo se cargan vía su tabla de enrutamiento (si una secundaria contradice el método, gana el método; las precondiciones de herramienta no se saltan; si el usuario nombra una skill, se usa directamente) | Guillermo Quintero | Evitar que varias skills de diseño compitan entre sí |
| 2026-10-09 | Método de entrega HTML→Figma (1920 / 240 / 80, múltiplos de 4, Fill/Hug, estilos del Figma del proyecto) es **regla general** | Guillermo Quintero | Es su forma de trabajar ("reglas de mi método, generales") |
| 2026-10-09 | 80/80 aplica a secciones de contenido; header/menú y footer exentos; hero exento **por confirmar** | Guillermo Quintero | Precisión del mismo día; el hero sigue pendiente |
| 2026-10-09 | 7 aprendizajes de los ejemplos promovidos a preferencia general: `gap`/`padding` en vez de `margin`; px enteros; reset de padding de `button`; un acento sin sombras (superficie + borde 1 px); secuencia de landing (hero → prueba cuantitativa → diferenciador → prueba cualitativa → caminos/CTA → contenido → FAQ → cierre); escala de radios ≤ 6; revelado fade + translateY 16–24 px ~400 ms con reduced-motion | Guillermo Quintero | Aprobados explícitamente |
| 2026-10-09 | Memoria de marca: criterio conservador, una sola fuente por marca (las notas que vivían en Obsidian se resumieron en `references/personal-design-profile.md` y se indexan en `proyectos/INDICE.md` por código) | Guillermo Quintero | No tener dos fuentes que diverjan |
| 2026-10-09 | `canva-design` es sub-skill propia y OBLIGATORIA para todo trabajo en Canva (proceso completo; manda sobre otras secundarias) | Guillermo Quintero | Caso `caso-diplomas-01` ("quedó muy bien") |
| 2026-10-11 | `design-illustrator` es sub-skill propia y OBLIGATORIA para todo trabajo en Illustrator; `adobe-suite` queda como referencia de API | Guillermo Quintero | Caso `caso-manual-marca-01` |
| 2026-10-13 | `web-go-high-level-ia` es sub-skill propia y OBLIGATORIA para webs hechas en el constructor de IA de GoHighLevel (también sub-skill de `seo-content-system`) | Guillermo Quintero | Caso `caso-web-universidad-01` |
| 2026-10-15 | `rea-reverse-engineer` se llama **por porción, no entera**, para entender referencias y benchmarks; si la referencia se entiende a simple vista, no se llama | Guillermo Quintero | "Entender, no copiar" |
| 2026-10-16 | La memoria primaria pasa al repo (HANDOFF/HANDSHAKE + `memoria/` + `proyectos/`); Obsidian queda como capa opcional (`~/.gui-skills/config.json`) | Guillermo Quintero | Poder compartir la skill con otras personas |

**Caso `caso-landing-industrial-01`** (solo proyecto, no es regla general; detalle en `proyectos/caso-landing-industrial-01.md`): footer de la página agrupadora en **HTML real, sin la imagen**; las imágenes de un bloque de UI aportadas por el usuario son **referencia visual, no entregable**; paint style `Surface` `#F1F1F1` creado en su Figma (dato del coordinador, no comprobado por esta skill); **fills duplicados** en ese Figma: `primary`, `Secondary`, `Primary 2`, `Typography`, `grayscale#5` ×2.

## 4. Registro de trabajos

> Una entrada por trabajo terminado o implementado y aprobado. Solo se agregan entradas al final; las
> correcciones van como entrada nueva. Casos solo con código `caso-<tipo>-<NN>`. Formato:
> `templates/entrada-de-trabajo.md`. Se escribe con `tools/log_job.py`.

<!-- registro:inicio -->
### 2026-10-09 · caso-home-01 · guille

- **Qué se hizo:** Se estudiaron dos sitios aprobados (una landing agrupadora de servicios B2B y la home de un sitio de marca agroalimentaria premium): lectura del CSS/marcado, render 1920 × 1080 con Playwright + Chrome, medición de valores computados y captura de página completa. De ahí salieron `conocimiento/02-analisis-ejemplos.md`, `references/web-patterns-from-examples.md`, el método HTML→Figma como regla general y el validador `scripts/validate_figma_ready.py` (modo estático y `--render`).
- **Salió bien:** El validador probado con ambos ejemplos separó con claridad lo que cumple el método (tokens en múltiplos de 4: 0 errores en 551 declaraciones en el sitio con tokens) de lo que no (52 % de valores computados fuera de múltiplos de 4 en la landing densa); 7 aprendizajes pasaron a preferencia general con aprobación explícita.
- **Salió mal / incidencia:** La landing mezclaba estilos inline y overrides con `!important` que impiden mapear estilos a Figma; el único hallazgo del sitio con tokens fue el padding por defecto de `<button>` (1 px / 6 px) y un bloque del carrusel desalineado a x = 160. Las capturas contienen marcas de clientes y quedaron fuera del repo.
- **Regla candidata:** Marcar los efectos que Figma no puede representar (máscaras complejas, `mix-blend`, efectos dependientes del cursor) como "solo web" en el handoff del HTML.
- **Herramientas:** Python 3 (`-I`), Playwright + Google Chrome instalado, servidor estático local, PIL

### 2026-10-09 · caso-landing-industrial-01 · guille

- **Qué se hizo:** Se pasó a Figma la página agrupadora aprobada en HTML (9 secciones, 573 nodos) con `use_figma`, usando los styles y componentes del archivo del proyecto; el footer se construyó en HTML real sin usar la imagen aportada y las imágenes del bloque de UI se trataron como referencia visual.
- **Salió bien:** Las 13 lecciones técnicas de `use_figma` (inspeccionar styles con sus IDs antes de construir, `createAutoLayout` con `fills = []` y `clipsContent = false`, orden crear → `appendChild` → `layoutSizing`, imágenes vía `upload_assets` y no `createImageAsync`, auditoría final por script) quedaron en `conocimiento/figma-use-lecciones-tecnicas.md` y sirven para cualquier proyecto del método.
- **Salió mal / incidencia:** El archivo Figma tenía fills duplicados con el mismo nombre (hubo que usar los styles que ya usaban los nodos); un style de gradiente se vio distinto al aplicarlo a nodos nuevos; los scripts de `use_figma` no son idempotentes y, si fallaban a medias, había que borrar lo creado antes de reintentar. Quedó sin decidir cuál fill duplicado es el canónico.
- **Regla candidata:** Antes de crear un style en Figma, comprobar si ya existe uno equivalente (los archivos pueden tener duplicados) y preguntar cuál es el canónico.
- **Herramientas:** MCP oficial de Figma (`use_figma`, `get_screenshot`, `upload_assets`), skill `figma:figma-use`

### 2026-10-17 · caso-landing-planes-01 · guille

- **Qué se hizo:** Página de venta de planes mensuales de contenido con IA para la marca personal del mantenedor, en HTML sin Figma (ruta UI/UX): hero con una parrilla simulada como visual del producto, diferenciador, 4 pasos, 3 planes con selector de moneda (local / USD, con parámetro de URL para la pauta), plan para agencias con tabla de descuento por volumen, sección 'sin letra pequeña', FAQ y cierre con muestra gratis. Marca tomada de la web anterior (Poppins, un solo acento verde, oscuro).
- **Salió bien:** Aprobada en la primera versión. La parrilla simulada mostró el producto sin fotos ni imágenes de IA, coherente con la promesa de 'que no parezca hecho con IA'. El QA con Playwright + Chrome a 1440 y 390 px detectó y permitió corregir problemas antes de entregar; el selector de moneda y el parámetro ?moneda=usd quedaron probados.
- **Salió mal / incidencia:** En móvil, la columna del hero desbordaba por un hijo de grid sin min-width: 0 (se corrigió con minmax(0,1fr)). Un caption de tabla con display inline-flex se renderizó debajo de la cabecera. La vista previa file:// del panel del navegador no cargaba assets relativos: hubo que servir la carpeta con un servidor local. Incidencia: Un <caption> con display:flex/inline-flex se desplaza fuera de su posición; usar un párrafo antes de la tabla.
- **Regla candidata:** En grids de 2 columnas que colapsan a 1 en móvil, declarar grid-template-columns: minmax(0,1fr) y min-width: 0 en los hijos para evitar desborde horizontal.
- **Herramientas:** Python 3 (-I), Playwright + Google Chrome, PIL, servidor http.server local, panel de navegador de Claude Code

### 2026-10-19 · caso-web-salud-01 · julian

- **Qué se hizo:** Home completa de un sitio de cirugía (13 secciones) diseñada en HTML a 1440 con contenido de 1200 (estándar de la agencia, en lugar de 1920/240), aprobada y pasada a Figma con use_figma: colección de variables de marca, 14 estilos de texto, 17 componentes y la página a 1440 × Hug con alturas de sección idénticas al HTML.
- **Salió bien:** Los tokens CSS con nombres 1:1 con las variables de Figma y los line-height en px enteros hicieron que cada sección saliera con la misma altura que en el HTML. El validador estático dio 0 errores de múltiplos de 4. Un solo marcador de posición reutilizable para imágenes faltantes permitió entregar el diseño completo sin fotos.
- **Salió mal / incidencia:** Tres tropiezos de herramienta: (1) findOne por nombre devolvió un frame homónimo en vez del texto y el script quedó a medias; (2) al sobrescribir el trazo de una instancia se perdió el enlace a la variable de color (se vio negro); (3) hijos con FILL vertical dentro de filas HUG dejaron alturas desiguales hasta alternar HUG y FILL. Material Symbols Outlined no existe en Figma: se usó Rounded Light.
- **Regla candidata:** En use_figma, buscar nodos por nombre Y tipo (findOne(n => n.name===x && n.type==='TEXT')); para tarjetas de igual alto en una fila usar layoutSizingVertical='FILL' en cada hija (no layoutAlign); no sobrescribir trazos en instancias, usar un divisor propio.
- **Herramientas:** MCP oficial de Figma (use_figma, upload_assets, get_screenshot), skills figma-use y figma-generate-design, validate_figma_ready.py, servidor local y panel de navegador

<!-- registro:fin -->

## 5. Reglas candidatas (sin aprobar)

| Regla | Visto en (casos) | Estado |
|---|---|---|
| El hero queda exento del 80/80 (hoy exento en `SKILL.md`, checklist y validador, marcado "por confirmar") | `caso-home-01`, `caso-landing-industrial-01` | Pendiente de confirmación del mantenedor |
| Las imágenes de un bloque de UI que aporta el usuario son referencia visual, no entregable | `caso-landing-industrial-01` | Solo proyecto; promover si se repite |
| Marcar como "solo web" en el handoff lo que Figma no representa sin trucos | `caso-home-01` | Candidata |
| En grids de 2 columnas que colapsan a 1 en móvil, declarar grid-template-columns: minmax(0,1fr) y min-width: 0 en los hijos para evitar desborde horizontal. | caso-landing-planes-01 | candidata |
| En use_figma, buscar nodos por nombre Y tipo (findOne(n => n.name===x && n.type==='TEXT')); para tarjetas de igual alto en una fila usar layoutSizingVertical='FILL' en cada hija (no layoutAlign); no sobrescribir trazos en instancias, usar un divisor propio. | caso-web-salud-01 | candidata |

### Decisiones pendientes heredadas (del cierre del 2026-10-09)

1. ¿El **hero** queda exento del 80/80? (afecta `SKILL.md`, checklist y validador).
2. ¿Aplicar la jerarquía principal/secundarias también en Codex (`AGENTS.md`) y Gemini (`GEMINI.md`)? Texto listo en el anexo.
3. Riesgo de secundarias con descripción amplia que pueden activarse solas y competir (`anthropic-skills:taste-unified`, `impeccable`, `ui-ux-pro-max`, `ckm:design`, `design-taste-frontend`, `high-end-visual-design`). Cambio mínimo propuesto si ocurre: anteponer a su `description` "Secondary skill — invoke only via direct-visual-design or when the user names it." (las que vienen de un plugin de cuenta quizá no sean editables).
4. Otros pendientes menores: verificar `proyectos/caso-landing-industrial-01.md` contra su Figma; decidir qué fill duplicado es canónico; `scripts/export_portable.py` no exporta `conocimiento/`, `memoria/` ni `proyectos/`; ¿unificar preferencias generales en una sola fuente?

## 6. Anexos heredados

### Jerarquía principal / secundarias — nombres verificados en disco (Claude Code, 2026-10-09)

| Grupo | Skills |
|---|---|
| (i) Criterio/estilo | `<usuario>-frontend-design` (propia del mantenedor), `frontend-design`, `anthropic-skills:taste-unified`, `design-taste-frontend`, `high-end-visual-design`, `gpt-taste`, `minimalist-ui`, `industrial-brutalist-ui`, `stitch-design-taste`, `emil-design-eng`, `impeccable`, `ui-ux-pro-max`, `redesign-existing-projects`, `ckm:brand`, `ckm:design-system`, `ckm:ui-styling` |
| (ii) Ejecución con herramienta | `figma:figma-use` (**obligatoria antes de `use_figma`**), `figma:figma-design-to-code` (**obligatoria antes de `get_design_context`**), `figma:figma-generate-design`, `figma:figma-generate-library`, `figma:figma-create-new-file`, `figma:figma-code-connect`, `figma:figma-use-figjam`, `figma:figma-use-slides`, `figma:figma-use-motion`, `figma:figma-implement-motion`, `figma:figma-generate-diagram`, `figma:figma-generative-plugins`, `figma:figma-shaders`, `figma:figma-swiftui`, `figma`, `figma-master`, `freepik-imagegen`, `imagegen-frontend-web`, `imagegen-frontend-mobile`, `image-to-code`, `brandkit`, `ckm:design`, `ckm:banner-design`, `ckm:slides`, `adobe-suite`, `anthropic-skills:open-design` |
| (iii) Plataforma | `odoo-website-design-to-theme`, `odoo-frontend`, `skill-web-astro` |

En Codex las `ckm` se llaman `ckm-*`; `taste-unified`/`open-design` en Claude Code vienen del plugin de cuenta `anthropic-skills`.

### Texto listo (no aplicado) para otros clientes

**`~/.codex/AGENTS.md`**, sección "## Direct visual design": sustituir la línea de memoria por

```markdown
- Record approved general learnings in `<repo>/skills/direct-visual-design/memoria/preferencias-generales-aprobadas.md`; brand memories are indexed in `<repo>/skills/direct-visual-design/proyectos/INDICE.md` (case codes only).
- `direct-visual-design` is the primary, orchestrating design skill. Other design skills are secondary: do not invoke them directly; load `direct-visual-design` first and use its routing table ("Skill principal y skills secundarias" in its SKILL.md), unless the user names a skill explicitly. In Codex the ckm skills are named `ckm-*`.
- For websites/landings designed in HTML for Figma, follow the skill's "Método de entrega HTML→Figma (Guille)".
```

**`~/.gemini/GEMINI.md`** (Antigravity y VS Code) — añadir al final, solo si la skill está instalada allí (no verificado):

```markdown
## Direct visual design
- `direct-visual-design` is the primary design skill (source: `<repo>/skills/direct-visual-design/`). Other design skills are secondary and are used through its routing table unless the user names one explicitly.
- For websites/landings designed in HTML for Figma, follow its "Método de entrega HTML→Figma (Guille)".
```

### Dónde está lo demás

- Método: `references/html-to-figma-method.md` · patrones: `references/web-patterns-from-examples.md`.
- Base de conocimiento: `conocimiento/`, `ejemplos/`, `memoria/`, `proyectos/INDICE.md`.
- Si el usuario usa Obsidian (`obsidian_vault`), sus notas de proyecto y el registro de skills (`obsidian_registry_note`) son una capa extra; no son necesarias para usar la skill.
