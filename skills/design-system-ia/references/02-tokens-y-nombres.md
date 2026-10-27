# 02 · Tokens y nombres

> **Estado:** borrador (C-2, 2026-10-27) · **Perfiles:** los tres (cambia cuántas capas) · **Modos que la usan:** `definir`, `construir`, `auditar`, `verificar`, `documentar`.
> **Fuentes (reexpresadas; ver `CREDITOS.md`):** el sistema **Helix** (MIT, © 2026 Marta Conde; commit `394823a`: estrategia de tokens, gramática de nombres, resolver, guía del paquete y archivo de Figma), los artículos, glosarios, videos y webinars de la misma autora, y las normas citadas. **Inferencia propia** va marcada.
> **Contrastado con fuente primaria el 2026-10-27:** formato y resolver de tokens (DTCG 2025.10), fórmula de contraste y exenciones (WCAG 2.2), y propiedades de variables de Figma (API de plugins). **No contrastado:** la lista de **tipos simples** del formato DTCG (solo se verificaron los compuestos y la forma de color y dimensión), la documentación pública de Figma (no detalla alcances ni «ocultar al publicar»; se usó la API) y los tokens de HTML/WordPress/Astro (sin caso propio).
> **Plantillas y scripts:** `templates/vocabulario.md` (tabla de traducción) · `templates/tabla-antes-despues.md` · `scripts/contraste.py`.

## 1. Qué es un token

Un **token** es una **decisión de diseño con nombre** que funciona igual en cualquier plataforma y está **sincronizada entre diseño y desarrollo**. Si solo vive en una plataforma (p. ej. variables de Figma sin conexión con el código), son **variables**, no tokens. *(Fuente: webinar de tokens de la autora; la definición no está en la norma.)*

Para qué sirve: consistencia (el mismo color en hover, siempre), cambios en un solo punto, otra marca o un tema oscuro cambiando valores y no componentes, y un **lenguaje común** para buscarlos.

## 2. Capas: cuántas según el perfil

| Capa | Qué contiene | Ejemplo | Quién la usa |
|---|---|---|---|
| **Primitivo** | Valores crudos con **nombre fijo** (paleta, escala) | `color.blue.600` | Solo otras capas; **nunca el componente** |
| **Semántico** | La **decisión**: para qué sirve | `color.fill.primary` | Los componentes |
| **Componente** | Alias propios de un componente | `button.fill.primary` | Solo ese componente |

| Perfil | Capas | Nota |
|---|---|---|
| `website` | **2** (primitivo + semántico) como variables CSS | **Sin tokens de componente**: se entrega el componente final con sus estados |
| `app` | **3**; la de componente solo si hace falta | Decisión #5: opcional, con necesidad y capacidad de mantenerla |
| `sistema compartido` | 3 + temas o modos por marca | Duplicar y cambiar valores da otra marca |

Reglas de las capas (varias fuentes coinciden):
- **Un primitivo no cambia de valor.** Si necesitas otro verde, creas `color.green.500`; no reutilizas el nombre de otro color. El nombre fijo es lo que lo hace estable.
- **El componente solo mira semánticos.** Un componente que salta la capa semántica entra en una **tabla de excepciones** con su motivo (en Helix se genera con un script; es la única forma de saber cuántos se saltan la regla).
- **No toda cosa necesita las tres capas.** Una decisión sin capa semántica no es un error si no la necesita. **Crea solo lo que se va a usar.**
- **Los primitivos no se exponen.** En Figma, se ocultan de los selectores (ver 10); en CSS, el componente no los referencia.

## 3. Formato

| Perfil | Formato recomendado |
|---|---|
| `website` | **Variables CSS** (`--nombre`) en `:root`, con los valores oscuros en `[data-theme="dark"]` y, si se quiere seguir al sistema, en `@media (prefers-color-scheme: dark)` |
| `app`, `sistema compartido` | **JSON en formato DTCG 2025.10** y compilarlo a CSS (y a constantes de JS si hace falta) |

