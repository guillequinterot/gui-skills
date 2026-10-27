"""Pruebas de los scripts de design-system-ia (unittest, solo biblioteca estándar).

  python -I -m unittest discover -s scripts/tests -p "test_*.py"

Los archivos de prueba se crean en una carpeta temporal; no hay datos de ningún cliente.
"""
import json
import os
import sys
import tempfile
import unittest

AQUI = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.dirname(AQUI)
sys.path.insert(0, SCRIPTS)

import comparar_figma_contrato as cfc  # noqa: E402
import contraste  # noqa: E402
import validar_contrato as vc  # noqa: E402
import vocabulario_check as vcheck  # noqa: E402
import _comun as c  # noqa: E402

PLANTILLAS = os.path.join(os.path.dirname(SCRIPTS), "templates")

CONTRATO_BUENO = {
    "name": "Button", "version": "1.0.0", "purpose": "Lanza una acción.",
    "neverUseFor": ["Navegar entre páginas (usa un enlace)"],
    "rationale": "Tres tamaños para evitar una escala dispersa.",
    "governance": {"mayExtendLocally": ["Añadir un icono"], "mustEscalateToDS": ["Variantes nuevas"]},
    "states": {"intrinsic": ["hover", "focus"], "authored": [{"name": "disabled", "description": "No interactivo", "aria": "disabled"}]},
    "anatomy": [{"part": "button", "element": "button", "description": "Raíz"}],
    "props": [
        {"name": "variant", "type": "'primary' | 'secondary'", "default": "primary", "description": "Estilo"},
        {"name": "size", "type": "'s' | 'm' | 'l'", "default": "m", "description": "Tamaño"},
        {"name": "onClick", "type": "() => void", "description": "Acción"},
    ],
    "tokenPolicy": {"allowed": ["color.fill"], "forbidden": ["primitive.color"]},
    "a11y": {"role": "button", "keyboardNav": ["Enter — activa"], "wcag": ["1.4.3 Contrast (Minimum), AA"]},
    "figma": {"figmaOnlyProps": ["state"], "stateAxis": ["default", "hover", "focus"]},
}


def escribir(carpeta, nombre, contenido, crlf=False):
    ruta = os.path.join(carpeta, nombre)
    if isinstance(contenido, (dict, list)):
        contenido = json.dumps(contenido, ensure_ascii=False, indent=2)
    if crlf:
        contenido = contenido.replace("\n", "\r\n")
    with open(ruta, "w", encoding="utf-8", newline="") as f:
        f.write(contenido)
    return ruta


class PruebasContraste(unittest.TestCase):
    def test_negro_sobre_blanco(self):
        self.assertAlmostEqual(contraste.contraste("#000000", "#ffffff"), 21.0, places=6)

    def test_gris_777_no_pasa_y_767676_si(self):
        # 4,48:1 no pasa 4,5:1; 4,54:1 sí. No se redondea antes de comparar.
        self.assertFalse(contraste.evaluar("normal", contraste.contraste("#777777", "#ffffff")))
        self.assertTrue(contraste.evaluar("normal", contraste.contraste("#767676", "#ffffff")))

    def test_texto_grande_y_no_texto_usan_3(self):
        r = contraste.contraste("#949494", "#ffffff")  # ~3,03:1
        self.assertTrue(contraste.evaluar("grande", r))
        self.assertTrue(contraste.evaluar("no-texto", r))
        self.assertFalse(contraste.evaluar("normal", r))

    def test_hex_corto_y_transparencia(self):
        self.assertEqual(contraste.parsear_color("#fff"), (255, 255, 255))
        with self.assertRaises(ValueError):
            contraste.parsear_color("#ffffff80")

    def test_pares_claro_oscuro_y_exento(self):
        datos = {"pares": [
            {"nombre": "ok", "texto": {"claro": "#111111", "oscuro": "#f0f0f0"}, "fondo": {"claro": "#ffffff", "oscuro": "#101010"}},
            {"nombre": "falla en oscuro", "texto": {"claro": "#111111", "oscuro": "#555555"}, "fondo": {"claro": "#ffffff", "oscuro": "#101010"}},
            {"nombre": "deshabilitado", "deshabilitado": True, "texto": {"claro": "#cccccc", "oscuro": "#333333"}, "fondo": {"claro": "#ffffff", "oscuro": "#101010"}},
        ]}
        filas, fallos = contraste.procesar_pares(datos)
        self.assertEqual(fallos, 1)
        self.assertTrue(any(f[0] == "falla en oscuro" and f[1] == "oscuro" and f[4] == "FALLA" for f in filas))
        self.assertTrue(all(f[4].startswith("exento") for f in filas if f[0] == "deshabilitado"))


    def test_sitio_solo_claro(self):
        datos = {"temas": ["claro"], "pares": [
            {"nombre": "texto", "texto": {"claro": "#1e1e1e"}, "fondo": {"claro": "#ffffff"}}]}
        filas, fallos = contraste.procesar_pares(datos)
        self.assertEqual((len(filas), fallos), (1, 0))
        self.assertEqual(filas[0][1], "claro")
        sin_tema = {"pares": [{"nombre": "texto", "texto": {"claro": "#1e1e1e"}, "fondo": {"claro": "#ffffff"}}]}
        filas, fallos = contraste.procesar_pares(sin_tema)
        self.assertEqual(fallos, 1)  # sin «temas», falta el oscuro y se informa


