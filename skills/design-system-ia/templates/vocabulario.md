<!--
PLANTILLA · vocabulario
Para qué: fijar UN nombre por concepto (props, valores, componentes, eventos) y los sinónimos prohibidos, con la misma palabra en código y en Figma. La columna de prohibidos es la que un verificador puede aplicar.
Modo: definir, contrato, auditar, verificar · Perfil: todos (en `website` se aplica a atributos `data-*`, `aria-*` y clases) · Referencia: references/03-vocabulario-de-props.md
Cómo se usa: una copia por proyecto. Empieza por lo que YA se usa (inventario de nombres en código y Figma), elige uno por concepto con el orden de la sección 1 y pasa los demás a «Prohibidos». Anota los rechazados con su motivo.
Reglas: la IA no inventa nombres: presenta 2–3 opciones con su efecto y espera; decide la persona responsable. Cada fila lleva fecha y porqué. El vocabulario es por prop, no global. Los ejemplos de abajo son de relleno: bórralos.
`scripts/vocabulario_check.py` aplica esta tabla a los atributos reales de tus archivos. Si no se ejecutó, no se escribe «vocabulario verificado»: se escribe «revisado a mano contra esta tabla».
-->

# Vocabulario · <proyecto>

**Fecha:** <AAAA-MM-DD> · **Decide:** <persona> · **Stack:** <React / HTML+CSS / Astro / WordPress / otro> · **Última revisión:** <AAAA-MM-DD>

## 1. Cómo se elige un nombre (en este orden)

1. **El nombre nativo**, si existe y significa lo mismo (HTML o ARIA: `disabled`, `required`, `checked`, `aria-expanded`…).
2. **Lo que los modelos ya escriben** (solo como desempate, nunca como prueba).
3. **Un concepto, un nombre; un nombre, un concepto.** Los ambiguos (`type`, `state`, `variant`, `layout`, `orientation`, `direction`, `mode`, `content`, `value`) no se reutilizan con otro sentido.
4. **El texto visible es `children` (o su equivalente), no `label`**, cuando el componente lo recibe como contenido. `label` queda para campos de formulario.
5. **Valídalo con diseño y desarrollo.**

## 2. Tabla del vocabulario

| Canónico | Prohibidos (→ alternativa) | Dónde aplica | Equivalencia nativa | Figma | Decisión (quién · cuándo · porqué) |
|---|---|---|---|---|---|
| `<nombre>` | `<sinónimo>` → `<nombre>`; `<sinónimo>` → `<nombre>` | <componentes o «todos»> | <atributo HTML/ARIA o —> | <tipo de propiedad y nombre> | <persona · AAAA-MM-DD · motivo> |
| *`disabled` (ejemplo)* | *`isDisabled`* | *controles de formulario* | *atributo `disabled`* | *VARIANT `disabled`* | *<…>* |
| *`required` (ejemplo)* | *`isRequired`* | *campos* | *`required` / `aria-required`* | *BOOLEAN `required`* | *<…>* |

## 3. Valores por prop

El vocabulario de valores es **por prop**: un valor prohibido en una prop puede ser válido en otra (p. ej. `default` en el eje `state` de Figma).

| Prop | Escala completa | Subconjunto que admite cada componente | Valores prohibidos (→ alternativa) |
|---|---|---|---|
| `<prop>` | `<s · m · l …>` | `<componente: s, m, l>` | `<small → s; medium → m>` |

## 4. Tabla de traducción por plataforma

| Concepto | React | HTML / ARIA nativo | Atributo propio en HTML+CSS *(si no hay nativo)* | Propiedad en Figma |
|---|---|---|---|---|
| <concepto> | `<prop>` | <atributo> | `data-<nombre>="<valor>"` | <VARIANT / BOOLEAN / TEXT / INSTANCE_SWAP> `<nombre>` |

*Regla de Figma:* un booleano que cambia el aspecto es una VARIANT `false/true`; uno que solo muestra u oculta una parte es BOOLEAN. Los manejadores de eventos no tienen propiedad en Figma. Detalle en la referencia 05.

## 5. Pasos permitidos (nombres que son atributos nativos)

Nombres que **no** se marcan como error porque el componente los pasa a un elemento HTML nativo.

| Nombre | Componentes donde se permite | Motivo |
|---|---|---|
| `<type / name / title / readonly / open …>` | <…> | <atributo nativo de `<elemento>`> |

## 6. Rechazados

| Nombre rechazado | Para el concepto | Motivo | Fecha |
|---|---|---|---|
| `<nombre>` | `<canónico>` | <por qué no> | <AAAA-MM-DD> |

## 7. Nombres de componentes (método de 4 pasos)

Una fila por componente nuevo o en disputa.

| Componente | 1. Identificar (componente o base · objeto · propiedad · valor) | 2. Estructura (qué lleva el nombre · orden) | 3. Gramática (palabra · número · mayúsculas · unión) | 4. Orden (alfabético / secuencial / jerárquico) |
|---|---|---|---|---|
| `<NombreEnPascalCase>` | <…> | <…> | <…> | <…> |

## 8. Conflictos y ambiguos detectados

| Palabra | Conceptos que la usan | Propuesta (2–3 opciones) | Decisión |
|---|---|---|---|
| <p. ej. un mismo nombre para tamaño y peso> | | | |

## 9. Estado de la revisión

☐ **Revisado a mano** contra esta tabla · **Fecha:** <AAAA-MM-DD> · **Por:** <persona>
☐ **Verificado** con <herramienta> *(solo cuando exista; debe mirar props reales y aceptar saltos de línea de Windows)*
**Filas dudosas revisadas:** ☐ `readonly` no es sinónimo de `disabled` · ☐ `open` frente a atributos nativos · ☐ escala frente a subconjunto · ☐ `default` por prop
**Lo que no se comprobó:** <…>
