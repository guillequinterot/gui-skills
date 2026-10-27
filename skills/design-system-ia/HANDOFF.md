# HANDOFF — design-system-ia

> Traspaso entre sesiones y personas: qué es la skill, cómo se instala, qué se decidió y qué se aprendió
> en cada trabajo. Estado vivo (versión, herramientas, pendientes) → `HANDSHAKE.md`. Historial de cambios → `CHANGELOG.md`.

## 1. Qué es y cuándo se usa

Skill **propia** del mantenedor, **sub-skill de `direct-visual-design`** (la principal y orquestadora de diseño). Cubre todo trabajo de **sistemas de diseño**: decidir si hace falta uno, definirlo desde un brief, auditarlo, escribir el contrato de cada componente, construirlo y documentarlo (HTML+CSS, WordPress, Astro, React/Next.js y Figma), verificar paridad código↔Figma, accesibilidad y estado, dejarlo legible para agentes y medirlo. Cuando se pide algo de sistemas de diseño, o se la nombra, **su proceso es obligatorio**.

Nace de analizar el sistema de código abierto **Helix** (MIT, de Marta Conde) y sus fuentes asociadas, contrastando cada referencia con fuentes primarias. Helix es un **ejemplo trabajado**, nunca un estándar ni una dependencia. Créditos y licencias: `CREDITOS.md`.

**Receta corta:** clasificar (perfil de proyecto `website` / `app` / `sistema compartido`; perfil de gobierno `individual` / `equipo`; fuente de verdad) → elegir modo (`auditar`, `definir`, `contrato`, `construir`, `verificar`, `documentar`, `medir`) → leer solo su referencia → ejecutar → verificar con lo que haya y declarar lo no verificado → entregar sin publicar (se pregunta el destino) → registrar.

## 2. Instalación y dependencias

- Viene con el repo gui-skills (`tools/install.ps1` / `tools/install.sh`); no se copia a mano. El instalador enlaza `~/.claude/skills/design-system-ia` al clon. `scripts/install.py --check` detecta ese enlace y no copia nada.
- Dependencias externas:
  - **Python 3.9+**, sin paquetes adicionales (los scripts usan solo la biblioteca estándar).
  - **Figma (opcional):** conector Figma MCP de la sesión; es *deferred* (se carga con `ToolSearch`) y `figma:figma-use` se carga **antes de cada** `use_figma`. Solo lectura por defecto; escribir exige previsualizar y aprobar.
  - **Publicación (opcional):** `cpanel-guillequinterot` o `ftp-los-creativos` para hosting, con su autorización por tarea; Google Drive con el enlace que indique el usuario.
  - **No necesita** navegador headless, Storybook ni Playwright en esta versión.
- Carpeta de la skill:

| Ruta | Contenido |
|---|---|
| `SKILL.md`, `references/` (9), `templates/` (17 + índice), `scripts/` | Núcleo |
| `HANDOFF.md`, `HANDSHAKE.md`, `CHANGELOG.md`, `CREDITOS.md` | Este estado y los créditos |
| `proyectos/` | `INDICE.md` + una ficha por caso (solo código `caso-ds-NN`) |
| `memoria/` | `preferencias-aprobadas.md`, `inbox-aprendizajes.md` |
| `conocimiento/` | `README.md` y `hallazgos-verificados.md` |
| `ejemplos/` | Ejemplos anonimizados por caso |

- La investigación completa (fichas, transcripciones, matriz de síntesis, copia local de Helix y su prueba) **no se publica**: vive en la carpeta local del mantenedor.

## 3. Decisiones vigentes

