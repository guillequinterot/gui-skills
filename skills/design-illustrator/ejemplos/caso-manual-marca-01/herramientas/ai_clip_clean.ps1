$ai = New-Object -ComObject Illustrator.Application
$js = @"
app.userInteractionLevel = UserInteractionLevel.DONTDISPLAYALERTS;
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
function firstPath(g) {
  for (var i = 0; i < g.pathItems.length; i++) { return g.pathItems[i]; }
  return null;
}
function unionContent(g, cp) {
  var b = null;
  for (var i = 0; i < g.pageItems.length; i++) {
    var it = g.pageItems[i];
    if (it === cp) continue;
    var gb = it.geometricBounds;
    if (!b) b = [gb[0], gb[1], gb[2], gb[3]];
    else { b[0] = Math.min(b[0], gb[0]); b[1] = Math.max(b[1], gb[1]); b[2] = Math.max(b[2], gb[2]); b[3] = Math.min(b[3], gb[3]); }
  }
  return b;
}
var tol = 0.6;
var all = [];
for (var i = 0; i < d.groupItems.length; i++) { if (d.groupItems[i].clipped) all.push(d.groupItems[i]); }
var vacios = [], asa = [], noop = [];
for (var i = 0; i < all.length; i++) {
  var g = all[i], cp = clipPathOf(g);
  if (!cp) continue;
  var cb = cp.geometricBounds, ct = unionContent(g, cp);
  if (!ct) { vacios.push(g); continue; }
  var ok = ct[0] >= cb[0] - tol && ct[1] <= cb[1] + tol && ct[2] <= cb[2] + tol && ct[3] >= cb[3] - tol;
  if (ok) noop.push({ g: g, cp: cp });
  else asa.push({ g: g, cp: cp, cb: cb });
}
var s = 'vacios=' + vacios.length + ' asa=' + asa.length + ' sin efecto=' + noop.length + '\n';

// 1) grupos con recorte y sin contenido: se borran
for (var i = 0; i < vacios.length; i++) { vacios[i].remove(); }

// 2) asa de la bolsa (lamina 41): un único trazo abierto en lugar de tres recortes
if (asa.length) {
  var ub = null, stroke = null, sw = 1;
  for (var i = 0; i < asa.length; i++) {
    var cb = asa[i].cb;
    if (!ub) ub = [cb[0], cb[1], cb[2], cb[3]];
    else { ub[0] = Math.min(ub[0], cb[0]); ub[1] = Math.max(ub[1], cb[1]); ub[2] = Math.max(ub[2], cb[2]); ub[3] = Math.min(ub[3], cb[3]); }
    var fp = null;
    try { fp = asa[i].g.pathItems.length ? asa[i].g.pathItems[0] : null; } catch (e) {}
    if (fp && fp.stroked && !stroke) { stroke = fp.strokeColor; sw = fp.strokeWidth; }
    else if (!stroke) {
      try { var cps = asa[i].g.compoundPathItems; if (cps.length && cps[0].pathItems[0].stroked) { stroke = cps[0].pathItems[0].strokeColor; sw = cps[0].pathItems[0].strokeWidth; } } catch (e2) {}
    }
  }
  var x0 = ub[0], x1 = ub[2], yTop = ub[1], yBot = ub[3];
  var rx = (x1 - x0) / 2, ry = yTop - yBot, k = 0.5523;
  var p = d.pathItems.add();
  p.setEntirePath([[x0, yBot], [x0 + rx, yTop], [x1, yBot]]);
  var pts = p.pathPoints;
  pts[0].leftDirection = [x0, yBot]; pts[0].rightDirection = [x0, yBot + ry * k];
  pts[1].leftDirection = [x0 + rx - rx * k, yTop]; pts[1].rightDirection = [x0 + rx + rx * k, yTop];
  pts[2].leftDirection = [x1, yBot + ry * k]; pts[2].rightDirection = [x1, yBot];
  pts[0].pointType = PointType.SMOOTH; pts[1].pointType = PointType.SMOOTH; pts[2].pointType = PointType.SMOOTH;
  p.closed = false; p.filled = false; p.stroked = true;
  if (stroke) p.strokeColor = stroke;
  p.strokeWidth = sw;
  p.name = 'Asa de la bolsa';
  s += 'asa redibujada: ' + Math.round(x1 - x0) + 'x' + Math.round(ry) + ' trazo ' + sw + (stroke ? '' : ' (SIN COLOR)') + '\n';
  for (var i = 0; i < asa.length; i++) { asa[i].g.remove(); }
}

// 3) recortes sin efecto: soltar el recorte, borrar el trazado de recorte (queda invisible) y deshacer el grupo contenedor
var liberados = 0;
for (var i = 0; i < noop.length; i++) {
  var g = noop[i].g, cp = noop[i].cp;
  try {
    g.clipped = false;
    cp.remove();
    while (g.pageItems.length > 0) { g.pageItems[0].move(g, ElementPlacement.PLACEBEFORE); }
    g.remove();
    liberados++;
  } catch (e) { s += 'error: ' + e.message + '\n'; }
}
s += 'recortes liberados=' + liberados + '\n';
var quedan = 0; for (var i = 0; i < d.groupItems.length; i++) { if (d.groupItems[i].clipped) quedan++; }
var invis = 0; for (var p2 = 0; p2 < d.pathItems.length; p2++) { var pi = d.pathItems[p2]; try { if (!pi.clipping && !pi.filled && !pi.stroked && !pi.guides) invis++; } catch (e3) {} }
s += 'quedan grupos con recorte=' + quedan + ' | invisibles=' + invis + ' | grupos=' + d.groupItems.length + ' | pathItems=' + d.pathItems.length + ' | textos=' + d.textFrames.length + '\n';
s;
"@
$ai.DoJavaScript($js)
