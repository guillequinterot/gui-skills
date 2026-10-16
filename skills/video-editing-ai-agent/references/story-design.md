# Diseño de la historia: explainer y piezas narradas (v1.3)

Adaptado y **reescrito** de `faceless-explainer/references/story-design.md`, `hyperframes-creative/references/{story-spine,narration,beat-direction}.md` y `faceless-explainer/references/motion-language.md` de HyperFrames (HeyGen, Apache-2.0; `NOTICE.md`), leídos el 2026-10-16. Cubre **qué enseña la pieza, en qué orden y por qué existe cada escena**. No define diseño visual (eso es `direct-visual-design`) ni la animación (`motion-doctrine.md`). Sirve para un video con narración o con texto que enseña algo, y para el video desde cero del QA final.

## Regla central
Un artículo es un volcado de información; un video es **un acto guiado de comprensión**. No sigas el orden de los párrafos: reordena, une, omite y comprime en una secuencia de enseñanza. Quita los incisos y muestra la columna vertebral. **El fallo más común es parafrasear el texto fuente en orden: no lo hagas.**

## 1. Extraer la verdad que se enseña
- **Público** — a quién habla y qué (no) sabe ya. · **Brecha o apuesta** — la confusión o el "por qué importa" que la explicación resuelve. · **Tesis** — la idea de una línea con la que se va el espectador. · **Columna** — 3–6 ideas (mecanismos, pasos, ítems) que construyen la tesis. · **Evidencia** — números, ejemplos, comparaciones o casos concretos. · **Aterrizaje** — la conclusión o la llamada a pensar, probar o actuar.
- Escribe el storyboard alrededor de **la tesis**, no de las secciones del artículo.

## 2. Valor primero (el "iceberg invertido")
1. **El gancho habla el idioma del espectador:** responde "¿por qué me importa?" en términos de resultado (lo que gana, evita o por fin entiende). Prohibido en el gancho el vocabulario interno del tema (nombres de archivo o función, lista de características, los títulos de sección del texto fuente). Los números solo valen si llevan una apuesta ("40 % más rápido al arrancar"), no inventario ("23 archivos cambiados").
2. **El valor llega antes de la escena 2.** Todo lo que sigue es evidencia a su servicio. Autocomprobación sobre la lista terminada: borra todas las escenas de evidencia — las restantes deben seguir enunciando el valor; borra las de valor — si el video "sigue funcionando", era un recorrido de funciones, no una historia.
3. **La propuesta no es un listado** (ver `production-workflow.md` §7): "Este video le dice a [público] que [mensaje]" + tabla con el "por qué" de cada escena.
4. **Los visuales apuntan a la fuente:** si la pieza deriva de material concreto, sus frases, entidades, verbos y motivos recurrentes son el atrezo. Autocomprobación por visual: si el elemento podría aparecer igual en el video de otro producto, no salió de la fuente; cámbialo por algo que solo este tema podría producir.

## 3. Elegir **una** estructura (no mezclar fases de dos)
| Estructura | "Es…" | Úsala cuando el contenido es… | Forma del cuerpo |
|---|---|---|---|
| `concepto` | "qué es X y por qué importa" | una idea o fenómeno que el público conoce a medias | nombrar el concepto → revelar el mecanismo por capas → aterrizar la implicación |
| `procedimiento` | "así se hace / así funciona" | pasos ordenados con inicio y fin claros | 3–6 pasos sobre un mismo escenario visual, un movimiento por paso |
| `lista` | "N cosas sobre X" | ítems paralelos y de igual rango (consejos, errores, razones) | gancho → N ítems casi iguales → cierre; la regla de tres es la más fuerte |
| `historia` | enseñar con un arco narrativo | casos, historias, relatos con moraleja | planteamiento → tensión → giro → resolución → lección que se generaliza |
Elige: una idea que entender → concepto; un procedimiento ordenado → procedimiento; ítems paralelos → lista; un caso concreto → historia. Los compuestos (arco externo + ritmo interno, p. ej. `concepto con procedimiento`) se nombran explícitamente en el `arco`.

