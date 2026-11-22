# 00 · Metodología de trabajo en Canva (del mantenedor) — OBLIGATORIA

Dada por el mantenedor el 2026-11-16 para **todo** trabajo en Canva. Va **antes** del pipeline de `01-pipeline-html-a-canva.md`: ese describe *cómo* se monta; esta fija *en qué orden se trabaja, qué se pregunta y qué se revisa*. Si algo choca con un detalle del pipeline, gana esta metodología.

## Orden de trabajo

1. **Analizar primero el o los archivos de Canva.** `resolve-shortlink` + `read-design`: páginas, tamaños, textos, miniaturas, fuentes, colores y estructura. Leer **todo** el archivo, no solo la página de la tarea.
2. **Entender y sacar el diseño existente** (línea gráfica, retícula, tipografías, paleta, elementos repetidos). **Si no hay diseño**, pedir antes de diseñar: UI kit o manual de marca, logo (en vector si existe), imágenes y referencias. No inventar la línea gráfica.
3. **Pruebas de diseño en HTML.** Todo diseño pasa primero por HTML (Canva-ready, ver `01`):
   1. Los HTML se pueden **subir al hosting del usuario** para poder importarlos (autorización permanente del mantenedor, ver «Hosting» abajo).
   2. Después se **importa el HTML a Canva** (`import-design-from-url`) para pasar todo el diseño.
4. **QA visual** (checklist abajo). Es lo más importante de la entrega.
5. **Doble chequeo del diseño base y de la línea gráfica**: comparar lo producido con el archivo/manual original (colores, fuentes, márgenes, uso del logo), no solo con el HTML.
6. **Fotos: edición simple.** Si hay degradados, van en **otra capa**, nunca sobre la imagen editada ni horneados en ella (así se puede cambiar o quitar sin tocar la foto).
7. **Usar elementos nativos de Canva** (marcos, cuadrículas, grupos, alineación, páginas) para organizar, siempre que se pueda.
8. **Al empezar, preguntar siempre:** «¿Quieres que trabaje en el archivo original o en una copia?» (`copy-design`). No tocar el original sin esa respuesta.
9. **Al terminar una tarea, enviar el link de Canva** del diseño final (más la lista de URLs si son varios y de los intermedios que queden en la cuenta).

## Checklist del QA visual

- **Alineación exacta.** Si un elemento va a la derecha, queda perfectamente alineado a ese borde; igual a la izquierda, centros y márgenes. Verificar bordes y ejes con las medidas, no a ojo.
- **Imágenes sin pérdida.** Usar el original sin recomprimir; comprobar resolución efectiva en la pieza final; no ampliar de más ni cambiar de formato con pérdida. Comparar la nitidez del export con el original.
- **Textos organizados y con su tipografía.** Familia, peso, tamaño y jerarquía de la línea gráfica; interlineado y alineación consistentes; nada cortado ni desbordado.
- **Superposiciones.** Cuidado al poner textos uno encima de otro. Y especialmente **texto sobre imagen**: si no hay contraste y no se lee, mejorarlo (capa de degradado u overlay propia, panel, cambio de posición o de color), nunca dejarlo ilegible.
- **Doble chequeo base/línea gráfica** (punto 5 del orden).
- **Verificar exportando** y mirando cada página (regla dura 10 de `SKILL.md`); decir con franqueza qué no se pudo comprobar.

## Hosting de los HTML (cambia la regla de «autorización por tarea»)

- El mantenedor autorizó de forma **permanente** subir a su hosting los HTML de diseño para importarlos a Canva (2026-11-16). Para quien use esta skill sin esa autorización dicha por escrito, sigue valiendo la regla de `03-hosting-temporal.md`: pedir permiso por tarea.
- Lo que **no cambia**: subir lo mínimo, carpeta `_tmp-…` con sufijo aleatorio, borrar apenas termine la importación y comprobar `404`, avisar al usuario de lo que se subió y se borró. La autorización cubre los HTML de diseño y sus assets, **no** otros archivos del usuario.
- El acceso sale de `~/.gui-skills/config.json` (`canva_tmp_*`) o de la skill de acceso a hosting del usuario; nunca de notas o código.
