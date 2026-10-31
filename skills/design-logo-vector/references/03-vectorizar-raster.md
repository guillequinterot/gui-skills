# 03 — Vectorizar un logo raster

Método reexpresado y adaptado de `pixel2svg-html` (MIT, Nolan Lai) y `pixel2motion`; ver `CREDITOS.md`. **Regla de gobierno: la complejidad suave más baja que pase el QA visual.** No se maximiza el ajuste por píxel; se empieza por la geometría más simple que explique la marca y solo se sube un peldaño cuando la superposición muestra un desajuste *estructural*.

## 0. Antes de empezar

- ¿Es el logo del usuario o de su cliente? (ver SKILL.md, preflight 2).
- Pide el **mejor original** que exista (PDF/vector viejo > PNG grande > JPG comprimido > captura). Un JPG con artefactos o una foto de un logo limita el resultado: dilo antes de prometer.
- Si el original está en baja resolución (< ~500 px en el lado largo), el vectorizado será una **reconstrucción**: se redibuja con primitivas y curvas, no se traza.
- Corre `handshake.py`. Sin Chrome/Edge no hay superposición ni IoU.

## 1. Medir primero

Registra tamaño, modo, alfa, colores de primer plano y fondo. Extrae por parte: máscaras por color, centros/radios (un punto: `√(área/π)`), muestras de borde. Reglas de medida que ahorran iteraciones:

- En curvas, muestrea por **columnas** donde la curva es suave y por **filas** donde es empinada (> 45°); el ancho perpendicular es la longitud del tramo × cos θ.
- Excluye zonas ocluidas (donde otra forma tapa el extremo de un trazo).
- Toda búsqueda de un rasgo (cima, vértice) va **acotada a una ventana**; un `argmin` sobre toda la curva encuentra casi siempre el rasgo equivocado.
- Fondos con cuadros de transparencia horneados: umbral por oscuridad/saturación y excluye el tablero. Fondo sólido: infiérelo de los bordes.

```bash
python <skill>/scripts/vendor/pixel2svg-html/raster_logo_trace.py original.png --out 02-vectorizado/medida
```

Esto produce `logo.svg`, `metrics.json`, `overlay.png` y un `logo.html` de arranque. **Es una medición, no el arte final**: normalmente son rectas por píxel (cientos de nodos).

## 2. Escalera de complejidad (usa el primer peldaño que alcance)

| Nivel | Qué | Cuándo |
|---|---|---|
| 1 | **Primitivas**: círculo, elipse, rect, línea, arco, transformaciones | Puntos, anillos, marcas geométricas |
| 2 | **Compuestos de pocas primitivas** (máscaras o huecos con `evenodd`) | Anillo con cuña, formas que se restan |
| 3 | **Pocas curvas cúbicas analíticas** | Cintas, remolinos, hojas, olas, escudos |
| 4 | **Contorno suavizado**: más nodos solo donde hay cambio real de forma, continuidad de tangente G1 | Siluetas orgánicas que el nivel 3 no explica |
| 5 | **Trazo automático** | Solo siluetas irregulares donde nada de lo anterior sirve; después se suaviza o reajusta |

Si subir de nivel solo mejora el antialiasing o unos píxeles de cobertura, **quédate en el nivel inferior**. Si el inferior tiene mal el centro, el ancho, los extremos, el hueco o deja bordes en escalera, sube un peldaño. Anota el nivel provisional y su razón.

Estructura el SVG con **ids semánticos** (`#simbolo`, `#punto`, `#wordmark`) aunque no vaya a animarse: cuesta nada, facilita editar y permite animarlo luego.

## 3. Compuerta de suavidad y de ajuste

El IoU **no** puede esconder mala artesanía.

- Falla el SVG si bordes que deberían ser suaves se ven en escalera, tiemblan, usan tramos ortogonales de la rejilla de píxeles, tienen nodos de trazado ruidosos o parecen una máscara de mapa de bits a 200–400 % de zoom, **aunque el IoU sea alto**.
- Calcula y registra el IoU en cada iteración, pero **sin umbral global fijo**: empújalo hacia arriba después de proteger suavidad y estructura. Un resultado con IoU algo menor puede aprobar si la superposición es fiel y los residuos se explican (suavizado deliberado, antialiasing, sustitución de fuente, artefacto del original). Si publicas uno de menor IoU sobre otro de mayor IoU pero dentado, di el compromiso.
- Guarda evidencia de suavidad: un recorte ampliado o el resultado de la auditoría de curvas.
- Rellenos con **degradado** (esferas, botones brillantes): la diferencia binaria contra la máscara es un artefacto del umbral; juzga esas partes por centro/radio/extensión y a ojo, y nómbralo.

## 4. Ajustar

1. **Primer artefacto de baja complejidad** (SVG con `viewBox` correcto, ids por parte).
2. Superponer y medir en un solo paso:
   ```bash
   python <skill>/scripts/vendor/pixel2svg-html/render_overlay.py logo.svg original.png \
     --out 02-vectorizado/fit_iteraciones/01_superposicion.png --render-out 02-vectorizado/render.png --report 02-vectorizado/metricas.json
   ```
   (Exporta `CHROME_BIN` si no encuentra el navegador. Los recuentos `src_only_px` y `render_only_px` son diagnóstico.)
