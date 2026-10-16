// ai_fix_text.jsx — Illustrator (ExtendScript).
// Los PDF de Chromium abren en Illustrator con UN TEXTO POR LETRA. Este script, sobre el documento activo,
// agrupa las letras de cada línea (misma línea base, mismo tamaño y misma fuente) en UN solo texto de punto,
// con la misma fuente, tamaño y color, anclado en la misma línea base, y ajusta el tracking para que la línea
// mida lo mismo que el original. Devuelve un resumen. Uso: se llama desde ai_pipeline.ps1 (no a mano).
//
// Parámetros leídos de variables globales: AI_BREAK (separación mínima, en em, que parte una línea en dos textos).

// anchor es de solo lectura al escribir: se coloca con translate (dx, dy) hasta que el ancla coincida con la original.
function aiPlace(t, ax, ay) {
  var a = t.anchor;
  t.translate(ax - a[0], ay - a[1]);
}

function aiColorKey(c) {
  try {
    if (c.typename === "RGBColor") return Math.round(c.red) + "," + Math.round(c.green) + "," + Math.round(c.blue);
    if (c.typename === "GrayColor") return "g" + Math.round(c.gray);
    if (c.typename === "CMYKColor") return Math.round(c.cyan) + "," + Math.round(c.magenta) + "," + Math.round(c.yellow) + "," + Math.round(c.black);
    return c.typename;
  } catch (e) { return "?"; }
}

function aiFixText(doc, breakEm) {
  var frames = doc.textFrames;
  var items = [];
  var i;
  for (i = 0; i < frames.length; i++) {
    var tf = frames[i];
    var ca = tf.textRange.characterAttributes;
    var gb = tf.geometricBounds;           // [izq, arriba, der, abajo] en coords de documento (y hacia arriba)
    var anc;
    try { anc = tf.anchor; } catch (e) { continue; }
    items.push({
      tf: tf,
      s: tf.contents,
      font: ca.textFont,
      fontName: ca.textFont.name,
      size: ca.size,
      fill: ca.fillColor,
      fillKey: aiColorKey(ca.fillColor),
      ax: anc[0],
      ay: anc[1],
      right: gb[2],
      left: gb[0]
    });
  }
  // orden: línea (y desc.), luego x
  items.sort(function (a, b) {
    if (Math.abs(a.ay - b.ay) > 0.5) return b.ay - a.ay;   // y mayor = más arriba
    return a.ax - b.ax;
  });

  // agrupar en líneas
  var lines = [];
  var cur = null;
  for (i = 0; i < items.length; i++) {
    var it = items[i];
    var join = false;
    if (cur) {
      var last = cur.items[cur.items.length - 1];
      var sameLine = Math.abs(it.ay - last.ay) <= 0.5 && Math.abs(it.size - last.size) < 0.1 && it.fontName === last.fontName && it.fillKey === last.fillKey;
      if (sameLine) {
        var gap = it.ax - last.ax;
        // avance esperado de la letra anterior: ancho de su caja si es visible; si es un espacio, ~0,3 em
        var adv = (last.s === " " || last.s === " ") ? last.size * 0.3 : (last.right - last.ax);
        if (gap <= adv + last.size * breakEm) join = true;
      }
    }
    if (join) cur.items.push(it);
    else { cur = { items: [it] }; lines.push(cur); }
  }

  var created = 0, removedFrames = 0;
  var outLines = [];
  for (i = 0; i < lines.length; i++) {
    var ln = lines[i];
    var first = ln.items[0];
    var str = "";
    var k;
    for (k = 0; k < ln.items.length; k++) str += ln.items[k].s;
    if (str.replace(/\s/g, "") === "") {
      // línea solo de espacios: se descarta
      for (k = 0; k < ln.items.length; k++) { ln.items[k].tf.remove(); removedFrames++; }
      continue;
    }
    // ancho objetivo = de la primera letra visible a la última visible (tinta)
    var firstVis = null, lastVis = null;
    for (k = 0; k < ln.items.length; k++) {
      if (ln.items[k].s.replace(/\s/g, "") !== "") { if (!firstVis) firstVis = ln.items[k]; lastVis = ln.items[k]; }
    }
    var targetInk = lastVis.right - firstVis.left;

    var t = doc.textFrames.add();
    t.contents = str;
    var ca2 = t.textRange.characterAttributes;
    ca2.textFont = first.font;
    ca2.size = first.size;
    ca2.fillColor = first.fill;
    ca2.tracking = 0;
    aiPlace(t, first.ax, first.ay);

    // ajuste de tracking para igualar el ancho original
    var b = t.geometricBounds;
    var natural = b[2] - b[0];
    var n = str.length - 1;
    if (n > 0 && Math.abs(targetInk - natural) > 0.4) {
      var trk = ((targetInk - natural) / n) / first.size * 1000;
      ca2.tracking = Math.round(trk);
      aiPlace(t, first.ax, first.ay);
    }
    created++;
    outLines.push({ frame: t, str: str, ax: first.ax, ay: first.ay, size: first.size, fontName: first.fontName, font: first.font, fill: first.fill });
    for (k = 0; k < ln.items.length; k++) { ln.items[k].tf.remove(); removedFrames++; }
  }
  return { created: created, removed: removedFrames, lines: outLines };
}


