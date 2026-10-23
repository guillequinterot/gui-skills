# Modelo operativo de tareas (gestor de proyectos) [ClickUp]

Origen: el estándar interno "Cómo usamos ClickUp" (vigente desde 2026-10) y patrones de unas 4.850 tareas, anonimizados. Sirve para que la skill **redacte** tareas y entregables con la estructura que espera el equipo. **La skill no crea ni modifica tareas en ninguna herramienta** sin una instrucción explícita.

## Carpetas por cliente
01 Fase inicial · 02 Operación mensual (recurrente) · 03 Bolsa de expansión · 04 Dependencias del cliente · 05 Solicitudes y control de alcance.

## Nombre de la tarea
`PREFIJO | Nombre`, donde el prefijo es la sigla del cliente o del frente. Cada tarea cita la **cláusula del contrato** que la cubre; si no hay cláusula, la tarea está **fuera de alcance** y se marca así antes de ejecutarla.

## Estados
Por hacer → En curso → Revisión interna → Enviado al cliente (el cliente tiene 3 días hábiles para responder) → Ajustes → Bloqueado por cliente → Aprobado → Cerrado.

## Campos útiles para el SEO
- **Frente**: Estrategia, SEO, IA, Sitio web, Contenido, Redes, Pauta, Comunicaciones, Reputación, Analítica, Gestión.
- **Tipo de pieza** y **Piezas que cuentan** (meta mensual de contenido, por ejemplo 10).
- **Mes de operación**.
- **Aprobación del cliente** y **Fecha de aprobación escrita**.
- **Nivel de servicio**: Crítica 2 h · Alta 4 h · Normal 1 día · Planificada.
- **Link entregable**.

Etiquetas típicas: `entregable`, `recurrente`, `esperando-cliente`, `fuera-de-alcance`.

## Tarea madre y subtareas
- La **tarea madre es el entregable**: 0 h, un solo día (la fecha de entrega), a cargo de la cuenta y con la etiqueta `entregable`.
- Las **subtareas son el trabajo**: una persona cada una, con horas estimadas. Las subtareas aparte son:
  - **QA**;
  - **"Ajustes · Ronda N"** (nunca como ítems de checklist);
  - las reuniones, que también son tareas con horas.
- La capacidad es de 8 h por persona y día.

## Operación mensual: 11 frentes
1. Contenido (mínimo de piezas).
2. SEO técnico y de contenidos.
3. SEO programático.
4. Posicionamiento en IA (GEO/AEO/entidad).
5. SEO local.
6. Pauta.
7. Comunicaciones.
8. Redes.
9. Voceros.
10. Escucha y reputación.
11. **Informe mensual de KPI**.

## Patrones recurrentes de tareas SEO (vistos en el histórico)
- Reunión SEO quincenal con acta (cada acuerdo pasa a ser una tarea) y sprints internos.
- Informes mensuales y trimestrales (SEO + pauta), con las novedades de estrategia del trimestre siguiente.
- Auditorías: inicial, "2.0" de seguimiento, pre/post migración, WordPress + servidor, rendimiento. Después viene la **validación de implementaciones**, que revisa en la pestaña de incidencias si cada fila quedó bien.
- Redirecciones: plan de redirecciones, mapa de 404, URLs duplicadas o "de prueba" que se redirigen a la oficial, redirect + noindex.
- Enlazado interno: TOP-20 de posts por tráfico hacia transaccionales, cursos o diplomados hacia programas largos, servicios↔industrias, banners, revisión de anchor text (visibles sin hover).
- Contenido: game plan, KWR por artículo (principal + long tail en una columna), FAQs nuevas por tema (calidad, reconocimiento, autoridad), "humanización + SEO" de landings, landings en tono conversacional y landings por país.
- Programático: plantilla → contenido → diseño → despliegue → canonical → solicitud de indexación → medición en Clarity.
- Local: optimización de GBP (nombre, fotos, ciudades de cobertura que enlazan a landings geolocalizadas) y publicaciones en GBP.
- Capacitación SEO al cliente: GSC, lectura de métricas, indexación, KWR básico.


## Ampliación [ClickUp 2]: higiene, prefijos, pedidos white-label y briefs

