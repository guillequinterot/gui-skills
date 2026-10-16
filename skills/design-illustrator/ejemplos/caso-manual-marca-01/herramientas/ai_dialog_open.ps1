$ai = New-Object -ComObject Illustrator.Application
$js = @"
app.userInteractionLevel = UserInteractionLevel.DISPLAYALERTS;
var d = app.activeDocument;
var n = d.selection.length;
app.executeMenuCommand('areatextoptions');
'dialogo cerrado; seleccion=' + n;
"@
$ai.DoJavaScript($js)