**Formato DTCG 2025.10** (contrastado con la especificación):
- Estado: **informe final del grupo comunitario (28-oct-2025)**; **no es un estándar del W3C**. Dilo así.
- Propiedades: `$value` (obligatoria), `$type`, `$description`, `$extensions` (y `$deprecated`).
- Referencias entre tokens: `{grupo.token}` (y `$ref` con puntero JSON).
- Color: objeto con `colorSpace` y `components` (opcionales `alpha` y `hex`). Dimensión: `{ "value", "unit" }` con unidad **`px` o `rem`** solamente.
- Tipos compuestos: sombra, borde, transición, estilo de trazo, degradado y tipografía.
- **Nombres:** no empiezan por `$` y no contienen `{`, `}` ni `.` (distinguen mayúsculas).
- **Resolver 2025.10:** `sets` (conjuntos de tokens), `modifiers` con `contexts` (p. ej. `light`/`dark`) y `resolutionOrder` (el último gana). Helix lo usa con un modificador de **tema** y otro de **ventana** (móvil).
- Una **sola función convierte** los valores a CSS (y viceversa) en Helix: ningún otro script los interpreta. Haz lo mismo en tu verificador propio.

## 4. La fórmula de nombre

**Cinco segmentos** (artículo de la autora, 2026): `categoría · elemento · rol · modificador · estado`. Los dos últimos son **opcionales**; no rellenes un segmento que no aporta y **omite `default`**.

| Segmento | Qué dice | Ejemplo |
|---|---|---|
| Categoría | Qué familia de decisión | `color` |
| Elemento | Dónde se aplica | `fill`, `text`, `icon`, `border` |
| Rol | Para qué sirve | `primary`, `danger`, `neutral` |
| Modificador | Un matiz junto al rol (opcional) | `light`, `dark` |
| Estado | Interacción (opcional) | `hover`, `press` |

**Reglas (varias fuentes):**
1. **El nombre dice la decisión, no el valor.** `…-hover`, no `…-gris`: si el valor cambia, el nombre sigue sirviendo.
2. **Claridad antes que brevedad;** estructura pequeña (pocos segmentos); de lo **genérico a lo específico**.
3. **El mismo nombre en todas las plataformas** (ver 5): si no, la sincronización falla.
4. **Valida el vocabulario con diseño y desarrollo** (una empresa decía «fondo», otra «superficie»): lo que a ti te parece estándar a otro le es ajeno.
5. **No crees segmentos ni tokens por adelantado.**
6. **Un segmento existe solo si comunica una diferencia real.**

**Vocabulario cerrado (ejemplo de Helix, no regla universal):** `{rol}[-interactive[-modificador]-estado][-modificador]` con roles, modificadores y estados enumerados, y **palabras prohibidas con su sustituto** (`rest`→`default`, `active`→`press`, `subtle`→`-light`, `strong`→`-dark`, `brand`→`primary`). Mapa (inferencia propia): `color.fill.primary-interactive-light-default` = categoría `color` · elemento `fill` · rol `primary` · marca `interactive` · modificador `light` · estado `default`.
La **fórmula de 4 cajas** del webinar de 2024 (elemento · tono · énfasis · estado) es el antecedente: úsala solo como caso simple de un `website`.

**Esquema frente a verificador (la misma lección que en el contrato):** el **esquema** de Helix comprueba la **estructura** (que cada palabra esté en su sitio y no haya palabras prohibidas); **no puede** comprobar si `-light` es de verdad el más claro entre sus hermanos: eso lo hace **otro script** que compara valores resueltos. Un nombre bien formado no es un nombre correcto.

## 5. Traducción entre plataformas

La misma decisión se escribe distinto en cada destino. **Mantén una tabla de traducción en el proyecto.** Ejemplo **verificado** en Helix (color):

| Destino | Escritura | Reglas observadas |
|---|---|---|
| JSON (DTCG) | `semantic.color.fill.primary-interactive-default` | Puntos; capa como primer segmento |
| CSS | `--helix-color-fill-primary-interactive-default` | Prefijo del sistema; guiones; **sin la capa**; con la categoría `color` |
| Figma | `fill/primary/interactive/default` en la colección `Theme` | Barras que crean grupos; **sin prefijo y sin la categoría**; los guiones del JSON pasan a barras |

