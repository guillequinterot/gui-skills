# HANDOFF — canva-design

> Traspaso entre sesiones y personas: qué es la skill, cómo se instala, qué se decidió y qué se aprendió
> en cada trabajo. Estado vivo (versión, herramientas, pendientes) → `HANDSHAKE.md`. Historial de cambios → `CHANGELOG.md`.

## 1. Qué es y cuándo se usa

Skill **propia** del mantenedor, **sub-skill de `direct-visual-design`** (la principal/orquestadora de diseño). Nace del caso `caso-diplomas-01`, donde pasar un diseño HTML a Canva dejó **todo editable y fiel** ("quedó muy bien"). Decisión del mantenedor (2026-10-09): cuando se pida algo de Canva, o se llame esta skill, **es obligatoria y con todo su proceso**; `direct-visual-design` la llama cuando el entregable vive en Canva (fila "Cualquier trabajo en Canva" de su tabla de enrutamiento y precondición en su regla 3). Si el entregable termina en Illustrator, la hermana es `design-illustrator`.

**Receta corta** (`references/01-pipeline-html-a-canva.md` es la receta completa): preflight → brief/formato (100 px/cm) → HTML Canva-ready + assets horneados + lint + render → **aprobación** → autorización de hosting temporal → `import-design-from-url` → `upload-asset-from-url` → `read-design` (transacción) → `edit-design` (`update_fill`, `insert_fill`, `insert_shape`, fixes) → `layer_element` → `commit` → (merge si el destino es un diseño existente) → `export-design` + `canva_verify.py` → `temp_host.sh cleanup` (404) → registro.

## 2. Instalación y dependencias

- Viene con el repo gui-skills (`tools/install.ps1` / `tools/install.sh`); no se copia a mano. El instalador enlaza `~/.claude/skills/canva-design` al clon. `scripts/install.py --check` detecta ese enlace y no copia nada.
- Dependencias externas:
  - Python 3.10+ con `pymupdf` (`fitz`), `pillow`, `numpy`, `scipy`; Chrome o Edge instalado (render headless del HTML; el navegador integrado del panel **no** sirve para QA de archivos locales).
  - Conector **Canva MCP** de la sesión (`import-design-from-url`, `upload-asset-from-url`, `read-design`, `edit-design`, `merge-designs`, `export-design`, `resolve-shortlink`, `copy-design`…). Son herramientas *deferred*: se cargan con `ToolSearch` (palabra `canva`) antes de usarlas. El id del servidor cambia según la cuenta.
  - Opcional: servidor Magnific/Freepik (`stock_search`, `stock_download`, `account_balance`) o la skill `freepik-imagegen` para stock/IA.
  - Para el hosting temporal: `ssh`, `tar`, `curl` y un hosting propio con SSL válido accesible por SSH con llave. Se configura **fuera del repo** con las variables `CANVA_TMP_HOST_KEY`, `CANVA_TMP_HOST`, `CANVA_TMP_PORT`, `CANVA_TMP_USER`, `CANVA_TMP_DOMAIN` o las claves `canva_tmp_*` de `~/.gui-skills/config.json`. Sin ellas `temp_host.sh` no sube nada.
- Carpeta de la skill:

| Ruta | Contenido |
|---|---|
| `SKILL.md`, `references/` (8), `scripts/` (11), `templates/` | Núcleo |
| `HANDOFF.md`, `HANDSHAKE.md`, `CHANGELOG.md` | Este estado |
| `ejemplos/caso-diplomas-01/` | README anónimo del caso modelo (especificación de capas, rondas, pendientes) + `scripts-originales/bake.py`, `streak.py` |
| `ejemplos/caso-piezas-universidad-01/` | Producción en serie: README, QA visual (checklist), notas del montaje en Canva y las herramientas genéricas del motor |
| `proyectos/` | `INDICE.md` + una ficha por caso (solo código) |
| `memoria/` | `preferencias-canva-aprobadas.md`, `inbox-aprendizajes.md` |
| `conocimiento/` | `README.md` (qué guardar aquí) |

- Los HTML, assets, logos, previews y exportaciones con marca de cliente **no** se suben al repo; viven en la carpeta del proyecto del usuario.

## 3. Decisiones vigentes