class PruebasValidarContrato(unittest.TestCase):
    def setUp(self):
        self.esquema = c.leer_json(vc.ESQUEMA_POR_DEFECTO)

    def test_contrato_bueno_pasa_forma_y_politica(self):
        self.assertEqual(vc.validar(CONTRATO_BUENO, self.esquema), [])
        self.assertEqual(vc.politica(CONTRATO_BUENO), [])

    def test_falta_campo_obligatorio_y_campo_desconocido(self):
        malo = {k: v for k, v in CONTRATO_BUENO.items() if k != "purpose"}
        malo["inventado"] = 1
        errores = vc.validar(malo, self.esquema)
        self.assertTrue(any("purpose" in e for e in errores))
        self.assertTrue(any("inventado" in e for e in errores))

    def test_patrones_y_tipos(self):
        malo = json.loads(json.dumps(CONTRATO_BUENO))
        malo["name"] = "boton"
        malo["version"] = "uno"
        malo["props"][0]["required"] = "si"
        errores = " | ".join(vc.validar(malo, self.esquema))
        self.assertIn("name", errores)
        self.assertIn("version", errores)
        self.assertIn("required", errores)

    def test_politica_detecta_lo_que_el_esquema_deja_opcional(self):
        flojo = {k: v for k, v in CONTRATO_BUENO.items() if k not in ("neverUseFor", "rationale", "governance", "a11y")}
        self.assertEqual(vc.validar(flojo, self.esquema), [])  # la forma es válida
        problemas = vc.politica(flojo)
        self.assertGreaterEqual(len(problemas), 4)

    def test_politica_kebab_case_y_token_en_allowed_y_forbidden(self):
        malo = json.loads(json.dumps(CONTRATO_BUENO))
        malo["anatomy"][0]["part"] = "BotonRaiz"
        malo["tokenPolicy"] = {"allowed": ["color.fill"], "forbidden": ["color.fill"]}
        problemas = " | ".join(vc.politica(malo))
        self.assertIn("kebab-case", problemas)
        self.assertIn("allowed y en forbidden", problemas)

    def test_objetos_anidados_admiten_campos_extra_pero_la_raiz_no(self):
        extra = json.loads(json.dumps(CONTRATO_BUENO))
        extra["props"][0]["usage"] = "nota"
        extra["a11y"]["notes"] = "nota"
        self.assertEqual(vc.validar(extra, self.esquema), [])
        extra["sizes"] = {}
        self.assertTrue(any("sizes" in e for e in vc.validar(extra, self.esquema)))

    def test_plantilla_json_no_pasa_en_modo_estricto(self):
        plantilla = c.leer_json(os.path.join(PLANTILLAS, "contrato-completo.json"))
        self.assertTrue(vc.marcadores(plantilla))

    def test_plantilla_minima_tiene_los_campos_y_el_estricto_la_rechaza(self):
        texto = c.leer_texto(os.path.join(PLANTILLAS, "contrato-minimo.md"))
        self.assertEqual(vc.validar_minimo(texto, estricto=False), [])
        self.assertTrue(vc.validar_minimo(texto, estricto=True))

    def test_minimo_rellenado_con_crlf(self):
        with tempfile.TemporaryDirectory() as d:
            texto = ("# Botón\n**Propósito:** lanza una acción.\n**Nunca usar para:** navegar (usa un enlace).\n"
                     "**Justificación:** tres tamaños.\n**Se adapta en el proyecto:** añadir un icono.\n"
                     "**Se escala al sistema:** variantes nuevas.\n**Anatomía:** `boton` (raíz).\n"
                     "**Estados que se entregan:** normal · hover · foco.\n")
            ruta = escribir(d, "boton.md", texto, crlf=True)
            self.assertEqual(vc.main([ruta, "--estricto"]), 0)

    def test_main_devuelve_1_con_contrato_malo(self):
        with tempfile.TemporaryDirectory() as d:
            malo = {k: v for k, v in CONTRATO_BUENO.items() if k != "tokenPolicy"}
            ruta = escribir(d, "malo.json", malo)
            self.assertEqual(vc.main([ruta]), 1)
            ruta2 = escribir(d, "bueno.json", CONTRATO_BUENO)
            self.assertEqual(vc.main([ruta2, "--politica"]), 0)