Otros tipos (espaciado, radio, tipografía) siguen un patrón parecido en Figma (`spacing/component/m`, `radius/m`), pero **su equivalente en CSS no se verificó**. **Para HTML+CSS, WordPress y Astro la regla de traducción es inferencia propia: se fija en `caso-ds-01`.**

## 6. Glosario de tokens (antes de escalar)

Un glosario evita que cada persona nombre a su manera. Mínimo (6 campos): **concepto · segmento que ocupa · definición · escala · sinónimos a comparar · ejemplos**. Ampliado (12): + rol, familia, propiedad, origen y fuentes, estado de revisión y registro de cambios (según el glosario de la autora).

- **Los sinónimos son lo valioso:** *warning / alert / caution / attention*; sin ellos no sabes si dos sistemas hablan de lo mismo. Anota también los **términos rechazados**.
- **Taller por categoría:** elige una (color), pinta los componentes con primitivos, crea semánticos **por repetición**, escala y valida con diseño y desarrollo.
- **Prueba de calidad:** ¿alguien deduce el uso sin ver el valor?
- **Un conflicto típico:** `medium` como tamaño y como peso; `neutral` blanco y `neutral` gris (se distinguen con `default`/`light`, bajo/alto).
- **Descripción:** cada token **semántico** lleva una línea de **para qué sirve** (no repite el valor). En Helix es **obligatoria en semánticos y prohibida en primitivos y de componente**, y es la **fuente única** del texto que se copia a la descripción de la variable de Figma (`description` es una propiedad real de la variable; ver 10).
- **Un asistente de IA** puede sugerir nombres a partir del glosario, pero **no valida** (ver 11).

## 7. Tipos de token y compuestos

**Lista de comprobación de tipos** (webinar de la autora; no es una lista normativa): color · tipografía · radio · tamaño · borde · movimiento · degradado · sombra · compuesto · tiempo · recursos (íconos e ilustraciones) · espaciado · z-index.

**Compuestos = una unidad.**
- **Tipografía** (en DTCG es un compuesto; Helix exige sus **5** propiedades: familia, tamaño, peso, espaciado de letras e interlineado). En Figma, **una variable no compone** otras: se **enlazan** variables a un **estilo de texto** (verificado en el archivo de Helix: el estilo `Caption / Semibold` usa variables de tamaño, interlineado, peso y familia; *que Figma siga sin variable compuesta en 2026 no se verificó*).
- **Sombra** (color, desplazamiento, desenfoque, expansión) y otras: igual, **un token**, no varias decisiones sueltas.
- **Interlineado:** en Helix es una **proporción sin unidad** en el JSON y un **valor en píxeles** en Figma (una variable enlazada no admite proporción). Es un caso donde el mismo token toma **distinta forma** por plataforma: documéntalo.

**Escala desde una base** (webinar de tipografía): una variable base (p. ej. 16 px) y las demás por **fórmula** (÷1,3, ×1,1); al cambiar la base cambia la escala. En CSS, con `calc()`/`clamp()`; en Figma, mediante un plugin *(herramienta ajena: se rescata la idea, no la dependencia)*.

## 8. Temas (claro y oscuro) y ventanas

- **El oscuro es un modificador, no una copia.** En Helix, un archivo aparte con **61** tokens anulados produce **254** variables CSS distintas, porque **los alias se encadenan** (646 de 646 se emiten como `var()` de otra variable). *Verificado (prueba local, `394823a`).*
- **Un token de componente no tiene entrada oscura propia**: si alias un semántico, **sigue su valor oscuro solo**. Si necesita otro, apunta a **otro semántico**.
- **Los alias se resuelven después de aplicar el tema.**
- **Ventana:** en Helix, bajo el punto de corte de tablet, los tamaños de 18 px o más se sustituyen por los de `fontSize.mobile.*`; tablet comparte el valor de escritorio.
- `website`: `[data-theme="dark"]` y/o `prefers-color-scheme`; **no copies valores**: sobrescribe solo las variables que cambian.

