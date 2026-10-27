# 01 · Contrato del componente

> **Estado:** borrador (C-2, 2026-10-27) · **Perfiles:** los tres (cambia el nivel) · **Modos que la usan:** `contrato`, `construir`, `auditar`, `documentar`.
> **Fuentes (reexpresadas con palabras propias; ver `CREDITOS.md`):** el esquema y los contratos del sistema **Helix** (licencia MIT, © 2026 Marta Conde; commit `394823a`), el artículo de la misma autora sobre sistemas «listos para IA», sus videos y plantillas, y las normas citadas abajo. Lo que es **inferencia propia** va marcado.
> **Contrastado con fuente primaria el 2026-10-27:** los criterios WCAG 2.2 de la sección 10 (nombre, nivel y umbrales) y la versión vigente de JSON Schema. **No contrastado:** ARIA/teclas por componente, ni el funcionamiento de los verificadores de Helix más allá de ejecutarlos (ver la matriz, filas 109–116).
> **Plantillas y scripts:** `templates/contrato-minimo.md` · `templates/contrato-completo.json` · `scripts/validar_contrato.py` y `scripts/contrato.schema.json` · `scripts/comparar_figma_contrato.py`.

## 1. Qué es y para qué sirve

Un **contrato** es un documento corto que dice **qué ES un componente y cómo se usa**, no cómo está programado. Lo lee una persona para decidir, una IA para no inventar y un verificador para comprobar. Si el componente cambia, el contrato cambia primero.

Regla central: **la fuente de verdad se elige y se registra por proyecto** (por defecto, contrato/código primero; si el proyecto parte de Figma, se anota). Si Figma y el contrato no coinciden, **manda la fuente registrada** y se corrige la otra.

## 2. Cuánto contrato según el perfil

| Perfil | Qué se escribe | Formato |
|---|---|---|
| `website` | **Contrato mínimo** (5 campos, sección 3) **+ lista de estados que se entregan** *(la lista es inferencia propia: el componente final se entrega con sus estados)* | Markdown |
| `app` | **Contrato completo** (sección 4) | JSON con esquema |
| `sistema compartido` | Completo **+ versión, estado y guía de migración** | JSON con esquema |

No se escribe el contrato de **todo** el sistema de golpe: se empieza por los **componentes más usados** (la fuente propone tres y crecer desde ahí) y se amplía cuando haga falta.

## 3. Contrato mínimo (5 campos)

Vale para un `website` o para empezar. Se escribe **antes que el código**: diseño lo define y desarrollo completa la anatomía.

| # | Campo | Responde a | Fuente |
|---|---|---|---|
| 1 | **Propósito** | Una frase, desde la perspectiva de quien lo usa: ¿para qué es? | Helix (`purpose`); artículo de 5 pasos |
| 2 | **Nunca usar para** | Lista de usos que **no** corresponden y qué usar en su lugar | Helix (`neverUseFor`); artículo |
| 3 | **Justificación** | ¿Por qué es así? Una o dos frases con la decisión y su motivo | Helix (`rationale`); artículo («decisiones, no solo reglas») |
| 4 | **Qué se adapta y qué se escala** | Qué puede cambiar cada proyecto por su cuenta y qué debe pedirse al sistema | Helix (`governance`); artículo |
| 5 | **Anatomía** | Las partes, con el **mismo nombre en código y en Figma** | Helix (`anatomy`); artículo |

**Plantilla** (Markdown; ejemplo propio, no tomado de Helix):

```markdown
# Botón de acción
**Propósito:** lanza una acción o lleva a un destino cuando la persona lo pulsa.
**Nunca usar para:** navegar entre páginas (usa un enlace) · guardar un ajuste que persiste (usa un interruptor).
**Justificación:** tres tamaños para evitar una escala dispersa; el estado «cargando» conserva el tamaño para que nada salte.
**Se adapta en el proyecto:** añadir un icono; pasar una etiqueta accesible.
**Se escala al sistema:** una variante nueva; cambiar su relleno o altura.
**Anatomía:** `boton` (raíz, elemento nativo) · `boton-icono` (hueco, opcional) · `boton-etiqueta` (texto).
**Estados que se entregan (website):** normal · hover · foco · deshabilitado · cargando.
```

