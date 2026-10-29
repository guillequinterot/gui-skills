#!/usr/bin/env python3
"""buffer_api.py — cliente mínimo, seguro y con mesura de la API GraphQL de Buffer (https://api.buffer.com).

Solo biblioteca estándar. Reglas de seguridad incorporadas:
  * La clave NUNCA se imprime ni se escribe: se lee de BUFFER_API_KEY, de BUFFER_KEY_FILE (primera línea del archivo),
    de --key-file, o de ~/.buffer-social/config.json  {"api_key_file": "ruta"}.
  * Por defecto todo es BORRADOR (saveToDraft). Programar, encolar o publicar exige --confirmo.
  * --simular imprime la petición sin enviarla (no gasta cuota).
  * Tope de solicitudes por ejecución (--max-solicitudes, 8 por defecto) y respeto de Retry-After en 429.
Salida: JSON por pantalla, sin la clave.
"""
import argparse, json, os, re, sys, time, urllib.error, urllib.request

try:  # Windows redirige la salida en cp1252: se fuerza UTF-8 para que el JSON sea legible en cualquier sitio
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:  # noqa
    pass

API = "https://api.buffer.com"
LIMITES = {"linkedin": 3000, "instagram": 2196, "facebook": 5000, "twitter": 280, "youtube": 5000, "threads": 500, "bluesky": 300, "mastodon": 500, "pinterest": 500, "tiktok": 2200, "googlebusiness": 1500}
_contador = {"n": 0, "max": 8}


def sal(obj, code=0):
    print(json.dumps(obj, ensure_ascii=False, indent=2))
    sys.exit(code)


def cargar_clave(ruta_arg=None):
    if os.environ.get("BUFFER_API_KEY"):
        return os.environ["BUFFER_API_KEY"].strip()
    ruta = ruta_arg or os.environ.get("BUFFER_KEY_FILE")
    if not ruta:
        cfg = os.path.join(os.path.expanduser("~"), ".buffer-social", "config.json")
        if os.path.exists(cfg):
            ruta = json.load(open(cfg, encoding="utf-8")).get("api_key_file")
    if ruta and os.path.exists(ruta):
        primera = open(ruta, encoding="utf-8-sig").read().splitlines()[0].strip()
        if primera:
            return primera
    sal({"error": "SIN_CLAVE", "ayuda": "Define BUFFER_API_KEY, BUFFER_KEY_FILE (primera línea = clave), --key-file o ~/.buffer-social/config.json. La clave se crea en Buffer > Settings > API."}, 2)


def llamar(clave, query, variables=None):
    if _contador["n"] >= _contador["max"]:
        sal({"error": "TOPE_DE_SOLICITUDES", "max": _contador["max"], "ayuda": "Mesura: sube --max-solicitudes solo si es necesario."}, 3)
    for intento in (1, 2):
        _contador["n"] += 1
        req = urllib.request.Request(API, data=json.dumps({"query": query, "variables": variables or {}}).encode(),
                                     headers={"Content-Type": "application/json", "Authorization": "Bearer " + clave, "User-Agent": "gui-skills-buffer-social-post/0.1"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                h = {k.lower(): v for k, v in r.headers.items() if k.lower().startswith(("ratelimit", "retry-after"))}
                return json.loads(r.read()), h
        except urllib.error.HTTPError as e:
            if e.code == 429 and intento == 1:
                espera = min(int(e.headers.get("Retry-After", "5") or 5), 60)
                time.sleep(espera + 0.5)
                continue
            sal({"error": "HTTP_%d" % e.code, "retry_after": e.headers.get("Retry-After")}, 4)
        except urllib.error.URLError as e:
            sal({"error": "RED", "detalle": str(e.reason)}, 4)


def revisar_errores(d):
    if d.get("errors"):
        sal({"error": "GRAPHQL", "errores": [{"codigo": (x.get("extensions") or {}).get("code"), "mensaje": x.get("message")} for x in d["errors"]]}, 5)


def utf16(t):
    return len(t.encode("utf-16-le")) // 2


def contar(servicio, texto):
    """Cuenta como Buffer: UTF-16; en LinkedIn cada URL cuenta 24; en Instagram cada salto de línea cuenta 2."""
    t = texto
    if servicio == "linkedin":
        t = re.sub(r"https?://\S+", "x" * 24, t)
    n = utf16(t)
    if servicio == "instagram":
        n += t.count("\n")
    return n


def comprobar_url_publica(url):
    """Buffer descarga el archivo al publicar: debe ser https, directo, público y estable."""
    problemas = []
    if not url.lower().startswith("https://"):
        problemas.append("no es https")
    if re.search(r"drive\.google|dropbox|onedrive|1drv\.ms|X-Amz-Signature|Expires=", url, re.I):
        problemas.append("enlace de Drive/Dropbox o firmado (caduca): no sirve")
    try:
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "gui-skills-buffer-social-post/0.1"})
        with urllib.request.urlopen(req, timeout=20) as r:
            if r.status != 200:
                problemas.append("responde %s" % r.status)
            if r.url != url:
                problemas.append("redirige a otra URL (debe ser directa)")
    except Exception as e:  # noqa
        problemas.append("no se pudo abrir sin sesión: %s" % e)
    return problemas


