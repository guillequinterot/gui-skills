"""streak.py — ejemplo de la sesión de `caso-diplomas-01` (anonimizado, no mantenido; la versión general de los assets es `scripts/bake_assets.py`).

Reconstruye como SVG los dibujos de una página de PDF filtrados por color de relleno (trazos de pincel de un brochure):
lee `get_drawings()`, convierte `items` (l, c, re, qu) a un `d` de path y recolorea al color oficial de la marca.
Ajustar RED_R (canal rojo normalizado 0-1 del relleno a filtrar), COLOR (hex oficial) y x0 (recorte lateral en pt).
"""
RED_R = 0.885
COLOR = "#DA111C"
import fitz
A = "assets"   # carpeta de assets del proyecto (salida)
b = fitz.open("brochure.pdf")   # PDF del cliente con los trazos (fuera del repo)
bp = b[0]
W,H = bp.rect.width, bp.rect.height
red = [x for x in bp.get_drawings() if x.get("fill") and abs(x["fill"][0]-RED_R)<0.02]
def path(x):
    d=[]; 
    for it in x["items"]:
        k=it[0]
        if k=="l":
            p1,p2=it[1],it[2]
            if not d: d.append(f"M{p1.x:.2f} {p1.y:.2f}")
            d.append(f"L{p2.x:.2f} {p2.y:.2f}")
        elif k=="c":
            p1,c1,c2,p2=it[1:5]
            if not d: d.append(f"M{p1.x:.2f} {p1.y:.2f}")
            d.append(f"C{c1.x:.2f} {c1.y:.2f} {c2.x:.2f} {c2.y:.2f} {p2.x:.2f} {p2.y:.2f}")
        elif k=="re":
            r=it[1]; d.append(f"M{r.x0:.2f} {r.y0:.2f}H{r.x1:.2f}V{r.y1:.2f}H{r.x0:.2f}Z")
        elif k=="qu":
            q=it[1]; d.append(f"M{q.ul.x:.2f} {q.ul.y:.2f}L{q.ur.x:.2f} {q.ur.y:.2f}L{q.lr.x:.2f} {q.lr.y:.2f}L{q.ll.x:.2f} {q.ll.y:.2f}Z")
    if x.get("closePath") or True: d.append("Z")
    return "".join(d)
paths = "".join(f'<path d="{path(x)}"/>' for x in red)
x0=352.0
svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0} 0 {W-x0} {H}" width="{W-x0:.0f}" height="{H:.0f}"><g fill="{COLOR}" fill-rule="evenodd">{paths}</g></svg>'
open(A+"/trazos-rojos-brochure.svg","w",encoding="utf-8").write(svg)
print(len(svg), W-x0, H)
