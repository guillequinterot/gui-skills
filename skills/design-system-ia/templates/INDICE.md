# Plantillas de `design-system-ia`

> **Estado:** borrador (2026-10-27). Ninguna plantilla se ha rellenado todavía con un caso real (prueba: `caso-ds-01`).
> Cada plantilla empieza con un comentario que dice para qué sirve, qué modo y perfil, qué referencia la explica y qué reglas sigue. **Bórralo al usarla.** Las plantillas son la copia completa; la explicación de cada idea y su fuente están en `references/`.

## Qué plantilla usar

| Plantilla | Modo | Perfil | Referencia | Entrega |
|---|---|---|---|---|
| [`plan-de-arranque.md`](plan-de-arranque.md) | `definir`, `auditar` | Todos | 09 | Decisiones de arranque, MVP, fases y señales de salto |
| [`decision.md`](decision.md) | `definir`, `documentar` | Todos | 08 | Una decisión con opciones, recomendación y consecuencias |
| [`contrato-minimo.md`](contrato-minimo.md) | `contrato` | `website` | 01 | Contrato de 5 campos + estados |
| [`contrato-completo.json`](contrato-completo.json) | `contrato` | `app`, `sistema compartido` | 01 | Contrato completo (esquema en `scripts/`) |
| [`vocabulario.md`](vocabulario.md) | `definir`, `contrato`, `auditar` | Todos | 03 | Un nombre por concepto y prohibidos |
| [`tabla-antes-despues.md`](tabla-antes-despues.md) | `construir`, `documentar` | `app`, `sistema compartido` | 09 (§7), 02, 03 | Sincronización o migración de nombres |
| [`pagina-de-componente.md`](pagina-de-componente.md) | `documentar` | Todos | 04 | Página de un componente |
| [`lista-de-control-componente.md`](lista-de-control-componente.md) | `verificar` | Todos | 04, 08 | Control manual con evidencia |
| [`nota-para-agentes.md`](nota-para-agentes.md) | `documentar` | Todos | 06 | `AGENTS.md` |
| [`indice-llms.txt`](indice-llms.txt) | `documentar` | `website` (opcional en los demás) | 06 | `llms.txt` (propuesta, no estándar) |
| [`solicitud.md`](solicitud.md) | `documentar` | `app`, `sistema compartido` | 06 (§10), 09 | Lo que falta en el sistema |
| [`ficha-de-auditoria.md`](ficha-de-auditoria.md) | `auditar` | Todos | 01–09 | Informe con hallazgos y lo no comprobado |
| [`tabla-de-metricas.md`](tabla-de-metricas.md) | `medir` | Todos (filas por perfil) | 07 | Métricas con fórmula, tipo y acción |
| [`biblioteca-manifiesto.json`](biblioteca-manifiesto.json) | `documentar` | Todos | 04 (§13) | **Entrega estándar:** manifiesto de la biblioteca de módulos → `python -I scripts/generar_biblioteca.py manifiesto.json salida/` (carpeta con página, logo del cliente y capa para IA) |
| [`patron.md`](patron.md) *(opcional)* | `documentar` | `app`, `sistema compartido` | 04, 06 | Patrón de composición que ya se repite |
| [`tarea.md`](tarea.md) *(opcional)* | `documentar`, `definir` | `equipo` | 09 (§11) | Plantillas de tareas por tipo de trabajo |
| [`encuesta-corta.md`](encuesta-corta.md) *(opcional)* | `medir` | `app`, `sistema compartido` | 09 (§10), 07 | 3 preguntas de satisfacción |

## Mínimo por perfil

- **`website` + `individual`:** `plan-de-arranque` (secciones 1, 2, 4, 5, 8, 9 y 11) → `contrato-minimo` por componente → `vocabulario` → `pagina-de-componente` + `lista-de-control-componente` → `nota-para-agentes` (+ `indice-llms.txt` si se publica) → `ficha-de-auditoria`.
- **`app`:** lo anterior con `contrato-completo.json`, más `decision`, `solicitud`, `tabla-de-metricas` y `tabla-antes-despues`.
- **`sistema compartido`:** todo, con `equipo` si hay más de una persona (más `tarea` y `patron` cuando hagan falta).

## Guía de campos de `contrato-completo.json`

El JSON no admite comentarios; esta tabla es su guía (más detalle en `references/01-contrato.md`, sección 4).

| Campo | Quién lo escribe | Qué poner |
|---|---|---|
| `$schema` | Persona | Ruta al esquema del contrato (`scripts/contrato.schema.json`) |
| `name` | Persona | PascalCase |
| `version` | Persona | `x.y.z` |
| `status` | **Script** | `draft` · `beta` · `stable` · `deprecated`; no se edita a mano (`deprecated` es la excepción manual) |
| `kind` | Persona | `component` o `base` *(propuesta propia, sin probar)* |
| `purpose` | Persona | Una frase desde quien lo usa |
| `import` | **Script** | Instrucción de importación generada del índice |
| `origin` | Persona | Sistema propio, librería abierta o tercero; repositorio; archivo y nombre en Figma; regla «usa el nuestro» *(propuesta propia, sin probar)* |
| `neverUseFor` | Persona | Antipatrones con la alternativa |
| `rationale` | Persona | La decisión y su motivo |
| `governance` | Persona | `mayExtendLocally` y `mustEscalateToDS` |
| `states` | Persona | `intrinsic` (los gestiona el navegador) y `authored` (nombre, descripción, ARIA) |
| `anatomy` | Persona | Partes con el mismo nombre en código y Figma; `optional` en las opcionales |
| `props` | Persona | Nombre canónico (vocabulario), tipo, defecto igual en código y Figma, `required`, descripción |
| `tokenPolicy` | Persona | `allowed` y `forbidden`: prefijos de token |
| `a11y` | Mixto | `role`, `keyboardNav`, `wcag` (nombre oficial y nivel), `announces`, `humanReview` (persona); `applied` y `results` (**script**) |
| `sizing` | Persona | Altura y ancho |
| `figma` | Persona | Propiedades solo-Figma, excepciones aprobadas y estados del eje `state` *(forma propia, distinta a la de Helix)* |

Los valores que dicen `GENERADO` los escribe un script: no los edites a mano. El validador de contratos es `scripts/validar_contrato.py`, con el esquema `scripts/contrato.schema.json`.
