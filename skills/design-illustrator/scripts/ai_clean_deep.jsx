// ai_clean_deep.jsx — Illustrator (ExtendScript).
// Limpieza de máscaras de recorte en un documento ya montado y ANIDADO (el caso típico: un PDF de Illustrator/CAD
// abierto en Illustrator, con un recorte por lámina, uno por foto y recortes dentro de recortes).
//
// Diferencia con ai_clean.jsx (pensado para el PDF crudo de Chromium, recortes planos): aquí se calcula el límite
// VISIBLE EFECTIVO de cada objeto — un grupo con recorte mide la intersección de su recorte con lo que contiene —, de modo
// que un recorte interno que solo repite el tamaño de una foto (y la foto ya la recorta un recorte externo) se detecta
// como «sin efecto» y se suelta, aunque la foto sobresalga de él.
//
//   aiCleanDeep(doc, dry) -> { vistos, liberados, vacios, movidos, necesarios:[...], errores:[...] }
//
// Reglas, de dentro hacia fuera (postorden):
//  1. Un grupo con recorte cuyo contenido visible cabe dentro del recorte (tol. 0,6 pt) -> se suelta: se borra el trazado de
//     recorte (no queda invisible) y se deshace el grupo conservando el orden. Si el grupo tiene nombre, opacidad o
//     modo de fusión propios, solo se le quita el recorte (el grupo se queda).
//  2. Grupo con recorte sin contenido visible -> se borra.
//  3. Grupo con recorte cuyo contenido queda ENTERO fuera del recorte (oculto): no se borra; se aparta a la capa
//     «_fuera-de-mesa (oculto)» (oculta y bloqueada).
//  4. Recorte que sí recorta algo visible -> NO se toca: se devuelve en `necesarios` (lámina, tamaño, qué sobresale).
// dry = true no modifica nada (solo cuenta).

function aiCD_clipPath(g) {
  for (var i = 0; i < g.pageItems.length; i++) {
    var it = g.pageItems[i];
    try {
      if (it.typename == "PathItem" && it.clipping) return it;
      if (it.typename == "CompoundPathItem" && it.pathItems.length && it.pathItems[0].clipping) return it;
    } catch (e) {}
  }
  return null;
}

// límites visibles efectivos: [izq, arriba, der, abajo] (arriba > abajo) o null si no hay nada visible
function aiCD_eff(it, cpSkip) {
  var tn = it.typename, gb, i;
  try {
    if (tn == "GroupItem") {
      var cp = it.clipped ? aiCD_clipPath(it) : null;
      var b = null;
      for (i = 0; i < it.pageItems.length; i++) {
        var ch = it.pageItems[i];
        if (cp && ch === cp) continue;
        var cb = aiCD_eff(ch);
        if (!cb) continue;
        if (!b) b = [cb[0], cb[1], cb[2], cb[3]];
        else { b[0] = Math.min(b[0], cb[0]); b[1] = Math.max(b[1], cb[1]); b[2] = Math.max(b[2], cb[2]); b[3] = Math.min(b[3], cb[3]); }
      }
      if (b && cp) {
        var c = cp.geometricBounds;
        var r = [Math.max(b[0], c[0]), Math.min(b[1], c[1]), Math.min(b[2], c[2]), Math.max(b[3], c[3])];
        if (r[0] >= r[2] || r[3] >= r[1]) return null;
        return r;
      }
      return b;
    }
    if (tn == "PathItem") {
      if (it.clipping) return null;
      if (!it.filled && !it.stroked) return null;
      return it.geometricBounds;
    }
    if (tn == "CompoundPathItem") {
      if (it.pathItems.length && it.pathItems[0].clipping) return null;
      return it.geometricBounds;
    }
    return it.geometricBounds;
  } catch (e) { return null; }
}

function aiCD_inside(ct, cb, tol) {
  return ct[0] >= cb[0] - tol && ct[1] <= cb[1] + tol && ct[2] <= cb[2] + tol && ct[3] >= cb[3] - tol;
}

function aiCD_artboardOf(doc, x, y) {
  for (var a = 0; a < doc.artboards.length; a++) {
    var r = doc.artboards[a].artboardRect;
    if (x >= r[0] && x <= r[2] && y <= r[1] && y >= r[3]) return a + 1;
  }
  return 0;
}

function aiCD_hasRaster(g) {
  for (var i = 0; i < g.pageItems.length; i++) {
    var it = g.pageItems[i];
    if (it.typename == "RasterItem" || it.typename == "PlacedItem") return true;
    if (it.typename == "GroupItem" && aiCD_hasRaster(it)) return true;
  }
  return false;
}


// capa donde se aparta lo que quedó oculto (se crea una vez; al final queda oculta y bloqueada)
function aiCD_hiddenLayer(doc, st) {
  if (!st.capaOculta) {
    try { st.capaOculta = doc.layers.getByName("_fuera-de-mesa (oculto)"); }
    catch (eL) { st.capaOculta = doc.layers.add(); st.capaOculta.name = "_fuera-de-mesa (oculto)"; }
  }
  st.capaOculta.locked = false;
  st.capaOculta.visible = true;
  return st.capaOculta;
}

