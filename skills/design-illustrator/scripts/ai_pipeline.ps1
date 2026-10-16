# ai_pipeline.ps1 — PDF de Chromium -> documento maestro de Illustrator (.ai + PDF editable), listo para trabajar.
#
# Requisitos: Illustrator instalado (se controla por COM), la fuente del diseño INSTALADA en Windows, y haber ejecutado antes
#   python -I export_pdf.py --root <proyecto>        (genera <proyecto>\export\pdf\*.pdf)
#   python -I extract_paragraphs.py --root <proyecto> (genera <proyecto>\export\dom\*.json)
#
# Uso:  powershell -NoProfile -File ai_pipeline.ps1 -Root D:\ruta\proyecto [-Max N] [-Width 1920 -Height 1080 -Cols 6] [-Master nombre] [-NoClean]
#
# Para cada lámina:
#   1. abre el PDF (una letra = un texto) y agrupa las letras en UN texto por línea (ai_fix_text.jsx: aiFixText),
#   2. une las líneas del mismo bloque en UN texto de área (texto corrido) solo si el ajuste de líneas coincide con el del
#      navegador (aiMergeParagraphs; separación silábica desactivada),
#   3. guarda un PDF editable y copia la lámina a su mesa de trabajo del .ai maestro (con reintento de pegado).
# Al final limpia los recortes (ai_clean.jsx: aiCleanClips) y guarda el .ai y un PDF multipágina.
# NO cierra ningún documento que ya tengas abierto.  Illustrator puede cerrarse solo en corridas largas: GUARDA antes de lanzarlo.
#
# Salida: <Root>\export\illustrator\pdf\<lámina>.pdf · <Master>.ai · <Master>.pdf · _informe.txt
param(
    [Parameter(Mandatory = $true)][string]$Root,
    [int]$Max = 0, [int]$Width = 1920, [int]$Height = 1080, [int]$Cols = 6,
    [string]$Master = "maestro", [switch]$NoClean,
    [string]$PdfDir = "export\pdf", [string]$DomDir = "export\dom", [string]$OutDir = "export\illustrator"
)
$ErrorActionPreference = "Stop"
$skill = Split-Path -Parent $PSScriptRoot
$out = Join-Path $Root $OutDir
$outPdf = Join-Path $out "pdf"
New-Item -ItemType Directory -Force $out, $outPdf | Out-Null
$lib = (Get-Content "$PSScriptRoot\ai_fix_text.jsx" -Raw -Encoding utf8) + "`n" + (Get-Content "$PSScriptRoot\ai_clean.jsx" -Raw -Encoding utf8)
$ai = New-Object -ComObject Illustrator.Application
$pdfs = Get-ChildItem (Join-Path $Root $PdfDir) -Filter "*.pdf" | Where-Object { $_.Name -notlike "_*" } | Sort-Object Name
if ($Max -gt 0) { $pdfs = $pdfs | Select-Object -First $Max }
$n = $pdfs.Count
if ($n -eq 0) { throw "No hay PDF en $Root\$PdfDir (ejecuta export_pdf.py)" }
$aiPath = ((Join-Path $out "$Master.ai") -replace '\\', '/')
$pdfPath = ((Join-Path $out "$Master.pdf") -replace '\\', '/')
$informe = @()
function Js([string]$code) { return $ai.DoJavaScript($code) }

# 1) documento maestro: n mesas de trabajo en rejilla. El lienzo de Illustrator mide 16383 pt alrededor del origen: la rejilla se desplaza para que entre.
$gap = 200
$x0 = -[int](($Cols * ($Width + $gap)) / 2)
$setup = @"
app.userInteractionLevel = UserInteractionLevel.DONTDISPLAYALERTS;
var m = app.documents.add(DocumentColorSpace.RGB, $Width, $Height, 1);
var X0 = $x0, Y0 = 5000;
m.artboards[0].artboardRect = [X0, Y0, X0 + $Width, Y0 - $Height];
for (var i = 1; i < $n; i++) {
  var c = i % $Cols, r = Math.floor(i / $Cols);
  m.artboards.add([X0 + c * ($Width + $gap), Y0 - r * ($Height + $gap), X0 + c * ($Width + $gap) + $Width, Y0 - r * ($Height + $gap) - $Height]);
}
var a0 = new IllustratorSaveOptions(); a0.pdfCompatible = true;
m.saveAs(new File('$aiPath'), a0);
'ok ' + m.artboards.length + ' ' + m.name;
"@
Write-Host ("Maestro: " + (Js $setup))

