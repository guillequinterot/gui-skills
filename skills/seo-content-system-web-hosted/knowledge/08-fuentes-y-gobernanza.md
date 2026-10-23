<!-- GENERADO por tools/build_hosted.py desde skills/seo-content-system (v1.5.0, huella 4a445df6cfd7). NO EDITAR A MANO: cambia la skill o hosted-src/ y regenera con `python tools/build_hosted.py`. -->

# Fuentes, evidencia y gobernanza de actualizaciones

Cómo verificar y jerarquizar fuentes, el registro oficial de referencias, y cómo promover un aprendizaje de candidato a regla estable.

---

## Fuente original: `source-verification-and-evidence.md`

# Verificación de fuentes y evidencia

## Índice

- Jerarquía
- Registro
- Verificación
- Citas
- Temas sensibles
- Caducidad

## Jerarquía

1. Documentación oficial y fuentes primarias.
2. Investigación académica original.
3. Organizaciones profesionales reconocidas.
4. Medios y análisis especializados.
5. Proveedores y blogs comerciales.
6. Comunidades y anécdotas.
7. Síntesis internas.

Una síntesis interna organiza conocimiento; no prueba sus propias conclusiones.

## Registro

| Campo | Contenido |
|---|---|
| Afirmación | Texto verificable |
| Fuente | URL o documento |
| Autor/organización | Responsable |
| Publicación/actualización | Fecha |
| Consulta | Fecha |
| Tipo | Primaria, académica, etc. |
| Alcance | País, muestra, producto |
| Limitaciones | Sesgos o condiciones |
| Estado | Pendiente, verificada, descartada |
| Próxima revisión | Fecha |

## Verificación

- Abrir la fuente completa.
- Confirmar que respalda la afirmación exacta.
- Revisar fecha y versión.
- Preferir la fuente original.
- Contrastar cifras importantes.
- Diferenciar correlación y causalidad.
- Conservar contexto y limitaciones.

## Citas

Parafrasear con fidelidad. No atribuir declaraciones que la fuente no hace. No usar una cita solo para aumentar “densidad factual”.

## Temas sensibles

Aplicar controles adicionales en salud, finanzas, legal, seguridad y políticas públicas. No extrapolar estudios a poblaciones distintas sin advertencia.

## Caducidad

Asignar frecuencia:

- Alta: plataformas, algoritmos, leyes, precios, interfaces.
- Media: benchmarks, estudios y herramientas.
- Baja: fundamentos lingüísticos o conceptuales.

Un contenido antiguo no es automáticamente incorrecto; una fuente reciente no es automáticamente mejor.

---

## Fuente original: `official-source-register.md`

# Registro de fuentes oficiales

## Índice

- Google Search
- Medición
- Datos estructurados y web
- Lenguaje y accesibilidad
- Plataformas de skills
- Política de uso

## Google Search

- Search Essentials: https://developers.google.com/search/docs/essentials
- SEO Starter Guide: https://developers.google.com/search/docs/fundamentals/seo-starter-guide
- Helpful content: https://developers.google.com/search/docs/fundamentals/creating-helpful-content
- AI features: https://developers.google.com/search/docs/appearance/ai-features
- Title links: https://developers.google.com/search/docs/appearance/title-link
- Snippets: https://developers.google.com/search/docs/appearance/snippet
- Image SEO: https://developers.google.com/search/docs/appearance/google-images
- Crawlable links: https://developers.google.com/search/docs/crawling-indexing/links-crawlable
- Structured data policies: https://developers.google.com/search/docs/appearance/structured-data/sd-policies
- Spam policies: https://developers.google.com/search/docs/essentials/spam-policies
- Search Central Blog: https://developers.google.com/search/blog
- Search Status Dashboard: https://status.search.google.com/
- Search Console: https://search.google.com/search-console/about
- Business Profile ranking: https://support.google.com/business/answer/7091

## Medición

- Google Analytics: https://support.google.com/analytics/
- Search Console API: https://developers.google.com/webmaster-tools
- Microsoft Clarity: https://learn.microsoft.com/clarity/
- Google Trends: https://trends.google.com/trends/

## Datos estructurados y web

- Schema.org: https://schema.org/
- Schema.org releases: https://github.com/schemaorg/schemaorg/releases
- Web.dev: https://web.dev/
- W3C Web Accessibility Initiative: https://www.w3.org/WAI/
- WCAG: https://www.w3.org/WAI/standards-guidelines/wcag/

## Lenguaje y accesibilidad

- RAE: https://www.rae.es/
- FundéuRAE: https://www.fundeu.es/
- WAI alt decision tree: https://www.w3.org/WAI/tutorials/images/decision-tree/

## Plataformas de skills

- Codex skills: https://developers.openai.com/codex/build-skills
- Claude Code skills: https://code.claude.com/docs/en/skills
- Antigravity skills: https://codelabs.developers.google.com/antigravity/how-to-create-agent-skills-for-antigravity-cli

