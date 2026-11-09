# Línea de producción de artículos de blog (formato probado)

> Origen: caso `caso-migracion-01` (2026-11), 16 artículos convertidos o nuevos con este mismo formato, video, PDF, carrusel y publicación en redes. Se pidió el 2026-11-08 que **cuando el usuario pida artículos de blog en otra tarea salgan muy parecidos**: mismo esqueleto, mismas puertas, mismos componentes, mismo orden de trabajo. Lo que cambia entre proyectos son los **parámetros** (sección 1), no el método.
> Se usa junto con [blog-article-writing-rules.md](blog-article-writing-rules.md) (reglas de redacción), [editorial-quality-gates.md](editorial-quality-gates.md), la puerta anti-slop (`contenido-sin-slop`) y [schema-markup-for-ai-citation.md](schema-markup-for-ai-citation.md).

## 0. Reglas que no se negocian

1. **Schema: un solo bloque JSON-LD con `@graph` por página. OBLIGATORIO** (sección 5). Se genera desde lo visible; nunca se escribe a mano ni en bloques sueltos por tipo.
2. **Nada en vivo sin aprobación escrita** del dueño del sitio (publicar, cambiar contenido, redirecciones, plantillas, robots, sitemap). Antes de cada cambio: respaldo de la entrada original y forma de revertir anotadas en el registro de aprobaciones.
3. **Verificar en vivo sin parámetros de caché** (sin `?cb=`) después de purgar la caché por el mecanismo que funcione en ese sitio (API del constructor, no la línea de comandos si no purga).
4. **Cada dato con su fuente abierta y leída**; lo que no se pueda verificar no se escribe. Cada afirmación de producto sale de la ficha oficial o del banco de material propio del cliente.
5. **Pasar `contenido-sin-slop`** antes de publicar (propósito, sustancia propia, procedencia, revisión humana). Si ese mes no hay nada propio que decir, no se publica.
6. **Nada de redes ni de video sin orden expresa**: publicar o programar exige la orden del dueño para ese texto, canal y hora.

## 1. Parámetros por proyecto (se fijan una vez en un `config.json` del proyecto)

| Parámetro | Valor de referencia (caso de origen) | Se adapta según |
|---|---|---|
| Marca escrita y variantes prohibidas | una grafía; las demás bloquean | guía de marca |
| Autor firmante (persona real, cargo, usuario del CMS) | el firmante visible, con fecha de actualización | E-E-A-T; su permiso |
| Palabras | 3.000 a 4.500 para artículos nuevos; mínimo 1.700 al convertir uno antiguo | intención y competencia |
| Metatítulo / metadescripción | ≤ 59 / ≤ 140 caracteres | SERP |
| H2 / FAQ | ≥ 6 H2; 3 a 6 preguntas | tema |
| Enlaces | ≥ 4 internos y ≥ 1 a un producto o servicio; ≥ 2 fuentes externas | arquitectura del sitio |
| Imagen destacada | WebP ≤ 100 KB, proporción baja (p. ej. 1600×640) y texto alternativo | plantilla del tema |
| Sector sensible (YMYL) | frases de promesa solo en contexto preventivo; aviso de riesgo y de «no es asesoría» dentro del cuerpo; enlace a la página legal | regulación |
| Estilo de enlaces | un color de marca, subrayados, `rel` según el caso (`sponsored` en afiliados, `noopener` en externos) | tema oscuro o claro |

## 2. Carpeta del lote (una por artículo)

`lotes/<id>/` con: `articulo.html` (solo el cuerpo; **sin H1**, lo pone el CMS), `meta.json` (`post_id`, `slug`, `titulo`, `seo_title`, `seo_desc`, `focus`, `autor`, `imagen`, `imagen_alt`, `pdf`, `fuentes`, `dato_propio`, y `video` cuando exista), la imagen WebP, el PDF, las láminas del carrusel, los textos de redes, `publicacion.json` (ids de medios y enlace en vivo) y las copias `*.ANTES-*` de cada cambio. Una sola persona o IA por mes sobre el mismo lote.

