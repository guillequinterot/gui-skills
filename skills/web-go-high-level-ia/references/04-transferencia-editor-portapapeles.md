# 04 · Transferencia local → editor del constructor (portapapeles + «Guardar»)

El constructor no permite re-subir archivos. Método verificado (2026-10-13, 22 archivos; operado desde Claude in Chrome, ver 07 §L): **copiar el archivo local al portapapeles de Windows y pegarlo en el editor** con Claude in Chrome (solo en Chrome; no Arc).

## Preparación
- `tabs_context_mcp {createIfEmpty:true}` → tab del proyecto: `https://app.gohighlevel.com/v2/location/<loc>/vibe/projects/<id>?view=codeEditor`.
- Árbol de archivos: se puede expandir carpetas; la caja «Buscar archivos» filtra por nombre **y** por contenido (los resultados salen como carpetas colapsadas: hay que hacer clic en `src` para expandir y recién entonces aparece el archivo → **más fiable navegar el árbol expandido** que buscar).

## Un archivo (receta)
1. **PowerShell:** `Get-Content -Raw -Encoding UTF8 "<ruta>" | Set-Clipboard; (Get-Clipboard -Raw).Substring(0,60)` (comprobar el inicio).
2. **Chrome (`browser_batch`):**
   1. clic en el archivo del árbol;
   2. `zoom` de la franja de pestañas/primeras líneas → **verificar que se abrió el archivo correcto**;
   3. clic dentro del editor (≈ 1100,400), `ctrl+a`, `ctrl+v`;
   4. `ctrl+Home` + `zoom` → **verificar la primera línea pegada** (que sea el archivo y no otra cosa);
   5. clic en **«Guardar»** (≈ 1488,22 en pantalla de 1568 de ancho);
   6. `wait 10` (máx. 10 s por espera) + captura pequeña.
3. Tras guardar, **a veces** el panel pasa a «Vista previa» (se reconstruye): para volver al código clic en `</>` (≈ 522,22). Si no pasó, seguimos en código. **Mirar la captura antes del siguiente lote** para saber en qué vista estamos.

## Trampas (todas ocurrieron)
| Trampa | Efecto | Prevención / arreglo |
|---|---|---|
| **Ctrl+S** | escribe una «s» al final del archivo (y abre autocompletado) | no usarlo; si pasó: `Escape`, `BackSpace` y guardar con el botón |
| Clic en «Guardar» cuando la vista es «Vista previa» | esa esquina es **«Publicar»** | comprobar la vista con captura; **nunca** pulsar sin pedido |
| Búsqueda → clic en el 1.er resultado abre **otra pestaña** (AGENTS.md) | se pega el archivo equivocado | verificar nombre de pestaña + primera línea; `ctrl+z` y reintentar |
| El constructor **abre pestañas `vibepreview`** y pisa el portapapeles | se pega una URL en un archivo (rompe la compilación) | re-copiar justo antes de pegar y **verificar la primera línea**; cerrar pestañas extra; reparar re-pegando |
| Recargar el panel (`navigate`) tarda ~20 s («Vamos a vibrar») | pierde estado del árbol | no recargar; reabrir con `?view=codeEditor` solo si hace falta |
| `screenshot` agota 5-30 s con la ventana oculta | error | reintentar |
| `scroll_amount` máx. 10 | error de validación | repetir |
| El código vive en un iframe de otro origen | `get_page_text`/`find` no leen el código | verificar con `zoom` y, después, en la vista previa |
| Guardar durante la compilación anterior | tarjeta «Compilación fallida» temporal | esperar; la siguiente compilación la reemplaza |

## Orden de pegado (para que la vista previa no se rompa a medias)
`<p>-data.ts` (exporta lo nuevo) → componentes que lo usan → `__root.tsx` (shell) → `index.tsx` y rutas → `AGENTS.md`/`README.md`. Entre medias puede verse un header duplicado: es esperado.

## Verificación posterior
Pestaña propia en `https://preview-<id>.vibepreview.app/` y script JS: `h1`, `header.site-header`, `footer`, `main > section`, imágenes rotas, `fetch` de cada ruta (200 / `<title>` / `noindex`). Cerrar la pestaña.

## Si cambia la interfaz
Las coordenadas se tomaron en una ventana de 1568×726 (capturas). Si cambia, tomar una captura completa y recalcular; el patrón (clic → verificar → pegar → verificar → guardar) no cambia.

## Regla reforzada (2026-10-13, tras 2 pegados erróneos)
**Pegar y guardar en llamadas separadas:** 1) `Set-Clipboard` → 2) pegar + `ctrl+Home` + captura de la primera línea → 3) solo si es correcta, «Guardar». El portapapeles es compartido con el usuario (que trabaja a la vez) y el constructor también lo pisa.
Para añadir contenido al final de un archivo (datos, CSS) sin pisar lo que la IA haya escrito: `ctrl+End` y pegar solo el bloque nuevo (con un salto de línea inicial).
