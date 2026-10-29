"""Pruebas sin red de buffer_api.py (no usan la clave ni gastan cuota). Ejecutar: python -I test_buffer_api.py"""
import json, os, subprocess, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(AQUI, "buffer_api.py")
sys.path.insert(0, AQUI)
import buffer_api as b  # noqa: E402

fallos = 0


def ok(cond, nombre):
    global fallos
    print(("OK    " if cond else "FALLA ") + nombre)
    fallos += 0 if cond else 1


def correr(*args, env=None):
    e = dict(os.environ); e.pop("BUFFER_API_KEY", None); e.pop("BUFFER_KEY_FILE", None); e["HOME"] = e["USERPROFILE"] = AQUI
    e.update(env or {})
    r = subprocess.run([sys.executable, "-I", SCRIPT, *args], capture_output=True, text=True, env=e)
    try:
        return r.returncode, json.loads(r.stdout)
    except Exception:
        return r.returncode, {"raw": r.stdout + r.stderr}


# Conteo de caracteres como Buffer
ok(b.contar("linkedin", "hola") == 4, "conteo simple")
ok(b.contar("linkedin", "mira https://ejemplo.com/una/ruta/muy/larga/que/no/importa ya") == len("mira ") + 24 + len(" ya"), "LinkedIn: cada URL cuenta 24")
ok(b.contar("linkedin", "😀") == 2, "emoji cuenta 2 (UTF-16)")
ok(b.contar("instagram", "a\nb") == 4, "Instagram: salto de línea cuenta 2")

# Sin clave
c, d = correr("canales")
ok(c == 2 and d.get("error") == "SIN_CLAVE", "sin clave: falla de forma explícita y no imprime nada secreto")

# Borrador simulado
c, d = correr("--simular", "borrador", "--canal", "C1", "--texto", "prueba", "--servicio", "linkedin")
ok(c == 0 and d["input"]["saveToDraft"] is True and d["input"]["mode"] == "addToQueue", "borrador simulado: saveToDraft verdadero")
ok("Bearer" not in json.dumps(d), "la salida no contiene cabeceras de autenticación")

# Publicar sin confirmar
for accion in ("programar", "cola", "ahora"):
    extra = ["--cuando", "2026-11-03T15:00:00.000Z"] if accion == "programar" else []
    c, d = correr("--simular", accion, "--canal", "C1", "--texto", "x", *extra)
    ok(c == 2 and d.get("error") == "FALTA_CONFIRMACION", "'%s' exige --confirmo" % accion)
c, d = correr("--simular", "ahora", "--canal", "C1", "--texto", "x", "--confirmo")
ok(c == 0 and d["input"]["mode"] == "shareNow" and "saveToDraft" not in d["input"], "'ahora' con --confirmo usa shareNow")
c, d = correr("--simular", "programar", "--canal", "C1", "--texto", "x", "--confirmo")
ok(d.get("error") == "FALTA_CUANDO", "programar exige --cuando")