## 4. Contrato completo

Basado en el esquema de Helix (JSON Schema **draft-07**; la versión vigente es **2020-12**: elige una y **fíjala**, no mezcles). Reexpresado:

| Campo | ¿Obligatorio en el esquema de Helix? | Quién lo escribe | Qué dice |
|---|---|---|---|
| `name` | Sí | Persona | Nombre del componente en PascalCase |
| `version` | Sí | Persona | `x.y.z` (formato comprobado por patrón) |
| `status` | No | **Script** (se calcula; ver 07) | `draft` · `beta` · `stable` · `deprecated` |
| `purpose` | Sí | Persona | Una frase desde quien lo usa |
| `import` | No | **Script** (generado del índice de exportaciones; «no editar a mano») | La instrucción exacta de importación |
| `neverUseFor` | No | Persona | Antipatrones |
| `rationale` | No | Persona | Por qué se decidió así |
| `governance` | No | Persona | `mayExtendLocally` (adaptaciones permitidas, con `// [CUSTOM] motivo`) y `mustEscalateToDS` (cambios que alteran lo compartido) |
| `states` | Sí | Persona | `intrinsic` y `authored` (sección 6) |
| `anatomy` | Sí | Persona | Lista de partes: `part`, `element` (etiqueta HTML o `slot`), `description`, `optional` |
| `props` | Sí | Persona | Lista de props: `name` (canónico, ver 03), `type`, `default`, `required`, `description` |
| `tokenPolicy` | Sí | Persona | `allowed` y `forbidden`: prefijos de token permitidos y prohibidos (ver 02) |
| `a11y` | No | Mixto | `role`, `keyboardNav`, `wcag`, `announces`, `humanReview` (persona) + `applied` y `results` (**script**, «no editar a mano») |
| `sizing` | No | Persona | Altura (`fixed` o «según filas»), ancho (`hug`, `fill`, `fixed`), notas |
| `figma` | No | Persona | Cómo se representa en Figma: propiedades **solo-Figma**, excepciones aprobadas, estados que debe tener el eje `state` (ver 05) |

**Observaciones sobre la fuente (verificadas leyendo el esquema y un contrato, 2026-10-27):**
- El esquema **exige solo 7 campos** (`name`, `version`, `purpose`, `states`, `anatomy`, `props`, `tokenPolicy`) y **prohíbe campos desconocidos** en la raíz. «Nunca usar para», justificación y gobierno son **opcionales en el esquema**: que los 33 componentes los tengan lo exige **otro verificador** (el de gobierno). Moraleja: *el esquema fija la forma, un verificador aparte fija la política*.
- **Se mezclan partes humanas y generadas** en el mismo archivo. Esa mezcla es la que obliga a marcar «no editar a mano». En tu proyecto, **sepáralas o márcalas** (`generado` en el campo) para que nadie —ni una IA— las edite.

## 5. Origen del componente (campo propio, recomendado en `app` y `sistema compartido`)

Un contrato debe declarar **de dónde sale el componente**: repositorio, archivo de Figma y nombre exacto, y si viene del sistema propio, de una librería abierta o de un tercero. Sin eso, una IA elige al azar y **mezcla fuentes** (usa el de la librería pública porque hay mucha información sobre ella). Añade una regla explícita: **«usa el nuestro, no el de la librería base»**.
*Fuente: dos videos de la autora (`ud25`, `9c1Z`). **No está en el esquema de Helix**: es una propuesta a incorporar al esquema propio y a probar en un caso real.*

## 6. Estados

