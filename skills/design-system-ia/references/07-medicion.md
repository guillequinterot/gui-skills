# 07 · Medición

> **Estado:** borrador (C-2, 2026-10-27) · **Perfiles:** los tres (cambia cuánto se mide) · **Modos que la usan:** `medir`, `verificar`, `auditar`, `definir`.
> **Fuentes (reexpresadas; ver `CREDITOS.md`):** el sistema **Helix** (MIT, © 2026 Marta Conde; commit `394823a`: la decisión sobre el estado calculado, la de observabilidad de calidad y su guía de evaluaciones), los dos artículos de métricas y el video de «nuevas métricas» de la misma autora. **Inferencia propia** va marcada.
> **Contrastado con fuente primaria el 2026-10-27:** la guía de Anthropic sobre criterios de éxito y métodos de calificación, y las opciones de `git log`. **No contrastado:** las **fórmulas** de las 14 métricas (son de la autora y **no se comprobó que Helix las calcule así**), la calibración del juez de IA, cuántas repeticiones bastan, y todo lo que dependa de ejecutar Storybook, navegadores o modelos (**no se ejecutó**: ni el cálculo del estado, ni las evaluaciones, ni el panel de calidad).
> **Plantillas:** `templates/tabla-de-metricas.md` · `templates/encuesta-corta.md` (opcional).

## 1. Principios

- **Medir para actuar:** una métrica **sin decisión asociada es ruido**; cada una lleva su **acción prevista** (actualizar, renombrar, eliminar, escribir más para agentes, unificar nombres).
- **No hay una puntuación única:** se leen **señales por versión y en tendencia**.
- **Lo que falta no es un cero:** si no hay datos (sin evaluaciones, sin retroalimentación), se informa como **«no disponible»**, nunca como un número engañoso. *(Principio de la decisión de observabilidad de Helix.)*
- **La revisión de una persona no puntúa:** se **registra** y se muestra, **pero no entra en ninguna puntuación** (regla de Helix).
- **Lo que un script comprueba, con script;** la IA no hace lo que un script hace mejor.
- **Tres tipos de medición, declarados:** **script**, **script + IA** (casos límite) y **script + revisión manual obligatoria** (p. ej. accesibilidad).
- **«Existir no es estar al día»**: guarda la **fecha de revisión**, no solo si algo existe.

## 2. Cuánto se mide según el perfil

| Perfil | Qué se mide |
|---|---|
| `website` | **Lista de control corta** (04), literales de color o medida sueltos, frescura de la documentación y **cinco pruebas a mano** con IA en una hoja |
| `app` | **Estado calculado** (sección 3), **5–7 métricas** (sección 4) y pruebas con IA repetidas |
| `sistema compartido` | Todo + **adopción en productos, estabilidad, solicitudes y deuda de ejemplos**, **por versión** |

## 3. Estado de un componente: calculado

**Idea (decisión de Helix, ADR-018):** el estado **no se escribe a mano**; **lo calcula un verificador**. Antes, «estable» había pasado a significar «está en Figma» y nada comprobaba accesibilidad, contraste en oscuro ni teclado; **la primera ejecución automática encontró fallos reales** (contraste en oscuro en 10 componentes marcados como estables y ninguna prueba de teclado).

| Estado | Significado |
|---|---|
| `draft` | Existe y funciona, pero **falla** al menos uno de los 8 criterios |
| `beta` | Pasa los **8 criterios automáticos**; aún no está en Figma o está desactualizado |
| `stable` | `beta` **y** está en Figma **y alineado con el código** |
| `deprecated` | El único que se pone **a mano** |

**Los 8 criterios** (de Helix; reexpresados): 1) **contrato completo** (rol y criterios WCAG rellenos, sin deriva en el índice); 2) **código = contrato** (cada prop del contrato está en los tipos); 3) **tokens resueltos** (sin filas de excepción sin explicar); 4) **historias + accesibilidad** (cada variante, tamaño y estado aparece en alguna historia y un analizador de accesibilidad **no halla violaciones en un navegador real**); 5) **teclado probado** (cada tecla del contrato se ejercita en una prueba y pasa); 6) **contraste AA en claro y oscuro**; 7) **movimiento reducido** respetado; 8) **una evaluación con IA** que importa el componente y comprueba su uso.
**Figma (9) es manual y a petición;** si sigue alineado se comprueba solo con **tres estados**: ✓ sincronizado, ⚠ **deriva** (cambió en el código lo visual desde la última sincronización) y ✗ falta. **Solo ✓ cuenta para `stable`;** un estable cuyo código cambia **baja a beta** hasta que Figma lo alcance. Un cambio que solo toca comportamiento, historias o prosa **no cuenta**. *(Cuando se añadió la deriva, 16 de 19 componentes en Figma estaban desactualizados.)*

