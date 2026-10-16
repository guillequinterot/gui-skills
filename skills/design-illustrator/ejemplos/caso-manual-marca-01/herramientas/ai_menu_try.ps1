$ai = New-Object -ComObject Illustrator.Application
$log = Join-Path $env:TEMP "cand.log"
$js = @"
app.userInteractionLevel = UserInteractionLevel.DONTDISPLAYALERTS;
var lf = new File('$log');
lf.open('w');
var cands = ['area type options', 'AreaTypeOptions', 'Area Type Options', 'areaTextOptions', 'areatextoptions', 'Adobe Area Type Options', 'Area Type Options...', 'type area options'];
for (var c = 0; c < cands.length; c++) {
  lf.writeln('probando ' + cands[c]); lf.close(); lf.open('a');
  try { app.executeMenuCommand(cands[c]); lf.writeln('  OK (se ejecuto) ' + cands[c]); lf.close(); lf.open('a'); break; }
  catch (e) { lf.writeln('  error: ' + e.message); lf.close(); lf.open('a'); }
}
lf.close();
'fin';
"@
$ai.DoJavaScript($js)
