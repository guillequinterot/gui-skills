# 08 · Gobierno, accesibilidad y estabilidad

> **Estado:** borrador (C-2, 2026-10-27) · **Perfiles:** los tres (cambia el gobierno por defecto) · **Modos que la usan:** `auditar`, `verificar`, `construir`, `contrato`, `medir`, `definir`.
> **Fuentes (reexpresadas; ver `CREDITOS.md`):** el sistema **Helix** (MIT, © 2026 Marta Conde; commit `394823a`: sus reglas críticas, la guía de contribución, la puerta del dueño, el ejecutor de accesibilidad y las decisiones sobre estado y renombres), la charla de un equipo de Celonis, una conversación en un festival de producto y una entrevista, los artículos de métricas y el glosario de IA. **Inferencia propia** va marcada.
> **Contrastado con fuente primaria el 2026-10-27:** criterios WCAG 2.2 (nombre, nivel y requisito), el patrón de diálogo modal de WAI-ARIA, `prefers-reduced-motion` (MDN), Versionado Semántico 2.0.0 y los hooks de Claude Code (ver 06). **No contrastado:** que cada una de las 12 comprobaciones de accesibilidad de Helix mida bien su criterio (se leyó su definición, **no se ejecutaron**), el efecto de las prácticas de gobierno de equipo (son experiencias) y todo lo de WordPress/Astro.
> **Plantillas y scripts:** `templates/decision.md` · `templates/lista-de-control-componente.md` · `templates/ficha-de-auditoria.md` · `scripts/contraste.py`.

## 1. Qué es gobierno

Gobierno es **quién puede cambiar qué, con qué evidencia y con qué aviso**. Un sistema sin gobierno acaba en parches locales; con demasiado, nadie contribuye. Esta referencia fija **tres cosas**: la **escalera de decisión** de cada cambio, el **perfil** (individual o equipo) y la **accesibilidad y estabilidad** como condiciones medibles.

Reglas que se repiten en todas las fuentes:
- **Escribe decisiones, no solo reglas:** una decisión corta (contexto, decisión, consecuencias) explica los casos no previstos. Helix guarda **24** así.
- **El que decide es una persona;** la IA propone.
- **Todo cambio estructural pasa antes por una propuesta con opciones.**

## 2. La escalera «¿puede? ¿debería? ¿se le permite?»

| Nivel | Pregunta | Qué lo comprueba | Dónde vive |
|---|---|---|---|
| **¿Puede?** | ¿Es mecánicamente correcto? (compila, props y tokens válidos) | **Un verificador** (linter, tipos, script) | 03, 02, 07 |
| **¿Debería?** | ¿Respeta el **juicio de diseño**? («nunca usar para», accesibilidad, límites responsive) | **El contrato** (01) y una revisión | 01 |
| **¿Se le permite?** | ¿Tiene **autoridad**? Qué adapta localmente y qué debe escalar | **La gobernanza del contrato** y una puerta del dueño | 01, esta referencia |

Ejemplo de Helix (agentes que usan el sistema): **pueden** usar los componentes y crear componentes propios con la marca `// [CUSTOM] motivo`; **no pueden** alterar los tokens compartidos con estilos locales, cambiar el relleno o la altura internos ni redefinir el contrato de una prop; si un patrón no se logra con lo que hay, **deben marcarlo para revisión humana o pedirlo**.

**Cómo se escala:** en el contrato, `mustEscalateToDS` lista lo que cambia lo compartido (variantes globales nuevas, tocar medidas internas, nuevos escalones de tamaño); `mayExtendLocally` lo que se puede hacer sin pedirlo (envolver con un tooltip, pasar una etiqueta accesible).

**Componente propio (`[CUSTOM]`):** se parte de un andamio con la cabecera, los tokens semánticos y una base accesible (Helix lo genera con un comando), **no de cero**. Cuenta como **deuda** y se mide (07).

## 3. Los dos perfiles de gobierno

Se elige **al arrancar** (decisión de Guille); **el camino individual es el que se presenta primero y el valor por defecto**. Son independientes del perfil de proyecto.

| | `individual` | `equipo` |
|---|---|---|
| **Quién decide** | Una persona (el usuario) | Un grupo, con **líderes alineados** |
| **Verificación** | Por **script**; el humano aprueba lo que define el sistema | Por **revisión y canales**, con scripts donde se pueda |
| **Cambios a tokens, contratos y vocabulario** | **Puerta del dueño:** el agente presenta **2–3 opciones** con su efecto y espera | Propuesta con opciones en un canal y revisión; **no se cambia «al momento»** |
| **Contribución** | Una sola persona; las propuestas de otros pasan por **una incidencia** | **Abierta** (poco burocrática) o **cerrada**: se elige y se anota |
| **Canales** | Un archivo de solicitudes (06) | Varios (p. ej. de **1 a 4 canales**: Figma, ingeniería, sistema, diseño) + **comentarios en Figma**, **horas abiertas de consulta** y **una persona campeona por equipo** |
| **Avisos** | Registro de cambios | Registro + canal de novedades |
| **Riesgo típico** | Decisiones sin segunda mirada | Un bloqueo en **niveles superiores** que no ves desde el equipo |