**Costes (de Helix):** necesita **Storybook en marcha y un navegador automatizado**, es **demasiado lento** para el *pre-commit*; al adoptarlo, 29 de 30 componentes cayeron a `draft` (faltaban pruebas de teclado y evaluaciones: lagunas reales, no regresión). **No se ejecutó en esta investigación: el cálculo del estado sigue sin verificar.**

**Para esta skill:**
- `app` y `sistema compartido`: usa estos criterios (adáptalos a tu stack: sin Storybook, **páginas de ejemplo** + un analizador de accesibilidad en un navegador).
- `website`: **sin cálculo**; el estado se escribe a mano y se marca **«no verificado»**.
- El estado va en el contrato y lo **escribe un script**, no una persona (ver 01).

## 4. Las 14 métricas

De los dos artículos de la autora; **el nivel «reducido» es inferencia propia**. Cada fila es una proporción (para ver tendencia), no un semáforo. *(Fórmulas de la fuente, **no contrastadas con otra**.)*

**A. Calidad de componente y alineación (parte 1)**

| Métrica | Fórmula (idea) | Tipo | Cuidado |
|---|---|---|---|
| Gobierno | Contratos con las secciones obligatorias completas ÷ componentes | Script | Una plantilla completa no es una regla útil: revisa una muestra |
| Accesibilidad | Ejemplos que lo pasan todo ÷ ejemplos, **contando cada tema por separado**; **teclado aparte** | Script + manual | Fallar solo en oscuro; el analizador no cubre todo |
| Tokens | Valores de token ÷ (token + literales) | Script | Decide antes qué literales se permiten (0, 100 %) |
| Contrato frente a código | Componentes sin diferencias ÷ total | Script | Las props heredadas del HTML: el contrato dice que las acepta |
| Pruebas de interacción | Comportamientos del contrato probados ÷ listados | Script + IA | Pruebas que solo comprueban que «renderiza» |
| Alineación con Figma | Existe **y** coincide ÷ total; **falta** y **desactualizado** por separado | Script | Guarda la fecha de revisión |
| Frescura de la documentación | Documentación más nueva que el último cambio de props ÷ total | Script (historial) | Un refactor interno no cuenta |

**B. IA, adopción y operación (parte 2)**

| Métrica | Idea | Tipo | Cuidado |
|---|---|---|---|
| Fiabilidad del agente | % de respuestas que cumplen **toda** la lista oculta; **varias respuestas por ejercicio**; juez calibrado | Script + IA | No mezclar salidas de antes y después de un renombre |
| Cumplimiento de reglas | % por regla (compilador + linter) y promedio, **mostrando cada regla** | Script | Si compilador y linter discrepan, es un ejemplo de regresión |
| Calidad de diseño | **Juez de IA independiente**, rúbrica por criterios (los críticos marcados), formato fijo, repetido **dos veces**, con **muestra humana** | Script + IA + manual | El juez puede tomar un ejemplo como texto obligatorio: escribe criterios, no frases |
| Deuda de ejemplos | Infracciones de las reglas **en las propias historias y guías** | Script | Los «qué no hacer» se marcan como excepción |
| Estabilidad | Cambios que rompen ÷ cambios; rompientes **con guía de migración** ÷ rompientes | Script | Clasifica con **prefijos explícitos**, no por palabra clave |
| Adopción en productos | Usos del sistema ÷ (usos + equivalentes hechos a mano), **por producto y con la versión usada** | Script | `[CUSTOM]` separa «no lo tiene» de «no lo miró» |
| Solicitudes y respuesta | Mediana de resolución, atraso abierto, edad y volumen por tipo | Script | **Sin registro de lo que llega por chat o reunión, la métrica no existe** |

**La columna «Tipo» es asignación propia,** salvo dos casos que la fuente sí fija: **accesibilidad** (revisión manual obligatoria) y **calidad de diseño** (juez de IA + muestra humana). La fuente solo dice que casi todo se mide con script, que algunas métricas suman IA para casos límite y que la accesibilidad exige revisión manual.

**Perfil reducido (inferencia propia):** `app` = gobierno, accesibilidad (por tema), tokens, contrato frente a código, alineación con Figma (con frescura), fiabilidad del agente y cumplimiento de reglas (**7**). `sistema compartido` añade estabilidad, adopción, solicitudes, deuda de ejemplos y calidad de diseño. `website` = tokens, accesibilidad por lista y frescura.

## 5. Medir el uso, no solo el acierto

Tres capas (video de la autora): **documentación** (visitas), **adopción en código** y **uso por agentes** (llamadas al servidor de consulta). Las visitas ayudan a decidir **en qué formato invertir** (si bajan las humanas y suben las de agentes, menos ilustración y más información densa y legible por máquina).

