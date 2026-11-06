// ai_fix_text_inplace.jsx — Illustrator (ExtendScript).
// Une los textos PARTIDOS de un documento que viene de un PDF (letras sueltas o trozos de palabra: «oposed SQ. F»)
// en UN texto de punto por línea, SIN sacar los textos de su sitio:
//   - cada texto nuevo nace dentro del MISMO contenedor (capa o grupo) que los trozos que reemplaza y en su misma
//     posición de apilado, de modo que no se rompen grupos, recortes ni el orden de capas;
//   - solo se unen trozos que son hermanos (mismo contenedor), misma línea base, misma fuente, tamaño, color,
//     escala, desplazamiento de línea base y opacidad;
//   - la unión se VALIDA: el ancho natural del texto nuevo debe coincidir (12 %; la diferencia la absorbe el tracking) con el ancho de tinta de los trozos.
//     Si no coincide (p. ej. faltaba un espacio entre columnas) NO se une: los trozos se dejan como estaban.
// Los trozos pueden tener fuente/color distintos (se respetan por carácter). A diferencia de ai_fix_text.jsx (pensado para el PDF de Chromium, una letra por objeto, todo en la raíz), este
// script es seguro para documentos ya montados con grupos y máscaras.
//
//   aiFixTextInPlace(doc, breakEm) -> { lineas, unidas, trozosQuitados, rechazadas:[...], omitidos, contenedores }
//
// breakEm = hueco máximo (en em, entre bordes de tinta) que se tolera cuando en la unión hay un espacio real
// (0,6 ≈ un espacio de palabra con sus bearings). Sin espacio en la unión solo se tolera 0,15 em (kerning).

function aiFTColorKey(c) {
  try {
    if (c.typename === "RGBColor") return Math.round(c.red) + "," + Math.round(c.green) + "," + Math.round(c.blue);
    if (c.typename === "GrayColor") return "g" + Math.round(c.gray * 10) / 10;
    if (c.typename === "CMYKColor") return Math.round(c.cyan * 10) / 10 + "," + Math.round(c.magenta * 10) / 10 + "," + Math.round(c.yellow * 10) / 10 + "," + Math.round(c.black * 10) / 10;
    if (c.typename === "SpotColor") return "spot:" + c.spot.name + ":" + Math.round(c.tint);
    return c.typename;
  } catch (e) { return "?"; }
}

function aiFTPlace(t, ax, ay) {
  var a = t.anchor;
  t.translate(ax - a[0], ay - a[1]);
}

// Recoge, por contenedor, los textos que son hijos directos suyos.
function aiFTCollect(container, out, stats) {
  var n = container.pageItems.length, local = [], subs = [], i, it;
  for (i = 0; i < n; i++) {
    it = container.pageItems[i];
    if (it.typename == "TextFrame") local.push(it);
    else if (it.typename == "GroupItem") subs.push(it);
  }
  if (local.length) out.push({ container: container, tfs: local });
  stats.contenedores++;
  for (i = 0; i < subs.length; i++) aiFTCollect(subs[i], out, stats);
}

