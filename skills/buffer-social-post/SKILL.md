---
name: buffer-social-post
description: Publicar y programar posts en redes sociales (LinkedIn, Instagram, YouTube, Facebook, X, Threads y más) a través de la API GraphQL de Buffer, de forma segura y con mesura. Usar cuando el usuario pida crear un borrador, programar, encolar o publicar un post en Buffer, listar canales o posts, eliminar un borrador, adjuntar imágenes, videos o un PDF (carrusel de LinkedIn) a un post, o preparar el post de redes que acompaña a un artículo de blog. Por defecto todo queda como BORRADOR; publicar exige confirmación explícita del dueño de la cuenta. Nunca imprime ni guarda la clave de API.
---

# Buffer — publicar posts en redes con la API

## Protocolo gui-skills (obligatorio)

Esta skill vive en el repo **gui-skills** y sigue [`shared/protocolo-skill.md`](../../shared/protocolo-skill.md):

1. **Paso 0 — cada vez que uses la skill:** corre `python <repo>/tools/check_update.py --quiet --pull`.
   `ACTUALIZADA n` → díselo al usuario en una línea y **vuelve a leer este `SKILL.md`** antes de seguir;
   `CAMBIOS_LOCALES` → avisa y no actualices; `SIN_RED` / `SIN_CREDENCIAL` → sigue con la copia local y dilo.
   Si avisa de aportes sin publicar, corre `python <repo>/tools/publish_job.py --reintentar` (preaprobado).
   Luego lee `HANDSHAKE.md` y el "Registro de trabajos" de `HANDOFF.md`.
2. **Privacidad:** en el repo los clientes solo se nombran con un código `caso-<tipo>-<NN>`; nunca
   nombres, marcas, dominios, correos, rutas personales ni credenciales. **Aquí además: ningún identificador de
   organización, canal o post de Buffer ni ninguna clave de API se escribe en el repo.**
3. **Paso final — obligatorio y preaprobado** (trabajo terminado y aprobado por el usuario; no pidas permiso):
   (1) `python <repo>/tools/log_job.py --skill buffer-social-post ...` (qué se hizo, qué salió bien, qué salió mal,
   incidencias); (2) actualiza `HANDSHAKE.md` si cambió el estado vivo; (3) publica con
   `python <repo>/tools/publish_job.py --tema <caso-o-tema>`; (4) dile al usuario el resultado
   (`PR_CREADO <url>` / `PUBLICADO <url>` / `PENDIENTE` / `BLOQUEADO`). Obsidian es opcional.

`<repo>` = `repo_path` de `~/.gui-skills/config.json`, o dos carpetas arriba de esta skill.

## Reglas que no se saltan

1. **Borrador por defecto.** `scripts/buffer_api.py borrador` crea el post con `saveToDraft`; no se publica nada. Programar (`programar`), encolar (`cola`) o publicar ya (`ahora`) exigen `--confirmo`, y **solo se usa cuando el dueño de la cuenta lo dijo en esta conversación** para ese texto y ese canal. Enseña antes el texto final, el canal y la hora.
2. **La clave no se imprime, no se copia y no se guarda.** Se lee de `BUFFER_API_KEY`, de `BUFFER_KEY_FILE` (primera línea del archivo), de `--key-file` o de `~/.buffer-social/config.json` (`{"api_key_file": "ruta"}`). Si falta, el script dice `SIN_CLAVE`; no la pidas por chat: pide que la guarde en un archivo fuera del repo (con `.gitignore` si está dentro de un repo). Una clave por cuenta, sin alcance por organización: si se filtra, se rota en Buffer > Settings > API.
3. **Mesura con la cuota.** Los límites son por cuenta y comparten todas las claves. El plan gratuito (según la documentación) permite 150 solicitudes cada 15 minutos, 600 cada 24 horas y 1.000 cada 30 días por canal (hasta 3.000). Una prueba completa gasta 3–5 solicitudes. El script corta a las 8 por ejecución (`--max-solicitudes`) y respeta `Retry-After` una vez. Nunca hagas bucles de consulta.
4. **Medios: se suben, se publican y se BORRAN.** Alojar en `assets/social/<slug>/` del hosting del dueño; **una vez publicado (`sent`) se procede a borrarlos del cPanel con `limpiar`** (paso 7 del flujo). URL pública, HTTPS, directa y estable mientras dura la publicación. La API **no sube archivos**; Buffer los descarga al publicar. Drive, Dropbox y enlaces firmados que caducan no sirven. El script comprueba la URL antes de enviar. Un PDF (carrusel de LinkedIn) exige `--miniatura` (imagen) y `--titulo`.
5. **No inventes datos del usuario** (canales, IDs, textos). Primero `canales`, después actuar.
6. **Antes de publicar contenido hecho con IA, pasa la puerta `contenido-sin-slop`.**

