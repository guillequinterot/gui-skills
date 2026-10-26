# Semáforo por párrafo: criterios de revisión

> Para revisar un contenido ya hecho, párrafo por párrafo, y decir si cada uno es slop o no con una regla que se pueda
> repetir. **Un párrafo no es slop por cómo suena, sino por lo que no aporta.** Por eso el semáforo mide cinco cosas
> (novedad, especificidad, respaldo, lo propio, función) y usa los síntomas de lenguaje solo como pista.

## 1. De dónde salen los criterios

Se leyeron ocho fuentes (2026-10-26). Cada criterio de abajo está en al menos dos; las etiquetas `[H] [W] [R] [S] [O] [I] [B] [V]` dicen cuáles.

| Etiqueta | Fuente | Qué aporta al semáforo |
|---|---|---|
| `[H]` | HubSpot, «fórmula para escribir un blog» | Cada párrafo aporta información nueva o ejemplos; un texto corto y denso gana a uno largo con relleno; afirmaciones con datos verificables, no frases vagas; voz activa, términos técnicos definidos; la introducción cumple lo que promete; releer en voz alta y pedir revisión externa |
| `[W]` | WeComm, glosario «AI slop» | Tres rasgos: volumen, falta de especificidad, ausencia de revisión. Señales: frases de relleno sin desarrollar, consejos obvios sin decir cómo ni para quién, ausencia de pruebas (casos, cifras, capturas), mismo tono para sectores distintos, fuentes inventadas o «expertos» sin nombre. Prueba práctica: si no queda claro qué se aprende, es slop |
| `[R]` | Redactor Freelance, trucos para blogs | Cada idea directa, sin repetir palabras clave; temas útiles para la comunidad; citar siempre las fuentes y no copiar; muchos lectores escanean antes de leer (subtítulos, listas) |
| `[S]` | Salesforce, contenido auténtico con IA | Apariencia pulida pero vacía; falta de punto de vista (la IA sin guía replica el promedio de internet); volumen sin estrategia; las personas ponen idea, criterio y empatía, la IA lo repetitivo; datos propios del cliente para no caer en lo genérico |
| `[O]` | OpenArt, cómo evitar el AI slop (imagen) | Uniformidad, prompts prestados, publicar la primera generación sin curar, no editar después. Para texto es una **extrapolación**: brief claro, descartar variantes, editar siempre |
| `[I]` | ImpactoTIC, AI slop en empresas | «Workslop»: se ve profesional pero no ayuda a decidir. Señales: obviedades bien redactadas, datos inventados con seguridad, no responde lo pedido, sin experiencia propia, sin voz de la organización, cuesta más revisar que escribir. Cinco preguntas antes de publicar |
| `[B]` | BrandCrops, el consumidor penaliza el slop | Mensaje genérico rinde menos aunque nadie detecte la IA; test de intercambiabilidad (sin logo, ¿podría ser de la competencia?); lo que más daña es el uso no declarado; revisión editorial humana de copy y datos |
| `[V]` | Video de YouTube (zpcokOxIrY8), trucos de contenido | Hablar de lo que se sabe; estilo propio y naturalidad; repasar ortografía; destacar lo importante con negritas/citas; CTA con sentido; usar la IA para **ayudar**, no para crear sin más. **Parte del video se rechaza** (ver §6) |

**Fuente 9:** el mensaje llegó con el punto 9 vacío; no se evaluó ninguna fuente adicional.

## 2. Las cinco preguntas (se responden por párrafo)

| # | Pregunta | Falla cuando… | Fuentes |
|---|---|---|---|
| **P1 Novedad** | ¿Qué sabe el lector después de este párrafo que no sabía antes? | Repite el título, el párrafo anterior o algo obvio; «consejos» sin decir cómo aplicarlos; reformula la idea con otras palabras | H W I |
| **P2 Especificidad** | ¿Podría estar en el artículo de cualquier otra marca o tema sin cambiar nada? | Se puede cambiar el nombre, la ciudad o el sector y sigue valiendo; tono idéntico para sectores distintos | W B S |
| **P3 Respaldo** | Lo que afirma como hecho, ¿tiene fuente, cifra con origen o ejemplo comprobable? | «Los expertos coinciden», «según estudios», cifras sin origen, fuentes que no existen o no dicen eso | H W I R |
| **P4 Lo propio** | ¿Hay algo que solo esta persona o marca puede decir: experiencia, dato interno, criterio con sus límites? | Cobertura neutra y simétrica («tiene ventajas y desventajas») sin posición; ninguna experiencia; sin «depende de…» | S I V H |
| **P5 Función** | ¿Cumple un papel para el lector (responde su pregunta, da un paso, enlaza dos ideas en una frase, invita a una acción con sentido) o es relleno? | Anuncia lo que va a decir; resume lo que acaba de decir; adorno que se puede borrar sin pérdida; no responde lo que el lector buscaba | H W I |

