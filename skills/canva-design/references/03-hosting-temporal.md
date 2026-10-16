# 03 · Hosting temporal para la importación

Canva solo importa HTML por **URL pública HTTPS**. Esto implica publicar archivos en internet un rato. Reglas:

1. **Autorización explícita del usuario por tarea.** Se le dice: qué archivos, a qué dominio, que se borrarán al terminar. "Sí, súbelo y bórralo después" vale para esa tarea; la siguiente se vuelve a pedir (así se hizo en las dos rondas de `caso-diplomas-01`).
2. **Subir lo mínimo** (v1.1: un solo HTML por programa con sus assets en la misma subida; **sin fuentes TTF**: el importador ignora `@font-face`; nada de HTML de sondeo fuera de la lista autorizada sin avisar): el HTML y los assets que `upload-asset-from-url` necesita (Canva no descarga las `<img>` del HTML pero sí necesita URL pública para subir el asset). Nada de datos personales extra (en `caso-diplomas-01`: un nombre de pila de ejemplo y texto del diploma).
3. **Carpeta con sufijo aleatorio y prefijo `_tmp-`** (`_tmp-<slug>-q8m2x5`): no listable, no enlazada. `temp_host.sh cleanup` solo borra carpetas `_tmp-*`.
4. **Borrar apenas termine la importación y la subida de assets** (no al final de todo el trabajo) y comprobar `404`.
5. Cero credenciales en notas o código: se usa una llave OpenSSH ya autorizada por el usuario. `scripts/temp_host.sh` lee host, usuario, puerto, llave y dominio de las variables de entorno `CANVA_TMP_HOST`, `CANVA_TMP_USER`, `CANVA_TMP_PORT`, `CANVA_TMP_HOST_KEY`, `CANVA_TMP_DOMAIN` o de las claves `canva_tmp_*` de `~/.gui-skills/config.json` (fuera del repo); sin ellas no sube nada. Si el usuario tiene una skill de acceso a su hosting (p. ej. una de cPanel), úsala para el acceso y respeta sus límites.

## Dominio y certificado

Requisito del importador: **HTTPS con certificado válido** en un dominio que apunte al hosting del usuario.

| Dominio | ¿Sirve? |
|---|---|
| Dominio raíz del hosting del usuario (`https://<tu-dominio>/`) con SSL válido | **Sí** |
| Subdominios de otros proyectos (producción, staging con datos reales) | No los uses: no mezcles la importación con proyectos vivos |
| Subdominios de prueba **sin SSL válido** (curl error 60) | **No**: Canva no importa |
| Subdominios protegidos con clave (HTTP 401) | No: el importador no puede leerlos |

Si hay otro dominio con SSL válido y sin mezclar con producción, preferirlo y anotar aquí cuál es (sin guardar credenciales).

## Comandos

```bash
bash scripts/temp_host.sh --dry-run upload <slug> "<carpeta>" diplomas-v2-20x14.html assets/a.jpg assets/b.png   # ver qué haría
bash scripts/temp_host.sh upload <slug> "<carpeta>" diplomas-v2-20x14.html assets/a.jpg assets/b.png             # → DIR=_tmp-<slug>-xxxxxx
bash scripts/temp_host.sh verify  _tmp-<slug>-xxxxxx diplomas-v2-20x14.html assets/b.png
#  ... import-design-from-url + upload-asset-from-url con https://<tu-dominio>/_tmp-.../...
bash scripts/temp_host.sh cleanup _tmp-<slug>-xxxxxx        # debe imprimir 404
```

## Bug corregido en v1.1
`temp_host.sh upload` con **varios** archivos subía una carpeta vacía (`tar` recibía `"$@"` como un único argumento). Corregido en la fuente (cada archivo como argumento propio; admite espacios). Si se usa una versión instalada antigua: subir con `tar -cf - … | ssh … "cd ~/public_html/$DIR && tar -xf -"`.

## Qué decirle al usuario al terminar

"Subí los archivos un momento a `<dominio>` para poder importar y ya los borré (devuelven 404)." Y listar los diseños intermedios que quedaron en su cuenta de Canva.

## Si el usuario NO autoriza

Alternativas (peores, avisar de la pérdida): reconstruir por API (`edit-design`: sin control de fuente ni espaciado → tipografía por defecto que el usuario deberá cambiar) o entregar el HTML + assets + `HANDOFF` con la tabla de capas para montaje manual en Canva.
