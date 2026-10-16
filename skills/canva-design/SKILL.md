---
name: canva-design
description: Skill propia y OBLIGATORIA para cualquier trabajo en Canva (diseñar, montar, editar, migrar o crear plantillas), con su proceso completo HTML→Canva que deja todo editable (texto real, capas ordenadas, verificación por exportación). Es sub-skill de direct-visual-design, que la llama cuando el entregable vive en Canva, pero si el usuario pide algo de Canva o la nombra, esta skill manda y su proceso no se salta. Cubre formato físico en cm, importación de varias páginas de tamaños mixtos (posts, historias, banners), merge-designs, producción en serie con un motor de diseño, límites del conector Canva MCP (p. ej. la fuente de marca no se aplica al importar), hosting temporal para importar, assets horneados y QA. Usar ante Canva, enlaces canva.com o canva.link, diplomas, posts, historias, banners, plantillas o piezas que se editarán en Canva.
---

# Canva Design — sub-skill propia de `direct-visual-design`

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
   (1) `python <repo>/tools/log_job.py --skill canva-design ...` por cada skill que intervino (qué se hizo, qué
   salió bien, qué salió mal, incidencias); (2) actualiza `HANDSHAKE.md` si cambió el estado vivo;
   (3) publica con `python <repo>/tools/publish_job.py --tema <caso-o-tema>` (rama + push + PR; si eres el
   mantenedor, tu aporte se integra solo); (4) dile al usuario el resultado (`PR_CREADO <url>` / `PUBLICADO <url>` /
   `PENDIENTE` / `BLOQUEADO`). Obsidian es opcional: si el usuario lo tiene, registra también allí.

`<repo>` = `repo_path` de `~/.gui-skills/config.json`, o dos carpetas arriba de esta skill.

**Estatus (decisión del usuario, 2026-10-09):** `direct-visual-design` sigue siendo la skill principal y orquestadora de diseño; esta es su **sub-skill propia para todo lo que viva en Canva**. Cuando el usuario pide algo de Canva, o nombra esta skill, **su proceso es OBLIGATORIO y completo** ("quedó muy bien": no se improvisa ni se acorta). Precedencia: instrucción actual del usuario > brief/marca del proyecto > esta skill > heurísticas de otras skills secundarias (si una contradice este proceso, gana este proceso).

Reparto: `direct-visual-design` clasifica, analiza referencias, fija dirección y hace el QA de diseño; **`canva-design` decide cómo se construye y se monta en Canva** y verifica el resultado exportado. Si se invoca sola, aplica igualmente los principios de la principal (referencias: mantener/adaptar/evitar; QA estratégico→técnico).

## Regla de oro

> **Diseñar en HTML (Canva-ready) → aprobar → importar a Canva → colocar assets → ordenar capas → exportar y verificar → limpiar.**
> Nunca "dibujar directo en Canva por API": el conector no permite elegir fuente ni espaciado de letras, y se pierde la fidelidad. El importador de HTML sí conserva texto, fuente, tamaño, peso, color, interletraje y posiciones al píxel.

## Flujo obligatorio (detalle en [01-pipeline](references/01-pipeline-html-a-canva.md))

0. **Preflight:** `python -I scripts/handshake.py`; cargar herramientas Canva con `ToolSearch` (son *deferred*); leer la nota del proyecto (en el vault de Obsidian, si el usuario lo usa), la memoria de marca y `proyectos/`; si hay enlaces de Canva → `resolve-shortlink` + `read-design`.
1. **Brief y formato:** medida real → px (**100 px/cm**: 20×14 cm = 2000×1400). Texto **literal**; incoherencias señaladas, no corregidas; faltantes = marcadores + pendientes.
2. **Diseñar en HTML** con `templates/` + reglas Canva-ready; hornear assets (`scripts/bake_assets.py`); `lint_html_for_canva.py` = 0 errores; render con Chrome headless (`render_html.sh`) y **mirar las imágenes**; escala de impresión. **Mostrar previews y esperar aprobación.**
3. **Montar en Canva:** (3.1) pedir **autorización explícita para el hosting temporal de esta tarea** → `temp_host.sh upload`; (3.2) `import-design-from-url`; (3.3) `upload-asset-from-url` de cada asset; (3.4) `read-design` con transacción para los ids; (3.5) `edit-design` por página: `update_fill` del fondo, `insert_fill` de ornamentos/logo con medidas exactas, `insert_shape` para marcos, correcciones de texto, compensar numerales (−0,1 em); (3.6) `layer_element back` (ornamentos primero, fondo al final); (3.7) `update_title` + `commit`; (3.8) si el destino es un diseño existente: `merge-designs` (**1 operación por llamada**, con aprobación).
4. **Verificar:** `export-design` png → `canva_verify.py` → leer cada PNG y comparar con el render HTML; corregir y repetir.
5. **Limpiar y registrar:** `temp_host.sh cleanup` (comprobar 404); avisar de los diseños intermedios que quedan en la cuenta; registrar el trabajo con el Paso final del protocolo (HANDOFF §4), `memoria/` y, si hay Obsidian, la nota del proyecto y el registro de herramienta.

