# HANDOFF — design-illustrator

> Traspaso entre sesiones y personas: qué es la skill, cómo se instala, qué se decidió y qué se aprendió
> en cada trabajo. Estado vivo (versión, herramientas, pendientes) → `HANDSHAKE.md`. Historial de cambios → `CHANGELOG.md`.

## 1. Qué es y cuándo se usa

Skill **propia** del mantenedor, **sub-skill de `direct-visual-design`** (la principal/orquestadora de diseño), hermana de `canva-design`. Nace del caso `caso-manual-marca-01` (manual de marca de 46 láminas): pasar HTML a Illustrator con un PDF de Chromium dejó **cada letra como un objeto**, **cientos de máscaras de recorte** (que al soltarlas dejan trazados invisibles) y **cajas de texto sin ajustar**. La skill documenta y automatiza la solución verificada. Decisión del mantenedor (2026-10-11): cuando se pida algo de Illustrator / `.ai` / EPS / PDF editable, o se llame esta skill, **es obligatoria y con todo su proceso**; `direct-visual-design` la llama cuando el entregable vive en Illustrator (fila "Cualquier trabajo en Illustrator" de su tabla de enrutamiento y mención en su regla 3; `adobe-suite` queda como referencia de API).

**Receta corta** (`references/01-pipeline-html-a-illustrator.md` es la receta completa): `handshake.py` → HTML aprobado → `export_pdf.py` → `extract_paragraphs.py` → **avisar al usuario** → `ai_pipeline.ps1 -Root <proyecto>` (probar con `-Max 3`) → `ai_autosize_text.ps1` (el ratón se mueve ~10 s) → `ai_audit.ps1` + `verify_fidelity.py` → reparar láminas con `ai_repair_page.ps1` → entrega y registro.

## 2. Instalación y dependencias

- Viene con el repo gui-skills (`tools/install.ps1` / `tools/install.sh`); no se copia a mano. El instalador enlaza `~/.claude/skills/design-illustrator` al clon. `scripts/install.py --check` detecta ese enlace y no copia nada.
- Dependencias externas: **Windows** con PowerShell y **Adobe Illustrator** (control por COM `Illustrator.Application` + ExtendScript; verificado en Illustrator Beta 31.0.0, interfaz en español, escala 125 %); Python 3.10+ con `playwright` (Chromium) y `pymupdf` (`fitz`); la fuente del diseño disponible **en Illustrator** (instalada o Adobe Fonts: `handshake.py` lo pregunta por COM). macOS, Illustrator estable 2025/2026 e interfaz en inglés: sin probar.
- El **MCP de Illustrator** (Beta, `http://localhost:18412/v1/mcp`, token del panel «MCP y herramientas») se puede registrar en Claude/Codex (comandos en `references/04`), pero a 2026-10-11 acepta la conexión y no responde: la vía verificada es COM. **El token nunca va en la skill ni en notas**: vive en la configuración de usuario del cliente o en una variable de entorno.
- Carpeta de la skill:

| Ruta | Contenido |
|---|---|
| `SKILL.md`, `references/` (6), `scripts/` (13) | Núcleo |
| `HANDOFF.md`, `HANDSHAKE.md`, `CHANGELOG.md` | Este estado |
| `ejemplos/caso-manual-marca-01/` | Herramientas originales de la sesión + README |
| `proyectos/` | `INDICE.md` + ficha del caso (solo código) |
| `memoria/` | `preferencias-illustrator-aprobadas.md`, `inbox-aprendizajes.md` |
| `conocimiento/` | `README.md` (qué guardar aquí) |

## 3. Decisiones vigentes

| Fecha | Decisión | Quién la aprobó | Por qué |
|---|---|---|---|
| 2026-10-11 | `design-illustrator` es OBLIGATORIA con todo su proceso ante cualquier trabajo en Illustrator / `.ai` / EPS / PDF editable; manda sobre otras secundarias | Guillermo Quintero | Petición de creación de la skill |
| 2026-10-10 | Los textos llegan a Illustrator **dentro de su caja de texto**: nunca una letra o una palabra por objeto | Guillermo Quintero | «Cada letra quedó por separado» |
| 2026-10-11 | Los **párrafos son texto corrido** (una caja de texto de área por párrafo), con separación silábica desactivada | Guillermo Quintero | «Los textos no quedaron como corridos» |
| 2026-10-11 | Todas las cajas de texto de área en **«Tamaño automático»** | Guillermo Quintero | «Que quede el texto área en automático… ajustadas» |
| 2026-10-11 | **Clipping mask solo si el diseño lo amerita**; al soltar uno se borra su trazado; ningún objeto invisible o basura | Guillermo Quintero | «Hay muchas cosas en clipping mask y eso no me gusta» |
| 2026-10-11 | Se puede trabajar directamente en el documento abierto del usuario cuando él lo pide (con aviso y sin cerrar nada); entrega = un `.ai` con una mesa de trabajo por página (más PDF editable) | Guillermo Quintero | «Yo lo quiero en el abierto que tiene todas las páginas» |
| 2026-10-11 | HTML primero, aprobación, después Illustrator; nunca editar el `.ai` a mano como fuente de verdad | Guillermo Quintero | El HTML es la fuente de verdad |
| 2026-10-11 | No cerrar ni sobrescribir documentos del usuario; backup antes de limpiar; no terminar Illustrator sin permiso; avisar antes de las operaciones largas (~15 min) o que mueven el ratón (~10 s) | Guillermo Quintero | Illustrator Beta se cerró solo una vez y se perdió lo no guardado |
| 2026-10-11 | Registrar el MCP de Illustrator en Claude (comando de Codex documentado) | Guillermo Quintero | Petición de creación de la skill |
| 2026-10-16 | Memoria primaria en el repo; Obsidian opcional | Guillermo Quintero | Poder compartir la skill |