VOCABULARIO = """# Vocabulario

## 2. Tabla del vocabulario

| Canónico | Prohibidos (→ alternativa) | Dónde aplica | Equivalencia nativa | Figma | Decisión |
|---|---|---|---|---|---|
| `onClick` | `onPress` → `onClick`; `onTap` | todos | evento click | — | x |
| `isLoading` | `loading`, `pending` | todos | `aria-busy` | VARIANT | x |
| `variant` | `kind`, `data-kind` | todos | — | VARIANT | x |
| `<nombre>` | `<sinónimo>` → `<nombre>` | | | | |

## 5. Pasos permitidos

| Nombre | Componentes donde se permite | Motivo |
|---|---|---|
| `title` | todos | atributo nativo |
"""

CODIGO = """<Button onPress={() => a > b} loading kind="x">Guardar</Button>
<p>La palabra onPress y loading en un texto no cuentan.</p>
<div data-kind="primary" class="card"></div>
<input type="text" title="ok">
<Card pending={cargando} title="t" />
<!-- <Button onPress> comentado -->
const x = a < b && c > d;
"""


class PruebasVocabulario(unittest.TestCase):
    def test_lee_prohibidos_alternativas_y_permitidos(self):
        proh, perm = vcheck.leer_vocabulario(VOCABULARIO)
        self.assertEqual(proh["onPress"], ["onClick"])
        self.assertEqual(proh["onTap"], ["onClick"])
        self.assertEqual(proh["loading"], ["isLoading"])
        self.assertNotIn("<sinónimo>", proh)
        self.assertEqual(perm, {"title"})

    def test_detecta_atributos_reales_y_no_texto_ni_comentarios(self):
        proh, perm = vcheck.leer_vocabulario(VOCABULARIO)
        with tempfile.TemporaryDirectory() as d:
            ruta = escribir(d, "a.tsx", CODIGO, crlf=True)
            hs = vcheck.revisar_archivo(ruta, proh, perm, None, False)
        encontrados = {(h[1], h[2]) for h in hs}
        self.assertIn(("Button", "onPress"), encontrados)
        self.assertIn(("Button", "loading"), encontrados)
        self.assertIn(("div", "data-kind"), encontrados)
        self.assertIn(("Card", "pending"), encontrados)
        self.assertEqual(len(hs), 5, hs)  # incluye Button kind
        self.assertNotIn(("input", "title"), encontrados)  # permitido y nativo
        self.assertEqual(sorted({h[0] for h in hs if h[1] == "Button"}), [1])  # número de línea con CRLF

    def test_con_contratos_solo_avisa_si_declara_la_prop_canonica(self):
        proh, perm = vcheck.leer_vocabulario(VOCABULARIO)
        contratos = {"Button": {"onClick", "variant"}, "Card": {"title"}}
        with tempfile.TemporaryDirectory() as d:
            ruta = escribir(d, "a.tsx", CODIGO)
            hs = vcheck.revisar_archivo(ruta, proh, perm, contratos, False)
        encontrados = {(h[1], h[2]) for h in hs}
        self.assertIn(("Button", "onPress"), encontrados)      # Button declara onClick
        self.assertNotIn(("Button", "loading"), encontrados)   # Button no declara isLoading
        self.assertNotIn(("Card", "pending"), encontrados)     # Card no declara isLoading

    def test_modo_informe_y_bloqueo(self):
        with tempfile.TemporaryDirectory() as d:
            voc = escribir(d, "vocabulario.md", VOCABULARIO)
            cod = escribir(d, "a.html", '<Button onPress="x"></Button>')
            self.assertEqual(vcheck.main(["--vocabulario", voc, cod]), 0)
            self.assertEqual(vcheck.main(["--vocabulario", voc, cod, "--bloqueo"]), 1)

    def test_vocabulario_sin_filas_rellenadas_es_error_de_uso(self):
        with tempfile.TemporaryDirectory() as d:
            voc = escribir(d, "vocabulario.md", c.leer_texto(os.path.join(PLANTILLAS, "vocabulario.md")))
            cod = escribir(d, "a.html", "<p></p>")
            # la plantilla trae dos filas de ejemplo con nombres reales (disabled, required): se cargan
            proh, _ = vcheck.leer_vocabulario(c.leer_texto(voc))
            self.assertIn("isDisabled", proh)
            self.assertNotIn("<sinónimo>", proh)
            self.assertEqual(vcheck.main(["--vocabulario", voc, cod]), 0)


