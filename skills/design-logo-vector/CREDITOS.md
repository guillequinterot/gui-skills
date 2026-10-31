# Créditos y licencias — design-logo-vector

> Esta skill **reexpresa con palabras propias** el método de las fuentes de abajo y **redistribuye sin modificar** solo scripts con licencia MIT, junto a su texto de licencia (obligación de conservar el aviso de copyright y de permiso). Fecha de la investigación: 2026-10-31. Lo que es criterio propio está marcado «(propio)» en las referencias.

## Fuentes incorporadas

| Fuente | Autoría / licencia | Qué se tomó | Cómo |
|---|---|---|---|
| `kaankiziltug/logo-design-skill` (commit `7340903`, 2026-10-20) | MIT, © 2026 kaankiziltug | Proceso de diseño de logos (brief, mapa de palabras, tipos de marca, conceptos, checkpoint, pruebas, optical corrections, kit), 7 scripts de apoyo | Método **reexpresado** en `references/02`, `04`, `05`; scripts **vendorizados sin modificar** en `scripts/vendor/logo-design-skill/` con su `LICENSE` |
| `nolangz/pixel2svg-html` (commit `ab14240`, 2026-06-26) | MIT, © 2026 Nolan Lai | Vectorizado de logos raster: escalera de complejidad, compuerta de suavidad, ajuste con superposición, cintas, wordmarks | Método **reexpresado** en `references/03`; 6 scripts **vendorizados sin modificar** en `scripts/vendor/pixel2svg-html/` con su `LICENSE` |
| `nolangz/pixel2motion` (commit `e9faedb`, 2026-08-21) | MIT, © 2026 Nolan Lai | Idea de traspaso a animación (SVG semántico, brief de movimiento, contrato del fotograma final) | Solo reexpresada en `references/06` §1; **sin scripts** |
| `op7418/logo-generator-skill` (commit `bf4e9ac`, 2026-04-16) | **Sin archivo de licencia** en el repo | Solo la idea general de flujo (recoger datos → varias variantes → iterar → presentar). Su generador de showcases depende de una clave de API de Gemini | **No se copió texto ni código**; no se incorporó el generador |
| `seb1n/awesome-ai-agent-skills`, ficha `design-and-ui-ux/logo-design` (commit `75865a5`, 2026-08-09) | MIT (repo: © 2026 Burhan Sebin; la ficha declara «AI Agent Skills Community») | Lista de entregables y casos límite (nombre largo, fondo fotográfico, bordado, sub-marcas) | Solo ideas reexpresadas en `references/04` y `05`; sin texto copiado |

## Lo que NO se incorporó, y por qué

- La **biblioteca de 1.400+ SVG** de `logo-design-skill` (y `search_library.py`, `build_catalog.py`, `gallery.html`): cada logo es **marca registrada de su titular**; su propio `TRADEMARKS.md` aclara que la licencia MIT no los cubre. No se redistribuyen.
- Las imágenes de ejemplo de cada repo (marcas ficticias o de terceros).
- `scripts/` de animación de `pixel2motion` y el generador de `logo-generator-skill`.

## Avisos MIT

Los dos textos de licencia completos están en `scripts/vendor/pixel2svg-html/LICENSE` y `scripts/vendor/logo-design-skill/LICENSE`. Aplican **solo** a los archivos de esas carpetas; el resto de la skill (texto, referencias, `handshake.py`, `verificar_vectorizado.py`) es propio del mantenedor.

## Marcas

Esta skill no contiene ni autoriza el uso de logos de terceros. Estudiar cómo se construye una marca no da permiso para calcarla o imitarla.
