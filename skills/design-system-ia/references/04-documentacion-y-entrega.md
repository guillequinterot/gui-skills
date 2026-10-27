# 04 · Documentación y entrega

> **Estado:** borrador (C-2, 2026-10-27) · **Perfiles:** los tres (cambia cuánto se documenta) · **Modos que la usan:** `documentar`, `auditar`, `construir`, `definir`.
> **Fuentes (reexpresadas; ver `CREDITOS.md`):** los videos y la plantilla de documentación de la autora de **Helix** (MIT, © 2026 Marta Conde), el sistema Helix (commit `394823a`: su página de estado, su registro de cambios y sus tarjetas de documentación en Figma), dos kits de documentación de la comunidad de Figma (autoría no vista; **tratar su licencia como «consultar antes de reutilizar»**), la charla de un equipo de Celonis y dos conversaciones sobre sistemas. **Inferencia propia** va marcada.
> **Contrastado con fuente primaria el 2026-10-27:** los criterios WCAG 2.2 que la lista de control cita, y cómo excluir una página de los buscadores (documentación de Google). **No contrastado:** el efecto real de cada práctica de documentación (son experiencias de equipos), la sección «handoff» (definición propia) y todo lo de WordPress/Astro.
> **Plantillas y scripts:** `scripts/generar_biblioteca.py` + `templates/biblioteca-manifiesto.json` (sección 13) · `templates/pagina-de-componente.md` · `templates/lista-de-control-componente.md` · `templates/patron.md` (opcional).

## 1. Qué es documentar un sistema

Tres pilares, conectados con desarrollo: **un kit de componentes, guías y documentación, y una guía de estilo**. Un conjunto de componentes en una librería **que nadie usa** no es un sistema; tampoco lo es un kit que **no llega a desarrollo** (sin documentación ni gobierno, el diseño y el código acaban siendo distintos).

Reglas generales:
- **No se documenta todo:** se documentan **las decisiones que más duelen**, empezando por lo que más preguntan.
- **Una sola fuente por dato:** el texto de propósito del componente es **el mismo** en el contrato, la página y Figma. Lo que se pueda **generar** de una fuente (tabla de estado, lista de tokens, cambios) **no se escribe a mano**.
- **Documentación para personas** (esta referencia) y **para agentes** (06) son dos documentos distintos.

## 2. Cuánta documentación según el perfil

| Perfil | Qué se documenta |
|---|---|
| `website` | **Página de componente breve** (sección 4) en el soporte que el usuario elija (HTML, Astro, WordPress o Figma) + una lista de estados; sin tabla de salud |
| `app` | Página de componente completa con Do/Don't y **lista de control**; tabla de estado; registro de cambios |
| `sistema compartido` | Todo lo anterior + **guía de contribución**, portada del sistema y canal de consulta |

## 3. MVP de documentación (orden de trabajo)

Fuente: video de la autora sobre el MVP de documentación, adaptado **sin** la herramienta de terceros ni Storybook (la adaptación es inferencia propia).

1. **Mapear los puntos de dolor:** las **preguntas repetidas** en los canales del equipo (se pueden resumir con IA). Ejemplos: tokens distintos entre diseño y desarrollo; dudas entre dos componentes parecidos.
2. **Una sola fuente al empezar** (tokens o componentes), la que más duele.
3. **Tabla de estado** de unos 10 componentes: nombre · **estado** · repositorio · Figma · documentación; ordenada alfabéticamente. «Sano» solo si **nombres y propiedades coinciden** entre Figma y código; mientras no hay página, «sin documentar». *Al arrancar se escribe a mano; **se desactualiza**: cuando haya verificadores se calcula (07).*
4. **Portada:** nombre, descripción corta de qué es y qué se encuentra, y **~5 accesos** a las secciones clave (novedades, componentes, fundamentos, recursos, soporte).
5. **Aspecto mínimo:** logo, color principal y de acento, superficies y navegación (unos 5 minutos).
6. **Novedades:** enlazar el **archivo de versiones o cambios** del repositorio: coste de mantenimiento casi nulo y resuelve «nadie se entera de los cambios».
7. **Una sola página de componente** como plantilla (sección 4); **pedir opinión** a diseño y desarrollo; **solo entonces replicar**.
8. **Fundamentos** (color: una pestaña por colección, con una explicación de qué es un token semántico), **recursos** (enlaces clave) y **soporte** (a quién preguntar).