## Reglas duras

1. El HTML es la fuente de verdad del texto y la composición; **Canva se construye desde él**, no al revés.
2. Todo en capas absolutas con `data-layer`; **sin** `transform`, gradientes, `background:url()`, `box-shadow`, `filter`, flex/grid dentro de la página. Centrar = `left` explícito.
3. Texto = texto real. Fuentes nativas de Canva (Montserrat, Playfair Display, …); la fuente propietaria de la marca (p. ej. serif propia de la marca) se sustituye por la serif equivalente **y se avisa**.
4. Imágenes/fondos con degradé/pinceladas/mármol/triángulos = assets aparte (`bake_assets.py` o stock) colocados con `insert_fill`; Canva no importa `<img>`.
5. **Escala física antes que escala de pantalla:** al pasar a cm, reescalar la tipografía (cuerpo ≥ 28 px a 100 px/cm).
6. Lo que se inserta entra arriba: **orden de capas** siempre se corrige (ornamentos atrás, fondo al final).
7. Canva coloca los numerales grandes ~0,1 em más abajo: compensar. Cajas de texto con ancho ≥ 1,15× el real.
8. **Hosting temporal = publicación:** autorización por tarea, carpeta `_tmp-…` aleatoria, borrado inmediato y comprobación 404.
9. `merge-designs`: una operación por llamada; borrar páginas solo con aprobación de las operaciones exactas.
10. **Verificar siempre exportando** y mirando; no declarar "listo" sin comparar con el HTML. Decir con franqueza qué no se verificó.
11. No inventar contenido (firmantes, fechas, cifras). Señalar contradicciones del texto del cliente y esperar su decisión.
12. Credenciales: nunca en notas ni código; el acceso al hosting temporal sale de variables de entorno `CANVA_TMP_*` o de `~/.gui-skills/config.json` (fuera del repo), o de la skill de acceso a hosting que el usuario tenga.
13. **La fuente de marca no se aplica al importar** (solo fuentes de la biblioteca pública de Canva). Solución verificada por el usuario: cambiar la fuente en Canva **en bloque** tras importar → diseñar con **una sola familia y ≤3 estilos (Regular, Bold, Italic)**; con 2 familias, estilos casi idénticos (mapeo 1 a 1). Ver `references/08` §4.
14. **Probar merges y ediciones en una COPIA** (`copy-design`); no tocar el diseño original del usuario sin su aprobación. `merge-designs` = una operación por llamada; con `after_page_number` las páginas se invierten (arreglar con `move_pages`); los ids cambian tras cada operación.
15. **Varias páginas/tamaños**: un HTML con las páginas en orden importa como un solo diseño de tamaños mixtos; usar `scripts/prepare_multipage_import.py` (marcadores en lugar de `<img>`) y el título de página sale del `data-label`. Dar al usuario la **lista de URLs** de los diseños creados y avisar de los intermedios que no se pueden borrar.
16. **Producción en serie**: motor de diseño + config por programa (no HTML a mano), aprobar un programa de prueba, imágenes como archivos reemplazables, y montar en Canva **al final** por tandas (ver `references/08` y `ejemplos/caso-piezas-universidad-01/`).

## Qué NO hacer

- No usar el navegador integrado del panel para QA de archivos locales (abre una instantánea `data:` sin imágenes ni fuentes).
- No crear texto nuevo con `add_text` esperando la fuente de marca (se pierde); importar HTML.
- No reutilizar la autorización de hosting de una tarea anterior.
- No asumir que un diseño importado quedó bien porque la herramienta devolvió "success".
- No mezclar con el flujo HTML→Figma de `direct-visual-design` (1920/240/80, auto layout): son entregas distintas; si el usuario pide ambas, tratarlas por separado.

## Enrutamiento de referencias y scripts

| Necesidad | Archivo |
|---|---|
| Proceso completo paso a paso (la receta) | [01-pipeline-html-a-canva.md](references/01-pipeline-html-a-canva.md) |
| Límites y trucos del conector (importador, edit-design, offsets) | [02-limites-y-trucos-canva-mcp.md](references/02-limites-y-trucos-canva-mcp.md) |
| Hosting temporal, dominio, autorización, limpieza | [03-hosting-temporal.md](references/03-hosting-temporal.md) |
| cm→px, escala tipográfica de impresión, márgenes, contraste | [04-formato-impresion-y-escala.md](references/04-formato-impresion-y-escala.md) |
| Assets horneados y stock | [05-assets-procedurales.md](references/05-assets-procedurales.md) |
| QA local y en Canva; fallos típicos | [06-qa-verificacion.md](references/06-qa-verificacion.md) |
| Caso modelo (`caso-diplomas-01`): decisiones, errores, resultado | [07-caso-diplomas-01.md](references/07-caso-diplomas-01.md) |
| **Varios formatos/programas, merge, títulos de página, fuente de marca, costes** | [08-montaje-multipieza-y-fuentes.md](references/08-montaje-multipieza-y-fuentes.md) |
| Plantilla HTML Canva-ready 20×14 | `templates/diploma-20x14.template.html` |