## Flujo estándar

1. `python scripts/buffer_api.py canales` → organizaciones y canales (servicio, si está desconectado o bloqueado). 2 solicitudes.
2. Redactar el post respetando el límite del canal (`references/02-redes-y-limites.md`). El script valida el largo con el conteo de Buffer (UTF-16; en LinkedIn cada URL cuenta 24; en Instagram cada salto de línea cuenta 2) si pasas `--servicio`.
3. `... --simular borrador --canal <id> --texto "..." --servicio linkedin` → ver la petición exacta sin gastar cuota.
4. `... borrador --canal <id> --texto "..." --servicio linkedin` → crea el borrador y devuelve el `id` y el estado `draft`.
5. El dueño revisa en Buffer. Solo con su orden explícita: `programar --cuando 2026-11-03T15:00:00.000Z --confirmo` (ISO 8601 en UTC), `cola --confirmo` (siguiente hueco del horario) o `ahora --confirmo`.
6. `listar --org <id> --canal <id>` para comprobar el estado; `eliminar --post <id> --confirmo` para borrar un borrador.
7. **Una vez publicado, se procede a borrar del cPanel (obligatorio, sin pedir permiso):** cuando el post figura `sent` (Buffer ya subió las imágenes a la red social), ejecuta `python scripts/buffer_api.py limpiar --slug <slug> --post <id> --org <org> --canal <canal> --url <url-de-un-medio>`. El comando comprueba que el post esté `sent` (si no, se niega y no borra nada), borra la carpeta `assets/social/<slug>/` del hosting del dueño por SSH y comprueba que la URL da 404. Nunca borres antes de `sent` (Buffer descarga el medio al publicar; en un post programado, espera a que se envíe). Solo toca esa carpeta (el `slug` solo admite minúsculas, números y guiones). Evita llenar el espacio del hosting. Es regla del dueño (2026-10-28). El hosting se toma de `BUFFER_MEDIA_HOST/PORT/USER/KEY/DOMAIN`, de `"hosting"` en `~/.buffer-social/config.json` o, en el PC del dueño, de las claves `canva_tmp_*` de `~/.gui-skills/config.json` (mismo hosting).

Con imagen: `--imagen https://…/foto.webp` (repetible). Con PDF: `--documento https://…/carrusel.pdf --miniatura https://…/portada.jpg --titulo "Título"`. Con video: `--video https://…/clip.mp4`.

## Para el blog de guillequinterot.com (uso previsto)

- Cada artículo semanal puede llevar un post de LinkedIn (texto + enlace al artículo) y un carrusel (PDF de láminas 1080×1350). Los archivos pueden alojarse en el propio sitio (URL pública y estable) o en otro host con enlace directo.
- Hasta que el usuario lo autorice de forma permanente, el flujo es: **borrador en Buffer → revisión del dueño → programar con su orden**.

## Qué está verificado y qué no

Ver `HANDSHAKE.md`. Resumen: verificados en vivo con una cuenta real el listado de canales, la creación, el listado y la eliminación de borradores, y **una publicación inmediata (`ahora`) de texto + imagen JPG en LinkedIn** (estado `sent`). **Sin probar:** video, documento (PDF), programar, encolar y los metadatos por red (los tipos de entrada están confirmados, el script aún no los envía). No afirmes que funcionan hasta probarlos con una sola publicación de prueba que el dueño autorice.

**Carrusel de Instagram:** `ahora --servicio instagram --texto "…" --imagen URL1 --imagen URL2 …` (hasta lo que admita Instagram; probado con 4 JPG de 1080×1350). La skill añade sola `metadata.instagram` (`type: post`, `shouldShareToFeed: true`, obligatorios). Instagram: los enlaces del texto no son clicables (mencionar el sitio sin enlace) y cada salto de línea cuenta 2 caracteres. Opciones: `--ig-tipo reel|story`, `--primer-comentario` (LinkedIn e Instagram).

**Imágenes en LinkedIn: usa JPG o PNG**, no WebP (LinkedIn no lo admite oficialmente). Aloja el archivo en una URL pública estable del hosting del dueño (convención: `assets/social/<slug>/<pieza>.jpg`), súbelo con la skill del hosting del dueño (p. ej. `cpanel-guillequinterot`) y comprueba que responde 200 sin redirección.

**El explorador web de Buffer pide teclear la clave en un formulario: no se usa.** Para conocer el esquema, consulta la API por introspección (`__type(name:"…")`) con el script; cuesta una solicitud.

## Referencias

- `references/01-api.md` — endpoint, autenticación, objetos, mutaciones, enumeraciones, errores.
- `references/02-redes-y-limites.md` — límites de texto por red, medios, metadatos, cuotas.
- `scripts/buffer_api.py` y `scripts/test_buffer_api.py` — cliente y pruebas sin red.
