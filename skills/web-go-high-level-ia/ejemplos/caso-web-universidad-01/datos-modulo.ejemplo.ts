// EJEMPLO SANITIZADO del «módulo de datos único» (src/lib/<p>-data.ts) del caso caso-web-universidad-01.
// Muestra el patrón, no el contenido del cliente: todo lo que se repite en más de una página vive aquí,
// no dentro de un componente. Los valores son marcadores; nada de esto es un dato real.

import { IMG_MAP } from "./<p>-img";

export const P_CONFIG = {
  // Número de mensajería pendiente del cliente (vacío hoy). Con indicativo y sin signos (ej. 570000000000).
  // Mientras esté vacío, los botones de mensajería llevan al formulario de la Home.
  whatsapp: "" as string,
  whatsappText: "Hola, quiero más información.",
  // Dominio público (canonical, og:url, schema). Confirmar con el cliente antes de indexar.
  siteUrl: "https://dominio-por-confirmar.example",
  // Respaldo de imágenes. Las imágenes reales se resuelven por IMG_MAP (CDN de Medios); esto solo se usa
  // si un archivo todavía no está en IMG_MAP. Nunca escribir rutas de imagen sueltas en los componentes.
  imgBase: "/imagenes/",
};

/** Ruta de una imagen del proyecto. Ej.: img("hero-persona-sonriendo.jpg"). */
export const img = (file: string) => IMG_MAP[file] ?? `${P_CONFIG.imgBase}${file}`;

/** URL absoluta de una ruta del sitio (para canonical / og:url). Ej.: siteUrl("/contacto"). Sin barra final. */
export const siteUrl = (path = "/") => `${P_CONFIG.siteUrl}${path}`;

/** Destino de los botones de mensajería (o del formulario de la Home mientras no haya número). */
export const waHref = () =>
  P_CONFIG.whatsapp
    ? `https://wa.me/${P_CONFIG.whatsapp}?text=${encodeURIComponent(P_CONFIG.whatsappText)}`
    : "/#orientacion";

// Listados del cliente: tipados, en un solo sitio, con el `id` y el `slug` que usan las rutas.
export type Sede = { id: string; img: string; alt: string; nombre: string; sub: string };
export const SEDES: Sede[] = [
  { id: "sede-a", img: "sede-a-fachada.jpg", alt: "Fachada de la sede A", nombre: "Sede A", sub: "Descripción corta" },
];

/**
 * Medición: UN listener delegado (se monta una vez en __root.tsx) que convierte cualquier clic en un
 * elemento con data-track="evento" en un evento de dataLayer / Clarity. Para medir un botón nuevo basta con
 * ponerle data-track="click_nombre_en_snake_case"; no hay que escribir onClick.
 * (Incidencia C7: sin este listener, los data-track del HTML no medían nada.)
 */
export function initTracking() {
  const onClick = (e: MouseEvent) => {
    const el = (e.target as Element | null)?.closest?.("[data-track]") as HTMLElement | null;
    if (!el) return;
    track(el.dataset["track"] || "click", {
      destino: el.getAttribute("href") || "",
    });
  };
  document.addEventListener("click", onClick);
  return () => document.removeEventListener("click", onClick);
}

// dataLayer / Clarity (GA4/GTM y Microsoft Clarity si el cliente los instala; sin ellos no hace nada).
export function track(name: string, params: Record<string, unknown> = {}) {
  try {
    const w = window as unknown as { dataLayer?: unknown[]; clarity?: (e: string, n: string) => void };
    w.dataLayer = w.dataLayer || [];
    w.dataLayer.push(Object.assign({ event: name }, params));
    if (typeof w.clarity === "function") w.clarity("event", name);
  } catch {
    /* sin medición todavía */
  }
}

// El envío de formularios al CRM (`postTrackingEvent`, IDs de campos personalizados, `form_tracking`) lo
// genera la plataforma con IDs propios de cada cuenta: no se copia entre proyectos y los IDs nunca se
// escriben en notas ni en esta skill.
