$ai = New-Object -ComObject Illustrator.Application
$js = @"
app.userInteractionLevel = UserInteractionLevel.DONTDISPLAYALERTS;
var d = app.activeDocument;
function artboardOf(x, y) {
  for (var a = 0; a < d.artboards.length; a++) { var r = d.artboards[a].artboardRect; if (x >= r[0] && x <= r[2] && y <= r[1] && y >= r[3]) return a + 1; }
  return 0;
}
var s = '';
for (var i = 0; i < d.groupItems.length; i++) {
  var g = d.groupItems[i];
  var gb = g.geometricBounds;
  var types = [];
  for (var k = 0; k < g.pageItems.length; k++) { var it = g.pageItems[k]; var c = ''; try { c = (it.typename == 'PathItem' ? 'clip=' + it.clipping + ',fill=' + it.filled + ',stroke=' + it.stroked : ''); } catch (e) {} types.push(it.typename + '(' + c + ')'); }
  s += 'grupo ' + i + ' clipped=' + g.clipped + ' lamina=' + artboardOf((gb[0]+gb[2])/2, (gb[1]+gb[3])/2) + ' tam=' + Math.round(gb[2]-gb[0]) + 'x' + Math.round(gb[1]-gb[3]) + ' hijos=' + g.pageItems.length + ' [' + types.join('; ') + ']\n';
}
// color del asa
var p = null;
for (var j = 0; j < d.pathItems.length; j++) { if (d.pathItems[j].name == 'Asa de la bolsa') { p = d.pathItems[j]; break; } }
if (p) {
  p.stroked = true; p.filled = false; p.strokeWidth = 1;
  var c = new RGBColor(); c.red = 95; c.green = 87; c.blue = 51;
  p.strokeColor = c;
  s += 'asa: trazo oliva aplicado, ancho=' + p.strokeWidth + '\n';
}
s;
"@
$ai.DoJavaScript($js)