| Señal | Cómo se calcula | Acción |
|---|---|---|
| **Adopción de componentes** | Componentes distintos usados ÷ componentes totales; **y** el total de usos | Priorizar lo que no se usa |
| **Amplitud y profundidad** | Archivos que lo usan frente a veces que se usa | Distinguir un componente en muchos sitios de uno repetido |
| **Ahorro estimado** | Tiempo que costó crearlo × veces que se usa | Justificar el sistema *(fórmula simple de la fuente)* |
| **Sin uso en 5 meses** | Lista de «necesitan atención» | Eliminar, descartar por una versión nueva o renombrar (nadie lo encuentra) |
| **Props realmente usadas** | Qué propiedades se aplican de verdad | Aplicar accesibilidad a lo más usado primero |
| **Llamadas de consulta** | Lectura frente a **escritura**; **usuarios activos distintos** frente a llamadas (337 llamadas pueden ser una persona) | Saber quién consume y quién contribuye |
| **Herramientas más llamadas** | Si dominan «nombre en Figma» y «nombre en código», probablemente los **nombres no coinciden** | Unificar nombres *(inferencia de la autora, no un dato)* |

- Los datos de adopción salen de un **script que recorre el repositorio** (sin herramientas de terceros) y de **cruzar con el historial** (`git log` admite restringir por ruta, `--since`, `--format` y `-n`; **contrastado**). Los de consulta salen de **registrar cada llamada** (fecha, herramienta, lectura o escritura, contexto): **una línea de registro basta**.
- **Lo que falta en el sistema no es «no adopción»: es una solicitud** (ver 06).
- **Qué se puede escanear en tu caso** (varios clientes, hosting en cPanel, repositorios de terceros) **no está definido**: no se mide lo que no se puede ver.

## 6. Pruebas con IA (evaluaciones)

**Bucle (Helix, basado en una guía de evaluaciones para equipos de producto):** una IA **no da la misma respuesta dos veces**, así que **un acierto no prueba nada**: se mide **con qué frecuencia** acierta.

1. **Comprueba las propias pruebas:** cada respuesta de referencia debe puntuar **100 %** y cada calificador debe **atrapar errores plantados** sin marcar las referencias.
2. **Línea base:** cada prueba **varias veces** (Helix usa 5) → una **tasa de acierto** por prueba.
3. **Análisis de errores:** **lee las respuestas antes de arreglar nada**; anota, agrupa en categorías (sinónimo prohibido, inventado u omitido, valor suelto, importación equivocada, hueco o composición equivocada) y prioriza.
4. **Un solo cambio** (el mapa de props, un contrato, la guía) y **vuelve a medir** como una variante con su nota.
5. **Compara contra la línea base** y **conserva el cambio solo si ayuda sin empeorar otras pruebas.**
6. Añade lo aprendido a un archivo de **lecciones**.

**Banco de ejercicios (4 partes):** enunciado · **lista de comprobación oculta** · **rúbrica oculta** · respuesta de referencia. Las pantallas reales **no nombran componentes, props ni detalles del sistema**: el agente debe orientarse solo. **Guarda cada salida** con **modelo, fecha, contexto y versión del sistema**; **no mezcles salidas de antes y después de un renombre**.

**Calificador:** por patrones (comprueba que ciertos fragmentos de código aparezcan o no); una línea **sin fragmento** no se puede comprobar y se excluye de la puntuación; los **patrones inválidos** ponen la prueba en 0. **Comprobaciones globales** (colores sueltos, estilos en línea, íconos sin pasar por el componente, controles nativos) se informan **aparte** y no cambian la nota. **Todas las respuestas se vuelven a puntuar con los criterios actuales**: arreglar un criterio mal escrito arregla también las antiguas.

**Escalera de contexto:** la misma tarea con **solo** una fuente de conocimiento cada vez (nada, el índice, la guía, el servidor de consulta, el bucle de lint) y con todo junto, **medida por separado** y por rondas con fecha y *commit*. Registra los **tokens** de cada respuesta.

**Versión sin código (`website` y primeras pruebas, de la autora):** una **petición real** → una **lista sí/no definida antes** → **cinco ejecuciones** en una conversación nueva → **leer los fallos** → cambiar **una** cosa → volver a medir. *«Las evaluaciones miden el sistema, no al agente.»*

**Contrastado con la guía de Anthropic (2026-10-27):**
- Criterios **específicos, medibles, alcanzables y relevantes**, y casi siempre **multidimensionales** (fidelidad a la tarea, consistencia, tono, privacidad, uso del contexto, latencia, precio).
- **Calificar con código cuando se pueda;** un modelo para lo matizado; personas con moderación (alto valor, caro y no escala).
- **Un modelo distinto** del que generó la salida para el juez; **anclajes explícitos en la escala**; **salida con formato restringido**; términos definidos.
- **«Volumen antes que calidad»:** muchas preguntas con calificación automática por encima de pocas calificadas a mano; incluye **casos límite**.
- **Esa página no cubre** cómo **calibrar a un juez** contra etiquetas humanas: la calibración de Helix (las referencias deben pasar; las respuestas **mal diseñadas a propósito, que compilan y pasan el linter, deben fallar** en los puntos que su defecto rompe) es **práctica suya, sin contrastar**.

