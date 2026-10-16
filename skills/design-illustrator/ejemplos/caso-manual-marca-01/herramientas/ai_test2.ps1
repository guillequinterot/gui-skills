param([string]$name, [string]$outPdf, [string]$report)
$ErrorActionPreference = "Stop"
$root = "<carpeta-del-proyecto>"   # carpeta del proyecto (HTML en paginas\, export\ y scripts\)
$lib = Get-Content "$root\scripts\ai_fix_text.jsx" -Raw -Encoding utf8
$json = Get-Content "$root\export\dom\$name.json" -Raw -Encoding utf8
$pdfJs = ("$root\export\pdf\$name.pdf") -replace '\\', '/'
$outJs = $outPdf -replace '\\', '/'
$ai = New-Object -ComObject Illustrator.Application
$body = @"
app.userInteractionLevel = UserInteractionLevel.DONTDISPLAYALERTS;
app.preferences.PDFFileOptions.pageToOpen = 1;
var d = app.open(new File('$pdfJs'));
var before = d.textFrames.length;
var r = aiFixText(d, 0.5);
var m = aiMergeParagraphs(d, AI_PARAS, r.lines);
var s = 'letras=' + before + ' lineas=' + r.created + ' bloques unidos=' + m.merged + ' (lineas absorbidas ' + m.absorbed + ') sin unir=' + m.failed + ' marcos finales=' + d.textFrames.length + '\n';
for (var i = 0; i < d.textFrames.length; i++) {
  var t = d.textFrames[i];
  if (t.kind == TextType.AREATEXT) s += '[AREA ' + t.lines.length + ' lineas] ' + t.contents.replace(/\r/g, ' <CR> ').substr(0, 110) + '\n';
}
for (var q = 0; q < m.dbg.length; q++) s += m.dbg[q] + ' || ';
var o = new PDFSaveOptions();
o.preserveEditability = true;
o.compatibility = PDFCompatibility.ACROBAT7;
d.saveAs(new File('$outJs'), o);
d.close(SaveOptions.DONOTSAVECHANGES);
s;
"@
$code = $lib + "`n" + "var AI_PARAS = " + $json + ";`n" + $body
$r = $ai.DoJavaScript($code)
Set-Content -Path $report -Value $r -Encoding utf8
