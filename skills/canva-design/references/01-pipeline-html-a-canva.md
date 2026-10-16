# 01 · Pipeline HTML → Canva (proceso OBLIGATORIO)

Este es el proceso que dio el resultado del caso `caso-diplomas-01` (diplomas): texto 100 % editable en Canva, fuentes y espaciados correctos, capas ordenadas y exportación visualmente idéntica al diseño HTML aprobado. **No se salta ninguna fase.** Si una fase no aplica (p. ej. no hay assets), se dice y se anota por qué.

Rutas: scripts en `scripts/` (usar `python -I`), plantilla en `templates/`, resumen del caso real en `ejemplos/caso-diplomas-01/` (los archivos con la marca del cliente no están en el repo).

## Fase 0 · Preflight (2 min)

1. `python -I scripts/handshake.py` → librerías, Chrome, llave SSH, skill instalada.
2. **Cargar las herramientas Canva** (son *deferred*): `ToolSearch select:` con `import-design-from-url`, `upload-asset-from-url`, `read-design`, `edit-design`, `merge-designs`, `export-design`, `resolve-shortlink` (lista exacta en `scripts/handshake.py`). Si no aparecen: ToolSearch con la palabra `canva`.
3. Leer contexto: la nota del proyecto (en el vault de Obsidian del usuario, si lo usa), la memoria de marca (`direct-visual-design/proyectos/INDICE.md`) y `proyectos/` de esta skill.
4. Si el usuario dio **enlaces de Canva** (`canva.link/...`): `resolve-shortlink` → `read-design` (miniaturas + texto) para entender el estilo y para saber si el destino está vacío. Un destino vacío y de otro tamaño ⇒ se crea uno nuevo por importación (ver Fase 3).
5. `direct-visual-design` ya clasificó el brief (gráfico/UI/híbrido) y fijó dirección; esta skill **ejecuta** en Canva. Si se invocó sola, aplicar igualmente sus principios (referencias → mantener/adaptar/evitar; QA estratégico→técnico).

## Fase 1 · Brief y formato

- **Formato real primero.** Medida física → px a **100 px/cm** (20×14 cm = 2000×1400). Pantalla: el tamaño de Canva del diseño destino. Preguntar/confirmar si cambia el formato de un trabajo ya aprobado: es otro diseño.
- **Texto literal.** Se usa tal cual lo da el usuario. Las incoherencias (p. ej. "11 años" vs "8 años", falta de nexo) se **señalan, no se corrigen**; se dejan literales y se piden decisiones.
- Lo que falta (firmantes, fecha, país) → marcadores claros ("Nombre Apellido") y lista de pendientes. No inventar contenido.
- Referencias: descomponer qué se mantiene / adapta / evita (principio de `direct-visual-design`). Las referencias dan estructura, no se copian.

## Fase 2 · Diseñar en HTML (nunca directo en Canva)

1. Partir de `templates/diploma-20x14.template.html` (la especificación de capas del caso modelo está en `ejemplos/caso-diplomas-01/README.md`).
2. **Reglas Canva-ready** (resumen; detalle y por qué en `02`): una página = `div.page[data-document-role=page]` de tamaño fijo; todo capa absoluta con `data-layer`; sin transform/gradiente/background:url/box-shadow/flex; centrar con `left` explícito; texto real; solo Montserrat/Playfair Display u otras nativas de Canva; escala de impresión (`04`).
3. **Assets** que Canva no puede importar (pinceladas, mármol, fondos con degradé, triángulos, texturas) → `scripts/bake_assets.py` (ver `05`) o stock (Magnific/Freepik MCP; verificar saldo y revisar a ojo si es IA). Logo: del `.ai` oficial con `bake_assets.py logo` (artboard plano para fondos claros, con contorno blanco para fondos oscuros/rojos).
4. `python -I scripts/lint_html_for_canva.py <html> --w W --h H` → **0 ERROR** antes de seguir.
5. Render: `bash scripts/render_html.sh <html> W H_total out.png` + `python -I scripts/split_pages.py ...`. **Mirar la imagen.** Iterar hasta que pase el QA local (`06`).
6. **Mostrar previews al usuario y esperar aprobación** (o su elección entre opciones). Sin aprobación no se monta en Canva.

## Fase 3 · Montaje en Canva

### 3.1 Hosting temporal (el importador pide URL pública)
- **Pedir autorización explícita al usuario para ESTA tarea** (qué se sube, a qué dominio, que se borrará). Una autorización anterior no vale.
- `bash scripts/temp_host.sh upload <slug> <carpeta> <html> <assets...>` → devuelve `DIR` y la URL base (v1.1: ya sube **varios** archivos; las TTF no hace falta subirlas). `verify` → 200 en el HTML y en cada asset.

