# 05 · Figma: variables, propiedades, paridad y auditoría

> **Estado:** borrador (C-2, 2026-10-27) · **Perfiles:** los tres (cambia cuánto se espeja) · **Modos que la usan:** `construir`, `auditar`, `verificar`, `documentar`.
> **Fuentes (reexpresadas; ver `CREDITOS.md`):** el sistema **Helix** (MIT, © 2026 Marta Conde; commit `394823a`: su estándar de conversión código→Figma, sus guías de construcción y la **lectura real de su archivo de Figma** hecha en esta investigación), los archivos de la comunidad F1–F5 y los videos de la autora. **Inferencia propia** va marcada.
> **Contrastado con fuente primaria el 2026-10-27:** los tipos de propiedad de componente, la visibilidad como único uso del BOOLEAN y el orden de las propiedades de variante (ayuda de Figma y API de plugins); propiedades de variables (alcances, ocultar al publicar, descripción; ver 02). **No contrastado:** los trucos de la API que Helix documenta (color de reserva, opacidad, sombra con expansión), el comportamiento de `SLOT`, y los **valores por modo** de las variables del archivo.
> **Plantillas y scripts:** `templates/tabla-antes-despues.md` · `templates/ficha-de-auditoria.md` (anexo de Figma) · `scripts/comparar_figma_contrato.py`.

## 1. Qué papel juega Figma

Figma es **la representación visual** del sistema; **la fuente de verdad la fija el proyecto** (por defecto contrato/código; si el proyecto parte de Figma, se registra). Esta referencia dice **cómo se espeja** sin que se separen. Requisitos de la herramienta (resumen de `SKILL.md`):
- **Cargar `figma:figma-use` antes de cada `use_figma`.** Una lectura (solo consulta) no necesita las skills de creación; **escribir** exige además la skill de diseño o de librería.
- **Mostrar y esperar aprobación antes de escribir.** Lecturas por API: **una página por llamada** y varias llamadas en paralelo.
- **Nunca** leer `componentPropertyDefinitions` de una variante suelta: se lee del **conjunto**.

| Perfil | Qué se espeja |
|---|---|
| `website` | Una **página por componente** con sus estados y los **mismos nombres** que el código; variables de color y de espaciado si ya hay; sin librería publicada |
| `app` | Las **cuatro colecciones** (sección 2), propiedades con paridad exacta y **auditoría** por componente |
| `sistema compartido` | Igual + **librería publicada** y un archivo de la comunidad o de consumo |

## 2. Colecciones y modos

Estructura **real** del archivo de Helix (leída por API, 2026-10-27):

| Colección | Variables | Modos | Contenido |
|---|---|---|---|
| `Primitives` | 115 | `default` | 61 de color, 52 numéricas, 2 de texto |
| `Semantic` | 49 | `default` | Numéricas: radios, espaciado de componente y de maquetación, tamaños de fuente móvil; 33 son alias |
| `Theme` | 73 | `light`, `dark` | Colores semánticos: **todos alias** de primitivos |
| `Responsive` | 14 | `desktop`, `tablet`, `mobile` | Tamaños de fuente e interlineados: alias |

- **No se espeja todo:** 251 variables frente a 803 tokens del código; **no existe la capa de componente** (487) como variables. Los colores semánticos viven en `Theme`, no en `Semantic`.
- **Nombres:** barras que crean grupos, **sin prefijo del sistema** y sin la categoría (ver 02, sección 5). **Las colecciones tampoco llevan prefijo** del sistema.
- **Alcance (`scopes`) y ocultar al publicar:** ver 02, sección 10. En Helix, los primitivos de color tienen alcance «ninguno»; `Theme`, el de rellenos, trazos y efectos. **Fija siempre el alcance.**
- **Modos:** el tema es un modo de `Theme`; el responsive es un modo de `Responsive`. Un nodo o un marco **toma el modo de su contenedor**, así que un marco `Mobile` cambia todo lo que lleva dentro (lo muestra el webinar de tipografía; **no** se verificó ni en el archivo ni en la API).
- **Una colección por punto de corte con estructura fija,** aunque algo no cambie, para que el desarrollo no tenga que adivinar.
- **Descripción:** pon en `description` de la variable **la misma frase** que el `$description` del token (ver 02).
- **Discrepancia hallada en la guía de Helix:** su texto de proceso habla de colecciones llamadas `Color` y `Spacing`, pero el **archivo real** tiene `Theme`, `Semantic`, `Primitives` y `Responsive`. **Documentos de proceso y archivo real se separan**: cuando los dos difieren, **manda el archivo** y se corrige el documento.
- **Valores por modo:** no se leyeron (solo estructura y alcances).

