# HANDOFF — buffer-social-post

> Traspaso entre sesiones y personas: qué es la skill, cómo se instala, qué se decidió y qué se aprendió
> en cada trabajo. Estado vivo (versión, herramientas, pendientes) → `HANDSHAKE.md`.

## 1. Qué es y cuándo se usa
Cliente seguro de la API GraphQL de Buffer para crear borradores, programar y publicar posts en redes, con mesura de cuota y sin exponer la clave. Se usa cuando el usuario pide un post en redes (LinkedIn, Instagram, YouTube…) o el post que acompaña a un artículo o un video.

## 2. Instalación y dependencias
- Viene con el repo gui-skills; en cada PC se enlaza con `tools/install.ps1` / `tools/install.sh` (junction en `~/.claude/skills/buffer-social-post`).
- Solo biblioteca estándar de Python 3. Cada persona necesita **su propia clave de Buffer** (Buffer > Settings > API) guardada fuera del repo y apuntada con `BUFFER_KEY_FILE`, `BUFFER_API_KEY` o `~/.buffer-social/config.json`.

## 3. Decisiones vigentes
| Fecha | Decisión | Quién la aprobó | Por qué |
|---|---|---|---|
| 2026-10-28 | Todo es borrador por defecto; publicar exige `--confirmo` y orden explícita del dueño | Guille (prueba «con mesura») | Publicar es una acción externa y visible |
| 2026-10-28 | Tope de 8 solicitudes por ejecución | Claude Code | Cuota compartida por cuenta (plan gratuito: 150/15 min, 600/24 h, hasta 3.000/30 días) |
| 2026-10-28 | Medios solo por URL pública https directa (la API no sube archivos) | Documentación de Buffer | Buffer descarga al publicar |

## 4. Registro de trabajos

> Una entrada por trabajo terminado o implementado y aprobado. Solo se agregan entradas al final; las correcciones van como entrada nueva. Se escribe con `tools/log_job.py`.

<!-- registro:inicio -->
### 2026-10-28 — creación de la skill (caso interno)
- **Hecho:** lectura de la documentación oficial (autenticación, primer post, programación, medios, límites de caracteres, errores, límites de la API); consultas de solo lectura con una clave real (organización, canales, esquema); creación y eliminación de borradores de texto en LinkedIn; cliente `buffer_api.py` con 16 pruebas sin red.
- **Salió bien:** el flujo borrador → listar → eliminar funciona de punta a punta; el esquema se confirmó por introspección (`CreatePostInput` exige `needsApproval`; la documentación no lo mostraba).
- **Salió mal / lecciones:** (1) la salida por redirección en Windows salía en cp1252: se fuerza UTF-8; (2) `read` de bash con un archivo sin salto final devuelve error y corta cadenas `&&`; (3) corrección: el tipo de metadatos de LinkedIn sí existía (`LinkedInPostMetadataInput`); mi script de introspección se rompió al imprimir un tipo de lista y lo interpreté mal. Lección: ante un fallo, leer el error antes de concluir que algo no existe.