**Criterio de éxito:** que se **desbloqueen puntos de dolor** (p. ej. la falta de sincronía entre diseño y desarrollo o de avisos de cambios), **no la cobertura**.

## 4. La página de componente

Una plantilla única que combina dos fuentes (la mezcla es **inferencia propia**: la de cuatro secciones de la comunidad y la de «resumen + uso» del video):

| Bloque | Contenido |
|---|---|
| **Cabecera** | Nombre · **propósito en una frase (el del contrato)** · estado · enlaces a código y a Figma · **enlace de referencia** |
| **1. Propiedades** | **Una matriz** de variantes y estados, con las **etiquetas de propiedad con el nombre exacto del código** |
| **2. Anatomía** | Partes (mismos nombres que en código y Figma), márgenes, relleno y dimensiones |
| **3. Comportamiento** | Guías de uso en casos concretos: **qué hacer y qué no** (tarjetas *hacer / no hacer*, y una de *dudoso*), buenas prácticas de contenido (textos cortos, verbos) |
| **4. Aplicación** | Dónde se coloca en pantalla, con **ejemplos reales** |
| **Accesibilidad** | Tabla-lista de control (sección 8) |
| **Contacto** | Canal de dudas y de contribución |

Reglas:
- **Muestra el componente real,** no una captura: en Figma, **instancias**; en HTML, el propio componente. Así la página se actualiza sola.
- **El componente solo se muestra una vez** (una matriz): las propiedades booleanas se activan en el panel, no se despliegan como columnas (se leen como variantes que no existen). *(Regla de Helix para sus páginas de Figma.)*
- **Un componente compuesto** (una tabla) o de **superposición** (un modal) **no tiene la «matriz única»**: documenta sus piezas y su comportamiento (ver 01).
- La **primera página** es la plantilla; las demás se replican **tras** el visto bueno.
- Plantilla en Markdown (propia):

```markdown
# <Componente>   · estado: <borrador|beta|estable> · [código] [Figma] [referencia]
> <Propósito en una frase — el mismo del contrato>

## Propiedades        (matriz variante × tamaño × estado; etiquetas = nombres del código)
## Anatomía           (partes, márgenes, relleno, dimensiones)
## Comportamiento     ✔ Hacer · ✘ No hacer · ? Dudoso · contenido
## Aplicación         (dónde va; ejemplos reales)
## Accesibilidad      (lista de control)
## Contacto           (canal, cómo contribuir)
```

## 5. Documentar dentro de Figma (kit de documentación)

Dos kits de la comunidad coinciden en lo esencial; **se adapta la idea, no su convención de nombres**:
- **Piezas:** marcadores de **márgenes, relleno y dimensión**, **flechas de flujo**, **estado** (hecho · en curso · obsoleto · en revisión), **etiquetas de referencia** (16 tipos de enlace: gestores de tareas, documentación, código, Figma, Drive…), **ejemplos** (*hacer / no hacer / dudoso*), **notas** (añadir · cambiar · cambio hecho · revisar) y una **portada** con proyecto, categoría, estado, personas y etiqueta.
- **Componentes base ocultos** con un prefijo que los esconde (un punto inicial) y propiedades de la ficha (`Type`: componente o base; `Deprecated`; `Old version`).
- **Lo que no se sigue:** el kit usa **variantes «yes/no»** y nombres con flechas y espacios; **va contra la regla de paridad** con el código (booleanos reales, nombres sin adornos): no la copies.
- **En Helix:** cada página de componente lleva **una tarjeta** con su nombre, su **propósito** (el mismo del contrato) y la tabla de variantes; el orden de las páginas es **alfabético**. *Estilo de un sistema, no regla.* Detalle: referencia 05.

