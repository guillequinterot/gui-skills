<!--
PLANTILLA · ficha-de-auditoria
Para qué: el informe del modo `auditar`: hallazgos con evidencia y, sobre todo, lo que NO se comprobó. Recorre las listas de revisión de las referencias según el perfil.
Modo: auditar · Perfil: todos (las secciones marcadas [app] y [compartido] se borran en `website`) · Referencias: 01–09 (cada sección indica la suya)
Cómo se usa: una ficha por auditoría. En cada punto escribe ✓ / ✗ / n.a. / NC (no comprobado) y la EVIDENCIA (archivo, línea, captura, comando). Sin evidencia, el punto es NC.
Reglas: no escribas «verificado» ni «válido» sin un verificador que lo haya comprobado: escribe «revisado a mano» · un hallazgo sin evidencia no es un hallazgo · lo que el análisis no cubre (Figma sin acceso, evaluaciones sin permiso, hosting no escaneable) se declara en la última sección · el agente no cambia nada durante una auditoría: propone, y decide la persona responsable · una auditoría no cambia el perfil: solo avisa de las señales de la regla de salto.
-->

# Auditoría · <proyecto o código de caso>

**Fecha:** <AAAA-MM-DD> · **Auditor:** <persona o agente> · **Perfil de proyecto:** <website | app | sistema compartido> · **Perfil de gobierno:** <individual | equipo> · **Fuente de verdad registrada:** <contrato/código | Figma>

## 1. Alcance y fuentes consultadas

- **Qué se auditó:** <componentes, archivos, Figma, documentación>
- **Con qué:** <lectura de archivos, scripts, lecturas de solo consulta de Figma, ninguna herramienta>
- **Versión o commit:** <…>

## 2. Resumen

<Tres a cinco frases: estado general, lo más grave y lo que no se pudo comprobar.>

| ✓ | ✗ | n.a. | NC |
|---|---|---|---|
| <n> | <n> | <n> | <n> |

## 3. Hallazgos

| # | Área | Hallazgo | Evidencia | Impacto (alto · medio · bajo) | Recomendación | Ref. |
|---|---|---|---|---|---|---|
| 1 | <contrato / tokens / vocabulario / documentación / Figma / IA / medición / accesibilidad / gobierno> | <qué pasa> | <archivo, línea, captura o comando> | <…> | <qué hacer; si implica elegir, 2–3 opciones> | <nº de referencia> |

## 4. Tres pilares (¿es un sistema o un UI kit?) — 04, 09

| Pilar | Estado | Evidencia |
|---|---|---|
| Piezas de interfaz | | |
| Guías y documentación | | |
| Guía de estilo / gobierno conectada con desarrollo | | |

## 5. Contrato — 01

| Punto | Estado | Evidencia |
|---|---|---|
| Propósito en una frase y desde quien lo usa | | |
| «Nunca usar para» con alternativa | | |
| Justificación con la decisión | | |
| Qué se adapta y qué se escala | | |
| Anatomía con el mismo nombre en código y Figma | | |
| Estados: intrínsecos separados de los gestionados, con ARIA | | |
| Props con nombre canónico y valor por defecto igual en ambos lados | | |
| Origen declarado [app][compartido] | | |
| Criterios WCAG con nombre oficial | | |
| Partes generadas marcadas y sin editar a mano | | |
| Sin cifras copiadas que se desactualicen | | |

## 6. Tokens y nombres — 02

| Punto | Estado | Evidencia |
|---|---|---|
| Perfil y número de capas coherentes (website: 2, sin tokens de componente) | | |
| Componentes sin primitivos directos (o con excepción documentada) | | |
| Nombres sin valor dentro y con vocabulario cerrado | | |
| Tabla de traducción entre plataformas | | |
| Glosario con sinónimos y términos rechazados | | |
| Cada semántico con descripción (y la misma en Figma) | | |
| Oscuro como modificador, no copia | | |
| Contraste por par y por tema, sin redondear; deshabilitado documentado | | |
| Cifras con capa y fecha | | |

## 7. Vocabulario — 03

| Punto | Estado | Evidencia |
|---|---|---|
| Una palabra por concepto y un concepto por palabra | | |
| Prohibidos con alternativa y fecha | | |
| Nombres nativos de HTML/ARIA donde existen; sin choques | | |
| Texto como contenido (`children`); `label` solo en campos | | |
| Valores en la escala corta y por prop | | |
| Misma palabra en código y en Figma | | |
| Filas dudosas (`readonly` ≠ `disabled`, `open`, escala frente a subconjunto) | | |
| Verificador sobre props reales (o «revisado a mano») | | |

## 8. Documentación y entrega — 04