def assets_desde_args(a):
    assets = []
    for u in (a.imagen or []):
        assets.append({"image": {"url": u}})
    if a.documento:
        if not (a.miniatura and a.titulo):
            sal({"error": "DOCUMENTO_INCOMPLETO", "ayuda": "Un documento (PDF) exige --miniatura y --titulo."}, 2)
        assets.append({"document": {"url": a.documento, "thumbnailUrl": a.miniatura, "title": a.titulo}})
    if a.video:
        if a.miniatura and not a.documento:  # la API lo rechaza (verificado 2026-10-28): las redes no aceptan miniatura propia
            sal({"error": "MINIATURA_VIDEO_NO_SOPORTADA", "ayuda": "Buffer rechaza thumbnailUrl en videos: ponla a mano en la red (p. ej. YouTube Studio)."}, 2)
        assets.append({"video": {"url": a.video}})
    for x in assets:
        for u in [v for sub in x.values() for v in ([sub.get("url"), sub.get("thumbnailUrl")] if isinstance(sub, dict) else [])]:
            if u and not os.environ.get("BUFFER_TEST_SIN_RED"):  # solo las pruebas sin red lo activan
                p = comprobar_url_publica(u)
                if p:
                    sal({"error": "MEDIA_NO_PUBLICA", "url": u, "problemas": p}, 2)
    return assets


TIPOS_INSTAGRAM = ("post", "reel", "story")


def metadatos_desde_args(a, servicio):
    """Metadatos por red (tipos confirmados por introspección el 2026-10-28)."""
    meta = {}
    if servicio == "instagram":
        tipo = a.ig_tipo or ("post" if a.imagen or a.video else None)
        if tipo is None:
            sal({"error": "INSTAGRAM_SIN_MEDIO", "ayuda": "Instagram exige imagen o video."}, 2)
        if tipo not in TIPOS_INSTAGRAM:
            sal({"error": "TIPO_INSTAGRAM", "validos": TIPOS_INSTAGRAM}, 2)
        meta["instagram"] = {"type": tipo, "shouldShareToFeed": True}
        if a.primer_comentario:
            meta["instagram"]["firstComment"] = a.primer_comentario
    elif servicio == "youtube":
        if not a.video:
            sal({"error": "YOUTUBE_SIN_VIDEO", "ayuda": "YouTube exige --video (URL pública del MP4)."}, 2)
        if not a.yt_titulo:
            sal({"error": "YOUTUBE_SIN_TITULO", "ayuda": "YouTube exige --yt-titulo (máx. 100 caracteres)."}, 2)
        if utf16(a.yt_titulo) > 100:
            sal({"error": "YOUTUBE_TITULO_LARGO", "caracteres": utf16(a.yt_titulo), "limite": 100}, 2)
        if a.primer_comentario or a.ig_tipo:
            sal({"error": "METADATO_NO_SOPORTADO", "ayuda": "--primer-comentario y --ig-tipo no aplican a YouTube."}, 2)
        meta["youtube"] = {"title": a.yt_titulo, "categoryId": a.yt_categoria, "privacy": a.yt_privacidad, "license": "youtube",
                           "embeddable": True, "madeForKids": False, "notifySubscribers": True, "isAiGenerated": bool(a.yt_ia)}
    elif servicio == "linkedin" and a.primer_comentario:
        meta["linkedin"] = {"firstComment": a.primer_comentario}
    elif a.primer_comentario or a.ig_tipo:
        sal({"error": "METADATO_NO_SOPORTADO", "ayuda": "--primer-comentario: linkedin o instagram; --ig-tipo: instagram. Pasa --servicio."}, 2)
    return meta