| Fecha | Decisión | Quién la aprobó | Por qué |
|---|---|---|---|
| 2026-10-09 | `canva-design` es OBLIGATORIA con todo su proceso ante cualquier trabajo en Canva; si el usuario pide Canva manda sobre otras skills secundarias | Guillermo Quintero | "Quedó muy bien": no se improvisa ni se acorta |
| 2026-10-08 | HTML primero (Canva-ready), aprobación, luego Canva; nunca construir por API a ciegas (sin control de fuente/espaciado) | Guillermo Quintero | El importador conserva texto, fuente, tamaño, peso, color, interletraje y posiciones al píxel |
| 2026-10-08 | Autorización de hosting temporal **por tarea**; subir lo mínimo; borrar y comprobar 404 | Guillermo Quintero | Es publicar contenido en internet |
| 2026-10-08 | Texto del cliente literal; incoherencias señaladas, no corregidas | Guillermo Quintero | Evitar "arreglar" lo que no se debe |
| 2026-10-08 | Medidas en cm reales mandan (100 px/cm); tipografía re-escalada a medida física; márgenes ≥ 5 mm | Guillermo Quintero | Ronda 4 de `caso-diplomas-01` |
| 2026-10-08 | Mostrar varias opciones (3) antes de producir el lote; stock vía Magnific (revisar saldo) | Guillermo Quintero | Rondas 1–5 de `caso-diplomas-01` |
| 2026-10-08 | Paleta tonal de rojos aprobada para `caso-diplomas-01` (solo ese caso, no regla general) | Equipo del cliente vía el mantenedor | Idea de una colega del cliente |
| 2026-10-09 | La fuente de marca no se aplica al importar: cambio de fuente **en bloque** en Canva tras importar → una sola familia y solo Regular/Bold/Italic | Guillermo Quintero | Verificado en `caso-piezas-universidad-01` |
| 2026-10-09 | Series grandes: motor de diseño + config por programa, aprobar UN programa de prueba, HTML de toda la serie primero, luego imágenes, luego montaje en Canva por tandas | Guillermo Quintero | `caso-piezas-universidad-01` ("super genial") |
| 2026-10-09 | Probar merges y ediciones en una COPIA (`copy-design`); los diseños intermedios que crea la importación no se pueden borrar con las herramientas: avisar | Guillermo Quintero | Límites del conector |
| 2026-10-16 | Memoria primaria en el repo; Obsidian opcional; hosting temporal configurable (sin datos del mantenedor en los scripts) | Guillermo Quintero | Poder compartir la skill |

Verificación por exportación: diferencia media HTML↔Canva de referencia 8–10 (zona de texto ~32 mientras la fuente sea el fallback).

## 4. Registro de trabajos

> Una entrada por trabajo terminado o implementado y aprobado. Solo se agregan entradas al final; las
> correcciones van como entrada nueva. Casos solo con código `caso-<tipo>-<NN>`. Formato:
> `templates/entrada-de-trabajo.md`. Se escribe con `tools/log_job.py`.

<!-- registro:inicio -->
### 2026-10-08 · caso-diplomas-01 · guille

- **Qué se hizo:** Ronda v1 de diplomas para el personal de una empresa: 3 opciones HTML a 1920 × 1080 (lienzo blanco con trazos de pincel, placa negra, panel pintado), importadas a Canva desde HTML con texto 100 % editable y assets (logos, trazos, panel de pincel, fondos) subidos aparte y colocados con la API; las 3 páginas se insertaron en el diseño de destino del usuario.
- **Salió bien:** El importador de HTML conservó texto real, fuente, tamaño, interletraje y posiciones; verificación por exportación PNG contra el render del HTML con diferencia media 8–10; el hosting temporal se borró y devolvió 404.
- **Salió mal / incidencia:** El importador no trae las imágenes (`<img>` ni fondos CSS) y desplaza el numeral grande ~0,1 em hacia abajo; lo insertado entra en primer plano y tapó el texto (hubo que ordenar capas); un marco redondeado se importó como 4 líneas; el panel del navegador no renderiza archivos locales (se usó Chrome headless). El texto del cliente tenía una incoherencia (11 vs 8 años) y se dejó literal, señalada.
- **Regla candidata:** Si el cliente aporta tonos de color vía un colega, tratarlo como input del usuario, no de la marca.
- **Herramientas:** Canva MCP (import, upload-asset, edit-design, merge-designs, export-design), Chrome headless, PyMuPDF, hosting SSH temporal

### 2026-10-08 · caso-diplomas-01 · guille

