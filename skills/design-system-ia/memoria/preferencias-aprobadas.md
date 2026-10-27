# Preferencias y decisiones aprobadas — design-system-ia

> Solo entra aquí lo que el mantenedor **aprobó** o lo que se **repitió en dos o más casos**. Lo que se observa en un solo trabajo va a `inbox-aprendizajes.md`. Las preferencias del usuario en el trabajo actual y los briefs del proyecto tienen prioridad sobre esta memoria.

## Decisiones del mantenedor (2026-10-26 y 2026-10-27)

| # | Decisión | Efecto en la skill |
|---|---|---|
| 1 | Nombre `design-system-ia`, sub-skill de `direct-visual-design` | Su proceso es obligatorio ante cualquier trabajo de sistemas de diseño; precede a las skills secundarias de diseño |
| 2 | Alcance: método agnóstico con perfil reducido para Figma, WordPress, HTML+CSS (y JS), Astro, React y Next.js; Helix como ejemplo, no se empaqueta | Los perfiles reducidos son obligatorios |
| 3 | Novena referencia de arranque y operación | `references/09-arranque-y-operacion.md` |
| 4 | Verdad por defecto: contrato/código primero; configurable y registrada por proyecto | Si el proyecto parte de Figma, se anota y la deriva se audita en ambos sentidos |
| 5 | Tokens de componente opcionales según el perfil de proyecto (`website` / `app` / `sistema compartido`) | `website`: 2 capas y componente final con sus estados; `app` y compartido: 3 capas y contrato completo |
| 6 | Regla de salto entre perfiles: señales, avisa, nunca cambia sola | Ver referencia 09 §8 |
| 7 | Dos perfiles de gobierno, `individual` (por defecto, se presenta primero) y `equipo`; se elige al arrancar | Referencia 08 |
| 8 | El handoff se define como contrato + página de componente + tabla de nombres, **marcado como inferencia** hasta probarlo | Referencia 04 §9 |
| 9 | Publicación: la skill prepara y **siempre pregunta el destino** (hosting, Google Drive con su enlace, o Figma) | `SKILL.md`, sección «Publicación» |
| 10 | Se construye en una carpeta local y se publica al final solo lo propio | La investigación y la copia de Helix no se publican |
| 11 | Todo se reexpresa y se atribuye (`CREDITOS.md`); cada referencia se contrasta con fuentes primarias | Cada referencia declara «Contrastado / No contrastado» |
| 12 | El primer caso real es el sitio web propio del mantenedor (`caso-ds-01`) | La página de documentación del caso usa `noindex` y solo se sube con autorización expresa |

## Página de documentación del sistema (aprobadas por petición explícita, 2026-10-27)

- Todo módulo y todo hallazgo lleva un **referente visual**; sin imagen no entra.
- **Menú a la izquierda**, tipo panel (no arriba), con el **logo del cliente arriba a la izquierda**.
- El **logo y los colores cambian con cada cliente**: salen del propio sitio, no de la agencia.
- Botón para **volver al home** y, en el pie del sitio, un botón «Design system» con `rel="nofollow"` hacia una página `noindex`.
- Cada módulo con **Copiar HTML, Copiar CSS, Copiar JSON, Copiar prompt** (para que una IA lo duplique), **Ver código** y **Ver CSS del módulo**.
- El código mostrado debe ser **legible** (se detectó un defecto de contraste en los paneles).
- **La entrega es una carpeta** (más fácil de ubicar): la página más una capa para IA (`sistema.json`, `llms.txt`, `AGENTS.md`, `modulos/`), con el **logo de la marca siempre**; si se monta en la web, una IA debe poder documentar todo y construir **solo con la URL** (el prompt maestro está en la página).
- Antes de publicar, **QA** de la página real; los cambios del usuario se aplican a la skill y a la construcción visual.

## Cómo trabajar con el mantenedor (proceso)

- Las referencias y las plantillas se entregaron **de una en una (o por lotes) con su OK entre cada una**. Para trabajos nuevos de gran tamaño, ofrece un plan antes de escribir.
- Declarar siempre lo que **no se comprobó**; no escribir «verificado» sin un verificador.
- La IA propone 2–3 opciones con su efecto y espera; no elige tokens ni valores nuevos.
