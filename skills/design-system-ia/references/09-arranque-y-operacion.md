# 09 · Arranque y operación

> **Estado:** borrador (C-2, 2026-10-27) · **Perfiles:** los tres (cambia el tamaño de cada paso) · **Modos que la usan:** `definir` (principal), `auditar` (regla de salto), `medir` (venta con números).
> **Fuentes (reexpresadas; ver `CREDITOS.md`):** una charla sobre nombrar tokens al llegar a una empresa nueva, un seminario sobre tokens, el relato de un equipo de Celonis sobre su primer sistema (2022–2023), un vídeo sobre documentar un sistema con un MVP, un testimonio sobre el trabajo con IA, una conversación en un festival de producto y una entrevista de podcast; el glosario de IA (orden MVP). **Inferencia propia** va marcada.
> **Contrastado con fuente primaria el 2026-10-27:** la definición de sistema de diseño, sus beneficios y su coste (Nielsen Norman Group), los modelos de equipo (Nathan Curtis, 2015 y su revisión de 2024), cómo las variables CSS permiten cambiar la apariencia sin cambiar nombres (MDN), y lo que dicen shadcn/ui y Mantine de sí mismas. **No contrastado:** todas las cifras de los relatos (son anécdotas), el efecto real de cada práctica y todo lo de WordPress y Astro.
> **Plantillas:** `templates/plan-de-arranque.md` · `templates/tabla-antes-despues.md` · `templates/tarea.md` (opcional) · `templates/encuesta-corta.md` (opcional). Índice: `templates/INDICE.md`.

## 1. Para qué sirve esta referencia

Responde a lo que ocurre **antes** de escribir un contrato: ¿hace falta un sistema?, ¿qué hay ya?, ¿por dónde se empieza?, ¿cómo se mantiene vivo? Es el contenido del modo `definir`. Lo que sale de aquí es **un plan por fases y unas decisiones anotadas**, no un sistema.

Orden de uso: **1)** ¿hace falta? → **2)** prerrequisitos → **3)** descubrimiento → **4)** librería de partida → **5)** MVP y fases → **6)** operación. En el perfil `individual` y `website` casi todo se reduce a **cinco preguntas al usuario** y una página (ver 3.1).

## 2. ¿Hace falta un sistema?

**Contrastado (Nielsen Norman Group):** un sistema de diseño es un conjunto de estándares con componentes y patrones reutilizables; sus beneficios **crecen con la escala** (muchas pantallas y productos), un prototipo de vida corta puede no justificar la inversión, y exige **mantenimiento continuo**, no una construcción única. Dicen que adoptar uno existente es lo más barato, adaptarlo cuesta más y crearlo cuesta lo máximo; **personalizarlo mucho borra el ahorro**.

**Lo que añaden los relatos (experiencias, sin medir):** una landing o un MVP no lo necesitan; varios productos o equipos grandes, sí; una sola persona no puede construirlo entero; un sistema suele nacer para **ordenar un caos** (patrones repetidos, trabajo duplicado, nadie sabe cómo contribuir); los plazos son **largos** (años para que desarrollo lo adopte y para ganar confianza).

**Lista «¿hace falta?» (propia, a partir de lo anterior):**

| Pregunta | Si la respuesta es… | Entonces |
|---|---|---|
| ¿Cuántas pantallas, páginas o productos comparten piezas? | Una página o un prototipo corto | **No** montes sistema: usa el «mínimo suficiente» (SKILL) |
| ¿Se repite trabajo o se duplican componentes? | Sí, varias veces | Hay un caso: empieza por el **perfil `website`** |
| ¿Cuántas personas cambian el diseño o el código? | Una | `individual`; **no** construyas todo a la vez |
| ¿Cuántas, o varios equipos? | Varias | `equipo` y regla de salto (sección 8) |
| ¿Quién lo mantendrá dentro de 6 meses? | Nadie | **Avisa:** sin mantenimiento un sistema envejece |
| ¿Hay ya una librería abierta o un tema que cumpla? | Sí | **Adopta** y documenta qué cambias (sección 5) |

