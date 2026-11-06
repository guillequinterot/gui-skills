// ai_merge_paragraphs_infer.jsx — Illustrator (ExtendScript).
// Une en UN texto de área (texto corrido) las líneas sueltas que forman un párrafo, SIN necesitar el DOM del HTML:
// el documento viene de un PDF, así que no hay nada que consultar; el párrafo se INFIERE de la geometría y se VERIFICA.
//
// Una cadena de líneas es candidata si son textos de punto hermanos (mismo contenedor), con el mismo borde izquierdo
// (±1 pt), misma fuente, tamaño, color y escala, y una distancia entre líneas base constante (0,9–1,5 em: interlineado de párrafo, no filas de una lista).
// Dentro de la cadena, una línea cierra párrafo (se inserta un salto de párrafo) si la primera palabra de la línea siguiente
// habría cabido en su sitio. Luego se prueba un ancho de caja (ancho de la línea más larga + 1…12 pt) y el texto de área
// SOLO se acepta si sus líneas son exactamente las originales (mismo ajuste que el PDF). Si no, no se toca nada.
// Separación silábica desactivada; interlineado fijo = el de la cadena; alineación izquierda.
//
//   aiMergeParagraphsInfer(doc, dry) -> { cadenas, unidas, lineasAbsorbidas, rechazadas:[...], detalle:[...] }

function aiMP_norm(s) {
  return String(s).replace(new RegExp(String.fromCharCode(160), "g"), " ").replace(new RegExp("[" + String.fromCharCode(0x2028) + String.fromCharCode(3) + "\\r\\n]", "g"), " ").replace(/\s+/g, " ").replace(/^ /, "").replace(/ $/, "");
}

function aiMP_colorKey(c) {
  try {
    if (c.typename === "RGBColor") return Math.round(c.red) + "," + Math.round(c.green) + "," + Math.round(c.blue);
    if (c.typename === "GrayColor") return "g" + Math.round(c.gray * 10) / 10;
    if (c.typename === "CMYKColor") return Math.round(c.cyan * 10) / 10 + "," + Math.round(c.magenta * 10) / 10 + "," + Math.round(c.yellow * 10) / 10 + "," + Math.round(c.black * 10) / 10;
    if (c.typename === "SpotColor") return "spot:" + c.spot.name + ":" + Math.round(c.tint);
    return c.typename;
  } catch (e) { return "?"; }
}

function aiMP_collect(container, out) {
  var n = container.pageItems.length, local = [], subs = [], i, it;
  for (i = 0; i < n; i++) {
    it = container.pageItems[i];
    if (it.typename == "TextFrame") local.push(it);
    else if (it.typename == "GroupItem") subs.push(it);
  }
  if (local.length) out.push({ container: container, tfs: local });
  for (i = 0; i < subs.length; i++) aiMP_collect(subs[i], out);
}

// ancho natural (tinta) de un texto de punto temporal con los atributos de la cadena
function aiMP_measure(container, str, ref) {
  var t = container.textFrames.add();
  t.contents = str;
  var c = t.textRange.characterAttributes;
  c.textFont = ref.font; c.size = ref.size; c.tracking = ref.tracking;
  c.horizontalScale = ref.hs; c.verticalScale = ref.vs;
  var b = t.geometricBounds, w = b[2] - b[0];
  t.remove();
  return w;
}

function aiMP_firstWord(s) {
  var m = /^\s*(\S+)/.exec(s);
  return m ? m[1] : "";
}

