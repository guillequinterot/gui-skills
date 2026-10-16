param([string]$pdf, [string]$out)
$ErrorActionPreference = "Stop"
$ai = New-Object -ComObject Illustrator.Application
$js = @"
app.userInteractionLevel = UserInteractionLevel.DONTDISPLAYALERTS;
var o = app.preferences.PDFFileOptions;
o.pageToOpen = 1;
var d = app.open(new File('$($pdf -replace '\\','/')'));
var res = {name: d.name, artboards: d.artboards.length, w: d.width, h: d.height, texts: d.textFrames.length, samples: [], fonts: {}};
for (var i = 0; i < d.textFrames.length; i++) {
  var t = d.textFrames[i];
  if (i < 25) res.samples.push(t.contents + ' | ' + t.textRange.characterAttributes.textFont.name + ' | ' + Math.round(t.textRange.characterAttributes.size));
  var fn = t.textRange.characterAttributes.textFont.name;
  res.fonts[fn] = (res.fonts[fn] || 0) + 1;
}
var s = '';
s += 'artboards=' + res.artboards + ' size=' + res.w + 'x' + res.h + ' textFrames=' + res.texts + '\n';
for (var f in res.fonts) s += 'font ' + f + ': ' + res.fonts[f] + '\n';
for (var k = 0; k < res.samples.length; k++) s += res.samples[k] + '\n';
d.close(SaveOptions.DONOTSAVECHANGES);
s;
"@
$r = $ai.DoJavaScript($js)
Set-Content -Path $out -Value $r -Encoding utf8