- **Intrínsecos:** los gestiona el navegador (hover, foco, activo). **Nunca se construyen como props.** En Figma se dibujan con la propiedad **solo-Figma** `state`.
- **Gestionados:** los controla el componente mediante props (cargando, deshabilitado, inválido); cada uno con su **atributo ARIA** cuando lo hay.
- **Deshabilitado:** con colores reales del sistema, no con opacidad *(decisión estética de Helix: va como ejemplo, no como regla universal)*.

## 7. Anatomía y partes

Cada parte lleva **un nombre** que se usa **igual** en el código (un atributo `data-…-part`) y en Figma (el nombre de la capa). `element` es la etiqueta HTML o `slot` (un hueco para otro componente). Marca las **opcionales**.

## 8. Props

Nombre **canónico** (de la referencia 03, no el que se te ocurra), tipo, valor por defecto, si es obligatoria, descripción. Si un texto se pasa como contenido, **no** lo llames `label`. **El valor por defecto debe ser el mismo en código y en Figma:** en el archivo de Helix, el contrato de Button dice que `size` es `m` por defecto y la propiedad de Figma tiene `s` por defecto; la auditoría debe **comparar los valores por defecto**.

## 9. Gobierno por componente

- **Nunca usar para** (antipatrones), **puede extender localmente** y **debe escalar al sistema**.
- Un componente propio de un proyecto se marca (`// [CUSTOM] motivo`) y se parte de un andamio con las reglas del sistema, no de cero. Cuenta como **deuda** y se mide (ver 07).
- Quién decide un cambio y con qué procedimiento depende del perfil de gobierno (ver 08).

## 10. Accesibilidad dentro del contrato

Registra el **rol**, las **teclas** y los **criterios WCAG** con su **nombre oficial y nivel**. Contrastado con la norma (WCAG 2.2, 2026-10-27):

| Criterio | Nombre oficial | Nivel | Umbral |
|---|---|---|---|
| 1.4.3 | Contrast (Minimum) | AA | 4,5:1 texto normal; 3:1 texto grande |
| 1.4.11 | Non-text Contrast | AA | 3:1 contra los colores adyacentes |
| 2.1.1 | Keyboard | A | — |
| 2.4.7 | Focus Visible | AA | — |
| 2.5.8 | Target Size (Minimum) | AA | **24 × 24 px CSS** (con excepciones) |
| 4.1.2 | Name, Role, Value | A | — |

El contrato de Helix escribe los nombres **abreviados** («1.4.3 Contrast (AA)»): usa los oficiales. Los resultados de comprobaciones automáticas **no se mezclan con una revisión humana** en una puntuación (idea de Helix: la revisión de una persona se registra pero no puntúa). Lo no automatizable (¿tiene sentido lo que lee el lector de pantalla?) se anota en `humanReview` con fecha, quién y con qué tecnología.

## 11. Figma dentro del contrato

Solo **cómo se representa**, no qué es el componente. Registra las propiedades **solo-Figma** (p. ej. `state`), las **excepciones** a la regla de conversión (con quién las aprobó y cuándo) y los estados que debe tener el eje `state`. La regla de conversión y la auditoría viven en la referencia 05.
**No copies cifras al contrato** («68 variantes»): en el archivo de Helix el contrato y la descripción del conjunto dicen 68 variantes y el conjunto real tiene **144**. **Cuenta con un script, no escribas el número.** *(Causa no verificada.)*

## 12. Componentes base, compuestos y de superposición

- **Base** (se usan para construir otros, no solos): se marcan en el contrato (p. ej. `kind: base`) y en Figma con un **prefijo que los oculta** (un punto o guion bajo al inicio, como `.[BC] Nombre`). *Fuente: plantillas de documentación de la comunidad (`F4`, `F5`); la propiedad `kind` es inferencia propia.*
- **Compuestos** (Table = Table + HeaderCell + Cell + Row): un contrato por pieza, o uno con **hijos** que enumere dónde vive cada prop en Figma. **No** esperes un único conjunto de variantes.
- **De superposición** (Modal): suele ser **un solo componente** sin variantes; su contrato pone el peso en **foco, teclas de cierre y anuncio**.

## 13. Cómo se valida un contrato