## 3. Estilos

- En Helix: **22 estilos de texto** (`Familia / tamaño / peso`, p. ej. `Body / m / Medium`), **6 de efecto** (sombras xs–xl y foco) y **0 de pintura**: **los colores solo existen como variables**.
- Un estilo de texto está **compuesto** por variables (tamaño, interlineado, peso, familia): **una variable no compone** otras, se enlazan al estilo (ver 02, sección 7).
- **El texto se aplica con un estilo de texto real,** no enlazando una variable de tamaño suelta (regla de la guía de Helix; el motivo exacto está en un registro suyo que **no se leyó**).
- **Interlineado:** en el código es una proporción; en Figma, píxeles (resultado de tamaño × proporción) **como literal**.

## 4. Propiedades de componente

**Tipos que ofrece Figma (contrastado):** `VARIANT`, `BOOLEAN`, `TEXT`, `INSTANCE_SWAP` y, **ya disponible,** `SLOT` (un hueco editable). Hechos comprobados:
- **Un BOOLEAN solo controla la visibilidad de una capa;** no puede cambiar un color ni un tamaño.
- **Las propiedades de variante van siempre arriba** en el panel y no se intercalan con las demás.
- `INSTANCE_SWAP` admite **valores preferidos**.
- En la API, las propiedades que no son de variante llevan un **sufijo oculto `#id`** en su nombre (`children#665:33`); **quítalo al comparar** con el código.

**Regla de conversión (estándar de Helix, aprobado una vez por el dueño):** *mismo nombre, mostrado igual en el panel.*

| Prop del código | Propiedad de Figma | Nota |
|---|---|---|
| Unión `'a' \| 'b'` | `VARIANT` con los **mismos valores** | |
| Booleano que **cambia el aspecto** (`disabled`, `invalid`, `checked`, `isLoading`, `fullWidth`) | `VARIANT` `false` / `true` | Se muestra como interruptor; un BOOLEAN **no puede** cambiar un color |
| Booleano que **solo muestra u oculta** una parte (`required`, `dismissible`) | `BOOLEAN`, mismo nombre | |
| Texto que una parte dibuja (`children`, `label`, `placeholder`) | `TEXT`, mismo nombre | |
| Texto opcional con su parte (`description`, `errorMessage`) | `BOOLEAN` `name.` + `TEXT` `name` | El ayudante lleva un **punto final** y va **antes** |
| Ícono (`icon`, `iconEnd`) | `BOOLEAN` `icon.` + `INSTANCE_SWAP` `icon` | Si el ícono es obligatorio, solo el intercambio |
| Hueco opcional (`header`, `footer`…) | `BOOLEAN`, mismo nombre | **`SLOT` es una opción nueva, sin probar** |
| Lista que el componente dibuja (`options`) | `VARIANT` con el **número** de elementos (2…7) | Figma no itera datos |
| Lista que se entrega a otro componente | Una **instancia anidada expuesta** de ese componente | El número va en el hijo |
| Manejadores `on*`, identificadores, referencias, texto solo para lectores de pantalla | **Ninguna** | No son una propiedad de diseño |

