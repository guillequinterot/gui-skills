param([string]$pdf, [string]$outPdf, [string]$report)
$ErrorActionPreference = "Stop"
$root = "<carpeta-del-proyecto>"   # carpeta del proyecto (HTML en paginas\, export\ y scripts\)
$lib = Get-Content "$root\scripts\ai_fix_text.jsx" -Raw -Encoding utf8
$ai = New-Object -ComObject Illustrator.Application
$pdfJs = $pdf -replace '\\', '/'
$outJs = $outPdf -replace '\\', '/'
$js = @"
$lib
app.userInteractionLevel = UserInteractionLevel.DONTDISPLAYALERTS;
while (app.documents.length > 0) { app.activeDocument.close(SaveOptions.DONOTSAVECHANGES); }
app.preferences.PDFFileOptions.pageToOpen = 1;
var d = app.open(new File('$pdfJs'));
var before = d.textFrames.length;
var r = aiFixText(d, 1.6);
var after = d.textFrames.length;
var s = 'before=' + before + ' after=' + after + ' created=' + r.created + ' removed=' + r.removed + '\n';
for (var i = 0; i < d.textFrames.length && i < 40; i++) {
  var t = d.textFrames[i];
  s += t.contents + ' | ' + t.textRange.characterAttributes.textFont.name + ' | ' + Math.round(t.textRange.characterAttributes.size) + ' | trk ' + t.textRange.characterAttributes.tracking + '\n';
}
var o = new PDFSaveOptions();
o.preserveEditability = true;
o.compatibility = PDFCompatibility.ACROBAT7;
d.saveAs(new File('$outJs'), o);
d.close(SaveOptions.DONOTSAVECHANGES);
s;
"@
$r = $ai.DoJavaScript($js)
Set-Content -Path $report -Value $r -Encoding utf8
