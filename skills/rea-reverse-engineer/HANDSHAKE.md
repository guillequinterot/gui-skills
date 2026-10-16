# HANDSHAKE — rea-reverse-engineer

> Estado vivo. Se lee en el Paso 0 antes de actuar y se actualiza cuando algo cambia.
> Si este archivo contradice lo que "sabes" de una herramienta, manda este archivo.

| Campo | Valor |
|---|---|
| Versión | 1.0.1 |
| Última actualización | 2026-10-16 por guille (migración al repo gui-skills; estado del MCP `rea`) |
| Skill principal / padre | ninguna (skill de apoyo transversal) |
| Llama a | ninguna (solo entiende; no construye) |
| La llaman | `direct-visual-design`, `seo-content-system`, `video-editing-ai-agent`, `web-go-high-level-ia`, `canva-design`, `design-illustrator` y cualquier otra, **por porción** |

## Herramientas y su estado verificado

Todo lo de esta tabla se verificó **solo en el Windows 11 del mantenedor**. Para tu máquina:
`python -I scripts/handshake.py` (preflight de solo lectura: Node, REA, navegador, Playwright, enrutamiento).

| Herramienta / MCP | Estado | Verificado el | Notas |
|---|---|---|---|
| Sonda N1 `scripts/web_probe.py` | verificado | 2026-10-15 | Sobre el sitio público de REA: capturas 1440/390, estructura, tipografía, paleta, movimiento, SEO, red, crudo vs renderizado. Playwright 1.59 + Chrome/Edge |
| `scripts/handshake.py` | verificado | 2026-10-15 | Reconoce el Node portátil `node-v24*` en `~/.claude/mcp-servers/` |
| `scripts/install.py --check` | verificado | 2026-10-15 | En el repo comprueba el enlace a `~/.claude/skills/`; `--copy` / `--codex` copian el núcleo |
| MCP `rea` (rea-agents 6.5.0) | **registrado y conectado; sin herramienta de análisis ejecutada** | 2026-10-16 | Registrado el 2026-10-15 (aprobación del mantenedor) con un **Node 24.22.0 portátil** en `~/.claude/mcp-servers/node-v24.22.0-win-x64`; handshake stdio `initialize` + `tools/list` = **207 herramientas** verificado; el servidor **conectó en una sesión de Claude Code el 2026-10-16**; **todavía no se ha corrido ninguna herramienta de análisis real** (p. ej. `inspect_web_page` o `analyze_javascript_application` sobre algo propio) |
| Node del sistema 22.15.0 (mantenedor) | falla para REA | 2026-10-15 | REA exige ≥ 22.19; por eso el Node 24 portátil |
| Skill upstream `reverse-engineer-anything` | instalada por el `setup` de REA; **no invocar directamente** | 2026-10-15 | Puede competir con `rea-reverse-engineer`; conservarla ignorada y vigilar en una sesión real |
| REA en Windows con navegador (`REA_BROWSER_EXECUTABLE`) | sin probar | — | La documentación de REA verifica Linux/Chrome 153; Ghidra en Windows es experimental |
| N3 (binarios, APK, .NET, firmware, WASM, SQLite, pcap) | sin probar | — | Motores externos (Ghidra, JADX…) no instalados; nunca se marca disponible por defecto |
| macOS / Linux | sin probar | — | El Node portátil y el comando de registro de esta guía son de Windows |

## Capacidades confirmadas

- Sonda N1 sobre una web real (8 secciones, 4870 px de alto): coincide con la captura vista.
- Crudo vs renderizado: detecta si el contenido depende de JS (rea.tools: 10 687 vs 5 044 caracteres, no depende).
- Enrutamiento escrito en las skills que la llaman (copias fuente = instaladas, verificadas con `cmp` el 2026-10-15).
- Lectura de REA upstream (repo, SKILL, docs): npm `rea-agents` 6.5.0 = repo `morluto/rea`, commit `42fc6c5`.

## Pendientes abiertos

- [ ] **Ejecutar una herramienta de análisis REA real** en una sesión nueva (`mcp__rea__*` ya aparecen en el listado) y registrar el resultado aquí y en el «Registro de trabajos».
- [ ] Probar que `direct-visual-design` (y las demás) la invoquen solas ante un benchmark real (la regla está escrita, no observada).
- [ ] Decidir si se conserva la skill upstream `reverse-engineer-anything` tras verla competir (o no).
- [ ] Hover, menús, modales, carruseles y flujos: la sonda N1 no los prueba (N2 `capture_browser_scenario` sí, sin probar).
- [ ] Sondas contra sitios con bloqueo de bots, geolocalizados o con intros largas; `--scroll`/`--wait` solo probados una vez.
- [ ] Instalación en Codex / Antigravity / VS Code.

## Límites conocidos

- Una huella de tecnología es un indicio, no una certeza; un valor computado no es el sistema de diseño original.
- Los resultados de REA y de la sonda **llegan al modelo**: aplica la política de datos del proveedor; no pasar nada que el usuario no pueda compartir.
- Observación **pasiva** por defecto; `capture_browser_scenario` ejecuta acciones sobre la página (decirlo).
- Una página por llamada, sin login, CAPTCHA, paywall ni rastreo masivo.
- Las capturas de sitios de terceros **no** se archivan en el repo (`ejemplos/README.md`).