## 4. Secuencia de escenas: cada una con **un trabajo**
Evita escenas que solo digan "más detalle" o "otro punto". Cada escena define: `tipo` (gancho, dolor, concepto, mecanismo/paso/ítem, implicación, evidencia, tesis, llamada), `persuasión` (una técnica **con nombre**, no "explicar la idea"), `beat` (el sentimiento objetivo, no un genérico "positivo"), `escena` (una línea visual), `voz`, `transición de entrada`, y en el texto: **función narrativa** ("concreta el interés compuesto como una bola de nieve", no "muestra un gráfico") y **mensaje clave** (una frase).
- El cuerpo suele ser **3–6 escenas sobre un mismo escenario visual**, cada una avanzando un mecanismo, paso, ítem o capa, **construyendo comprensión acumulada**; una escena de cuerpo aislada casi nunca enseña nada.
- **Continuidad:** un *escenario consistente* (misma idea de composición en escenas consecutivas: el mismo diagrama que crece, la misma recta numérica) y una *transición consistente* (un tipo de costura repetido en la secuencia). Cuando un elemento **se transforma** entre dos ideas (un nodo se vuelve barra, una fórmula se vuelve su resultado) mantenlo **dentro de una escena** como un beat de desarrollo, no partido por una costura.
- **Transiciones:** 2–3 tipos para todo el video, repetidos; la primera escena es corte. Pasos ordenados → un empuje consistente; revelado suave de capas → fundido; acercarse a un detalle → zoom-through; cambio limpio de tema o ítem nuevo → corte.

## 5. Estrategias de gancho (los 3–5 primeros segundos)
Abre una **brecha cognitiva o una apuesta**; nunca una definición genérica. Elige una:
| Estrategia | Úsala cuando… | Ejemplo |
|---|---|---|
| Estadística que sacude | un número creíble cuantifica la apuesta | "El 90 % del plástico fabricado nunca se ha reciclado." |
| Pregunta retórica | quieres abrir la brecha ya | "¿Por qué el tiempo parece ir más rápido al envejecer?" |
| Afirmación contraintuitiva | la verdad contradice la creencia común | "Añadir carriles a una autopista empeora el tráfico." |
| Validar el dolor | el público ya siente la confusión | "Todos dicen 'diversifica'; nadie dice qué significa." |
| Metáfora visceral | la idea es abstracta y debe hacerse concreta | "Tu atención es un foco y las apps pelean por el interruptor." |
| Anuncio del concepto | el término mismo es el tema | "Hay una palabra para esto: el efecto espectador." |
| Apelación directa | el público está bien definido | "Si alguna vez abandonaste una receta a medias, esto es para ti." |
| Imagina / escenario | un experimento mental enmarca todo | "Imagina un dinero que pierde valor si no lo gastas." |
| Apuesta / consecuencia | el "por qué ahora" es un costo real | "Falla un solo paso y se pierde todo el lote." |
La tesis (`mensaje`) aterriza **antes de la escena 2**. **Varía el tipo de gancho** entre piezas; no abras siempre con una cifra.

## 6. Catálogo de técnicas de claridad (la `persuasión` de cada escena)
| Familia | Técnicas |
|---|---|
| Hacer concreto | analogía o metáfora · concretización (de lo abstracto a un objeto) · ejemplo resuelto con números reales · anclar en algo familiar |
| Revelar en orden | divulgación progresiva (un término o capa a la vez) · construcción (de lo simple a lo general) · señalización ("primero… luego… por último") |
| Contraste | antes/después · creencia común contra realidad · comparación de dos opciones · contraejemplo (aquí es donde falla) |
| Estructura | regla de tres · enumeración numerada · pareja pregunta→respuesta · marco y relleno (enuncia la forma, luego la llenas) |
| Evidencia | prueba estadística · cita o fuente · demostración (mostrar el mecanismo funcionando) · cadena causal (A → B → C) |
| Memoria y aterrizaje | eco (volver a la imagen del gancho) · destilación (comprimir a una línea) · término acuñado o regla mnemotécnica · generalización (de lo específico al principio) |
Si ninguna encaja, **nombra una nueva en línea** y explica su mecanismo. Nunca escribas un genérico "explicar la idea".

