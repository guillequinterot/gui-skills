# 01 — Contrato y alcance

## Contrato de entrada (lo que hay que tener claro antes de empezar)

| Campo | Pregunta | Si falta |
|---|---|---|
| Modo | ¿crear, vectorizar, criticar/rediseñar, entregar o animar? | Inferirlo del pedido y decirlo en una línea |
| Insumo | ¿Hay original? (raster, vector viejo, boceto, captura, PDF) ¿qué calidad tiene? | Si es una foto o captura de baja resolución, decirlo: limita el resultado |
| Derechos | ¿Es la marca del usuario/cliente o está autorizado? | Preguntar solo si hay duda real; nunca vectorizar la marca de un tercero para reutilizarla |
| Destino | ¿Dónde vive? (web, app, impreso, bordado, rotulación, redes) | Asumir web + una tinta + favicon y declararlo |
| Intocables | ¿Qué NO se puede cambiar? (nombre exacto, color de marca, fuente, proporción) | Se preserva todo lo que el usuario declare |
| Formatos | SVG siempre; ¿`.ai`/EPS/PDF? ¿PNG a qué tamaños? ¿favicon? | SVG maestro + PNG 512/1024 |
| Restricciones | Colores, tipografías, competidores a evitar, plazo | Anotar supuestos |

## Contrato de salida por modo

| Modo | Entrega mínima | Evidencia obligatoria |
|---|---|---|
| **crear** | Hoja de conceptos (3) en gris + una frase por concepto + recomendación + riesgo honesto de cada uno. *Nada más hasta que el usuario elija.* | Auditoría SVG y hoja de pruebas de cada concepto |
| **vectorizar** | `logo.svg` (ids por parte, `viewBox` correcto), `render.png`, `superposicion.png`, `reporte.md` de `verificar_vectorizado.py` | IoU **y** inspección visual de la superposición **y** zoom al 400 % de las curvas |
| **criticar** | Diagnóstico por severidad (qué identifica, qué estorba, qué conservar) con corrección concreta | Pruebas de `references/04` ejecutadas o declaradas no ejecutadas |
| **rediseñar** | Decisión refresh vs. rebrand + conceptos como en *crear* | Comparación lado a lado con el logo actual |
| **entregar** | Variantes, PNG, set web, guía de uso de una página, tablero si se pidió | `svg_audit` ≥ ~90 sin FAIL; archivos abiertos y mirados |
| **animar** | SVG con ids semánticos y estructura pensada para movimiento + brief de movimiento (3 palabras, contexto de uso) | El SVG estático ya pasó *vectorizar* |

## Lo que esta skill NO hace

- No garantiza ni sustituye una **búsqueda marcaria**; solo recomienda hacerla.
- No entrega un PNG generado por IA como "el logo": un raster nunca es el maestro. Se **vectoriza o se redibuja** y se verifica.
- No convierte tipografía licenciada en contornos para uso comercial sin que el usuario confirme que la licencia lo permite.
- No publica ni sube nada a internet; el hosting o la entrega a un tercero necesitan autorización por tarea.
- No hace el pipeline completo a Illustrator/Canva/Figma: lo delega (ver `06`).
- No inventa el contenido de la marca (nombre, eslogan): usa lo que dio el usuario, literal.

## Dónde van los archivos

Carpeta del proyecto del usuario, con esta forma (la nota de Obsidian, si existe, enlaza la carpeta):

```
<carpeta-del-proyecto>/logo/
  00-original/          # el raster o vector recibido, intacto
  01-conceptos/         # concepto-a-v1.svg …  + hoja de conceptos
  02-vectorizado/       # logo.svg, render.png, superposicion.png, fit_work/
  03-verificacion/      # reporte.md / reporte.json, hojas de prueba
  04-entrega/           # variantes, PNG, set web, guía de uso, tablero
```

Nunca dentro del repo gui-skills (privacidad: los logos de clientes no se publican).