# Largo y medios
c, d = correr("--simular", "borrador", "--canal", "C1", "--texto", "a" * 3001, "--servicio", "linkedin")
ok(d.get("error") == "TEXTO_LARGO", "LinkedIn de más de 3000 caracteres se rechaza antes de enviar")
c, d = correr("--simular", "borrador", "--canal", "C1", "--texto", "x", "--imagen", "https://drive.google.com/file/d/abc/view")
ok(d.get("error") == "MEDIA_NO_PUBLICA", "enlace de Drive se rechaza")
c, d = correr("--simular", "borrador", "--canal", "C1", "--texto", "x", "--documento", "https://ejemplo.invalid/a.pdf")
ok(d.get("error") == "DOCUMENTO_INCOMPLETO", "documento sin miniatura ni título se rechaza")
# Instagram: carrusel con metadatos obligatorios
c, d = correr("--simular", "borrador", "--canal", "C1", "--texto", "x", "--servicio", "instagram", "--imagen", "https://ejemplo.invalid/1.jpg", "--imagen", "https://ejemplo.invalid/2.jpg", env={"BUFFER_TEST_SIN_RED": "1"})
ok(c == 0 and d["input"]["metadata"]["instagram"] == {"type": "post", "shouldShareToFeed": True} and len(d["input"]["assets"]) == 2, "Instagram: varias imágenes = post con type y shouldShareToFeed")
c, d = correr("--simular", "borrador", "--canal", "C1", "--texto", "x", "--servicio", "instagram")
ok(d.get("error") == "INSTAGRAM_SIN_MEDIO", "Instagram sin imagen ni video se rechaza")
c, d = correr("--simular", "borrador", "--canal", "C1", "--texto", "x", "--servicio", "linkedin", "--primer-comentario", "hola")
ok(d["input"]["metadata"] == {"linkedin": {"firstComment": "hola"}}, "LinkedIn: primer comentario en metadata")
# YouTube (metadatos confirmados por introspección el 2026-10-28)
os.environ["BUFFER_TEST_SIN_RED"] = "1"
c, d = correr("--simular", "borrador", "--canal", "C1", "--texto", "desc", "--servicio", "youtube", "--video", "https://e.com/v.mp4", "--yt-titulo", "Titulo", env={"BUFFER_TEST_SIN_RED": "1"})
yt = d.get("input", {}).get("metadata", {}).get("youtube", {})
ok(yt.get("privacy") == "private" and yt.get("categoryId") == "27" and yt.get("title") == "Titulo" and yt.get("isAiGenerated") is False, "YouTube: privado por defecto, categoría 27, sin marca de IA")
c, d = correr("--simular", "borrador", "--canal", "C1", "--texto", "desc", "--servicio", "youtube", "--video", "https://e.com/v.mp4", "--miniatura", "https://e.com/m.jpg", "--yt-titulo", "T", "--yt-privacidad", "public", "--yt-ia", env={"BUFFER_TEST_SIN_RED": "1"})
ok(d.get("error") == "MINIATURA_VIDEO_NO_SOPORTADA", "video con --miniatura se rechaza (Buffer no acepta miniatura propia)")
c, d = correr("--simular", "borrador", "--canal", "C1", "--texto", "desc", "--servicio", "youtube", "--video", "https://e.com/v.mp4", "--yt-titulo", "T", "--yt-privacidad", "public", "--yt-ia", env={"BUFFER_TEST_SIN_RED": "1"})
ok(d["input"]["assets"] == [{"video": {"url": "https://e.com/v.mp4"}}] and d["input"]["metadata"]["youtube"]["privacy"] == "public" and d["input"]["metadata"]["youtube"]["isAiGenerated"] is True, "YouTube: público e IA solo si se piden")
c, d = correr("--simular", "borrador", "--canal", "C1", "--texto", "d", "--servicio", "youtube", "--video", "https://e.com/v.mp4", env={"BUFFER_TEST_SIN_RED": "1"})
ok(d.get("error") == "YOUTUBE_SIN_TITULO", "YouTube sin título se rechaza")
c, d = correr("--simular", "borrador", "--canal", "C1", "--texto", "d", "--servicio", "youtube", "--yt-titulo", "T")
ok(d.get("error") == "YOUTUBE_SIN_VIDEO", "YouTube sin video se rechaza")
c, d = correr("--simular", "borrador", "--canal", "C1", "--texto", "d", "--servicio", "youtube", "--video", "https://e.com/v.mp4", "--yt-titulo", "x" * 101, env={"BUFFER_TEST_SIN_RED": "1"})
ok(d.get("error") == "YOUTUBE_TITULO_LARGO", "YouTube: título de más de 100 caracteres se rechaza")
# Limpieza de medios del hosting tras publicar
c, d = correr("--simular", "limpiar", "--slug", "mi-articulo", "--post", "P1", "--org", "O1", "--canal", "C1")
ok(c == 0 and d.get("simulado") and d["plan"]["borrar"].endswith("assets/social/mi-articulo/"), "limpiar (simulado) apunta a assets/social/<slug>/")
for malo in ("../etc", "a/b", "MAYUS", "ab", "x; rm -rf ~"):
    c, d = correr("--simular", "limpiar", "--slug", malo, "--post", "P1", "--org", "O1", "--canal", "C1")
    ok(d.get("error") == "SLUG_INVALIDO", "limpiar rechaza el slug «%s»" % malo)
c, d = correr("--simular", "eliminar", "--post", "P1")
ok(d.get("error") == "FALTA_CONFIRMACION", "eliminar exige --confirmo")

print("\nRESULTADO:", "TODO CORRECTO" if fallos == 0 else "%d fallo(s)" % fallos)
sys.exit(1 if fallos else 0)
