# 01 · Pipeline HTML → Illustrator (la receta)

Orden fijo. Cada paso tiene un criterio de salida. Rutas con `<proyecto>` = carpeta del proyecto (p. ej. `<carpeta-del-proyecto>`) y `<skill>` = `<repo>/skills/design-illustrator`.

## 0 · Preflight

```
python -I <skill>\scripts\handshake.py --font Poppins
```
Debe dar `TODO LISTO`. Si Illustrator no está abierto, la fuente solo se puede comprobar abriendo Illustrator (si viene de Adobe Fonts no hay archivos en Windows). Si Poppins (o la fuente del diseño) **no** está disponible en Illustrator: instalarla antes (Google Fonts o Adobe Fonts) y reiniciar Illustrator; sin ella la sustituye al abrir.

## 1 · HTML aprobado y validado

Reglas del HTML en [03](03-html-illustrator-ready.md). El HTML debe estar **aprobado por el usuario** y pasar su validador de proyecto (en `caso-manual-marca-01`: el validador de páginas del proyecto, `scripts/validate_pages.py`, = 0 errores). Fuentes cargables al imprimir (Google Fonts con internet, o `@font-face` local).

## 2 · PDF crudo a tamaño exacto

```
python -I <skill>\scripts\export_pdf.py --root <proyecto> --pages "paginas/p[0-9][0-9]-*.html" --size 1920x1080
```
Salida `<proyecto>\export\pdf\*.pdf`: una página de 1920 × 1080 pt por lámina, texto vivo, vectores, sin imágenes raster (`_informe.txt` lo lista). **Es un intermedio**: abierto en Illustrator da una letra por texto.

## 3 · Estructura de párrafos

```
python -I <skill>\scripts\extract_paragraphs.py --root <proyecto> --pages "paginas/p[0-9][0-9]-*.html" --size 1920x1080
```
Salida `<proyecto>\export\dom\*.json`: por bloque de texto de varias líneas, su caja (x, ancho), alineación, tamaño, interletraje, interlineado y las líneas tal como las maquetó el navegador.

## 4 · Construir el maestro en Illustrator

Antes de lanzar: **avisar al usuario** (Illustrator trabaja ~15 min con ventanas que cambian; guardar sus documentos abiertos; el proceso no cierra nada pero Illustrator Beta puede cerrarse solo).

```
powershell -NoProfile -File <skill>\scripts\ai_pipeline.ps1 -Root <proyecto> -Master "nombre-maestro" [-Width 1920 -Height 1080 -Cols 6] [-Max N para probar]
```
Por lámina: abre el PDF → `aiFixText` (letras → un texto por línea, mismo tracking) → `aiMergeParagraphs` (líneas → texto de área, solo si el ajuste de líneas coincide) → guarda PDF editable → copia y pega en su mesa de trabajo (reintenta 3 veces). Al final `aiCleanClips`, guarda `<proyecto>\export\illustrator\<maestro>.ai` y `.pdf` y **deja el `.ai` abierto**. Informe en `_informe.txt` (letras → líneas → bloques, `sin unir`, pegado `n/n`).

Probar SIEMPRE antes con `-Max 3` (y `-OutDir export\illustrator-prueba`) y revisar el informe.

## 5 · Tamaño automático

```
powershell -NoProfile -File <skill>\scripts\ai_autosize_text.ps1
```
Con el `.ai` maestro como documento activo y **ningún cuadro de diálogo abierto**. Selecciona todos los textos de área, abre *Opciones de texto de área*, marca «Tamaño automático» y OK. **Mueve el ratón ~10 s: avisar.** Verifica que cada caja midió lo que mide su texto. Luego guardar (`Ctrl+S`).

## 6 · Auditar y verificar

```
powershell -NoProfile -File <skill>\scripts\ai_audit.ps1
python -I <skill>\scripts\verify_fidelity.py --raw <proyecto>\export\pdf --master <proyecto>\export\illustrator\<maestro>.ai
```
Criterios: ver [05](05-qa-verificacion.md). Si una lámina sale en blanco o con error: `ai_repair_page.ps1 -Root <proyecto> -Page N -Master <maestro>` y repetir el paso 5.

## 7 · Entrega y registro

Entregar las rutas del `.ai` (para trabajar) y del PDF editable; decir qué se verificó. Si el PDF maestro/individuales se generaron **antes** de la limpieza o del «Tamaño automático», **avisar** de que el `.ai` es la versión al día (o regenerarlos desde él). Registrar el trabajo con el Paso final del protocolo gui-skills (entrada en el Registro de trabajos del `HANDOFF.md`, con `tools/log_job.py`); HANDOFF del proyecto en la carpeta del usuario y, si usa Obsidian, su nota del proyecto; aprendizajes → `memoria/inbox-aprendizajes.md`.

## Si cambia el HTML

`validar HTML → export_pdf.py → extract_paragraphs.py → ai_pipeline.ps1 → ai_autosize_text.ps1 → verify_fidelity.py`. Para una sola lámina: regenerar su PDF/JSON y `ai_repair_page.ps1`.
