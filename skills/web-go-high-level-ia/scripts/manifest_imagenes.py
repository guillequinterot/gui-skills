import os, re, glob, sys
base = sys.argv[1]          # carpeta de la entrega
num = sys.argv[2]           # número de entrega
nombre = sys.argv[3]        # nombre legible (Home, Listado...)
srcdir = sys.argv[4]        # src del proyecto
src = ''
for f in glob.glob(srcdir + '/**/*.ts*', recursive=True):
    if 'components/ui' in f.replace(chr(92), '/'):
        continue
    src += open(f, encoding='utf-8').read() + '\n'
files = sorted(os.listdir(os.path.join(base, 'A-IMAGENES-subir-a-Medios')))
rows = []
for n in files:
    i = src.find(n)
    desc = ''
    if i >= 0:
        m = re.search(r'alt(?:=|:\s*)\{?"([^"]*)"', src[i:i + 900], re.I)
        if m:
            desc = m.group(1)
    rows.append((n, desc))
out = ['# Manifiesto de imágenes · Entrega %s (%s)' % (num, nombre), '',
       'Sirve para emparejar cada URL de Medios con su archivo. Total: %d.' % len(rows), '',
       '| # | Archivo | Qué se ve |', '|---|---|---|']
for k, (n, d) in enumerate(rows, 1):
    out.append('| %d | `%s` | %s |' % (k, n, d or '(logo / sello / decorativa)'))
open(os.path.join(base, 'MANIFIESTO-IMAGENES.md'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print(len(rows), 'con descripción:', sum(1 for r in rows if r[1]))
