# Auditoría previa al lanzamiento (sitio en stage)

> Tres frentes sobre el sitio en el entorno de pruebas, antes de migrar. Se socializa con el equipo y luego con el cliente. Complementa [launch-checklist-new-site.md](../../references/launch-checklist-new-site.md) y [migration-redirects-and-validation.md](../../references/migration-redirects-and-validation.md). Las horas son de una plantilla de referencia: medir las reales.

**Sitio en stage:** {url} · **Fecha:** {dd/mm/aaaa} · **Respaldo previo:** {sí/no}

## SEO (≈ 3 h de referencia)
- [ ] Estructura de URLs: solo `a-z 0-9 -`, sin mayúsculas ni guiones bajos; coincide con el documento de arquitectura.
- [ ] Metadatos: title y meta únicos, con la keyword y dentro del límite del cliente.
- [ ] Imágenes: alt útil, nombre de archivo con la keyword (nombrado desde el diseño), peso por debajo del tope acordado.
- [ ] Encabezados: un H1, jerarquía sin saltos, sin H1 en el logotipo.
- [ ] Códigos de respuesta: sin 404 internos ni cadenas de redirección.
- [ ] El entorno de pruebas está bloqueado a los buscadores y **se levanta el bloqueo en el lanzamiento** (verificar el día del lanzamiento).

## UX (≈ 3 h)
- [ ] Diagramación de módulos y estilos coinciden con el prototipo aprobado.
- [ ] Navegación: el menú replica el árbol firmado en el documento de arquitectura.
- [ ] Responsive en los anchos acordados.
- [ ] Core Web Vitals revisados (laboratorio; el dato de campo tarda unos 28 días).

## Front (≈ 6 h)
- [ ] Formularios: envían al canal correcto y el lead de prueba llega al CRM.
- [ ] Core Web Vitals, seguridad (cabeceras, formularios) y enlaces rotos.
- [ ] Contenido: sin texto de relleno ni placeholders.
- [ ] **Las herramientas de analítica están conectadas** (GA4, GTM, píxeles) y los eventos se disparan al cambiar de ruta.
- [ ] Metadatos y responsive verificados en el HTML publicado (ver código fuente, no solo el inspector).

## Cierre
- [ ] Hallazgos clasificados (Alta / Media / Baja) con responsable; los de prioridad Alta se corrigen antes de migrar.
- [ ] Socialización interna → socialización con el cliente → aprobación escrita.
- [ ] URL de lanzamiento, matriz del sitio, plan de redirecciones y accesos a servidor y dominio a mano.
- [ ] Post-lanzamiento: auditoría de rastreo, comprobación de los 301 y línea base de métricas marcada.