function aiCD_fullyOutside(eb, cb) {
  return eb[2] < cb[0] || eb[0] > cb[2] || eb[1] < cb[3] || eb[3] > cb[1];
}

function aiCD_proc(doc, g, st, dry) {
  var i, subs = [];
  for (i = 0; i < g.pageItems.length; i++) if (g.pageItems[i].typename == "GroupItem") subs.push(g.pageItems[i]);
  for (i = 0; i < subs.length; i++) aiCD_proc(doc, subs[i], st, dry);
  if (!g.clipped) return;
  st.vistos++;
  var cp = aiCD_clipPath(g);
  if (!cp) return;
  var cb = cp.geometricBounds;
  // hijos que quedan ENTEROS fuera del recorte (ocultos por él): se apartan; si no, soltar el recorte los dejaría ver
  var k, hid = [];
  for (k = 0; k < g.pageItems.length; k++) {
    var hc = g.pageItems[k];
    if (hc === cp) continue;
    var hb = aiCD_eff(hc);
    if (hb && aiCD_fullyOutside(hb, cb)) hid.push(hc);
  }
  if (hid.length) {
    st.movidos += hid.length;
    if (!dry) {
      for (k = 0; k < hid.length; k++) {
        try { hid[k].move(aiCD_hiddenLayer(doc, st), ElementPlacement.PLACEATEND); }
        catch (eH) { st.errores.push("mover hijo oculto: " + eH.message); }
      }
    }
  }
  // contenido visible efectivo SIN recortar por este recorte: unión de los hijos que quedan (no de su intersección)
  var un = null;
  for (k = 0; k < g.pageItems.length; k++) {
    var ch = g.pageItems[k];
    if (ch === cp) continue;
    var eb = aiCD_eff(ch);
    if (!eb) continue;
    if (!un) un = [eb[0], eb[1], eb[2], eb[3]];
    else { un[0] = Math.min(un[0], eb[0]); un[1] = Math.max(un[1], eb[1]); un[2] = Math.max(un[2], eb[2]); un[3] = Math.min(un[3], eb[3]); }
  }
  if (!un) {   // no hay nada visible dentro: grupo vacío de verdad
    st.vacios++;
    if (!dry) { try { g.remove(); } catch (e0) { st.errores.push(e0.message); } }
    return;
  }
  if (aiCD_inside(un, cb, 0.6)) {
    st.liberados++;
    if (dry) return;
    try {
      var keep = (g.name !== "") || (g.opacity < 100) || (g.blendingMode != BlendModes.NORMAL);
      g.clipped = false;
      cp.remove();
      if (!keep) {
        while (g.pageItems.length > 0) g.pageItems[0].move(g, ElementPlacement.PLACEBEFORE);
        g.remove();
      }
    } catch (e1) { st.errores.push(e1.message); }
  } else {
    var sob = [Math.round(cb[0] - un[0]), Math.round(un[1] - cb[1]), Math.round(un[2] - cb[2]), Math.round(cb[3] - un[3])];
    var oculto = aiCD_eff(g) === null;   // todo el contenido queda fuera del recorte: está oculto
    if (oculto) {
      // contenido que el recorte esconde por completo (restos de copiar y pegar): no se borra, se aparta a una capa oculta
      st.movidos++;
      if (!dry) {
        try { g.move(aiCD_hiddenLayer(doc, st), ElementPlacement.PLACEATEND); }
        catch (eM) { st.errores.push("mover oculto: " + eM.message); }
      }
      return;
    }
    st.necesarios.push({
      lamina: aiCD_artboardOf(doc, (cb[0] + cb[2]) / 2, (cb[1] + cb[3]) / 2),
      clip: Math.round(cb[2] - cb[0]) + "x" + Math.round(cb[1] - cb[3]),
      pos: Math.round(cb[0]) + "," + Math.round(cb[1]),
      foto: aiCD_hasRaster(g),
      oculto: oculto,
      sobresale: sob.join(",")
    });
  }
}

function aiCleanDeep(doc, dry) {
  var st = { vistos: 0, liberados: 0, vacios: 0, movidos: 0, necesarios: [], errores: [], gruposVacios: 0, capaOculta: null };
  var L, i, tops;
  for (L = 0; L < doc.layers.length; L++) {
    if (doc.layers[L].name == "_fuera-de-mesa (oculto)") continue;
    tops = [];
    for (i = 0; i < doc.layers[L].pageItems.length; i++) if (doc.layers[L].pageItems[i].typename == "GroupItem") tops.push(doc.layers[L].pageItems[i]);
    for (i = 0; i < tops.length; i++) aiCD_proc(doc, tops[i], st, dry);
  }
  if (!dry) {
    if (st.capaOculta) { try { st.capaOculta.visible = false; st.capaOculta.locked = true; } catch (eV) {} }
    for (i = doc.groupItems.length - 1; i >= 0; i--) {
      try { if (doc.groupItems[i].pageItems.length == 0) { doc.groupItems[i].remove(); st.gruposVacios++; } } catch (e) {}
    }
  }
  return st;
}