Una **pista de legibilidad** acompaña a las cinco (no puntúa como slop): párrafos de más de unas 120 palabras o sin ningún destacado en textos largos dificultan el escaneo `[H] [R] [V]`. Solo puede dejar un párrafo en amarillo si ya tenía otro motivo; nunca lo vuelve rojo.

## 3. Qué se le exige a cada tipo de párrafo

No todo párrafo tiene que traer una cifra. Exigirlo daría falsos amarillos. Se clasifica primero y se exige solo lo que corresponde:

| Tipo | Qué es | Obligatorio | No se le exige |
|---|---|---|---|
| Apertura | Primer párrafo de la pieza o de una sección | P5, P2 (empezar por el problema o el dato, no por «en el mundo actual») | P3 si no afirma hechos |
| Definición | Explica un término | P1, P2, P3 (si cita una norma o un dato) | P4 |
| Paso / instrucción | Dice cómo hacer algo | P1, P2 (con el detalle que lo hace ejecutable: herramienta, ajuste, orden) | P4 |
| Dato / hecho | Afirma algo verificable | P1, **P3**, P2 | P4 |
| Ejemplo / caso | Muestra un caso concreto | P1, P2, **P4** (de dónde sale: propio, con permiso, o fuente) | P3 salvo que cite cifras |
| Criterio / opinión | Recomienda o compara | P4 (posición y «depende de…»), P2 | P3 salvo que cite hechos |
| Transición | Una o dos frases que unen secciones | P5 | P1–P4 |
| CTA | Invita a una acción | P5 (relevante al punto donde aparece) | P1–P4 |
| Cierre | Último párrafo | P5 (siguiente paso útil, no resumen) | P3 |

## 4. Reglas del semáforo (por párrafo)

El orden importa: se mira de arriba hacia abajo y gana la primera regla que se cumpla.

### 🔴 Rojo — se arregla de fondo o se borra
Cualquiera de estas:
1. **Resto objetivo**: marcador sin completar, frase del chatbot, enlace con `utm_*`.
2. **Hecho que no se sostiene**: cifra, estudio, cita, caso o autor que no existe, no se encuentra o no dice lo que se le atribuye (P3 grave). También la atribución vaga («los expertos coinciden») **sobre una afirmación que el texto necesita como prueba**.
3. **Ni nuevo ni propio**: falla P1 **y** P2 (nada que el lector no supiera y lo diría cualquiera). Borrar, o reescribir desde cero con material propio.
4. **Copia o paráfrasis de contenido ajeno** hecha para «parecer distinto» (ver §6).

### 🟡 Amarillo — falta algo debajo
Cualquiera de estas (sin que se cumpla ningún rojo):
1. Falla **una** de P1–P5 (la que corresponde a su tipo, §3).
2. Es correcto pero **intercambiable**: se arregla con un dato, un ejemplo o una experiencia real.
3. Tiene **síntomas de lenguaje o formato** del detector (importancia inflada, tono de folleto, muletilla, cierre de resumen, meta-anuncio) **y** nada concreto que los sostenga.
4. Cifra sin fuente cercana (en el mismo párrafo o con enlace).
5. Pista de legibilidad más otro motivo.

El arreglo siempre es **añadir lo que falta** (dato con fuente, ejemplo, posición) o recortar. Cambiar palabras no baja un amarillo a verde.

### 🟢 Verde — pasa
Cumple las preguntas de su tipo (§3) y no hay síntoma sin sustancia. **Un síntoma de lenguaje aislado en un párrafo que sí aporta** (por ejemplo, una tríada que resulta ser real) **se queda en verde** y se anota como observación: el síntoma no prueba nada.

## 5. Del párrafo al documento

| Documento | Cuándo | Decisión |
|---|---|---|
| 🟢 Verde | 0 rojos y menos de un cuarto de párrafos amarillos, con procedencia clara (paso 3 de la puerta) | Publicar |
| 🟡 Amarillo | Algún rojo corregible, o amarillos en más de un cuarto de los párrafos | Reescribir los marcados y volver a pasar solo esos |
| 🔴 Rojo | Restos objetivos sin corregir, un tercio o más de rojos, o sin procedencia (autor, fuentes o revisión inventados) | Rehacer o descartar |

Los umbrales son una guía de trabajo, no una ley: una pieza de cinco párrafos con un rojo de hecho inventado ya es rojo. **El semáforo del documento nunca se calcula sin mirar los rojos uno a uno.**

Además del semáforo por párrafo, se miran cuatro cosas **de la pieza entera** (no de un párrafo):
- **Propósito** (¿para quién, qué problema, lo buscaría?) `[H] [W]`.
- **Procedencia y revisión humana** (¿quién firma, qué se hizo con IA, quién revisó?) `[I] [S] [B]`.
- **Promesa cumplida** (¿el título y la introducción se cumplen en el cuerpo?) `[H] [I]`.
- **Redundancia entre párrafos** (dos párrafos que dicen lo mismo → uno sobra) `[H] [W]`.