FIGMA = {"component": "Button", "properties": {
    "variant": {"type": "VARIANT", "defaultValue": "primary", "variantOptions": ["primary", "secondary"]},
    "size": {"type": "VARIANT", "defaultValue": "s", "variantOptions": ["s", "m", "l", "xl"]},
    "state": {"type": "VARIANT", "defaultValue": "default", "variantOptions": ["default", "hover"]},
    "children#1:2": {"type": "TEXT", "defaultValue": "Botón"},
    "extra#3:4": {"type": "BOOLEAN", "defaultValue": True},
    "icon.#5:6": {"type": "BOOLEAN", "defaultValue": False},
}}


class PruebasFigma(unittest.TestCase):
    def test_detecta_defecto_opciones_extra_y_estados(self):
        contrato = json.loads(json.dumps(CONTRATO_BUENO))
        contrato["props"].append({"name": "children", "type": "string", "description": "Texto"})
        dif = " | ".join(cfc.comparar(contrato, cfc.leer_figma(FIGMA)))
        self.assertIn("valor por defecto distinto en «size»", dif)
        self.assertIn("opciones distintas en «size»", dif)
        self.assertIn("«extra»", dif)
        self.assertIn("eje «state»", dif)         # falta focus
        self.assertNotIn("onClick", dif)          # los manejadores no tienen propiedad
        self.assertNotIn("icon", dif)             # ayudante solo-Figma con punto final

    def test_coincidencia_total(self):
        contrato = {"name": "X", "props": [{"name": "variant", "type": "'a' | 'b'", "default": "a", "description": ""},
                                           {"name": "isLoading", "type": "boolean", "default": False, "description": ""}],
                    "figma": {"figmaOnlyProps": ["state"]}}
        figma = {"variant": {"type": "VARIANT", "defaultValue": "a", "variantOptions": ["a", "b"]},
                 "isLoading": {"type": "VARIANT", "defaultValue": "false", "variantOptions": ["false", "true"]},
                 "state": {"type": "VARIANT", "defaultValue": "default", "variantOptions": ["default"]}}
        self.assertEqual(cfc.comparar(contrato, cfc.leer_figma(figma)), [])

    def test_orden_variantes_primero(self):
        contrato = {"name": "X", "props": [{"name": "a", "type": "string", "description": ""},
                                           {"name": "b", "type": "string", "description": ""}]}
        figma = [{"name": "a", "type": "TEXT"}, {"name": "b", "type": "VARIANT"}]
        self.assertTrue(any("orden" in d for d in cfc.comparar(contrato, cfc.leer_figma(figma))))


class PruebasPlantillas(unittest.TestCase):
    def test_el_json_de_la_plantilla_es_valido_json(self):
        c.leer_json(os.path.join(PLANTILLAS, "contrato-completo.json"))

    def test_comentarios_y_bloques_cerrados(self):
        for nombre in os.listdir(PLANTILLAS):
            if nombre.endswith((".md", ".txt")):
                t = c.leer_texto(os.path.join(PLANTILLAS, nombre))
                self.assertEqual(t.count("<!--"), t.count("-->"), nombre)
                self.assertEqual(t.count("```") % 2, 0, nombre)


if __name__ == "__main__":
    unittest.main()
