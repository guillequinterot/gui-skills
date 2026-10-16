---
tags:
  - seo
---

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

