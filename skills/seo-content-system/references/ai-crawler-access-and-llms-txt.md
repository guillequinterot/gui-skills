---
tags:
  - seo
  - geo
  - technical
---

# Acceso de bots de IA: robots.txt, llms.txt y verificación

## Índice

- Principio
- Estado de la evidencia
- Bots de entrenamiento vs. bots de recuperación
- Auditar y configurar robots.txt
- El archivo llms.txt
- Cómo verificar que la configuración funciona en la práctica
- Errores frecuentes
- Lista de revisión

## Principio

Ninguna estrategia de contenido, Densidad de Señales o schema markup produce efecto si la infraestructura técnica bloquea el acceso de los bots de IA desde el origen. Esta es la capa que se revisa **antes** de cualquier trabajo editorial: de nada sirve construir señales si la puerta técnica está cerrada. Complementa el rastreo genérico ya cubierto en [technical-seo-and-indexability.md](technical-seo-and-indexability.md) con la capa específica de bots de IA, que ese archivo no distingue.

## Estado de la evidencia

| Afirmación | Estado | Origen |
|---|---|---|
| Existen bots de IA diferenciados por función (entrenamiento vs. recuperación) con nombres de user-agent específicos | Confirmado, documentado por los propios proveedores (OpenAI, Anthropic, Google) | Documentación pública de cada proveedor |
| Bloquear un bot de entrenamiento tiene efecto retardado (meses); bloquear uno de recuperación tiene efecto inmediato | Consistente con cómo funcionan ambos mecanismos (ver distinción entrenamiento/recuperación en [ai-citation-and-geo-playbook.md](ai-citation-and-geo-playbook.md)) | Framework Los Creativos, coherente con arquitectura conocida de los sistemas |
| `llms.txt` es un estándar propuesto por Jeremy Howard en 2024 | Confirmado, es un hecho verificable de la comunidad técnica | Propuesta pública de Jeremy Howard, 2024 |
| Adopción de `llms.txt` cercana al 10% entre sitios corporativos | **Cifra sin fuente identificable** citada por el artículo como "estimaciones recientes del sector" | Los Creativos, sin cita primaria — tratar como estimación no verificada |
| Casos y cifras de bloqueo (340 intentos de GPTBot, "casi la mitad de las empresas auditadas bloquean algún bot sin saberlo") | Anécdota/caso ilustrativo y cifra de la propia cartera de clientes de Los Creativos | Los Creativos, dato interno no auditable externamente |

## Bots de entrenamiento vs. bots de recuperación

Distinción operativa central, ya alineada con "entrenamiento vs. recuperación" de `ai-citation-and-geo-playbook.md`:

**Bots de entrenamiento** (rastrean para incorporar contenido en versiones futuras de un modelo; efecto retardado, medido en meses):
- `GPTBot` (OpenAI)
- `ClaudeBot` (Anthropic)
- `Google-Extended` (Google)

**Bots de recuperación** (rastrean en vivo para construir la respuesta que alguien recibe en el momento; efecto inmediato):
- `OAI-SearchBot` (OpenAI)
- `PerplexityBot` (Perplexity)
- `ChatGPT-User` (agente de usuario cuando una persona pide a ChatGPT que visite una URL)
- `Claude-SearchBot` y `Claude-User` (Anthropic: búsqueda y agente de usuario), `Perplexity-User`, `DuckAssistBot`: nombres tomados de la lista de `seo-skills.com` (2026-10-30), por verificar en la documentación de cada proveedor. Lista completa de 22 bots en [robots-txt-audit-and-generation.md](robots-txt-audit-and-generation.md).

**Postura por tipo de negocio (criterio, no regla universal):** una empresa cuyo contenido *es* el producto (medio, proveedor de datos) puede considerar bloquear bots de entrenamiento mientras deja abiertos los de recuperación, protegiendo propiedad intelectual sin perder visibilidad conversacional. Una empresa que vende productos o servicios normalmente gana más dejando ambos grupos sin restricción, porque su objetivo es visibilidad máxima, no protección editorial.

Decisión de bloqueo/apertura: corresponde a marketing (qué bots importan para el objetivo de negocio) y a tecnología (ejecutar la configuración) en conjunto — nunca delegada por completo a un solo equipo, y nunca heredada sin revisión de una plantilla o plugin de seguridad configurado por defecto.

## Auditar y configurar robots.txt

`robots.txt` vive en `tudominio.com/robots.txt` desde 1994. Es una solicitud, no una barrera técnica absoluta — pero los rastreadores serios de OpenAI, Anthropic y Google la respetan.

**Paso 1 — Auditar la configuración actual.** Abrir `tudominio.com/robots.txt` y revisar línea por línea. Buscar directivas genéricas tipo `User-agent: *` seguidas de `Disallow: /` heredadas de plantillas o plugins de seguridad — bloquean todo tráfico automatizado sin distinguir bots de IA legítimos de scrapers maliciosos.

**Paso 2 — Definir postura explícita por tipo de bot, sin escribir grupos para los bots permitidos.** `robots.txt` solo puede denegar: "permitir" no se escribe, se omite. Un bot sin regla propia cae bajo `User-agent: *` y puede rastrear todo lo que ese grupo no bloquee. **Cuidado con el error contrario:** un bot que tiene su **propio grupo ignora por completo el grupo `*`**. Por eso un bloque como `User-agent: GPTBot` + `Allow: /` no "abre la puerta" sino que deja a ese bot sin los `Disallow` de rutas sensibles del grupo `*` (panel, área de cliente). Ejemplo de política "visibilidad máxima" (empresa que vende productos o servicios):

