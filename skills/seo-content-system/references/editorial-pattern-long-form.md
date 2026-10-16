---
tags:
  - seo
  - redaccion
  - geo
---

# Patrón editorial de artículo largo con autoridad (modelo Los Creativos)

## Índice

- Principio
- Métricas medidas del modelo
- Arquitectura del artículo
- Rasgos de voz
- Recursos explicativos
- Lo que el patrón evita deliberadamente
- Cómo aplicarlo sin copiar
- Errores frecuentes
- Lista de revisión

## Principio

Este patrón describe la estructura y la voz de un artículo de investigación divulgativa que funciona como **agrupador citable**. Se documentó midiendo un artículo real cuyo enfoque es coherente con los hallazgos de [ai-citation-and-geo-playbook.md](ai-citation-and-geo-playbook.md): autoridad humana declarada, prosa natural y valor resolutivo concentrado en una sola URL.

No es una plantilla para rellenar. Es un conjunto de decisiones editoriales con su razón.

## Métricas medidas del modelo

Medición directa sobre el artículo de referencia (agosto 2026):

| Rasgo | Valor medido | Lectura |
|---|---|---|
| Extensión | ~6.100 palabras | Agrupador extenso, no artículo de blog corto |
| Párrafos | 131 | — |
| Palabras por párrafo | mediana 45 (media 46,6) | Párrafos sustanciales, ~3 frases |
| Palabras por frase | mediana 24 | Frases largas y subordinadas |
| Frases de 30+ palabras | 33 % | Un tercio son frases complejas |
| Frases de 12 o menos palabras | 21 % | Ritmo variable, no uniforme |
| Elementos de lista (`li`) | 37 en 6.100 palabras | **Muy pocas listas** para la extensión |
| Negritas (`strong`) | 98 | Énfasis léxico frecuente |
| Tablas | 10 | Los datos van en tabla, no en prosa |
| Enlaces | 29 | Ecosistema interno y fuentes |
| Encabezados | 6 H2, 20 H3, 3 H4 | Jerarquía profunda y ordenada |

El dato más contraintuitivo: **densidad de listas muy baja y frases largas.** Es lo contrario del patrón de "contenido escaneable" con viñetas cada tres líneas, y coincide con el hallazgo de que la IA premia la prosa fluida de experto.

## Arquitectura del artículo

Orden observado, con su función:

1. **Bloque de autoría, antes del contenido.** Nombre completo, formación, años de experiencia, cargo actual y organización, para cada persona implicada. Se distingue el rol: "investigación por X", "interpretación y divulgación práctica por Y". Ancla EEAT desde el primer píxel.
2. **Nota de resumen disponible.** Se ofrece un resumen descargable, aclarando que se recomienda leer el texto completo.
3. **Contexto del trabajo previo.** Qué se publicó antes, qué sostenía y por qué era todavía una hipótesis.
4. **La pregunta central**, formulada de forma explícita y honesta.
5. **Marco conceptual** ("¿Qué es X? Un repaso antes de entrar al experimento").
6. **Diseño y método**: variables de control, variable independiente, herramientas, un ejemplo real, y por qué se eligió ese contexto.
7. **Resultados por termómetro de medición**, cada fuente de datos por separado, y luego cómo se cruzan.
8. **Caso de validación a escala** que amplifica el hallazgo.
9. **Explicación del porqué**, con analogía primero y mecanismo técnico después.
10. **Conclusiones en tres partes**: qué confirma, qué corrige, qué queda abierto.
11. **Cierre con límites reconocidos** y CTA conversacional, no comercial agresivo.

Los encabezados combinan enunciado y aclaración con punto seguido:

> Conclusiones. Qué confirma, qué corrige y qué preguntas deja abiertas este experimento
> Lo que queda abierto. Honestidad sobre los límites de este ejercicio

Y muchos son preguntas reales del lector:

> ¿Por qué ocurre esto? La explicación detrás del hallazgo
> ¿Cómo se construyó la prueba?

## Rasgos de voz