## 6. Página «Acerca de» del sistema

Una página con **qué es** y **qué hay**: cifras **por capa y con fecha** (ver 02), qué vive en cada «casa» (el archivo de Figma y el repositorio), la **regla de la fuente de verdad** del proyecto y qué se ofrece a los agentes. En el archivo de Helix, el texto dice «33 componentes» y la biblioteca de Figma tiene 28 páginas de componentes más íconos: **una cifra del código no es una cifra del archivo**; **cada número lleva su origen**.

## 7. Tabla de estado

- Columnas: **estado · repositorio · Figma · documentación** (el orden es el recomendado). Para stakeholders, **solo las columnas útiles**; las de mantenimiento interno, ocultas.
- Valores del video: «sano» y «sin documentar». **No dice cuándo se pasa de uno a otro:** define tú los criterios.
- **Versión generada** (Helix): una página de estado con una columna ✓/✗ por criterio automático y la de Figma, y al pasar sobre una ✗ se ve **qué falta**; sale de un archivo calculado. Detalle: referencia 07.

## 8. Lista de control por componente

Base: la plantilla de la comunidad (482 textos leídos), reexpresada. Cada bloque es una sección de la lista:

| Bloque | Qué comprueba |
|---|---|
| **Variantes** | Tamaño, tipo, estado (normal, hover, activo, foco, deshabilitado), cantidad, retroalimentación (info, error, aviso, éxito), eje y tema (claro y oscuro) |
| **Tokens** | Color (contenido, superficie, borde), tipografía, espacio, borde, radio, ancho, taxonomía y sombras; nombres de componente, variante y capa; anatomía |
| **Contenido (QA)** | Caracteres especiales; líneas largas **sin** espacios y **con** espacios; nombres largos; estado vacío; datos **perfectos** y datos **«feos»** |
| **Convenciones** | Todos los estados y variantes cubiertos; **nombres en sincronía con el código**; tokenización completa y reutilizable; control de versiones |
| **Pruebas** | Revisión por una persona de desarrollo; responsive; resistencia a redimensionado extremo; comportamiento; pruebas funcionales y de interacción; **varios navegadores** |
| **Accesibilidad** | Ver abajo |
| **Otros** | Capas con nombre según las guías; descripción del componente; soporte de temas; soporte de **internacionalización** |

**Accesibilidad (cada punto con su criterio WCAG 2.2, contrastado):**

| Punto de la lista | Criterio | Nivel |
|---|---|---|
| El color no debe ser **el único** indicador de una acción o información | 1.4.1 Use of Color | A |
| Contraste 4,5:1 (texto normal) y 3:1 (texto grande) | 1.4.3 Contrast (Minimum) | AA |
| Contraste 3:1 de objetos que no son texto | 1.4.11 Non-text Contrast | AA |
| Foco de teclado visible | 2.4.7 Focus Visible | AA |
| Alternativas de texto para el contenido no textual | 1.1.1 Non-text Content | A |
| Separar el texto esencial de las imágenes (sin imágenes de texto) | 1.4.5 Images of Text | AA |
| Encabezados y etiquetas descriptivos | 2.4.6 Headings and Labels | AA |
| Probar con un **simulador de daltonismo** | — (práctica recomendada, **no** es un criterio) | — |

*La plantilla original escribe «4:5:1»: es un error tipográfico de la fuente (el umbral es 4,5:1).* Esta lista es **manual**: es la base del verificador (07).

## 9. Handoff diseño → desarrollo *(definición propia, inferencia, sin probar)*

