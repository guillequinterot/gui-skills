# 06 · QA y verificación (antes de dar un trabajo en Canva por terminado)

Orden del QA de `direct-visual-design` (estratégico → contenido → visual → accesible → técnico → fidelidad) más los controles propios de Canva. **Mirar siempre las imágenes** (no basta con que el comando no falle).

## A · QA local (HTML, antes de montar)

- [ ] `lint_html_for_canva.py` → 0 ERROR (revisar AVISOS).
- [ ] Render con Chrome headless (`render_html.sh` + `split_pages.py`) — **visto** a tamaño completo y recortes de esquinas/zonas densas.
- [ ] Texto literal (comparar con el que dio el usuario); incoherencias señaladas en el mensaje, no corregidas.
- [ ] Jerarquía: un héroe (numeral/nombre), un nivel de apoyo, cuerpo; sin competencia entre el logo y el título.
- [ ] Escala de impresión y márgenes (`04`); ningún texto < 19 px; cuerpo ≥ 28 px.
- [ ] Contraste de cada par texto/fondo (ratios en `04`); coral solo sobre oscuro.
- [ ] Citas partidas mal ("trazo / a trazo"): usar `&nbsp;`; viudas/huérfanos de una palabra: ajustar ancho.
- [ ] Logo en la versión correcta para el fondo (plano vs contorno blanco); área de reserva respetada.
- [ ] Marcadores de lo que falta ("Nombre Apellido", fecha) y lista de pendientes.
- [ ] El usuario **aprobó** (o eligió) el HTML.

## B · QA en Canva (después de montar)

1. `export-design` png (ancho/alto exactos) → `canva_verify.py download` → **leer cada PNG**.
2. `canva_verify.py compare html_pag.png canva_pag.png` → referencia 8–10; > 15 ⇒ mirar qué capa falta o se movió.
3. Revisar en la exportación: ¿está el fondo? ¿ornamentos **detrás** del texto? ¿logo delante? ¿numeral separado del título? ¿"Y Color" en una línea? ¿marco con esquinas redondeadas? ¿subrayado de pincel visible?
4. `read-design` (sin transacción) → fuentes (`fontRef`) y tamaños de los textos clave = los del HTML (menos el ajuste de posición del numeral).
5. Dimensiones de página = formato pedido (`page_metadata`).
6. Editabilidad: los textos son `type:"text"` (no imagen); fondo/ornamentos/logos son `rect` con relleno de imagen reemplazable.

## C · Cierre

- [ ] Hosting temporal borrado y verificado (404).
- [ ] Lista de diseños intermedios que quedan en la cuenta del usuario.
- [ ] Nota de proyecto, HANDOFF del proyecto y (si procede) registro de herramienta actualizados.
- [ ] Resumen al usuario: enlace, qué se puede editar, ajustes hechos, pendientes y lo que **no** se verificó.

## C2 · QA con tamaños mixtos y fuente de marca no aplicada
- Exportar sin `width/height` (tamaño nativo por página) y comparar con los previews del HTML. Referencia `caso-piezas-universidad-01`: diferencia media 7–9 global; zonas sin texto 2–5; **zona de texto ~32 mientras la fuente sea el fallback** (esperado, no es un fallo de montaje).
- Mirar a ojo: saltos de línea, titulares largos (historia con 6 líneas), chips, botón, capas (persona detrás del texto / delante del panel), logo.
- Reportar con franqueza qué no coincide y qué no se verificó (p. ej. edición manual posterior, plantillas con cuadros en fuente de marca).

## D · Fallos típicos y causa

| Síntoma | Causa | Arreglo |
|---|---|---|
| Fondo blanco/negro liso, sin imágenes | El importador no carga `<img>` | Subir assets + `update_fill`/`insert_fill` |
| Pincelada tapa el texto | Insertado en primer plano | `layer_element back` (ornamento primero, fondo último) |
| Ornamento desaparece | Se mandó al fondo antes que el rect de fondo | Mandar el rect de fondo al fondo **al final** |
| Subtítulo en minúsculas / partido | `text-transform` con hijos; ancho justo | `find_and_replace_text`, `resize_element` |
| "11" pisa el título | Offset ~0,1 em de Canva | `position_element` top −0,1·font-size |
| Marco sin esquinas redondeadas / 4 líneas | `border` importado como rects | Borrar 4 rects + `insert_shape` path con arcos |
| Coincide en HTML pero el texto se ve diminuto impreso | Escala de pantalla en pieza física | Reescalar tipografía (`04`) |