- **Primera persona del plural con la organización:** "Hace unos meses publicamos…", "Hemos desarrollado…", "en Los Creativos seguimos documentando…". Nunca "nosotros" vacío: siempre asociado a un acto verificable.
- **Contrato explícito con el lector sobre el lenguaje técnico.** El artículo declara que si usa un término técnico sin explicarlo, es un error propio. Cumplirlo.
- **Definición en línea entre paréntesis**, sin desviarse a un glosario: "PMI (información mutua puntual)", "los dos corpus (el conjunto de artículos comparados)".
- **Conceptos propios en mayúscula inicial** cuando son entidades del marco: Entidad, Señales, Densidad de Señales, Knowledge Graph. Coherente con el trabajo de entidades.
- **Honestidad intelectual sostenida**: "seguía siendo, en esencia, una hipótesis", "este rompecabezas todavía incompleto", "buena parte de lo que hoy parece intuición todavía espera su turno de convertirse en evidencia".
- **Atribución nominal de fuentes**: no "estudios demuestran", sino "una investigación conjunta entre Anthropic, el Alan Turing Institute y el UK AI Security Institute".
- **CTA consultivo**: invita a conversar sobre aplicar los hallazgos, no a comprar.

## Recursos explicativos

- **Analogía antes que mecanismo.** El bingo para explicar acumulación de señales; la esfera y la eficiencia energética para explicar por qué gana el agrupador. Primero la intuición, después la técnica.
- **Tablas para todo dato comparativo.** Nunca describir en prosa una comparación de cifras que cabe en una tabla.
- **Ejemplo real y nombrado** en medio del método (una ciudad concreta, un caso concreto).
- **Distinciones explícitas** cuando dos conceptos suelen confundirse, con encabezado propio para cada uno.

## Lo que el patrón evita deliberadamente

- Viñetas como estructura por defecto: la prosa carga el argumento.
- Frases cortas encadenadas al estilo de contenido generado.
- Apertura genérica de tipo "En el mundo actual…".
- Adjetivación promocional sobre la propia agencia dentro del cuerpo.
- Cifras sin fuente nombrada.
- Conclusiones más seguras de lo que el dato permite.
- Resúmenes artificiales al final de cada sección.

## Cómo aplicarlo sin copiar

Este patrón sirve cuando hay **algo real que contar**: una investigación, un experimento, datos propios, un caso con cifras. Aplicarlo a contenido sin sustancia produce un artículo largo y vacío, que es peor que uno corto y honesto.

Antes de usarlo, verificar:

- ¿Hay autoría real que se pueda nombrar y respaldar?
- ¿Hay datos propios o fuentes primarias nombrables?
- ¿El tema justifica varios miles de palabras en una sola URL?
- ¿Se puede sostener la honestidad sobre los límites?

Si alguna respuesta es no, elegir otro formato. Ver [content-brief-and-architecture.md](content-brief-and-architecture.md).

Adaptar además la voz a la marca del proyecto: este patrón es el de una agencia que divulga investigación. Ver [brand-voice-and-language-variants.md](brand-voice-and-language-variants.md).

## Errores frecuentes

- Copiar la extensión sin tener la sustancia.
- Imitar la voz "nosotros" sin actos verificables detrás.
- Poner autores genéricos para simular EEAT.
- Usar analogías decorativas que no explican el mecanismo.
- Declarar el contrato de claridad y luego dejar tecnicismos sin definir.
- Convertir el patrón en plantilla rígida y perder la variación de ritmo.

## Lista de revisión

- ¿Hay bloque de autoría con credenciales verificables antes del contenido?
- ¿La pregunta central está formulada de forma explícita?
- ¿Cada dato comparativo está en tabla?
- ¿Cada término técnico se define la primera vez que aparece?
- ¿Las fuentes están nombradas, no aludidas?
- ¿Existe una sección honesta de límites y preguntas abiertas?
- ¿La proporción de listas es baja y la prosa sostiene el argumento?
- ¿El ritmo alterna frases largas y cortas, sin uniformidad mecánica?
- ¿El CTA es consultivo y coherente con el tono?
