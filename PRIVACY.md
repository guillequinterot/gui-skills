# Privacidad en gui-skills

Este repo es privado, pero lo leen varias personas y su historial es permanente. Por eso la regla no es
"está privado, da igual": **los datos de clientes nunca se escriben aquí**. Lo aprendido se conserva; lo
identificable se queda en la computadora de cada quien.

## Qué nunca va en el repo

- **Clientes, marcas y personas:** nombres, logos, sus textos, sus archivos, capturas de sus sitios o de sus
  piezas. En su lugar, un código de caso: `caso-<tipo>-<NN>` o `banco-pruebas-<tema>`.
- **Dominios y direcciones web** de clientes, y enlaces a sus carpetas, tableros o cuentas.
- **Datos de contacto:** correos, teléfonos, direcciones.
- **Rutas personales:** `C:\Users\<usuario>`, `/Users/<usuario>`, `/home/<usuario>`, carpetas de discos con tu
  nombre. Usa marcadores: `~`, `<repo>`, `<skill>`, `<carpeta-del-proyecto>`, `<usuario>`.
- **Credenciales de cualquier tipo:** tokens de GitHub, claves de API, `Bearer ...`, claves privadas,
  contraseñas, cookies.
- **Binarios con contenido de cliente** (imágenes, PDF, comprimidos, archivos de oficina). Si una skill de
  verdad necesita una imagen de ejemplo, debe ser inventada o libre de derechos y revisada a mano.
- **Tu correo personal en los commits:** el correo del autor queda en el historial para siempre. Usa
  `<alias>@gui-skills.local` (el instalador lo configura en el clon).

Lo que sí va: la lección (qué funcionó, qué falló, por qué), las reglas, los comandos, las versiones de las
herramientas, ejemplos **inventados** (`usuario@ejemplo.com`, `C:\Users\<usuario>`).

La equivalencia código -> cliente vive solo en `~/.gui-skills/equivalencias.md` de cada persona.

## Las tres barreras

**1. Términos privados + hook local (la barrera principal).** Cada persona escribe en
`~/.gui-skills/private-terms.txt` los nombres de **sus** clientes, marcas y personas (una por línea; texto plano =
coincidencia sin distinguir mayúsculas y por palabra completa; prefijo `re:` = expresión regular de Python que
distingue mayúsculas; `#` = comentario). Ese archivo no sale de tu computadora y nadie más puede crearlo por ti,
porque solo tú sabes quiénes son tus clientes. Con él, `tools/privacy_scan.py` corre en cada `git commit` (hook
`.githooks/pre-commit`) sobre lo que vas a subir, y también dentro de `log_job.py` antes de escribir un registro.
También revisa los **nombres de archivo**. Además aplica los patrones genéricos: correos, teléfonos,
tokens y claves (GitHub, Anthropic/OpenAI `sk-`, AWS, Google `AIza`, `Bearer`, claves privadas) y rutas
personales. Si bloquea, corrige el texto; nunca saltes el hook.

Falsos positivos: si un hallazgo es un ejemplo inventado y legítimo, agrega una expresión regular a
`tools/privacy-allowlist.txt` (solo cubre ese fragmento de la línea) o termina la línea con el marcador
`privacy-scan: ignore`. Jamás pongas ahí nombres reales.

Los **binarios** (imágenes, PDF, comprimidos, archivos de oficina) no se pueden leer: el escáner los lista como
`binario-revisar` para que los mires tú. Con `--strict-binaries` bloquean.

**2. GitHub Actions.** `.github/workflows/privacy-scan.yml` corre `privacy_scan.py --ci` en cada push y Pull
Request: solo los patrones genéricos, porque GitHub no puede conocer tus términos privados (no deben estar en el
repo). Es la red por si alguien no tiene el hook instalado.

**3. Revisión del mantenedor.** Todo aporte entra por Pull Request y el mantenedor lo lee antes de fusionar. Es la
única barrera que entiende contexto (un cliente descrito sin nombre, una captura reconocible). El acuerdo de no
empujar directo a `main` existe por esto (GitHub Free no permite proteger `main` en repos privados).

Ninguna barrera es perfecta: la primera depende de que tu lista esté completa. Cuando conozcas un cliente
nuevo, agrégalo a `private-terms.txt` ese mismo día.

## Comandos útiles

```
python <repo>/tools/privacy_scan.py                  # todo el repo (tracked + sin rastrear)
python <repo>/tools/privacy_scan.py --staged         # solo lo preparado para commit
python <repo>/tools/privacy_scan.py ruta/a/archivo   # archivos o carpetas concretas
python <repo>/tools/privacy_scan.py --ci             # solo patrones genéricos (como en GitHub)
```

Código de salida 1 = hay hallazgos (`archivo:línea: [categoría] detalle`).

## Si algo se filtra

1. **No lo borres y listo:** un commit que lo quita no lo quita del historial. Avisa al mantenedor de inmediato.
2. **Credenciales:** revócalas primero. Si es el token compartido, el mantenedor lo revoca en GitHub
   (Settings > Developer settings > Fine-grained tokens), crea otro y se lo manda a todos por privado. Si es la
   clave de un servicio, rótala en ese servicio.
3. **Limpiar el historial:** el mantenedor lo reescribe con `git filter-repo` (quitando el archivo o la cadena
   en todos los commits) y hace el force-push a todas las ramas; se coordina para que nadie suba nada mientras
   tanto. GitHub puede conservar copias en la caché de Pull Requests: si importa, se le pide a soporte purgarlas.
4. **Todos vuelven a clonar:** las copias locales tienen el historial viejo y volverían a subirlo. Cada persona
   borra su clon y vuelve a clonar (conserva `~/.gui-skills`, que está fuera del clon), y vuelve a correr el instalador.
5. Después: agrega el término a `private-terms.txt` y, si el escáner pudo haberlo detectado y no lo hizo, avisa
   para mejorar el patrón.