## 9. Contraste

Reglas (WCAG 2.2, contrastado):
- **1.4.3 Contrast (Minimum), AA:** 4,5:1 para texto normal; 3:1 para texto grande. **1.4.11 Non-text Contrast, AA:** 3:1 para iconos y bordes que transmiten significado.
- **Fórmula:** `(L1 + 0,05) / (L2 + 0,05)`, con `L1` la luminancia relativa del color **más claro**; `L = 0,2126·R + 0,7152·G + 0,0722·B` tras linealizar cada canal (si ≤ 0,04045, `÷12,92`; si no, `((c + 0,055)/1,055)^2,4`). **No se redondea:** 4,499 **no** cumple 4,5.
- **Lo inactivo está exento:** los componentes no disponibles para la interacción (un control deshabilitado) **no deben cumplir** los requisitos de contraste. Documéntalo, como hace Helix.

Cómo aplicarlo a tokens:
1. **Se comprueba el par** (texto o icono sobre **su** relleno), no el token suelto: dos roles en el mismo escalón nominal pueden tener luminancias distintas.
2. **Claro y oscuro por separado:** un par que cumple en un tema no garantiza el otro.
3. En Helix `verify:tokens` revisa **nombres, no contraste**; el contraste lo revisan otros comprobadores y una revisión manual al añadir un color. **Verificador propio de contraste:** `scripts/contraste.py` (fórmula de WCAG sin redondear antes de comparar, claro y oscuro por separado, lo deshabilitado exento y documentado); recibe los pares en un JSON y **no lee tus archivos de tokens por su cuenta**. Si no se ejecutó, la skill **dice que lo calculó a mano**.

## 10. Lo que concierne a Figma (detalle en la 05)

- **Colecciones y modos:** en Helix, `Theme` (73, claro/oscuro, todas alias), `Primitives` (115), `Semantic` (49) y `Responsive` (14; escritorio/tablet/móvil). **No se espeja todo:** 251 variables frente a **803** tokens del código; **la capa de componente no existe como variables**.
- **Alcance (`scopes`):** controla en qué selectores aparece la variable. El valor por defecto (`ALL_SCOPES`) casi nunca es el deseado; fíjalo siempre. En Helix, los **primitivos de color** tienen alcance **«ninguno»** y los de `Theme` el de rellenos, trazos y efectos.
- **Ocultar al publicar (`hiddenFromPublishing`):** propiedad **distinta** del alcance, a nivel de variable **y** de colección (lo oculta todo si la colección lo está). *El texto de la propia API sobre cuál valor permite publicar es ambiguo; no se resolvió.*
- **Descripción:** `description` es una propiedad de la variable: copia ahí la misma frase que el `$description` del token.
- **Renombrar:** cambia el nombre **en su sitio**, nunca crees una segunda variable (deja huérfanas las instancias enlazadas).

## 11. La IA propone, otro decide

- **No delegues sin verificación** la auditoría ni la generación de tokens: la IA **inventa** y limpiar cuesta más que auditar. *(Lo afirman tres fuentes, todas de la misma autora.)*
- Útil: dar a la IA el **glosario, las estructuras y las restricciones** (qué no se puede renombrar) y pedirle **sugerencias**; **extraer tokens de una imagen** de componentes; **buscar por intención** (en Helix, `helix tokens "danger background"` devuelve la variable, su valor claro y oscuro y para qué sirve; probado).
- **Valida un esquema, un script o una persona.** Y **las respuestas de la IA mejoran con datos reales del producto y sus restricciones**.

## 12. Añadir un token (procedimiento por perfil)

