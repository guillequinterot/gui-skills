# ai_audit.ps1 — auditoría de SOLO LECTURA del documento ACTIVO de Illustrator: ¿está limpio y editable?
#   - textos: cuántos son de punto / de área, fuentes usadas, textos vacíos, texto de área DESBORDADO (oculto), letras sueltas
#   - recortes: grupos con recorte, cuántos no recortan nada, cuántos recortan de verdad, trazados invisibles, grupos vacíos
# Uso: powershell -NoProfile -File ai_audit.ps1 [-Font Poppins]
param([string]$Font = "")
$ErrorActionPreference = "Stop"
$lib = Get-Content "$PSScriptRoot\ai_clean.jsx" -Raw -Encoding utf8
$ai = New-Object -ComObject Illustrator.Application
$body = @"
var d = app.activeDocument;
var s = d.name + ' | mesas de trabajo=' + d.artboards.length + ' | textos=' + d.textFrames.length + '\n';
var kinds = { punto: 0, area: 0, otros: 0 }, fonts = {}, over = [], empty = 0, single = 0, ajustadas = 0;
for (var i = 0; i < d.textFrames.length; i++) {
  var t = d.textFrames[i], k = t.kind;
  if (k == TextType.POINTTEXT) kinds.punto++; else if (k == TextType.AREATEXT) kinds.area++; else kinds.otros++;
  var ca = t.textRange.characterAttributes;
  var fn = ca.textFont.name; fonts[fn] = (fonts[fn] || 0) + 1;
  var c = t.contents.replace(/\s/g, '');
  if (c === '') empty++;
  if (c.length <= 1) single++;
  if (k == TextType.AREATEXT) {
    var shown = 0; for (var j = 0; j < t.lines.length; j++) shown += t.lines[j].contents.replace(/\s/g, '').length;
    if (shown < c.length) over.push(t.contents.substr(0, 40));
    if (t.height <= t.lines.length * ca.leading + ca.size * 0.6) ajustadas++;
  }
}
s += 'textos de punto=' + kinds.punto + ' | de area=' + kinds.area + ' (ajustados al texto=' + ajustadas + ') | otros=' + kinds.otros + ' | vacios=' + empty + '\n';
s += 'textos de UNA letra (posible defecto de importacion)=' + single + '\n';
for (var f in fonts) s += 'fuente ' + f + ': ' + fonts[f] + '\n';
s += 'texto de area DESBORDADO=' + over.length + '\n';
var a = aiAuditClips(d);
s += 'grupos=' + a.grupos + ' | con recorte=' + a.conRecorte + ' (vacios ' + a.vacios + ', sin efecto ' + a.sinEfecto + ', que recortan ' + a.queRecortan + ') | trazados invisibles=' + a.invisibles + '\n';
s;
"@
Write-Host ($ai.DoJavaScript($lib + "`n" + $body))