$i = 0
foreach ($f in $pdfs) {
    $name = $f.BaseName
    $src = ($f.FullName -replace '\\', '/')
    $dst = ((Join-Path $outPdf "$name.pdf") -replace '\\', '/')
    $jsonFile = Join-Path $Root "$DomDir\$name.json"
    $json = if (Test-Path $jsonFile) { Get-Content $jsonFile -Raw -Encoding utf8 } else { "[]" }
    $body = @"
app.userInteractionLevel = UserInteractionLevel.DONTDISPLAYALERTS;
app.preferences.PDFFileOptions.pageToOpen = 1;
var master = app.documents.getByName('$Master.ai');
var d = app.open(new File('$src'));
var before = d.textFrames.length;
var r = aiFixText(d, 0.5);
var mg = aiMergeParagraphs(d, AI_PARAS, r.lines);
var o = new PDFSaveOptions(); o.preserveEditability = true; o.compatibility = PDFCompatibility.ACROBAT7;
d.saveAs(new File('$dst'), o);
d.activate();
app.executeMenuCommand('selectall');
var srcSel = d.selection.length;
app.copy();
master.activate();
var pasted = 0;
for (var attempt = 0; attempt < 3; attempt++) {
  master.selection = null;
  master.artboards.setActiveArtboardIndex($i);
  app.executeMenuCommand('pasteInPlace');
  pasted = master.selection.length;
  if (pasted === srcSel) break;
}
app.executeMenuCommand('deselectall');
d.close(SaveOptions.DONOTSAVECHANGES);
'${name}: ' + before + ' letras -> ' + r.created + ' lineas -> ' + mg.merged + ' bloques (' + mg.failed + ' sin unir) | pegado ' + pasted + '/' + srcSel + (mg.dbg.length ? ' | ' + mg.dbg.join(' || ') : '');
"@
    $code = $lib + "`n" + "var AI_PARAS = " + $json + ";`n" + $body
    try { $line = Js $code } catch { $line = "${name}: ERROR " + $_.Exception.Message }
    Write-Host $line
    $informe += $line
    $i++
}

# 2) limpiar recortes y guardar
$clean = if ($NoClean) { "var cl = null;" } else { "var cl = aiCleanClips(m);" }
$save = @"
app.userInteractionLevel = UserInteractionLevel.DONTDISPLAYALERTS;
var m = app.documents.getByName('$Master.ai');
m.activate();
$clean
for (var k = 0; k < m.artboards.length; k++) { m.artboards[k].name = 'p' + (k < 9 ? '0' : '') + (k + 1); }
m.selection = null;
m.save();
var o = new PDFSaveOptions(); o.preserveEditability = true; o.compatibility = PDFCompatibility.ACROBAT7; o.artboardRange = '';
m.saveAs(new File('$pdfPath'), o);
m.close(SaveOptions.DONOTSAVECHANGES);
app.open(new File('$aiPath'));
'guardado' + (cl ? ' | recortes: ' + cl.total + ' -> liberados ' + cl.liberados + ', vacios borrados ' + cl.vacios + ', invisibles ' + cl.invisibles + ', NECESARIOS sin tocar ' + cl.necesarios.length : '');
"@
$res = Js ($lib + "`n" + $save)
Write-Host $res
$informe += $res
$informe | Set-Content (Join-Path $out "_informe.txt") -Encoding utf8
Write-Host "Listo: $n laminas. Siguiente: ai_autosize_text.ps1 (cajas de texto de área en automático) y verify_fidelity.py"