function aiMergeParagraphsInfer(doc, dry) {
  var res = { cadenas: 0, unidas: 0, lineasAbsorbidas: 0, rechazadas: [], detalle: [] };
  var jobs = [], L, jb, i, k;
  for (L = 0; L < doc.layers.length; L++) {
    if (doc.layers[L].name == "_fuera-de-mesa (oculto)") continue;
    aiMP_collect(doc.layers[L], jobs);
  }
  for (jb = 0; jb < jobs.length; jb++) {
    var container = jobs[jb].container, tfs = jobs[jb].tfs, items = [];
    for (i = 0; i < tfs.length; i++) {
      var tf = tfs[i];
      try {
        if (String(tf.kind).indexOf("POINT") < 0) continue;
        var s = tf.contents;
        if (s.replace(/\s/g, "") === "" || s.indexOf("\r") >= 0 || s.indexOf(String.fromCharCode(3)) >= 0) continue;
        var mixed = false;
        try {   // estilos mezclados dentro de la línea: no se unen (si el último carácter no se deja leer, se asume uniforme)
          var chs = tf.textRange.characters, c0 = chs[0].characterAttributes, cN = chs[chs.length - 1].characterAttributes;
          if (c0.textFont.name !== cN.textFont.name || Math.abs(c0.size - cN.size) > 0.05) mixed = true;
        } catch (eMix) {}
        if (mixed) continue;
        var ca = tf.textRange.characterAttributes;   // se lee DESPUÉS de recorrer los caracteres (si no, el rango queda inválido)
        var gb = tf.geometricBounds, an = tf.anchor;
        items.push({
          tf: tf, z: i, s: s, font: ca.textFont, fontName: ca.textFont.name, size: ca.size,
          fill: ca.fillColor, fillKey: aiMP_colorKey(ca.fillColor), hs: Math.round(ca.horizontalScale * 10) / 10,
          vs: Math.round(ca.verticalScale * 10) / 10, bs: Math.round(ca.baselineShift * 10) / 10, tracking: ca.tracking,
          op: Math.round(tf.opacity), ax: an[0], ay: an[1], left: gb[0], right: gb[2]
        });
      } catch (e) {}
    }
    if (items.length < 2) continue;
    // columnas: mismo borde izquierdo y mismo estilo
    items.sort(function (a, b) { if (Math.abs(a.left - b.left) > 1) return a.left - b.left; return b.ay - a.ay; });
    var cols = [], cur = null;
    for (i = 0; i < items.length; i++) {
      var it = items[i];
      var same = cur && Math.abs(it.left - cur.left) <= 1 && it.fontName === cur.fontName && Math.abs(it.size - cur.size) < 0.1 &&
        it.fillKey === cur.fillKey && it.hs === cur.hs && it.vs === cur.vs && it.bs === cur.bs && it.op === cur.op;
      if (same) cur.items.push(it);
      else { cur = { left: it.left, fontName: it.fontName, size: it.size, fillKey: it.fillKey, hs: it.hs, vs: it.vs, bs: it.bs, op: it.op, items: [it] }; cols.push(cur); }
    }
    for (var ci = 0; ci < cols.length; ci++) {
      var col = cols[ci];
      if (col.items.length < 2) continue;
      col.items.sort(function (a, b) { return b.ay - a.ay; });
      // cadenas por interlineado constante
      var chains = [], ch = null, d0 = 0;
      for (i = 0; i < col.items.length; i++) {
        var li = col.items[i];
        if (ch) {
          var prev = ch[ch.length - 1], d = prev.ay - li.ay;
          if (d >= col.size * 0.9 && d <= col.size * 1.5 && (ch.length === 1 || Math.abs(d - d0) <= 0.6)) { if (ch.length === 1) d0 = d; ch.push(li); continue; }
        }
        ch = [li]; chains.push(ch); d0 = 0;
      }
      for (var qi = 0; qi < chains.length; qi++) {
        var chain = chains[qi];
        if (chain.length < 2) continue;
        res.cadenas++;
        var lead = chain[0].ay - chain[1].ay;
        var ref = chain[0];
        var rows = [], wmax = 0;
        for (i = 0; i < chain.length; i++) { rows.push(aiMP_norm(chain[i].s)); wmax = Math.max(wmax, chain[i].right - chain[i].left); }
        var label = "'" + rows[0].substr(0, 36) + "' x" + chain.length;
        if (dry) { res.detalle.push(label + " lead=" + Math.round(lead * 10) / 10 + " wmax=" + Math.round(wmax)); continue; }
        // saltos de párrafo: la línea cierra párrafo si la primera palabra de la siguiente habría cabido
        var W0 = wmax + 2, text = rows[0];
        try {
          for (i = 1; i < chain.length; i++) {
            var fw = aiMP_firstWord(rows[i]);
            var fits = fw !== "" && aiMP_measure(container, rows[i - 1] + " " + fw, ref) <= W0 - 0.5;
            text += (fits ? "\r" : " ") + rows[i];
          }
        } catch (em) { res.rechazadas.push(label + " ERROR medir: " + em.message); continue; }
        var tracks = [];
        for (i = 0; i < chain.length; i++) tracks.push(chain[i].tracking);
        tracks.sort(function (a, b) { return a - b; });
        var trk = tracks[Math.floor(tracks.length / 2)];
        var widths = [wmax + 1, wmax + 2, wmax + 4, wmax + 6, wmax + 9, wmax + 12, wmax + 0.5], got = null, wTried = [];
        var areaT = null;
        for (var wi = 0; wi < widths.length; wi++) {
          var rect = container.pathItems.rectangle(ref.ay + ref.size * 1.05, ref.left, widths[wi], chain.length * lead + ref.size * 2);
          var t = container.textFrames.areaText(rect);
          t.contents = text;
          var c = t.textRange.characterAttributes;
          c.textFont = ref.font; c.size = ref.size; c.fillColor = ref.fill; c.tracking = trk;
          c.horizontalScale = ref.hs; c.verticalScale = ref.vs; c.baselineShift = ref.bs;
          c.autoLeading = false; c.leading = lead;
          var pa = t.textRange.paragraphAttributes; pa.justification = Justification.LEFT; pa.hyphenation = false;
          var okw = (t.lines.length === chain.length), q;
          for (q = 0; okw && q < chain.length; q++) { if (aiMP_norm(t.lines[q].contents) !== rows[q]) okw = false; }
          if (okw) { areaT = t; got = widths[wi]; break; }
          wTried.push(Math.round(widths[wi]) + ":" + t.lines.length);
          t.remove();
        }
        if (!areaT) { res.rechazadas.push(label + " ajuste distinto (anchos " + wTried.join(" ") + ")"); continue; }
        // calibrar primera línea base con la tinta del primer renglón original
        var dA = areaT.duplicate(), oa = dA.createOutline(), topA = oa.geometricBounds[1]; oa.remove();
        var dP = ref.tf.duplicate(), op = dP.createOutline(), topP = op.geometricBounds[1]; op.remove();
        areaT.translate(0, topP - topA);
        // ajustar la altura de la caja a su texto
        var tp = areaT.textPath, topY = tp.top;
        tp.height = chain.length * lead + ref.size * 0.5; tp.top = topY;
        if (areaT.lines.length !== chain.length) { res.rechazadas.push(label + " altura rompió el ajuste"); areaT.remove(); continue; }
        try { areaT.move(ref.tf, ElementPlacement.PLACEBEFORE); } catch (emv) {}
        for (i = 0; i < chain.length; i++) { try { chain[i].tf.remove(); res.lineasAbsorbidas++; } catch (er) {} }
        res.unidas++;
        res.detalle.push(label + " -> area ancho " + Math.round(got));
      }
    }
  }
  return res;
}
