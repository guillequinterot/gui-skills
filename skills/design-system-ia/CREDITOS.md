# Créditos y licencias — design-system-ia

> Esta skill **reexpresa con palabras propias** ideas y métodos de las fuentes de abajo. No copia textos, imágenes ni código de terceros; los nombres de campos técnicos (por ejemplo, los del contrato) se mencionan solo como referencia. Lo que es **inferencia propia** está marcado como tal en cada referencia. Fecha de la investigación: 2026-10-27.

## Fuente principal: Helix (MIT)

- **Helix**, sistema de diseño de código abierto de **Marta Conde**. Repositorio `MartaCondeDesign/helixds`, revisado en el *commit* `394823a` (2026-10-22). Licencia **MIT**, «Copyright (c) 2026 Marta Conde».
- Se usó como **ejemplo trabajado** (contratos, esquema, tokens DTCG, vocabulario de props, guía para agentes, ejecutor de accesibilidad, estado calculado y gobierno) y se **probó en local, en una carpeta aislada**, sin ejecutar `setup:ai` ni registrar su servidor MCP. Ninguna parte del código de Helix se incluye en esta skill.
- Aviso MIT: la licencia exige conservar su aviso de copyright y de permiso en las copias o partes sustanciales del software. Esta skill no redistribuye partes sustanciales; si en el futuro se incorpora código o contenido de Helix, se añadirá el texto completo de la licencia.

## Otras obras de la misma autora (reexpresadas)

| Obra | Tipo | Licencia |
|---|---|---|
| «Measure Design System Impact», partes 1 y 2 | Artículos en su sitio web | No declarada en lo leído |
| «Make your design system agent-ready (5 steps)» | Artículo | No declarada en lo leído |
| «Naming Design Tokens» | Artículo | No declarada en lo leído |
| Glosario de IA para sistemas de diseño (120 páginas) y glosario de tokens | Bases de datos públicas en Notion | No declarada en lo leído |
| «AI-ready Design System · Helix» (archivo de la comunidad de Figma) | Archivo de Figma | No declarada en lo leído |
| «Name components, properties and values in Design Systems» (archivo y página de la comunidad de Figma) | Archivo de Figma | **CC BY 4.0** (según su página de la comunidad) |
| «Fundamentos del sistema de diseño» (charla de un equipo de Celonis) | Presentación en Figma | No declarada en lo leído |
| Vídeos de su canal: documentar un sistema (MVP) · preparar la documentación para la IA · cómo empezar · mi nuevo rol con la IA · nuevas métricas · feedback con Supernova · escalar con IA · de Figma a código con Supernova | YouTube (subtítulos automáticos) | No declarada |
| Charla «Design Tokens Glossary» (Into Design Systems Conference) y webinars de The Hero Camp (tokens, sistema tipográfico) | YouTube | No declarada |
| Conversaciones: podcast «La diseñería» (T2 E5) y una entrevista de podcast sobre qué es un design system | YouTube | No declarada |

**Atribución CC BY 4.0:** las ideas del archivo de nombres de componentes, propiedades y valores (método de cuatro pasos, tablas de sinónimos) se reexpresan y se atribuyen a su autora, con enlace a su licencia: <https://creativecommons.org/licenses/by/4.0/>. No se hicieron cambios al archivo original (solo se leyó).

**Otros archivos de la comunidad de Figma** leídos como referencia de estructura y textos (kits de documentación, lista de control de componentes): su autoría y licencia no se verificaron; solo se reexpresaron ideas generales.

## Normas y documentación primaria contrastadas

| Tema | Fuente |
|---|---|
| Criterios de accesibilidad | W3C, *Web Content Accessibility Guidelines (WCAG) 2.2* |
| Diálogo modal (foco, Escape, retorno del foco) | W3C WAI, *ARIA Authoring Practices Guide* |
| Movimiento reducido | MDN, `prefers-reduced-motion` |
| Variables CSS | MDN, *Using CSS custom properties* |
| Versionado | *Semantic Versioning 2.0.0* (semver.org) |
| Esquema de contratos | JSON Schema (json-schema.org; versión vigente 2020-12) |
| Formato de tokens | Design Tokens Community Group, formato 2025.10 (informe final de un grupo comunitario; **no** es un estándar del W3C) |
| Propiedades de componentes en Figma | Documentación para desarrolladores de Figma |
| `AGENTS.md` | agents.md (formato abierto) |
| `llms.txt` | llmstxt.org (propuesta, no estándar) |
| Hooks y herramientas | Documentación de Claude Code; Model Context Protocol |
| Evaluaciones | Guía de evaluaciones de Anthropic |
| Indexación | Documentación de Google sobre `noindex` |
| Definición, beneficios y coste de un sistema de diseño | Nielsen Norman Group, *Design Systems 101* |
| Modelos de equipo | Nathan Curtis, *Team Models for Scaling a Design System* (2015) y *The Fallacy of Federated Design Systems* (2024) |
| Librerías abiertas | Documentación de shadcn/ui y de Mantine |

## Qué no se publica

La investigación completa (fichas de cada fuente, transcripciones, matriz de síntesis, copia local de Helix y su prueba) vive **fuera del repositorio**, en la carpeta local del mantenedor. Los casos se nombran solo con código (`caso-ds-NN`); la equivalencia con el cliente real vive en `~/.gui-skills/equivalencias.md`, fuera del repo.