3. **Mira** centros, radios, extremos, perfil de ancho, extremos de curvas, huecos y suavidad del borde.
4. **Una** cosa por iteración; **máximo 10**; guarda `NN_nombre_superposicion.png` con sus métricas. Todo el estado del ajuste (scripts, muestras, parámetros) en `fit_work/` dentro del proyecto, **nunca en `/tmp`**: la reanudabilidad es parte de la entrega.
5. Si una curva sale bultuda, **quita nodos y reajusta las curvas grandes** antes de añadir más. Si un tramo local está mal, añade complejidad solo ahí (un segmento puente corto sobre el pico de curvatura).
6. Como mucho **una** ronda de corrección por retroalimentación, con un polinomio de bajo orden, no interpolación irregular (perseguir deltas de ±3 px inyecta rasgos falsos que luego se leen como quiebres).

### Cintas y trazos de ancho variable

- Un trazo con grosor constante puede ser `stroke`; **cualquier ancho variable es un contorno relleno**. No construyas el contorno desplazando una línea central ajustada: hereda sus saltos de curvatura como quiebres falsos de 10–15°. Ajusta **cada borde contra los puntos medidos del original**.
- Extremos bajo una forma que los cubre: terminaciones planas ocultas, nunca terminaciones redondas que sobresalgan.
- **Cintas cerradas o que se cruzan a sí mismas** (∞, firmas): no existen dos bordes abiertos que ajustar. Usa `fit_ribbon_centerline.py`: una línea central densa como andamio → recentrado medido → reconstrucción por longitud de arco → ajuste de bordes al original. Detalle y trampas medidas en el código y en el ejemplo upstream.
  ```bash
  python <skill>/scripts/vendor/pixel2svg-html/fit_ribbon_centerline.py original.png --seeds semillas.json --out-dir 02-vectorizado/cinta
  ```

### Wordmarks

Por defecto, `<text>` vivo en el borrador **solo si** la fuente existe en el equipo; el logo final lleva contornos.

1. **Enumera las fuentes realmente instaladas** antes de probar candidatas. Dos familias "distintas" con IoU *idéntico* significa que ambas cayeron a la misma fuente.
2. Ajusta el tamaño de fuente a la **altura de mayúscula** medida del original (2–3 vueltas de render → medida → reescala).
3. Ordena candidatas por IoU de la región **y por la razón de peso de tinta** (px de tinta renderizada ÷ px de tinta del original). Un peso ≈ 1,0 con IoU algo menor se ve más fiel que un IoU más alto con trazos 1,2× más gruesos: el desajuste de peso salta a la vista antes que las diferencias de forma de letra.
4. Fija la geometría entre plataformas con `textLength` + `lengthAdjust="spacingAndGlyphs"`, `text-anchor` y la línea base medida; documenta la sustitución de fuente como residuo conocido. Si las letras originales son dibujadas a medida, redíbujalas como contornos.

## 5. Verificar (obligatorio)

```bash
python -I <skill>/scripts/verificar_vectorizado.py 02-vectorizado/logo.svg --source 00-original/logo.png --out-dir 03-verificacion
```

Devuelve semáforo: **ROJO** si el trazado es un polígono de rectas por píxeles; **AMARILLO** por IoU bajo, uniones con quiebre > 8° (confirma cuáles son esquinas de diseño; solo las uniones *no diseñadas* son fallo, **incluso con IoU alto**), ángulos casi limpios o avisos del auditor; **VERDE** si no encuentra nada. Es ayuda, no veredicto: mira la superposición y haz zoom al 400 %.

Limitación conocida: el auditor de curvas aproxima los **arcos SVG (`A/a`)** con rectas, por eso el script omite sus avisos de unión cuando el trazado los usa.

Después, las pruebas de producción de `04-pruebas-y-qa.md` (16 px, una tinta, invertido).

## 6. Criterios de aceptación

Termina cuando hay **evidencia**, no afirmaciones:

- El SVG existe, renderiza y su render coincide con el original en escala, posición y color.
- Superposición final **mirada**; IoU y diferencias en píxeles reportados sin umbral fijo.
- Sin desajuste estructural: centro, escala, extremos, perfil de ancho, espaciado, espacio negativo y silueta.
- Curvas sin quiebres no diseñados > 8°, o el quiebre se declara como defecto conocido.
- Las diferencias restantes se explican por antialiasing, suavizado deliberado o fuente sustituida.
- **Entrega con presupuesto agotado (10 iteraciones):** se empaqueta el mejor candidato si pasa suavidad, estructura y QA visual, con los residuos declarados; si no, se etiqueta como **borrador** y se deja el estado reanudable en `fit_work/`, ofreciendo seguir.

Reporta en el mensaje final: nivel de la escalera usado, número de nodos/segmentos, IoU, residuos conocidos y qué NO se verificó.

## 7. Entregables

`logo.svg` (maestro limpio, ids semánticos, `<title>`), `render.png`, superposición final y tira de progreso (`overlay_progress_strip.py` junta original → iteraciones → render), `reporte.md`, y si se pidió, `logo.html` con JS (`svg_to_js_html.py`; verifica en un navegador real que no salga en blanco, cortado ni a otra escala).
