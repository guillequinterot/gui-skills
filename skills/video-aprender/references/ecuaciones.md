# Leer y verificar ecuaciones de un video (finanzas y similares)

Una ecuación que se **lee** de una imagen puede estar mal leída; una que se **dice** puede estar mal transcrita. Entenderla = transcribirla, nombrar sus variables, **recalcularla** y probar que se comporta como debe. Marca **[verificado]** solo lo que recalculaste.

## 0. La fuente de las ecuaciones manda más que la herramienta
| Fuente | ¿Se leen las ecuaciones? |
|---|---|
| **Archivo original de las diapositivas (PDF/PPT)** | **Sí, perfectamente** (1280 px, con su capa de texto). Es la fuente correcta |
| Grabación de pantalla, Zoom con pantalla compartida, pizarra de cerca | Sí, si la resolución es suficiente: `slides_extract.py` captura cada estado estable |
| **Video de aula con cámara(s)** (el profesor, el público y la diapositiva proyectada en un rincón) | **No de forma fiable.** Medido con una clase real de MIT (YouTube la ofrece como máximo a 640×480): la diapositiva proyectada ocupaba ~190 px de ancho y las cámaras cambian de ángulo y de zoom, así que **ni el cuadro completo ni `--roi` detectan cambios de diapositiva** (9 «estados» eran la misma carátula desde ángulos distintos). **Pide el archivo original** y usa `--slides` |
Recortar y ampliar **no inventa resolución**: si el texto no se lee en el original, se declara ilegible.

## 1. Transcribir desde la imagen
- Abre la imagen del estado (`pantalla/slides/slide_NN_*.jpg`, 1280 px). Si la ecuación es pequeña: `frame_probe.py VIDEO --at T --crop x,y,w,h --scale 2` (x,y,w,h en fracciones 0–1).
- Escríbela en **texto plano o LaTeX exacto**, símbolo a símbolo (subíndices, exponentes, barras de fracción, sumatorias con sus límites). Lo ilegible se marca `[ilegible]`, **no se adivina**.
- Anota la diapositiva y el minuto (`#07 · 12:41`) y lo que la voz decía en ese momento (`contenido.md`).

## 2. Nombrar variables, unidades y supuestos
Cada símbolo: qué es, en qué unidades y qué convención usa. En finanzas pregunta siempre:
- ¿La tasa es **anual** o **por periodo**? ¿Nominal o efectiva? ¿**Capitalización** (anual, mensual, continua)?
- ¿Los flujos caen al **final** o al **inicio** de cada periodo? ¿Cuándo es t = 0?
- ¿Es nominal o **real** (con o sin inflación)? ¿Hay impuestos o costos ignorados?
- ¿Hay una condición de validez? (p. ej. perpetuidad creciente exige tasa > crecimiento).

## 3. Recalcular con Python (con los números del propio video)
```python
# Ejemplo de forma (sustituye por la ecuación real del video):
def pv(fv, r, n): return fv / (1 + r) ** n
assert abs(pv(1000, 0.05, 3) - 863.8376) < 1e-3   # el video dice «863.84»
```
- Usa **los números que el video usa** en su ejemplo y compara con el resultado que el instructor da. Una diferencia es un hallazgo (error del video, de la transcripción o de tu lectura): **repórtalo**, no lo tapes.
- **Potencias grandes desbordan** (`OverflowError`): calcula una razón de potencias, `((1+g)/(1+r))**(t-1)`, o usa logaritmos, `math.exp(-T*math.log1p(r))` en vez de `1/(1+r)**T` (visto al verificar el caso T→∞ y una serie de 20 000 términos).
- `numpy` está instalado; `sympy` **no** (instalarlo es opcional: `pip install sympy`). Para valores exactos usa `fractions.Fraction` o `decimal`.
- Si la ecuación define una cantidad, **despeja** y comprueba que la inversa reproduce la entrada (ida y vuelta).

### Ejemplo real (MIT 15.401, diapositivas 23 y 25, leídas del PDF original)
Perpetuidad creciente `PV = C/(1+r) + C(1+g)/(1+r)² + … = C/(r−g), r > g`: la serie de la diapositiva sumada a 20 000 términos con C=100, r=8 %, g=3 % da **2000.000000** = C/(r−g); el paso intermedio `[(1+r)/(1+g) − 1]·PV = C/(1+g)` da 97.087379 en ambos lados; con r ≤ g la serie **diverge** (73 557 268 con 500 términos, 1 103 296 632 878 con 1000), o sea que la condición r > g **es necesaria**. Anualidad `PV = C·(1/r)[1 − 1/(1+r)^T] = C·ADF(r,T)`: las tres formas escritas coinciden con la suma de flujos descontados (9107.9140 para C=1000, r=7 %, T=15), tiende a C/r cuando T→∞ y **las 60 celdas de la tabla de factores (6 tasas × 10 plazos) coinciden con la fórmula** (±0.0006).

## 4. Pruebas de sentido (casos límite y forma)
| Prueba | Qué comprobar |
|---|---|
| Límites | tasa → 0, n → ∞, n → 0: ¿el resultado tiende a lo esperado? |
| Monotonía | más tasa ⇒ menor valor presente; más periodos ⇒ mayor valor futuro (si r > 0) |
| Unidades | ambos lados en las mismas unidades; la tasa y el número de periodos con la misma base de tiempo |
| Conservación | suma de valores presentes de un flujo = valor presente del flujo completo |
| Redondeo | el video suele redondear: ¿la diferencia está dentro del redondeo mostrado? |

## 5. Fórmulas de finanzas que suelen aparecer (para **contrastar**, no para reemplazar lo que dice el video)
Úsalas solo como referencia de verificación; si el video usa otra convención, manda el video y se anota la diferencia.
- Valor futuro: FV = PV·(1 + r)^n · Valor presente: PV = FV / (1 + r)^n.
- Anualidad (pagos C al final de cada periodo, T periodos): PV = C/r · [1 − 1/(1 + r)^T].
- Perpetuidad: PV = C / r · Perpetuidad creciente: PV = C / (r − g), válida solo si r > g.
- Capitalización continua: FV = PV·e^(r·t).
- Real y nominal: (1 + nominal) = (1 + real)·(1 + inflación); la aproximación real ≈ nominal − inflación vale solo para tasas pequeñas.
- Tasa efectiva anual con m capitalizaciones: (1 + r/m)^m − 1.

## 6. Qué entregar por ecuación (tabla de `analisis.md` §3)
Ecuación (texto exacto) · variables y unidades · supuestos · **verificación en Python** (entradas → salida) · ¿coincide con lo dicho? · diapositiva y minuto.

## 7. Límites y prudencia
- **No es asesoría financiera.** Se explican conceptos y se calcula con los números que aporte el usuario; no se recomienda comprar, vender ni contratar.
- Un error común de la transcripción: números ("fifteen" / "fifty"), "r" frente a "R", "n" frente a "in", "log" frente a "ln". **La imagen manda sobre el audio** para símbolos y cifras.
- Si el video muestra un gráfico (curva de rendimiento, flujo de caja), describe lo que se ve con el eje y la escala; no extrapoles valores que no se leen.