### 2026-10-28 — primera publicación real con imagen (caso interno)
- **Pedido del dueño:** revisar la documentación (incluido el explorador), subir imágenes y videos a su hosting y hacer la prueba con imagen publicada de inmediato.
- **Hecho:** (1) el explorador web exige teclear la clave en un formulario: no se usó; se obtuvo el esquema por introspección (1 solicitud): `ImageAssetInput` (`url!`, `thumbnailUrl`, `metadata`), `VideoAssetInput`, `DocumentAssetInput` (`url!`, `thumbnailUrl!`, `title!`), metadatos de LinkedIn/Instagram/YouTube; (2) imagen de la tarjeta de un artículo publicado, convertida a JPG (LinkedIn no admite WebP de forma oficial) y subida por SCP al hosting con comprobación SHA-256 a `assets/social/<slug>/card.jpg`; (3) post de texto + imagen + enlace al artículo publicado con `ahora --confirmo`; (4) comprobado `sent`.
- **Salió bien:** URL pública directa aceptada por Buffer a la primera; 5 solicitudes en total.
### 2026-10-28 — carrusel de Instagram publicado (caso interno)
- **Pedido del dueño:** publicar en Instagram el carrusel de prueba de la línea gráfica. **Hecho:** se revisaron las 4 láminas (1080×1350) y sus afirmaciones contra el artículo (las 6 decisiones coinciden; el dato de 2,5 s coincide con web.dev); se convirtieron a JPG (calidad 90, 150–220 KB) y se subieron por SCP a `assets/social/<slug>/carrusel/` con SHA-256 verificado y respuesta 200 `image/jpeg`; se añadieron al script los metadatos de Instagram (`--ig-tipo`, `--primer-comentario`) con 3 pruebas nuevas; publicado con `ahora --confirmo` (4 imágenes) y comprobado `sent`.
- **Texto del post (Instagram):** la frase inicial del artículo, una invitación a deslizar para las 6 decisiones y el dato de Core Web Vitals, y la mención del sitio sin enlace (en Instagram no es clicable) con 4 hashtags. No se afirmó nada que no esté en el artículo (no se dijo «enlace en la bio» porque no consta).
### 2026-10-28 — regla de limpieza: «una vez publicado se procede a borrar del cPanel»
- **Pedido del dueño:** dejar escrito en la skill que, publicado el post, los medios se borran del cPanel (espacio limitado). **Hecho:** nuevo comando `buffer_api.py limpiar` (exige `--slug`, `--post`, `--org`, `--canal`; consulta el estado del post y **se niega si no es `sent`**; borra solo `assets/social/<slug>/` por SSH; comprueba 404), paso 7 del flujo y regla 4 en `SKILL.md`, 22 pruebas sin red (incluye slugs maliciosos) y prueba en vivo (rechazo con borrador y borrado con post `sent`). Configuración del hosting: `BUFFER_MEDIA_*`, `~/.buffer-social/config.json` o `canva_tmp_*` del dueño.
- **Lección:** las pruebas «sin red» llamaban a una URL real (HEAD); al borrarse las imágenes fallaron. Ahora una variable de entorno (`BUFFER_TEST_SIN_RED`) desactiva esa comprobación solo en simulación.
- **Convención de alojamiento (propuesta):** `assets/social/<slug-del-articulo>/<pieza>.jpg|png|pdf|mp4` en el hosting del dueño; archivos con nombre estable, sin redirecciones ni firmas.
- **Regla candidata (1 caso, no es regla aún):** pedir siempre introspección del tipo antes de usar un campo que la documentación no muestra.

### 2026-10-28 · banco-pruebas-buffer-api · guille

- **Qué se hizo:** Skill nueva buffer-social-post: cliente seguro de la API GraphQL de Buffer (borrador por defecto, --confirmo para publicar, tope de 8 solicitudes, clave nunca impresa), documentacion leida y verificada en vivo: canales, borrador, post con imagen en LinkedIn, carrusel de 4 imagenes en Instagram, eliminar y limpiar medios del hosting tras 'sent'. 22 pruebas sin red.
- **Salió bien:** El flujo borrador -> publicar -> comprobar -> limpiar funciona de punta a punta; la introspeccion del esquema encontro campos que la documentacion no mostraba (needsApproval, metadatos obligatorios de Instagram).
- **Salió mal / incidencia:** Una prueba 'sin red' dependia de una URL real y fallo al borrarse la imagen; la salida redirigida en Windows salia en cp1252; un fallo de introspeccion se interpreto mal al principio.
- **Regla candidata:** Los medios alojados para publicar en redes se borran del hosting tras 'sent' (con comando que se niega antes de ese estado).
- **Herramientas:** Python 3 estandar; API GraphQL de Buffer; SSH al hosting del usuario

<!-- registro:fin -->

## 5. Reglas candidatas (sin aprobar)

| Regla | Visto en (casos) | Estado |
|---|---|---|
| Ante un campo que la documentación no muestra, usar introspección del tipo antes de enviarlo | banco-pruebas-buffer-api | candidata |
| Los medios alojados para publicar en redes se borran del hosting tras 'sent' (con comando que se niega antes de ese estado). | banco-pruebas-buffer-api | candidata |