| Fecha | Decisión | Quién la aprobó | Por qué |
|---|---|---|---|
| 2026-10-26 | Nombre `design-system-ia`; sub-skill de `direct-visual-design`; su proceso es obligatorio ante sistemas de diseño | Guillermo Quintero | Una sola skill para todo el ciclo, bajo la orquestadora de diseño |
| 2026-10-27 | Alcance: método agnóstico con perfil reducido para Figma, WordPress, HTML+CSS (y JS), Astro, React y Next.js; Helix como ejemplo, no se empaqueta | Guillermo Quintero | Es el stack de trabajo real |
| 2026-10-27 | Verdad por defecto: contrato/código primero, configurable y registrada por proyecto | Guillermo Quintero | Encaja con su flujo HTML → Figma |
| 2026-10-27 | Tokens de componente opcionales según el perfil de proyecto; `website` lleva 2 capas, componente final con sus estados y contrato mínimo | Guillermo Quintero | Un sitio no necesita la maquinaria de una aplicación |
| 2026-10-27 | Regla de salto entre perfiles: señales, avisa, nunca cambia sola | Guillermo Quintero | Evitar tanto la sobreingeniería como quedarse corto |
| 2026-10-27 | Dos perfiles de gobierno; `individual` por defecto y se presenta primero; se elige al arrancar | Guillermo Quintero | Casi todo su trabajo es individual |
| 2026-10-27 | Handoff con definición propia, **marcada como inferencia** hasta probarla en un caso real | Guillermo Quintero | Ninguna fuente lo define |
| 2026-10-27 | Publicar = preguntar el destino (hosting, Google Drive con su enlace, o Figma) | Guillermo Quintero | Es publicar contenido; el hosting exige permiso por tarea |
| 2026-10-27 | Todo se reexpresa y se atribuye; cada referencia se contrasta con fuentes primarias y declara «Contrastado / No contrastado» | Guillermo Quintero | Casi todo vino de una sola autora |
| 2026-10-27 | Contrato completo con JSON Schema 2020-12; la raíz prohíbe campos desconocidos y los objetos anidados admiten extras; esquema y validador en `scripts/` | Guillermo Quintero | Atrapar errores de escritura sin frenar la extensión |
| 2026-10-27 | `indice-llms.txt` es plantilla normal; `llms.txt` se trata como propuesta, no estándar | Guillermo Quintero | Capa de descubrimiento separada de la de instrucción |
| 2026-10-27 | Primer caso real: el sitio web propio del mantenedor (`caso-ds-01`); la página de documentación lleva `noindex` y solo se sube con autorización expresa | Guillermo Quintero | Probar `website` + `individual` |

## 4. Registro de trabajos

> Una entrada por trabajo terminado o implementado y aprobado. Solo se agregan entradas al final; las
> correcciones van como entrada nueva. Casos solo con código `caso-<tipo>-<NN>`. Formato:
> `templates/entrada-de-trabajo.md` del repo. Se escribe con `tools/log_job.py`.

<!-- registro:inicio -->

### 2026-10-27 · caso-ds-01 · guille

- **Qué se hizo:** Primera prueba real de la skill con el sitio propio del mantenedor (Astro): plan de arranque, 4 contratos minimos, vocabulario con verificador (5 usos no canonicos), contraste de 14 pares, auditoria con 11 hallazgos y entrega estandar: biblioteca de modulos navegable (menu lateral, logo y colores del cliente, referente visual por modulo, botones Copiar HTML/CSS/JSON/prompt, Ver codigo y CSS del modulo) mas capa para IA (sistema.json, llms.txt, AGENTS.md) subida a una ruta noindex del propio sitio
- **Salió bien:** Extraer el HTML y el CSS reales del sitio evito redibujar componentes; el QA de la pagina real (consola, 320 px, copias, menu movil) encontro defectos que la copia local no mostraba; una herramienta externa de lectura de URLs listo los 11 modulos desde llms.txt
- **Salió mal / incidencia:** El primer panel de codigo era ilegible (el estilo de codigo en linea daba fondo claro a texto claro); la tarjeta que compone un boton salio sin boton hasta declarar dependencias de CSS; un lector que convierte la pagina a texto no ve el HTML de los componentes Incidencia: El verificador de contratos del sistema de referencia no valida el esquema completo; el boton de cerrar el cajon movil apuntaba al boton equivocado; la skill no admitia un sitio de un solo tema en contraste.py
- **Regla candidata:** La entrega de documentacion de un sistema es una carpeta con logo del cliente y capa para IA (sistema.json, llms.txt, AGENTS.md), no solo una pagina
- **Herramientas:** Claude Code, Python 3, Edge headless, navegador integrado

<!-- registro:fin -->

## 5. Reglas candidatas (sin aprobar)

| Regla | Visto en (casos) | Estado |
|---|---|---|
| La entrega de documentacion de un sistema es una carpeta con logo del cliente y capa para IA (sistema.json, llms.txt, AGENTS.md), no solo una pagina | caso-ds-01 | candidata |