**Prácticas de equipo (de la charla de Celonis y de dos conversaciones; son experiencias, sin medir):**
- **Enfocarse en una tarea y no crear nuevas;** **acompañar al equipo durante los procesos;** **no hacer cambios al momento.**
- **Una contribución «boomerang»:** quien pide algo vuelve a recibirlo hecho y documentado; un **sandbox** y unos **procesos** escritos.
- **Alinear a los líderes,** no solo a los equipos: el bloqueo real estaba en revisiones de niveles superiores.
- **Pedir lo que aún no está terminado** a los equipos para saber hacia dónde van y **dejar comentarios en sus archivos** («este componente está desvinculado»).
- **Aceptar un cambio que sirve a toda la aplicación** sin burocracia; otros sistemas son **cerrados**: cualquier cambio exige un proceso.
- **Un componente que solo sirve a un producto se construye allí;** si se reutiliza en más de uno, se **evalúa subirlo al sistema.**
- **«Si no hay un perfil de operaciones, lo eres tú.»**

**Mecanismo de la puerta del dueño (Helix, leído; no ejecutado):** un hook que **pregunta antes de escribir** en los archivos que definen el sistema (tokens y temas, contratos, mapa de props, estándar de conversión de Figma y, en una aplicación, el propio paquete del sistema). Es **un punto de control para un agente de buena fe, no un cajón de arena**: un script que escriba el archivo desde otro sitio **no se ve**, y **si no puede leer la orden, la deja pasar** («falla abierto»). **Los guardarraíles duros que fallan en silencio son blandos** (06).

## 4. Cómo se propone un cambio

Quien contribuye empieza por una **incidencia** y no por el código; **la propuesta lista las opciones que consideró** (con su contraste en claro y oscuro, si son colores) **y recomienda una**: se decide más rápido. En Helix: un fallo → informe; un token → propuesta de token; un componente → propuesta de componente; un cambio transversal → una incidencia y, quizá, una **decisión escrita**; una errata → directamente una solicitud de cambio.
- **Un asunto por solicitud** (un cambio de componente y uno de token son dos).
- **Revisores automáticos** para lo que define el sistema (un archivo de propietarios del código).
- **Contribuir no exige Figma:** un componente llega a `beta` sin él; quien mantiene lo lleva a `stable` (07).

**Plantilla de decisión (propia, a partir del formato de las de Helix):**

```markdown
# Decisión NNN — <título>
**Fecha:** · **Estado:** propuesta | aceptada | sustituida por NNN
## Contexto        (qué problema y qué evidencia)
## Decisión        (qué se hace y qué opciones se descartaron)
## Consecuencias   (positivas, negativas y cómo se mitigan)
```

## 5. Reglas de composición: método y estilo

El **método** es que las reglas de composición **existan, estén escritas y sean comprobables**. Los **valores concretos** son de cada sistema. Ejemplos de Helix (**estilo de un sistema, no regla universal**):

| Regla de Helix | Tipo | ¿Verificable? |
|---|---|---|
| No usar `<div>` para maquetar: usa los componentes de maquetación | Composición | Por lint |
| Los íconos pasan siempre por el componente `Icon`; el trazo lo deriva el tamaño | Composición | Por lint (`verify:icons`, ejecutado) |
| Color y radio, **siempre un token**; el espaciado también salvo por encima de la escala | Tokens | Por verificador |
| Una distancia fuera de escala **se parte en dos** cajas con tokens, nunca un valor suelto | Tokens | Parcial |
| **Elementos del mismo tipo seguidos separados por 4 px** (botones, chips, insignias); más solo entre grupos distintos | Composición | Revisión |
| **El borde existe siempre;** los estados solo cambian su color | Estilo | Revisión + auditoría de Figma |
| **Deshabilitado con colores reales, nunca con opacidad** | Estilo | Revisión |
| **Una sola altura y un ancho** para los campos de formulario | Estilo | Por verificador (`verify:field-sizes`, ejecutado) |
| Sombra solo en superficies que **flotan** (diálogo, menú, tooltip) | Estilo | Revisión |

Un componente que se salta una regla entra en una **tabla de excepciones** con motivo (02).

