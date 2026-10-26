# Síntomas de texto con IA sin criterio: causa y arreglo

> **Un síntoma no prueba nada.** Las personas también escriben así y los modelos cambian de hábitos con cada generación. Esta tabla sirve para **encontrar la causa** (falta de sustancia, de fuente, de revisión), no para «limpiar» palabras. Si se corrige solo la superficie, el problema sigue y es más difícil de ver.
>
> Niveles: **[fuente]** = descrito en la guía de síntomas de Wikipedia o en un estudio (ver `01-…` y `05-…`); **[candidato]** = observación sin fuente, sobre todo en español. El detector (`scripts/slop_lint.py`) rotula cada hallazgo con su nivel.

## 1. Restos objetivos (siempre se corrigen)

Son errores de proceso, no de estilo. El detector los trata como fallo.

| Resto | Ejemplos | Arreglo |
|---|---|---|
| Marcadores de posición | `[insertar …]`, `TODO`, `lorem ipsum`, `{{variable}}`, `XXX` | Completar o quitar |
| Frases dirigidas al usuario del chatbot | «Como modelo de lenguaje…», «Espero que esto te ayude», «¡Claro! Aquí tienes…», «As an AI language model», «Certainly! Here is…» | Borrar y revisar que no queden más |
| Enlaces con seguimiento | `?utm_source=…` (p. ej. `chatgpt.com`) | Limpiar el enlace y abrir la fuente real |
| Citas rotas o sin comprobar | enlaces que no responden, referencias sin fuente | Abrir cada fuente, sustituir o quitar la afirmación |

## 2. Síntomas de contenido (lo más importante)

| Síntoma | Nivel | Causa probable | Arreglo |
|---|---|---|---|
| **Importancia inflada** («juega un papel fundamental», «testimonio de», «se erige como», «pivotal role», «stands as a testament») | fuente | No hay hecho concreto que sostener la afirmación | Sustituir por el hecho: qué pasó, cuándo, qué se midió |
| **Tono promocional / de folleto** («impresionante», «innovador», «líder») | fuente | Falta evidencia; se compensa con adjetivos | Quitar el adjetivo y poner la prueba, o quitar la frase |
| **Atribuciones vagas** («los expertos coinciden», «según estudios», «muchos creen») | fuente | No se abrió ninguna fuente | Citar el estudio o la persona con enlace, o eliminar |
| **Cobertura genérica y simétrica** (todo «tiene ventajas y desventajas», ningún criterio) | candidato | Falta una posición defendible | Dar una recomendación con sus límites («depende de…») |
| **Secciones de relleno** («Desafíos y perspectivas futuras», «Conclusión» que repite todo) | fuente | Plantilla, no necesidad del lector | Borrar la sección o sustituirla por el siguiente paso útil |
| **Sin ejemplos propios** (todo se podría decir de cualquier empresa) | candidato | No se usó el banco de experiencia | Añadir un caso o dato real con permiso; si no existe, no escribir esa parte |
| **Cifras sin fuente** o «redondas» sospechosas | candidato | Dato inventado o recordado sin comprobar | Fuente abierta con fecha o quitar la cifra |

## 3. Síntomas de lenguaje (los más visibles y los menos importantes)

| Síntoma | Nivel | Qué hacer |
|---|---|---|
| Vocabulario «de moda» de modelos: *delve, showcasing* (guía de Wikipedia); *intricate, notably* (estudio de Kobak, según su cobertura); *tapestry, landscape…* y, en español, «adentrarse», «panorama», «tejido», «desbloquear», «sumérgete» | fuente (las dos primeras) / candidato (el resto) | No es prohibición: si la palabra es la exacta, se queda. Si es adorno, se reescribe diciendo la cosa. La lista cambia con cada generación de modelos |
| «Serves as / features» en vez de «es / tiene»; «sirve como», «cuenta con» | fuente / candidato | Usar el verbo simple |
| **«No solo X, sino también Y»** repetido | fuente | Reservarlo para cuando hay un contraste real |
| **Tríadas** («rápido, fácil y seguro») en casi todos los párrafos | fuente | Decir los elementos que de verdad hay (a veces son dos o cuatro) |
| Muletillas editoriales: «es importante destacar que», «cabe señalar», «it's important to note» | fuente / candidato | Quitar y decir directamente lo importante |
| Conectores de ensayo escolar en cadena: «además», «asimismo», «por otro lado», *moreover, furthermore* | fuente / candidato | Dejar que el orden de las ideas haga el trabajo |
| Cierres de resumen: «En resumen», «En conclusión», *In summary, Overall* | fuente | Cerrar con la acción siguiente, no con una repetición |
| Aperturas de «en el mundo actual / digital / hoy en día» | candidato | Empezar por el dato o el problema |
| Meta-anuncios: «en esta guía vamos a ver…» | candidato | Entrar al contenido |

## 4. Síntomas de formato

| Síntoma | Nivel | Arreglo |
|---|---|---|
| **Exceso de negritas** (varias por párrafo) | fuente | Dejar solo lo que alguien buscaría al escanear |
| **Listas con encabezado en línea** («**Rapidez:** …», «**Calidad:** …» ×6) | fuente | Prosa o una lista corta con criterio |
| **Títulos en mayúscula en cada palabra** (en español se escribe como en una frase) | fuente / candidato | Capitalizar como oración |
| **Niveles de título saltados** (H2 → H4), o emojis como viñetas | fuente | Respetar la jerarquía |
| Párrafos de longitud y ritmo idénticos | candidato | Solo se corrige si además falta sustancia; no se «mezcla» por sistema |

## 5. Cómo se usa la tabla

1. Correr el detector y agrupar los hallazgos por **familia** (contenido, lenguaje, formato, restos).
2. Para cada hallazgo, preguntar **qué falta debajo**: un hecho, una fuente, un ejemplo propio, una posición.
3. Añadir eso o quitar la frase. **No** cambiar una palabra por su sinónimo y seguir.
4. Releer la pieza completa como lector: ¿hay algo que no sabía? Si no, volver al paso 2 de la puerta (sustancia).
5. Registrar qué patrones aparecieron y de dónde salieron (qué prompt, qué tema): así se mejora el proceso y no solo la pieza.

## 6. Lo que no se hace (anti-patrones del propio anti-slop)

- Pasar el texto por un «humanizador» o parafraseador: es la misma máquina otra vez y suele empeorar la precisión.
- Meter errores, jerga o muletillas a propósito.
- Imponer cuotas («máximo 2 conectores por página», «frases de 12 a 25 palabras»).
- Usar el porcentaje de un detector de IA como criterio de aprobación.
