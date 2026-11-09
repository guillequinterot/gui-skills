"""Pruebas de check_schema_single_block.py sin red.
Ejecutar: python -I test_check_schema_single_block.py"""
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import check_schema_single_block as c  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:  # noqa: BLE001
    pass
fallos = 0


def ok(cond, nombre):
    global fallos
    print(("OK    " if cond else "FALLA ") + nombre)
    fallos += 0 if cond else 1


def bloque(obj):
    return '<script type="application/ld+json">' + json.dumps(obj) + "</script>"


U = "https://ejemplo.test/a/"
bueno = {"@context": "https://schema.org", "@graph": [
    {"@type": "Organization", "@id": "https://ejemplo.test/#organization"},
    {"@type": "WebPage", "@id": U + "#webpage", "isPartOf": {"@id": "https://ejemplo.test/#organization"}},
    {"@type": "FAQPage", "@id": U + "#faq", "isPartOf": {"@id": U + "#webpage"}, "mainEntity": []},
    {"@type": "VideoObject", "@id": U + "#video", "isPartOf": {"@id": U + "#webpage"}}]}
r = c.revisar("<html>" + bloque(bueno) + "</html>")
ok(r["pasa"] and r["bloques"] == 1, "una página con un solo @graph conectado pasa")

r = c.revisar("<html>" + bloque(bueno) + bloque({"@context": "https://schema.org", "@type": "FAQPage"}) + "</html>")
ok(not r["pasa"] and any("2 bloques" in f for f in r["fallos"]), "dos bloques fallan")

r = c.revisar("<html></html>")
ok(not r["pasa"] and any("0 bloques" in f for f in r["fallos"]), "cero bloques fallan")

r = c.revisar("<html>" + bloque({"@context": "https://schema.org", "@type": "FAQPage"}) + "</html>")
ok(not r["pasa"] and any("@graph" in f for f in r["fallos"]), "un bloque sin @graph falla")

malo = json.loads(json.dumps(bueno)); malo["@graph"][2]["isPartOf"] = {"@id": U + "#otro"}
r = c.revisar("<html>" + bloque(malo) + "</html>")
ok(not r["pasa"] and any("no están definidos" in f for f in r["fallos"]), "una referencia a un @id inexistente falla")

solo_cuerpo = {"@context": "https://schema.org", "@graph": [
    {"@type": "FAQPage", "@id": U + "#faq", "isPartOf": {"@id": U + "#webpage"}},
    {"@type": "VideoObject", "@id": U + "#video", "isPartOf": {"@id": U + "#webpage"}}]}
ok(not c.revisar("<html>" + bloque(solo_cuerpo) + "</html>")["pasa"], "fuente del artículo sin --cuerpo: #webpage no está definido y falla")
ok(c.revisar("<html>" + bloque(solo_cuerpo) + "</html>", cuerpo=True)["pasa"], "fuente del artículo con --cuerpo: #webpage se acepta como externo")

dup = json.loads(json.dumps(bueno)); dup["@graph"].append({"@type": "Organization", "@id": "https://ejemplo.test/#org2"})
r = c.revisar("<html>" + bloque(dup) + "</html>")
ok(not r["pasa"] and any("2 nodos Organization" in f for f in r["fallos"]), "dos Organization fallan")

r = c.revisar('<html><script type="application/ld+json">{no es json}</script></html>')
ok(not r["pasa"] and any("JSON válido" in f for f in r["fallos"]), "JSON inválido falla")

nid = json.loads(json.dumps(bueno)); del nid["@graph"][3]["@id"]
ok(not c.revisar("<html>" + bloque(nid) + "</html>")["pasa"], "un nodo sin @id falla")

print(f"\n{fallos} fallos")
sys.exit(1 if fallos else 0)