| Paso | `website` | `app` / `sistema compartido` |
|---|---|---|
| 1. Nombre contra el vocabulario | Sí | Sí (script de nombres) |
| 2. Descripción de una línea (semánticos) | Sí | Sí; misma frase en Figma |
| 3. Valor (y valor oscuro si cambia) | Variable CSS | `$value` + modificador de tema |
| 4. Compilar | — | Build a CSS |
| 5. Contraste del par en ambos temas | A mano con la fórmula | Script |
| 6. Figma: variable, alcance, descripción | Si hay archivo | Sí |
| 7. Documentación lo muestra | Página de tokens | Generada desde la fuente (sin lista a mano) |
| 8. Excepciones | — | Actualizar la tabla de excepciones |

**Decisión de quién elige el valor:** en `app` y `sistema compartido`, **la IA no elige tokens ni valores nuevos: presenta 2–3 opciones** y espera al dueño (regla del `SKILL.md`).

## 13. Cifras: siempre con capa y fecha

Ejemplo (Helix, `394823a`): **803** tokens DTCG (148 primitivos, 168 semánticos, 487 de componente), **879** propiedades CSS tras compilar, **251** variables de Figma, **61** tokens oscuros que cambian **254** variables. Cualquier cifra sin capa y sin fecha se descarta.

## 14. Lista de revisión (la usa `auditar`)

- [ ] Perfil y número de **capas** coherentes (website: 2; sin tokens de componente).
- [ ] Componentes **sin** primitivos directos (o con excepción documentada).
- [ ] Nombres **sin valor** dentro y con vocabulario cerrado; sin palabras prohibidas.
- [ ] **Tabla de traducción** entre plataformas.
- [ ] Glosario con **sinónimos** y términos rechazados.
- [ ] Cada semántico con **descripción** (y la misma en Figma).
- [ ] Compuestos tratados como **unidad**.
- [ ] Oscuro como **modificador**, no copia; sin entradas oscuras en tokens de componente.
- [ ] **Contraste por par y por tema**, sin redondear; deshabilitado documentado.
- [ ] Figma: **alcance** fijado y primitivos ocultos de los selectores; renombres en sitio.
- [ ] Cifras con capa y fecha.

## 15. Fuentes y estado de la verificación

| Idea | Fuente | Estado |
|---|---|---|
| 3 capas, componente solo semánticos, primitivo de nombre fijo | Estrategia de tokens y guía de Helix; webinar de tokens | Leído; coincide en varias fuentes |
| Formato, resolver, nombres de token | Especificación DTCG 2025.10 | **Contrastado** (formato y compuestos; **tipos simples sin contrastar**) |
| Fórmula de 5 segmentos | Artículo de nombres de la autora (2026) | Reexpresada; sin otra fuente |
| Gramática cerrada con palabras prohibidas | Esquema y script de nombres de Helix | **Ejecutado** (`verify:tokens` pasa); estilo de un sistema |
| Esquema ≠ verificador de nombres | Esquema de Helix (su propia descripción) | **Leído** |
| Traducción JSON ↔ CSS ↔ Figma (color) | Helix (código y archivo de Figma) | **Verificada**; el resto, inferido |
| Oscuro como modificador: 61 → 254 | Prueba local de Helix | **Verificado** (build) |
| Contraste, exención de lo inactivo, no redondear | WCAG 2.2 y su guía | **Contrastado** |
| Alcance, ocultar al publicar, descripción | API de plugins de Figma + archivo real | **Contrastado** (la API); la ayuda pública no lo detalla |
| Tipografía compuesta enlazada a un estilo | Archivo de Helix y webinar de tipografía | **Observado en el archivo**; vigencia en 2026 sin verificar |
| Escala desde una base | Webinar de tipografía | Idea; plugin ajeno |
| Glosario de 6 y 12 campos | Artículo y glosario de la autora | Reexpresado |
| 13 tipos de token | Webinar de tokens | Lista de la autora, no normativa |
| Regla de traducción para HTML/WordPress/Astro | — | **Inferencia propia, sin probar** |

**Límites:** casi todo viene de una autora y de un sistema (Helix). La parte de `website` (variables CSS, dos capas, sin tokens de componente) sale de **tu decisión** y de la investigación, **no se probó** con un sitio real (`caso-ds-01`).