MUT_POST ="""mutation($input: CreatePostInput!){ createPost(input:$input){
  ... on PostActionSuccess { post { id status text dueAt channelService assets { id mimeType } } }
  ... on MutationError { message } } }"""


def cmd_canales(a, clave):
    d, h = llamar(clave, "query { account { organizations { id name } } }")
    revisar_errores(d)
    salida = []
    for o in d["data"]["account"]["organizations"]:
        c, h = llamar(clave, "query($o: OrganizationId!){ channels(input:{organizationId:$o}){ id name service isDisconnected isLocked isQueuePaused timezone } }", {"o": o["id"]})
        revisar_errores(c)
        salida.append({"organizacion": o, "canales": c["data"]["channels"]})
    sal({"organizaciones": salida, "limites": h})


def cmd_listar(a, clave):
    q = "query($o: OrganizationId!, $c: [ChannelId!], $n: Int){ posts(first:$n, input:{organizationId:$o, filter:{channelIds:$c}}){ edges{ node{ id status text dueAt channelService } } } }"
    d, h = llamar(clave, q, {"o": a.org, "c": [a.canal] if a.canal else None, "n": a.n})
    revisar_errores(d)
    posts = [e["node"] for e in d["data"]["posts"]["edges"]]
    if a.estado:
        posts = [p for p in posts if p["status"] == a.estado]
    sal({"posts": posts, "limites": h})


def cmd_crear(a, clave):
    modo = {"borrador": "addToQueue", "programar": "customScheduled", "cola": "addToQueue", "ahora": "shareNow"}[a.accion]
    if a.accion != "borrador" and not a.confirmo:
        sal({"error": "FALTA_CONFIRMACION", "ayuda": "Programar, encolar o publicar ahora exige --confirmo (decisión explícita del dueño de la cuenta).", "accion": a.accion}, 2)
    if a.accion == "programar" and not a.cuando:
        sal({"error": "FALTA_CUANDO", "ayuda": "Usa --cuando 2026-11-03T15:00:00.000Z (ISO 8601 en UTC)."}, 2)
    servicio = (a.servicio or "").lower()
    if servicio:
        n, lim = contar(servicio, a.texto), LIMITES.get(servicio)
        if lim and n > lim:
            sal({"error": "TEXTO_LARGO", "caracteres_buffer": n, "limite": lim}, 2)
    entrada = {"text": a.texto, "channelId": a.canal, "schedulingType": "automatic", "mode": modo, "needsApproval": False}
    if a.accion == "borrador":
        entrada["saveToDraft"] = True
    if a.accion == "programar":
        entrada["dueAt"] = a.cuando
    assets = assets_desde_args(a)
    if assets:
        entrada["assets"] = assets
    meta = metadatos_desde_args(a, servicio)
    if meta:
        entrada["metadata"] = meta
    if a.simular:
        sal({"simulado": True, "mutation": "createPost", "input": entrada})
    d, h = llamar(clave, MUT_POST, {"input": entrada})
    revisar_errores(d)
    r = d["data"]["createPost"]
    if "message" in r:
        sal({"error": "MUTATION_ERROR", "mensaje": r["message"], "limites": h}, 6)
    sal({"ok": True, "post": r["post"], "limites": h})


