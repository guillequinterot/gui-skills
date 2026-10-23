---
tags:
  - seo
  - operacion
  - alcance
---

# Contrato por fases y control de alcance [ClickUp 2]

Origen: una carpeta de contrato con cinco listas, sus descripciones y campos personalizados, más tareas de otros contratos (anonimizado). **Evidencia parcial:** la carpeta se creó el 2026-10-16 y casi no tiene tareas reales; el modelo sale de las descripciones de lista y de los campos, no de meses de operación. Tratarlo como **modelo propuesto y verificado en estructura**, no como práctica probada. Complementa [clickup-task-operating-model.md](clickup-task-operating-model.md) y [agency-operating-methodology.md](agency-operating-methodology.md).

## Índice

- Estructura de la carpeta
- Reglas de cada lista
- Campos y vocabularios
- Estados y la trampa de «en revisión»
- Tarea madre de una landing con nueve subtareas
- Matriz de solicitudes y informe de acciones
- Lista de convergencia entre cuentas hermanas
- Higiene de tareas

## Estructura de la carpeta

Una carpeta por contrato y cinco listas que reflejan las cláusulas. Cada lista lleva en su descripción: monto o regla económica, plazos, responsable y reglas de uso.

| Lista | Qué contiene | Regla central |
|---|---|---|
| 01 Fase inicial | Cobro único, ~6 semanas: ganancias tempranas y estrategia | **Una tarea por literal del contrato**, cada una con su cláusula. Un hito grande (p. ej. una feria) es tarea padre con subtareas |
| 02 Operación mensual | Tarifa mensual desde la semana 7 | **Una tarea recurrente mensual por frente**; cada pieza de contenido es subtarea |
| 03 Bolsa de expansión y mercados | Monto sugerido para terceros (no son honorarios ni gasto obligatorio) | **Una tarea por solicitud de uso** con concepto, valor, fecha de aprobación escrita y soporte. **Saldo = bolsa − suma de los valores aprobados**. Sin aprobación escrita no se compromete nada |
| 04 Dependencias del cliente | Insumos, accesos, información y aprobaciones a cargo del cliente | Cada tarea lleva fecha de solicitud, a quién se pidió y fecha de entrega. **Si el cliente se demora, el cronograma se corre y no cuenta como incumplimiento** |
| 05 Solicitudes y control de alcance | Bandeja de entrada de lo no planeado | Se clasifica por **nivel de servicio** y por **alcance** (ver abajo) |

## Reglas de cada lista

- **Reglas de conteo de piezas** (operación mensual): la misma pieza en otra red o una adaptación solo técnica **no** cuenta otra vez; una adaptación con redacción, edición o montaje nuevos **sí** cuenta aparte; la producción externa se cotiza.
- **Mercado nuevo**: tarifa fija por país por la estrategia; la **ejecución en ese mercado se cotiza aparte**.
- **Aprobaciones**: cada pieza pasa por «enviado al cliente» con plazo de **3 días hábiles**; la aprobación escrita se registra con fecha. No se publica ni se activa pauta sin ella.
- **Correos y reuniones no cambian el alcance.** Solo cambia por una cotización aprobada por escrito.
- **Bandeja 05**: toda solicitud nueva entra aquí y se clasifica en dos ejes:
  1. Nivel de servicio: Crítica (primera respuesta en 2 h laborales) · Alta (4 h) · Normal (1 día hábil) · Planificada (según lo acordado). Horario laboral definido en el contrato.
  2. Alcance: si está dentro del contrato **se mueve a la lista 01 o 02**; si está fuera se marca «Fuera de alcance (cotizar)» y solo se ejecuta cuando pasa a «Cotizado y aprobado por escrito».
- **Una tarea sin cláusula no se ejecuta hasta clasificarla** («Sin cláusula (revisar alcance)»).
- **Reestructuración a mitad de camino**: conservar una lista «[Migrar] tareas anteriores» con una nota («se migran a 01-05; cuando quede vacía se archiva») en vez de borrar o dejar tareas sueltas.

## Campos y vocabularios

| Campo | Valores |
|---|---|
| Frente (11) | Estrategia · SEO · Posicionamiento en IA · Sitio web · Contenido · Redes sociales y CM · Pauta · Comunicaciones y voceros · Reputación y social listening · Analítica · Gestión de cuenta |
| Tipo de pieza | Blog (~3.000 palabras) · Adaptación a LinkedIn (~1.000) · Video horizontal · Short/Reel · Carrusel · Pieza gráfica · Pieza fotográfica · Secuencia de stories · **Adaptación técnica (no cuenta)** |
| Piezas que cuentan / Mes de operación | Número · Mes 1…N del contrato |
| Alcance (4) | Dentro del contrato · Fuera de alcance (cotizar) · Cotizado y aprobado por escrito · Bolsa de expansión |
| Cláusula | Un valor por cada literal del contrato (fase inicial a–o, operación mensual a–k, bolsa, mercado nuevo, obligación del cliente, gestión de cuenta) + «Sin cláusula (revisar alcance)» |
| Nivel de servicio (4) | Crítica (2 h) · Alta (4 h) · Normal (1 día hábil) · Planificada |
| Aprobación del cliente (5) | No requiere · Pendiente de enviar · Enviado, esperando respuesta · Con observaciones · Aprobado por escrito |
| Tipo de trabajo (5) | Producción · QA · Reproceso interno · Ajuste pedido por el cliente · Gestión de cuenta |
| Otros | Fecha de solicitud · Contacto cliente · Fecha de entrega del cliente · Fecha de envío al cliente · Fecha de aprobación escrita · Valor (moneda, para la bolsa) · Link entregable · Responsable externo |

