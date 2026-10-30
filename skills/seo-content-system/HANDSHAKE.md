# HANDSHAKE — seo-content-system

> Estado vivo. Se lee en el Paso 0 antes de actuar y se actualiza cuando algo cambia.
> Si este archivo contradice lo que "sabes" de una herramienta, manda este archivo.

| Campo | Valor |
|---|---|
| Versión | 1.7.0 |
| Última actualización | 2026-10-30 (1.7.0: metodología de SEO Skills integrada: auditoría con puntuación, robots.txt, HTML renderizado, title y metadescripción, imágenes, enlazado y clústeres; antes, 2026-10-29: 1.6.0: puerta SEO para sitios de servicios y páginas nuevas, derivada de una auditoría real; antes, 2026-10-23: 1.5.0: segunda y tercera pasada ClickUp + Obsidian + Drive/Sheets integradas; hosted regenerada; decisiones pendientes de Guille resueltas; publicada. ClickUp sigue pendiente por el tope diario del conector) |
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
| `scripts/site_seo_gate.py` (estático y `--live`) | verificado | 2026-10-29 | 16 pruebas sin red externa (`test_site_seo_gate.py`); probado sobre el build real de un sitio de servicios y, en vivo, con las cuatro variantes del host. Los avisos son candidatos, no hallazgos; no mide similitud semántica (usa la frase raíz del título y los primeros 60 palabras), así que no sustituye la verificación con Search Console |
| `scripts/disavow_desde_exportacion.py` | verificado | 2026-10-29 | Prueba con CSV falso (`test_disavow_desde_exportacion.py`); lee exportaciones de Ahrefs/Search Console, agrupa por dominio y separa confianza alta (archivo) de media (revisión). No sube nada: el archivo se sube a mano en Search Console |
| Referencias de SEO Skills (`audit-scoring-and-weights`, `robots-txt-audit-and-generation`, `title-and-description-generation`, `rendered-html-crawl`) | metodología, sin script | 2026-10-30 | Reformuladas de nueve fuentes de un tercero sin licencia declarada. Los umbrales son valores iniciales de su autor. Ningún script de la fuente se copió ni se probó aquí |
| Rastreo con Cloudflare Browser Rendering (`rendered-html-crawl.md`) | sin probar | — | Requiere cuenta, token con permiso de edición sobre Browser Rendering y `.env` fuera del repo; las rutas de la API pueden haber cambiado |
| Lista de 22 user-agents de IA (`robots-txt-audit-and-generation.md`) | sin verificar | 2026-10-30 | Tomada de `seo-skills.com`; confirmar nombre y función de cada bot en la documentación de su proveedor antes de bloquearlo en un cliente |
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
- [ ] (1.7.0) Decidir si se implementan como scripts propios (solo biblioteca estándar, con pruebas) las piezas que la fuente resolvía con código: extractor de metadatos con peso real de imágenes, grafo de enlaces (huérfanas, profundidad, anchors) y agrupador léxico de keywords. Hoy son solo metodología.
- [ ] (1.7.0) Ajustar con casos reales los pesos de `audit-scoring-and-weights.md` (30/25/20/15/10), las deducciones y los rangos 45 a 55 / 150 a 160, y probar `rendered-html-crawl.md` con una cuenta de Cloudflare.
- [ ] (1.7.0) Verificar los nombres de los bots de IA nuevos contra la documentación de cada proveedor y registrarlos en `official-source-register.md`.
- [ ] Validar o descartar las reglas candidatas de `HANDOFF.md` §5 cuando se repitan en otros casos.
- [ ] Decidir si los aprendizajes candidatos que viven en la bóveda privada del mantenedor se migran a `memoria/aprendizaje/inbox/` (con códigos de caso) o se quedan solo resumidos en el HANDOFF.

## Límites conocidos

- No tiene acceso a Search Console, GA4, Clarity, CMS ni SERP salvo que el usuario los conecte; nunca se simula.
- Las afirmaciones sobre citación en IA vienen de un experimento pequeño (dos sitios, un sector, un idioma, datos de Copilot): no extrapolar a otros modelos como hecho.
- El recopilador de novedades solo recopila: el agente debe verificar la fuente completa antes de cambiar una recomendación.
- Ninguna observación de un solo trabajo es regla; todo aprendizaje entra como `candidate`.
- La versión hosted no incluye `keyword-research-ia-local-desktop.md` ni los scripts, y no puede leer ni escribir memoria por sí sola.

