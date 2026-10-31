# 02 — Crear un logo (brief → conceptos → checkpoint)

Método reexpresado y adaptado; fuentes y licencias en `CREDITOS.md`. Lo marcado **(propio)** es criterio del mantenedor o decisión de esta skill.

## 1. Descubrimiento y brief

Aprender lo imprescindible: **nombre exacto** (ortografía literal), qué hace, para quién, 3–5 adjetivos de marca, competidores, restricciones (colores, equity, dónde debe funcionar) y quién decide. Los adjetivos son el insumo más valioso: se convierten en rasgos visuales.

- **Vía rápida** (el usuario quiere resultados ya, o da poca información): máximo cinco preguntas en un solo mensaje, o ninguna → declarar los supuestos y pasar directo a tres conceptos. Se itera después de que reaccione. *(propio: es el modo por defecto)*
- Brief corto con la plantilla `templates/brief-logo.md`. Lista los supuestos.

## 2. Investigación y estrategia

1. Mira cómo se ve la categoría para no mimetizarte: busca marcas del sector (con el navegador o con tu conocimiento) y **lista sus clichés** (finanzas: azul, flechas hacia arriba, escudos; café: granos, vapor, tazas). Son terreno prohibido salvo que les des una forma realmente fresca.
2. **Mapa de palabras:** nombre, oferta, adjetivos, promesa → sustantivos, metáforas y opuestos; marca las intersecciones. Un concepto vive donde se cruzan dos ideas, no en una palabra suelta.
3. Elige **al menos dos tipos de marca distintos** a explorar (tabla abajo).

## 3. Tipos de marca — cuál elegir

| Tipo | Qué es | Va bien cuando | Cuidado |
|---|---|---|---|
| Wordmark | El nombre en tipografía con carácter | Nombre corto y distintivo; marca nueva sin presupuesto de exposición | Genérico si la fuente es de serie; nombres largos se encogen mal |
| Monograma | 2+ iniciales unidas | Nombres largos; herencia, moda, instituciones | Pierde significado si solo entrelaza letras |
| Letra-símbolo | Una inicial como símbolo | Ícono de app, tecnología, finanzas | Muchas marcas comparten la letra: necesita un giro |
| Pictórico | Objeto/animal reconocible | La historia tiene una imagen potente | Literalidad, detalle de más |
| Abstracto | Forma no figurativa | Posicionamiento conceptual; grupos diversificados | Sin significado propio hasta que se explica |
| Espacio negativo | Dos siluetas comparten un borde | Existe un par conceptual real | El más difícil; se fuerza fácil |
| Mascota | Personaje | Familiar, comida, juegos, comunidad | Complejidad, se fecha, rinde mal pequeño |
| Emblema | Texto dentro de insignia | Instituciones, clubes, oficio | Ilegible chico, poco flexible |
| Combinado | Símbolo + wordmark | La mayoría de marcas nuevas | Dos mitades débiles no suman una fuerte |

Diseña símbolo y lockup horizontal como **pareja** desde el primer día: los íconos suelen ser casi cuadrados y los logos completos, anchos.

## 4. Conceptos

- Escribe **8–12 conceptos de una frase** repartidos entre tipos. Cada uno necesita un giro propio: si la frase describiría el logo de un competidor, no es un concepto.
- Puntúa rápido (claridad de idea, distinción, simplicidad, pertinencia, fuerza a tamaño pequeño) y elige los **tres más fuertes y más distintos**. Muestra la lista larga solo si ayuda al usuario a orientar.
- Antes de construir: ¿ya existe esa marca? Busca la combinación sujeto + técnica en tu conocimiento y en la web; no recrees una existente.
- Una frase cuesta poco; una construcción cuesta mucho. **Construye solo los tres.**

## 5. Construcción en SVG (negro primero)

