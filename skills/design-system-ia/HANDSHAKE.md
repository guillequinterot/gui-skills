# HANDSHAKE — design-system-ia

> Estado vivo. Se lee en el Paso 0 antes de actuar y se actualiza cuando algo cambia.
> Si este archivo contradice lo que "sabes" de una herramienta, manda este archivo.

| Campo | Valor |
|---|---|
| Versión | 0.2.0 (borrador; probada en parte con un caso real) |
| Última actualización | 2026-10-27 por guille |
| Skill principal / padre | `direct-visual-design` |
| Llama a | `figma:figma-use` y `figma:figma-generate-library` (Figma), `cpanel-guillequinterot` / `ftp-los-creativos` (publicación en hosting), `rea-reverse-engineer` (benchmarks, por porción), `seo-content-system` (páginas públicas de documentación) |
| La llaman | `direct-visual-design` |

## Herramientas y su estado verificado

| Herramienta / MCP | Estado | Verificado el | Notas |
|---|---|---|---|
| Scripts de `scripts/` (Python 3.9+, sin dependencias) | verificado | 2026-10-27 | 55 pruebas unitarias; `validar_contrato.py` también sobre 33 contratos reales de otro sistema |
| `validar_contrato.py` | verificado (forma y política) | 2026-10-27 | No compara con el código del proyecto ni con Figma |
| `contraste.py` | verificado | 2026-10-27 | Recibe los pares de colores; no lee archivos de tokens |
| `vocabulario_check.py` | verificado | 2026-10-27 | Atributos de etiquetas; no revisa valores ni corrige |
| `comparar_figma_contrato.py` | verificado con datos de prueba | 2026-10-27 | Falta probarlo con una lectura real de Figma |
| `generar_biblioteca.py` + `extraer_modulo.py` | verificado | 2026-10-27 | Probado con el sitio de `caso-ds-01`: 11 módulos, 22 variantes, 83 copias sin vacíos; QA a 1440, 375 y 320 px; la entrega completa (16 archivos, con capa para IA) está en el hosting con `noindex` y SHA-256 verificado. Una herramienta externa de lectura de URLs leyó `llms.txt` y listó los 11 módulos. **Sin probar:** una IA construyendo una página completa solo con la URL; lector de pantalla real; otros navegadores |
| Figma MCP (`use_figma`, solo lectura) | verificado | 2026-10-27 | Lectura de archivos de la comunidad sin duplicarlos; las funciones síncronas de variables no se probaron |
| Figma MCP (escritura) | sin probar | — | Exige previsualizar y aprobar; cargar `figma:figma-use` antes |
| Cálculo automático del estado de un componente | no existe | — | Necesitaría un catálogo de ejemplos y un navegador automatizado |
| Pruebas de teclado, analizador de accesibilidad en navegador, evaluaciones con IA | no existen | — | No se lanzan evaluaciones que gasten turnos de un modelo sin permiso expreso |
| Servidor MCP de otro sistema (Helix) y su instalador de IA | sin probar | — | Por seguridad no se ejecutaron ni se registraron |
| Publicación en hosting / Drive / Figma | sin probar | — | La skill pregunta siempre el destino |

Estados: `verificado` · `falla` · `sin probar` · `no existe` · `no aplica en Mac/Windows`.

## Capacidades confirmadas

- Revisa la forma y la política de contratos (JSON y Markdown mínimo) y declara su alcance.
- Calcula contraste WCAG en claro y oscuro sin redondear antes de comparar.
- Detecta sinónimos prohibidos en atributos reales de HTML, JSX, Astro, Vue y similares, con CRLF.
- Compara propiedades de Figma con el contrato a partir de una lectura guardada.
- Nueve referencias contrastadas con fuentes primarias, cada una con su «Contrastado / No contrastado».
- Diecisiete plantillas con cabecera de uso y perfil.
- Genera la entrega estándar de la documentación: biblioteca de módulos navegable (logo y colores del cliente, referente visual por módulo, botones para copiar HTML, CSS, JSON y un prompt para IA) **más** una capa para IA (`sistema.json`, `llms.txt`, `AGENTS.md`) para que una IA documente y construya con solo la URL.

## Pendientes abiertos

- [~] Primera prueba real con `caso-ds-01` (perfil `website` + `individual`): **hecha en parte el 2026-10-27**: plan de arranque, 4 contratos mínimos, vocabulario con verificador (5 hallazgos reales, sin falsos positivos observados), contraste (14 pares) y página de documentación con `noindex` subida y verificada. **Pendiente:** que el dueño apruebe o cambie las propuestas y envíe cambios visuales; revisión humana con lector de pantalla.
- [ ] Hallazgos de la prueba para mejorar la skill: (1) la regla de salto necesita una categoría «parcial» (un formulario con validación nativa y sin estados de error); (2) `vocabulario_check.py` avisa en los sitios de uso pero el renombre también exige cambiar la definición del componente; (3) falta una plantilla o script para generar la página de documentación (hoy el generador vive en la carpeta del caso); (4) el QA de la página halló tres defectos que una lista de control de documentación debería cubrir (títulos con marcas de formato visibles, tablas sin título, texto menor de 13 px).
- [ ] Validar o corregir lo marcado «sin probar» o «inferencia propia»: MVP por perfil, umbrales de la regla de salto, handoff, contrato mínimo para `website`, reglas de WordPress y Astro.
- [ ] Decidir si el bloque `figma` del contrato se unifica con las claves de otro sistema (hoy tiene forma propia).
- [ ] Probar `comparar_figma_contrato.py` con una lectura real de Figma.
- [ ] Verificador de la tercera comprobación (props del código frente al contrato) y de **valores** del vocabulario.
- [ ] Cálculo del estado de un componente y panel de métricas (hoy solo existen las plantillas).
- [ ] Segundo caso real (`app`) para confirmar el perfil completo.

## Límites conocidos

- Casi todo el método viene de **una sola autora y un solo sistema**; se contrastó con fuentes primarias cada vez que fue posible, pero **ninguna práctica se ha ejecutado en un proyecto propio** todavía.
- El modelo de gobierno `equipo` se apoya en experiencias de empresas grandes, sin medir y sin caso propio.
- Las cifras de los relatos (68 componentes en 3 meses, etc.) son anécdotas, no referencias de plazo.
- No hay verificación de WordPress ni de Astro.