def cmd_eliminar(a, clave):
    if not a.confirmo:
        sal({"error": "FALTA_CONFIRMACION", "ayuda": "Eliminar exige --confirmo."}, 2)
    if a.simular:
        sal({"simulado": True, "mutation": "deletePost", "id": a.post})
    d, h = llamar(clave, "mutation($i: PostId!){ deletePost(input:{id:$i}){ __typename ... on MutationError { message } } }", {"i": a.post})
    revisar_errores(d)
    sal({"respuesta": d["data"], "limites": h})


def config_hosting():
    """Hosting donde el dueño aloja los medios. Orden: BUFFER_MEDIA_* → ~/.buffer-social/config.json ("hosting") → claves canva_tmp_* de ~/.gui-skills/config.json."""
    cfg = {}
    ruta = os.path.join(os.path.expanduser("~"), ".buffer-social", "config.json")
    if os.path.exists(ruta):
        cfg = json.load(open(ruta, encoding="utf-8")).get("hosting", {}) or {}
    g = os.path.join(os.path.expanduser("~"), ".gui-skills", "config.json")
    gcfg = json.load(open(g, encoding="utf-8")) if os.path.exists(g) else {}
    def pick(env, k, gk):
        return os.environ.get(env) or cfg.get(k) or gcfg.get(gk) or ""
    h = {"host": pick("BUFFER_MEDIA_HOST", "host", "canva_tmp_host"), "port": str(pick("BUFFER_MEDIA_PORT", "port", "canva_tmp_port") or 22),
         "user": pick("BUFFER_MEDIA_USER", "user", "canva_tmp_user"), "key": os.path.expanduser(pick("BUFFER_MEDIA_KEY", "key", "canva_tmp_host_key")),
         "domain": pick("BUFFER_MEDIA_DOMAIN", "domain", "canva_tmp_domain").rstrip("/")}
    h["base"] = os.environ.get("BUFFER_MEDIA_DIR") or cfg.get("base") or "public_html/assets/social"
    return h


SLUG_OK = re.compile(r"^[a-z0-9][a-z0-9\-]{2,80}$")


