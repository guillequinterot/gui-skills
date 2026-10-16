<!-- VIBE:BEGIN -->
(Conservar tal cual el bloque que genera la plataforma: no editarlo ni moverlo.)
<!-- VIBE:END -->

# <Proyecto> — guía para quien programa este proyecto

Lee este archivo completo antes de tocar código. Aquí está lo que ya está decidido y aprobado; si algo de lo que te piden choca con esto, avisa en el chat en vez de improvisar.

## 0. Memoria del proyecto: `README.md` (obligatorio)
1. **Antes de empezar cualquier tarea:** lee `README.md` (*Estado actual*, *Pendientes*, *Próxima acción* y el final del *Registro de cambios*) y guíate por él.
2. **Al terminar cada tarea, sin que te lo pidan:** actualiza `README.md` — estado, casillas de pendientes, próxima acción, fecha y una entrada nueva en el registro (qué cambió, por qué, cómo se comprobó, qué queda).
3. **Si falta o se contradice algo** (dato del cliente, enlace, imagen): anótalo en *Pendientes del cliente* y deja el marcador `.placeholder`.
4. No borres el historial del registro; solo agrega. Una tarea no está terminada hasta que `README.md` refleja lo que hiciste.

## 1. Qué es este proyecto
<Cliente, campaña, público, acciones que debe provocar el sitio> + tabla de páginas (ruta · archivo · estado).

## 2. Reglas de oro
1. No inventes contenido (cifras, fechas, requisitos, testimonios, enlaces). Marcador `.placeholder` + aviso.
2. No prometas nada (<lista según el cliente>).
3. No cambies lo aprobado sin pedido explícito.
4. Una sola fuente de datos: `src/lib/<proyecto>-data.ts`.
5. Español de <país>, trato de «tú», lenguaje claro.
6. Accesible por defecto: un `h1`, jerarquía, `alt`, foco visible, teclado.

## 3. Pila técnica y qué NO tocar
- TanStack Start + Router, React 19, TypeScript estricto, Tailwind v4.
- Estilos de marca = `src/<proyecto>.css`. No Tailwind ni `components/ui/*` en páginas de marca.
- No nombres una clase propia como una de Tailwind (`container`, `hidden`, `block`, `flex`, `grid`, `fixed`, `relative`…). `.container` del kit lleva `max-width:none; width:100%; margin-inline:0;`.
- **No edites:** `src/routeTree.gen.ts`, `.env`, `vite.config.ts`, `src/start.ts`, `src/server.ts`, `src/integrations/supabase/*`, `src/lib/error-*`, `src/lib/vibe-error-reporting.ts`, `.vibe/`.
- No instales dependencias sin necesidad y aviso. Enlaces internos con `<Link>`; externos con `target="_blank" rel="noopener"`. URLs sin barra final.

## 4. Mapa del código
(archivo → qué hace; `__root.tsx` = shell común; `routes/*`; `components/<p>/*`; `lib/<p>-data.ts`; CSS; `public/`.)

## 5. Sistema de diseño
Tokens (color, tipografías, espacio múltiplos de 4, radios, sombras), piezas del kit reutilizables, motivos de marca, reglas de composición, interacciones ya resueltas (no reescribirlas).

## 6. Imágenes
- Solo fotografía real de la marca. Siempre `img("nombre.jpg")`; nunca rutas sueltas.
- **El CDN de Medios renombra los archivos al subirlos** (no modificable): la relación «nombre original → URL» vive solo en `IMG_URLS` (`<p>-data.ts`); al añadir imágenes, **añade** sin borrar y empareja viendo la imagen.
- `width`/`height`, `alt` descriptivo en español, `loading="lazy"` salvo la principal.

## 7. Datos y contenido
Oferta/datos vigentes y fuente, qué NO mostrar, enlaces permitidos, pendientes del cliente.

## 8. SEO por página (obligatorio)
`title` único ≤ 60, `description` 120–155, canonical y og:* con `siteUrl()`, un `h1`, schema por tipo de página, `noindex` mientras sea provisional, enlazado interno descriptivo.

## 9. Formularios, CRM y medición
Campos y orden, integración `form_tracking` con sus IDs (no cambiarlos), `data-track="click_nombre"` (listener global en `__root.tsx`), scripts pendientes (Clarity/GA4/GTM).

## 10. Cómo agregar páginas
(Agrupadora: editar `<ruta>.tsx`; ficha dinámica: `<ruta>_.$slug.tsx` para no anidar; copiar el `head()` de una existente; solo componentes/clases del kit.)

## 11. Lista de revisión antes de dar algo por terminado
1. Lo aprobado se ve idéntico. 2. Sin desbordes (375/768/1280/1920). 3. Enlaces del menú a rutas que existen. 4. Un `h1`, `alt`, foco, teclado. 5. SEO completo y schema válido. 6. Nada inventado; pendientes marcados. 7. Sin errores de consola; `npm run build` compila. 8. `README.md` actualizado. 9. Commits claros; nunca reescribas historial publicado.
