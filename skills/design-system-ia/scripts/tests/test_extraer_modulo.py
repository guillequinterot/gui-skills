"""Pruebas de extraer_modulo.py (HTML y CSS reales de un módulo)."""
import os, sys, tempfile, unittest
SCRIPTS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SCRIPTS)
import extraer_modulo as ex  # noqa: E402

HTML = '<!doctype html><html><body><article class="tarjeta"><div class="tarjeta__cuerpo"><h3>Título</h3><img src="/a.webp" alt="x"><a class="boton tarjeta__cta" href="/x/">Ver</a></div></article><article class="tarjeta tarjeta--compacta"><p>Otra</p></article></body></html>'
CSS = """
:root { --color: #111; --espacio: 8px; }
/* comentario */
.tarjeta, .otra-cosa { border-radius: 8px; padding: var(--espacio); }
.tarjeta__cuerpo h3 { color: var(--color); }
.seccion .tarjeta { margin: 0; }
.boton { display: inline-flex; }
@media (max-width: 600px) { .tarjeta--compacta { padding: 0; } .ajeno { color: red; } }
"""


class Pruebas(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.d, "dist")); os.makedirs(os.path.join(self.d, "css"))
        open(os.path.join(self.d, "dist", "index.html"), "w", encoding="utf-8").write(HTML)
        open(os.path.join(self.d, "css", "a.css"), "w", encoding="utf-8", newline="").write(CSS.replace("\n", "\r\n"))
        ex.configurar(os.path.join(self.d, "dist"), os.path.join(self.d, "css"), ["a.css"])

    def test_elemento_real_con_hijos(self):
        h = ex.elemento("index.html", "tarjeta", exacto="tarjeta")
        self.assertIn('<article class="tarjeta">', h)
        self.assertIn("tarjeta__cuerpo", h)
        self.assertIn('<img src="/a.webp" alt="x">', h)

    def test_variante_por_clase_exacta(self):
        self.assertIn("tarjeta--compacta", ex.elemento("index.html", "tarjeta", exacto="tarjeta tarjeta--compacta"))

    def test_css_solo_reglas_que_empiezan_por_la_clase_y_con_bem(self):
        t = ex.a_texto(ex.css_del_modulo(["tarjeta"]))
        self.assertIn(".tarjeta__cuerpo h3", t)
        self.assertIn("@media (max-width: 600px)", t)
        self.assertNotIn(".seccion .tarjeta", t)   # regla de contexto descartada
        self.assertNotIn(".otra-cosa", t)          # solo el selector del módulo dentro de una lista
        self.assertNotIn(".ajeno", t)
        self.assertNotIn(".boton", t)

    def test_dependencia_incluye_el_css_del_otro_modulo(self):
        t = ex.a_texto(ex.css_del_modulo(["tarjeta", "boton"]))
        self.assertIn(".boton", t)

    def test_variables(self):
        t = ex.a_texto(ex.css_del_modulo(["tarjeta"]))
        self.assertEqual(ex.variables_usadas(t), ["--color", "--espacio"])
        self.assertEqual(ex.raiz_vars()["--color"], "#111")


if __name__ == "__main__":
    unittest.main()
