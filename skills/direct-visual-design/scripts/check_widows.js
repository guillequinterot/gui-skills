/* Detector de viudas para páginas HTML (direct-visual-design · typography.md § 4).
   Uso: pegar en la consola del navegador o en una herramienta de JavaScript del navegador
   (Playwright, pane del navegador) con la página abierta al ancho que se quiere revisar.
   Devuelve la lista de textos cuya última línea tiene una sola palabra; [] = sin viudas.
   Las palabras unidas con espacio duro (&nbsp;) cuentan como una sola. Ignora .sr-only y lo oculto.
   Para varios anchos sin cambiar la ventana: cargar la página en un <iframe> de ese ancho y pasar
   su contentDocument a checkWidows(doc). */
(function () {
  function checkWidows(doc) {
    doc = doc || document;
    var out = [];
    var sel = 'main p, main li, main h1, main h2, main h3, main h4, main blockquote, main summary, main address, main figcaption, footer p';
    doc.querySelectorAll(sel).forEach(function (el) {
      if (el.closest('.sr-only') || el.offsetParent === null) return;
      // solo el bloque de texto más interno (evita contar dos veces un <li> que contiene <p>)
      if (Array.prototype.some.call(el.children, function (c) { return /^(P|LI|UL|OL|DIV)$/.test(c.tagName); })) return;
      var words = [];
      var walker = doc.createTreeWalker(el, NodeFilter.SHOW_TEXT);
      var node;
      while ((node = walker.nextNode())) {
        var data = node.data.replace(/ /g, '\u0001'); // &nbsp; une las palabras
        var re = /[^\s]+/g, m;
        while ((m = re.exec(data))) {
          var r = doc.createRange();
          r.setStart(node, m.index);
          r.setEnd(node, m.index + m[0].length);
          var rects = r.getClientRects();
          if (rects.length) words.push({ t: m[0].replace(/\u0001/g, ' '), top: rects[0].top, bottom: rects[rects.length - 1].top });
        }
      }
      if (words.length < 3) return;
      var last = words[words.length - 1], prev = words[words.length - 2];
      if (last.top - prev.bottom > 4 && last.t.indexOf(' ') === -1) {
        out.push(el.textContent.trim().replace(/\s+/g, ' ').slice(0, 60) + '… [' + last.t + ']');
      }
    });
    return out;
  }
  if (typeof window !== 'undefined') window.checkWidows = checkWidows;
  return checkWidows(document);
})();