### 3.2 Importar el HTML → diseño nuevo
`import-design-from-url` (`url`, `name`, `intended_design_type: "other"`). El diseño resultante hereda el tamaño de la página HTML (`custom`, p. ej. 2000×1400) y un nº de páginas = nº de `data-document-role=page`. Es el **diseño final** salvo que el usuario exija meterlo en uno suyo existente (3.8).
Qué se conserva: texto como texto real, fuente (fontRef), tamaño, peso, cursiva, color, `letter-spacing`, alineación, interlineado, regiones de estilo mixto, posiciones al píxel, rectángulos/líneas, SVG inline (como imagen reemplazable).
Qué NO: `<img>` y fondos CSS (no se descargan), `text-transform` con hijos de otro estilo, `border` (4 rectángulos finos), gradientes, sombras.

### 3.3 Subir los assets a la biblioteca de Canva
`upload-asset-from-url` por cada archivo (JPG/PNG/**SVG** valen). Guardar los `asset id` (`MAHX…`). Los logos ya subidos se reutilizan (ids en `proyectos/caso-diplomas-01.md`).

### 3.4 Leer ids
`read-design` con `open_transaction: true`, `filter.fields: ["design_content"]`, `page_indices: [1,2,3]` → `transaction_id` + `locator_id` = `PAGEID-ELEMENTID` de cada elemento. **Los ids cambian tras un `merge-designs`**: releer.

### 3.5 Editar cada página (`edit-design`, `finalize: keep_open`, una llamada por página)
Orden recomendado de operaciones:
1. `update_fill` sobre el **primer rect de página completa** (es el `background` del `.page`) con el asset de fondo → conserva z-order al fondo y deja un sangrado de ~20 px.
2. `delete_element` de los 4 rectángulos de un marco/borde + `insert_shape` con `path` (solo M/L/H/V/C/S/A/Z; sin Q/T), `stroke_color`/`stroke_weight`, sin `color` ⇒ sin relleno.
3. `insert_fill` de cada ornamento/imagen/logo con `left/top/width/height` **exactos del HTML** (alto = ancho × proporción real del archivo).
4. Correcciones de texto: `find_and_replace_text` (conserva regiones), `format_text` (aplica a TODO el cuadro: solo tamaño/color global), `resize_element` (ancho) para que "Y Color" no se parta, `position_element`.
5. **Compensar el numeral grande**: Canva lo coloca ~0,1 em más abajo que el navegador → `top − 0,1·font-size`.
6. Tras cada llamada: **comparar la miniatura devuelta** y el `document` (`edits_unverified` obliga a mirar).

### 3.6 Orden de capas (segunda llamada por página)
Lo insertado queda **encima** de todo. `layer_element back` en cada ornamento (los que van detrás del texto) y **al final** `layer_element back` del rect de fondo (si no, los ornamentos quedan detrás del fondo y desaparecen). Los logos y marcos delante del texto no se tocan.

### 3.7 Título y commit
`update_title` (nombre claro con medida/versión) → `finalize: commit` (sin operaciones en la misma llamada).

### 3.8 Si el destino es un diseño existente del usuario
`merge-designs` `modify_existing_design`: **una operación por llamada** (`insert_pages` y luego `delete_pages` de la página en blanco), cada una con aprobación explícita de las operaciones exactas. Un diseño `presentation` se puede insertar en uno `custom` del mismo tamaño. Si el tamaño difiere (p. ej. 1920×1080 vs 2000×1400) → diseño nuevo.

### 3.9 Exportar y verificar (obligatorio)
`export-design` png con `width/height` exactos → `canva_verify.py download` → **leer cada imagen** y compararla con el render HTML (`06`). Corregir (nueva transacción) y volver a exportar hasta que coincida.

### 3.10 Limpieza
`temp_host.sh cleanup <DIR>` → comprobar **404**. Informar al usuario. Los diseños intermedios creados en su cuenta no se pueden borrar con las herramientas: listarlos y decírselo.

### 3.11 Variante multipieza (varios formatos o programas)
Cuando son muchas piezas o de tamaños distintos (posts + historias + banners): seguir `references/08-montaje-multipieza-y-fuentes.md` — un HTML por programa con las páginas en orden, `scripts/prepare_multipage_import.py` (marcadores en vez de `<img>`), un `edit-design` por página con `update_fill`+`crop_media`, `merge-designs` (insert → move → delete) **sobre una copia**, y **antes decidir con el usuario la fuente de marca** (el importador no la aplica).

## Fase 4 · Registro y entrega

- Registrar el trabajo con el Paso final del protocolo gui-skills (entrada en el Registro de trabajos del `HANDOFF.md` de la skill, con `tools/log_job.py`). Si el usuario usa Obsidian: nota del proyecto (decisiones, enlaces de Canva, pendientes, próxima acción) y, si se aprendió algo de la herramienta, el registro de skills (`obsidian_registry_note`).
- `HANDOFF` del proyecto (en la carpeta del proyecto del usuario) actualizado: `ejemplos/caso-diplomas-01/README.md` muestra el modelo de especificación de capas, rondas y pendientes.
- Respuesta al usuario: enlace del diseño, qué es editable, qué se ajustó, qué queda pendiente, qué se borró del servidor, qué queda en su cuenta. Sin vender lo que no se verificó.
- Aprendizajes nuevos → `memoria/inbox-aprendizajes.md`; promover solo con aprobación o repetición.
