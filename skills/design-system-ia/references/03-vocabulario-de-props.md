# 03 · Vocabulario de props y nombres de componentes

> **Estado:** borrador (C-2, 2026-10-27) · **Perfiles:** los tres (en `website` se aplica a atributos y clases, ver 3) · **Modos que la usan:** `contrato`, `construir`, `auditar`, `verificar`, `definir`.
> **Fuentes (reexpresadas; ver `CREDITOS.md`):** el sistema **Helix** (MIT, © 2026 Marta Conde; commit `394823a`: su mapa de props, la decisión ADR-022, la regla del linter y las pruebas que ejecuté), el artículo de agentes de la misma autora y el archivo de la comunidad de nombres de componentes, propiedades y valores (**CC BY 4.0**). **Inferencia propia** va marcada.
> **Contrastado con fuente primaria el 2026-10-27:** los atributos ARIA y HTML nativos que los nombres reutilizan (MDN) y la convención de nombres de React. **No contrastado:** que `readOnly` figure en la documentación de React (se deduce de su convención), cómo nombran props otras librerías, y cualquier regla para WordPress o Astro.
> **Plantillas y scripts:** `templates/vocabulario.md` · `templates/tabla-antes-despues.md` · `scripts/vocabulario_check.py`.

## 1. Para qué sirve

Un agente **no puede preguntar** cómo se llama algo: escribe lo que cree. Si el sistema acepta cinco nombres para lo mismo, el código queda inconsistente y nadie sabe cuál es el correcto. Un **vocabulario canónico** fija **un nombre por concepto** y lista los **sinónimos prohibidos**; la columna de **prohibidos** es la clave, porque es lo que un verificador puede aplicar y lo que permite corregir solo.

Se compone de: **props** (`variant`, `size`…), **valores** (`primary`, `m`…), **nombres de componentes** (`IconButton`) y **eventos** (`onClick`). Todo con **la misma palabra en código y en Figma**.

## 2. Cómo se elige un nombre (en este orden)

1. **El nombre nativo, si existe y significa lo mismo.** Si HTML o ARIA ya tienen la palabra (`disabled`, `required`, `checked`, `placeholder`, `aria-expanded`, `aria-invalid`…), úsala; no inventes otra.
2. **Lo que los modelos ya escriben.** En Helix, 35 respuestas de agentes **sin ninguna guía** eligieron `onClick` (12 frente a 3 de `onPress`) y `isLoading` (6 frente a 2 de `loading`), y el sistema cambió sus nombres a esos. *Es evidencia de una muestra muy pequeña; úsala como criterio de desempate, no como prueba.*
3. **Un concepto, un nombre.** Y **un nombre, un concepto**: los nombres ambiguos (`type`, `state`, `variant`, `layout`, `orientation`, `direction`, `mode`, `content`, `value`) **no se reutilizan con otro sentido** en el mismo sistema.
4. **Patrón observado (inferencia propia):** en Helix, los estados que HTML o ARIA ya nombran van **sin prefijo** (`disabled`, `checked`, `invalid`, `required`, `expanded`, `current`) y los propios del sistema **con `is`** (`isLoading`); lo de diseño sin prefijo (`fullWidth`). Úsalo como guía, no como regla escrita por Helix.
5. **El texto visible es `children`, no `label`,** cuando el componente lo recibe como contenido (en Helix, un Button nunca lleva `label`); `label` queda para los campos de formulario. *El vocabulario depende de la **clase de prop**, no solo de la palabra.*
6. **Valida con diseño y desarrollo:** lo que a ti te parece estándar a otra persona le es ajeno.

## 3. Mismo concepto, cada plataforma (tabla de traducción)

Mantén esta tabla **en el proyecto**. Ejemplo con el vocabulario de Helix; **las columnas de ARIA, HTML y React están contrastadas; la de HTML/WordPress/Astro para atributos propios es inferencia propia, sin probar (`caso-ds-01`).**

| Concepto | Prop en React | HTML / ARIA nativo | Atributo propio en HTML+CSS *(inferencia)* | Propiedad en Figma |
|---|---|---|---|---|
| Estilo visual | `variant` | — | `data-variant="primary"` | VARIANT `variant` |
| Tamaño | `size` | — | `data-size="m"` | VARIANT `size` |
| Cargando | `isLoading` | `aria-busy` | `aria-busy="true"` + `data-loading` | VARIANT `isLoading` (false/true) |
| Deshabilitado | `disabled` | atributo `disabled` (solo controles de formulario) / `aria-disabled` | `disabled` o `aria-disabled` | VARIANT `disabled` |
| Actual (navegación) | `current` | `aria-current` | `aria-current="page"` | VARIANT `current` |
| Expandido | `expanded` | `aria-expanded` | `aria-expanded` | VARIANT `expanded` |
| Marcado | `checked` | `checked` / `aria-checked` | igual | VARIANT `checked` |
| Inválido | `invalid` | `aria-invalid` | igual | VARIANT `invalid` |
| Obligatorio | `required` | `required` / `aria-required` | igual | BOOLEAN `required` |
| Acción | `onClick` | evento `click` | `addEventListener('click', …)` | — (los manejadores no tienen propiedad) |