- **Qué se hizo:** Ronda v2: los diplomas se rehicieron a medida física 20 × 14 cm (2000 × 1400 px a 100 px/cm) con una sola firma, logo arriba y tres opciones nuevas (pincelada tonal, mármol y vino, triángulos tonales) sobre una paleta tonal de rojos; se montaron en un diseño nuevo de Canva con el mismo pipeline.
- **Salió bien:** La tipografía re-escalada para impresión (cuerpo ≥ 28 px) y los assets horneados con `bake_assets.py` (6 de 7 idénticos byte a byte a los reales); compensar el numeral (−0,1 em) y ensanchar la caja de "Y Color" evitó los defectos de v1.
- **Salió mal / incidencia:** El diseño existente era de otro tamaño (1920 × 1080), así que hubo que crear un diseño nuevo en vez de insertar; una pincelada con cerdas verticales largas parecía sangre y se rehízo con arrastre horizontal; quedó pendiente elegir D/E/F, el nombre del firmante, la fecha y resolver 11 vs 8 años.
- **Regla candidata:** Pedir la medida física real antes de diseñar y reescalar la tipografía a esa medida (cuerpo ≥ 28 px a 100 px/cm).
- **Herramientas:** Canva MCP, `bake_assets.py`, `lint_html_for_canva.py`, `canva_verify.py`, Magnific stock (id de textura y de pintura fluida registrados)

### 2026-10-09 · caso-piezas-universidad-01 · guille

- **Qué se hizo:** Serie de 36 programas × 2 diseños × 3 formatos (post 1080², historia 1080 × 1920, banner 1200 × 628) para anuncios de un centro de educación continua: un motor de diseño con config por programa, un programa de prueba aprobado, y un montaje real de ese programa en una **copia** del Canva del usuario (importación de HTML con páginas de tamaños mixtos, `update_fill` + `crop_media`, `merge-designs` insert → move → delete, exportación y comparación).
- **Salió bien:** Un solo HTML con páginas de tamaños distintos importa como un diseño de tamaños mixtos; el truco de sustituir `<img>` por rectángulos grises evita `layer_element`; el título de página sale del `data-label`; fidelidad verificada por exportación (diferencia media 7–9 salvo el texto); el usuario calificó el resultado del programa de prueba de "super genial".
- **Salió mal / incidencia:** El importador no aplica la fuente institucional del Brand Kit (15 nombres probados, todos caen en un fallback tipo Arial, más ancho: saltos de línea distintos y un titular de 6 líneas que pisa el párrafo); `merge-designs` solo admite una operación por llamada e invierte el orden con `after_page_number` (se arregla con `move_pages`); `edit-design` no renombra páginas; `temp_host.sh` subía una carpeta vacía con varios archivos (corregido en v1.1.0); 4 diseños intermedios que la API no puede borrar quedaron en la cuenta.
- **Regla candidata:** Para series grandes, construir primero un motor y aprobar UN programa antes de escalar; preguntar siempre cómo se resuelve la fuente de marca antes de montar en serie.
- **Herramientas:** Canva MCP, `prepare_multipage_import.py`, `temp_host.sh`, `canva_verify.py`, motor de diseño en Python (PIL), Chrome headless

### 2026-10-09 · caso-piezas-universidad-01 · guille

- **Qué se hizo:** Fase 2 de imágenes de la serie: se colocaron fotos de stock de Magnific en el diseño 2 de 34 programas (convención `assets/img-c2-fondo.jpg`, recorte de la foto a la franja visible en layouts `split`, foco opcional por formato), y se renderizaron y miraron los 34 diseños.
- **Salió bien:** 34 diseños 2 renderizados y revisados, 100 HTML con lint 0 errores y `qa_copy_check.py` sin diferencias nuevas; el flujo de selección (búsquedas gratis → hoja de contacto de 3–4 candidatos por pieza → elegir por vista previa → descargar solo la elegida → colocar con foco → mirar los 3 formatos) funcionó.
- **Salió mal / incidencia:** En layouts `split` el motor recortaba la foto para toda la página y el panel tapaba ~60 %, perdiendo al sujeto (se añadió `strip_fit`); un script de Python que lanzaba `bash` resolvió el de WSL y falló en silencio, de modo que se revisaron previews viejas; cada descarga de stock cuesta créditos y el stock genérico no sirve para escenas con gente local.
- **Regla candidata:** Comprobar el código de salida y la fecha de las previews tras cada render; avisar del coste antes de descargar stock.
- **Herramientas:** Magnific MCP (`stock_search`, `stock_download`), motor de diseño en Python, Git Bash, Chrome headless

### 2026-10-24 · caso-carrusel-01 · guille