## 3. Esqueleto del artículo (orden obligatorio)

Video (si existe) → firma («Por [autor], [cargo] · Actualizado el … · Lectura de unos N minutos») → **tabla de contenido** (enlaces a cada H2; los H2 llevan `id`) → **La respuesta corta** (H2: respuesta con la palabra clave en el primer párrafo, por qué importa y una tabla «de un vistazo») → **Para quién es y qué no resuelve** (límites explícitos) → **Núcleo** (H2/H3 con criterio, ejemplo y, si ayuda, tabla) → banner de producto a mitad → **Tabla de producto** solo con datos de fichas oficiales y la nota «no describe resultados» → **Los datos que respaldan esta guía** (tabla dato · fuente enlazada con fecha · qué significa; decir si es de otro país o antiguo) → **Qué hacer esta semana** (5 a 7 pasos + visor del PDF) → **Preguntas frecuentes** (H3 que terminan en «?»; respuestas de 30 a 80 palabras) → **Para cerrar** + caja de aviso de riesgo + **Fuentes consultadas** → **bloque de schema único** (sección 5).

Reglas de forma: comillas rectas dobles; título con número real y año cuando es lista; tablas con estilos en línea (no depender del CSS del tema); sin la raya larga U+2014; sin relleno; cada cifra con fuente.

## 4. Componentes fijos (funciones reutilizables)

- **Tabla de contenido** en dos columnas con anclas.
- **Banner de producto** a mitad del artículo (tarjetas con una línea por producto, sin cifras de rendimiento, con la nota de riesgo).
- **Visor del PDF** (abanico con las 3 páginas + botón de descarga; el enlace abre en pestaña nueva con `rel="noopener"`).
- **Bloque de video** debajo de la imagen principal (embed sin cookies, 16:9, carga diferida). Sin ID de video no se muestra nada en público; en la copia de vista previa se ve un recuadro punteado que **nunca** puede llegar al sitio en vivo.
- **Caja de aviso de riesgo** y bloque de fuentes.

## 5. Schema: un solo bloque con `@graph` (OBLIGATORIO)

**Regla:** cada página tiene **exactamente un** `<script type="application/ld+json">` con `@graph`; todos los nodos con `@id` único y conectados por referencias `{"@id": …}`; ningún bloque suelto por tipo (ni FAQPage por un lado ni VideoObject por otro).

**Cómo se cumple en un CMS con plugin de SEO** (WordPress + Rank Math u otro que ya emita su `@graph`):
1. **El schema del artículo es un dato derivado.** Una función lo arma desde lo que el lector ve: `FAQPage` desde las preguntas visibles y `VideoObject` desde el video incrustado (nunca a mano). Cada nodo lleva `@id` = `{url}#faq`, `{url}#video` y `isPartOf` → `{url}#webpage` (el WebPage que emite el plugin de SEO). El plugin ya emite Organization, WebSite, WebPage, BreadcrumbList, Person y Article: **no se duplican** en el cuerpo.
2. **Se regenera siempre al publicar** (idempotente), así que nunca queda desfasado de las preguntas o del video.
3. **La página final queda con un solo script** fundiendo esos nodos dentro del `@graph` del plugin de SEO y quitando el bloque del cuerpo. Fragmento de referencia, sin marca: [`assets/blog-kit/wordpress-schema-unico.php`](../assets/blog-kit/wordpress-schema-unico.php) (filtro `rank_math/json_ld` y `the_content`). **Instalarlo en el sitio es un cambio en vivo: pide aprobación escrita.** Mientras no esté instalado, la puerta de la página en vivo avisa «hay N bloques»; no se declara cumplido.
4. Si el sitio **no** tiene plugin de SEO que emita schema, el artículo lleva un único bloque propio que incluye también Organization, WebSite, WebPage, BreadcrumbList, Person y Article.