**Figma:** verificado en el archivo real solo para `variant`, `size`, `isLoading`, `fullWidth`, `disabled`, `checked`, `invalid` (VARIANT) y `required` (BOOLEAN); `current` y `expanded` siguen la regla de conversión de Helix (un booleano que cambia el aspecto es VARIANT) **sin haberse visto en un componente**.

Convenciones comprobadas: React escribe los manejadores en camelCase (`onClick`), usa `className` y `htmlFor`, y deja `aria-*` y `data-*` **como en HTML**.

## 4. La tabla del vocabulario

Una fila por concepto. Columnas: **Canónico · Prohibidos · Dónde aplica · Equivalencia nativa · Figma · Decisión (quién y cuándo)**. La fila lleva su **fecha y su porqué**, porque las reglas cambian.

**Ejemplo (tomado de Helix; cada proyecto decide el suyo):**

| Canónico | Prohibidos | Nota |
|---|---|---|
| `variant` | `type`, `kind`, `mode` | Estilo visual (primary, secondary…) |
| `size` | `scale`, `sz` | Valores con letras cortas: `xs` `s` `m` `l` `xl` (y no `small`, `md`, `large`, `base`) |
| `isLoading` | `loading`, `pending`, `isPending`, `busy` | Estado de carga del propio sistema |
| `disabled` | `isDisabled` | Nativo |
| `current` | `active`, `isActive`, `selected` | Elemento actual de una navegación |
| `expanded` | `isExpanded`, `open`, `isOpen` | Apertura de un desplegable |
| `checked` | `isChecked`, `selected` | Casilla o radio |
| `invalid` | `hasError`, `isError`, `error` | Fallo de validación |
| `required` | `isRequired` | Campo obligatorio |
| `danger` / `success` / `warning` / `info` / `neutral` (valores) | `error`·`destructive`·`delete`, `positive`·`ok`·`valid`, `caution`·`alert`, `information`·`tip`, `default`·`muted`·`subtle` | Variantes de significado |
| `onClick` · `onChange` · `onFocus` · `onBlur` · `onDismiss` | `onPress`·`onTap`·`onAction`, `onValueChange`·`onUpdate`, `onFocused`, `onBlurred`, `onClose`·`onCancel` | Manejadores |
| `label` · `description` · `placeholder` · `icon` · `iconEnd` · `labelEnd` · `children` · `options` | `title`·`name`·`text`, `subtitle`·`hint`·`helper`, `hintText`, `leftIcon`·`startIcon`, `rightIcon`·`endIcon`, `meta`·`suffix`, `content`·`body`·`slot`, `items`·`choices`·`list` | Contenido; los íconos se pasan **por referencia**, no ya creados |
| `fullWidth` · `align` | `block`·`fluid`·`stretch`, `textAlign`·`justifyContent` | Ancho y alineación |

**Cuatro filas que revisar antes de copiarlas (hallazgos de la lectura):**
1. **`readonly` figura como prohibido de `disabled`.** Contrastado: en HTML son atributos **distintos** (`readonly` solo en `<input>` y `<textarea>`; `disabled` en los controles de formulario) y ARIA los separa (`aria-readonly` / `aria-disabled`). **No son sinónimos**: no lo copies.
2. **`open` figura como prohibido de `expanded`,** pero `open` es un atributo **nativo** de `<details>` y `<dialog>`. Cuando el componente envuelve uno de esos elementos, el nombre nativo gana (Helix tiene una **lista de pasos permitidos**, ver 6, para estos choques).
3. **`default` está prohibido como valor** (`neutral`, `m`) pero `state=default` es un valor válido del eje `state` de Figma. **El vocabulario es por prop, no global.**
4. **`size` lista `xs` y `xl`,** pero el contrato de Button solo admite `s`, `m` y `l`: el vocabulario es la **escala**, el contrato el **subconjunto**.

## 5. Partir de lo que ya se usa: tablas de sinónimos