## 6. Accesibilidad

**Objetivo:** **WCAG 2.2 AA en claro y oscuro**, **medido, no supuesto**. El contrato registra rol, teclas y criterios (01).

**Criterios que toca un sistema de componentes (contrastados con WCAG 2.2, 2026-10-27):**

| Criterio | Nivel | Requisito en una línea | ¿Comprobación en Helix? |
|---|---|---|---|
| **1.4.1** Use of Color | A | El color no es el único indicador | Aviso de IA (no puntúa) |
| **1.4.3** Contrast (Minimum) | AA | 4,5:1 texto normal; 3:1 grande | Sí (claro **y** oscuro) |
| **1.4.10** Reflow | AA | Sin desplazamiento en dos dimensiones a **320 px CSS** | Sí, **solo** componentes de maquetación |
| **1.4.11** Non-text Contrast | AA | 3:1 en objetos que no son texto | Aviso de IA |
| **2.1.1** Keyboard | A | Todo operable con teclado | Sí (pruebas de teclas en un navegador) |
| **2.1.2** No Keyboard Trap | A | Si el foco entra con teclado, sale con teclado | Sin comprobación propia visible |
| **2.4.3** Focus Order | A | Orden con sentido | Sí (a dónde va el foco al cerrar con Escape) |
| **2.4.7** Focus Visible | AA | Foco visible | Sí (cada parada se ve distinta, claro y oscuro) |
| **2.4.11** Focus Not Obscured (Minimum) | AA | Un componente con foco no queda **oculto del todo** por contenido del autor | **No figura entre las 12 comprobaciones** |
| **2.5.8** Target Size (Minimum) | AA | **24 × 24 px** (o espaciado equivalente) | Sí |
| **3.3.1** Error Identification | A | El error se identifica y describe **en texto** | Sin comprobación propia visible |
| **3.3.2** Labels or Instructions | A | Etiquetas o instrucciones donde se pide entrada | Sin comprobación propia visible |
| **4.1.2** Name, Role, Value | A | Nombre, rol y valor accesibles | Sí (contrato + lo que anuncia el lector de pantalla) |
| **2.3.3** Animation from Interactions | **AAA** | El movimiento por interacción se puede desactivar | Criterio 7 del estado (ver 07) |

**Las 12 comprobaciones de Helix (leídas, no ejecutadas):** contrato · teclas probadas · **retorno del foco** · teclado (en navegador) · analizador de accesibilidad (reglas AA, claro y oscuro) · contraste · foco visible · tamaño del objetivo · reflow · lector de pantalla (el árbol de accesibilidad tiene el rol que promete el contrato) · **revisión de IA** (solo orienta) · **revisión humana** con un lector de pantalla real. **La puntuación es el % de comprobaciones automáticas que aplican y pasan** (lo pendiente cuenta como no pasado) y **las revisiones no puntúan.** *Resultado de Button en su archivo: 100 con la revisión humana pendiente.*

**Prácticas contrastadas:**
- **Diálogo modal (patrón de WAI-ARIA):** al abrir, el foco va a un elemento **dentro**; **Tab y Mayús+Tab dan la vuelta dentro del diálogo**; **Escape lo cierra**; **al cerrar, el foco vuelve al elemento que lo abrió** (salvo que ya no exista o el flujo pida otro destino). Es lo que debe decir el contrato de un modal.
- **Movimiento reducido:** `prefers-reduced-motion` (`no-preference` o `reduce`) permite quitar, reducir o **sustituir** el movimiento; el ejemplo de MDN **sustituye** un efecto de escala por una disolución más suave **en lugar de quitar todo** *(la página no lo enuncia como regla)*. **WCAG lo exige solo en AAA (2.3.3);** Helix lo trata como **criterio de calidad** igualmente: lo mismo debes decidir tú.
- **Lo deshabilitado está exento de contraste** (WCAG 1.4.3, componentes no disponibles para la interacción): documéntalo.
- **Cada comprobación automática no sustituye una revisión humana:** «¿tiene sentido lo que lee el lector de pantalla?» se registra con fecha, persona y tecnología (01).

**Por perfil:** `website` → lista de control (04) y un analizador en un navegador sobre **páginas de ejemplo**; `app` y `sistema compartido` → las comprobaciones como **estado** (07).

**Hueco propio:** los criterios **2.1.2, 2.4.11, 3.3.1 y 3.3.2** no tienen comprobación propia **visible** en las 12 de Helix; añádelos a **tu** lista de control. *(Que no la tengan visible no prueba que el sistema no los cumpla.)*

## 7. Estabilidad y cambios que rompen

