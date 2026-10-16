$ai = New-Object -ComObject Illustrator.Application
$js = @"
var d = app.activeDocument;
function clipPathOf(g) {
  for (var i = 0; i < g.pageItems.length; i++) {
    var it = g.pageItems[i];
    try {
      if (it.typename == 'PathItem' && it.clipping) return it;
      if (it.typename == 'CompoundPathItem' && it.pathItems.length && it.pathItems[0].clipping) return it;
    } catch (e) {}
  }
  return null;
}
function artboardOf(x, y) {
  for (var a = 0; a < d.artboards.length; a++) { var r = d.artboards[a].artboardRect; if (x >= r[0] && x <= r[2] && y <= r[1] && y >= r[3]) return a + 1; }
  return 0;
}
var out = [];
for (var i = 0; i < d.groupItems.length; i++) {
  var g = d.groupItems[i];
  if (!g.clipped) continue;
  var cp = clipPathOf(g);
  var cb = cp.geometricBounds;
  var n = 0, b = null, types = {};
  for (var k = 0; k < g.pageItems.length; k++) {
    var it = g.pageItems[k];
    if (it === cp) continue;
    n++; types[it.typename] = (types[it.typename] || 0) + 1;
    var gb = it.geometricBounds;
    if (!b) b = [gb[0], gb[1], gb[2], gb[3]]; else { b[0] = Math.min(b[0], gb[0]); b[1] = Math.max(b[1], gb[1]); b[2] = Math.max(b[2], gb[2]); b[3] = Math.min(b[3], gb[3]); }
  }
  var tol = 0.6;
  var ok = b && b[0] >= cb[0] - tol && b[1] <= cb[1] + tol && b[2] <= cb[2] + tol && b[3] >= cb[3] - tol;
  if (ok) continue;
  var ab = artboardOf((cb[0] + cb[2]) / 2, (cb[1] + cb[3]) / 2);
  var ts = []; for (var t in types) ts.push(t + 'x' + types[t]);
  var rel = '';
  if (b) rel = ' sobresale izq/arr/der/abj=' + [Math.round(cb[0]-b[0]), Math.round(b[1]-cb[1]), Math.round(b[2]-cb[2]), Math.round(cb[3]-b[3])].join(',');
  out.push('lamina ' + ab + ' | recorte ' + Math.round(cb[2]-cb[0]) + 'x' + Math.round(cb[1]-cb[3]) + ' | hijos=' + n + ' (' + ts.join(',') + ')' + (b ? rel : ' VACIO'));
}
out.join('\n');
"@
$ai.DoJavaScript($js)