Para definir el vocabulario de un sistema que ya existe, no empieces por una página en blanco: lista **cómo lo llama cada persona y cada librería** y elige uno. La comunidad publica tablas así (CC BY 4.0); ejemplos de ellas:

| Propiedad | Nombres en uso |
|---|---|
| Tamaño | size · sizing · sizes · measure |
| Estado | state · status |
| Retroalimentación | feedback · validation error · state · type · status · variant |
| Eje | axis · orientation · layout · direction · type · vertical/horizontal · alignment |
| Posición | position · orientation · direction · placement |
| Tema | theme · visual context · style |
| Densidad | compact · extend · mode · spacing · density |
| Cantidad | amount · value · items · quantity · number |
| Se puede cerrar | dismissible · removable |

| Valor | Nombres en uso |
|---|---|
| `sm` | sm · small · s |
| `default` | default · enabled |
| `active` | active · press |
| `activated` | activated · active |
| `read only` | read only · view only |
| `error` | error · invalid |
| `success` | success · validated |
| `boolean` | boolean · yes/no · true/false · on/off |

**Cómo usarlas:** (1) subraya los nombres que **ya existen en tu código y en Figma**; (2) elige **uno** por concepto aplicando la sección 2; (3) los demás pasan a la columna de **prohibidos**; (4) **anota los rechazados** con su motivo. *Las tablas de la fuente **no dicen** cuál es el elegido: es tu decisión.* Fíjate en las colisiones: `type`, `state`, `variant`, `layout`, `orientation` y `direction` aparecen en **varios** conceptos a la vez.

## 6. Cómo aplicarlo: el verificador

**Lo que se probó en Helix (prueba local, `394823a`):**
- `verify:props` (script que busca el nombre **como texto**) dio **12 falsos positivos**: la palabra «default» o «selected» dentro de un mensaje y `type` dentro de la configuración de un gráfico; por eso corre en modo «solo informe».
- La regla de linter `helix/prop-vocabulary` (que mira **atributos reales** de cada componente importado) detectó **3 de 3** errores de un fragmento de prueba y **dijo la alternativa**: «`onPress` no es una prop de Helix; Button usa `onClick`», `loading`→`isLoading`, `size="medium"`→`"m"`, con corrección automática.

**Requisitos de un verificador propio (inferencia a partir de lo anterior). Implementados en `scripts/vocabulario_check.py` los puntos 1, 2, 3, 6, 7 y 8 (con atributos `data-*` y `aria-*` en etiquetas nativas); del 4, solo el mensaje con la alternativa, no la corrección automática; no implementado el 5 (valores):**
1. Mirar **props reales de cada componente**, no texto suelto.
2. **Solo avisar si el componente declara la prop canónica** (si no la tiene, no hay nada que corregir).
3. **Lista de pasos permitidos:** nombres que son atributos nativos (`type`, `name`, `title`, `readonly`…) en los componentes que reciben atributos HTML.
4. **Mensaje con la alternativa** y, si no choca con otra prop ya puesta, **corrección automática**.
5. **Valores** además de props (`size="medium"` → `m`).
6. **Aceptar saltos de línea de Windows (CRLF).**
7. Modo **informe** y modo **bloqueo**.
8. En `website` (HTML+CSS) el equivalente revisa **atributos `data-*`, `aria-*` y clases**, *sin caso propio*.
Si no se ejecutó el verificador, la skill **no puede decir «vocabulario verificado»**: dice «revisado a mano contra esta tabla».

## 7. Nombres de componentes (método de 4 pasos)

Guion de taller (archivo de la comunidad de la autora, CC BY 4.0), útil para `definir`:

1. **Identificar** qué es: componente (o base), **objeto** (contenedor o elemento: texto, componente, forma, medio), **propiedad** (tamaño, estado, dirección, expandible, tipo, cantidad, espaciado, tema) y **valor** (variante, booleano).
2. **Estructura:** qué lleva el nombre (un ícono, un signo, una palabra, una abreviatura) y **en qué orden** (modificador + elemento o elemento + modificador).
3. **Gramática:** categoría de palabra (sustantivo, adjetivo, participio, verbo…), **singular o plural**, mayúsculas (`camelCase`, `PascalCase`, `kebab-case`, `snake_case`) y cómo se **une** (sin espacio, espacio, punto, guion, guion bajo).
4. **Ordenar:** alfabético, secuencial o jerárquico.

**Ejemplo (de la fuente):** `icon-button` → componente · una palabra con modificador + elemento · sustantivo, singular, minúsculas y guion · ordenado junto a `button` y `close-button`.
**Alfabético,** además, en la lista de componentes de Storybook y en las páginas de Figma (decisión de Helix, **estilo de un sistema**, no regla universal).
**Componentes base:** se distinguen del resto (ver 01, `kind: base`, y el prefijo que los oculta en Figma).