// ---------------------------------------------------------------------------------------------------------------
// Párrafos: une las líneas que el HTML maqueta como un mismo bloque en UN texto de área (texto corrido).
// paras = datos de scripts/extract_paragraphs.py (x, w, align, size, ls, lh, runs[[{t, top, bottom}]]).
// Solo se acepta el texto de área si su ajuste de líneas coincide exactamente con el del navegador.
// ---------------------------------------------------------------------------------------------------------------
function aiNorm(s) {
  return String(s).replace(/\u00A0/g, " ").replace(/[\u2028\u0003\r\n]/g, " ").replace(/\s+/g, " ").replace(/^ /, "").replace(/ $/, "");
}

function aiJust(a) {
  if (a === "center") return Justification.CENTER;
  if (a === "right" || a === "end") return Justification.RIGHT;
  return Justification.LEFT;
}

function aiMakeArea(doc, P, L0, text, width, top, nLines, trk, ox) {
  var rect = doc.pathItems.rectangle(top, P.x + ox, width, nLines * P.lh + P.size * 2);
  var t = doc.textFrames.areaText(rect);
  t.contents = text;
  var ca = t.textRange.characterAttributes;
  ca.textFont = L0.font;
  ca.size = L0.size;
  ca.fillColor = L0.fill;
  ca.tracking = trk;
  ca.autoLeading = false;
  ca.leading = P.lh;
  var pa = t.textRange.paragraphAttributes;
  pa.justification = aiJust(P.align);
  pa.hyphenation = false;      // Illustrator separa palabras por sílabas por defecto: el navegador no
  return t;
}

function aiWrapMatches(t, expected) {
  var ls = t.lines;
  if (ls.length !== expected.length) return false;
  for (var i = 0; i < expected.length; i++) {
    if (aiNorm(ls[i].contents) !== expected[i]) return false;
  }
  return true;
}

