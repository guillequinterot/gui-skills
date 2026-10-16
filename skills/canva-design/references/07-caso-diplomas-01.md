# 07 · Caso de referencia: `caso-diplomas-01` — diplomas para el personal de una empresa (2026-10-08/09)

Caso que originó la skill. Sirve de modelo de **proceso, decisiones y resultado**. Resumen y especificación de capas en `ejemplos/caso-diplomas-01/README.md`; los archivos con la marca del cliente (HTML, assets, logos, exportaciones) no están en el repo.

## Encargo

Diplomas de "11 años de trayectoria" para el personal de una empresa de materiales para arte y manualidades (marca rojo/negro/blanco, Montserrat + una serif propia de la marca). Primero 1920×1080 horizontal "en HTML pero pensado para pasar a Canva y que sea editable"; luego medida física **20×14 cm** (marco). Referencia del cliente: diploma vertical con esquinas de ágata azul y dorado.

## Línea gráfica deducida (fuentes: manual de marca, premios 2026, brochure, calendario 2027, 6 Canva, web, Instagram)

- Rojo `#DA111C` + negro + blanco; Montserrat (principal) y una serif propia de la marca → **Playfair Display** en Canva (la serif que ya usan sus posts).
- Trazos de pincel rojos diagonales (portada y cierre del brochure), manchas de pincel con bordes deshilachados como etiqueta de titulares (Canva), tarjetas redondeadas, "11 AÑOS" como lockup de la placa acrílica de premios.
- Tono: cálido, orgulloso, metáforas de pintura ("trazo a trazo", "lienzo").

## Rondas y decisiones

| Ronda | Pedido del usuario | Decisión / resultado |
|---|---|---|
| 1 | 1 diploma HTML 1920×1080, texto dado, "usa Magnific si necesitas fondo/pattern (stock)" | Opción A "Lienzo blanco": numeral "11" + título, trazos de pincel del brochure (vector extraído del PDF con PyMuPDF, borde de página desvanecido con ruido alargado), nombre en Playfair cursiva, textura de lienzo (stock 1273386). HANDOFF + HANDSHAKE de proyecto. |
| 2 | "2 opciones más" | B "Placa negra" (eco de la placa de premios) y C "Panel pintado" (panel rojo con borde de pincel seco horneado). Logo con contorno blanco para fondos oscuros/rojos. |
| 3 | "Pasa las 3 al Canva que te envié, todo editable; busca la mejor opción" | Elegido: **import HTML**. Autorización de hosting temporal → import → assets → insert_fill/layer → fixes → merge en el diseño del usuario (1 op por llamada) → export + verificación → borrado del servidor. |
| 4 | Medida 14×20 cm, una firma (Director Gerente), logo arriba, más referencias, "tonos de rojo (vino/profundo/vivo)" de una colega | v2 en 2000×1400: D Pincelada tonal, E Mármol y vino, F Triángulos tonales. Tipografía re-escalada para impresión (cuerpo ≥ 28 px). Paleta tonal vino/profundo/marca/vivo/coral. |
| 5 | "Monta esos 3 en Canva" | Mismo pipeline en diseño **nuevo** 2000×1400 (el existente era 1920×1080). Compensación del "11" (−0,1 em), "Y Color" ensanchado, orden de capas. Exportación = HTML (dif. media 8–10). |
| 6 | "Crea una skill con todo esto" | Esta skill. |

## Resultado

- v1 (1920×1080, opciones A/B/C) y v2 (2000×1400, opciones D/E/F): dos diseños en la cuenta de Canva del usuario (enlaces e ids en su nota de proyecto, no en el repo).
- Un diseño intermedio de la importación v1 quedó en la cuenta («…3 opciones (import HTML)»).
- Texto 100 % editable; fondo/ornamentos/logo = capas de imagen; subrayado = SVG reemplazable; marco = forma vectorial.

## Qué salió mal y cómo se arregló (para no repetirlo)

1. Imágenes ausentes tras importar → subir assets + `insert_fill`.
2. Ornamentos tapaban texto → `layer_element back` en el orden correcto.
3. Subtítulo en minúsculas y partido → `find_and_replace_text`, `format_text`, ancho mayor.
4. "11" pisaba el título en Canva → −0,1 em.
5. Marco redondeado importado como 4 líneas → `insert_shape` con path.
6. Texto minúsculo en impresión → escala física (`04`).
7. Pincelada "de sangre" (cerdas verticales largas) → rehecha con arrastre horizontal y borde de cerdas paralelas.
8. Panel del navegador no renderiza archivos locales → Chrome headless.
9. Incoherencias del texto del cliente (11 vs 8 años; falta de nexo) → señaladas, no corregidas; pendientes de su decisión.

## Pendientes del proyecto (a 2026-10-09)

Elegir D/E/F · nombre del Director Gerente · 11 vs 8 años · fecha · versión para otro país. Estado vivo: `ejemplos/caso-diplomas-01/README.md` y, si el usuario usa Obsidian, la nota del proyecto de su vault.