## 8. Figma: la misma palabra

Cada prop que un diseñador ve tiene **una propiedad de Figma con el mismo nombre**, en el mismo orden que en el código y con las propiedades que son variantes **primero**. Verificado en el archivo real de Helix (Button, Input, Checkbox): `variant`, `size`, `isLoading`, `fullWidth`, `disabled`, `state` como **VARIANT**; `children` como **TEXT**; `icon.` + `icon` como **BOOLEAN + INSTANCE_SWAP**. **Un booleano que cambia el aspecto es una VARIANT `false/true`**; uno que solo muestra u oculta una parte es un BOOLEAN, con un **punto final** el ayudante solo-Figma (`icon.`). La única propiedad solo-Figma regular es `state`. Detalle y auditoría: referencia 05.

## 9. Gobierno del vocabulario

- **Quién decide:** en `app` y `sistema compartido`, **cambiar una fila del vocabulario es una decisión del dueño**; la IA **no** inventa nombres: presenta **2–3 opciones** con su efecto y espera. En Helix un *hook* lo exige antes de tocar el mapa.
- **Renombrar es un cambio mayor:** Helix cambió `onPress`→`onClick` y `loading`→`isLoading` de golpe, en contratos, tipos, historias, mapa, linter y pruebas a la vez, **sin periodo de alias** porque **no estaba publicado**. *En un sistema publicado, la propuesta (inferencia propia) es un periodo de alias con aviso de obsolescencia y una guía de migración.*
- **Registra los rechazados** y la fecha de cada decisión: «lo que no se escribe, se vuelve a discutir».

## 10. Lista de revisión (la usa `auditar`)

- [ ] **Una palabra por concepto** y **un concepto por palabra**; ambiguos no reutilizados.
- [ ] Prohibidos escritos **con alternativa** y con la fecha de la decisión.
- [ ] Nombres nativos de HTML/ARIA usados donde existen; sin choques con atributos nativos (lista de pasos permitidos).
- [ ] Texto como `children` cuando es contenido; `label` solo en campos.
- [ ] **Valores** en la escala corta y por prop (no `default` global).
- [ ] **Misma palabra en código y en Figma**; booleanos que cambian el aspecto como VARIANT.
- [ ] **Tabla de traducción** del proyecto (React / HTML / Figma).
- [ ] Filas dudosas revisadas (`readonly`≠`disabled`, `open`, `xs/xl`).
- [ ] Verificador que mira **props reales** y acepta CRLF; si no hay, «revisado a mano».

## 11. Fuentes y estado de la verificación

| Idea | Fuente | Estado |
|---|---|---|
| Un nombre por concepto, prohibidos como columna clave | Mapa de props de Helix y artículo de agentes de la autora | Leído; de una sola autora |
| Elegir lo que el modelo ya escribe (`onClick`, `isLoading`) | ADR-022 de Helix (35 respuestas sin guía) | **Leído**; muestra pequeña |
| Atributos ARIA y su significado | MDN | **Contrastado** (los 10 existen; `aria-current` frente a `aria-selected`) |
| Atributos HTML nativos y a qué elementos aplican (`readonly`, `disabled`, `open`…) | MDN | **Contrastado** |
| Convención de React (camelCase, `className`, `aria-*` y `data-*` iguales a HTML) | Documentación de React | **Contrastado**; `readOnly` deducido |
| `readonly` no es sinónimo de `disabled` | MDN + mapa de Helix | **Hallazgo propio** apoyado en la norma |
| Comprobación por texto frente a por atributos reales | `verify:props` y `helix/prop-vocabulary` | **Ejecutado** (12 falsos positivos; 3 de 3 detectados) |
| Método de 4 pasos y tablas de sinónimos | Archivo de la comunidad de nombres (CC BY 4.0) | Reexpresado; no dice cuál sinónimo es el elegido |
| Propiedades de Figma = props de código | Archivo real de Helix | **Verificado** en 3 componentes |
| Patrón `is` + estados nativos sin prefijo | Observación sobre Helix | **Inferencia propia** |
| Atributos `data-*` para `website`; verificador para HTML | — | **Inferencia propia, sin probar** |
| Periodo de alias para un sistema publicado | — | **Propuesta propia** |

**Límites:** casi todo viene de **un sistema** y **una autora**; los nombres concretos (`isLoading`, `onClick`…) son una decisión de Helix, no una norma. La traducción para `website` (HTML+CSS, WordPress, Astro) **no se ha probado** en un sitio real.
