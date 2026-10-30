# Puntaje 1 a 100 por bloque y excepciones SEO

> Complementa el semáforo ([`06-semaforo-por-parrafo.md`](06-semaforo-por-parrafo.md)) con una **escala numérica** para cuando hace falta
> comparar bloques o artículos, priorizar qué reescribir primero o dejar una salida legible por máquina. Añade además la lista de
> **excepciones SEO** que el semáforo no tenía: lo que parece relleno pero en una página que debe posicionar es correcto.

## 1. Origen y límites

Basado en la skill `no-slop` de `seo-skills.com` (Jorge Jaramillo, consultada el 2026-10-30), que a su vez adapta `stop-slop` de Hardik Pandya (MIT). El sitio y su repositorio no declaran licencia: aquí está **reformulado**, sin copiar sus textos ni sus ejemplos.

- Es **criterio editorial en español para artículos de blog**, no un estudio. Los puntos de corte son valores iniciales.
- Mide **cuánto del bloque no informa**, no si lo escribió una IA. Mismas reglas de fondo que el semáforo: un puntaje bajo no prueba que sea humano ni uno alto que sea de IA.
- El puntaje **no sustituye** la puerta anti-slop (propósito, procedencia, revisión humana, hechos verificados). Es una ayuda para el paso de síntomas y para la revisión.
- Encaja con el principio 7 de la skill: no se imponen cuotas de palabras, conectores ni longitudes. La pregunta no cambia: ¿cuánto de este bloque le da al lector un dato, una instrucción o un ejemplo?

## 2. La pregunta de cada bloque

> ¿Cuánto de este bloque le da al lector un dato, una instrucción o un ejemplo, y cuánto se podría borrar sin perder nada?

Cómo leer un bloque antes de puntuarlo:

1. **Proporción de relleno.** Orientación: una oración vacía de cada cinco, alrededor de 25 a 40; la mitad vacía, de 50 a 65; solo una oración útil, 70 o más.
2. **Apertura y cierre.** ¿Anuncian lo que se va a decir o cierran con una consigna?
3. **Ritmo interno.** Oraciones de longitud uniforme, tríadas y preguntas retóricas que no responden nada.
4. **Redundancia** dentro del bloque y frente a otros (citar el identificador del bloque).
5. **Promesa.** El encabezado o la primera oración prometen algo que el párrafo no entrega.
6. **Listas.** Una lista de elementos concretos baja el puntaje; una de elementos genéricos lo sube.
7. **Encabezados.** Se juzgan junto con el párrafo que encabezan, no solos.

## 3. Escala

| Puntaje | Nivel | Qué es | Equivalencia propuesta con el semáforo |
|---|---|---|---|
| 1 a 20 | Limpio | Datos concretos, instrucciones específicas, ejemplos, cifras | 🟢 |
| 21 a 40 | Aceptable | Genérico pero funcional | 🟢 (con observación) |
| 41 a 60 | Sospechoso | Gran parte se puede borrar | 🟡 |
| 61 a 80 | Slop | Tics de IA, promesas vacías, adjetivos inflados | 🔴 si además falla P1 y P2; si no, 🟡 |
| 81 a 100 | Slop puro | El párrafo existe solo para ocupar espacio | 🔴 |

La equivalencia es una **propuesta de trabajo** (ver pendientes en `HANDSHAKE.md`): el semáforo mira cinco preguntas y el puntaje mide proporción de relleno, así que pueden discrepar; cuando lo hagan, manda la lectura de las cinco preguntas con su motivo escrito.

El puntaje refleja **el bloque entero**, no su peor oración. Anclas de calibración aproximadas: una oración de definición limpia o una instrucción concreta, 5 a 10; una transición útil antes de una lista, alrededor de 30; la oración típica de relleno, 70 a 90. Un párrafo con datos concretos y una lista, cerca de 15; uno con apertura de plantilla, relleno y consigna final sin ningún dato, cerca de 80.

## 4. Excepciones SEO: lo que nunca se penaliza

En una página que debe posicionar, esto no es relleno:

- Repetir la keyword y sus variantes en titles, encabezados, introducción, preguntas frecuentes y cuerpo.
- Encabezados en forma de pregunta que coinciden con búsquedas reales.
- Preguntas frecuentes cuya respuesta repite la pregunta en la primera oración.
- Nombrar la entidad completa en lugar de usar un pronombre.
- Definiciones directas al comienzo de una sección, mientras cada una responda a una búsqueda distinta.

Lo que **sí** se penaliza:

- Relleno de keywords, sobre todo repetido dentro de una misma oración.
- Oraciones que existen solo para colocar la keyword.
- Redundancia de ideas: la misma información con otras palabras.

Esto aclara la sección 6 de [`06-semaforo-por-parrafo.md`](06-semaforo-por-parrafo.md): las recomendaciones de optimización (palabra clave en el title, longitudes) no son criterios de calidad, pero **tampoco deben convertir en rojo** un párrafo SEO legítimo. Las reglas de optimización viven en `seo-content-system`.

## 5. Dieciséis familias de señales

Sirven para nombrar el motivo de un puntaje alto. Ninguna prueba nada por sí sola; cuentan por acumulación y sin sustancia debajo. Las que ya tiene [`02-sintomas-de-texto.md`](02-sintomas-de-texto.md) no se repiten; aquí se indican solo con una línea.

