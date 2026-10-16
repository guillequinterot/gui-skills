"""match_cdn.py — empareja URL de Medios (CDN) con los archivos originales por SHA-256.

  python -I match_cdn.py <urls.txt> <carpeta-A-IMAGENES> [--out <carpeta-salida>] [--md]

- urls.txt: una URL por línea (las que da «Insertar enlaces» de Medios).
- Descarga cada URL a <out>/cdn_dl (carpeta propia: son archivos no confiables, no ejecutar nada de ahí).
- Compara el SHA-256 contra cada archivo de <carpeta-A-IMAGENES>. El CDN renombra los archivos al subirlos,
  pero NO los recomprime: lo esperable es N de N exactos.
- Escribe <out>/cdn_match.json y, con --md, MAPA-URL-IMAGENES.md e IMG_URLS-listo.ts.txt en <out>.
Código de salida 1 si alguna URL no coincide con ningún original.
"""
import argparse
import hashlib
import json
import os
import sys
import urllib.request

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ap = argparse.ArgumentParser()
ap.add_argument("urls")
ap.add_argument("carpeta")
ap.add_argument("--out", default=".")
ap.add_argument("--md", action="store_true")
a = ap.parse_args()

dl = os.path.join(a.out, "cdn_dl")
os.makedirs(dl, exist_ok=True)
urls = [u.strip() for u in open(a.urls, encoding="utf-8") if u.strip()]
local = {}
for n in os.listdir(a.carpeta):
    p = os.path.join(a.carpeta, n)
    if os.path.isfile(p):
        local[hashlib.sha256(open(p, "rb").read()).hexdigest()] = n
res = []
for u in urls:
    fn = u.rsplit("/", 1)[1]
    p = os.path.join(dl, fn)
    if not os.path.exists(p):
        req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
        open(p, "wb").write(urllib.request.urlopen(req, timeout=60).read())
    h = hashlib.sha256(open(p, "rb").read()).hexdigest()
    res.append({"url": u, "cdn": fn, "size": os.path.getsize(p), "match": local.get(h)})
json.dump(res, open(os.path.join(a.out, "cdn_match.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
ok = sum(1 for r in res if r["match"])
print(f"exactos: {ok} de {len(res)} · originales sin URL: {len(local) - len({r['match'] for r in res if r['match']})}")
for r in res:
    print(r["cdn"], r["size"], r["match"] or "SIN COINCIDENCIA")
if a.md:
    good = sorted((r for r in res if r["match"]), key=lambda r: r["match"])
    md = ["# Mapa archivo → URL de Medios", "", f"Verificado por SHA-256: {ok} de {len(res)} coinciden exactamente.", "",
          "| # | Archivo original | URL de Medios |", "|---|---|---|"]
    md += [f"| {i} | `{r['match']}` | {r['url']} |" for i, r in enumerate(good, 1)]
    open(os.path.join(a.out, "MAPA-URL-IMAGENES.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    ts = ["// Pegar dentro de src/lib/<proyecto>-data.ts (verificado archivo por archivo).", "export const IMG_URLS: Record<string, string> = {"]
    ts += [f'  "{r["match"]}": "{r["url"]}",' for r in good] + ["};"]
    open(os.path.join(a.out, "IMG_URLS-listo.ts.txt"), "w", encoding="utf-8").write("\n".join(ts) + "\n")
sys.exit(0 if ok == len(res) else 1)