- **Qué se hizo:** Carrusel de redes 1080x1350 en 2 versiones (3 y 6 láminas) con texto largo del cliente: HTML Canva-ready con generador en Python, estilo gris claro con cuadrícula, stickers de manos en B/N con trama de puntos (fotos de stock recortadas con OpenCV), importación por flujo B (marcadores grises + update_fill + crop_media), export y verificación (diferencia media 9-14).
- **Salió bien:** El flujo B funcionó a la primera con 3 y 6 páginas; píldoras y tarjetas redondeadas como SVG inline se importan como imágenes y mantienen el texto editable encima; update_fill + crop_media sirve también para PNG que sobresalen de la página; hosting temporal borrado justo tras importar (404).
- **Salió mal / incidencia:** Brote en mano de stock descartado por mal recorte (tierra oscura); una línea de texto con serif incrustada en una línea sans se partió en Canva. Incidencia: prepare_multipage_import.py exige tamaño inline en el div de página y left/top con unidad px (left:0 no se lee) o falla con TypeError; cajas de texto más anchas que la página hacen que Canva parta la línea: bajar el ancho a <= 960 con resize_element.
- **Regla candidata:** Al generar el HTML para flujo B escribir siempre style=width/height en la página y left:0px/top:0px en los img; limitar el ancho de cada caja de texto a (1080 - margen) aunque el 1,15x la desborde.
- **Herramientas:** Canva MCP (import-design-from-url, edit-design, export-design), Magnific stock, OpenCV, PIL, Chrome headless

<!-- registro:fin -->

## 5. Reglas candidatas (sin aprobar)

Estas viven en `memoria/inbox-aprendizajes.md` (candidatas, sin promover); se promueven a `memoria/preferencias-canva-aprobadas.md` con aprobación del mantenedor o al repetirse en otro caso.

| Regla | Visto en (casos) | Estado |
|---|---|---|
| Los colegas del cliente aportan feedback de estilo que el usuario traslada: tratarlo como input del usuario, no de la marca | `caso-diplomas-01` | Candidata |
| Canva coloca el numeral grande ~0,1 em más abajo: subir de heurística a regla en `references/02` si se repite con otras fuentes | `caso-diplomas-01` (medido solo con Montserrat ExtraBold) | Candidata |
| Series grandes: construir un motor y aprobar UN programa antes de escalar | `caso-piezas-universidad-01` | Candidata |
| Series: todos los HTML primero, luego imágenes, luego montaje en Canva al final | `caso-piezas-universidad-01` | Candidata |
| Preguntar siempre cómo resolver la fuente de marca antes de montar en serie | `caso-piezas-universidad-01` | Candidata (ya reflejada en `references/08`) |
| La pieza lleva solo el texto del brief/copy; nada de elementos de referencias antiguas | `caso-piezas-universidad-01` | Candidata |
| En layouts split, recortar la foto a la franja visible y mirar el render por formato | `caso-piezas-universidad-01` | Candidata |
| Stock: avisar del costo en créditos; ofrecer recorte de persona antes de recurrir a IA generativa | `caso-piezas-universidad-01` | Candidata |
| Comprobar código de salida y fecha de las previews tras cada render | `caso-piezas-universidad-01` | Candidata |
| Al generar el HTML para flujo B escribir siempre style=width/height en la página y left:0px/top:0px en los img; limitar el ancho de cada caja de texto a (1080 - margen) aunque el 1,15x la desborde. | caso-carrusel-01 | candidata |

## 6. Anexos heredados

### Integración con `direct-visual-design` (hecha el 2026-10-09)

Fila "Cualquier trabajo en Canva → `canva-design`" en la tabla (ii) "Ejecución con herramienta" y precondición en la regla 3 de su sección de skills secundarias. La copia de Codex de `direct-visual-design` no se tocó (queda sin la fila). La sección "Canva design" del `CLAUDE.md` global del mantenedor refuerza la regla.

### Estado de los dos casos que originaron la skill

- `caso-diplomas-01`: dos diseños en la cuenta de Canva del usuario (v1 1920 × 1080, v2 20 × 14 cm). Pendientes del cliente: elegir D/E/F (y borrar las otras páginas), nombre del firmante, 11 vs 8 años, fecha, versión para otro país. Ficha: `proyectos/caso-diplomas-01.md`.
- `caso-piezas-universidad-01`: programa de prueba montado en una copia; fase actual = HTML → imágenes → montaje por tandas. Ficha: `proyectos/caso-piezas-universidad-01.md`; notas completas del montaje: `ejemplos/caso-piezas-universidad-01/herramientas/MONTAJE-CANVA-notas.md`.

### Pendientes de la skill

Ver `HANDSHAKE.md` ("Pendientes abiertos" y "Límites conocidos").

### Dónde mirar

- Receta: `references/01-pipeline-html-a-canva.md` · límites del conector: `references/02-...` · caso: `references/07-caso-diplomas-01.md` · serie y fuente de marca: `references/08-...`.
- Si el usuario usa Obsidian (`obsidian_vault`), su nota del proyecto y el registro de skills (`obsidian_registry_note`) son una capa extra; no son necesarias para usar la skill.