Más reglas:
- **Nombres en camelCase,** nunca con espacios; la propiedad es **el nombre del código sin cambiar** (`isLoading`).
- **`state` es la única propiedad solo-Figma regular:** `default`, `hover`, `press`, `focus` (y `open`, `selected`): son **pseudoclases**, no props. **`disabled`, `invalid`, `checked`, `isLoading`… nunca son valores de `state`.**
- Los **ayudantes solo-Figma** terminan en punto, también como VARIANT (`value.` vacío/relleno, `placement.`). Según Helix, Figma **no admite dos propiedades con el mismo nombre**, por eso el ayudante es el que cambia *(no contrastado)*.
- **Una propiedad de Figma sin prop de código es un fallo,** no una nota: se renombra, se quita o se aprueba como excepción con motivo.
- **Props que nunca tienen propiedad:** una URL de imagen (Figma no puede cargarla; la apariencia «foto o iniciales» es una VARIANT solo-Figma) y los `aria-*` (se leen, no se dibujan).
- **Valores por defecto iguales** en código y Figma: se **comparan** (en Helix, `size` era `m` en el código y `s` en Figma).

**Verificado en el archivo real de Helix:** Button (144 variantes), Input (64) y Checkbox (21) cumplen la regla; **Table** se arma con componentes sueltos más un conjunto `TableRow` y **Modal es un solo componente** sin variantes.

## 5. Cómo se dibujan las variantes

- **Estados:** el eje `state` lleva todos los valores del contrato. «Diseñar solo normal y deshabilitado» es una sincronización fallida.
- **Deshabilitado** solo con `state=default` y sin invalidez (no recibe hover ni foco); **todo su texto** usa el color de texto deshabilitado.
- **Interruptores secundarios** (`fullWidth`, `isLoading`…) en **todos los tamaños y estados que el código puede alcanzar**; el límite es lo que el código no puede mostrar (un botón cargando está deshabilitado: se dibuja solo en `state=default`).
- **Combinaciones imposibles no se dibujan** (casilla marcada e indeterminada a la vez). El contrato las enumera.
- **Los booleanos se activan en el panel,** nunca se expanden en variantes ni columnas.
- **Anillo de foco sin recortar:** en Helix, los marcos que rodean el anillo tienen *Clip Content* desactivado, y la propia capa del anillo lo tiene activado (una sombra con expansión solo se dibuja en un marco que recorta). *Observación de Helix, sin contrastar.*
- **El borde siempre existe:** una variante con borde lo tiene en todas, y los estados solo cambian su color.
- **Mostrar/ocultar partes con BOOLEAN, no con VARIANT:** reduce el número de variantes (en Chip, de 100 a 50), pero **solo si el código lleva el espaciado dentro de la parte** y los rellenos del contenedor no cambian al activarla.
- **Colores:** salen del **código** (se renderiza cada variante y estado en claro y oscuro y se registran los colores calculados), **no de leer el CSS**, y se **enlazan a una variable semántica**; nunca un color suelto ni una variable primitiva. Una mezcla de colores del CSS (`color-mix`) no tiene variable: se modela con una capa de estado con **opacidad de capa**.
- **Espaciado:** siempre una **variable enlazada**; ni nodos «separadores» ni espacios negativos; una distancia fuera de escala se **parte en dos valores de escala** en cajas anidadas (primero en el código, luego en Figma).

**Trampas de la API que Helix documenta** *(sin contrastar, salvo la primera)*: una pintura enlazada **devuelve una pintura nueva** que hay que reasignar (contrastado: regla de la guía de Figma); el color de reserva de una pintura enlazada puede dibujarse en lugar de la variable (se pone el valor claro resuelto); la opacidad de la pintura se ignora si hay variable (se usa opacidad de capa); la expansión de una sombra solo se dibuja en un marco con recorte.

## 6. Patrones

Cada componente sigue **un patrón** y un componente nuevo se convierte **igual que sus hermanos**. Helix usa seis (ejemplo; tu proyecto define los suyos):

