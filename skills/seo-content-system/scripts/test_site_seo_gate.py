"""Pruebas de site_seo_gate.py sin red externa: un build falso en una carpeta temporal y un servidor local que simula redirecciones.
Ejecutar: python -I test_site_seo_gate.py"""
import http.server
import os
import sys
import tempfile
import threading

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import site_seo_gate as g  # noqa: E402

fallos = 0


def ok(cond, nombre):
    global fallos
    print(("OK    " if cond else "FALLA ") + nombre)
    fallos += 0 if cond else 1


def pagina(titulo, h1, cuerpo, lang="es", extra="", robots=""):
    return f"""<!doctype html><html lang="{lang}"><head><title>{titulo}</title><meta name="description" content="descripcion de {titulo}">
<link rel="canonical" href="https://ejemplo.test/x/"><link rel="alternate" hreflang="{lang}" href="https://ejemplo.test/x/">{robots}</head>
<body><header><nav><a href="/">Inicio</a><a href="/a/">A</a><a href="/b/">B</a><a href="/c/">C</a><a href="/d/">D</a><a href="/e/">E</a></nav></header>
<main><h1>{h1}</h1>{cuerpo}{extra}</main><footer>pie</footer></body></html>"""


def crear(raiz, paginas):
    for ruta, html in paginas.items():
        d = os.path.join(raiz, ruta.strip("/"))
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(html)


class A:  # argumentos como los de la linea de comandos
    ignorar = "colombia"
    prefijo_servicio = "servicios"
    min_palabras = 800
    umbral_apertura = 0.4


relleno = " ".join(["palabra%d" % i for i in range(900)])
with tempfile.TemporaryDirectory() as t:
    crear(t, {
        "/": pagina("Disenador web en Colombia | Marca", "Inicio", "<p>" + relleno + "</p>", lang="es-CO"),
        "/servicios/rediseno/": pagina("Diseno web y rediseno en Colombia | Marca", "Rediseno", "<p>corto</p>"),
        "/servicios/branding/": pagina("Branding y diseno web en Colombia | Marca", "Branding", "<p>" + relleno + "</p><h2>Para quien es</h2><h2>Que incluye</h2><h2>Proceso</h2><h2>Preguntas frecuentes</h2><h2>Casos</h2>"),
        "/blog/art/": pagina("Landing pages que convierten | Marca", "Art", "<p>" + relleno + "</p>", extra='<img src="/img/foto.webp"><img src="/img/logo.svg" alt=""><a href="/x/" aria-label="ver"><img src="/img/p.webp" alt=""></a>'),
        "/oculta/": pagina("Oculta | Marca", "Oculta", "<p>x</p>", robots='<meta name="robots" content="noindex, follow">'),
    })
    open(os.path.join(t, "google123abc.html"), "w").write("google-site-verification: google123abc.html")
    r = g.revisar_estatico(t, A)
    ok(r["paginas"] == 5 and r["indexables"] == 4, "ignora el archivo suelto de verificacion y detecta el noindex")
    ok(any("sin atributo alt" in f and "foto.webp" in f for f in r["fallos"]), "imagen sin atributo alt = fallo")
    ok(any("posible logo con alt vacio" in a for a in r["avisos"]), "logo con alt vacio y sin etiqueta = aviso")
    ok(any("decorativas" in i or "alt vacio dentro" in i for i in r["info"]), "alt vacio dentro de un enlace con aria-label = correcto (info)")
    ok(any("lang inconsistente" in a for a in r["avisos"]) and any("hreflang inconsistente" in a for a in r["avisos"]), "lang y hreflang inconsistentes")
    ok(any("CANDIDATO" in a and "disen web" in a and "/servicios/rediseno/" in a and "/servicios/branding/" in a for a in r["avisos"]), "frase raiz compartida entre dos servicios = candidato a canibalizacion (la que no ve una unicidad exacta)")
    ok(any("delgada" in a and "/servicios/rediseno/" in a for a in r["avisos"]) and not any("delgada" in a and "/servicios/branding/" in a for a in r["avisos"]), "servicio delgado marcado y el completo no")
    ok(any("faltan secciones" in a and "/servicios/rediseno/" in a for a in r["avisos"]), "secciones de servicio que faltan")
    ok(any("ul/ol" in a for a in r["avisos"]), "menu sin lista, agrupado en un solo aviso")
    ok(not any("H1 duplicado" in f for f in r["fallos"]), "sin H1 duplicado")
    # H1 duplicado y titulo vacio
    crear(t, {"/servicios/otro/": pagina("", "Rediseno", "<p>x</p>")})
    r = g.revisar_estatico(t, A)
    ok(any("titulo vacio" in f for f in r["fallos"]) and any("H1 duplicado" in f for f in r["fallos"]), "titulo vacio y H1 duplicado = fallos")

# titulos con numeros y palabras de relleno no cuentan como frase raiz
fr1, _ = g.frase_raiz("Guia de 2026: 5 claves para disenar paginas | Marca", set())
fr2, _ = g.frase_raiz("Otra guia 2026 con 5 claves distintas | Marca", set())
ok(not (fr1 & fr2), "anos, numeros y palabras de relleno no generan canibalizacion falsa")
ok(g.similitud("uno dos tres cuatro cinco seis siete ocho nueve diez", "uno dos tres cuatro cinco seis siete ocho nueve diez") == 1.0, "similitud de aperturas identicas = 1")


# host: servidor local; www se comporta segun el modo
class H(http.server.BaseHTTPRequestHandler):
    modo = "bien"

    def log_message(self, *a):
        pass

    def do_GET(self):
        host = self.headers.get("Host", "")
        if host.startswith("www.") and H.modo == "bien":
            self.send_response(301)
            self.send_header("Location", "https://ejemplo.test" + self.path)
        elif host.startswith("www.") and H.modo == "temporal":
            self.send_response(302)
            self.send_header("Location", "https://ejemplo.test" + self.path)
        else:
            self.send_response(200)
        self.send_header("Content-Length", "0")
        self.end_headers()


srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H)
threading.Thread(target=srv.serve_forever, daemon=True).start()
res = ("127.0.0.1", srv.server_address[1])
H.modo = "bien"
# las variantes http con www redirigen a https canonica; el servidor local no distingue el esquema: se acepta la canonica 200 y los 301
r = g.revisar_host("https://ejemplo.test", "/blog/", sin_tls=True, resolver=res)
ok(any("www.ejemplo.test" in x and "301" in x for x in r["ok"]), "www que redirige 301 a la canonica = ok")
H.modo = "malo"
r = g.revisar_host("https://ejemplo.test", "/blog/", sin_tls=True, resolver=res)
ok(any("www.ejemplo.test" in x and "responde 200" in x for x in r["fallos"]), "www que responde 200 = fallo (el caso de la auditoria)")
H.modo = "temporal"
r = g.revisar_host("https://ejemplo.test", "/blog/", sin_tls=True, resolver=res)
ok(any("temporal" in x for x in r["fallos"]), "redireccion 302 = fallo (debe ser 301)")
srv.shutdown()

print("\nRESULTADO:", "TODO CORRECTO" if fallos == 0 else "%d fallo(s)" % fallos)
sys.exit(1 if fallos else 0)
