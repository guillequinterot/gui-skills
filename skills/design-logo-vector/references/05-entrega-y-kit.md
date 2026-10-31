# 05 — Entrega y kit

El kit se construye **solo** cuando el usuario eligió una dirección y dijo sí en el checkpoint (o pidió entrega directa). Si el insumo es un logo existente (vectorizado o recibido), el kit parte de ese maestro.

## 1. Refinar la dirección elegida

Geometría final, optical corrections (`04` §2), **versión de tamaño pequeño** si la marca pierde detalle a 16–24 px, versión invertida adelgazada si hace falta.

## 2. Color

1–2 colores idealmente, propios de la categoría, reproducibles (HEX/RGB/CMYK/tinta directa si aplica) y accesibles. La versión de una tinta y la de grises deben seguir funcionando. Contraste del símbolo sobre fondo: ≥ 3:1 (`svg_audit.py --bg "#HEX"` lo informa). Si la marca ya tiene paleta o variables de Figma, **se usan esas** y se pregunta antes de inventar (regla del método de `direct-visual-design`).

## 3. Tipografía y lockups

Estudio tipográfico breve; letras propias o modificadas para que la marca sea ownable; espaciado óptico; **máximo dos familias**. Lockups: horizontal, apilado, solo símbolo, solo wordmark — fija tamaños relativos y espacios. Verifica la **licencia** de las fuentes para uso en logo y di cuáles asumiste. Las letras del logo final van como contornos.

## 4. Exportar

```bash
# desde el símbolo maestro
python -I <skill>/scripts/vendor/logo-design-skill/export_variants.py marca-simbolo.svg --title "Marca" \
  --mono "#HEX" --icon-bg "#HEX" --web-icons [--favicon-source marca-simbolo-chico.svg] --out-dir 04-entrega/simbolo
# desde el lockup horizontal
python -I <skill>/scripts/vendor/logo-design-skill/export_variants.py marca-horizontal.svg --title "Marca" \
  --only black white mono --mono "#HEX" --png 1200 --out-dir 04-entrega/horizontal
```

Produce `-black.svg`, `-white.svg`, `-mono-<hex>.svg`, `-square.svg`, `-favicon.svg`, `-app-icon.svg`, PNG a los tamaños pedidos y, con `--web-icons`, `favicon.ico` (16/32/48), `favicon-16/32/48.png`, `apple-touch-icon.png`, `icon-192/512.png`, `maskable-512.png`, `site.webmanifest` y `head-snippet.html`.

Notas medidas:
- La conversión a una tinta reemplaza **todos** los colores: las formas blancas usadas como "recortes falsos" se vuelven manchas. Arregla el maestro con huecos reales (`fill-rule="evenodd"`) o usa `--keep-white`.
- Revisa cada archivo abriendo su PNG: no entregues a ciegas.
- `.ai`, EPS, PDF editable: los hace **`design-illustrator`** a partir del SVG maestro; esta skill no los promete.

## 5. Tablero de presentación (opcional, recomendado en rondas con cliente)

`templates/presentation-spec.example.json` → copia y edita (`brand`, `brief`, `adjectives`, `industry` o lista de `mockups`, `concepts[]` con `symbol`/`lockup`/`idea`/`rationale`, `recommendation`):

```bash
python -I <skill>/scripts/vendor/logo-design-skill/presentation_board.py spec.json -o tablero.html --png-dir 04-entrega/slides
python -I <skill>/scripts/vendor/logo-design-skill/presentation_board.py --list-mockups
```

Genera un HTML de una sola pieza: qué entendimos del brief, cada concepto grande/pequeño/invertido con 6 mockups del sector, comparación y recomendación. En gris para la primera ronda (`"greyscale": true`); en color para el diseño final (`"final": true`). Las marcas de varios colores deben pasar artes `symbol_on_tile` / `lockup_on_dark` para conservar sus colores en los mockups.

## 6. Guía de uso (una página)

Plantilla `templates/guia-de-uso-logo.md`: zona de respeto (medida con un elemento del propio logo), tamaños mínimos (px y mm), colores con códigos, fondos aprobados, versiones y cuándo usar cada una, y **usos incorrectos** (estirar, recolorear fuera de la paleta, fondos ruidosos, sombras). Para marcas grandes, ampliar a sistema: patrones, íconos, movimiento (`06`).

## 7. Lista final antes de entregar

- [ ] Cada archivo abierto y mirado (no solo generado).
- [ ] `svg_audit` ≥ ~90 sin FAIL en maestros; `verificar_vectorizado.py` en VERDE/AMARILLO explicado si hay original.
- [ ] 16 px, una tinta e invertido pasados (o declarados no verificados).
- [ ] Nombre y texto del cliente literales; fuentes y licencia declaradas.
- [ ] Recordatorio: búsqueda marcaria pendiente; Pantone/CMYK por probar en impresión si aplica.
- [ ] Archivos en `04-entrega/` del proyecto, nada con marca de cliente en el repo.
- [ ] Nota del proyecto (Obsidian, si hay) actualizada: decisiones, entregables, próxima acción.

## 8. Qué se declara en el mensaje final

Qué se hizo, qué pasó las pruebas, qué se ajustó (con cifras: "adelgacé la versión invertida 3 %; abrí el hueco de 6 a 10 unidades para que sobreviva a 16 px"), qué queda por hacer al usuario (búsqueda marcaria, prueba de impresión, licencia de fuente) y qué **no** se verificó.
