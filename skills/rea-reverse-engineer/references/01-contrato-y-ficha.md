# 01 · Contrato de llamada y Ficha de referencia

## Principio: porción, no skill entera

Una skill que necesita entender algo **no carga REA completa**. Pide una porción acotada y recibe una ficha. Quien llama conserva el control del proyecto y de la construcción.

```
consumidor ──(consumidor, referencia, pregunta, profundidad máx., entrega)──▶ rea-reverse-engineer
consumidor ◀──(resumen ≤ 1 página + ruta de la ficha completa + capturas)────  rea-reverse-engineer
```

## Los cinco campos

1. **consumidor** — quién llama y para qué proceso (determina la receta de [03](03-recetas-por-consumidor.md)).
2. **referencia** — URL, ruta local, nombre de app/plugin, captura, repositorio. Si dice «mi app» sin nombre: preguntar cuál (no elegir una de ejemplo).
3. **pregunta** — concreta y respondible («qué tipografía y escala usa el hero», «cómo carga el catálogo», «qué schema tiene»). Una referencia sin pregunta se resuelve con la **pregunta por defecto** del consumidor ([03](03-recetas-por-consumidor.md)).
4. **profundidad máxima** — N0–N3; por defecto N1. Subir requiere decir qué pregunta no cerró el nivel previo.
5. **entrega** — resumen corto al consumidor + ficha completa en `<carpeta del proyecto>/referencias/<slug>-<fecha>/`.

## Flujo (siempre el mismo)

1. **Clasificar** la referencia (web renderizada · web con flujo · app de escritorio/móvil · paquete/plugin · captura/imagen · binario · video → derivar a `video-editing-ai-agent`).
2. **Elegir nivel mínimo** que responda la pregunta; avisar si requiere algo no disponible (REA sin instalar).
3. **Ejecutar** y **mirar** (capturas/imágenes con Read).
4. **Redactar la ficha** con la plantilla `templates/ficha-referencia.md`.
5. **Entregar** el resumen y la ruta; si hay hallazgos que cambian decisiones, anotarlos en las notas del proyecto (y en la nota de Obsidian, si el usuario la usa).

## Estructura de la ficha

| Sección | Contenido | Regla |
|---|---|---|
| Identidad | referencia, fecha, nivel usado, herramienta/versión, huella (URL/SHA-256 si es archivo) | sin esto no es reproducible |
| Pregunta | la pregunta literal | |
| **Observado** | lo medido o visto, con su fuente (captura, `probe.json`, Evidence ID de REA) | solo hechos |
| **Inferido** | conclusiones con su razón y confianza (alta/media/baja) | marcar cada una |
| **Desconocido** | lo que no se pudo ver y qué haría falta (otro nivel, permiso, sesión) | no rellenar con suposiciones |
| Mantener / Adaptar / Evitar | decisiones para el consumidor | alineado con `direct-visual-design` |
| Límites | qué no cubre la sonda; qué no se debe copiar | |
| Siguiente paso | una acción concreta | |

### Resumen al consumidor (≤ 1 página)

Cinco a diez líneas: qué es, 3–5 hallazgos clave (con etiqueta observado/inferido), qué conviene mantener/adaptar/evitar, qué quedó desconocido, ruta de la ficha y de las capturas. Nada de volcar `probe.json`.

## Confianza

- **Alta:** medido directamente y repetible (valor computado, cabecera, estructura del DOM, Evidence de REA).
- **Media:** inferido de varios indicios coherentes (huellas de tecnología + rutas + cabeceras).
- **Baja:** una sola señal o dependiente de estado no observado (hover, sesión, A/B).

## Qué NO entrega esta skill

- Código, componentes o textos copiados de un tercero.
- Un diseño o contenido ya construido: eso es del consumidor.
- Veredictos legales. Si la referencia tiene licencia o restricciones visibles, se señalan y se escala al usuario.