## Estados y la trampa de «en revisión»

- Carpeta de contrato (8): por hacer · en curso · revisión interna · enviado al cliente · ajustes · bloqueado por cliente · **aprobado** (tipo hecho) · **cerrado** (tipo cerrado).
- **Trampa de configuración en listas heredadas:** en las listas de cinco estados (nuevo · en proceso · estancado · en revisión · completado), «en revisión» puede estar definido como tipo *hecho* y «completado» como *cerrado*. Resultado observado: decenas de tareas «en revisión» que para el sistema ya cuentan como hechas y nadie cierra. Al diseñar o auditar un flujo, comprobar el **tipo** de cada estado, no solo su nombre, y dar al cierre un responsable.

## Tarea madre de una landing con nueve subtareas

Modelo de referencia (~17,5 h). Descripción de la madre: **Contexto** (objetivo y público) → **Alcance y cláusula** (con la interpretación explícita cuando el contrato no la nombra literal, «dentro del fee mensual», «sin costos de terceros») → **Qué hacer** (las subtareas con su rol) → **Qué NO hacer** (no publicar ni activar pauta sin aprobación escrita; no usar fotos de banco que parezcan generadas por IA) → **Criterio de hecho** → **Cómo entregar** (cada subtarea pasa a revisión con el enlace en «Link entregable»).

| Subtarea | Rol | Horas | Tipo de trabajo |
|---|---|---|---|
| Brief y estructura | Cuenta | 1 | Gestión de cuenta |
| Copy | Contenido | 2 | Producción |
| Diseño desktop y mobile con el sistema de diseño | Diseño | 4 | Producción |
| Maquetación responsive en el sitio | Front | 5 | Producción |
| Formulario y eventos de medición (GA4 + píxel) | SEO técnico | 1,5 | Producción |
| QA interno contra el criterio de hecho (diseño, responsive, textos, formulario, evento) | UX | 1 | QA |
| Ajustes del QA interno, ronda 1 | Front | 1,5 | Reproceso interno |
| Envío al cliente y seguimiento de aprobación | Cuenta | 0,5 | Gestión de cuenta |
| Ajustes pedidos por el cliente, ronda 1 | Front | 1 | Ajuste pedido por el cliente (**se ejecuta solo si el cliente pide cambios; si no, se cierra en 0**) |

Criterio de hecho: landing publicada, formulario probado (envío y evento registrado), QA cerrado sin pendientes y aprobación escrita. Las horas son orden de magnitud, no compromiso.

## Matriz de solicitudes y informe de acciones

- **Matriz mensual de solicitudes del cliente**: una hoja con pestaña por mes y filas numeradas (fecha de solicitud, actividad, OK al implementar, si entra al informe). Cada fila se convierte en tarea (`Contexto: fila N, fecha` → `Actividad` → `Origen`) o se implementa directamente, y se cierra con el OK en la matriz.
- **Informe mensual de acciones**: lista de las acciones del mes con el **tiempo real**, estado de cada fila de la matriz y borrador revisado antes de enviar. **Nunca inflar ni «exagerar» horas**: si una tarea pide hacerlo, no se replica; se reporta el tiempo real y trazable. Casi todas las tareas SEO leídas tenían las horas gastadas en 0: sin tiempo real no se puede calibrar esfuerzo; exigir cargarlo al terminar.
- **Plan de link building por país** (contrato multipaís): medios de menor costo para masificar información; los medios internacionales que aporte el cliente quedan solo como referencia hasta consolidar el mercado piloto. Criterios por medio: tráfico, autoridad de dominio, tendencia editorial y afinidad o animadversión editorial con el sector.

## Lista de convergencia entre cuentas hermanas

Cuando dos cuentas relacionadas comparten decisiones, una lista aparte solo para seis frentes: modelo de voceros y redes alternas; reputación y social listening (**una alerta que toque a la otra marca se escala a ambas cuentas**); SEO de entidad y asistentes de IA; narrativa y arquitectura de marca; mercados internacionales y medios (**no duplicar gasto**); gobierno del contrato (firmante, SLA, aprobaciones, facturación, mora). **Regla:** los entregables, valores y obligaciones de cada cuenta no se registran ahí; viven en la carpeta de cada cuenta y se enlazan.

## Higiene de tareas

- «En revisión» exige responsable y plazo (p. ej. 5 días). Si pasa del plazo, se cierra o se devuelve con motivo.
- Una tarea estancada lleva: bloqueada por quién, quién la destraba y fecha de reintento. Las obsoletas se archivan con una nota («qué se alcanzó y por qué quedó abierta»), no se marcan «hacer caso omiso».
- Una lista «del año» sigue recibiendo tareas años después: abrir listas por fase, no por año, o cerrar la del año.
- Criterio de hecho **verificable** en toda tarea. Sin él, la misma tarea se reabre una y otra vez (caso observado: una tarea de menú de navegación repetida cinco veces).
- Todo hallazgo de una auditoría viaja como tarea con su criterio de hecho; ver [technical-audit-by-finding.md](technical-audit-by-finding.md).
