# Retirada controlada del índice (documentos/PDF) [ClickUp]
1. Conseguir los accesos al servidor o CDN y a GSC.
2. Hacer el inventario de URLs en CSV, sin duplicados y comprobando que cada una abre.
3. Confirmar la infraestructura y cómo se sirven las cabeceras.
4. Poner `X-Robots-Tag: noindex` solo en los documentos a retirar. Deben seguir públicos y responder 200. **No usar robots.txt**: bloquearía el rastreo y Google no vería la orden.
5. Probar con un piloto de unas 10 URLs, validando la cabecera con cURL o Python.
6. Desplegar en todo el conjunto y lanzar una auditoría automatizada.
7. Pedir retiradas temporales en GSC para los casos urgentes.
8. Monitorear con la URL Inspection API.
9. Entregar un reporte final con el estado de cada URL y un protocolo de encarpetado (`/documentos/<tipo>/<año>/`, con noindex por ruta).
10. Dejar escritas las decisiones de retención del cliente (despublicar o eliminar, repositorio permanente).

Requiere aprobación antes de los pasos 4, 6 y 7, porque tocan el sitio en vivo.


## Propuesta al cliente [Drive]
Para vender e implementar este procedimiento usa `assets/templates/technical-proposal-deck.md`. El plan va en 7 pasos con piloto y monitoreo vía URL Inspection API, y la prevención archiva por carpetas `/documentos/{tipo}/{año}/` con noindex heredado. Ver `references/drive-deliverables-and-guidelines.md` §5.


## Ampliación [ClickUp 2]: disparador, límites y reglas de datos

Origen: un proyecto real de desindexación de unos 800 PDF con datos personales (anonimizado).

- **Disparador y solución estructural.** El caso nace de un reporte de atención al usuario (documentos con datos de personas visibles en la web y en Google). `noindex` es la **medida de contención**; la solución estructural es la **consulta controlada** (el usuario consulta su documento por número de contrato o de interacción, de modo que nada sea público). Proponer ambas y dejar claro cuál es cuál.
- **Una sola directiva.** Fijar `noindex` (no mezclar `follow`/`nofollow`: en un PDF sin enlaces es irrelevante y confunde). Planificar que la implementación de la cabecera puede requerir una **segunda pasada**: en el caso real la tarea se abrió dos veces.
- **Paso 3 (infraestructura).** Identificar el alojamiento (Apache, NGINX, WordPress, CDN), confirmar que se pueden modificar las cabeceras HTTP y que **robots.txt no bloquea** el rastreo de esos documentos («si se bloquea, Google no puede leer la orden»).
- **Retirada temporal en Search Console:** dura ~6 meses, acelera la salida pero **no reemplaza** el `noindex`.
- **URL Inspection API:** tope de **2.000 consultas por día**; planear el monitoreo de ~800 URLs en varios días. Verificar también que los PDF **nuevos** no se indexan.
- **Fuera de alcance (se cotiza aparte):** caducidad de las actas, copia de seguridad en almacenamiento frío, contraseñas en los PDF, reorganizar los PDF antiguos.
- **Reglas de datos:** no copiar nombres ni datos de los documentos en tareas, comentarios ni informes (usar la URL o el ID del archivo); no prometer fechas de salida de Google; carpeta restringida para el proyecto.
- **Decisiones pendientes con el cliente** (registrarlas en el reporte final): días de publicación de cada acta, si al vencer se despublica o se elimina, y si se quiere un repositorio permanente.
- **Tareas posteriores al reporte:** implementación y revisión del encarpetado (`/documentos/<tipo>/<año>/` con `noindex` por ruta).
- **Dependencias previas:** crear o recibir la propiedad de Search Console con permisos completos; accesos al servidor.
- Estimación del caso real: ~8,5 h entre todos los pasos con horas (inventario 2 h, monitoreo 2 h, reporte 1,5 h); prioridad Alta para los pasos 1-7 y Normal para 8-10. Cada paso es una tarea numerada `[Proyecto] N. paso`; la descripción de la lista lleva objetivo, roles, aprobación y duración, técnica aprobada, plan por semanas, fuera de alcance y reglas.
