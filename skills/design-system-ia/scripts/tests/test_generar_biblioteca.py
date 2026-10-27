"""Pruebas del generador de la biblioteca de módulos (unittest, solo biblioteca estándar)."""
import copy
import json
import os
import re
import sys
import tempfile
import unittest

AQUI = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.dirname(AQUI)
sys.path.insert(0, SCRIPTS)

import generar_biblioteca as gb  # noqa: E402
import contraste as ct  # noqa: E402

LOGO = ('<?xml version="1.0"?><svg id="Capa" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10"><defs><style>.cls-1{fill:#1d1d1b}</style></defs>'
        '<path class="cls-1" d="M0 0h10v10H0z"/></svg>')

MAN = {
    "meta": {"titulo": "Sistema de prueba", "subtitulo": "Sub", "version": "v1", "fecha": "hoy", "noindex": True,
             "home_url": "https://ejemplo.test/", "home_etiqueta": "Volver al sitio", "base_preview": "a{color:inherit}"},
    "marca": {"nombre": "Cliente de prueba", "logo_svg": LOGO, "acento": "#A3E635", "tinta": "#1E1E1E", "fondo": "#F8FAFF"},
    "reglas_ia": ["Usa solo las variables del módulo."],
    "grupos": [{"etiqueta": "Componentes", "modulos": ["m1"]}, {"etiqueta": "Calidad", "modulos": ["m2"]}],
    "resumen": {"kpis": [{"valor": "3/4", "etiqueta": "pasan", "nota": "n", "tono": "ok", "barra": 75}]},
    "modulos": [
        {"id": "m1", "n": "M1", "titulo": "Botón", "estado": "Propuesta", "descripcion": "d", "css": ".b{color:var(--c)}", "tokens": {"--c": "#111111"},
         "variantes": [{"id": "m1-a", "nombre": "Primario", "uso": "u", "html": '<a class="b" href="#">Hola </script></a>', "tipo": "componente", "json": {"name": "Boton"}}]},
        {"id": "m2", "n": "M2", "titulo": "Datos", "estado": "Hallazgo", "descripcion": "d", "variantes": [
            {"id": "m2-a", "nombre": "Colores", "tipo": "doc", "html": gb.bloque_swatches([("--c", "#111111")]), "json": {"--c": "#111111"}}]},
    ],
}


