// EJEMPLO SANITIZADO de src/lib/<p>-img.ts: el mapa «nombre original → URL del CDN de Medios».
//
// El CDN de GHL RENOMBRA cada archivo al subirlo (queda un identificador) y eso no se puede cambiar, así que
// este objeto es la ÚNICA relación entre el nombre que usa el código y la URL real. Se llena con el mapa
// verificado por SHA-256 (scripts/match_cdn.py --md genera «IMG_URLS-listo.ts.txt»). Se AÑADE al objeto sin
// borrar lo anterior; en cada entrega se agrega un bloque con su comentario.
//
// Los identificadores de abajo son marcadores.

const CDN = "https://assets.cdn.filesafe.space/<location>/media/";

export const IMG_MAP: Record<string, string> = {
  "hero-persona-sonriendo.jpg": CDN + "<id-del-cdn-1>.jpg",
  "logo-horizontal-blanco.svg": CDN + "<id-del-cdn-2>.svg",
  // ===== Entrega 2: fotos nuevas =====
  "ficha-laboratorio.jpg": CDN + "<id-del-cdn-3>.jpg",
  // Una imagen subida por el chat del constructor puede vivir en otro host (`vibe.filesafe.space/<id>/attachments/…`):
  // también va aquí, con la URL completa.
};