function aiMergeParagraphs(doc, paras, lines, ab) {
  if (!ab) { var r0 = doc.artboards[0].artboardRect; ab = { left: r0[0], top: r0[1] }; }
  var top0 = ab.top;
  var ox = ab.left;
  var used = {};
  var cache = {};
  var merged = 0, failed = 0, absorbed = 0;
  var dbg = [];
  var p, r, j, k, i;
  for (p = 0; p < paras.length; p++) {
    var P = paras[p];
    t = null;
    try {
    var runsFound = [];
    var ok = true;
    var expected = [];
    for (r = 0; r < P.runs.length && ok; r++) {
      var run = P.runs[r];
      var found = [];
      for (j = 0; j < run.length; j++) {
        var dl = run[j];
        var want = aiNorm(dl.t);
        var hit = -1;
        for (k = 0; k < lines.length; k++) {
          if (used[k]) continue;
          var L = lines[k];
          var ycss = top0 - L.ay;
          if (ycss < dl.top - 3 || ycss > dl.bottom + 3) continue;
          if (aiNorm(L.str) !== want) continue;
          hit = k; break;
        }
        if (hit < 0) { ok = false; break; }
        found.push(hit);
        expected.push(want);
      }
      runsFound.push(found);
    }
    if (!ok) { failed++; dbg.push('SIN COINCIDENCIA: ' + aiNorm(P.runs[0][0].t).substr(0, 50) + ' | x=' + Math.round(P.x)); continue; }

    var L0 = lines[runsFound[0][0]];
    var text = "";
    for (r = 0; r < runsFound.length; r++) {
      var parts = [];
      for (j = 0; j < runsFound[r].length; j++) parts.push(aiNorm(lines[runsFound[r][j]].str));
      text += (r ? "\r" : "") + parts.join(" ");
    }
    var trk = L0.frame.textRange.characterAttributes.tracking;
    var key = L0.fontName + "|" + L0.size + "|" + P.lh + "|" + P.align;
    var guess = L0.size * 1.05;
    var widths = [P.w, P.w + 1, P.w + 2, P.w + 4, P.w - 1, P.w - 2, P.w + 8, P.w + 12];
    var t = null;
    var gotStr = '';
    for (i = 0; i < widths.length; i++) {
      var off = (cache[key] !== undefined) ? cache[key] : guess;
      var cand = aiMakeArea(doc, P, L0, text, widths[i], L0.ay + off, expected.length, trk, ox);
      if (aiWrapMatches(cand, expected)) { t = cand; break; }
      if (i === 0) { var got = []; for (var gi = 0; gi < cand.lines.length; gi++) got.push(aiNorm(cand.lines[gi].contents)); gotStr = got.join(' / '); }
      cand.remove();
    }
    if (!t) { failed++; dbg.push('AJUSTE DISTINTO: ' + expected[0].substr(0, 40) + ' | w=' + Math.round(P.w) + ' lineas=' + expected.length + ' trk=' + trk + ' GOT[' + gotStr + '] EXP[' + expected.join(' / ') + ']'); continue; }

    if (cache[key] === undefined) {
      // calibrar la distancia entre el borde superior del marco y la línea base (comparando la tinta de la 1.ª línea)
      var dA = t.duplicate(); var oa = dA.createOutline(); var topA = oa.geometricBounds[1]; oa.remove();
      var dP = L0.frame.duplicate(); var op = dP.createOutline(); var topP = op.geometricBounds[1]; op.remove();
      var dy = topP - topA;
      t.translate(0, dy);
      cache[key] = guess + dy;
    }
    var all = [];
    for (r = 0; r < runsFound.length; r++) for (j = 0; j < runsFound[r].length; j++) all.push(runsFound[r][j]);
    for (j = 0; j < all.length; j++) { used[all[j]] = true; lines[all[j]].frame.remove(); absorbed++; }
    merged++;
    } catch (err) {
      failed++;
      dbg.push('ERROR: ' + err.message + ' @ ' + aiNorm(P.runs[0][0].t).substr(0, 40));
      if (t) { try { t.remove(); } catch (e2) {} }
    }
  }
  return { merged: merged, failed: failed, absorbed: absorbed, dbg: dbg };
}


// Recoge, como «líneas», los textos de punto (un texto por línea) que ya existen dentro de una mesa de trabajo.
// Sirve para aplicar la unión de párrafos directamente sobre un documento ya generado.
function aiCollectLines(doc, ab) {
  var out = [];
  var frames = doc.textFrames;
  for (var i = 0; i < frames.length; i++) {
    var tf = frames[i];
    if (tf.kind !== TextType.POINTTEXT) continue;
    var gb = tf.geometricBounds;
    var cx = (gb[0] + gb[2]) / 2, cy = (gb[1] + gb[3]) / 2;
    if (cx < ab.left || cx > ab.left + 1920 || cy > ab.top || cy < ab.top - 1080) continue;
    var anc;
    try { anc = tf.anchor; } catch (e) { continue; }
    var ca = tf.textRange.characterAttributes;
    out.push({ frame: tf, str: tf.contents, ax: anc[0], ay: anc[1], size: ca.size, fontName: ca.textFont.name, font: ca.textFont, fill: ca.fillColor });
  }
  return out;
}