function aiFixTextInPlace(doc, breakEm) {
  if (breakEm === undefined) breakEm = 0.6;
  var stats = { lineas: 0, unidas: 0, trozosQuitados: 0, rechazadas: [], omitidos: 0, contenedores: 0, sinCambio: 0 };
  var jobs = [], L, i, k, j;
  for (L = 0; L < doc.layers.length; L++) aiFTCollect(doc.layers[L], jobs, stats);

  for (var jb = 0; jb < jobs.length; jb++) {
    var container = jobs[jb].container, tfs = jobs[jb].tfs;
    var items = [];
    for (i = 0; i < tfs.length; i++) {
      var tf = tfs[i];
      try {
        var s = tf.contents;
        if (s.length === 0) { stats.omitidos++; continue; }
        var ca = tf.textRange.characterAttributes;
        var gb = tf.geometricBounds, anc = tf.anchor;
        if (s.replace(/\s/g, "") === "") gb = [anc[0], 0, anc[0] + ca.size * 0.28 * s.length, 0];   // solo espacios: sin tinta
        items.push({
          tf: tf, z: i, s: s, font: ca.textFont, fontName: ca.textFont.name, size: ca.size,
          fill: ca.fillColor, fillKey: aiFTColorKey(ca.fillColor),
          hs: Math.round(ca.horizontalScale * 10) / 10, vs: Math.round(ca.verticalScale * 10) / 10,
          bs: Math.round(ca.baselineShift * 10) / 10, op: Math.round(tf.opacity),
          stroked: ca.stroked ? 1 : 0, rot: Math.round(ca.rotation * 10) / 10,
          ax: anc[0], ay: anc[1], left: gb[0], right: gb[2]
        });
      } catch (e) { stats.omitidos++; }
    }
    if (items.length < 2) continue;
    items.sort(function (a, b) { if (Math.abs(a.ay - b.ay) > 0.5) return b.ay - a.ay; return a.ax - b.ax; });

    var lines = [], cur = null;
    for (i = 0; i < items.length; i++) {
      var it = items[i], join = false;
      if (cur) {
        var last = cur.items[cur.items.length - 1];
        // misma línea base y mismo tamaño/escala; la fuente y el color PUEDEN cambiar entre trozos (p. ej. la ligadura «fi»
        // que el PDF saca en otra fuente): el texto unido conserva la fuente y el color de cada trozo
        var same = Math.abs(it.ay - last.ay) <= 0.5 && Math.abs(it.size - last.size) < 0.1 &&
          it.hs === last.hs && it.vs === last.vs && it.bs === last.bs && it.op === last.op &&
          it.stroked === last.stroked && it.rot === last.rot && it.stroked === 0 && it.rot === 0;
        if (same) {
          var gap = it.left - last.right;               // hueco entre bordes de tinta
          // con un espacio real en la unión se tolera un hueco de palabra; sin espacio solo el de kerning/bearing
          var ws = /\s$/.test(last.s) || /^\s/.test(it.s);
          var maxGap = last.size * (ws ? breakEm : 0.15);
          if (gap >= -last.size * 0.7 && gap <= maxGap) join = true;   // fuentes script se solapan: se tolera hasta -0,7 em
        }
      }
      if (join) cur.items.push(it);
      else { cur = { items: [it] }; lines.push(cur); }
    }

    for (i = 0; i < lines.length; i++) {
      var ln = lines[i];
      stats.lineas++;
      if (ln.items.length < 2) { stats.sinCambio++; continue; }
      var first = ln.items[0], str = "", firstVis = null, lastVis = null, topZ = 1e9;
      for (k = 0; k < ln.items.length; k++) {
        str += ln.items[k].s;
        if (ln.items[k].s.replace(/\s/g, "") !== "") { if (!firstVis) firstVis = ln.items[k]; lastVis = ln.items[k]; }
        if (ln.items[k].z < topZ) topZ = ln.items[k].z;
      }
      if (!firstVis) continue;   // solo espacios: no se toca
      var targetInk = lastVis.right - firstVis.left;
      var t = null;
      try {
        t = container.textFrames.add();
        t.contents = str;
        var c2 = t.textRange.characterAttributes;
        c2.textFont = first.font; c2.size = first.size; c2.fillColor = first.fill; c2.tracking = 0;
        c2.horizontalScale = first.hs; c2.verticalScale = first.vs; c2.baselineShift = first.bs;
        t.opacity = first.op;
        var pos = 0;
        for (k = 0; k < ln.items.length; k++) {      // estilos distintos por trozo: se aplican carácter a carácter
          var itk = ln.items[k], lenk = itk.s.length;
          if (itk.fontName !== first.fontName || itk.fillKey !== first.fillKey) {
            for (var q = 0; q < lenk; q++) { var chq = t.characters[pos + q].characterAttributes; chq.textFont = itk.font; chq.fillColor = itk.fill; }
          }
          pos += lenk;
        }
        aiFTPlace(t, first.ax, first.ay);
        var b = t.geometricBounds, natural = b[2] - b[0];
        var tol = Math.max(2, targetInk * 0.12);
        if (Math.abs(natural - targetInk) > tol) {
          stats.rechazadas.push("'" + str.substr(0, 40) + "' natural=" + Math.round(natural * 10) / 10 + " objetivo=" + Math.round(targetInk * 10) / 10);
          t.remove(); t = null;
          continue;
        }
        var nChars = str.length - 1;
        if (nChars > 0 && Math.abs(targetInk - natural) > 0.3) {
          c2.tracking = Math.round(((targetInk - natural) / nChars) / first.size * 1000);
        }
        aiFTPlace(t, first.ax, first.ay);
        // alinear el borde de tinta izquierdo con el del primer trozo visible
        var dx = firstVis.left - t.geometricBounds[0];
        if (Math.abs(dx) > 0.05) t.translate(dx, 0);
        // misma posición de apilado que el trozo más alto del conjunto
        try { t.move(first.tf, ElementPlacement.PLACEBEFORE); } catch (em) {}
        for (k = 0; k < ln.items.length; k++) { ln.items[k].tf.remove(); stats.trozosQuitados++; }
        stats.unidas++;
      } catch (err) {
        stats.rechazadas.push("ERROR " + err.message + " @ '" + str.substr(0, 30) + "'");
        if (t) { try { t.remove(); } catch (e3) {} }
      }
    }
  }
  return stats;
}