## 7. Arco emocional (`beat`)
Un explainer recorre un arco de comprensión; usa una palabra específica o un compuesto, no "positivo" o "interesado".
- **Valle negativo** (abrir la brecha: gancho, dolor): curiosidad · desconcierto · sorpresa · tensión · preocupación · escepticismo · reconocimiento · intriga.
- **Giro** (orientar: nombrar el concepto): claridad · orientación · anticipación · foco.
- **Construcción** (cuerpo): comprensión · "ajá" · confianza · fascinación · previsión · impulso · convicción · deleite · inquietud (para una salvedad) · dominio.
- **Resolución** (aterrizar: tesis, cierre): claridad · satisfacción · decisión · inspiración · inevitabilidad · "ahora lo entiendo".
Los compuestos suelen ser los más fuertes ("sorpresa + reconocimiento", "comprensión + deleite").

## 8. Dirección de cada beat (el "mundo" de la escena)
Cada beat es un **mundo, no un layout**: antes de escribir CSS y GSAP, describe lo que el espectador **experimenta**.
- Mediocre: "Fondo azul marino oscuro. '1.9T' en blanco, 280 px. Logo arriba a la izquierda."
- Bueno: "La cámara ya va a mitad de vuelo sobre un lienzo oscuro y vasto. La ola de degradado barre el cuadro como una aurora, viva, cambiante. '1.9T' IRRUMPE con tanta fuerza que la ola responde con una onda. Esto no es una diapositiva: es un momento." Escribe lo segundo y después averigua los píxeles.
- Cada beat lleva: **concepto** (2–3 frases: qué mundo, qué metáfora, qué debe *sentir* el espectador — lo más importante), **dirección de ánimo** (referencias culturales y de diseño, no hex), **coreografía** (un **verbo** de movimiento por elemento — si no puedes nombrar el verbo, el elemento aún no está diseñado; el verbo sale del concepto, no de un cubo de "alta energía"), **transición** (tipo y parámetros), **capas de profundidad** (al menos 2: fondo, medio, primer plano), **efectos de sonido** (qué suena y cuándo, o el silencio elegido).
- Verbos por carácter físico: **impacto/peso** (irrumpe, estrella, golpea, sella, rompe, cae con fuerza) · **direccional** (desliza, empuja, tira, barre, corta) · **revelado/construcción** (dibuja, rellena, crece, expande, ensambla, cuenta hacia arriba) · **orgánico** (flota, deriva, respira, pulsa, orbita, se transforma) · **mecánico** (teclea, hace clic, encaja, chasquea, avanza por pasos).
- **Ritmo:** antes de escribir HTML, **declara el ritmo de la pieza** y nómbralo (rápido-rápido-LENTO-rápido-IMPACTO-pausa). Se deriva del storyboard y de la marca, no de una tabla: dos anuncios de 15 s (un estudio de arquitectura y una marca de videojuegos) no comparten ritmo. Preguntas: ¿qué viaje emocional hace el espectador y dónde está el pico? ¿dónde cae el mayor énfasis de la narración (ahí suele ir el pico de energía)? ¿qué sugiere el ritmo visual de la marca? ¿cuántos beats soporta de verdad la duración sin apurarse ni rellenar? Un anuncio social que intenta gancho en 2 s, tres funciones y una llamada en 15 s es ruido; a veces "gancho–pausa–llamada" con una sola función es lo correcto.
- **Qué tipo de costura:** *shader* para revelados, reacciones grandes, presentaciones de producto o logo y cambios de energía (todo momento que la música o la voz puntúan con un golpe); *CSS* para beats de cámara continua y ritmos editoriales mínimos; *corte seco* para listas rápidas, cortes percusivos al compás y humor. Si el beat es el **centro** del video, costura con shader; si es tejido conectivo, un fundido basta. Un reel de marca de 5–7 beats suele querer 1–2 transiciones de shader (la revelación principal y la llamada final): demasiadas aplanan su impacto.