| Patrón | Componentes | `state` |
|---|---|---|
| **Campo de formulario** | Input, Textarea, Select, MultiSelect | default / hover / focus |
| **Casilla** | Checkbox, RadioButton, Switch | default / hover / focus |
| **Grupo** | CheckboxGroup, RadioGroup, ChipGroup | ninguno (cada elemento tiene el suyo) |
| **Acción** | Button, IconButton, FAB, Chip, SegmentedControl, NavItem | default / hover / press / focus |
| **Superposición** | Modal, SidePanel, Menu, Tooltip | default; se dibuja **abierto** |
| **Hueco de maquetación** | AppShell, PageHeader, Card, TopBar, SideNav | default |

Reglas de patrón: los **campos de formulario comparten un ancho** (en Helix, 320 px; y una versión «ancho completo» dibujada con relleno); un elemento **flotante** (tooltip) dibuja **el componente al que acompaña** como un intercambio de instancia con valores preferidos; un aspecto que el código solo muestra al interactuar puede **dibujarse como un estado** si forma parte del diseño. *Todo ello es decisión de Helix.*

## 7. Paridad: orden y cobertura

- **Orden de las propiedades:** primero las que son variantes y después el resto, **en el mismo orden en código y Figma**. La referencia del orden es **lo que muestra la documentación**, no el orden del contrato (en Helix, 9 componentes estaban desordenados mientras la comprobación decía ✓).
- **Cada historia o ejemplo tiene una representación en Figma** (las propiedades y valores que lo dibujan, el valor por defecto, «solo disposición», o una decisión del dueño de que no se dibuja). Una historia de teclado se dibuja como `state=focus`. Una historia sin entrada **impide** marcar el componente como sincronizado. *(Helix; en `website`, sin historias, se omite.)*
- **Generado, no escrito a mano:** el listado de cada prop con la propiedad de Figma en que se convierte se **genera** desde la regla; el contrato solo guarda las **excepciones aprobadas**.
- **Componentes que no están en Figma por decisión:** en Helix, los de maquetación y las páginas; y **Icon**, que solo existe en el código (en Figma cada variante coloca su ícono al tamaño y trazo correctos). **Documéntalo en el contrato** para que no se tome por deriva.

## 8. Auditoría de un componente

**Lista (basada en la auditoría automática de Helix; en esta skill, de momento, manual o por lecturas de solo consulta):**
1. Cada color de relleno, trazo y texto está **enlazado a una variable semántica del tema**, sin colores sueltos ni primitivas.
2. Espaciado y radios **enlazados**; sin espacios negativos ni nodos separadores.
3. **Todos los valores de `state`** del contrato están dibujados.
4. **Colores iguales a los del código** en claro y oscuro.
5. **El borde siempre existe.**
6. **Paridad de propiedades:** nombres, tipos y valores iguales; sin propiedad solo-Figma sin aprobar; **valores por defecto iguales**.
7. **Listas:** el número vive en el componente que dibuja los elementos; los elementos de una lista están en reposo.
8. **Anillo de foco sin recortar.**
9. Descripción del componente presente; nombres de capa = nombres de las partes del contrato.

**Auditoría propia: parcial.** `scripts/comparar_figma_contrato.py` compara propiedades, valores por defecto, opciones, orden y eje de estados a partir de una lectura de solo consulta guardada en un archivo. La auditoría visual (variables enlazadas, colores, foco, listas) **sigue siendo manual**: la skill lo dice y entrega **«revisado a mano»**, con las lecturas de variables y propiedades como evidencia.

## 9. Organización del archivo

Convención de Helix (**estilo de un sistema**): `Cover` → `About` → separador → `Icons` → separador → **una página por componente en orden alfabético**, con separadores con nombre. En cada página, **una tarjeta** con nombre, propósito (el del contrato), un divisor y la **tabla de variantes**. Un cambio en el archivo de trabajo se repite en el **archivo publicado** en la misma tarea (regla de Helix).
En `website`: una página por componente alcanza; el resto es opcional.

