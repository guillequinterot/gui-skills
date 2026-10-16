$ErrorActionPreference = "Stop"
$ai = New-Object -ComObject Illustrator.Application
$js = @"
app.userInteractionLevel = UserInteractionLevel.DONTDISPLAYALERTS;
var d = app.activeDocument;
var sel = [];
for (var i = 0; i < d.textFrames.length; i++) { if (d.textFrames[i].kind == TextType.AREATEXT) sel.push(d.textFrames[i]); }
d.selection = sel;
var s = 'seleccionados ' + d.selection.length + '\n';
var cands = ['area type options', 'Area Type Options', 'area text options', 'Adobe Area Type Options', 'areaTypeOptions', 'AreaTypeOptions', 'Area Type Options...'];
for (var c = 0; c < cands.length; c++) {
  try { app.isValidMenuCommand ? s += cands[c] + ' valido=' + app.isValidMenuCommand(cands[c]) + '\n' : s += 'sin isValid\n'; } catch (e) { s += cands[c] + ' -> ' + e.message + '\n'; }
}
s;
"@
$ai.DoJavaScript($js)
