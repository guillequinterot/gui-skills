# Crítica visual y QA

## Contenido

1. Método de crítica
2. Severidad
3. QA por tipo
4. Validación final

## 1. Método de crítica

Evaluar desde el objetivo, no desde preferencias personales:

1. resumir qué intenta lograr la pieza;
2. identificar qué funciona y por qué;
3. detectar fallas con evidencia observable;
4. priorizar por impacto;
5. proponer una corrección concreta;
6. indicar cómo verificar la mejora.

Formular hallazgos como: **observación → consecuencia → corrección → prueba**.

Evitar comentarios vagos como “hazlo más moderno”, “le falta impacto” o “no se siente premium” sin traducirlos a variables visuales.

## 2. Severidad

| Nivel | Criterio |
|---|---|
| Bloqueante | Impide comprender, usar, producir o cumplir un requisito esencial |
| Alto | Daña objetivo, accesibilidad, marca o acción principal |
| Medio | Reduce claridad, consistencia o calidad sin impedir la tarea |
| Bajo | Refinamiento óptico o preferencia justificable |

No asignar puntajes numéricos sin una rúbrica definida. No sumar dimensiones incomparables para producir falsa precisión.

## 3. QA por tipo

### Diseño gráfico

- objetivo y mensaje;
- orden de lectura;
- concepto y diferenciación;
- composición, balance y espacio;
- tipografía y copy;
- color e imagen;
- identidad;
- adaptación;
- producción y exportación.

### UI/UX

- tarea y flujo;
- arquitectura y navegación;
- jerarquía y contenido;
- convenciones y feedback;
- prevención/recuperación de errores;
- estados y datos reales;
- teclado, foco y lector de pantalla;
- contraste, color, zoom y responsive;
- rendimiento percibido sin promesas arbitrarias;
- consistencia diseño-código.

### HTML que pasará a Figma

Además de la lista UI/UX: 1920 × Hug, contenido en x = 240, 80 px por sección, múltiplos de 4, Fill/Hug, sin clip innecesario, solo estilos y componentes existentes en el Figma del proyecto. Checklist completo en `conocimiento/03-checklist-qa-listo-para-figma.md`; validación automática con `scripts/validate_figma_ready.py`.

### Híbrido

Ejecutar ambas listas y comprobar que la expresión de marca no degrade la interacción ni que la interfaz diluya el concepto.

### Imagen generada o editada

- identidad de sujeto/producto;
- número y forma de objetos;
- anatomía y manos;
- luz, sombras y reflejos;
- perspectiva y contacto;
- etiquetas/texto;
- artefactos y repetición;
- espacio para diseño;
- resolución y recorte.

## 4. Validación final

Antes de entregar:

- comparar contra brief y elementos intocables;
- inspeccionar a tamaño final y ampliado;
- renderizar/exportar y abrir el archivo final;
- revisar ortografía y datos;
- probar formatos, estados o páginas representativas;
- comprobar enlaces y archivos empaquetados;
- documentar límites reales;
- no declarar cumplimiento legal o accesible total basándose solo en una revisión visual.