**Tres pilares como criterio de `auditar`:** un conjunto de piezas de interfaz **sin** implementación en código, **sin** documentación y **sin** gobierno **no es un sistema**: es un UI kit (ver 04 y 08). Definición de las dos fuentes de entrevista: UI kit + guías y documentación + guía de estilo, **conectados con desarrollo**.

**Resultado del modo `definir` en este punto:** una de tres respuestas anotadas, con la razón: *no hace falta sistema*, *hace falta uno mínimo* (`website`) o *hace falta uno completo* (`app` o `sistema compartido`). **Decide el usuario.**

## 3. Prerrequisitos y descubrimiento

### 3.1 Prerrequisitos (lista de arranque)

Antes de planificar, averigua y **anota**; lo que no se sepa se declara:

- **Herramientas y permisos:** ¿qué repositorio, qué archivo de Figma, qué hosting, qué MCP o servidores están **disponibles y permitidos**? Un testimonio cuenta que su empresa **bloqueaba los MCP propios** y que el alta tardó un mes: no lo asumas.
- **Qué IA se usa:** elegir **una herramienta** y profundizar en ella es el consejo del testimonio; los patrones (chat + instrucciones + agentes) se parecen.
- **Fundamentos del usuario:** qué sabe de tokens y de la relación diseño-desarrollo. Sin eso, el usuario no sabe qué pedir (idea del mismo testimonio; **inferencia mía**: adapta cuánto explicas).
- **Entorno de código:** ¿sabe clonar, usar la terminal o Git? Si no, la skill lo hace y **lo explica en una línea**.
- **Librería de partida:** ¿ya usa una abierta (sección 4)?
- **Dónde se publicará** la documentación (SKILL, «Publicación»): hosting, Drive o Figma; **siempre se pregunta**.

### 3.2 Inventario de recursos (primer paso del descubrimiento)

Lista lo que existe, como hizo el equipo del relato (documentación manual, repositorio, catálogo de componentes en vivo, hojas de cálculo): **dónde vive cada cosa, quién la mantiene y si está al día**. En un proyecto `website` suele ser: la hoja de estilos, el tema, el archivo de Figma y las páginas existentes.

### 3.3 Lienzo de preguntas (versión corta)

Una charla propone una plantilla de **90 días de descubrimiento reducida a 30**, con conversaciones de unos 30 minutos con las partes interesadas. Esta referencia la reduce más (**propia**):

| Para… | Preguntas | Perfil |
|---|---|---|
| **El usuario** (siempre) | 1) ¿Qué es lo que más repites o te duele? 2) ¿Qué tienes ya (inventario)? 3) ¿Qué no se puede cambiar (marca, tema, plugin, nombres de colores)? 4) ¿Quién más tocará esto? 5) ¿Dónde se mostrará la documentación? | Todos; **bastan en `individual` + `website`** |
| **Desarrollo** | ¿Qué framework y qué nomenclatura impone? ¿Qué formato prefiere recibir los nombres? | `app`, `sistema compartido` |
| **Equipos/líderes** | ¿Qué esperan del sistema? ¿Quién bloquea las revisiones? ¿Qué están construyendo sin terminar? | `equipo` |

**Puntos de dolor:** el vídeo del MVP de documentación mapea primero **las preguntas que más se repiten** (p. ej. en el canal de un equipo) con ayuda de una IA, y empieza por el mayor dolor. Sin canal de equipo, usa tus propias incidencias o los correos del cliente. **Una IA que resume mensajes es apoyo, no un contador fiable:** revisa una muestra.

### 3.4 Cuatro bloques de contexto

Resume lo aprendido en cuatro bloques (de la charla; sirve como entrada de `definir`):
1. **Requisitos visuales** (qué se quiere ver).
2. **Estructura** del sistema o de la página.
3. **Límites de desarrollo** (p. ej. nombres de colores primarios que no se pueden renombrar → hace falta **otra capa encima**).
4. **Límites de diseño.**

### 3.5 Conflictos de nombres reales (se anotan al descubrir)

La charla muestra dos: `medium` como **tamaño y como peso**; **dos fondos neutros** (blanco y gris) que se distinguen con `default`/`subtle` o con bajo/alto. Se anotan **antes** de nombrar (02 y 03).

## 4. Librería de partida

