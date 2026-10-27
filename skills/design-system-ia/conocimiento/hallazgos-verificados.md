# Hallazgos verificados

> Estado: 2026-10-27. Cada fila dice **cómo se comprobó**. «Observado» = visto en un archivo o ejecución concretos; no implica que sea general. La explicación completa está en la referencia indicada.

| # | Hallazgo | Cómo se comprobó | Referencia |
|---|---|---|---|
| 1 | El verificador de contratos de Helix **no valida el esquema completo** (solo campos obligatorios, estado, sinónimos prohibidos, anatomía en kebab-case y tokens duplicados) y está en modo solo informe. Con un validador de esquema, 2 de los 33 contratos incumplen la declaración del esquema (seis campos de raíz no declarados y un estado escrito como texto). | Lectura del script y ejecución de `scripts/validar_contrato.py` sobre los 33 contratos | 01 §13 |
| 2 | Un script que busca nombres prohibidos **como texto** da falsos positivos (12 en la prueba); la regla que mira atributos reales atrapó 3 de 3 errores y dijo la alternativa. | Ejecución local de ambos en Helix | 03 §6 |
| 3 | `readonly` figura como sinónimo prohibido de `disabled` en un mapa de Helix, pero en HTML y ARIA son atributos distintos. | Contraste con MDN | 03 §4 |
| 4 | El valor por defecto de `size` difería entre el contrato (`m`) y Figma (`s`); el contrato y la descripción decían 68 variantes y el conjunto real tenía 144. | Lectura del archivo de Figma por MCP (solo lectura) | 01 §8 y §11, 05 |
| 5 | «Estable» había pasado a significar «está en Figma»; al calcular el estado con criterios automáticos aparecieron fallos reales (contraste en oscuro en 10 componentes y ninguna prueba de teclado). | Lectura de la decisión de Helix; **el cálculo no se ejecutó** | 07 §3 |
| 6 | Un hook de Claude Code que **agota su tiempo no bloquea** la llamada salvo que se configure `onFailure: "block"`: un guardarraíl «duro» que falla en silencio es blando. | Documentación de Claude Code | 06 §7 |
| 7 | La puerta del dueño de Helix **deja pasar** el cambio si no puede leer la orden («falla abierto»). | Lectura del hook; **no se ejecutó** | 08 §3 |
| 8 | Las 12 comprobaciones de accesibilidad de Helix no incluyen comprobación propia visible para WCAG 2.1.2, 2.4.11, 3.3.1 y 3.3.2. | Lectura del ejecutor frente a WCAG 2.2 | 08 §6 |
| 9 | La fórmula de luminancia de WCAG nombra 0,03928 como umbral, pero la nota de erratas del W3C dice que el valor correcto es 0,04045; con colores de 8 bits la diferencia no es significativa. | Página de luminancia relativa del W3C | `scripts/contraste.py` |
| 10 | El modo oscuro no obliga por sí solo a abandonar una librería abierta: Mantine lo trae nativo y shadcn/ui entrega el código para editarlo. | Documentación de ambas | 09 §4 |
| 11 | DTCG 2025.10 es un informe final de un grupo comunitario, **no** un estándar del W3C. | Documentación del grupo | 02 |
| 12 | `llms.txt` es una propuesta, no un estándar; el de Helix no usa enlaces Markdown. | Documentación de la propuesta y lectura del archivo | 06 §4 |
| 13 | Una guía copiada se desactualiza: la guía de Helix tenía una línea que contradice su propia regla de paridad. | Lectura de la guía | 06 §5 |

## Sin verificar (pendientes de un caso real)

- Cálculo del estado de un componente, pruebas de teclado y evaluaciones con IA (no se ejecutaron).
- Servidor MCP de Helix por stdio y `setup:ai` (no se probaron por seguridad).
- Reglas específicas de WordPress y Astro.
- Las cifras de los relatos de empresas (68 componentes en 3 meses, etc.): son anécdotas.
