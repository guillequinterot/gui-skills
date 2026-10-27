<!--
PLANTILLA · tabla-de-metricas
Para qué: definir qué se mide, con qué fórmula, de qué tipo, con qué acción prevista y cuándo se revisó, para leer señales por versión y en tendencia (no una puntuación única).
Modo: medir · Perfil: website (3 filas), app (5–7 filas), sistema compartido (todas) · Referencia: references/07-medicion.md (secciones 1, 2, 4, 5 y 8)
Cómo se usa: una copia por proyecto y una columna nueva de valores por cada versión o revisión. Borra las filas que tu perfil no mide.
Reglas: una métrica sin acción prevista es ruido · donde no hay datos escribe «no disponible», NUNCA un cero · la revisión humana se registra pero no puntúa · el tipo de medición se declara (script · script + IA · script + revisión manual) · accesibilidad por tema (claro y oscuro por separado) y teclado aparte · define antes qué literales de token se permiten · no mezcles salidas de IA de antes y después de un renombre · no lances evaluaciones que gasten turnos de un modelo sin permiso expreso. Las fórmulas son las de la fuente, no están contrastadas con otra.
-->

# Métricas · <proyecto>

**Perfil:** <website | app | sistema compartido> · **Revisión:** <AAAA-MM-DD> · **Versión del sistema medida:** <x.y.z> · **Responsable:** <persona>

## Literales permitidos para la métrica de tokens

<Decide antes qué valores sueltos se aceptan (p. ej. 0, 100 %, `auto`).>

## Métricas

| # | Métrica | Fórmula | Tipo | Acción prevista si empeora | Perfil | Valor (<versión>) | Fecha | Cómo se obtuvo |
|---|---|---|---|---|---|---|---|---|
| 1 | Tokens | Valores de token ÷ (token + literales) | Script | Sustituir literales por tokens | website · app · compartido | <% o «no disponible»> | | |
| 2 | Accesibilidad (claro) | Ejemplos que lo pasan todo ÷ ejemplos | Script + manual | Corregir y repetir la revisión humana | website · app · compartido | | | |
| 3 | Accesibilidad (oscuro) | Ídem, tema oscuro | Script + manual | | website · app · compartido | | | |
| 4 | Accesibilidad (teclado) | Teclas del contrato probadas y correctas ÷ listadas | Script + manual | | app · compartido | | | |
| 5 | Frescura de la documentación | Documentación más nueva que el último cambio de props ÷ componentes | Script (historial) | Actualizar la página | website · app · compartido | | | |
| 6 | Gobierno | Contratos con las secciones obligatorias completas ÷ componentes | Script | Completar contratos (revisa una muestra) | app · compartido | | | |
| 7 | Contrato frente a código | Componentes sin diferencias ÷ total | Script | Alinear contrato o código | app · compartido | | | |
| 8 | Alineación con Figma | Existe y coincide ÷ total; «falta» y «desactualizado» por separado | Script | Sincronizar | app · compartido | | | |
| 9 | Fiabilidad del agente | Respuestas que cumplen toda la lista oculta ÷ respuestas (varias por ejercicio) | Script + IA | Escribir más para agentes, unificar nombres | app · compartido | | | |
| 10 | Cumplimiento de reglas | % por regla (compilador + linter), mostrando cada regla | Script | Corregir la regla o la guía | app · compartido | | | |
| 11 | Pruebas de interacción | Comportamientos del contrato probados ÷ listados | Script + IA | Añadir pruebas | compartido | | | |
| 12 | Calidad de diseño | Juez de IA distinto del generador, rúbrica con anclajes, dos pasadas, muestra humana | Script + IA + manual | Revisar criterios | compartido | | | |
| 13 | Deuda de ejemplos | Infracciones de reglas en las propias guías e historias | Script | Corregir o marcar excepción | compartido | | | |
| 14 | Estabilidad | Cambios que rompen ÷ cambios; rompientes con guía de migración ÷ rompientes (clasifica con prefijos explícitos) | Script | Escribir guías de migración | compartido | | | |
| 15 | Adopción en productos | Usos del sistema ÷ (usos + equivalentes hechos a mano), por producto y versión | Script | Priorizar lo que no se usa | compartido | | | |
| 16 | Solicitudes y respuesta | Mediana de resolución, atraso abierto, edad y volumen por tipo | Script | Documentar lo que se pregunta mucho | compartido | | | |

*(Las filas 1–16 incluyen las 14 métricas de la referencia 07, con la accesibilidad desglosada en tres.)*

## Uso, no solo acierto *(app y sistema compartido)*

| Señal | Cómo se calcula | Acción | Valor | Fecha |
|---|---|---|---|---|
| Adopción de componentes | Componentes distintos usados ÷ totales; y total de usos | Priorizar lo que no se usa | | |
| Sin uso en 5 meses | Lista de «necesitan atención» | Eliminar, descartar por versión nueva o renombrar | | |
| Props realmente usadas | Qué propiedades se aplican de verdad | Aplicar accesibilidad a lo más usado primero | | |
| Llamadas de consulta | Lectura frente a escritura; usuarios activos distintos frente a llamadas | Saber quién consume y quién contribuye | | |

*Lo que no se puede escanear (clientes, hosting, repositorios de terceros) no se mide: escríbelo aquí.* → <…>

## Registro de mejoras

| Fecha | Área | Evidencia | Cambio | Métrica esperada | Estado |
|---|---|---|---|---|---|
| <AAAA-MM-DD> | <…> | <enlace o dato> | <…> | <cuál y hacia dónde> | <abierta / medida / descartada> |

## Qué no se midió

<Métricas sin datos y por qué.>
