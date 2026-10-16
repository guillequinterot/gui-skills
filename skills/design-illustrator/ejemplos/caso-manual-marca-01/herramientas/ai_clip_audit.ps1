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
function contentBounds(g, cp) {
  var b = null;
  for (var i = 0; i < g.pageItems.length; i++) {
    var it = g.pageItems[i];
    if (it === cp) continue;
    var gb;
    try { gb = it.geometricBounds; } catch (e) { continue; }
    if (!b) b = [gb[0], gb[1], gb[2], gb[3]];
    else { b[0] = Math.min(b[0], gb[0]); b[1] = Math.max(b[1], gb[1]); b[2] = Math.max(b[2], gb[2]); b[3] = Math.min(b[3], gb[3]); }
  }
  return b;
}
var groups = d.groupItems.length, clipped = 0, noop = 0, needed = 0, noClip = 0, sizes = {}, neededList = [];
for (var i = 0; i < groups; i++) {
  var g = d.groupItems[i];
  if (!g.clipped) continue;
  clipped++;
  var cp = clipPathOf(g);
  if (!cp) { noClip++; continue; }
  var cb = cp.geometricBounds, ct = contentBounds(g, cp);
  var key = Math.round(cb[2] - cb[0]) + 'x' + Math.round(cb[1] - cb[3]);
  sizes[key] = (sizes[key] || 0) + 1;
  var tol = 0.6;
  if (ct && ct[0] >= cb[0] - tol && ct[1] <= cb[1] + tol && ct[2] <= cb[2] + tol && ct[3] >= cb[3] - tol) noop++;
  else { needed++; if (neededList.length < 12) neededList.push(key + ' contenido sobresale: ' + (ct ? Math.round(ct[0]-cb[0]) + ',' + Math.round(ct[1]-cb[1]) + ',' + Math.round(ct[2]-cb[2]) + ',' + Math.round(cb[3]-ct[3]) : '?')); }
}
var invis = 0, paths = d.pathItems.length;
for (var p = 0; p < paths; p++) {
  var pi = d.pathItems[p];
  try { if (!pi.clipping && !pi.filled && !pi.stroked && !pi.guides) invis++; } catch (e) {}
}
var s = 'documento=' + d.name + '\n';
s += 'grupos=' + groups + ' | con recorte=' + clipped + ' | recorte que NO recorta nada=' + noop + ' | recorte que SI recorta=' + needed + ' | sin trazado de recorte=' + noClip + '\n';
s += 'pathItems=' + paths + ' | invisibles (sin relleno ni trazo, no son recorte)=' + invis + '\n';
s += 'compuestos=' + d.compoundPathItems.length + ' | capas=' + d.layers.length + '\n';
s += 'tamanos de recorte (ancho x alto): ';
var ks = []; for (var k in sizes) ks.push(k + ' x' + sizes[k]); ks.sort(function(a,b){ return parseInt(b.split(' x')[1]) - parseInt(a.split(' x')[1]); });
s += ks.slice(0, 15).join(' | ') + '\n';
for (var q = 0; q < neededList.length; q++) s += '  necesario: ' + neededList[q] + '\n';
s;
"@
$ai.DoJavaScript($js)
