"""Genera un archivo de desautorizacion (disavow) POR DOMINIO a partir de una exportacion de enlaces entrantes (CSV de Ahrefs, de
Search Console o de cualquier herramienta con columnas de URL de origen y, si existe, texto del enlace). Solo lectura sobre el CSV.

Clasifica cada dominio por señales de granja de enlaces y escribe:
  disavow.txt     -> SOLO los dominios de confianza alta (formato de Google: «# comentario» y «domain:ejemplo.com»)
  revision.csv    -> todos los dominios con sus señales y el nivel (alta, media, baja) para que una persona los revise ANTES de subir nada
Uso: python -I disavow_desde_exportacion.py exportacion.csv [--salida carpeta]
El archivo se sube a mano en Search Console (herramienta de desautorizacion). Esto es precaucion, no cura: no sustituye conseguir enlaces reales."""
import argparse, collections, csv, os, re, sys, urllib.parse

sys.stdout.reconfigure(encoding="utf-8")
TLD_BARATOS = {"shop", "agency", "store", "xyz", "top", "click", "site", "online", "icu", "buzz", "cyou", "monster", "lol", "cfd", "sbs", "rest", "bond"}
HOST_SENAL = re.compile(r"seo|backlink|rank|serp|linkbuil|linkrank|buylink|dofollow|booster|guestpost", re.I)
TEXTO_SENAL = re.compile(r"backlink|dofollow|\bDA ?\d+|\bPA ?\d+|\bPBN\b|higher rankings|seo expert|buy .*links|rank (#|no\.?) ?1|premium|serp", re.I)
DOS_NIVELES = {"com.co", "co.uk", "com.mx", "com.ar", "com.br", "com.es", "org.co", "net.co"}


def dominio(url):
    h = (urllib.parse.urlsplit(url if "//" in url else "//" + url).hostname or "").lower()
    p = h.split(".")
    if len(p) >= 3 and ".".join(p[-2:]) in DOS_NIVELES:
        return ".".join(p[-3:])
    return ".".join(p[-2:]) if len(p) >= 2 else h


def columna(cols, *claves):
    for c in cols:
        if any(k in c.lower() for k in claves):
            return c
    return None


ap = argparse.ArgumentParser()
ap.add_argument("csv")
ap.add_argument("--salida", default=".")
a = ap.parse_args()
raw = open(a.csv, "rb").read()
txt = raw.decode("utf-16") if raw[:2] in (b"\xff\xfe", b"\xfe\xff") else raw.decode("utf-8-sig", errors="ignore")
dialecto = csv.Sniffer().sniff(txt[:4096], delimiters=",;\t")
filas = list(csv.DictReader(txt.splitlines(), dialect=dialecto))
cols = list(filas[0].keys())
c_url = columna(cols, "referring page url", "source url", "origen", "url de origen", "referring url", "url") or cols[0]
c_dom = columna(cols, "referring domain", "dominio")
c_txt = columna(cols, "anchor", "texto")
c_rel = columna(cols, "nofollow", "rel")
info = collections.OrderedDict()
for f in filas:
    d = (f.get(c_dom) or "").strip().lower() if c_dom else ""
    d = dominio(d) if d else dominio(f.get(c_url, ""))
    if not d:
        continue
    x = info.setdefault(d, {"enlaces": 0, "textos": collections.Counter(), "nofollow": 0})
    x["enlaces"] += 1
    if c_txt and f.get(c_txt):
        x["textos"][f[c_txt].strip()[:120]] += 1
    if c_rel and re.search(r"nofollow|true|1|yes|si", str(f.get(c_rel, "")), re.I):
        x["nofollow"] += 1

res = []
for d, x in info.items():
    senales = []
    if d.split(".")[-1] in TLD_BARATOS:
        senales.append("extension barata (." + d.split(".")[-1] + ")")
    if HOST_SENAL.search(d.split(".")[0]):
        senales.append("el nombre del dominio habla de SEO/backlinks")
    t = next((t for t, _ in x["textos"].most_common() if TEXTO_SENAL.search(t)), "")
    if t:
        senales.append("texto de enlace de granja: «" + t[:70] + "»")
    if x["enlaces"] >= 5 and not any("texto" in s for s in senales) and x["textos"] and len(x["textos"]) == 1:
        senales.append("mismo texto repetido en %d enlaces" % x["enlaces"])
    nivel = "alta" if len(senales) >= 2 else ("media" if senales else "baja")
    res.append({"dominio": d, "enlaces": x["enlaces"], "nivel": nivel, "senales": "; ".join(senales) or "sin señales", "texto_mas_comun": (x["textos"].most_common(1) or [("", 0)])[0][0]})

os.makedirs(a.salida, exist_ok=True)
with open(os.path.join(a.salida, "revision.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(res[0].keys()))
    w.writeheader()
    w.writerows(sorted(res, key=lambda r: ({"alta": 0, "media": 1, "baja": 2}[r["nivel"]], -r["enlaces"])))
alta = sorted(r["dominio"] for r in res if r["nivel"] == "alta")
with open(os.path.join(a.salida, "disavow.txt"), "w", encoding="utf-8", newline="\n") as f:
    f.write("# Desautorizacion por dominio. Generado a partir de una exportacion de enlaces; revisado por una persona antes de subir.\n")
    f.write("# Solo dominios de confianza alta (granjas de enlaces automaticas). Revisar cada trimestre.\n")
    for d in alta:
        f.write("domain:%s\n" % d)
n = collections.Counter(r["nivel"] for r in res)
print(f"Dominios: {len(res)} | alta: {n['alta']} | media (revisar a mano): {n['media']} | baja: {n['baja']}")
print("Escrito:", os.path.join(a.salida, "disavow.txt"), "y", os.path.join(a.salida, "revision.csv"))