- **Versión semántica (contrastada, SemVer 2.0.0):** **MAJOR** = cambio incompatible; **MINOR** = añadir funcionalidad compatible **o deprecar**; **PATCH** = corrección compatible. **Antes de quitar algo, se publica al menos una versión menor con la deprecación** y se actualiza la documentación.
- **Contrato con `version`** (`x.y.z`) y estado `deprecated` (el único **manual**, ver 07).
- **Un renombre es un cambio mayor:** Helix cambió `onPress`→`onClick` y `loading`→`isLoading` **a la vez** en contratos, tipos, mapa y linter y subió **sus contratos a 2.0.0**, **sin periodo de alias porque no estaba publicado**. Para un sistema **publicado** (propuesta propia): versión menor con **alias y aviso**, **guía de migración** y retirada en la mayor siguiente.
- **Métricas de estabilidad (07):** cambios que rompen ÷ cambios; los rompientes **con guía de migración** ÷ rompientes. **Clasifica con prefijos explícitos,** no por palabra clave: el **propio registro de cambios de Helix** etiqueta cada cambio por una **heurística de palabras** y **dice que no es autoritativa**.
- **Un cambio visual en un componente `stable` lo baja a `beta`** hasta que Figma lo alcance (07).
- **Cambios de versión juntos:** en Helix, todos los paquetes comparten una versión y siguen en `0.x` **hasta que la API sea estable**.

## 8. Lista de revisión (la usa `auditar`)

- [ ] **Perfil de gobierno** elegido y anotado (individual por defecto).
- [ ] **Dueño** y **archivos protegidos** definidos (tokens, contratos, vocabulario, estándar de Figma).
- [ ] **Escalera** de tres niveles aplicada a las reglas del sistema.
- [ ] **Qué se adapta y qué se escala** en cada contrato.
- [ ] Un **procedimiento de propuesta** con opciones y recomendación.
- [ ] **Decisiones escritas** (contexto, decisión, consecuencias).
- [ ] **Modelo de contribución** (abierto o cerrado) escrito; líderes alineados (`equipo`).
- [ ] **Reglas de composición** escritas y, donde se pueda, verificadas; excepciones con motivo.
- [ ] **Accesibilidad por tema, teclado aparte,** y criterios 2.1.2, 2.4.11, 3.3.1 y 3.3.2 en tu lista.
- [ ] **Revisión humana** registrada con fecha, persona y tecnología.
- [ ] **Versiones semánticas,** deprecación antes de retirar y guía de migración.
- [ ] Los guardarraíles **duros** declaran qué ocurre **si fallan** (fallo abierto o cerrado).

## 9. Fuentes y estado de la verificación

| Idea | Fuente | Estado |
|---|---|---|
| Escalera «¿puede? ¿debería? ¿se le permite?» y gobierno por componente | Guía para agentes y contrato de Helix | **Leído**; estilo de un sistema |
| Puerta del dueño: qué protege y cómo falla | Hook de Helix + hooks de Claude Code | **Leído y contrastado** (**no ejecutado**) |
| Proceso de propuesta y contribución | Guía de contribución de Helix | **Leída**; **de un solo mantenedor** |
| Prácticas de gobierno de equipo | Charla de Celonis, conversaciones y entrevista | **Experiencias, sin medir**; autoría y contexto distintos entre sí |
| Criterios WCAG 2.2 (tabla de la sección 6) | W3C | **Contrastados** (nombre, nivel y requisito) |
| Las 12 comprobaciones de Helix | Ejecutor de accesibilidad de Helix | **Leídas**; **no ejecutadas** |
| Diálogo modal: foco dentro, Escape, retorno del foco | WAI-ARIA Authoring Practices | **Contrastado** |
| Movimiento reducido: valores y sustitución | MDN | **Contrastado** (la regla «no quitar todo» es **inferencia**) |
| Versionado semántico y deprecación | semver.org | **Contrastado** |
| Renombrar sin alias en un sistema no publicado | ADR-022 de Helix | **Leído** |
| Alias y aviso para un sistema publicado | — | **Propuesta propia, sin probar** |
| Criterios sin comprobación propia visible (2.1.2, 2.4.11, 3.3.1, 3.3.2) | Ejecutor de Helix frente a WCAG | **Hallazgo propio** (lectura de la lista de comprobaciones) |
| Modelo individual y de equipo para `website` en HTML/WordPress/Astro | — | **Inferencia propia, sin probar** (`caso-ds-01`) |

**Límites:** casi todo viene de **un sistema con un solo mantenedor** y de **tres experiencias de equipo**. **Ningún guardarraíl ni comprobación de accesibilidad se ejecutó** en esta investigación; el modelo de **equipo** no tiene un caso propio y puede no encajar con tu forma de trabajar.