## Política de uso

- Registrar fecha de consulta.
- Leer la página completa antes de citar.
- Revisar enlaces al menos trimestralmente.
- No interpretar una función de interfaz como factor de ranking.
- No usar una fuente secundaria para contradecir documentación oficial sin evidencia.

---

## Fuente original: `update-governance-and-research.md`

# Gobernanza de actualizaciones e investigación periódica

## Índice

- Objetivo
- Tres niveles
- Flujo de investigación
- Criterios de promoción
- Conflictos
- Cadencia
- Seguridad

## Objetivo

Permitir que el sistema aprenda sin reescribir reglas estables a partir de una sesión aislada, una opinión o una noticia no verificada.

## Tres niveles

### 1. Observación

Hallazgo de un proyecto:

- Contexto.
- Acción.
- Resultado.
- Evidencia.
- Limitaciones.
- Fecha.

Estado: `candidate`.

### 2. Hipótesis validable

La observación se repite, coincide con datos o tiene respaldo independiente.

Estado: `testing`.

### 3. Regla estable

Existe evidencia suficiente, se define el alcance y se aprueba el cambio.

Estado: `promoted`.

No sobrescribir una regla sin guardar la decisión y la versión anterior.

## Flujo de investigación

```text
Recopilar cambios
→ deduplicar
→ leer fuente completa
→ clasificar autoridad
→ identificar afirmación
→ contrastar
→ evaluar impacto
→ probar
→ promover o descartar
```

`research_update.py` recopila y compara fuentes; no valida por sí solo el significado del cambio.

## Criterios de promoción

Promover cuando:

- La fuente es oficial o primaria, o existe contraste sólido.
- La recomendación tiene alcance definido.
- No contradice evidencia superior sin explicación.
- Puede convertirse en una acción verificable.
- Se documentan riesgos y excepciones.
- La fecha de revisión está asignada.

## Conflictos

Si dos fuentes discrepan:

1. Priorizar la más cercana al sistema evaluado.
2. Revisar fechas y versiones.
3. Distinguir política, documentación, experimento y opinión.
4. Registrar ambos puntos.
5. Mantener la regla anterior si no existe evidencia suficiente.

## Cadencia

- Semanal: recopilar novedades de alta volatilidad.
- Mensual: revisar Search Central, Search Console, GA4, schema y plataformas clave.
- Trimestral: auditar reglas estables y enlaces de fuentes.
- Por evento: revisar tras core update, spam update o cambio de producto.

La frecuencia se configura; no debe implicar modificación automática de producción.

## Seguridad

- No guardar tokens, cookies, contraseñas ni datos personales.
- No ejecutar código descargado desde fuentes.
- Limitar tamaño y tiempo de descargas.
- Registrar errores sin volcar secretos.
- Mantener la investigación en modo lectura.

---

## Fuente original: `agency-operating-methodology.md`

# Metodología operativa de agencia [ClickUp]
Origen: patrones de unas 4.850 tareas (paginación completa, 2022–2026) y 59 leídas a fondo en ClickUp, anonimizados.

## Fases y listas por contrato
1. **Fase inicial:** accesos (GSC, GA4, GTM, CMS, Screaming Frog), entendimiento del negocio, auditoría técnica, estrategia, game plan y keyword mapping.
2. **Operación mensual:** sprint quincenal, correcciones por hallazgo, contenido, informe mensual.
3. **Bolsa de expansión y mercados:** nuevos países o idiomas (hreflang), programático.
4. **Dependencias del cliente:** insumos, aprobaciones, entrevistados, fotos. Se registran como tareas bloqueantes.
5. **Solicitudes y control de alcance:** cada pedido se asocia a una cláusula y se indica si entra en el fee.

Ciclo de crecimiento (variante GDD): Entendimiento → Estrategia → Launchpad → Dashboard → Mejoras continuas → Handoff de operaciones.

## Cadencia
- Reunión semanal o quincenal con acta. Cada acuerdo se convierte en tarea.
- Sprint quincenal.
- Informes: mensual, de rendimiento después de las implementaciones, y semestral.

## Contenido
- **Flujo:** game plan → KWR → redacción → portada → CMS → enlazado interno o módulo de relacionados.
- **Fuentes:** entrevistas con expertos (EEAT), podcast, video y conferencias.
- **Multiformato:** blogpost, presentación, resumen ejecutivo, tabla de datos e infografía.

## Link building
1. Matriz de notas en medios.
2. Resumen de prensa con enlaces al home, a la nota original y a 1–2 servicios.
3. Newsletter de LinkedIn.
4. Publicación en GBP.

## Roles y flujo de una landing
- **Roles:** account (brief, aprobación), contenido, diseño UI, front, SEO técnico (formularios, GA4 y eventos de píxel), QA.
- **Flujo:** brief → copy → UI → maquetación → medición → QA interno → ajustes → envío al cliente → ronda 1 de ajustes.
- **Criterio de hecho:** publicada, formulario probado con el evento registrado, QA cerrado y aprobación escrita del cliente.

