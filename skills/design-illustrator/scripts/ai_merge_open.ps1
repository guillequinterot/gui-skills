# ai_merge_open.ps1 — une las líneas de cada párrafo en texto corrido DENTRO de un documento ya abierto en Illustrator
# que tenga una mesa de trabajo por lámina (p. ej. el maestro generado por una versión anterior del proceso).
# No guarda ni cierra nada: el documento queda modificado y abierto para revisarlo (Ctrl+Z deshace por pasos).
#
# Uso: powershell -NoProfile -File ai_merge_open.ps1 -Root D:\ruta\proyecto -Doc "nombre-del-documento.ai" [-From 1] [-To 46]
param([Parameter(Mandatory = $true)][string]$Root, [Parameter(Mandatory = $true)][string]$Doc, [int]$From = 1, [int]$To = 0,
      [string]$PdfDir = "export\pdf", [string]$DomDir = "export\dom", [int]$Width = 1920)
$ErrorActionPreference = "Stop"
$lib = Get-Content "$PSScriptRoot\ai_fix_text.jsx" -Raw -Encoding utf8
$ai = New-Object -ComObject Illustrator.Application
$names = Get-ChildItem (Join-Path $Root $PdfDir) -Filter "*.pdf" | Where-Object { $_.Name -notlike "_*" } | Sort-Object Name | ForEach-Object { $_.BaseName }
if ($To -le 0) { $To = $names.Count }
for ($i = $From - 1; $i -lt $To; $i++) {
    $name = $names[$i]
    $json = Get-Content (Join-Path $Root "$DomDir\$name.json") -Raw -Encoding utf8
    $body = @"
app.userInteractionLevel = UserInteractionLevel.DONTDISPLAYALERTS;
var d = app.documents.getByName('$Doc');
var r = d.artboards[$i].artboardRect;
var ab = { left: r[0], top: r[1] };
var lines = aiCollectLines(d, ab);
var mg = aiMergeParagraphs(d, AI_PARAS, lines, ab);
'$name : ' + lines.length + ' lineas -> ' + mg.merged + ' bloques (' + mg.failed + ' sin unir)' + (mg.dbg.length ? ' | ' + mg.dbg.join(' || ') : '');
"@
    try { Write-Host ($ai.DoJavaScript($lib + "`n" + "var AI_PARAS = " + $json + ";`n" + $body)) } catch { Write-Host "${name}: ERROR " + $_.Exception.Message }
}
