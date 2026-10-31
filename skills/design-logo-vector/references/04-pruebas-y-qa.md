# 04 — Pruebas, optical corrections y crítica

Un logo no está terminado hasta sobrevivir esto. Corre las pruebas sobre cada concepto antes de presentarlo y otra vez sobre el arte final. Lo que no corriste se declara **no verificado**.

## 1. Pruebas (checklist)

**Escala**
- [ ] **16 px (favicon):** la idea sobrevive, sin mancha. Si no, versión simplificada para tamaño pequeño (menos elementos, trazos más gruesos, huecos más grandes).
- [ ] **24–32 px** (listas de apps, avatares): reconocible de un vistazo.
- [ ] **Muy grande** (valla, fachada): curvas suaves, sin nodos grumosos; lo que no se ve chico se ve enorme.
- [ ] **Tamaño mínimo:** reduce hasta que pierda sus rasgos; el tamaño justo por encima es el mínimo documentado (px en pantalla, mm en impreso).

**Color y valor**
- [ ] **Una tinta negra** sobre blanco.
- [ ] **Una tinta blanca** sobre negro, sin verse más pesada (irradiación). Si pesa más, entrega la versión invertida ligeramente adelgazada.
- [ ] Sobre **color de marca**, **fotos** y **patrones** (si no, recurso gráfico: contorno o contenedor).
- [ ] **Escala de grises:** los segmentos se separan por valor; nada depende solo del tono.
- [ ] Reproduce en **CMYK**; equivalente en tinta directa si es vívido.

**Forma**
- [ ] **Entrecerrar los ojos / desenfoque:** la silueta sola ya es distintiva.
- [ ] **Espejo:** voltearlo no revela errores de proporción a los que te acostumbraste.
- [ ] **Giro 90° y 180°, muy pequeño, a distancia:** busca lecturas no deseadas (letras accidentales, partes del cuerpo, símbolos ofensivos/sexuales, políticos o religiosos, parecido a señales de peligro). Muéstralo a alguien que no vio el brief.
- [ ] **Prueba de la letra:** cada letra modificada se lee como esa letra al primer vistazo.
- [ ] **Uniones:** en cada cruce de trazos no hay muescas, astillas, grumos, huecos finos ni trampas de tinta.
- [ ] **Geometría limpia:** sin ángulos casi limpios, radios y grosores consistentes (`svg_audit.py` los marca).
- [ ] **Equilibrio:** no inclinada sin querer; peso repartido; símbolo casi cuadrado.

**Distinción**
- [ ] **Estantería:** puesto entre competidores no se mimetiza (`preview_sheet.py --refs ...`).
- [ ] **Familiaridad:** no recuerda a una marca existente (a ti ni a quien le preguntes).
- [ ] **Búsqueda marcaria:** recomienda búsqueda en bases de marcas y búsqueda inversa de imagen **antes del lanzamiento**; no das autorización legal.

**Sentido y encaje**
- [ ] La idea cabe en **una frase**; el tono coincide con los adjetivos (afilado/redondo, pesado/ligero, cálido/frío).
- [ ] Identifica, no explica; seguirá encajando si el negocio crece.
- [ ] Significado cultural de colores y símbolos revisado para su audiencia.
- [ ] Funciona sin eslogan y, si es símbolo, a futuro sin el nombre.

**Producción**
- [ ] Una tinta, bordado (sin líneas de pelo; huecos ≥ ~1 mm a tamaño de pecho), grabado láser, corte de vinilo, rotulación, modo oscuro.
- [ ] Ícono de app: dimensionado óptico dentro del contenedor redondeado; sin texto fino.
- [ ] Avatar: sobrevive al recorte circular.
- [ ] **Archivo maestro:** solo vector, texto en contornos, trazos expandidos, sin filtros ni raster, `viewBox` limpio, `<title>`; `svg_audit` ≥ ~90 sin FAIL.

**Contexto**
- [ ] 5–6 **mockups pertinentes al negocio** (la taza de la cafetería, no la bolsa del gimnasio) en estilo consistente. Nunca juzgar un logo solo sobre un lienzo blanco.
- [ ] Lockups (horizontal, apilado, solo símbolo) probados a sus tamaños.

## 2. Optical corrections (oficio)

Se hacen al final, con uno o dos retoques de nodos; no sustituyen un concepto débil.

| Corrección | Qué hacer | Magnitud orientativa |
|---|---|---|
| **Sobreimpresión (overshoot)** | Formas redondas y puntiagudas se pasan un poco de la línea base/altura/borde para *parecer* alineadas con las planas | 1–3 % de la altura en curvas; 3–6 % en vértices |
| **Efecto hueso (bone effect)** | Un tramo recto entre dos extremos redondos parece pinzarse hacia dentro; engrosa un poco el centro del tramo | Ajuste mínimo; a veces es expresivo y se deja |
| **Irradiación** | El blanco sobre negro se ve más grueso: adelgaza la geometría de la versión invertida | ~2–5 % del grosor de trazo |
| **Horizontales** | Las horizontales parecen más gruesas que las verticales del mismo ancho | Adelgazar 5–10 % |
| **Centro óptico** | Centrar un poco por encima del centro geométrico | `--optical-offset -0.02` de `export_variants.py` para cuadrados/ícono |
| **Uniones agudas** | Adelgaza el trazo cerca de ángulos agudos para evitar manchas | Caso a caso |

## 3. Criterios de aceptación de un SVG final

- `<svg>` con `viewBox` y `<title>`; sin `<text>` vivo, rasters incrustados, filtros ni máscaras (salvo recorte justificado).
- Máx. 2–3 colores (idealmente 1–2) con razón conceptual; sin degradados que rescaten una forma.
- Pocos nodos; arcos para lo circular; huecos con `fill-rule="evenodd"` en lugar de formas blancas "falsas".
- Margen interno razonable y centrado óptico verificado.
- Renderiza igual en Chrome y en el rasterizador usado para PNG.
- Pasó 16 px, una tinta y invertido, o está declarado lo contrario.

## 4. Crítica de un logo existente (modo criticar)

Diagnostica primero; no modifiques archivos si solo pidieron análisis. Estructura:

1. **Resultado general** (una frase honesta).
2. **Qué identifica y funciona** (conservar).
3. **Hallazgos por severidad** con causa y corrección concreta: estrategia (¿dice lo que debe y se diferencia?), construcción (geometría, oficio), escala (16 px, una tinta), color, tipografía, legibilidad, producción.
4. **Puntaje** de 1–5 en cada eje: claridad de idea · distinción · simplicidad · pertinencia · fuerza a tamaño pequeño · oficio. El puntaje orienta, no decide.
5. **Qué haría y en qué orden** (refresh vs. rebrand, ver `02` §8).

No presentar el gusto personal como evidencia; no usar "simple", "memorable" o "atemporal" como notas absolutas: demuestra cómo funciona en contextos relevantes.
