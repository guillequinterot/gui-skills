# Qué es el slop y qué evidencia hay (verificado el 2026-10-26)

> Cada afirmación lleva su nivel: **primaria** (leída en la fuente oficial o en el estudio), **secundaria** (la cuenta un medio o un resumen) o **vendor** (la publica quien vende una herramienta relacionada). Fuentes con enlace en [`05-fuentes.md`](05-fuentes.md).

## 1. Definición

- **Slop** es el nombre que se le dio al contenido no pedido, generado con IA y no revisado, igual que *spam* nombró el correo no deseado. Quien lo popularizó en 2024 lo define como «contenido generado con IA que nadie pidió y que nadie revisó», aclara que **no todo contenido con IA es slop** y propone como mínimo ético «no publicar slop» (**primaria**: lectura de su artículo; él mismo dice que el término ya circulaba antes).
- El diccionario Merriam-Webster eligió «slop» palabra del año 2025 y lo define como contenido digital de baja calidad producido, por lo general en cantidad, con inteligencia artificial (**secundaria**: cobertura de la prensa del anuncio de diciembre de 2025).
- En español se explica igual: contenido que nadie pidió, generado con IA sin supervisión humana y de forma masiva, con el objetivo de generar ingresos, en texto, imagen o video (**secundaria**: artículo de un medio de tecnología en español, 2024).

**Definición de trabajo de esta skill:** slop = baja calidad + hecho con IA + en cantidad + sin propósito para el lector + sin revisión humana. Quitar cualquiera de los tres últimos elementos cambia el caso: una pieza con IA, útil, con sustancia propia y revisada **no** es slop.

## 2. Lo que dicen las plataformas (política, no opinión)

| Plataforma | Qué dice | Nivel |
|---|---|---|
| **Google Search** | La política de **abuso de contenido a escala** prohíbe generar muchas páginas con el fin principal de manipular el posicionamiento, **sin importar cómo se hagan** (IA, personas o automatización). Entre los ejemplos: usar IA generativa para crear muchas páginas sin valor para el usuario, reescribir o traducir contenido ajeno de forma automática y combinar contenido de otras páginas sin aportar | primaria |
| **Google, contenido útil** | Preguntas de autoevaluación: ¿ofrece información, investigación o análisis originales?, ¿cubre el tema con más que lo obvio?, ¿alguien la guardaría o la recomendaría?, ¿no es producción masiva? Pide explicar **quién, cómo y por qué**; **divulgar** el uso sustancial de IA donde el lector se lo preguntaría; nunca inventar autores. Texto con IA producido a escala sin supervisión humana se considera «poco o ningún esfuerzo» | primaria |
| **YouTube** | Desde el 15 de julio de 2025 la categoría antes llamada «contenido repetitivo» se llama **contenido no auténtico** (genérico o repetitivo): plantillas, videos casi iguales con poco valor y **contenido de IA basado en plantillas genéricas sin la perspectiva propia del creador**. Usar IA o plantillas es aceptable si el resultado refleja una visión propia y aporta valor educativo o de entretenimiento; cada video debe tener un concepto distinto | primaria |
| **YouTube, divulgación** | Hay que declarar el contenido alterado o sintético **que parezca realista** (persona real diciendo algo que no dijo, evento o lugar alterado, escena realista inventada, música como foco). **No** hace falta para contenido claramente irreal, retoques estéticos menores ni **ayuda de producción** (guion, esquema, título, miniatura, subtítulos, mejora de audio). Se marca en YouTube Studio, sección «Atributos» | primaria |

## 3. Evidencia sobre lenguaje y calidad

- **Guía de síntomas de la comunidad de Wikipedia** (página de consejos, no política): catalogó patrones de textos de chatbots (tono promocional, importancia inflada, atribuciones vagas, vocabulario típico como «delve» o «showcasing», «serves as», «no solo X sino Y», listas de tres, títulos en mayúsculas, exceso de negritas, restos de chatbot, enlaces con `utm_source`). **Advierte** que ningún síntoma prueba autoría de IA, que los detectores tienen tasas de error no triviales, que un estudio de 2025 halló a las personas no mejores que el azar para distinguir texto humano de texto de IA y que **corregir solo los marcadores superficiales** puede ocultar los problemas de fondo (fuentes no verificables, falta de sustancia) (**primaria**, leída en la página; se leyeron los primeros 100.000 de ~250.000 caracteres).
- **Kobak et al.** analizaron más de 15 millones de resúmenes biomédicos de 2010 a 2024: tras la llegada de los LLM, ciertas **palabras de estilo** (que no aportan contenido) subieron de golpe; estiman que al menos **13,5 %** de los resúmenes de 2024 se procesaron con LLM, con valores de hasta ~40 % en algunos subconjuntos (**primaria**: resumen del artículo en arXiv; es una cota inferior y un patrón de **vocabulario**, no una medida de calidad).
- **Doshi y Hauser** (Science Advances, 2024): en un experimento, quienes recibieron ideas de un LLM escribieron cuentos mejor valorados individualmente, pero **los cuentos con IA se parecían más entre sí** que los escritos solo por personas: ganancia individual, empobrecimiento colectivo (**primaria/secundaria**: resumen del resumen y notas de prensa de la universidad). Es el mecanismo detrás de «todo suena igual».
- **Ahrefs** (julio de 2025, **vendor**): en ~600.000 páginas del top 20 no encontró correlación entre el porcentaje de IA detectado y la posición (0,011); solo 4,6 % era «IA pura», 81,9 % mezcla y 13,5 % «humano puro»; el #1 tendía a tener algo menos de IA. Es correlación, con el detector de la propia empresa: sirve para **no** concluir que «la IA se penaliza por ser IA», no para concluir que no importa la calidad.
- **Divulgar la IA y la confianza** (estudios de 2024-2026, **secundaria**, muestras pequeñas): etiquetar una noticia como generada con IA redujo la confianza unos 7 a 14 puntos en un experimento grande; en un estudio de 40 personas solo la divulgación **muy detallada** bajó la confianza mientras todas aumentaron la verificación de fuentes, y la mayoría prefería la divulgación detallada. Lectura prudente: la gente quiere saber, y cómo se divulga importa.

## 4. Lo que NO está demostrado (no usarlo como regla)

- Que Google «penalice» el texto por ser de IA: su política habla de propósito y valor, no de método (primaria).
- Que ciertas palabras «delaten» una pieza: son síntomas estadísticos de épocas de modelos que cambian (la propia guía lo dice).
- Que un detector de IA sirva de árbitro.
- Que existan umbrales de volumen: Google no ha publicado cuántas páginas o qué ritmo activan la política.
- Cifras y listas de palabras prohibidas en español: **no hay una fuente comparable a la guía de Wikipedia para español**; los síntomas en español de esta skill son **candidatos** (observación) hasta que se verifiquen.

## 5. Consecuencia para esta skill

El criterio es de **valor para el lector y de procedencia**, no de apariencia. De ahí la puerta de cinco pasos: propósito → sustancia → procedencia y revisión humana → síntomas (solo ayuda) → decisión.