## Migración
- QA por prioridad (Crítico/Alto/Medio/Bajo/Neutral).
- En el lanzamiento: redirecciones, GA4, GSC, GTM, HTTPS y cabeceras, nomenclatura de URLs.
- Chequeos post-migración.

## Ver también
- `onboarding-and-initial-audit.md` · `growth-driven-design-gdd.md` · `clickup-task-operating-model.md` · `migration-redirects-and-validation.md` · `wordpress-technical-audit-checklist.md`


## Ampliación [ClickUp 2]

Origen: lectura de listas de tres años, de un contrato por fases y de plantillas GDD (anonimizado; cobertura parcial, ver `docs/INVESTIGACION-CLICKUP-SEO.md` §23). Detalle en [contract-phases-and-scope-control.md](contract-phases-and-scope-control.md), [launch-checklist-new-site.md](launch-checklist-new-site.md), [ecommerce-seo-multicountry.md](ecommerce-seo-multicountry.md) y [education-program-seo.md](education-program-seo.md).

### Fases de un contrato (variante observada)
Accesos y entendimiento → investigación en paralelo (~2 semanas: KWR, benchmark, competidores, auditoría UX, dashboard, GSC/GA4 en subdominios) → cronograma de estrategia y OKR → socialización → optimización de lo existente (metadatos, encabezados, rendimiento, 404, sitemap, enlazado, CTA, mapas de calor) → producción de landings (geolocalizadas, por industria, por evento) → gobernanza (reunión semanal, SEO quincenal, informes) → capacitación al equipo que despliega. Una reunión de revisión interna **antes** de mostrar entregables al cliente.

### Reparto y secuencia de un sprint de lanzamiento
SEO de contenido (keywords, textos, metas, alt) separado de SEO técnico + analítica (especificación, medición, QA); el texto bloquea al diseño; validar el render con desarrollo antes del prototipo; entrega al cliente y revisión a los 7 días. Ver [launch-checklist-new-site.md](launch-checklist-new-site.md).

### Contenido y venta
- **Artículo + versión LinkedIn** como entregable estándar por artículo propio; **pipeline podcast/episodio → artículo → imágenes → LinkedIn → PDF de recursos → programas relacionados**.
- **Gestión por matriz de colores** de aprobación (verde aprobado · azul comentarios por atender · naranja ajustado y listo para reenviar · amarillo/rojo/rosado pendientes) y columna «implementado».
- Rutina de cambios del cliente: el cliente envía ajustes por correo, PDF o grabación → la PM crea tareas → quien ejecuta devuelve una **captura por punto**.
- **Auditoría comercial a un prospecto:** hoja completa + presentación resumida sin marca; **exploración de un CMS ajeno en 8 puntos** (solo explorar, nunca modificar) con entregable de 4 secciones y lista de dudas para el contacto. Los accesos de un CMS ajeno nunca viajan por mensajería ni en la tarea.
- **SEO + CRO:** mapas de calor, CTAs por tipo de página, banners de conversión y enlazado, página de gracias para medir conversión, pruebas A/B sobre las páginas transaccionales prioritarias; refresco de casos de éxito (filtro por industria, tarjetas con métrica, testimonios con retrato).
- **Biblioteca de módulos** (equipo, banners, sucursales, galería de videos, descarga de guía, carrusel de blog) como activo de diseño y SEO.

### Link building: variantes
- Artículo de nota de prensa en variante larga (1.400-1.700 palabras) con enlaces obligatorios y opcionales.
- **Cadena de publirreportajes:** plan de compra → plan de redacción → redacción → revisión → compra → registro, con presupuesto por enlace y plataforma. Estimar con holgura: el esfuerzo se subestimó varias veces.
- **Alerta de política de enlaces:** un ranking propio con enlace *do-follow* con UTM hacia terceros, o un enlace pagado, puede ser esquema de enlaces; usar `rel="sponsored"` o `nofollow` y documentarlo.
- Plan de medios de bajo costo por país (ver [contract-phases-and-scope-control.md](contract-phases-and-scope-control.md)); antes de comprar enlaces, consolidar el mercado piloto.

### Estimaciones (orden de magnitud, no compromiso)
Título/meta de un lote 1-2 h; KWR 2,5-3 h; benchmark 2 h; competidores 0,5-3 h; auditoría UX 6 h; mapas de calor 4 h; optimización de contenido por URL 1 h; artículo + versión LinkedIn ~2,3 h; optimización semántica ≥ 2 h por artículo; montar un programa en el CMS ~40 min; dashboard 15 h + 2 ajustes de 1 h. Las tareas de «ajustes» se reabren: dar holgura.

---

## Fuente original: `contract-phases-and-scope-control.md`

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

---

## Fuente original: `clickup-task-operating-model.md`

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
