# 05 · QA y verificación

No declarar «listo» por que el script no dio error. Se verifica con números **y** mirando.

## Checklist de aceptación (todos deben cumplirse)

| # | Comprobación | Cómo | Criterio |
|---|---|---|---|
| 1 | Páginas y tamaño | `verify_fidelity.py` | N láminas = N páginas, todas W × H pt |
| 2 | Idéntico al original (visual) | `verify_fidelity.py` (píxeles que difieren de 2,07 M) | cada lámina < 6 000 (en `caso-manual-marca-01` el máximo fue 4 697; es suavizado del texto). Una página en blanco da ≈ 2 073 600 |
| 3 | Ningún carácter perdido o cambiado | `verify_fidelity.py` (conjunto de letras por lámina) | «ninguna» |
| 4 | Textos enteros | `ai_audit.ps1` | pocos textos «de una letra» (11 legítimos en `caso-manual-marca-01`: ««», «x»…); ningún texto vacío |
| 5 | Texto de área ajustado | `ai_audit.ps1` | `ajustados al texto` = nº de textos de área |
| 6 | Sin desbordes | `ai_audit.ps1` | `texto de area DESBORDADO = 0` |
| 7 | Fuentes reales | `ai_audit.ps1` y `fitz.get_fonts()` del PDF | solo las de la marca (en `caso-manual-marca-01`: Poppins Light/Regular/Medium/SemiBold) — ninguna `ArialMT` |
| 8 | Recortes | `ai_audit.ps1` / `ai_clean_clips.ps1 -AuditOnly` | `con recorte = 0` (o solo los que el diseño pide, justificados), `invisibles = 0`, grupos vacíos = 0 |
| 9 | Pegado completo | `_informe.txt` | `pegado n/n` en todas las láminas |
| 10 | Mirada humana | abrir 6-8 láminas (portada, la más densa, la de mockups, la última) y comparar con el PNG del HTML | sin desplazamientos, sin texto cortado |

## Notas

- `verify_fidelity.py` acepta el `.ai` (guardado con «Crear archivo compatible con PDF», que es lo que hace el proceso) o el PDF multipágina del maestro.
- Si cambia el **ajuste de líneas** de un párrafo, los píxeles lo delatan (una línea distinta ≈ cientos de píxeles) y la auditoría de caracteres no: mirar las láminas con más texto.
- Tras activar **Tamaño automático** o limpiar recortes, el `.ai` es la versión buena; los PDF generados antes **no** llevan esos cambios. Regenerarlos o avisar.
- No hay verificación de **CMYK/sangrado**: el entregable es RGB; la preparación para imprenta es otro paso.
- Lo que **no** se puede comprobar por script: que «Tamaño automático» esté *activado* (no hay API). Se infiere porque la altura de la caja coincide con la de su texto (`ajustados al texto`); si hay duda, seleccionar un texto y abrir *Opciones de texto de área*.
