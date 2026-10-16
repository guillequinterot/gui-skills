# Color y accesibilidad

## Contenido

1. Función del color
2. Construcción de paletas
3. 60-30-10
4. Accesibilidad WCAG
5. Temas y QA

## 1. Función del color

Asignar funciones antes que porcentajes:

- identidad y reconocimiento;
- jerarquía y énfasis;
- estado y feedback;
- agrupación y navegación;
- atmósfera y dirección de arte;
- codificación de datos;
- accesibilidad y legibilidad.

Evaluar asociaciones por cultura, categoría, audiencia y combinación. No asumir significados universales.

## 2. Construcción de paletas

Definir:

- neutrales y superficies;
- texto principal/secundario;
- colores de marca;
- acentos;
- estados semánticos;
- datos/categorías;
- pares de fondo/figura aprobados;
- comportamiento en impresión, pantalla, dark mode y fotografía.

Usar valor y luminancia además de matiz. Comprobar en escala de grises como diagnóstico de jerarquía, no como sustituto de pruebas de color.

## 3. Regla 60-30-10

Tratar 60-30-10 como heurística de distribución visual procedente de otros campos, no como fórmula matemática ni requisito de sistema. Puede ayudar a iniciar una paleta dominante/secundaria/acento. Ignorarla o modificarla cuando:

- la marca es monocromática o maximalista;
- hay visualización de datos;
- el contenido exige varios estados;
- el formato es editorial o fotográfico;
- el sistema necesita múltiples superficies o temas;
- una proporción distinta comunica mejor la prioridad.

No afirmar que Google, Apple, Spotify o LinkedIn usan exactamente esos porcentajes sin documentación directa.

## 4. Accesibilidad WCAG 2.2

Aplicar a contenido web y digital según el nivel acordado:

- Texto normal: mínimo **4.5:1** para AA.
- Texto grande: mínimo **3:1** para AA, usando la definición WCAG.
- Componentes UI e información gráfica necesaria: mínimo **3:1** frente a colores adyacentes cuando aplica SC 1.4.11.
- No usar color como único medio para comunicar información, acción, error o estado.
- Tratar los ratios como umbrales sin redondear.
- Recordar que logotipos tienen excepción en SC 1.4.3, pero considerar variantes accesibles cuando actúan como control.

Consultar la fuente normativa y no trasladar automáticamente WCAG a impresión como obligación legal. En impresión usarla como referencia solo si resulta pertinente y complementar con normativa local.

## 5. Temas y QA

Para light/dark/high-contrast:

- mapear tokens semánticos, no invertir colores mecánicamente;
- conservar jerarquía y estados;
- comprobar elevación, bordes y foco;
- evitar negro/blanco puros como prohibición universal; evaluar comodidad y marca;
- probar imágenes, transparencias y degradados detrás de texto;
- validar estados hover, focus, active, disabled, error y selección.

En gráficos, añadir forma, etiqueta, patrón o posición cuando el color sea insuficiente. Probar simulaciones de deficiencia cromática sin asumir que reemplazan pruebas con usuarios.

