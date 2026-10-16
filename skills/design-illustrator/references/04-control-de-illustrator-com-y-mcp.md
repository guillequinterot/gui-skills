# 04 · Controlar Illustrator: COM + ExtendScript (verificado) y MCP (registrado, sin respuesta)

## Vía verificada: COM + ExtendScript desde PowerShell

```powershell
$ai = New-Object -ComObject Illustrator.Application          # lanza Illustrator si no está abierto
$ai.DoJavaScript("app.version + ' docs=' + app.documents.length")   # ejecuta ExtendScript (ES3) y devuelve el último valor
```

- Verificado con **Illustrator (Beta) 31.0.0** (el COM por defecto lanzó la Beta; en la máquina también hay Illustrator 2025 y 2026). `handshake.py` lo avisa.
- Cada `DoJavaScript` es **atómico y secuencial**: dos clientes COM a la vez se serializan y cambian el documento activo del otro. No lanzar dos procesos.
- El código ExtendScript es **ES3** (sin `let/const`, flechas, `JSON`). Datos: `var X = <json>;` (JSON es JS válido) o `eval`.
- Pasar código largo: leer los `.jsx` como biblioteca y concatenar (`$lib + "`n" + $body`). En here-strings de PowerShell con comillas dobles (`@" … "@`) **se expanden `$var`**: usar `${name}` si va seguido de `:`/`.`; y no escribir `\n` literal dentro del JS (PowerShell/Python lo convierten en un salto de línea real que rompe una cadena JS): usar `' || '` u otro separador.
- Archivos `.ps1` **con BOM UTF-8** (PowerShell 5.1 los lee como ANSI si no) y sin acentos en lo que se compare con títulos de ventana.
- **Coordenadas:** Illustrator es **y hacia arriba**. `artboardRect = [izq, arriba, der, abajo]`; `geometricBounds = [izq, arriba, der, abajo]` (arriba > abajo). El lienzo mide **16 383 pt** alrededor del origen: mesas de trabajo fuera de ese rango dan `AOoC`.
- **Unidades:** un PDF a W × H pt se abre como W × H pt; 1 px del HTML = 1 pt.

### Cosas que NO existen o no funcionan por script (comprobado)

| Intento | Resultado | Alternativa |
|---|---|---|
| `TextFrame.autoSize / autoSizing` | `undefined` (no hay API) | UI: `ai_autosize_text.ps1` |
| `TextFrame.anchor = [x, y]` | `Error 1202 Not implemented` (solo lectura) | `translate` hasta que `anchor` coincida |
| `Document.name = '…'` | se ignora | guardar con `saveAs` antes |
| `app.isValidMenuCommand` | no existe | probar y capturar el error `BKey` |
| `executeMenuCommand('area type options')` y variantes con espacios/mayúsculas | `BKey` | **`'areatextoptions'`** |
| `executeMenuCommand` con `DONTDISPLAYALERTS` | no muestra el cuadro (y no aplica nada) | `DISPLAYALERTS` solo en esa llamada |
| Abrir un PDF multipágina entero | abre solo una página (`PDFFileOptions.pageToOpen`) | un PDF por lámina |

Ids internos de `app.executeMenuCommand` que **sí** funcionan: `selectall`, `deselectall`, `pasteInPlace`, `areatextoptions`; además `app.copy()`.

### Bloquear y desbloquear

- Un **cuadro de diálogo abierto** cuelga todos los `DoJavaScript` (la ventana pasa a «No responde» y la CPU no se mueve). `executeMenuCommand('areatextoptions')` **bloquea hasta que el cuadro se cierre**: se lanza en `Start-Job` y el cuadro se maneja desde otro proceso.
- Para localizar el cuadro: `EnumWindows` + `SendMessageTimeout(WM_GETTEXT, 400 ms)` (un `GetWindowText` normal puede colgar el propio script). Para que quede al frente: `SetWindowPos(HWND_TOPMOST)`. Clics proporcionales a su rectángulo (calibrado: Illustrator 31 español 125 %: casilla en `37/606, 648/765`, OK en `400/606, 702/765`, Cancelar en `521/606, 702/765`).
- Si hay que **cerrar un cuadro a la fuerza**: clic en Cancelar con ese mismo método; nunca terminar el proceso de Illustrator sin permiso del usuario.

## MCP de Illustrator (Beta)

Illustrator 31 (Beta) trae un servidor MCP propio (botón **«MCP y herramientas»**, arriba a la derecha de la ventana). Datos:

- Endpoint: `http://localhost:18412/v1/mcp` (transporte HTTP). Autenticación: cabecera `Authorization: Bearer <TOKEN>`; el token sale de ese panel (empieza por `ilst_`).
- **Registrado en Claude Code el 2026-10-11** (alcance de usuario, nombre `illustrator`) con:
  ```
  claude mcp add --transport http --header "Authorization: Bearer <TOKEN>" --scope user illustrator http://localhost:18412/v1/mcp
  ```
  El token queda en `~/.claude.json`; **no se guarda en esta skill**. Las herramientas aparecerán como `mcp__illustrator__*` en sesiones nuevas **si el servidor responde**.
- **Codex** (no instalado; comando que dio el usuario, token por variable de entorno):
  ```
  set "ADOBE_ILLUSTRATOR_MCP_BEARER_TOKEN=<TOKEN>" && codex mcp add adobe-illustrator --url http://localhost:18412/v1/mcp --bearer-token-env-var ADOBE_ILLUSTRATOR_MCP_BEARER_TOKEN
  ```
- Configuración JSON equivalente (otros clientes): `{"mcpServers":{"adobe-illustrator":{"type":"http","url":"http://localhost:18412/v1/mcp","headers":{"Authorization":"Bearer <TOKEN>"}}}}`.
- **Estado verificado (2026-10-10 y 11):** el puerto escucha y acepta la conexión, pero **no responde ni a `initialize` ni a una petición sin credenciales** (timeout de 40-60 s; `claude mcp list` → «connection timed out after 30000ms»). Illustrator estaba activo y COM funcionaba. Causas por descartar: el servidor necesita activarse/aprobar el cliente en el panel «MCP y herramientas», o un cuadro de diálogo pendiente. **Hasta que responda, usar COM.** Probar de nuevo con `handshake.py` (línea «MCP»).
- Cuando responda: listar herramientas (`tools/list`) y documentar aquí cuáles existen (¿texto de área con tamaño automático? ¿limpiar recortes?). Si alguna evita el clic de interfaz, preferirla.

## Rendimiento y estabilidad

- Un maestro de 46 láminas (~7 000 trazados, ~1 000 textos) tarda ~15 min con el proceso completo. Dividir con `-Max`/`ai_repair_page.ps1` si hace falta.
- Illustrator Beta se cerró solo una vez en una corrida larga (RPC `0x800706BE`/`0x800706BF`); al reabrir ofrece «[Recuperado]». Los documentos abiertos sin guardar se pierden.