**Ninguna fuente lo define:** el video de documentación dice que desarrollo solo **consulta** el enlace al repositorio, la lista de propiedades de Figma junto a la del código, la fecha de actualización y las versiones. La propuesta de la skill (decisión #8 de Guille, marcada como inferencia hasta probarla en `caso-ds-01`):

| Se entrega | Qué es |
|---|---|
| 1. **Contrato** | Mínimo (`website`) o completo (`app`, `sistema compartido`) — ver 01 |
| 2. **Página de componente** | Con propiedades, anatomía, comportamiento y ejemplos reales |
| 3. **Tabla de nombres Figma ↔ código** | La de la referencia 03; en una migración, una tabla **«antes → después»** por token o propiedad |
| 4. **Valores por defecto y estados iguales** en ambos lados | Se **comparan**, no se suponen (en Helix difería `size`) |
| 5. **Versión y fecha** del componente | Y enlace a los cambios |
| 6. **Canal de consulta** | A quién preguntar y cómo contribuir |

- **Pregunta al equipo de desarrollo en qué formato prefiere recibirlo** (una anécdota de la fuente: se entregó una tabla de cambios en dos formatos, captura lado a lado y tabla en un ticket, y se preguntó cuál servía).
- En `website`, la entrega es **el componente final con sus estados** (HTML o bloque, según el stack), no un paquete de especificaciones.

## 10. Mantener la documentación al día

- **Fuentes vivas:** lo que se pueda **enlazar o generar** (cambios, tokens, estado) no se copia. *«Cero mantenimiento» es una afirmación de la autora, no una medida; depende de que Figma y el repositorio ya estén ordenados.*
- **«Existir no es estar al día»:** mide la **frescura** (¿se tocó el componente sin tocar su documentación?) con el historial del repositorio (07).
- **Una descripción, una fuente:** en Helix la tarjeta de Figma usa el `purpose` del archivo de documentación del componente (la misma frase con la que abre su página en Storybook), y esa frase **coincide con la del contrato de Button**; que el contrato **comparta físicamente** esa fuente **no se verificó**. La regla para tu proyecto: **no se escribe un segundo texto**.
- **Avisos de cambios:** una página de novedades y un canal; el aviso es lo que más echaban en falta los equipos.

## 11. Publicar la documentación

La skill **prepara** y **pregunta el destino** (hosting, Google Drive —con su enlace— o Figma); nunca publica por su cuenta (ver `SKILL.md`).

**Páginas públicas de documentación: no deben indexarse** salvo que el usuario pida lo contrario. Contrastado con la documentación de Google:
- En HTML: `<meta name="robots" content="noindex">` en el `<head>`.
- Para archivos que no son HTML (PDF, imágenes): la cabecera de respuesta `X-Robots-Tag: noindex`.
- **No bloquees la URL en `robots.txt`:** si el rastreador no puede entrar, **no verá** el `noindex` y se ignora. La página debe seguir siendo rastreable.
- `noindex` **no protege el acceso**: cualquiera con el enlace la ve *(sentido común, no tomado de esa página)*. Si el contenido es sensible, hace falta autenticación.

`caso-ds-01`: la prueba (C-7) publica una página de documentación del sistema en una URL de nombre «design system», con `noindex`, **solo con tu autorización expresa en ese momento**, vía `cpanel-guillequinterot`.

## 12. Lista de revisión (la usa `auditar`)

- [ ] **Tres pilares** presentes y conectados con desarrollo.
- [ ] Documentación empezada por **puntos de dolor reales**, no por cobertura.
- [ ] **Una plantilla** de página de componente, probada con una página antes de replicar.
- [ ] **Propósito único** (contrato = página = Figma).
- [ ] Componentes **reales** en la página, no capturas; matriz **única**.
- [ ] **Do / Don't** y buenas prácticas de contenido.
- [ ] **Lista de control** con criterios WCAG con su nombre oficial.
- [ ] **Tabla de estado** con criterios definidos (y generada cuando se pueda).
- [ ] **Novedades** y canal de avisos.
- [ ] **Handoff** definido (sección 9) y **formato acordado con desarrollo**.
- [ ] Cifras con **capa y fecha**.
- [ ] Páginas públicas con **`noindex`** y sin bloqueo en `robots.txt`.
- [ ] **Biblioteca de módulos** (si se hace): referente visual en cada módulo, menú lateral, logo y colores del cliente, botón al home, acciones de copia (incluido el prompt) y enlace en el pie con `nofollow` (sección 13).

## 13. Biblioteca de módulos (la página de documentación navegable)

**Origen: petición del mantenedor (2026-10-27), probada en `caso-ds-01`; el patrón de interfaz viene de una biblioteca de módulos de su agencia. Es una decisión de producto de esta skill, no una norma.** Se genera con `scripts/generar_biblioteca.py` a partir de un manifiesto (`templates/biblioteca-manifiesto.json`); las piezas reales se extraen del propio proyecto, no se redibujan.

**Reglas de la página (aprobadas por el mantenedor):**

| # | Regla | Cómo se cumple |
|---|---|---|
| 1 | **Todo tiene un referente visual** | Cada módulo se ve: el componente real aislado (Shadow DOM, con su CSS real) o un bloque visual de datos (muestras de color, barras de escala, tarjetas de contraste, antes/después). Un hallazgo sin imagen no entra. |
| 2 | **Menú a la izquierda, tipo panel** | Menú lateral fijo con logo, buscador, grupos, estado de cada módulo (punto de color) y módulo activo según el scroll. En móvil se pliega en un cajón con botón «Menú». |
| 3 | **El logo y los colores son los del cliente** | Cambian con cada proyecto: `marca.logo_svg` y `acento`, `tinta`, `fondo` y `fuente_ui` salen del propio sitio, no de la agencia. El generador calcula un color de acento **seguro para texto** (≥ 4,5:1) y el color del texto sobre el acento. |
| 4 | **Botón para volver al home** | `meta.home_url`: aparece arriba en el menú y en la barra móvil. |
| 5 | **Acciones en cada variante** | Copiar HTML · Copiar CSS · Copiar JSON · **Copiar prompt** (reglas del sistema + contrato + HTML + CSS, con un hueco «escribe qué cambiar», para que una IA lo duplique) · Ver código (pestañas) · y, por módulo, **Ver CSS del módulo**. Solo se ofrece lo que existe. |
| 7 | **El logo de la marca es obligatorio** | Sin `marca.logo_svg` y `marca.nombre` el generador no entrega nada. El logo se pone arriba a la izquierda (menú y barra móvil) y viaja también como `logo.svg`. |
| 8 | **La entrega es una carpeta, no solo una página** | Más fácil de ubicar para el cliente (una URL, un lugar) y legible por una IA: `index.html` + `sistema.json` + `llms.txt` + `AGENTS.md` + `modulos/<id>.json` + `logo.svg`. Con la URL, una IA documenta todo y construye a partir de ahí; la página trae «Copiar prompt maestro» con esa URL. |
| 6 | **Enlace desde el sitio, sin que lo siga Google** | Botón «Design system» en el pie del sitio con `rel="nofollow"`; la página lleva `noindex, nofollow` (etiqueta y cabecera `X-Robots-Tag`). **No** se bloquea en `robots.txt`: si el rastreador no puede entrar, no ve el `noindex`. |

**Para que una IA solo necesite la URL (regla 8):** el contenido de cada variante (HTML real, CSS real con sus variables, contrato en JSON y su prompt) está en `sistema.json`; `llms.txt` sigue el formato de la propuesta (H1, cita, secciones con enlaces, «Optional») y `AGENTS.md` explica el orden de lectura y las reglas. Las vistas previas usan Shadow DOM declarativo, así que el componente está en el HTML estático aunque no corra JavaScript. Un lector que convierte la página a texto **no ve el marcado de los componentes**: por eso existe la capa de archivos.

**Qué extraer del proyecto (no inventar):** el HTML que emite el sitio (por ejemplo, la salida de la compilación), las reglas CSS cuyo selector empieza por la clase del módulo (incluidas las de `@media`), las variables que esas reglas usan y los contratos. Si un componente compone otro (una tarjeta con botón), el CSS del botón entra como dependencia o la vista previa sale rota.

**Errores reales que ya cometió la primera versión (y su regla):**
- El estilo de «código en línea» volvía ilegible el código de los paneles (fondo claro con texto claro) → el código dentro de `pre` no hereda el estilo de código en línea.
- Una tarjeta que compone un botón se veía sin botón → declarar dependencias de CSS.
- Cuatro chips en columnas estrechas se desbordaban → bloques de antes/después apilados y chips que parten línea.
- Los saltos de nivel de encabezado (`h1` → `h3`) y el texto de 10 px → niveles seguidos y mínimo de 12 px.
- El botón de cerrar el cajón móvil apuntaba al botón equivocado → seleccionar por `data-accion`, no por clase.

**Qué se verificó de la capa para IA (2026-10-27):** los 16 archivos de la entrega responden 200 en la URL real con su tipo correcto y el mismo SHA-256 que el local; se analizó el HTML estático sin ejecutar scripts (7 de 7 vistas previas con contenido); una tarjeta nueva armada solo desde `sistema.json` salió con los mismos estilos que la original; una herramienta externa de lectura de URLs listó los 11 módulos y el archivo de cada uno a partir de `llms.txt`. **No se verificó:** una IA real construyendo una página completa solo con la URL; que cada herramienta de IA respete o ignore la cabecera `noindex` al leer un archivo (la cabecera está para los buscadores, no para las IAs; si el cliente quiere que ninguna IA lea el sistema, hace falta autenticación).

**Qué se verificó (2026-10-27):** 22 variantes, 83 copias de HTML, CSS, JSON y prompt sin vacíos; el JSON de cada una se parsea; paneles de código con texto legible; menú activo según el scroll; búsqueda; cajón móvil (abre, cierra con Escape y al elegir módulo); sin desbordamiento horizontal a 320 px; contraste del texto de la página (636 elementos, 0 fallos). **No se verificó:** lector de pantalla real, otros navegadores, impresión; la vista previa no puede forzar `:hover`/`:focus` (se prueban con el ratón y Tab).

## 14. Fuentes y estado de la verificación

| Idea | Fuente | Estado |
|---|---|---|
| MVP de documentación, tabla de estado, portada, novedades, página de componente «resumen + uso» | Video de la autora sobre el MVP | Leído; **de una autora**; «cero mantenimiento» sin medir |
| Plantilla de cuatro secciones, kit de piezas, componentes base ocultos | Dos kits de la comunidad de Figma (autoría y licencia sin ver) | **Leídos por API** (estructura y textos) |
| Lista de control completa | Plantilla de la comunidad | **Leída** (texto completo) |
| Criterios WCAG de la lista | W3C | **Contrastados** (1.1.1 A, 1.4.1 A, 1.4.3 AA, 1.4.5 AA, 1.4.11 AA, 2.4.6 AA, 2.4.7 AA) |
| Tres pilares; el kit sin desarrollo no es sistema | Entrevista y conversación en un festival | Experiencia de dos personas; sin datos |
| Propósito único, página de estado, novedades, tarjeta de documentación | Helix | **Leído**; estilo de un sistema |
| Cifras de «Acerca de» frente a páginas reales | Archivo de Figma de Helix | **Observado** |
| `noindex` y `robots.txt` | Documentación de Google | **Contrastado** |
| Handoff como paquete de seis piezas | — | **Definición propia, sin probar** |
| Plantilla única mezclada; adaptación sin herramienta de terceros; documentación para `website` en HTML/WordPress/Astro | — | **Inferencia propia, sin probar** |

**Límites:** casi todo es experiencia de **una autora y dos kits**; ninguna práctica se ha medido. La parte de `website` y el handoff **no se han probado** en un sitio real (`caso-ds-01`).