| Script (`python -I`) | Para qué |
|---|---|
| `scripts/handshake.py` | Preflight local + lista de herramientas MCP a cargar |
| `scripts/lint_html_for_canva.py` | Detecta lo que el importador pierde (errores/avisos) |
| `scripts/build_import_html.py` | Une HTML de 1 página en un multipágina escopado y centra sin transforms |
| `scripts/render_html.sh` + `split_pages.py` | Render Chrome headless + corte por página + hoja de contacto |
| `scripts/bake_assets.py` | panel, swoosh, triangles, marble, canvas-bg, vignette, logo |
| `scripts/pdf_pages.py` | Analizar manuales/brochures `.pdf`/`.ai` (render, hoja de contacto, vectores) |
| `scripts/temp_host.sh` | Subir/verificar/borrar hosting temporal (con `--dry-run`) |
| `scripts/canva_verify.py` | Descargar exportaciones, comparar con el HTML, hoja de contacto |
| `scripts/prepare_multipage_import.py` | Combina HTML de varias páginas/tamaños, ordena por nomenclatura, cambia `<img>` por marcadores grises y escribe un manifiesto (flujo B) |
| `scripts/install.py` | Instalar por copia / verificar el núcleo (en gui-skills lo instala el instalador del repo con un enlace; este script detecta el enlace y no copia) |

## Base de conocimiento de la skill

Ruta: `<repo>/skills/canva-design/` (el instalador de gui-skills la enlaza en `~/.claude/skills/`; si no existe en la máquina actual, decirlo y usar las referencias empaquetadas).

| Carpeta | Contenido | ¿Se instala? |
|---|---|---|
| `SKILL.md`, `references/`, `scripts/`, `templates/` | Núcleo | Sí |
| `HANDOFF.md`, `HANDSHAKE.md`, `CHANGELOG.md` | Decisiones y registro de trabajos, estado vivo y capacidades verificadas, historial | Se leen en el Paso 0 |
| `ejemplos/caso-diplomas-01/` | Resumen anónimo del caso modelo (especificación de capas, rondas, resultado). Los HTML, assets y exportaciones con la marca del cliente quedaron fuera del repo | Solo lectura |
| `ejemplos/caso-piezas-universidad-01/` | Producción en serie: motor de diseño genérico (`motor_series.py`), regla tipográfica, hoja resumen, QA de texto, render por lotes y las notas del montaje en Canva. Configs por programa, textos y exportaciones del cliente quedaron fuera del repo | Solo lectura |
| `proyectos/` | Valores por marca para Canva, solo con código de caso (`caso-diplomas-01.md`, `caso-piezas-universidad-01.md`) + `INDICE.md` | Leer antes de trabajar para una marca |
| `memoria/` | Preferencias aprobadas e inbox de aprendizajes | Leer siempre |
| `conocimiento/` | Notas de apoyo | Opcional |

Antes de trabajar para una marca: leer `proyectos/INDICE.md` y su ficha. Aprendizajes nuevos → `memoria/inbox-aprendizajes.md`; promoverlos solo con aprobación explícita o repetición.

## Memoria, Obsidian y otras skills

- **Memoria primaria = el repo:** HANDOFF §4 (Registro de trabajos), `memoria/` y `proyectos/`. **Obsidian es una capa opcional**: solo si el usuario la tiene (`obsidian_vault` en `~/.gui-skills/config.json` o el MCP de Obsidian responde) se actualiza además la nota madre del proyecto (`obsidian_projects_folder`) y, si cambió la herramienta, la nota de registro de skills (`obsidian_registry_note`). Sin Obsidian, se salta.
- Accesos y publicación: el hosting temporal usa el acceso SSH por llave del usuario (variables `CANVA_TMP_*` o `~/.gui-skills/config.json`; ver `references/03`). Stock/IA: servidor Magnific/Freepik (`stock_search`, `stock_download`; revisar `account_balance`) o skill `freepik-imagegen`. Análisis de manuales: `scripts/pdf_pages.py`.
- Dirección de arte, tipografía, color y QA estratégico: `direct-visual-design` y sus referencias. Si el entregable termina en Illustrator: `design-illustrator`.

## Estado y portabilidad

**v1.1.0 (2026-10-09, núcleo; 1.1.2 solo cambia el ejemplo de serie).** Instalada en Claude Code por enlace desde el repo (`~/.claude/skills/canva-design`). Codex/Antigravity/VS Code: **no instalada ni verificada** (el conector Canva es de la sesión de Claude). Estado vivo y siguientes pasos: `HANDOFF.md` y `HANDSHAKE.md`.
