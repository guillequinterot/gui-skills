# HANDSHAKE — direct-visual-design

> Estado vivo. Se lee en el Paso 0 antes de actuar y se actualiza cuando algo cambia.
> Si este archivo contradice lo que "sabes" de una herramienta, manda este archivo.

| Campo | Valor |
|---|---|
| Versión | Sin versión numerada: estado del cierre 2026-10-09 + integración con las sub-skills hasta 2026-10-15 (ver `CHANGELOG.md`); migrada a gui-skills el 2026-10-16 |
| Última actualización | 2026-10-21 por julian (patrones y lecciones de subida a Figma, `caso-web-salud-01`) |
| Skill principal / padre | ninguna: es la skill principal y orquestadora de diseño |
| Llama a | `canva-design`, `design-illustrator`, `web-go-high-level-ia`, `rea-reverse-engineer` (por porción) y las skills secundarias de su tabla de enrutamiento (`figma:*`, `impeccable`, `ui-ux-pro-max`, etc., solo las que existan en el equipo) |
| La llaman | Todo trabajo de diseño la activa primero (regla del `CLAUDE.md` global del usuario); `seo-content-system` y `web-go-high-level-ia` la consultan para dirección visual |

## Siguiente paso recomendado

1. Pedir al mantenedor las decisiones pendientes de `HANDOFF.md` §5 — la más urgente: **¿el hero queda exento del 80/80?** (afecta `SKILL.md`, checklist y validador).
2. Si aprueba la jerarquía fuera de Claude Code, aplicar el texto listo de `HANDOFF.md` §6 en `~/.codex/AGENTS.md` (y `GEMINI.md` solo tras verificar que la skill existe allí), con respaldo previo.
3. En la próxima sesión de diseño real, observar si alguna secundaria de descripción amplia se activa sola; si ocurre, proponer el cambio mínimo de `HANDOFF.md` §5.

## Herramientas y su estado verificado

| Herramienta / MCP | Estado | Verificado el | Notas |
|---|---|---|---|
| `scripts/validate_figma_ready.py` (estático y `--render`) | verificado | 2026-10-09 | Probado con 2 ejemplos; exención header/hero/footer; código de salida 1 si hay errores de múltiplos de 4 |
| Python `-I`, PIL, Playwright + Chrome instalado, servidor estático local | verificado | 2026-10-09 | El servidor local se apaga al terminar |
| Frontmatter de `SKILL.md` | verificado | 2026-10-09 | YAML válido (js-yaml), descripción 887 caracteres (< 1024) |
| Carga en Claude Code | verificado | 2026-10-09 | La sesión mostró la descripción nueva tras instalar |
| Conector MCP oficial de Figma (`whoami`) | verificado | 2026-10-09 | No se leyó ni escribió ningún archivo Figma desde la tarea de creación del método; las escrituras reales se hicieron en el caso `caso-landing-industrial-01` |
| Plugin `plugin:figma:figma` | falla (pide OAuth, no autorizado) | 2026-10-09 | Autorizar desde la configuración de conectores del cliente |
| Nombres de skills secundarias | verificado | 2026-10-09 | Existen en disco en el PC del mantenedor; en otros equipos puede faltar alguna |
| Carga en Codex | sin probar | — | Solo verificación por hash, no de carga |
| Antigravity / VS Code | sin probar | — | Nada instalado ni comprobado |
| Exportar/colocar imágenes en Figma con el conector | verificado | 2026-10-09 | `upload_assets` desde un `RECTANGLE` (ver `conocimiento/figma-use-lecciones-tecnicas.md`) |
| Obsidian (MCP / vault) | no aplica por defecto | — | Capa opcional; la memoria primaria es el repo |

Estados: `verificado` · `falla` · `sin probar` · `no aplica en Mac/Windows`.

## Capacidades confirmadas

- Clasificar el encargo (gráfico / UI-UX / híbrido) y cargar solo las referencias pertinentes; QA estratégico → técnico, con el paso 7 "Listo para Figma" para sitios HTML→Figma.
- Método HTML→Figma completo (1920 / 240 / 80, múltiplos de 4, Fill × Hug) con validador automático y checklist; pasar una landing aprobada a Figma con `use_figma` (caso `caso-landing-industrial-01`, 573 nodos).
- Subir a Figma un sitio completo por tandas sobre una librería propia: componentes con propiedades, páginas con instancias, modales en contexto y propuestas A/B, con alturas verificadas contra el HTML (`caso-web-salud-01`; patrones en `references/html-to-figma-method.md` §11).
- Enrutar a skills secundarias con precondiciones de herramienta (`figma:figma-use` antes de `use_figma`, `figma:figma-design-to-code` antes de `get_design_context`).

## Pendientes abiertos

- [ ] ¿El hero queda exento del 80/80? — hoy exento y marcado "por confirmar".
- [ ] Verificar que la skill **cargue en Codex** (solo hay verificación por hash) y decidir si se aplica la jerarquía en `AGENTS.md` / `GEMINI.md`.
- [ ] Observar en uso real si las secundarias de descripción amplia compiten con la principal.
- [ ] Verificar el paint style `Surface` y los fills duplicados del Figma de `caso-landing-industrial-01` (dato del coordinador, no comprobado) y valores de color/tipografía contra su Figma.
- [ ] `scripts/export_portable.py` no exporta `conocimiento/`, `memoria/` ni `proyectos/`.
- [ ] Capturas de ejemplo: regenerarlas fuera del repo con material propio si se quiere una referencia visual (ver `ejemplos/README.md`).

## Límites conocidos

- Hug = alto por contenido; Fill = ancho 100 % del padre. Escala habitual 8/16/24/32/40/80/120; otros múltiplos de 4 son válidos si el proyecto ya los usa.
- `overflow: hidden` en máscaras de imagen, bandas a sangre y carruseles se considera "realmente necesario" (aviso, no error).
- Hero exento del 80/80 hasta confirmación.
- Si la ruta de la skill no existe en la máquina actual, decirlo y seguir con las referencias empaquetadas.

## Dónde mirar

- Estado, decisiones y registro de trabajos: `HANDOFF.md` · historial: `CHANGELOG.md`.
- Método: `references/html-to-figma-method.md` · patrones: `references/web-patterns-from-examples.md`.
- Base de conocimiento: `conocimiento/`, `ejemplos/`, `memoria/`, `proyectos/INDICE.md`.
- Obsidian (opcional): las claves `obsidian_vault`, `obsidian_registry_note` y `obsidian_projects_folder` de `~/.gui-skills/config.json` dicen dónde registrar además.