## 2026-10-23 · Actualización a 1.3.0
- Se instala seo-content-system 1.3.0 (marcas [ClickUp], [Obsidian], [Sheets] y [Drive]): nuevas referencias, plantillas en assets/templates y docs/CAMBIOS.md + docs/INVESTIGACION-CLICKUP-SEO.md.
- Respaldo de 1.2.0: D:\guille-diseno\skills\_respaldos\seo-content-system-v1.2.0-2026-10-23. <!-- privacy-scan: ignore -->
- Plantillas de proyecto: D:\guille-diseno\skills\seo-plantillas-proyecto. <!-- privacy-scan: ignore -->


## 2026-10-23 · Actualización a 1.4.0
- Revisión externa de solo lectura de la skill completa; informe fuera del repo (carpeta de revisiones del usuario).
- Aplicado: principios 18-20 (retiro de datos, roadmap como «próximamente», schema sin marcadores, sin `Offer` vacío, sin duplicar el grafo de Rank Math); paso 2 (investigar carpeta y sitio antes de preguntar); paso 8 (higiene de archivos en PowerShell, YMYL); editorial-quality-gates §8-10; schema-markup-for-ai-citation (productos sin precio, plugins SEO y ajustes globales); structured-data (validación); technical-audit-by-finding (riesgo y ámbito, entrega completa con brief por hallazgo); task-brief y audit-findings-matrix.csv con riesgo, ámbito, reversión, verificación y brief; notas en technical-seo-guidelines y drive-deliverables; manifest 1.4.0.
- Pendiente de decisión de guille: rutas personales en la entrada 1.3.0 (bloquean privacy_scan), regenerar versión hosted (knowledge-map sin las plantillas nuevas), tope de imagen 100 KB frente a 150 KB, unificar rangos de title/meta y escalas de prioridad/estado, flag `--sin-chequeo-privacidad` de capture_learning.py, script nuevo de chequeo de entregables, fusiones y borrados propuestos. No se hizo commit.


## 2026-10-23 · Actualización a 1.5.0 (borrador, sin commit, sin publicar)
- Segunda pasada por ClickUp (6 agentes de solo lectura, parcial por el tope de 1.000 llamadas/día del conector), Obsidian (5 notas) y, sin integrar todavía, Drive/Sheets. Cinco referencias nuevas, 18 ampliadas (sección `[ClickUp 2]`), principios 21-22 en `SKILL.md`, `knowledge-map.json` con 5 fuentes nuevas. Detalle y pendientes en `HANDOFF.md` (entrada 2026-10-23 · Segunda pasada).
- **Herramienta ClickUp:** verificada para lectura. `task.get_many` no devuelve descripciones (solo `content_size`, checklists, subtareas, adjuntos); la descripción se lee con `clickup_get_task`. **Tope de 1.000 llamadas/día para todo el workspace**: planificar el cupo. No se escribió nada en ClickUp.
- **MCP de Obsidian:** expiró (CONNECT_TIMEOUT) en esta sesión; se leyó la bóveda directo desde disco.
- **Estado de integración de Drive/Sheets:** integrada desde las notas de estructura de los agentes (que se detuvieron antes de cerrar): `sheets-workbook-templates.md` §10, `drive-deliverables-and-guidelines.md` §12 y 16 plantillas. **Hosted:** regenerada, `build_hosted.py --check` = AL DIA. **Copia de distribución** `seo-content-system-1.4.0` desfasada respecto al clon (sincronizada y renombrada a 1.5.0 el 2026-10-23).
- **Conector de ClickUp (2026-10-23, tarde):** sigue en `RATE_LIMIT_EXCEEDED` (1.000/1.000); reintentar tras el reinicio diario y con 2-3 agentes como máximo.
- **`privacy_scan` sobre la skill:** 8 hallazgos, todos rutas personales ya existentes en HANDOFF y HANDSHAKE (decisión de Guille); referencias, plantillas y hosted limpias.
- Pendiente de decisión de Guille: ver HANDOFF punto 7 (rutas personales que bloquean `privacy_scan`, 100 KB frente a 150 KB, rangos de title/meta, commit y publicación).
