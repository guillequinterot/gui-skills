# 06 · Caso modelo: `caso-manual-marca-01` — manual de marca de 46 láminas (2026-10-10/11)

Proyecto: carpeta del proyecto del usuario, fuera del repo (HTML 1920 × 1080, una lámina por archivo, solo Poppins). Resultado entregado: `export/illustrator/<maestro>.ai` (46 mesas de trabajo) + `.pdf` + `pdf/pNN.pdf`. Si el usuario usa Obsidian, la nota del proyecto vive en su vault.

## Cronología y decisiones

1. **PDF de Chromium** (`export_pdf.py`, escala 4/3 → 1920 × 1080 pt, 0 raster, Poppins incrustada). *El usuario lo abrió en Illustrator: «cada letra quedó por separado».* Medido: 489 textos en una lámina.
2. **Agrupar por línea** (`aiFixText`): 489 → 25 textos; tracking calculado (3 px → 214; −1 px a 56 px → −18). Fidelidad 396 px de 2,07 M. *Usuario: «mucho mejor, pero los textos no quedaron corridos».*
3. **Párrafos en texto de área** (`extract_paragraphs.py` + `aiMergeParagraphs`): 3 de 8 párrafos de la lámina 4 no coincidían → causa: **separación silábica** de Illustrator → desactivada → 8/8.
4. **Maestro de 46 mesas de trabajo** con pegado: rejilla de 6 columnas (error `AOoC` al principio por el lienzo de 16 383 pt → rejilla desplazada). La lámina 19 salió en blanco (pegado) y la 33 dio `CANT` → `ai_repair_page.ps1`.
5. **Illustrator Beta se cerró solo** una vez (RPC `0x800706BE`) y el documento del usuario se perdió; al reabrir, «[Recuperado]». Desde entonces el proceso **no cierra documentos** y se avisa de guardar.
6. **Tamaño automático:** sin API → clic automatizado en el cuadro (230 textos de área; las 230 cajas se ajustaron; el `.ai` se guardó).
7. **Recortes:** 427 máscaras → 394 sin efecto (soltadas y borrado su trazado), 28 + 3 vacías (borradas), 5 necesarias en la lámina 41: el **asa de la bolsa** (borde redondeado recortado en 3 trozos) → redibujada como **un arco abierto** (100 × 48, trazo oliva 1 pt). Resultado: 0 recortes, 0 invisibles, 0 grupos vacíos; las 46 láminas idénticas al original. Backup previo en `backups/`.
8. **MCP de Illustrator**: registrado en Claude el 2026-10-11; el servidor no respondió en ninguna prueba.

## Cifras de referencia

| Qué | Valor |
|---|---|
| Láminas / mesas de trabajo | 46 (1920 × 1080 pt, rejilla 6 columnas, separación 200) |
| Textos finales | 1 028 (798 de punto, 230 de área, 0 vacíos, 0 desbordados) |
| Fuentes | Poppins-Light 186 · Regular 371 · Medium 463 · SemiBold 8 |
| Letras sueltas iniciales → textos | p. ej. 489 → 25 (lámina 22); 937 → 34 (lámina 4) |
| Fidelidad | peor lámina 4 697 px de 2 073 600; 0 diferencias de caracteres |
| Recortes | 427 → 0 |
| Duración del proceso completo | ~15 min (más 10 min si hay que repetir láminas) |

## Qué mejorar la próxima vez

- Generar la lámina del **asa** (o cualquier arco) como **SVG** en el HTML para que no nazca un recorte (ver [03](03-html-illustrator-ready.md)).
- Regenerar los **PDF por lámina y el maestro** desde el `.ai` final (o ejecutar `ai_autosize_text.ps1` + limpieza *antes* de guardar los PDF) para que no queden versiones con recortes.
- Pasar también las **piezas** (flyers A5, plantillas de redes) por el proceso: en `caso-manual-marca-01` `export/piezas/*.pdf` siguen con letras sueltas y recortes.
- Probar el MCP de Illustrator cuando responda para evitar el clic de interfaz.

## Herramientas originales de la sesión

Copias en `ejemplos/caso-manual-marca-01/herramientas/` (sondeos de propiedades, de nombres de comandos de menú, de clics en el cuadro, auditorías de recortes). Las versiones generales y mantenidas son las de `scripts/`.