Entrevista y testimonio coinciden en dos ideas:
- **Empezar con una librería abierta** da agilidad; se cambia cuando deja de bastar (por ejemplo: modo oscuro, personalización total, varias marcas, responsive, otros dispositivos). Puede ser solo de íconos o de ilustraciones y no cambiarse nunca.
- **La IA tiende a usar lo público** (la librería original) en vez del sistema propio; hace falta una regla explícita «usa el nuestro» y declarar el **origen** de cada componente (01 y 06).

**Contraste con las propias librerías (2026-10-27):** *shadcn/ui* se describe como **no una librería de componentes, sino la forma de construir la tuya** (recibes el código y lo editas), así que «cambiar de librería» **no es el único camino**; *Mantine* trae **esquemas de color claro y oscuro de forma nativa**. Es decir, **el modo oscuro no obliga por sí solo a abandonar una librería abierta**: la afirmación del relato era de su caso. Pregunta y decide con el usuario.

**Pregunta de arranque:** «¿Usas ya una librería o un tema? ¿Cuál? ¿Qué quieres poder cambiar?» → se anota en el **origen** de cada contrato (01).

**Ejercicio opcional (fila 91):** reconstruir uno o dos componentes de una librería abierta para aprender su arquitectura. **No** es parte del flujo; se ofrece si el usuario quiere aprender.

## 5. MVP y orden de fases

### 5.1 Lo amplio al núcleo

El relato del equipo de Celonis usó **círculos concéntricos**: de lo amplio al núcleo, y de ahí un MVP con cuatro hitos. Su MVP de componentes fue **etiqueta, texto de ayuda, mensaje de aviso, tokens, componentes base, íconos e ilustraciones**; el testimonio y el vídeo del MVP de documentación coinciden en **priorizar por impacto**, no por cobertura.

### 5.2 Orden de fases (fusión de dos fuentes; **adaptado**, sin probar con proyecto propio)

| Fase | Qué se hace | Referencia |
|---|---|---|
| 0 | **Descubrimiento** (sección 3) | 09 |
| 1 | **MVP y priorización:** qué entra, qué no | 09 |
| 2 | **Propiedades y valores:** listar las de cada componente en una **tabla** antes de construir (el equipo lo hizo en una hoja de cálculo; aquí es el contrato o su borrador) | 01, 03 |
| 3 | **Nomenclatura:** vocabulario y fórmula de nombres; **taller** (sección 6) | 02, 03 |
| 4 | **Primera versión:** construir | 01, 05 |
| 5 | **Accesibilidad** | 08 |
| 6 | **Verificación** en grupo o con scripts | 07 |
| 7 | **Segunda versión:** componentes más complejos, ilustraciones | — |

El relato dice **68 componentes en 3 meses** y **4 más en diciembre** con un equipo; **son cifras de un caso, sin contrastar**, y **no** sirven de referencia de plazo para un proyecto individual.

### 5.3 MVP por perfil (propuesta propia, a probar con `caso-ds-01`)

| | `website` | `app` | `sistema compartido` |
|---|---|---|---|
| **Entra** | Variables de color, tipografía y espaciado (2 capas) + los **componentes realmente usados** completos con sus estados + una página de documentación breve | Lo anterior + contratos con esquema + `AGENTS.md` + estado calculado | Lo anterior + versionado, guía de contribución y avisos de cambios |
| **No entra todavía** | Tokens de componente, DTCG, evaluaciones | Librería publicada, multimarca | Todo lo que no tenga un segundo producto que lo pida |
| **Medida de éxito** | Los puntos de dolor del inventario desaparecen | + la verificación pasa | + adopción por versión (07) |

### 5.4 Dos puertas de entrada

- **Sistema nuevo con código:** primero el **contrato** (01).
- **Sistema existente sin contrato:** primero el **MVP de documentación** (04) —solo las decisiones que más duelen— y de ahí un **contrato mínimo**. (El vídeo del MVP de documentación parte de la documentación; Helix parte del contrato: son dos puertas, no una contradicción.)
- **Criterio de éxito de la primera página:** estandariza **una** página de componente, pide opinión a diseño y a desarrollo y **solo entonces** replícala.

## 6. Taller de vocabulario

