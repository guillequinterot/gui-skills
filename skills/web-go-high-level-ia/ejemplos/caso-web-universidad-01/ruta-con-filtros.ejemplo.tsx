// EJEMPLO SANITIZADO: página de listado con filtros en la URL (incidencia J3) y respaldo de imagen (K7).
// Patrón de TanStack Router: `validateSearch` tipa y limpia los parámetros; los filtros se pueden compartir
// y recargar; `replace: true` evita llenar el historial; `resetScroll: false` no salta al inicio.
// Los datos de `ITEMS` son inventados.

import { createFileRoute, useNavigate } from "@tanstack/react-router";

type Filtros = { q?: string; zona?: string };
type Item = { id: string; nombre: string; zona: string; img: string };

const ITEMS: Item[] = [
  { id: "a", nombre: "Elemento A", zona: "norte", img: "elemento-a.jpg" },
  { id: "b", nombre: "Elemento B", zona: "sur", img: "elemento-b.jpg" },
];

export const Route = createFileRoute("/listado")({
  // Solo se aceptan texto y valores conocidos; lo demás se descarta.
  validateSearch: (s: Record<string, unknown>): Filtros => {
    const f: Filtros = {};
    if (typeof s["q"] === "string" && s["q"]) f.q = s["q"];
    if (typeof s["zona"] === "string" && ["norte", "sur"].includes(s["zona"])) f.zona = s["zona"];
    return f;
  },
  head: () => ({
    meta: [
      { title: "Listado | Marca" },
      { name: "description", content: "Descripción de 120 a 155 caracteres, en lenguaje claro y sin promesas." },
    ],
  }),
  component: Listado,
});

function Listado() {
  const filtros = Route.useSearch();
  const navigate = useNavigate({ from: "/listado" });
  const set = (clave: keyof Filtros, valor: string) =>
    navigate({ search: { ...filtros, [clave]: valor || undefined }, replace: true, resetScroll: false });

  const lista = ITEMS.filter(
    (i) =>
      (!filtros.zona || i.zona === filtros.zona) &&
      (!filtros.q || i.nombre.toLowerCase().includes(filtros.q.toLowerCase())),
  );

  return (
    <main>
      <h1>Listado</h1>
      <select value={filtros.zona ?? ""} onChange={(e) => set("zona", e.target.value)}>
        <option value="">Todas las zonas</option>
        <option value="norte">Norte</option>
        <option value="sur">Sur</option>
      </select>
      {lista.length === 0 ? (
        // Estado vacío específico (J4): dice qué se filtró y ofrece salir, no un mensaje genérico.
        <p>No hay elementos con esos filtros. <a href="/listado">Ver todos</a></p>
      ) : (
        <ul>
          {lista.map((i) => (
            <li key={i.id}>
              {/* Respaldo (K7): si la foto aún no está en Medios, onError cambia UNA vez a otra imagen */}
              <img
                src={`/imagenes/${i.img}`}
                alt={i.nombre}
                width={400}
                height={300}
                onError={(e) => {
                  const el = e.currentTarget;
                  if (el.dataset["fallback"]) return;
                  el.dataset["fallback"] = "1";
                  el.src = "/imagenes/respaldo.jpg";
                }}
              />
              {i.nombre}
            </li>
          ))}
        </ul>
      )}
    </main>
  );
}