Tres comprobaciones **distintas**; no las confundas:
1. **Forma:** ¿el JSON cumple el esquema? (Helix: `verify:contract`, «33 contratos válidos». **Aclaración posterior (2026-10-27, al construir los scripts):** ese script **no valida el esquema completo**: comprueba campos obligatorios, valores de `status`, sinónimos prohibidos en props, partes de anatomía en kebab-case y que un token no esté a la vez en permitidos y prohibidos, y está en **modo solo informe**. Al pasar los 33 contratos por un validador de esquema, 2 incumplen la propia declaración del esquema: seis campos de raíz no declarados y un estado «authored» escrito como texto en lugar de objeto.)
2. **Política:** ¿tiene todo lo que el sistema exige, aunque el esquema lo deje opcional? (Helix: `verify:governance`.)
3. **Implementación:** ¿las **props** del código coinciden con el contrato? (Helix: `verify:types`; comprueba solo props, **no** las partes de la anatomía ni los estados.)

Estos tres se **ejecutaron** en Helix en el commit `394823a` (matriz, filas 109–116; ver la aclaración sobre el primero). **Verificador propio:** `scripts/validar_contrato.py` comprueba la **forma** (contra `scripts/contrato.schema.json`) y, con `--politica`, la **política**; acepta saltos de línea de Windows, declara su alcance y se probó con 25 pruebas y con los 33 contratos de Helix. **La tercera comprobación (props del código frente al contrato) no existe como script propio**: `scripts/vocabulario_check.py` revisa solo nombres de atributos y `scripts/comparar_figma_contrato.py` solo Figma. Si no se ejecutó un verificador, la skill **no puede decir «contrato válido»**: dice «revisado a mano contra esta lista».

## 14. Lista de revisión (la usa `auditar`)

- [ ] Propósito en **una frase** y desde quien lo usa.
- [ ] «Nunca usar para» con la **alternativa** nombrada.
- [ ] Justificación con la **decisión**, no solo la regla.
- [ ] Qué se adapta y qué se escala.
- [ ] Anatomía con el mismo nombre en código y Figma; partes opcionales marcadas.
- [ ] Estados: intrínsecos separados de los gestionados; ARIA de cada uno.
- [ ] Props con nombre canónico y **valor por defecto igual en código y Figma**.
- [ ] Origen declarado (`app`, `sistema compartido`).
- [ ] Criterios WCAG con nombre oficial.
- [ ] Partes **generadas** marcadas y no editadas a mano.
- [ ] Sin cifras copiadas que se desactualicen.

## 15. Fuentes y estado de la verificación

| Idea | Fuente | Estado |
|---|---|---|
| Contrato mínimo de 5 campos | Artículo de 5 pasos de la autora de Helix | Reexpresado; no contrastado con otra fuente |
| Esquema completo, estados, anatomía, props, política de tokens, gobierno | Esquema y contrato de Button de Helix (`394823a`) | **Leído y ejecutado**; no es una norma, es la decisión de un sistema |
| Qué exige el esquema frente a qué exige un verificador | Esquema + prueba local (`verify:governance`) | **Verificado** el 2026-10-27 |
| Valor por defecto de `size` distinto entre código y Figma; 68 frente a 144 variantes | Contrato de Button + lectura del archivo de Figma | **Observado**; causa no verificada |
| Origen del componente y regla «usa el nuestro» | Dos videos de la autora | Propuesta; sin caso propio |
| `kind: base` y prefijo que oculta | Plantillas de la comunidad | Convención observada; propiedad propia sin probar |
| WCAG (tabla de la sección 10) | W3C, WCAG 2.2 | **Contrastado** (nombre, nivel, umbrales) |
| Versión vigente de JSON Schema | json-schema.org | **Contrastado** (2020-12; draft-07 es anterior) |

**Límites:** nada de esto se ha probado en un proyecto propio (`caso-ds-01` pendiente); el contrato mínimo para `website` es la versión más barata y la que más falta por validar.
