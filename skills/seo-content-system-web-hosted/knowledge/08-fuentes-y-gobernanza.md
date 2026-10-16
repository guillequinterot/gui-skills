<!-- GENERADO por tools/build_hosted.py desde skills/seo-content-system (v1.2.0, huella c95f028e2cd0). NO EDITAR A MANO: cambia la skill o hosted-src/ y regenera con `python tools/build_hosted.py`. -->

# Fuentes, evidencia y gobernanza de actualizaciones

Cómo verificar y jerarquizar fuentes, el registro oficial de referencias, y cómo promover un aprendizaje de candidato a regla estable.

---

## Fuente original: `source-verification-and-evidence.md`

# Verificación de fuentes y evidencia

## Índice

- Jerarquía
- Registro
- Verificación
- Citas
- Temas sensibles
- Caducidad

## Jerarquía

1. Documentación oficial y fuentes primarias.
2. Investigación académica original.
3. Organizaciones profesionales reconocidas.
4. Medios y análisis especializados.
5. Proveedores y blogs comerciales.
6. Comunidades y anécdotas.
7. Síntesis internas.

Una síntesis interna organiza conocimiento; no prueba sus propias conclusiones.

## Registro

| Campo | Contenido |
|---|---|
| Afirmación | Texto verificable |
| Fuente | URL o documento |
| Autor/organización | Responsable |
| Publicación/actualización | Fecha |
| Consulta | Fecha |
| Tipo | Primaria, académica, etc. |
| Alcance | País, muestra, producto |
| Limitaciones | Sesgos o condiciones |
| Estado | Pendiente, verificada, descartada |
| Próxima revisión | Fecha |

## Verificación

- Abrir la fuente completa.
- Confirmar que respalda la afirmación exacta.
- Revisar fecha y versión.
- Preferir la fuente original.
- Contrastar cifras importantes.
- Diferenciar correlación y causalidad.
- Conservar contexto y limitaciones.

## Citas

Parafrasear con fidelidad. No atribuir declaraciones que la fuente no hace. No usar una cita solo para aumentar “densidad factual”.

## Temas sensibles

Aplicar controles adicionales en salud, finanzas, legal, seguridad y políticas públicas. No extrapolar estudios a poblaciones distintas sin advertencia.

## Caducidad

Asignar frecuencia:

- Alta: plataformas, algoritmos, leyes, precios, interfaces.
- Media: benchmarks, estudios y herramientas.
- Baja: fundamentos lingüísticos o conceptuales.

Un contenido antiguo no es automáticamente incorrecto; una fuente reciente no es automáticamente mejor.

---

## Fuente original: `official-source-register.md`

# Registro de fuentes oficiales

## Índice

- Google Search
- Medición
- Datos estructurados y web
- Lenguaje y accesibilidad
- Plataformas de skills
- Política de uso

## Google Search

- Search Essentials: https://developers.google.com/search/docs/essentials
- SEO Starter Guide: https://developers.google.com/search/docs/fundamentals/seo-starter-guide
- Helpful content: https://developers.google.com/search/docs/fundamentals/creating-helpful-content
- AI features: https://developers.google.com/search/docs/appearance/ai-features
- Title links: https://developers.google.com/search/docs/appearance/title-link
- Snippets: https://developers.google.com/search/docs/appearance/snippet
- Image SEO: https://developers.google.com/search/docs/appearance/google-images
- Crawlable links: https://developers.google.com/search/docs/crawling-indexing/links-crawlable
- Structured data policies: https://developers.google.com/search/docs/appearance/structured-data/sd-policies
- Spam policies: https://developers.google.com/search/docs/essentials/spam-policies
- Search Central Blog: https://developers.google.com/search/blog
- Search Status Dashboard: https://status.search.google.com/
- Search Console: https://search.google.com/search-console/about
- Business Profile ranking: https://support.google.com/business/answer/7091

