// ai_clean.jsx — Illustrator (ExtendScript). Limpieza de un documento importado desde PDF de Chromium.
//
// Los PDF de Chromium llegan a Illustrator con MUCHAS máscaras de recorte («clipping masks») sin sentido: una por lámina,
// una por cada logo SVG, una por cada contenedor… Al soltar el recorte a mano, el trazado de recorte queda como un objeto
// invisible (sin relleno ni trazo) que es basura en el archivo. Esta limpieza deja SOLO los recortes que recortan de verdad.
//
//   aiCleanClips(doc) -> { total, vacios, liberados, necesarios:[...], invisibles, gruposVacios, errores:[...] }
//
// Reglas (en este orden):
//  1. Grupo con recorte y SIN contenido (solo el trazado de recorte)  -> se borra.
//  2. Recorte que NO recorta nada (el contenido cabe dentro, tolerancia 0,6 pt) -> se suelta el recorte, se BORRA el trazado de
//     recorte (no queda invisible) y se deshace el grupo contenedor conservando el orden de apilado.
//  3. Recorte cuyo contenido sobresale del recorte -> NO se toca: se devuelve en `necesarios` con lámina y medidas para decidir
//     (rehacerlo con geometría real, p. ej. un arco abierto en vez de un borde redondeado recortado, o conservarlo si el diseño
//     lo necesita de verdad: foto recortada, máscara de forma).
//  4. Pasada final: grupos de recorte con ≤ 1 hijo (envoltorios que quedaron vacíos), grupos vacíos y trazados invisibles
//     (sin relleno, sin trazo, no son recorte ni guías) -> se borran.

function aiClipPathOf(g) {
  for (var i = 0; i < g.pageItems.length; i++) {
    var it = g.pageItems[i];
    try {
      if (it.typename == "PathItem" && it.clipping) return it;
      if (it.typename == "CompoundPathItem" && it.pathItems.length && it.pathItems[0].clipping) return it;
    } catch (e) {}
  }
  return null;
}

function aiUnionContent(g, cp) {
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

function aiArtboardOf(doc, x, y) {
  for (var a = 0; a < doc.artboards.length; a++) {
    var r = doc.artboards[a].artboardRect;
    if (x >= r[0] && x <= r[2] && y <= r[1] && y >= r[3]) return a + 1;
  }
  return 0;
}

function aiCleanClips(doc) {
  var tol = 0.6;
  var all = [];
  var i;
  for (i = 0; i < doc.groupItems.length; i++) { if (doc.groupItems[i].clipped) all.push(doc.groupItems[i]); }
  var vacios = [], noop = [], necesarios = [], errores = [];
  for (i = 0; i < all.length; i++) {
    var g = all[i], cp = aiClipPathOf(g);
    if (!cp) continue;
    var cb = cp.geometricBounds, ct = aiUnionContent(g, cp);
    if (!ct) { vacios.push(g); continue; }
    var ok = ct[0] >= cb[0] - tol && ct[1] <= cb[1] + tol && ct[2] <= cb[2] + tol && ct[3] >= cb[3] - tol;
    if (ok) noop.push({ g: g, cp: cp });
    else necesarios.push({
      lamina: aiArtboardOf(doc, (cb[0] + cb[2]) / 2, (cb[1] + cb[3]) / 2),
      clip: Math.round(cb[2] - cb[0]) + "x" + Math.round(cb[1] - cb[3]),
      hijos: g.pageItems.length - 1,
      sobresale: [Math.round(cb[0] - ct[0]), Math.round(ct[1] - cb[1]), Math.round(ct[2] - cb[2]), Math.round(cb[3] - ct[3])].join(",")
    });
  }
  for (i = 0; i < vacios.length; i++) { try { vacios[i].remove(); } catch (e1) { errores.push(e1.message); } }

  var liberados = 0;
  for (i = 0; i < noop.length; i++) {
    var g2 = noop[i].g, cp2 = noop[i].cp;
    try {
      g2.clipped = false;
      cp2.remove();                                   // el trazado de recorte, si no, queda invisible
      while (g2.pageItems.length > 0) { g2.pageItems[0].move(g2, ElementPlacement.PLACEBEFORE); }   // conserva el orden
      g2.remove();
      liberados++;
    } catch (e2) { errores.push(e2.message); }
  }

  // pasada final
  var extra = 0;
  for (i = doc.groupItems.length - 1; i >= 0; i--) {
    var g3 = doc.groupItems[i];
    try { if (g3.clipped && g3.pageItems.length <= 1) { g3.remove(); extra++; } } catch (e3) {}
  }
  var gv = 0;
  for (i = doc.groupItems.length - 1; i >= 0; i--) {
    try { if (doc.groupItems[i].pageItems.length == 0) { doc.groupItems[i].remove(); gv++; } } catch (e4) {}
  }
  var inv = 0;
  for (i = doc.pathItems.length - 1; i >= 0; i--) {
    var p = doc.pathItems[i];
    try { if (!p.clipping && !p.filled && !p.stroked && !p.guides) { p.remove(); inv++; } } catch (e5) {}
  }
  return { total: all.length, vacios: vacios.length + extra, liberados: liberados, necesarios: necesarios, invisibles: inv, gruposVacios: gv, errores: errores };
}

// Informe de solo lectura (no modifica nada): grupos con recorte, cuántos recortan algo y cuántos trazados invisibles hay.
function aiAuditClips(doc) {
  var tol = 0.6, total = 0, vacios = 0, noop = 0, necesarios = 0, i;
  for (i = 0; i < doc.groupItems.length; i++) {
    var g = doc.groupItems[i];
    if (!g.clipped) continue;
    total++;
    var cp = aiClipPathOf(g);
    if (!cp) continue;
    var cb = cp.geometricBounds, ct = aiUnionContent(g, cp);
    if (!ct) vacios++;
    else if (ct[0] >= cb[0] - tol && ct[1] <= cb[1] + tol && ct[2] <= cb[2] + tol && ct[3] >= cb[3] - tol) noop++;
    else necesarios++;
  }
  var inv = 0;
  for (i = 0; i < doc.pathItems.length; i++) {
    var p = doc.pathItems[i];
    try { if (!p.clipping && !p.filled && !p.stroked && !p.guides) inv++; } catch (e) {}
  }
  return { grupos: doc.groupItems.length, conRecorte: total, vacios: vacios, sinEfecto: noop, queRecortan: necesarios, invisibles: inv };
}