## 9. Guion y narración
- **Ritmo de habla: 2.5 palabras por segundo.** 15 s ≈ 37 palabras · 30 s ≈ 75 · 60 s ≈ 150. Deja espacio para pausas: **el silencio entre frases es un recurso, no tiempo muerto**. El guion debe *sentirse* más corto que el video.
- **Tono:** escribe como persona, no como folleto: contracciones, frases de longitud variada (cortas y contundentes mezcladas con otras largas y fluidas), léelo en voz alta; si suena robótico, reescríbelo; sin jerga salvo que el público la espere. Frases por escena de voz: 1–2, normalmente 6–20 palabras; concretas y humanas; enseña, no leas el artículo en voz alta.
- **Escribe cada línea como señales discretas, no como un solo aliento.** La pieza revela cada elemento en pantalla *cuando la voz lo nombra* (el mecanismo anti-diapositiva); una línea con límites claros de frase ("Primero la bola de nieve, luego la colina, luego la velocidad") le da a la escena su cadencia de revelado gratis; una cláusula larga no le da ritmo a nada. Fuerte: "El interés compuesto no es suma, es una bola de nieve: cada vuelta recoge la nieve de la anterior, y más." Débil: "El estudio, publicado en 2019, examinó tres cohortes y encontró que…" — eso es leer, no explicar.
- **Pronunciación de cifras:** la voz sintética lee literal; escribe lo que quieres que diga. `135+` → "más de ciento treinta y cinco" · `$1.9T` → "casi dos billones de dólares" · `99.999 %` → "noventa y nueve coma nueve nueve nueve por ciento" · `10x` → "diez veces" · `API` → "A P I" · `sitio.com` → "sitio punto com". La pantalla puede mostrar la cifra exacta mientras la voz redondea.
- **Estructura de piezas de producto:** gancho → historia (qué hace, quién lo usa, concreto) → prueba (cifras, nombres, prueba social **reales**) → llamada a la acción. No hace falta todo: un anuncio social de 15 s puede ser gancho + prueba + llamada.
- **La línea de apertura** es la frase más importante: debe crear tensión, curiosidad o sorpresa en 3 s. Si es genérica ("Bienvenidos a…", "Presentamos…"), empieza de nuevo.
- **Evitar:** "Desbloquea el poder de…", "experiencia sin fisuras", listas largas de sustantivos, una escena que sea solo un puente de relleno.
- **Escenas mudas** están permitidas y son comunes en explainers (un diagrama que se ensambla solo, un ejemplo que se anima, un beat de tensión sostenida antes de un giro): `voz` vacía y la escena queda fuera del guion; entonces `función narrativa` + `persuasión` deben cargar lo que el guion no dice.
- **Modos con guion del cliente:** *reestructurar* (el texto es material: reescribe, reordena, une u omite para la estructura y la duración elegidas) o *literal* (no cambies sus palabras: segmenta en trozos del tamaño de una escena en límites de oración o párrafo; la duración final la marca el guion). **El copy oficial del cliente manda** (`captions-subtitles.md`).

## 10. Música y silencio
La música es un estado de ánimo declarado en el storyboard (`música: …`). `música: ninguna` apaga la música (la narración sigue). **Sin música + sin guion + sin efectos = el marcador de video totalmente silencioso**: no se genera nada. La música y los efectos se **aportan o aprueban por el usuario** (`audio-mix.md`); no se inventan.

## 11. Lista final antes de pedir aprobación
Una estructura nombrada (compuesta solo si se nombró) · la secuencia sigue la narrativa, no el orden de párrafos · la apertura usa una estrategia de gancho nombrada · cada escena tiene un trabajo y el cuerpo construye de forma acumulada · cada escena tiene `tipo`, `persuasión` (técnica con nombre) y `beat` (específico) · cada línea de voz está segmentada en señales, no en una cláusula larga · el arco emocional varía de acuerdo con la estructura · transiciones: 2–3 tipos repetidos y corte en la primera escena · un escenario y una transición consistentes sostienen toda secuencia de varias escenas · sin inventario de recursos salvo los que el usuario aportó · el guion solo contiene la narración bloqueada.