## 10. Flujo de trabajo en Figma

1. **Variables** (colecciones, modos, alcances, descripciones) → 2. **íconos** → 3. **componente** (partes con los nombres del contrato; diseño automático; estados) → 4. **enlazar variables** y **estilos** → 5. **propiedades** (regla de la sección 4) → 6. **auditoría** → 7. **tabla de propiedades y tarjeta de documentación** → 8. registrar.
Los pasos 1 a 7 **se previsualizan y se aprueban** antes de escribir. Para el método HTML→Figma de `direct-visual-design` (1920 × Hug, 240 px laterales, 80 px por sección, múltiplos de 4), la entrega es **otra distinta**: no se mezclan.

## 11. Lectura de solo consulta (lo que esta skill puede hacer hoy)

Con `use_figma` en modo **solo lectura** (sin crear ni editar): listar colecciones, modos y variables; leer alcances y descripción; estilos locales; `componentPropertyDefinitions` **del conjunto**; texto de nodos; `get_variable_defs` de un componente. **Una página por llamada**, varias en paralelo; un identificador de página equivocado da un error de `null`. **Hecho en esta investigación** sobre archivos de la comunidad sin duplicarlos. Las funciones **asíncronas** de variables y estilos funcionan; **las síncronas que usa la guía de Helix no se probaron**.

## 12. Lista de revisión (la usa `auditar`)

- [ ] Fuente de verdad **registrada** y coherente con lo que hay.
- [ ] Colecciones y modos según el perfil; **alcance fijado**; primitivos fuera de los selectores.
- [ ] Nombres de variable con la **tabla de traducción** (02).
- [ ] Texto con **estilos de texto reales**.
- [ ] Propiedades según la regla de conversión; **sin propiedades solo-Figma sin aprobar**.
- [ ] **Valores por defecto iguales** que en el código.
- [ ] Todos los **estados** y combinaciones alcanzables dibujados.
- [ ] Colores y espaciado **enlazados**; sin literales.
- [ ] Documentación y orden **alfabético** (si el proyecto lo adopta).
- [ ] Componentes **fuera de Figma** documentados en el contrato.
- [ ] Documentos de proceso **coherentes con el archivo real**.

## 13. Fuentes y estado de la verificación

| Idea | Fuente | Estado |
|---|---|---|
| Colecciones, modos, alcances, nombres reales | Archivo de Figma de Helix (lectura por API) | **Verificado** (valores por modo sin leer) |
| Tipos de propiedad; BOOLEAN = visibilidad; variantes arriba; valores preferidos | Ayuda de Figma + API de plugins | **Contrastado** |
| `SLOT` como tipo nuevo | API de plugins y ayuda de Figma | **Contrastado que existe; uso sin probar** |
| Regla de conversión y patrones | Estándar de Helix (`figma-conversion`) | **Leído**; paridad **verificada** en Button, Input y Checkbox |
| Table y Modal sin conjunto de variantes | Archivo de Helix | **Verificado** |
| Discrepancia de colecciones entre la guía y el archivo | Guía de Helix + archivo | **Hallazgo propio** |
| Trampas de la API (color de reserva, opacidad, sombra) | Guía de Helix | **No contrastadas** (salvo la pintura nueva) |
| Auditoría de 12 comprobaciones | Guía y script de Helix | Leído; **no ejecutado** |
| Hueco `SLOT` como opción para huecos | — | **Propuesta sin probar** |
| Perfil `website`: página por componente y nombres iguales | — | **Inferencia propia, sin probar** (`caso-ds-01`) |

**Límites:** casi todo viene de **un sistema** (Helix) y de **un archivo**; no se ejecutó ninguna escritura en Figma, y la auditoría automática de Helix **no está adaptada** a esta skill.