def cmd_limpiar(a, clave):
    """Tras `sent`, borra del hosting del dueño la carpeta <base>/<slug>/ y comprueba que ya no es pública. Regla del dueño (2026-10-28)."""
    import subprocess
    if not SLUG_OK.match(a.slug):
        sal({"error": "SLUG_INVALIDO", "ayuda": "Solo minúsculas, números y guiones (3–81 caracteres); nunca rutas."}, 2)
    h = config_hosting()
    faltan = [k for k in ("host", "user", "key", "domain") if not h[k]]
    if faltan and not a.simular:
        sal({"error": "SIN_HOSTING", "faltan": faltan, "ayuda": "Define BUFFER_MEDIA_HOST/USER/KEY/DOMAIN, o \"hosting\" en ~/.buffer-social/config.json."}, 2)
    plan = {"borrar": "%s/%s/" % (h["base"], a.slug), "comprobar_404": a.url or ["%s/%s/%s/" % (h["domain"], h["base"].split("/", 1)[-1], a.slug)]}
    if a.simular:
        sal({"simulado": True, "requiere": "el post debe figurar 'sent' en Buffer", "plan": plan})
    # 1) El post debe estar enviado: antes de eso Buffer aún puede necesitar descargar los medios.
    q = "query($o: OrganizationId!, $c: [ChannelId!], $n: Int){ posts(first:$n, input:{organizationId:$o, filter:{channelIds:$c}}){ edges{ node{ id status } } } }"
    d, _ = llamar(clave, q, {"o": a.org, "c": [a.canal], "n": 25})
    revisar_errores(d)
    estado = next((e["node"]["status"] for e in d["data"]["posts"]["edges"] if e["node"]["id"] == a.post), None)
    if estado != "sent":
        sal({"error": "NO_ENVIADO", "estado": estado, "ayuda": "No se borra nada hasta que el post figure 'sent' (Buffer descarga los medios al publicar)."}, 7)
    # 2) Borrar por SSH (el slug ya está validado: no hay caracteres especiales)
    remoto = "rm -rf ~/%s/%s && (test ! -e ~/%s/%s && echo BORRADO)" % (h["base"], a.slug, h["base"], a.slug)
    r = subprocess.run(["ssh", "-o", "BatchMode=yes", "-o", "IdentitiesOnly=yes", "-i", h["key"], "-p", h["port"], "%s@%s" % (h["user"], h["host"]), remoto],
                       capture_output=True, text=True, timeout=60)
    borrado = "BORRADO" in r.stdout
    # 3) Comprobar que ya no es público
    codigos = {}
    for u in plan["comprobar_404"]:
        try:
            urllib.request.urlopen(urllib.request.Request(u, method="HEAD", headers={"User-Agent": "gui-skills-buffer-social-post/0.1"}), timeout=20)
            codigos[u] = 200
        except urllib.error.HTTPError as e:
            codigos[u] = e.code
        except Exception as e:  # noqa
            codigos[u] = "error: %s" % e
    ok = borrado and all(c in (404, 403, 410) for c in codigos.values())
    sal({"ok": ok, "borrado_en_el_hosting": borrado, "comprobacion_publica": codigos, "post": a.post, "estado_post": estado}, 0 if ok else 8)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--key-file")
    p.add_argument("--max-solicitudes", type=int, default=8)
    p.add_argument("--simular", action="store_true")
    s = p.add_subparsers(dest="cmd", required=True)
    s.add_parser("canales")
    l = s.add_parser("listar"); l.add_argument("--org", required=True); l.add_argument("--canal"); l.add_argument("--estado"); l.add_argument("-n", type=int, default=5)
    for nombre in ("borrador", "programar", "cola", "ahora"):
        c = s.add_parser(nombre)
        c.set_defaults(accion=nombre)
        c.add_argument("--canal", required=True); c.add_argument("--texto", required=True); c.add_argument("--servicio", help="linkedin, instagram… para validar el largo")
        c.add_argument("--imagen", action="append"); c.add_argument("--documento"); c.add_argument("--miniatura"); c.add_argument("--titulo"); c.add_argument("--video")
        c.add_argument("--cuando"); c.add_argument("--confirmo", action="store_true")
        c.add_argument("--ig-tipo", choices=TIPOS_INSTAGRAM, help="Instagram: post (por defecto; varias imágenes = carrusel), reel o story")
        c.add_argument("--primer-comentario", help="LinkedIn o Instagram")
        c.add_argument("--yt-titulo", help="YouTube: título (máx. 100); el texto del post es la descripción. OJO: Buffer solo publica YouTube Shorts (≤ 3 min, 9:16 o 1:1); un video horizontal largo se rechaza")
        c.add_argument("--yt-privacidad", choices=("private", "unlisted", "public"), default="private", help="YouTube: por defecto private (seguro)")
        c.add_argument("--yt-categoria", default="27", help="YouTube: categoryId (27 = Educación)")
        c.add_argument("--yt-ia", action="store_true", help="YouTube: marca el video como contenido alterado o sintético (voz generada con IA)")
    e = s.add_parser("eliminar"); e.add_argument("--post", required=True); e.add_argument("--confirmo", action="store_true")
    lm = s.add_parser("limpiar", help="Tras 'sent': borra del hosting la carpeta de medios del post y comprueba el 404")
    lm.add_argument("--slug", required=True); lm.add_argument("--post", required=True); lm.add_argument("--org", required=True); lm.add_argument("--canal", required=True)
    lm.add_argument("--url", action="append", help="URL pública que debe dar 404 (repetible)")
    a = p.parse_args()
    _contador["max"] = a.max_solicitudes
    if a.cmd in ("borrador", "programar", "cola", "ahora"):
        if a.simular:
            return cmd_crear(a, None)
        return cmd_crear(a, cargar_clave(a.key_file))
    if a.cmd == "eliminar" and a.simular:
        return cmd_eliminar(a, None)
    if a.cmd == "limpiar" and a.simular:
        return cmd_limpiar(a, None)
    clave = cargar_clave(a.key_file)
    {"canales": cmd_canales, "listar": cmd_listar, "eliminar": cmd_eliminar, "limpiar": cmd_limpiar}[a.cmd](a, clave)


if __name__ == "__main__":
    main()