Valida el vocabulario con quien lo usará **antes de escribirlo en todas partes**: el seminario de tokens lo ejemplifica con «`background` frente a `surface`» en una empresa. Si el framework impone una **nomenclatura fija**, el sistema **se adapta a ella** (misma fuente).

Guion (propio, a partir del método de 4 pasos de 03):
1. **Identifica** las piezas y sus nombres actuales en diseño y en código.
2. **Compara** (tabla *antes → después*; sección 7).
3. **Decide** los nombres con quien implementa; el usuario aprueba.
4. **Anota** los conflictos y sinónimos descartados (03).

**En `individual`:** el «taller» es una conversación corta entre la skill y el usuario, con **2–3 opciones** por nombre en disputa. **En `equipo`:** sesión con desarrollo y diseño, **aprobada por la persona responsable**.

**No contrastado:** qué nomenclatura impone concretamente WordPress (temas de bloques, clases de plugins) o Astro; **no la supongas**, pregúntala o léela del proyecto.

## 7. Sincronizar nombres sin gestor de tokens

Procedimiento de la entrevista (sirve cuando no hay un puente entre Figma y código):
1. **Captura** lo de Figma junto a lo del código.
2. **Tabla «antes → después»** en una incidencia o tarea.
3. **Pregunta a desarrollo en qué formato prefiere** recibirla.

```markdown
| Elemento | Nombre en Figma (antes) | Nombre en código (antes) | Nombre acordado (después) | Estado |
|---|---|---|---|---|
| Botón, tamaño | Size / S | .btn--small | size=sm | pendiente |
```

Aclaración del seminario de tokens: **no renombres dentro de las variables de Figma si hay un gestor de tokens; renombra en el gestor.** Sin gestor, las dos sedes se mantienen con la tabla (05).

## 8. Regla de salto (señales afinadas)

> Borrador del SKILL, afinado aquí. Los **umbrales** son orientativos (**propios, sin probar**); se ajustan con `caso-ds-01`.

**Cuándo se revisa:** al arrancar y en cada `auditar`. **Quién decide:** el usuario. **La skill nunca cambia de perfil por su cuenta.**

| Salto | Señales (anota cuáles se cumplen) |
|---|---|
| `website` → `app` | Hay **área de clientes o inicio de sesión** · **paneles o tablas con filtros** · **formularios con validación y estados de error** · **más de unos 5 componentes interactivos con estados** (modales, menús, pestañas) · **modo oscuro o responsive complejo con datos dinámicos** |
| `app` → `sistema compartido` | Un **segundo producto o marca** reutiliza componentes · **más de una persona o equipo** cambia el sistema · piden **versiones y avisos de cambio** · se **duplican componentes** entre proyectos · **temas por cliente** |

**Cómo se avisa (propuesta propia):**
- **1 señal:** se **anota** en la nota de decisiones del proyecto, sin avisar.
- **2 o más señales:** se **avisa**, con las señales vistas, qué cambiaría (tabla de perfiles del SKILL) y qué costaría; el usuario decide.
- **Si el usuario dice que no:** se anota la decisión y **no se vuelve a insistir** hasta que cambie una señal.

Modelo de aviso:
> «He visto estas señales: (1) …, (2) …. Con ellas, este proyecto se parece más al perfil `app`. Cambiaría: contratos con esquema, una tercera capa de tokens si hace falta y evaluaciones. Costaría: … ¿Quieres cambiar de perfil, quedarte como estás o decidirlo más adelante?»

**Relación con el gobierno (contraste, Curtis):** al pasar a `sistema compartido` y a `equipo`, el modelo de equipo que **funciona según su autor** es **un equipo central al que se le añade participación federada poco a poco**, no un modelo federado desde el inicio; su artículo de 2024 corrige su propia propuesta de 2015 de elegir entre uno u otro. Es la experiencia de un consultor, no una ley; en esta skill orienta la regla: **empieza por el responsable, añade colaboradores después** (08).

## 9. Cambio visual rápido

Una charla y la entrevista cuentan la misma táctica: **repintar los componentes más reutilizables** (insignias, alertas, controles, campos; unos 15) **cambiando solo los valores de los tokens primarios**, sin tocar los nombres, para dar una apariencia nueva en pocas semanas (3 en el relato) y **ganar tiempo para nombrar bien**. Sirve además para **traducir «más moderno, más brillante» a algo reutilizable** (un token) y no a un encargo puntual.

