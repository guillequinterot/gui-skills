# ai_fix_pdf_import.ps1 — arregla un documento YA ABIERTO en Illustrator que viene de un PDF (planos, láminas, CAD):
#   1) une los textos partidos en trozos/letras en UN texto de punto por línea, sin sacarlos de su grupo ni de su sitio (ai_fix_text_inplace.jsx)
#   2) limpia las máscaras de recorte anidadas con el límite visible efectivo; lo que queda oculto se aparta a una capa (ai_clean_deep.jsx)
#   3) infiere párrafos y los une en UN texto de área, verificando que el ajuste de líneas sea idéntico (ai_merge_paragraphs_infer.jsx)
# NO activa «Tamaño automático» (eso mueve el ratón): corre después ai_autosize_text.ps1 y avisa al usuario antes.
# NO resuelve a solas el texto que se sale de la página: eso lo lista (sobresale) y se decide con el usuario.
#
# Uso: powershell -NoProfile -File ai_fix_pdf_import.ps1 [-Dry] [-NoSave]
#   -Dry    solo cuenta y lista, no modifica nada
#   -NoSave no guarda al terminar
# Antes: copia de seguridad del .ai en backups/ y, si el documento no tiene versión «limpia», «Guardar como» un archivo nuevo
# (así el original no se toca). Ver references/07-pdf-importado-ya-montado.md.
param([switch]$Dry, [switch]$NoSave)
$ErrorActionPreference = "Stop"
$ai = New-Object -ComObject Illustrator.Application
$t1 = Get-Content "$PSScriptRoot\ai_fix_text_inplace.jsx" -Raw -Encoding utf8
$t2 = Get-Content "$PSScriptRoot\ai_clean_deep.jsx" -Raw -Encoding utf8
$t3 = Get-Content "$PSScriptRoot\ai_merge_paragraphs_infer.jsx" -Raw -Encoding utf8
$jsDry = if ($Dry) { "true" } else { "false" }
$body = @"
app.userInteractionLevel = UserInteractionLevel.DONTDISPLAYALERTS;
var d = app.activeDocument, out = [];
var lastLayer = null;
for (var q = 0; q < d.layers.length; q++) { if (!d.layers[q].locked && d.layers[q].visible) { d.activeLayer = d.layers[q]; break; } }
out.push(d.name + ': textos antes=' + d.textFrames.length);
if ($jsDry) {
  var c = aiCleanDeep(d, true);
  out.push('DRY recortes: vistos=' + c.vistos + ' liberarian=' + c.liberados + ' vacios=' + c.vacios + ' aApartar=' + c.movidos + ' necesarios=' + c.necesarios.length);
  var p = aiMergeParagraphsInfer(d, true);
  out.push('DRY parrafos candidatos=' + p.cadenas);
} else {
  var r1 = aiFixTextInPlace(d, 0.6);
  out.push('Texto: lineas=' + r1.lineas + ' unidas=' + r1.unidas + ' trozosQuitados=' + r1.trozosQuitados + ' rechazadas=' + r1.rechazadas.length);
  var c = aiCleanDeep(d, false);
  out.push('Recortes: vistos=' + c.vistos + ' liberados=' + c.liberados + ' vacios=' + c.vacios + ' apartados=' + c.movidos + ' errores=' + c.errores.length + ' NECESARIOS=' + c.necesarios.length);
  for (var i = 0; i < c.necesarios.length; i++) { var n = c.necesarios[i]; out.push('   lamina ' + n.lamina + (n.foto ? ' FOTO ' : ' ') + n.clip + ' sobresale izq/arr/der/abj ' + n.sobresale); }
  var p = aiMergeParagraphsInfer(d, false);
  out.push('Parrafos: cadenas=' + p.cadenas + ' unidas=' + p.unidas + ' lineasAbsorbidas=' + p.lineasAbsorbidas + ' rechazadas=' + p.rechazadas.length);
  for (var j = 0; j < r1.rechazadas.length; j++) out.push('   texto no unido: ' + r1.rechazadas[j]);
  for (var j = 0; j < p.rechazadas.length; j++) out.push('   parrafo no unido: ' + p.rechazadas[j]);
}
app.userInteractionLevel = UserInteractionLevel.DISPLAYALERTS;
out.push('textos despues=' + d.textFrames.length);
out.join('\n');
"@
Write-Host ($ai.DoJavaScript($t1 + "`n" + $t2 + "`n" + $t3 + "`n" + $body))
if (-not $Dry -and -not $NoSave) {
    $ai.DoJavaScript("app.userInteractionLevel = UserInteractionLevel.DONTDISPLAYALERTS; app.activeDocument.selection = null; app.activeDocument.save(); app.userInteractionLevel = UserInteractionLevel.DISPLAYALERTS;") | Out-Null
    Write-Host "Guardado. Siguiente: ai_autosize_text.ps1 (mueve el raton ~10 s) y revisar el render lamina por lamina."
}
