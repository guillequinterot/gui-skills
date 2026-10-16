# HANDSHAKE — seo-content-system-web-hosted

> Estado vivo. **Carpeta generada: no se edita a mano** (solo este `HANDSHAKE.md` y `HANDOFF.md` son manuales).
> Si este archivo contradice lo que "sabes" de una herramienta, manda este archivo.

| Campo | Valor |
|---|---|
| Versión | la de `seo-content-system` en el momento de generar (ver la cabecera de cada archivo y `skills/seo-content-system/HANDSHAKE.md`) |
| Última actualización | 2026-10-16 por guille |
| Skill principal / padre | `seo-content-system` (de la que se genera) |
| Llama a | ninguna |
| La llaman | ninguna (se usa pegada en un Project/GPT, no desde Claude Code) |

## Herramientas y su estado verificado

| Herramienta / MCP | Estado | Verificado el | Notas |
|---|---|---|---|
| `tools/build_hosted.py` (generar) | verificado | 2026-10-16 | Salida determinista; 13 archivos (3 plantillas + 10 documentos de `knowledge/`) |
| `tools/build_hosted.py --check` | verificado | 2026-10-16 | Sale con 0 si está al día y con 1 si falta, sobra o difiere algún archivo |
| Claude.ai Project con estas instrucciones y `knowledge/` | sin probar | — | La instalación se probó en agosto con la versión anterior; no con esta regeneración |
| ChatGPT Project / Custom GPT | sin probar | — | Ídem; el editor de instrucciones de un GPT puede tener un límite de caracteres más estricto |
| Search Console / GA4 / Bing | no aplica | — | Sin conector nativo en ninguna de las dos plataformas; solo vía exportación a Google Sheets |

Estados: `verificado` · `falla` · `sin probar` · `no aplica en Mac/Windows`.

## Capacidades confirmadas

- Se regenera de forma determinista a partir de la skill y detecta cuándo está desfasada (`--check`).
- Cualquier referencia nueva de la skill obliga a decidir si entra a `knowledge/` o se excluye (el script falla si no está clasificada).

## Pendientes abiertos

- [ ] Probar la carpeta regenerada en un Claude.ai Project y en un ChatGPT Project (instrucciones + 10 archivos de `knowledge/`).
- [ ] Revisión del 2026-11-26 (o antes si se contrata una herramienta de pago con MCP, o si las plataformas lanzan conector nativo de Search Console/GA4).
- [ ] Añadir `python tools/build_hosted.py --check` al escáner/CI del repo cuando exista.

## Límites conocidos

- No tiene scripts ni memoria propia: el usuario sube a mano las notas pertinentes (`10-memoria-sin-obsidian.md`).
- Los enlaces entre referencias que apuntan a `references/…` o a archivos excluidos (p. ej. `keyword-research-ia-local-desktop.md`) no resuelven dentro de un Project: son texto de referencia.
- `00-instrucciones-del-proyecto.md` empieza con un comentario HTML de «generado»; puede omitirse al pegarlo.