## Medición

- Google Analytics: https://support.google.com/analytics/
- Search Console API: https://developers.google.com/webmaster-tools
- Microsoft Clarity: https://learn.microsoft.com/clarity/
- Google Trends: https://trends.google.com/trends/

## Datos estructurados y web

- Schema.org: https://schema.org/
- Schema.org releases: https://github.com/schemaorg/schemaorg/releases
- Web.dev: https://web.dev/
- W3C Web Accessibility Initiative: https://www.w3.org/WAI/
- WCAG: https://www.w3.org/WAI/standards-guidelines/wcag/

## Lenguaje y accesibilidad

- RAE: https://www.rae.es/
- FundéuRAE: https://www.fundeu.es/
- WAI alt decision tree: https://www.w3.org/WAI/tutorials/images/decision-tree/

## Plataformas de skills

- Codex skills: https://developers.openai.com/codex/build-skills
- Claude Code skills: https://code.claude.com/docs/en/skills
- Antigravity skills: https://codelabs.developers.google.com/antigravity/how-to-create-agent-skills-for-antigravity-cli

## Política de uso

- Registrar fecha de consulta.
- Leer la página completa antes de citar.
- Revisar enlaces al menos trimestralmente.
- No interpretar una función de interfaz como factor de ranking.
- No usar una fuente secundaria para contradecir documentación oficial sin evidencia.

---

## Fuente original: `update-governance-and-research.md`

# Gobernanza de actualizaciones e investigación periódica

## Índice

- Objetivo
- Tres niveles
- Flujo de investigación
- Criterios de promoción
- Conflictos
- Cadencia
- Seguridad

## Objetivo

Permitir que el sistema aprenda sin reescribir reglas estables a partir de una sesión aislada, una opinión o una noticia no verificada.

## Tres niveles

### 1. Observación

Hallazgo de un proyecto:

- Contexto.
- Acción.
- Resultado.
- Evidencia.
- Limitaciones.
- Fecha.

Estado: `candidate`.

### 2. Hipótesis validable

La observación se repite, coincide con datos o tiene respaldo independiente.

Estado: `testing`.

### 3. Regla estable

Existe evidencia suficiente, se define el alcance y se aprueba el cambio.

Estado: `promoted`.

No sobrescribir una regla sin guardar la decisión y la versión anterior.

## Flujo de investigación

```text
Recopilar cambios
→ deduplicar
→ leer fuente completa
→ clasificar autoridad
→ identificar afirmación
→ contrastar
→ evaluar impacto
→ probar
→ promover o descartar
```

`research_update.py` recopila y compara fuentes; no valida por sí solo el significado del cambio.

## Criterios de promoción

Promover cuando:

- La fuente es oficial o primaria, o existe contraste sólido.
- La recomendación tiene alcance definido.
- No contradice evidencia superior sin explicación.
- Puede convertirse en una acción verificable.
- Se documentan riesgos y excepciones.
- La fecha de revisión está asignada.

## Conflictos

Si dos fuentes discrepan:

1. Priorizar la más cercana al sistema evaluado.
2. Revisar fechas y versiones.
3. Distinguir política, documentación, experimento y opinión.
4. Registrar ambos puntos.
5. Mantener la regla anterior si no existe evidencia suficiente.

## Cadencia

- Semanal: recopilar novedades de alta volatilidad.
- Mensual: revisar Search Central, Search Console, GA4, schema y plataformas clave.
- Trimestral: auditar reglas estables y enlaces de fuentes.
- Por evento: revisar tras core update, spam update o cambio de producto.

La frecuencia se configura; no debe implicar modificación automática de producción.

## Seguridad

- No guardar tokens, cookies, contraseñas ni datos personales.
- No ejecutar código descargado desde fuentes.
- Limitar tamaño y tiempo de descargas.
- Registrar errores sin volcar secretos.
- Mantener la investigación en modo lectura.
