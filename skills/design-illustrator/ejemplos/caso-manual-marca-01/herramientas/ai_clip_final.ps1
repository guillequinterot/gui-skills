$ai = New-Object -ComObject Illustrator.Application
$js = @"
app.userInteractionLevel = UserInteractionLevel.DONTDISPLAYALERTS;
var d = app.activeDocument;
var borrados = 0;
for (var i = d.groupItems.length - 1; i >= 0; i--) {
  var g = d.groupItems[i];
  if (g.clipped && g.pageItems.length <= 1) { g.remove(); borrados++; }
}
var quedan = 0; for (var i = 0; i < d.groupItems.length; i++) { if (d.groupItems[i].clipped) quedan++; }
var invis = 0, vacios = 0;
for (var p = 0; p < d.pathItems.length; p++) { var pi = d.pathItems[p]; try { if (!pi.clipping && !pi.filled && !pi.stroked && !pi.guides) invis++; } catch (e) {} }
for (var i = 0; i < d.groupItems.length; i++) { if (d.groupItems[i].pageItems.length == 0) vacios++; }
d.selection = null;
d.save();
'grupos vacios con recorte borrados=' + borrados + ' | quedan recortes=' + quedan + ' | trazados invisibles=' + invis + ' | grupos vacios=' + vacios + ' | grupos=' + d.groupItems.length + ' | textos=' + d.textFrames.length + ' | guardado=' + d.saved;
"@
$ai.DoJavaScript($js)