- Describe la construcción con palabras primero (primitivas, radios, ángulos, unidad de rejilla) y luego escribe el SVG. Lienzo `viewBox="0 0 256 256"` para símbolos; los lockups conservan altura 256.
- Negro sobre blanco, sin color. Pocos nodos, **arcos** para la geometría circular, ángulos exactos (0/15/30/45/60/90°), grosores y radios consistentes, huecos reales con `fill-rule="evenodd"`.
- Sin `<text>` en el arte final: las letras como contornos. En exploración se admite `<text>` marcado como provisional.
- Guarda cada iteración con versión. Renderiza y **mira** (`render_png.py`); no avances a ciegas.
- Patrones útiles que se componen bien: anillo con cuña, cuadrícula de puntos, nodos conectados, letra con un recorte, dos formas que comparten borde. Siempre con una idea detrás, nunca como decoración.

## 6. Probar y refinar (al menos dos vueltas)

```bash
python -I <skill>/scripts/vendor/logo-design-skill/svg_audit.py a.svg b.svg c.svg
python -I <skill>/scripts/vendor/logo-design-skill/preview_sheet.py a.svg b.svg c.svg -o preview.html
python <skill>/scripts/vendor/logo-design-skill/render_png.py preview.html --out-dir renders --size 1400
```

Abre el PNG y mira. Qué se corrige y cómo medirlo: `04-pruebas-y-qa.md`. Para la estantería de competidores usa `preview_sheet.py --refs <svgs de competidores que tú reúnas>` (la opción `--refs-industry` necesita la biblioteca del repo upstream, que esta skill no incluye).

**Pasada de oficio** (donde un logo hecho por IA suele flojear): (1) *prueba de la letra*: ¿cada letra modificada se sigue leyendo como esa letra a primera vista? (2) *uniones*: cada punto donde se tocan trazos, sin muescas, astillas ni grumos; (3) *literalidad*: si el concepto es solo el producto dibujado, empújalo más o descártalo.

## 7. Checkpoint — mostrar los conceptos y PARAR

```bash
python -I <skill>/scripts/vendor/logo-design-skill/concept_sheet.py a-simbolo.svg b-simbolo.svg c-simbolo.svg \
  --lockups a-lockup.svg b-lockup.svg c-lockup.svg --names "Nombre A" "Nombre B" "Nombre C" \
  --notes "Idea A" "Idea B" "Idea C" --recommend 1 --greyscale -o conceptos.png
```

Mira la imagen tú primero; luego muéstrala al usuario con este formato y espera:

```markdown
<imagen de la hoja de conceptos>

### A — <Nombre> · <tipo de marca>   ← recomendado
**Idea:** <una frase>
**Por qué encaja:** <2–3 puntos ligados a los adjetivos / audiencia / competencia>
**Riesgo honesto:** <uno>

### B — … / ### C — …

**Mi recomendación:** <una o dos frases>
**Siguiente:** elige una dirección (o dime qué te gusta de cada una). ¿Preparo el kit completo?
El kit incluye: paleta con versión a una tinta e invertida, lockups horizontal y apilado,
versión para tamaño pequeño, favicon + ícono de app + set web, tablero con mockups de tu sector y guía de uso de una página.
```

En gris primero (el color dispara debates de gusto). Si quiere cambios, vuelve a §5–6. Si el usuario no puede responder, para igual y describe qué contendría el kit.

## 8. Rediseño y refresh

- **Refresh** conserva el reconocimiento (misma idea, mejor oficio: limpiar geometría, corregir peso óptico, actualizar tipografía). **Rebrand** reemplaza la idea. Decide cuál es según qué equity vale la pena conservar y dilo antes de dibujar.
- Auditoría de equity: qué reconoce la gente hoy (forma, color, nombre), qué falla (no escala, no funciona a una tinta, se fecha) y qué está prohibido tocar (lo que el usuario declare).
- Entrega siempre una comparación lado a lado actual vs. propuesta y, si el cambio es grande, un plan de transición (cuándo conviven las dos versiones).
- Si el original es solo un raster, primero se **vectoriza** (`03`) para tener base limpia y poder medir qué cambió.

## 9. Kit

Solo si el usuario eligió y dijo sí: `05-entrega-y-kit.md`.