**Contraste (MDN):** las variables CSS **se heredan y se encadenan**; definidas en `:root` (o en un ámbito, p. ej. una clase de tema) y usadas con `var(--nombre, respaldo)`, **cambiar su valor en un solo sitio cambia todo lo que las usa**, y los nombres no cambian. **Limitación:** no se pueden usar dentro de la condición de una *media query*.

Condiciones (propias):
- **Solo si ya existen variables o tokens.** Si no, el primer paso es la **capa mínima de variables** (02); si no hay, **no hay atajo** y se dice.
- **Solo cambias valores,** nunca nombres ni estructura; **verifica el contraste AA en claro y oscuro** (02) antes de enseñarlo.
- **Muestra y espera aprobación** antes de aplicar (SKILL, paso 3).
- Es una **táctica de tiempo,** no el sistema: queda anotada como deuda hasta hacer la nomenclatura.

## 10. Vender con números

La conversación y la entrevista coinciden: **gran parte del trabajo es convencer**, y en diseño casi nunca se enseña a hablar en números. Los argumentos que citan: horas perdidas por repetir trabajo, costes, **tiempo por pantalla**, y reducción de **licencias** de herramientas; ambas dan además **ventajas medibles** (construir más rápido, menor coste de producción, decisiones ya tomadas). **Las cifras de sus anécdotas no se citan** (sin fuente).

**Guion (propio, a partir de lo anterior):**

| Paso | Qué hacer |
|---|---|
| 1 | **Mide el punto de partida** con datos del propio proyecto (inventario de la sección 3.2): cuántas veces se repite una pieza, cuánto se tarda en una pantalla o página |
| 2 | **Traduce a tiempo o dinero,** con la tarifa o el coste real del usuario (no uno inventado) |
| 3 | **Declara los costes del sistema** (construcción y **mantenimiento continuo**, según NN/g) |
| 4 | **Propón una medida de éxito** (07) y una fecha de revisión |
| 5 | **Encuesta muy corta** (de la entrevista), 2–3 preguntas: ¿te resulta más fácil encontrar y usar piezas?, ¿cuánto tiempo ahorras?, ¿qué falta? |

Si un dato no existe, **dilo**: «sin medición, solo hay una hipótesis».

## 11. Operación: tareas de «Design Ops»

La conversación y la entrevista afirman que, **si no hay un perfil de operaciones, lo hace quien lleva el sistema**; no hace falta una persona dedicada, bastan unas horas por semana. Esta skill trata el tema como **lista de tareas, no como definición de un rol**:

| Tarea | Frecuencia sugerida (propia, sin probar) | Perfil |
|---|---|---|
| Revisar qué se implementa **fuera del sistema** (archivos y código ajenos) y dejar comentarios o notas | Cada versión o mes | Todos |
| **Avisar de cambios** (registro de cambios; canal si hay equipo) | En cada versión | `app`, `sistema compartido` |
| **Revisión periódica** del sistema (componentes sin uso, deuda `[CUSTOM]`; 07) | Trimestral | Todos |
| Mantener **plantillas de tareas** por tipo de trabajo (crear un componente: hablar con desarrollo → propuesta → revisión → publicación) | Cuando el proceso cambie | `equipo` |
| **Escuchar** qué herramientas usa cada equipo y documentar sus puntos fuertes; **no imponer** | Continuo | `equipo` |
| **Canal de consulta,** una persona campeona por equipo y horas abiertas (08) | Continuo | `equipo` |
| **Pedir lo no terminado** para saber hacia dónde van | Cada ciclo | `equipo` |
| **Alinear a los líderes** (el bloqueo real puede estar arriba; 08) | Al arrancar y en cada salto | `equipo` |
| **No prometer fechas** que no puedes cumplir | Siempre | Todos |
| Responder a las preguntas repetidas con **formato fijo** (p. ej. una tabla de variantes) | Cuando se repitan | Todos |

**Aviso al crear algo nuevo y revisiones periódicas** (entrevista): un componente que solo sirve a un producto se construye allí; si se reutiliza en más de uno, se evalúa subirlo al sistema (08).