```text
User-agent: *
Disallow: /wp-admin/
Disallow: /area-cliente/

Sitemap: https://tudominio.com/sitemap.xml
```

Si se decide **bloquear** el entrenamiento, se añaden grupos solo para esos bots (y si alguno necesita rutas sensibles bloqueadas, se repiten dentro de su grupo):

```text
User-agent: GPTBot
User-agent: ClaudeBot
User-agent: Google-Extended
Disallow: /
```

Sintaxis, reglas de coincidencia (gana el patrón más largo; en empate, `Allow`), lista de bots y puntuación en [robots-txt-audit-and-generation.md](robots-txt-audit-and-generation.md).

**Paso 3 — Mantener rutas sensibles bloqueadas para todos los bots por igual** (paneles administrativos, áreas de cliente, contenido interno) — abrir la puerta a la IA no implica exponer lo que ninguna audiencia externa debería consultar. Ojo: robots.txt es público; la protección real de esas rutas va en el servidor.

**Paso 4 — Referenciar el sitemap dentro del mismo archivo**: `Sitemap: https://tudominio.com/sitemap.xml`. Confirmar que esa URL responde 200, no 404.

**Paso 5 — Validar tras cada cambio**: herramientas de verificación de robots.txt (Search Console y equivalentes) confirman sintaxis; revisar logs de servidor durante dos o tres semanas después del ajuste para confirmar que la actividad de los bots relevantes efectivamente cambió.

## El archivo llms.txt

Estándar propuesto por Jeremy Howard en 2024: un archivo Markdown simple en la raíz del dominio (`tudominio.com/llms.txt`) que entrega a un modelo una lista curada de las páginas más relevantes del sitio, sin que tenga que interpretar HTML completo con menús, banners y elementos decorativos. Ejemplo público: `https://loscreativos.co/llms.txt`. Vercel también publica el suyo.

Contenido básico: nombre de la empresa, descripción breve, enlaces organizados a las secciones más importantes (casos de éxito, servicios principales, contenido educativo destacado).

**No reemplaza nada, complementa:** `robots.txt` abre la puerta de acceso; `llms.txt` orienta la atención una vez adentro; el schema markup (ver [schema-markup-for-ai-citation.md](schema-markup-for-ai-citation.md)) confirma el significado exacto de cada pieza. Los tres trabajan juntos.

La cifra de adopción ("~10% de sitios corporativos") no tiene fuente primaria identificable en el artículo — tratarla como estimación de sector sin verificar, útil para argumentar oportunidad temprana pero no para citar como dato duro frente a un cliente.

## Cómo verificar que la configuración funciona en la práctica

- **Logs de servidor, revisión mensual**: filtrar por los user-agents relevantes (`GPTBot`, `ClaudeBot`, `PerplexityBot`, `OAI-SearchBot`) y confirmar si la frecuencia de visitas crece o cae mes a mes.
- **Probar desde ubicaciones distintas**, no solo desde la red de la oficina: reglas de CDN o firewall pueden variar por país de origen de la solicitud.
- **Validar el schema en cada publicación nueva** como paso obligatorio del flujo editorial, no como revisión ocasional.
- **Verificación cualitativa trimestral**: preguntar directamente a ChatGPT, Perplexity y Gemini sobre la categoría de la empresa y confirmar si la marca aparece mencionada.
- **Documentar cada hallazgo** en un reporte compartido entre marketing y tecnología (fecha, bots detectados, errores corregidos, menciones observadas) — evita que el mismo problema se repita sin que nadie recuerde cómo se resolvió antes.

Advertencia operativa: una configuración correcta hoy puede quedar obsoleta sin aviso tras un cambio de plataforma, un plugin nuevo o una actualización de seguridad no coordinada con marketing. La revisión recurrente importa tanto como la configuración inicial.

## Errores frecuentes

- Heredar `Disallow: /` genérico de una plantilla o plugin de seguridad sin revisarlo nunca.
- Escribir un grupo `Allow: /` por cada bot de IA: cada grupo propio anula las reglas de `*` para ese bot.
- Delegar la decisión de qué bots permitir exclusivamente a tecnología, sin criterio de negocio de marketing.
- Bloquear bots de IA pensando que son scrapers maliciosos sin verificar el user-agent real.
- Omitir la línea `Sitemap:` dentro de robots.txt.
- Publicar `llms.txt` una sola vez y no mantenerlo sincronizado con contenido nuevo relevante.
- Auditar la configuración una sola vez en vez de revisarla con frecuencia recurrente.
- Presentar la cifra de adopción de `llms.txt` (~10%) como dato verificado con fuente primaria.

## Lista de revisión

- ¿Se revisó robots.txt línea por línea buscando `Disallow: /` heredado?
- ¿Existe una postura explícita y documentada por tipo de bot (entrenamiento vs. recuperación), decidida junto con marketing?
- ¿Las rutas sensibles quedan bloqueadas para todos los bots por igual?
- ¿robots.txt referencia el sitemap y el sitemap responde 200?
- ¿Existe `llms.txt` publicado y actualizado con las secciones más relevantes?
- ¿Se revisan logs de servidor con frecuencia mensual filtrando por los user-agents de IA?
- ¿Se hizo la prueba cualitativa trimestral preguntando directamente a ChatGPT/Perplexity/Gemini?
- ¿Existe un reporte compartido entre marketing y tecnología con la fecha de cada revisión?

Fuente primaria: [Checklist técnico para que los motores de IA puedan rastrear tu sitio](https://loscreativos.co/blog/acciones-para-que-motores-ia-rastreen-sitio-web/) — Los Creativos, 19 de agosto de 2026. Autoría: Juan David Uribe Taquez, con citas de Fabio Araujo, David Martínez Mata y Esteban Ortiz.