## 6. Lo que se toma de las fuentes y lo que se rechaza

- **Se rechaza el consejo del video [V] de «copiar los consejos de otro blog, pedir a ChatGPT que los explique con otras palabras y luego pedir que se parezca menos al original para que no te detecten»**. Es spinning: no hay nada propio, es contenido ajeno reescrito para ocultarlo, y el propio video admite que Google «tarde o temprano las va a pillar». Esa práctica se marca **roja** (regla 4). Lo que sí se aprovecha del video: hablar de lo que se sabe, estilo propio, repasar, CTA con sentido y usar la IA como ayuda.
- **Se matiza la regla del video «un texto sin negritas lo hizo la IA».** La guía de Wikipedia señala el **exceso** de negritas como síntoma; el video señala su **ausencia** en textos largos como falta de trabajo editorial. Ninguna de las dos prueba nada. Se usa solo la parte de legibilidad: un tocho sin ningún apoyo para escanear es difícil de leer `[R] [V]`.
- **Se descartan como criterios de slop** las recomendaciones de SEO de [H] y [R] (palabra clave en el título, longitud de la meta, 1.500–2.500 palabras): son de optimización, no de calidad, y las cubre `seo-content-system`. Imponer longitudes o densidades sería ingeniería lingüística forzada.
- **Se toman con reserva** [O] (es de imagen; se extrapola) y las cifras de [B] (42 %, estudio de 3.000 consumidores: las cuenta un blog de agencia, nivel *vendor/secundaria*, no se usan como criterio, solo como contexto).
- **Se toma con reserva** la cifra de Gartner de [I] (53 %): la cita un blog, no se verificó en el original.

## 7. Cómo se aplica (protocolo de revisión)

1. Correr `python <skill>/scripts/slop_lint.py <archivo> --semaforo`. Da una luz **provisional** por párrafo con su evidencia (restos, síntomas, anclajes concretos) y el resumen del documento.
2. **Leer cada párrafo rojo y amarillo** y decidir el color final con las cinco preguntas. El detector no ve novedad ni verdad: solo ve pistas.
3. **Leer también los verdes** con las cinco preguntas, sobre todo si el documento es largo: el detector da verde a un párrafo sin síntomas aunque no diga nada.
4. Para cada rojo y amarillo, escribir **qué falta** (no «reescribir»): `falta fuente`, `falta ejemplo propio`, `falta posición`, `sobra, borrar`.
5. Emitir el informe: tabla párrafo → tipo → luz → motivo (pregunta que falla) → qué falta, más el semáforo del documento y la decisión (publicar / reescribir / descartar).
6. Si el color final difiere del provisional, anotar por qué: así se afinan las reglas del detector con casos reales.

Plantilla del informe:

```
SEMÁFORO DEL DOCUMENTO: 🟡 Reescribir
Propósito: ok · Procedencia: falta revisor · Promesa cumplida: sí · Redundancia: P4 y P7 repiten

| # | Tipo | Luz | Falla | Qué falta |
|---|------|-----|-------|-----------|
| 1 | Apertura | 🟡 | P2 | Entrar por el problema, no por «en el mundo actual» |
| 2 | Dato | 🔴 | P3 | Cifra sin fuente: abrir el estudio o quitarla |
| 3 | Ejemplo | 🟢 | — | — |
```

Cosas que el detector hace al armar el semáforo (descubiertas probándolo con dos artículos reales, 2026-10-26):
- **Mención vs uso:** una frase entre «» o “” se toma como ejemplo citado y no cuenta como síntoma (un glosario sobre el slop cita frases de relleno y salía en rojo). Los restos objetivos sí se buscan dentro de comillas.
- **HTML:** se descartan `nav`, `header`, `footer`, `aside`, `form` y botones, y los bloques de menos de tres palabras no se evalúan (menús y etiquetas).
- **Falsos amarillos conocidos:** un párrafo largo de definición sin cifra ni nombre propio sale amarillo («pista P1/P2»). Es una invitación a mirarlo, no una condena: si el párrafo define bien, se pasa a verde con nota.
- **Falsos verdes conocidos:** un párrafo sin síntomas de lenguaje sale verde aunque no diga nada nuevo. Por eso los verdes se leen igual.

## 8. Límites

- El semáforo mide el **valor del párrafo**, no si lo escribió una IA. Un párrafo humano vacío sale amarillo o rojo igual; uno asistido por IA con un dato propio y fuente sale verde.
- No sustituye la verificación de hechos: P3 pide que haya respaldo; comprobar que el respaldo es cierto requiere abrir la fuente.
- Los umbrales (cuarto, tercio, 120 palabras) son iniciales y se ajustarán con casos reales. Hasta entonces, el color final lo decide quien revisa, con motivo escrito.
