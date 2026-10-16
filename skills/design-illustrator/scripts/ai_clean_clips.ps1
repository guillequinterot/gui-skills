# ai_clean_clips.ps1 — limpia los recortes (clipping masks) del documento ACTIVO de Illustrator y lo guarda.
# Hace una auditoría de solo lectura (-AuditOnly) o la limpieza completa (ver ai_clean.jsx: reglas 1-4).
# Deja SIN TOCAR los recortes que sí recortan algo (los lista: lámina, tamaño y cuánto sobresale el contenido) para decidir.
#
# Uso: powershell -NoProfile -File ai_clean_clips.ps1 [-AuditOnly] [-NoSave]
# Recomendado: copia previa del .ai (carpeta backups/ del proyecto).
param([switch]$AuditOnly, [switch]$NoSave)
$ErrorActionPreference = "Stop"
$lib = Get-Content "$PSScriptRoot\ai_clean.jsx" -Raw -Encoding utf8
$ai = New-Object -ComObject Illustrator.Application
if ($AuditOnly) {
    $body = @"
var d = app.activeDocument;
var a = aiAuditClips(d);
d.name + ': grupos=' + a.grupos + ' | con recorte=' + a.conRecorte + ' | vacios=' + a.vacios + ' | sin efecto=' + a.sinEfecto + ' | que recortan de verdad=' + a.queRecortan + ' | trazados invisibles=' + a.invisibles;
"@
} else {
    $save = if ($NoSave) { "" } else { "d.selection = null; d.save();" }
    $body = @"
app.userInteractionLevel = UserInteractionLevel.DONTDISPLAYALERTS;
var d = app.activeDocument;
var r = aiCleanClips(d);
var s = d.name + ': recortes=' + r.total + ' -> liberados ' + r.liberados + ', vacios borrados ' + r.vacios + ', grupos vacios ' + r.gruposVacios + ', trazados invisibles borrados ' + r.invisibles + ', errores ' + r.errores.length + '\n';
s += 'NECESARIOS (no se tocan): ' + r.necesarios.length + '\n';
for (var i = 0; i < r.necesarios.length; i++) s += '  lamina ' + r.necesarios[i].lamina + ' | recorte ' + r.necesarios[i].clip + ' | hijos ' + r.necesarios[i].hijos + ' | sobresale izq/arr/der/abj ' + r.necesarios[i].sobresale + '\n';
$save
s;
"@
}
Write-Host ($ai.DoJavaScript($lib + "`n" + $body))