class PruebasGenerador(unittest.TestCase):
    def setUp(self):
        self.man = copy.deepcopy(MAN)
        self.html = gb.render(self.man)

    def test_manifiesto_valido(self):
        self.assertEqual(gb.validar_manifiesto(self.man), [])

    def test_manifiesto_invalido_detecta_errores(self):
        m = copy.deepcopy(MAN)
        m["modulos"][1]["id"] = "m1"
        m["grupos"][0]["modulos"].append("no-existe")
        m["modulos"][0]["variantes"][0].pop("html")
        e = " | ".join(gb.validar_manifiesto(m))
        self.assertIn("repetidos", e)
        self.assertIn("inexistente", e)

    def test_noindex_y_estructura(self):
        self.assertIn('<meta name="robots" content="noindex, nofollow">', self.html)
        self.assertIn('<aside class="rail"', self.html)       # menú lateral
        self.assertEqual(self.html.count('class="rail__logo"'), 2)  # menú y barra móvil
        self.assertIn('aria-label="Cliente de prueba"', self.html)
        self.assertNotIn("%%", self.html)

    def test_sin_noindex_si_se_pide(self):
        self.man["meta"]["noindex"] = False
        self.assertNotIn('name="robots"', gb.render(self.man))

    def test_boton_volver_al_sitio_en_menu_y_barra(self):
        self.assertEqual(self.html.count('href="https://ejemplo.test/"'), 2)
        self.assertIn("Volver al sitio", self.html)

    def test_sin_home_no_hay_boton(self):
        del self.man["meta"]["home_url"]
        self.assertNotIn("Volver al sitio", gb.render(self.man))

    def test_acciones_de_cada_variante(self):
        d = re.search(r'<article class="demo" id="m1-a".*?</article>', self.html, re.S).group(0)
        for t in ("html", "css", "json", "prompt"):
            self.assertIn(f'data-tipo="{t}"', d)
        self.assertIn("Ver código", d)
        d2 = re.search(r'<article class="demo" id="m2-a".*?</article>', self.html, re.S).group(0)
        self.assertNotIn('data-tipo="css"', d2)   # un bloque de datos sin CSS no ofrece «Copiar CSS»

    def test_datos_json_incrustados_y_seguros(self):
        m = re.search(r'<script type="application/json" id="datos">(.*?)</script>', self.html, re.S)
        self.assertIsNotNone(m)
        datos = json.loads(m.group(1))
        self.assertEqual(datos["modulos"][0]["variantes"][0]["id"], "m1-a")
        self.assertNotIn("</script>", m.group(1))             # el HTML del módulo contiene </script> y se escapa

    def test_acento_texto_seguro_cumple_aa(self):
        c, ratio = gb.acento_texto_seguro("#A3E635", "#F8FAFF")
        self.assertGreaterEqual(ratio, 4.5)
        self.assertGreaterEqual(ct.contraste(c, "#F8FAFF"), 4.5)

    def test_texto_sobre_el_acento_tiene_contraste(self):
        css = re.search(r"--sobre-acento:(#[0-9A-Fa-f]{6})", self.html).group(1)
        fondo = re.search(r"--acento-texto:(#[0-9A-Fa-f]{6})", self.html).group(1)
        self.assertGreaterEqual(ct.contraste(css, fondo), 4.5)

    def test_logo_sin_estilos_globales_que_choquen(self):
        self.assertNotIn(".cls-1", self.html)
        self.assertIn('style="fill: #1d1d1b"', self.html.replace("fill:#1d1d1b", "fill: #1d1d1b"))

    def test_bloques_visuales(self):
        self.assertIn("Pasa AA", gb.bloque_contraste("#000000", "#ffffff", "x"))
        self.assertIn("Falla AA", gb.bloque_contraste("#a3e635", "#ffffff", "x"))
        self.assertIn('class="b-escala"', gb.bloque_escala([("a", 4), ("b", 8)]))
        self.assertIn("Hoy", gb.bloque_antes_despues(["alt"], ["imageAlt"]))

    def test_bloque_de_codigo_no_hereda_el_estilo_de_codigo_en_linea(self):
        # Defecto real: el estilo de `code` (fondo claro) volvía ilegible el texto claro del panel de código.
        self.assertIn("pre code{background:none", self.html)

    def test_la_plantilla_de_manifiesto_genera_una_pagina(self):
        ruta = os.path.join(os.path.dirname(SCRIPTS), "templates", "biblioteca-manifiesto.json")
        man = json.load(open(ruta, encoding="utf-8"))
        self.assertEqual(gb.validar_manifiesto(man), [])
        html = gb.render(man)
        self.assertIn('class="demo"', html)
        self.assertIn("Volver al sitio", html)

    def test_main_escribe_el_archivo(self):
        with tempfile.TemporaryDirectory() as d:
            man = os.path.join(d, "m.json")
            json.dump(self.man, open(man, "w", encoding="utf-8"), ensure_ascii=False)
            salida = os.path.join(d, "sub", "index.html")
            self.assertEqual(gb.main([man, salida]), 0)
            self.assertTrue(os.path.getsize(salida) > 5000)


