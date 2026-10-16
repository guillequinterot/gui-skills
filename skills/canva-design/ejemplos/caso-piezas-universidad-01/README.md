# Ejemplo: `caso-piezas-universidad-01` — producción en serie (2026-10-09)

Caso: 36 programas × 2 diseños (c1/c2) × 3 formatos (Post 1080², Historia 1080×1920, Banner 1200×628) para anuncios de un centro de educación continua. El estado vivo del proyecto y su HANDOFF viven en la carpeta del proyecto del usuario (fuera del repo); decisiones y reglas aprendidas están en [`../../proyectos/caso-piezas-universidad-01.md`](../../proyectos/caso-piezas-universidad-01.md) y [`../../references/08-montaje-multipieza-y-fuentes.md`](../../references/08-montaje-multipieza-y-fuentes.md).

## Qué hay aquí

| Archivo | Para qué |
|---|---|
| `herramientas/motor_series.py` | Motor: parsea el copy de la hoja, mide con las TTF reales de la fuente de marca, fluye la columna sin solapes, hornea fondos (foto + scrim) y emite HTML Canva-ready. Convención de imágenes por diseño: `assets/img-c1-fondo.jpg`, `img-c2-fondo.jpg`, `img-c1-persona.png`, `img-c2-persona.png` |
| `herramientas/normalize_weights.py` | Regla tipográfica de la serie: una sola familia y solo Regular / Bold / Italic (para el cambio de fuente en bloque de Canva) |
| `herramientas/make_sheet.py` | Hoja resumen de un programa (`previews/00-resumen.jpg`) |
| `herramientas/qa_copy_check.py` | QA automático del texto: cada página contiene el copy literal de la hoja y ningún texto extra |
| `herramientas/render_programa.sh`, `render_carrusel.sh`, `rerender_all.sh` | Render Chrome headless por programa o carrusel (ruta absoluta interna; perfil propio), corte por página y lint de todo |
| `herramientas/MONTAJE-CANVA-notas.md` | Notas completas del montaje de prueba en Canva (copia del diseño de trabajo): importar HTML mixto, `merge-designs`, títulos de página, fuente |
| `QA-VISUAL.md` | Checklist de QA por pieza y plantilla de la tabla de estado por programa |

## Qué no se subió al repo y por qué

Quedaron fuera por llevar el copy, los programas, las marcas y las fotos del cliente: los módulos de configuración por programa (`programs_*.py`, `prog_02_*.py`, `build_*.py`), `place_c2.py` (depende de esos módulos), `extract_ai_images.py` (rutas y nombres de archivos del cliente), el HTML aprobado del programa modelo, las exportaciones PNG de Canva y las hojas resumen. Para reutilizar el patrón: escribir una config por programa con `n`, `slug`, `folder`, `copy_row`, `palette`, `assets` y `variants` (ver la docstring de `motor_series.py` y `build()`), un archivo `copys-anuncios.json` con el copy de la hoja y las TTF y logos de la marca en `_comun/`.

Las rutas internas de los scripts asumen la estructura `<proyecto>/02 - Diseno HTML/` con `_herramientas/` (estos scripts), `_comun/` (fuentes en `fonts/` y logos en `logos/`) y una carpeta por programa `<NN-slug>/`, más el copy en `<proyecto>/03 - Contenidos/copys-anuncios.json`; ajustar `ROOT` y `COPYS` en `motor_series.py` si se usa otra.
