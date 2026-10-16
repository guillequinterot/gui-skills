# ai_repair_page.ps1 — rehace UNA lámina del maestro (letras -> líneas -> texto corrido -> limpieza de recortes) y la vuelve a pegar.
# Úsalo cuando una lámina salió en blanco (fallo de pegado) o con error («CANT»/«BKey») en la corrida larga.
# Borra lo que haya en esa mesa de trabajo, pega la lámina rehecha, guarda el .ai y el PDF maestro y deja el .ai abierto.
#
# Uso: powershell -NoProfile -File ai_repair_page.ps1 -Root D:\ruta\proyecto -Page 33 [-Master maestro]
#   -Page = posición (1 = primera lámina por orden alfabético de export\pdf)
param(
    [Parameter(Mandatory = $true)][string]$Root, [Parameter(Mandatory = $true)][int]$Page,
    [string]$Master = "maestro", [string]$PdfDir = "export\pdf", [string]$DomDir = "export\dom", [string]$OutDir = "export\illustrator"
)
$ErrorActionPreference = "Stop"
$out = Join-Path $Root $OutDir
$lib = (Get-Content "$PSScriptRoot\ai_fix_text.jsx" -Raw -Encoding utf8) + "`n" + (Get-Content "$PSScriptRoot\ai_clean.jsx" -Raw -Encoding utf8)
$ai = New-Object -ComObject Illustrator.Application
$pdfs = Get-ChildItem (Join-Path $Root $PdfDir) -Filter "*.pdf" | Where-Object { $_.Name -notlike "_*" } | Sort-Object Name
$raw = $pdfs[$Page - 1]
$name = $raw.BaseName
$src = $raw.FullName -replace '\\', '/'
$dst = ((Join-Path $out "pdf\$name.pdf") -replace '\\', '/')
$aiPath = ((Join-Path $out "$Master.ai") -replace '\\', '/')
$pdfPath = ((Join-Path $out "$Master.pdf") -replace '\\', '/')
$jsonFile = Join-Path $Root "$DomDir\$name.json"
$json = if (Test-Path $jsonFile) { Get-Content $jsonFile -Raw -Encoding utf8 } else { "[]" }
$idx = $Page - 1

$body1 = @"
app.userInteractionLevel = UserInteractionLevel.DONTDISPLAYALERTS;
app.preferences.PDFFileOptions.pageToOpen = 1;
var d = app.open(new File('$src'));
var r = aiFixText(d, 0.5);
var mg = aiMergeParagraphs(d, AI_PARAS, r.lines);
var o = new PDFSaveOptions(); o.preserveEditability = true; o.compatibility = PDFCompatibility.ACROBAT7;
d.saveAs(new File('$dst'), o);
app.executeMenuCommand('selectall');
var n = d.selection.length;
app.copy();
d.close(SaveOptions.DONOTSAVECHANGES);
'$name : ' + r.created + ' lineas -> ' + mg.merged + ' bloques (' + mg.failed + ' sin unir) | copiados ' + n + (mg.dbg.length ? ' | ' + mg.dbg.join(' || ') : '');
"@
Write-Host ($ai.DoJavaScript($lib + "`n" + "var AI_PARAS = " + $json + ";`n" + $body1))

$body2 = @"
app.userInteractionLevel = UserInteractionLevel.DONTDISPLAYALERTS;
var m = app.open(new File('$aiPath'));
m.selection = null;
m.artboards.setActiveArtboardIndex($idx);
m.selectObjectsOnActiveArtboard();
var viejos = m.selection.length;
for (var i = m.selection.length - 1; i >= 0; i--) { m.selection[i].remove(); }
m.selection = null;
m.artboards.setActiveArtboardIndex($idx);
app.executeMenuCommand('pasteInPlace');
var pegados = m.selection.length;
app.executeMenuCommand('deselectall');
var cl = aiCleanClips(m);
m.save();
'borrados ' + viejos + ' | pegados ' + pegados + ' | recortes liberados ' + cl.liberados + ', necesarios sin tocar ' + cl.necesarios.length;
"@
Write-Host ($ai.DoJavaScript($lib + "`n" + $body2))

$body3 = @"
app.userInteractionLevel = UserInteractionLevel.DONTDISPLAYALERTS;
var m = app.documents.getByName('$Master.ai');
var o = new PDFSaveOptions(); o.preserveEditability = true; o.compatibility = PDFCompatibility.ACROBAT7; o.artboardRange = '';
m.saveAs(new File('$pdfPath'), o);
m.close(SaveOptions.DONOTSAVECHANGES);
var m2 = app.open(new File('$aiPath'));
'PDF maestro guardado; .ai abierto: ' + m2.name + ' (' + m2.artboards.length + ' mesas de trabajo)';
"@
Write-Host ($ai.DoJavaScript($body3))
Write-Host "Recuerda: la lámina rehecha vuelve sin la casilla «Tamaño automático»: ejecuta ai_autosize_text.ps1."