class PruebasCapaParaIA(unittest.TestCase):
    def setUp(self):
        self.man = copy.deepcopy(MAN)
        self.man["meta"]["url_publica"] = "https://ejemplo.test/design-system"
        self.d = tempfile.mkdtemp()
        self.archivos = gb.escribir_paquete(self.man, self.d)

    def leer(self, rel):
        return open(os.path.join(self.d, rel), encoding="utf-8").read()

    def test_la_entrega_es_una_carpeta_con_capa_para_ia(self):
        for rel in ("index.html", "sistema.json", "llms.txt", "AGENTS.md", "logo.svg", "modulos/m1.json", "modulos/m2.json"):
            self.assertIn(rel, self.archivos)
            self.assertTrue(os.path.getsize(os.path.join(self.d, rel)) > 50, rel)

    def test_sistema_json_trae_todo_lo_necesario_para_construir(self):
        sj = json.loads(self.leer("sistema.json"))
        self.assertEqual(sj["url"], "https://ejemplo.test/design-system/")
        self.assertTrue(sj["marca"]["logo"].endswith("/logo.svg"))
        v = sj["modulos"][0]["variantes"][0]
        for campo in ("html", "css", "json", "prompt"):
            self.assertTrue(v[campo], campo)
        self.assertIn("--c: #111111", v["css"])
        self.assertIn("Usa solo las variables del módulo.", v["prompt"])
        self.assertIn("https://ejemplo.test/design-system/llms.txt", sj["prompt_maestro"])

    def test_llms_txt_con_enlaces_absolutos_y_modulos(self):
        t = self.leer("llms.txt")
        self.assertTrue(t.startswith("# Sistema de prueba"))
        self.assertIn("[Sistema completo (JSON)](https://ejemplo.test/design-system/sistema.json)", t)
        self.assertIn("modulos/m1.json", t)
        self.assertIn("## Optional", t)

    def test_el_prompt_de_la_pagina_y_el_del_archivo_son_el_mismo_texto(self):
        m = self.man["modulos"][0]
        v = m["variantes"][0]
        py = gb.prompt_de(self.man, m, v)
        for trozo in ("Reglas del sistema:", "Contrato / datos (JSON):", "HTML de referencia", "CSS del módulo:", "Tarea: duplica este módulo", "Condiciones:"):
            self.assertIn(trozo, py)
            self.assertIn(trozo.split(":")[0], self.leer("index.html"))   # el JS de la página arma las mismas secciones

    def test_la_vista_previa_existe_sin_javascript(self):
        html = self.leer("index.html")
        self.assertIn('<template shadowrootmode="open">', html)
        previo = re.search(r'<template shadowrootmode="open"><style>(.*?)</style>(.*?)</template>', html, re.S)
        self.assertIn("--c: #111111", previo.group(1))
        self.assertIn('class="b"', previo.group(2))      # el componente real está en el HTML estático

    def test_pagina_muestra_la_url_y_el_prompt_maestro(self):
        html = self.leer("index.html")
        self.assertIn("Para una IA: entrégale esta URL", html)
        self.assertIn('data-accion="copiar-maestro"', html)
        self.assertIn('rel="alternate" type="application/json" href="https://ejemplo.test/design-system/sistema.json"', html)

    def test_sin_logo_no_hay_entrega(self):
        m = copy.deepcopy(MAN)
        m["marca"]["logo_svg"] = ""
        self.assertTrue(any("logo" in e for e in gb.validar_manifiesto(m)))
        m2 = copy.deepcopy(MAN)
        del m2["marca"]["nombre"]
        self.assertTrue(any("nombre" in e for e in gb.validar_manifiesto(m2)))

    def test_el_logo_viaja_en_la_entrega(self):
        self.assertIn("<svg", self.leer("logo.svg"))
        self.assertNotIn("<?xml", self.leer("logo.svg"))

    def test_main_con_carpeta_de_salida(self):
        with tempfile.TemporaryDirectory() as d:
            man = os.path.join(d, "m.json")
            json.dump(self.man, open(man, "w", encoding="utf-8"), ensure_ascii=False)
            self.assertEqual(gb.main([man, os.path.join(d, "entrega")]), 0)
            self.assertTrue(os.path.exists(os.path.join(d, "entrega", "sistema.json")))


if __name__ == "__main__":
    unittest.main()