Origen: lectura a fondo de unas 600 tareas de una cuenta de tres años y de varias listas de contrato (anonimizado). Para el modelo de contrato por fases y los campos de alcance, ver [contract-phases-and-scope-control.md](contract-phases-and-scope-control.md).

### Prefijos de título operativos
`URGENTE ·`, `HOY ·`, `[EN PAUSA]` (con estado estancado), `Repr <cliente> |` para el reproceso derivado de una auditoría de QA, y una **tarea madre mensual** («Ajustes sitio web (CMS) - <mes año>») con una hija por URL como contenedor de la cola de cambios del cliente. Nombres sin erratas ni mayúsculas inconsistentes: dificultan filtrar y reportar.

### Higiene de estados (reglas)
- «En revisión» lleva responsable y plazo; sin ellos funciona como cementerio (en dos cuentas, 20-30 % de las tareas del año quedaron ahí).
- Comprobar el **tipo** de cada estado: en listas heredadas «en revisión» puede ser tipo *hecho* y dejar tareas sin cerrar.
- Estancada = bloqueada por quién + quién destraba + fecha de reintento. Obsoleta = se archiva con una nota; nunca «hacer caso omiso» en el título.
- Una lista «del año» que sigue recibiendo tareas años después: cerrarla o abrir listas por fase.
- Comentario de decisión obligatorio cuando una tarea cambia de enfoque, y **criterio de hecho verificable** en toda tarea (sin él se reabre: una tarea de menú se repitió cinco veces). Crear una tarea de «ajustes finales» no sustituye al criterio.
- Cargar el tiempo real al terminar y estimar siempre; el tiempo gastado en 0 impide calibrar. Nunca inflar horas en un informe.
- En entregas a un tercero, el estado «revisión» no equivale a hecho: registrar la **fecha de implementación por el cliente** y re-medir.

### Pedido de optimización por URL en marca blanca
Contrato mínimo de entrada de una optimización on-page cuando la agencia trabaja para otra agencia:

`| <cliente final> | <fecha> | Optimización de contenido | <instrucción estándar> | URL · consultas de Search Console de 3-6 meses |`

- **Línea de audiencia en mayúsculas** («EL CLIENTE ES <país>, enfoque B2B, NO usuario final»): es el contrato de intención de la pieza.
- Opcionales: keyword principal impuesta; keyword con la que ya posiciona; «la URL no posiciona por ninguna keyword: buscar una»; competidores nombrados como referencia de profundidad; nota editorial (cubrir también la intención positiva, no solo las consecuencias).
- Variante antigua: lista de conceptos a proponer (metadatos, encabezados, enlazado interno, textos alternativos, preguntas frecuentes).
- Entregable: un **enlace por URL a una página anotada** (herramienta que superpone los cambios sobre la URL viva) en un comentario de la tarea y por correo al contacto; quien implementa es el equipo del cliente. 1 h por optimización.
- Riesgos: las filas de lotes anteriores se arrastran en la descripción (duplicar trabajo) y un entregable en un comentario es difícil de recuperar; guardar además el enlace en una hoja de seguimiento.

### Esqueletos de brief
- **Brief de 6 partes** y regla «las tareas apuntan a una pestaña de la hoja matriz, no copian datos».
- **Acción del cronograma:** `Tu apoyo con la siguiente acción del cronograma: <acción>: <propósito en una frase> 1. 2. 3. <alcance: páginas> <insumo> <dónde dejar el resultado: pestaña nombrada>`. En cronogramas de estrategia: una pestaña por acción y acciones «solo de contexto» marcadas por color (no se implementan).
- **Tarea de proyecto numerado** («tarea N de M»): contexto → qué se encontró → por qué importa → qué hacer → datos de referencia (área, semana, fase, severidad, tiempo, responsable por rol, depende de) → soportes a adjuntar.
- **Diseño de mockup:** padre con checklist de insumos (marca, arquitectura, wireframe, mockup, ubicación del archivo) + subtareas de ajustes; páginas listadas en «desktop y responsive».
- Defectos de plantilla a evitar al redactar: checklist del entregable vacío, sin criterio de hecho, sin prioridad, sin marcador del retraso del cliente.
