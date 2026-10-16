# HANDSHAKE — seo-content-system

> Estado vivo. Se lee en el Paso 0 antes de actuar y se actualiza cuando algo cambia.
> Si este archivo contradice lo que "sabes" de una herramienta, manda este archivo.

| Campo | Valor |
|---|---|
| Versión | 1.2.0 |
| Última actualización | 2026-10-16 por guille |
| Skill principal / padre | ninguna (es skill de primera capa para todo contenido; `web-go-high-level-ia` y `rea-reverse-engineer` son sus sub-skills / apoyo) |
| Llama a | `web-go-high-level-ia` (SEO dentro del constructor de GoHighLevel), `rea-reverse-engineer` (entender competidores), `screaming-frog-seo` (externa y opcional, no está en gui-skills) |
| La llaman | `web-go-high-level-ia`, `direct-visual-design` (cuando el diseño implica textos, metadatos o schema) |

## Herramientas y su estado verificado

| Herramienta / MCP | Estado | Verificado el | Notas |
|---|---|---|---|
| `scripts/capture_learning.py` sin bóveda | verificado | 2026-10-16 | Escribe en `memoria/aprendizaje/inbox/`; se niega (salida 2) si el texto trae términos privados, correos, rutas personales o un `--project` que no sea código de caso |
| `scripts/capture_learning.py` con bóveda de Obsidian | verificado | 2026-10-16 | Probado con una bóveda de prueba y con la configuración heredada `vault`; escribe en `06_Aprendizaje/Inbox/` |
| `scripts/research_update.py` | verificado sin red | 2026-10-16 | Probado con una fuente local; no se probó contra las fuentes oficiales reales en esta migración |
| `scripts/validate_vault.py` | verificado | 2026-10-16 | Sin bóveda valida `memoria/`; con bóveda avisa de carpetas sugeridas que falten y falla solo por frontmatter sin cerrar |
| `scripts/scheduler.py` (`show`) | verificado | 2026-10-16 | `install` (cron / launchd / schtasks) no se probó |
| `scripts/install.py` | verificado | 2026-10-16 | Crea enlaces en un HOME temporal (Windows); en macOS/Linux sin probar; `--force` no se probó con una copia real |
| `scripts/editorial_lint.py` | verificado | 2026-10-16 | Solo `--help`; es un detector de patrones, no sustituye el juicio editorial |
| `tools/build_hosted.py` | verificado | 2026-10-16 | Regenera `skills/seo-content-system-web-hosted/`; `--check` sale con 1 si está desfasado |
| MCP de Obsidian | sin probar | — | Opcional. El mantenedor lo usó con su bóveda; si no responde, la skill sigue con `memoria/` |
| Search Console / GA4 / Clarity / Bing | sin probar | — | Solo si el usuario los conecta; en entornos web, por exportación a Google Sheets |
| `screaming-frog-seo` (skill + MCP `sf_*`) | sin probar | — | Externa y opcional; no viene en gui-skills. Sin ella, pedir exportación CSV/XLSX |
| Herramientas de keywords de pago | no aplica | — | No hay ninguna contratada ni conectada |

Estados: `verificado` · `falla` · `sin probar` · `no aplica en Mac/Windows`.

## Capacidades confirmadas

- Flujo maestro con 15 modos (`research`, `strategy`, `brief`, `write`, `on-page`, `technical`, `local`, `programmatic`, `social-search`, `geo`, `keyword-research`, `entity`, `measure`, `update`, `learn`), 36 referencias, 5 plantillas y un detector editorial.
- Memoria en el repo sin Obsidian: aprendizajes, decisiones, novedades y fuentes en `memoria/`; el registro de casos terminados en `HANDOFF.md`.
- Versión web hosted regenerable de forma determinista desde esta skill (`tools/build_hosted.py`).
- Evidencia que respalda las reglas de GEO (lenguaje natural frente a optimizado, agrupadores): experimento de 90 días de la agencia del mantenedor, publicado en su blog; es evidencia direccional.

## Pendientes abiertos

- [ ] Invocar la skill en una sesión nueva tras la migración al repo y confirmar que el Paso 0 lee HANDOFF/HANDSHAKE y `memoria/` — nunca se ha corrido así.
- [ ] Probar `research_update.py` contra las fuentes oficiales reales y `scheduler.py install` en macOS/Linux/Windows.
- [ ] Revisión del 2026-11-25: contrastar el experimento de lenguaje natural frente a optimizado cuando se publiquen las fases con Claude, ChatGPT, Perplexity y Deepseek, y revisar la volatilidad de las cifras de citación de terceros.
- [ ] Revisión del 2026-11-26 de la versión hosted (o antes si se contrata una herramienta de pago con MCP, o si Claude.ai / ChatGPT lanzan conector nativo de Search Console/GA4).
- [ ] Validar o descartar las reglas candidatas de `HANDOFF.md` §5 cuando se repitan en otros casos.
- [ ] Decidir si los aprendizajes candidatos que viven en la bóveda privada del mantenedor se migran a `memoria/aprendizaje/inbox/` (con códigos de caso) o se quedan solo resumidos en el HANDOFF.

## Límites conocidos

- No tiene acceso a Search Console, GA4, Clarity, CMS ni SERP salvo que el usuario los conecte; nunca se simula.
- Las afirmaciones sobre citación en IA vienen de un experimento pequeño (dos sitios, un sector, un idioma, datos de Copilot): no extrapolar a otros modelos como hecho.
- El recopilador de novedades solo recopila: el agente debe verificar la fuente completa antes de cambiar una recomendación.
- Ninguna observación de un solo trabajo es regla; todo aprendizaje entra como `candidate`.
- La versión hosted no incluye `keyword-research-ia-local-desktop.md` ni los scripts, y no puede leer ni escribir memoria por sí sola.