| # | Familia | Qué buscar | ¿Ya está en 02? |
|---|---|---|---|
| 1 | Aperturas de relleno | "Es importante destacar que…", "En el mundo actual…" | Sí |
| 2 | Tics de énfasis | "juega un papel crucial", "sin lugar a dudas" | Sí (importancia inflada) |
| 3 | Jerga corporativa y verbos inflados | "navegar" por "manejar"; verbos grandilocuentes con objeto trivial | Parcial |
| 4 | Adverbios de relleno | "realmente", "básicamente". Los **funcionales** ("diariamente", "en ayunas") están bien | No |
| 5 | Metacomentario | "En este artículo exploraremos…", "En conclusión…" | Sí |
| 6 | Afirmaciones vagas | Dicen que algo importa sin decir nada concreto | Parcial |
| 7 | Adjetivos inflados sin respaldo | "tratamiento adecuado" sin decir cuál | Sí (tono de folleto) |
| 8 | Contrastes binarios forzados | "No se trata de X, sino de Y" | Sí |
| 9 | Fragmentación dramática | Frases cortas sueltas y cierres de consigna | Parcial |
| 10 | Preguntas retóricas de relleno en el cuerpo (las de preguntas frecuentes están exentas) | "¿Y sabes qué? …" | No |
| 11 | Falsa agencia | Cosas inanimadas que actúan como personas ("el mercado decide") | No |
| 12 | Fuente impersonal | "Se ha demostrado que…" sin fuente; riesgo YMYL | Sí (atribuciones vagas) |
| 13 | Narrador distante | "Es común que la gente…" | No |
| 14 | Absolutos perezosos | "siempre", "nunca", "todos" | No |
| 15 | Tríadas y ritmo mecánico; abuso de la raya | | Sí |
| 16 | Consejo de salud genérico | "consulta a tu médico" sin concretar. Una advertencia médica **concreta** está limpia | No |

Las familias 3, 4, 10, 11, 13, 14 y 16 son aportes nuevos: quedan como **candidatas** (nivel de [`02-sintomas-de-texto.md`](02-sintomas-de-texto.md)) hasta que se repitan en varios casos o las apruebe Guille. El detector `slop_lint.py` **todavía no las busca** (ver `HANDSHAKE.md`).

## 6. Lo que baja el puntaje

Cifras, dosis, tiempos, nombres de sustancias o herramientas, síntomas específicos, pasos accionables, encabezados y preguntas frecuentes (salvo que sean absurdamente genéricos), repeticiones SEO legítimas y explicaciones técnicas necesarias, **sea cual sea su longitud**.

## 7. Las cinco dimensiones del artículo (1 a 10; 10 es lo mejor)

| Dimensión | Pregunta |
|---|---|
| Directo | ¿Afirma las cosas o las anuncia? |
| Ritmo | ¿Varía la longitud y la forma de las oraciones o es monótono? |
| Confianza | ¿Respeta la inteligencia del lector? |
| Autenticidad | ¿Suena a alguien que conoce el tema? |
| Densidad | ¿Hay oraciones que se pueden borrar? |

**Regla de coherencia:** si la suma es menor de **35 sobre 50**, el puntaje global del artículo debe ser **41 o más**. Y el puntaje global **no es el promedio** de los bloques: refleja la proporción de contenido sin información, los tics repetidos y las dimensiones bajas. Las dimensiones son juicio humano y no hay detector que las mida.

## 8. Salida estructurada (para hojas y scripts)

Cuando la revisión alimenta una hoja o una automatización, se puede devolver este JSON, en español. En una conversación normal se usa la tabla del semáforo.

```json
{
  "score": 52,
  "resumen": "Diagnóstico en una o dos oraciones.",
  "hallazgos": ["3 a 5 patrones, cada uno con un fragmento corto citado"],
  "dimensiones": {"directo": 6, "ritmo": 5, "confianza": 7, "autenticidad": 5, "densidad": 5},
  "bloques": [
    {"id": "b1", "score": 18, "motivo": ""},
    {"id": "b2", "score": 77, "motivo": "Máx. 30 palabras: nombra la señal y cita el fragmento que se puede borrar."}
  ]
}
```

Reglas: un elemento por bloque y en orden; `motivo` vacío si el bloque puntúa menos de 41; los motivos **nombran la señal y citan el fragmento exacto** que se puede borrar (no "reescribir"). Igual que en el semáforo, se anota **qué falta** en cada bloque alto.

## 9. Cómo se usa junto al semáforo

1. Correr el semáforo provisional (`slop_lint.py --semaforo`) y leer los rojos y amarillos con las cinco preguntas.
2. Si se necesita comparar o priorizar, puntuar los bloques con este archivo. Atacar primero los de mayor puntaje que también fallan P1 y P2.
3. Antes de dar por malo un bloque con keyword repetida, comprobar la sección 4: ¿es una excepción SEO legítima?
4. Dejar en el informe el semáforo del documento y, si se usó, el puntaje global con sus cinco dimensiones.

## 10. Calibración pendiente

Los puntos de corte, la equivalencia con el semáforo y la regla de 35 sobre 50 no se han probado contra casos reales de Guille. Hasta entonces, el color final lo decide quien revisa con motivo escrito; registrar cada discrepancia entre puntaje y semáforo en el HANDOFF.