**Plantilla de tarea** (versión ligera, propia):

```markdown
## Tarea: <tipo> — <nombre>
- Tipo: crear componente | cambiar token | retirar | auditoría
- Quién decide: …
- Pasos: 1) … 2) … 3) …
- Verificación: …
- Aviso a: …
```

## 12. Lo que se deja fuera

- **Rol de servicio, motivación, carrera, repositorio de enlaces:** contexto de los relatos, no método.
- **Herramientas de terceros** del relato (gestores de tokens, documentación, catálogos): se rescata la idea, no la herramienta.
- **Entrevistas del rol, marca personal, mercado laboral, interfaces del futuro:** fuera del alcance.

## 13. Lista de revisión (la usa `definir`)

- [ ] ¿Hace falta un sistema? Respuesta anotada con la razón y **decidida por el usuario**.
- [ ] **Perfil de proyecto y de gobierno** elegidos.
- [ ] **Prerrequisitos** anotados (herramientas, permisos, destino de publicación).
- [ ] **Inventario de recursos** hecho.
- [ ] **Cinco preguntas** al usuario respondidas (o el lienzo, si hay equipo).
- [ ] **Cuatro bloques de contexto** resumidos.
- [ ] **Librería de partida** preguntada y anotada como origen.
- [ ] **MVP** definido con lo que **no** entra.
- [ ] **Orden de fases** con la puerta de entrada elegida (contrato o documentación).
- [ ] **Taller de vocabulario** hecho y los conflictos anotados.
- [ ] **Regla de salto** revisada y señales anotadas.
- [ ] **Medida de éxito** y fecha de revisión.
- [ ] **Qué no se verificó** declarado.

## 14. Fuentes y estado de la verificación

| Idea | Fuente | Estado |
|---|---|---|
| Definición, beneficios, coste y adoptar/adaptar/crear | Nielsen Norman Group | **Contrastado** |
| Criterio de necesidad y orígenes del sistema | Conversación y entrevista | **Experiencia**, sin medir |
| Tres pilares (UI kit + guías + guía de estilo, conectados con desarrollo) | Entrevista | **Experiencia**; coherente con NN/g (que no los llama «pilares») |
| Lienzo de descubrimiento y cuatro bloques de contexto | Charla de tokens | **Reexpresado**; transcripción automática traducida, **solo ideas** |
| Inventario de recursos, círculos concéntricos y MVP del equipo | Relato de Celonis | **Leído (texto de las láminas)**; cifras sin contrastar |
| Orden de fases | Relato + seminario de tokens | **Adaptado**; sin probar con proyecto propio |
| Taller con desarrollo y nomenclatura fija | Seminario de tokens | **Experiencia** |
| Librería abierta primero | Entrevista y testimonio | **Experiencia**; matizado con shadcn/ui y Mantine |
| Variables CSS: cambiar valores sin cambiar nombres | MDN | **Contrastado** |
| Cambio visual rápido (15 componentes, 3 semanas) | Charla y entrevista | **Experiencia** |
| Sincronización con tabla «antes → después» | Entrevista | **Experiencia** |
| Modelos de equipo: central + federado gradual | Nathan Curtis (2015; revisión de 2024) | **Contrastado** (opinión de un consultor) |
| Venta con números y encuestas cortas | Conversación y entrevista | **Experiencia**; cifras no citadas |
| Tareas de operaciones | Conversación, entrevista, testimonio | **Experiencia**; frecuencias **propias** |
| Prerrequisitos de permisos | Testimonio | **Experiencia** |
| Umbrales y modelo de aviso de la regla de salto | — | **Propuesta propia, sin probar** |
| MVP por perfil y fases para WordPress, HTML+CSS, Astro, React y Next.js | — | **Inferencia propia, sin probar** (`caso-ds-01`) |

**Límites:** casi todo es experiencia de personas con equipo en empresas grandes; el perfil `individual` + `website` **no tiene un caso propio todavía**. La entrevista de podcast se leyó **completa solo hasta el minuto 41**, y la charla de tokens, sobre **subtítulos traducidos automáticamente**. Ninguna práctica de esta referencia se ejecutó.