**Puertas (las dos):**
- Fuente del artículo (antes de publicar): `python scripts/check_schema_single_block.py lotes/<id>/articulo.html --cuerpo` (y la puerta del proyecto: 1 bloque, `@graph`, `@id` únicos, FAQPage = las mismas preguntas que se ven, VideoObject = el video incrustado, sin VideoObject si no hay video).
- Página en vivo (después de publicar): `python scripts/check_schema_single_block.py https://…/articulo/` debe dar **PASA** (1 bloque, referencias resueltas, sin Organization/WebPage duplicados).

Implementación de referencia lista para copiar: [`assets/blog-kit/schema_unico.py`](../assets/blog-kit/schema_unico.py).

## 6. Puertas de calidad (mecánicas; no sustituyen la revisión de fondo)

**Bloquean:** extensión · sin H1 en el cuerpo · H2 suficientes · FAQ visible · sin la raya larga · metatítulo y metadescripción · slug válido · marca bien escrita · sin el dominio anterior (si hubo migración) · frases de promesa solo en contexto preventivo · aviso de riesgo dentro del cuerpo y enlace a la página legal · enlaces internos y a producto · afiliados con `rel="sponsored"` · PDF en pestaña nueva · tabla de contenido · sin recuadro de vista previa · enlaces internos que responden 200 · imagen WebP ≤ 100 KB con texto alternativo · `fuentes` en `meta.json` · **las cinco reglas de schema de la sección 5**.
**Avisan:** palabra clave en las primeras ~250 palabras y en el metatítulo · fuentes externas ≥ 2 · enlaces externos que no responden (algunos sitios bloquean a los bots: confirmar a mano en un navegador antes de quitar un enlace) · dato propio declarado.
Antes de decir «pasa», comprobar que un aviso **ya existía sin tu cambio** (correr la puerta sobre la copia anterior) en vez de suponerlo.

## 7. Flujo y estados (cada paso se puede repetir sin efectos dobles)

`datos` (1 a 3 datos propios del cliente) → `borrador` (articulo.html + meta.json) → `anti-slop` → `assets` (imagen, PDF, láminas) → `preparado` (subir medios al CMS; reemplazar marcadores del PDF y de medios) → copia en borrador para vista previa → **aprobación escrita** → `aplicado` (respaldo automático de la entrada original y del SEO anterior, actualización, purga, verificación en vivo: 200, 1 H1, FAQ, canonical propio, sin noindex, imagen y PDF presentes, **bloques JSON-LD en vivo**) → `video` (el ID se añade después; la entrada se reconstruye y se vuelve a aplicar) → `redes` → `cerrado` (registro y siguiente paso).
Un artículo nuevo al mes sin autorización extra; las redirecciones 301 y las despublicaciones siempre con aprobación.

## 8. Derivados del artículo (mismo mensaje, formato propio)

- **PDF de apoyo:** 3 páginas, solo contenido del artículo, casillas, aviso de riesgo.
- **Carrusel:** 8 láminas 1080×1350 (portada, 5 o 6 ideas, aviso de riesgo, cierre con una sola llamada a la acción), con control automático de solapes.
- **Video:** guion → voz → palabras con tiempos → composición → revisión. **Horizontal 16:9** para YouTube y **vertical 1080×1920 recompuesto** (no un recorte del horizontal) para Shorts, Reels y TikTok, con la misma voz y música. Zona segura vertical: contenido entre y=250 y y=1300, subtítulos en 1330–1480. Volumen −16…−14 LUFS con pico ≤ −1 dBTP (normalizar si el render sale más bajo). Marca de contenido hecho con IA si hay voz sintética.
- **Redes:** un texto propio por red, aviso de riesgo, una sola llamada a la acción; Instagram y TikTok no enlazan («enlace en la bio»). Publicar con `buffer-social-post`: un video por día en cada canal, sin solapar lo ya programado (listar la cola antes de programar), medios temporales borrados después de `sent`.

## 9. Lo que no se hace

No inventar datos, citas, casos ni autores · no cambiar a mano el schema en el cuerpo · no tocar plantillas, redirecciones, robots, sitemap ni textos legales sin aprobación · no copiar cifras de un cliente a otro · no dejar claves en archivos del lote · no declarar «verificado» sin haber corrido la puerta.
