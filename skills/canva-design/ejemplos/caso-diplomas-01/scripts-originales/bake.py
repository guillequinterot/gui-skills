"""bake.py — ejemplo de la sesión de `caso-diplomas-01` (anonimizado, no mantenido; la versión general es `scripts/bake_assets.py`).

Rasteriza `trazos-rojos-brochure.svg` (ver streak.py) y desvanece el borde de corte de página con un umbral de ruido
alargado en la dirección del trazo (~27 grados), para que el borde parezca de pincel seco. Guarda dos esquinas
(volteo vertical y horizontal) como PNG transparente. COLOR_RGB = color oficial de la marca.
"""
COLOR_RGB = (0xDA, 0x11, 0x1C)
import fitz, numpy as np
from PIL import Image, ImageFilter
A = "assets"   # carpeta de assets del proyecto (entrada y salida)
d = fitz.open(A+"/trazos-rojos-brochure.svg"); p = d[0]
print(p.rect)
SC = 2.0
pix = p.get_pixmap(matrix=fitz.Matrix(SC,SC), alpha=True)
im = Image.frombytes("RGBA",(pix.width,pix.height),pix.samples)
print(im.size)
a = np.asarray(im).astype(float)
H,W = a.shape[:2]
alpha = a[...,3]/255.0
print("alpha mean", alpha.mean())
rng = np.random.default_rng(7)
# anisotropic noise elongated along stroke direction (~27deg from vertical, "\" direction)
def aniso_noise(seed, stretch=34, cell=6):
    r = np.random.default_rng(seed)
    base = r.random((int(H*1.6/cell), int(W*1.6/(cell*stretch)))+(), )
    img = Image.fromarray((base*255).astype('uint8')).resize((int(W*1.6), int(H*1.6)), Image.BICUBIC)
    img = img.rotate(-27, resample=Image.BICUBIC)   # align long axis with streaks
    cx, cy = img.width//2, img.height//2
    img = img.crop((cx-W//2, cy-H//2, cx-W//2+W, cy-H//2+H))
    n = np.asarray(img).astype(float)/255.0
    n = (n-n.min())/(n.max()-n.min())
    return n
n1 = aniso_noise(3)
n2 = np.asarray(Image.fromarray((np.random.default_rng(9).random((H//3,W//3))*255).astype('uint8')).resize((W,H),Image.BICUBIC)).astype(float)/255
n = 0.8*n1 + 0.2*n2
y = np.arange(H)[:,None]/SC           # pt from top edge
fade_len = 190.0
t = np.clip(y/fade_len,0,1)*np.ones((1,W))
keep = np.clip((t*1.25 - n*0.9 + 0.0)*3.2, 0, 1)   # ragged dry-brush onset
a2 = alpha*keep
out = np.zeros((H,W,4),dtype='uint8')
out[...,0], out[...,1], out[...,2] = COLOR_RGB
out[...,3]=(a2*255).astype('uint8')
res = Image.fromarray(out,"RGBA")
res.save(A+"/_trazos_base.png")
res.transpose(Image.FLIP_TOP_BOTTOM).save(A+"/esquina-trazos-sup-der.png")
res.transpose(Image.FLIP_LEFT_RIGHT).save(A+"/esquina-trazos-inf-izq.png")
print("saved")