| Punto | Estado | Evidencia |
|---|---|---|
| Documentación empezada por puntos de dolor reales | | |
| Una plantilla de página probada con una página antes de replicar | | |
| Propósito único (contrato = página = Figma) | | |
| Componentes reales en la página; matriz única | | |
| Hacer / no hacer y buenas prácticas de contenido | | |
| Lista de control con criterios WCAG | | |
| Tabla de estado con criterios definidos | | |
| Novedades y canal de avisos | | |
| Entrega a desarrollo definida y formato acordado | | |
| Páginas públicas con `noindex` y sin bloqueo en `robots.txt` | | |

## 9. Figma — 05 [app][compartido]

| Punto | Estado | Evidencia |
|---|---|---|
| Fuente de verdad registrada y coherente | | |
| Colecciones y modos según el perfil; alcance fijado | | |
| Nombres de variable con la tabla de traducción | | |
| Texto con estilos de texto reales | | |
| Propiedades según la regla de conversión; sin propiedades solo-Figma sin aprobar | | |
| Valores por defecto iguales que en el código | | |
| Todos los estados dibujados | | |
| Colores y espaciado enlazados; sin literales | | |
| Componentes fuera de Figma documentados en el contrato | | |

**Anexo · auditoría de un componente en Figma:** colores y trazos enlazados a variables semánticas · espaciado y radios enlazados · todos los valores de `state` dibujados · colores iguales al código en claro y oscuro · el borde siempre existe · paridad de propiedades · listas · anillo de foco sin recortar · descripción presente y capas con los nombres de las partes.

| Componente | Resultado por punto (✓/✗/NC) | Evidencia |
|---|---|---|
| <…> | <…> | <lecturas de solo consulta de Figma, captura o «revisado a mano»> |

## 10. Listo para IA — 06

| Punto | Estado | Evidencia |
|---|---|---|
| Nota raíz con la regla de leer el contrato antes de escribir | | |
| Dos audiencias separadas (usar / construir) | | |
| Instrucción y descubrimiento distintos; `llms.txt` con forma oficial si se publica | | |
| Inventario y tablas generados; la guía no contradice al contrato | | |
| Errores frecuentes vistos en pruebas reales | | |
| Guardarraíles clasificados (blando o duro); los hooks con su `onFailure` conocido | | |
| Archivo de solicitudes con modelo usado [app][compartido] | | |
| El agente no elige tokens ni valores: presenta opciones | | |
| Nada se instala ni registra sin permiso expreso | | |

## 11. Medición — 07

| Punto | Estado | Evidencia |
|---|---|---|
| Cada métrica con su acción prevista | | |
| Sin puntuación única; por versión y en tendencia | | |
| «No disponible» donde no hay datos | | |
| Estado calculado (o «no verificado» a mano en `website`) | | |
| Accesibilidad por tema y teclado aparte; las revisiones humanas no puntúan | | |
| Literales permitidos definidos | | |
| Permiso antes de lanzar evaluaciones que gastan turnos de un modelo | | |

## 12. Gobierno, accesibilidad y estabilidad — 08

| Punto | Estado | Evidencia |
|---|---|---|
| Perfil de gobierno elegido y anotado | | |
| Dueño y archivos protegidos definidos | | |
| Escalera ¿puede? ¿debería? ¿se le permite? aplicada | | |
| Procedimiento de propuesta con opciones y recomendación | | |
| Decisiones escritas (contexto, decisión, consecuencias) | | |
| Reglas de composición escritas, con excepciones y motivo | | |
| Accesibilidad por tema; criterios 2.1.2, 2.4.11, 3.3.1 y 3.3.2 en la lista de control | | |
| Revisión humana registrada con fecha, persona y tecnología | | |
| Versiones semánticas; deprecación antes de retirar; guía de migración | | |
| Los guardarraíles duros declaran qué pasa si fallan | | |

## 13. Arranque y regla de salto — 09

| Punto | Estado | Evidencia |
|---|---|---|
| ¿Hace falta un sistema? (respuesta decidida y anotada) | | |
| MVP definido con lo que no entra | | |
| Librería de partida anotada como origen | | |
| Señales de salto de perfil vistas | ☐ 0–1 (se anotan) ☐ 2 o más (se avisa) | <señales> |

## 14. Qué NO se comprobó

<Lista obligatoria. Para cada punto NC: por qué (sin acceso, sin permiso, sin verificador, fuera de alcance) y qué haría falta. Si no hay nada pendiente, escribe «nada pendiente» solo si es cierto.>

## 15. Siguiente paso propuesto

<Las 1–3 acciones de mayor impacto. Si hay que elegir entre opciones, preséntalas con su efecto; decide la persona responsable.>