Detalle de las 12 reglas duras y el criterio de aceptación (qué debe cumplir SIEMPRE el archivo entregado): `SKILL.md`.

## 4. Registro de trabajos

> Una entrada por trabajo terminado o implementado y aprobado. Solo se agregan entradas al final; las
> correcciones van como entrada nueva. Casos solo con código `caso-<tipo>-<NN>`. Formato:
> `templates/entrada-de-trabajo.md`. Se escribe con `tools/log_job.py`.

<!-- registro:inicio -->
### 2026-10-11 · caso-manual-marca-01 · guille

- **Qué se hizo:** Un manual de marca de 46 láminas (HTML 1920 × 1080, solo Poppins) se llevó a un `.ai` maestro con 46 mesas de trabajo y su PDF editable: PDF de Chromium a tamaño exacto en pt, letras → un texto por línea → párrafos en texto de área, limpieza de máscaras de recorte, «Tamaño automático» por clic automatizado, auditoría y verificación píxel a píxel y letra a letra. De ahí salieron los scripts generalizados (`-Root`, `-Master`, `-OutDir`).
- **Salió bien:** Resultado final con 1 028 textos (798 de punto, 230 de área ajustados), 0 recortes, 0 invisibles y 0 grupos vacíos; las 46 láminas idénticas al original (peor lámina 4 697 px de 2 073 600; 0 diferencias de caracteres); un texto de 489 letras sueltas pasó a 25 textos con tracking calculado; 427 máscaras de recorte pasaron a 0 (394 sin efecto soltadas, 31 vacías borradas, 5 necesarias rehechas a mano como un arco abierto); el proceso completo tarda ~15 min.
- **Salió mal / incidencia:** El PDF crudo de Chromium abre con una letra por objeto y cientos de recortes; 3 de 8 párrafos no coincidían por la **separación silábica** que Illustrator activa por defecto (se desactivó); la lámina 19 salió en blanco por el pegado y la 33 dio `CANT` (se rehicieron con `ai_repair_page.ps1`); error `AOoC` por el lienzo de 16 383 pt (rejilla desplazada); **Illustrator Beta se cerró solo** una vez (RPC `0x800706BE`) y el documento del usuario se perdió hasta «[Recuperado]» (desde entonces el proceso no cierra documentos y se avisa de guardar); «Tamaño automático» no tiene API (se automatizó el clic en el cuadro de Illustrator, con primer clic en la ventana equivocada → TOPMOST); un borde redondeado parcial (asa de bolsa) se dibuja como anillo recortado en 3 trozos; el MCP de Illustrator acepta la conexión pero no responde. Los PDF por lámina y el maestro se generaron antes de la limpieza.
- **Regla candidata:** Diseñar los arcos/asas como SVG en el HTML para que no nazcan recortes al exportar; generar los PDF por lámina y el maestro después de la limpieza y del Tamaño automático; un solo `.ai` maestro como versión buena.
- **Herramientas:** Illustrator Beta 31.0.0 (COM + ExtendScript), PowerShell, Python (playwright, PyMuPDF), Poppins vía Adobe Fonts
<!-- registro:fin -->

## 5. Reglas candidatas (sin aprobar)

Viven en `memoria/inbox-aprendizajes.md`; se promueven a `memoria/preferencias-illustrator-aprobadas.md` con aprobación del mantenedor o al repetirse en otro caso.

| Regla | Visto en (casos) | Estado |
|---|---|---|
| Diseñar los arcos/asas como SVG en el HTML para que no nazcan recortes al exportar | `caso-manual-marca-01` (asa de la bolsa: 5 recortes → 1 arco) | Candidata |
| Generar los PDF por lámina y el maestro **después** de la limpieza y del Tamaño automático | `caso-manual-marca-01` | Candidata |
| Avisar siempre antes de operaciones que mueven el ratón o abren Illustrator ~15 min | `caso-manual-marca-01` | Candidata |
| Un solo documento maestro por proyecto (`.ai`) como versión buena; los PDF se regeneran desde él | `caso-manual-marca-01` | Candidata |

## 6. Anexos heredados

### Integración con `direct-visual-design` (hecha el 2026-10-11)

Fila en la tabla (ii) «Ejecución con herramienta»: **Cualquier trabajo en Illustrator → `design-illustrator` (propia, OBLIGATORIA)** y mención en la regla 3 de la sección de skills secundarias. La copia de Codex de `direct-visual-design` no se tocó. La sección «Illustrator design» del `CLAUDE.md` global del mantenedor refuerza la regla.

### Estado del caso que la originó

`.ai` maestro con 46 mesas de trabajo, 1 028 textos (230 de área ajustados), 0 recortes, abierto en Illustrator. Ficha: `proyectos/caso-manual-marca-01.md`; cronología y cifras: `references/06-caso-manual-marca-01.md`.

### Pendientes de la skill

Ver `HANDSHAKE.md` ("Pendientes abiertos").

### Dónde mirar

- Receta: `references/01` · defectos: `references/02` · HTML: `references/03` · COM/MCP: `references/04` · QA: `references/05` · caso: `references/06`.
- Si el usuario usa Obsidian (`obsidian_vault`), su nota del proyecto y el registro de skills (`obsidian_registry_note`) son una capa extra; no son necesarias para usar la skill.
