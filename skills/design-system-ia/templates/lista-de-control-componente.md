<!--
PLANTILLA · lista-de-control-componente
Para qué: comprobar a mano, componente a componente, variantes, tokens, contenido, pruebas y accesibilidad antes de dar un componente por listo. Es la base manual del verificador.
Modo: verificar, auditar · Perfil: todos (en `website` usa las secciones 1, 3, 4 y 5; en `app` y `sistema compartido`, todas) · Referencias: references/04-documentacion-y-entrega.md (sección 8) y references/08-gobierno-accesibilidad-estado.md (sección 6)
Cómo se usa: una copia por componente. En cada punto escribe ✓ (cumple), ✗ (no cumple) o n.a. (no aplica) y la EVIDENCIA (qué se miró, con qué). Sin evidencia, el punto queda «no comprobado».
Reglas: claro y oscuro se comprueban por separado · lo deshabilitado está exento del contraste de texto (WCAG 1.4.3), pero documéntalo · una comprobación automática no sustituye la revisión humana con lector de pantalla · esta lista es manual: no escribas «verificado por script» si no hubo script.
-->

# Lista de control · <Componente>

**Fecha:** <AAAA-MM-DD> · **Por:** <persona> · **Versión revisada:** <x.y.z> · **Perfil:** <website | app | sistema compartido>

## 1. Variantes y estados

| Punto | ✓ / ✗ / n.a. | Evidencia |
|---|---|---|
| Tamaños cubiertos | | |
| Tipos o variantes cubiertos | | |
| Estados: normal · hover · activo · foco · deshabilitado | | |
| Retroalimentación (info · error · aviso · éxito), si aplica | | |
| Eje o dirección, si aplica | | |
| Tema claro | | |
| Tema oscuro | | |

## 2. Tokens y nombres

| Punto | ✓ / ✗ / n.a. | Evidencia |
|---|---|---|
| Color (contenido, superficie, borde) con tokens, sin valores sueltos | | |
| Tipografía, espacio, borde, radio, ancho y sombras con tokens | | |
| Nombres de componente, variante y capa según el vocabulario | | |
| Nombres en sincronía con el código | | |
| Valores por defecto iguales en código y en Figma | | |
| Anatomía con los mismos nombres en ambos lados | | |

## 3. Contenido (QA)

| Caso | ✓ / ✗ / n.a. | Evidencia |
|---|---|---|
| Caracteres especiales | | |
| Línea larga sin espacios | | |
| Línea larga con espacios | | |
| Nombre largo | | |
| Estado vacío | | |
| Datos perfectos | | |
| Datos «feos» (incompletos, extremos) | | |

## 4. Pruebas

| Punto | ✓ / ✗ / n.a. | Evidencia |
|---|---|---|
| Revisión por una persona de desarrollo | | |
| Responsive | | |
| Redimensionado extremo | | |
| Comportamiento e interacción | | |
| Varios navegadores | | |

## 5. Accesibilidad (WCAG 2.2)

| Punto | Criterio (nombre oficial) | Nivel | Claro | Oscuro | Evidencia |
|---|---|---|---|---|---|
| El color no es el único indicador | 1.4.1 Use of Color | A | | | |
| Contraste de texto 4,5:1 (3:1 si es grande) | 1.4.3 Contrast (Minimum) | AA | | | |
| Contraste 3:1 de objetos que no son texto | 1.4.11 Non-text Contrast | AA | | | |
| Alternativas de texto para contenido no textual | 1.1.1 Non-text Content | A | | | |
| Sin imágenes de texto | 1.4.5 Images of Text | AA | | | |
| Encabezados y etiquetas descriptivos | 2.4.6 Headings and Labels | AA | | | |
| Operable con teclado | 2.1.1 Keyboard | A | | | |
| Sin trampa de teclado | 2.1.2 No Keyboard Trap | A | | | |
| Orden del foco con sentido; el foco vuelve donde debe al cerrar | 2.4.3 Focus Order | A | | | |
| Foco visible | 2.4.7 Focus Visible | AA | | | |
| El foco no queda oculto del todo por contenido del autor | 2.4.11 Focus Not Obscured (Minimum) | AA | | | |
| Objetivo de al menos 24 × 24 px CSS (con excepciones) | 2.5.8 Target Size (Minimum) | AA | | | |
| Error identificado y descrito en texto, si hay validación | 3.3.1 Error Identification | A | | | |
| Etiquetas o instrucciones donde se pide entrada | 3.3.2 Labels or Instructions | A | | | |
| Nombre, rol y valor accesibles | 4.1.2 Name, Role, Value | A | | | |
| Sin desplazamiento en dos dimensiones a 320 px CSS *(solo componentes de maquetación)* | 1.4.10 Reflow | AA | | | |
| Movimiento: respeta `prefers-reduced-motion` *(criterio de calidad; WCAG lo exige solo en AAA)* | 2.3.3 Animation from Interactions | AAA | | | |
| Probado con simulador de daltonismo | — práctica recomendada, no es un criterio | — | | | |

**Diálogo modal, si aplica:** el foco entra en el diálogo · Tab y Mayús+Tab dan la vuelta dentro · Escape lo cierra · al cerrar, el foco vuelve a quien lo abrió.

**Revisión humana con tecnología de apoyo** *(no se puntúa; se registra)*

| Fecha | Persona | Tecnología usada | Qué se observó (¿tiene sentido lo que se anuncia?) |
|---|---|---|---|
| <AAAA-MM-DD> | <…> | <lector de pantalla y navegador> | <…> |

## 6. Otros

| Punto | ✓ / ✗ / n.a. | Evidencia |
|---|---|---|
| Capas con nombre según las guías | | |
| Descripción del componente | | |
| Soporte de temas | | |
| Internacionalización | | |
| Control de versiones | | |

## Resultado

**Puntos ✓:** <n> · **✗:** <n> · **Sin evidencia (no comprobado):** <n>
**Pendiente antes de dar el componente por listo:** <…>
**Lo que no se comprobó y por qué:** <…>
