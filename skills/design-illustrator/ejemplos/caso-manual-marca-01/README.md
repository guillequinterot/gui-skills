# Ejemplo: manual de marca (`caso-manual-marca-01`) → Illustrator

Caso completo en [`../../references/06-caso-manual-marca-01.md`](../../references/06-caso-manual-marca-01.md); ficha en [`../../proyectos/caso-manual-marca-01.md`](../../proyectos/caso-manual-marca-01.md). El proyecto (HTML de las 46 láminas, exportaciones, backups) vive en la carpeta del proyecto del usuario, fuera del repo.

`herramientas/` guarda las herramientas **en bruto** de la sesión (no mantenidas; las generales están en `../../scripts/`). Las rutas de los scripts apuntan a `<carpeta-del-proyecto>` y a la carpeta temporal del sistema: ajustarlas si se reutilizan.

| Archivo | Qué hizo |
|---|---|
| `ai_probe.ps1`, `ai_test.ps1`, `ai_test2.ps1` | Abrir un PDF en Illustrator por COM y listar sus textos; probar la unión de líneas/párrafos en una lámina |
| `ai_autosize_probe.ps1` | Buscar propiedades de «Tamaño automático» en `TextFrame` (no existen) |
| `ai_menu_try.ps1`, `ai_dialog_open.ps1` | Probar nombres de `executeMenuCommand` hasta dar con `areatextoptions` y abrir el cuadro |
| `shot.ps1`, `click.ps1` | Capturar el cuadro y pulsar la casilla/OK por coordenadas (primer clic cayó en la ventana equivocada → TOPMOST) |
| `ai_clip_audit.ps1`, `ai_clip_list.ps1`, `ai_clip_clean.ps1`, `ai_clip_rest.ps1`, `ai_clip_final.ps1` | Auditar, listar y limpiar recortes; redibujar el asa de la bolsa |
| `mcp_probe.py` | Sondeo del servidor MCP de Illustrator por HTTP (sin respuesta). **Lee el token de la variable `ILLUSTRATOR_MCP_TOKEN` o de un archivo local fuera del repo; el token no se guarda aquí.** |

Nota: en estas herramientas las funciones de la biblioteca ExtendScript se llaman `aiFixText`, `aiMergeParagraphs`, etc. (en la sesión original llevaban el nombre del cliente como prefijo; se renombraron al anonimizar, igual que en `../../scripts/`).