**Costes y permisos:** cada generación es **un turno completo de agente** (en Helix, 32 pruebas × 5 repeticiones = **160 turnos** de un plan existente). **Esta skill no lanza evaluaciones que llamen a un modelo sin permiso expreso** (ver `SKILL.md`).
**No se sabe cuántas repeticiones ni cuántos ejercicios bastan:** las fuentes no lo dicen (Helix usa 5 por costumbre).

## 7. Registro de mejoras (observabilidad)

Un informe **derivado y vinculado a evidencia** (ADR-020 de Helix): un **resumen portátil** con un esquema (cualquier sistema puede aportar el suyo), un **subconjunto semanal** de los últimos 7 días **sin inventar historia**, y **registros de mejora escritos por una persona** (área, **evidencia**, cambio, **métrica esperada**, estado). **No acepta recomendaciones de un modelo automáticamente:** una observación sacada de una conversación se **anonimiza**, la registra una persona y se **revisa** antes de volverse regla, token, contrato, componente o comprobación. *(Leído; **el panel no se ejecutó**: el de Helix falló por saltos de línea de Windows.)*

## 8. Frescura y alineación

- **Frescura de la documentación:** compara la fecha del **último cambio de props** (historial del repositorio, por ruta) con la de la documentación; un refactor interno **no** cuenta.
- **Figma:** separa **«falta»** de **«desactualizado»**, con la **fecha de revisión** (ver 05).
- **Accesibilidad por tema** y **teclado aparte**; el analizador **no lo cubre todo**; lo que no se automatiza se registra como **revisión humana con fecha, quién y con qué tecnología** (ver 01).

## 9. Lista de revisión (la usa `auditar`)

- [ ] Cada métrica tiene **su acción prevista**.
- [ ] **Sin puntuación única**; **por versión** y en tendencia.
- [ ] **«No disponible»** donde no hay datos; sin ceros falsos.
- [ ] **Estado calculado** (o «no verificado» a mano en `website`).
- [ ] Accesibilidad **por tema** y **teclado aparte**; las revisiones humanas **no puntúan**.
- [ ] **Literales permitidos** definidos antes de medir tokens.
- [ ] **Salidas guardadas** con modelo, fecha, contexto y versión; sin mezclar antes y después de un renombre.
- [ ] **Referencias puntúan 100 %**; el calificador **atrapa errores plantados**.
- [ ] Evaluaciones **repetidas**, un cambio cada vez, **leer antes de arreglar**.
- [ ] Juez **distinto** del generador, rúbrica con anclajes y **muestra humana**.
- [ ] **Permiso** antes de lanzar evaluaciones que gastan turnos de un modelo.
- [ ] Adopción solo de **lo que se puede escanear**.

## 10. Fuentes y estado de la verificación

| Idea | Fuente | Estado |
|---|---|---|
| Estado calculado: 8 criterios, tres estados de Figma, costes | ADR-018 de Helix | **Leído**; **no ejecutado** (necesita Storybook y navegador) |
| Informe de observabilidad con evidencia | ADR-020 de Helix | **Leído**; panel **no ejecutado** |
| Bucle de evaluaciones, escalera de contexto, calificador | Guía de evaluaciones de Helix | **Leída**; **no ejecutada** (llaman a un modelo) |
| Las 14 métricas y sus fórmulas | Dos artículos de la autora | Reexpresadas; **no contrastadas ni comprobado que Helix las calcule así** |
| Uso: adopción, amplitud, ahorro, sin uso en 5 meses, llamadas | Video de la autora | Reexpresado; algunas son **inferencia de la autora** |
| Criterios de éxito y métodos de calificación | Guía de Anthropic | **Contrastado** (primeras 100 000 de 153 000 caracteres) |
| Calibrar a un juez | Guía de Helix | **Sin contrastar** (la página de Anthropic no lo cubre) |
| `git log` por ruta, fecha, formato y cantidad | Documentación de git | **Contrastado** |
| Perfil reducido de métricas; permisos para evaluar; qué escanear | — | **Inferencia propia, sin probar** |

**Límites:** casi todo viene de **una autora y un sistema**. **Ninguna evaluación, cálculo de estado ni panel se ha ejecutado**; el cuadro de mando de esta skill **no existe todavía** (los scripts de `scripts/` no calculan estado ni métricas).
