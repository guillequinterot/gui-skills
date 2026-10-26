---
name: contenido-sin-slop
description: Puerta de calidad contra el «slop» (contenido de baja calidad hecho con IA, en cantidad y sin revisión). Usar SIEMPRE antes de publicar o entregar contenido hecho o asistido con IA (artículos, posts, carruseles, guiones y videos, PDFs, correos, imágenes) y al revisar contenido ya hecho, también cuando otra skill (seo-content-system, direct-visual-design, video-editing-ai-agent, video-aprender) va a producirlo. Evalúa propósito, sustancia, procedencia y revisión humana, y usa un detector de síntomas solo como ayuda. Con modo revisión: semáforo 🔴🟡🟢 párrafo por párrafo (novedad, especificidad, respaldo, lo propio, función) para decir qué párrafos son slop y qué les falta. Arregla la causa (falta de algo propio que decir) y no los síntomas (palabras de moda, estructura repetida).
---

# Contenido sin slop

## Protocolo gui-skills (obligatorio)

Esta skill vive en el repo **gui-skills** y sigue [`shared/protocolo-skill.md`](../../shared/protocolo-skill.md):

1. **Paso 0 — cada vez que uses la skill:** corre `python <repo>/tools/check_update.py --quiet --pull`.
   `ACTUALIZADA n` → díselo al usuario en una línea y **vuelve a leer este `SKILL.md`** antes de seguir;
   `CAMBIOS_LOCALES` → avisa y no actualices; `SIN_RED` / `SIN_CREDENCIAL` → sigue con la copia local y dilo.
   Si avisa de aportes sin publicar, corre `python <repo>/tools/publish_job.py --reintentar` (preaprobado).
   Luego lee `HANDSHAKE.md` y el "Registro de trabajos" de `HANDOFF.md`.
2. **Privacidad:** en el repo los clientes solo se nombran con un código `caso-<tipo>-<NN>`; nunca
   nombres, marcas, dominios, correos, rutas personales ni credenciales.
3. **Paso final — obligatorio y preaprobado** (trabajo terminado y aprobado por el usuario; no pidas permiso):
   (1) `python <repo>/tools/log_job.py --skill contenido-sin-slop ...` por cada skill que intervino (qué se hizo, qué
   salió bien, qué salió mal, incidencias); (2) actualiza `HANDSHAKE.md` si cambió el estado vivo;
   (3) publica con `python <repo>/tools/publish_job.py --tema <caso-o-tema>` (rama + push + PR; si eres el
   mantenedor, tu aporte se integra solo); (4) dile al usuario el resultado (`PR_CREADO <url>` / `PUBLICADO <url>` /
   `PENDIENTE` / `BLOQUEADO`). Obsidian es opcional: si el usuario lo tiene, registra también allí.

`<repo>` = `repo_path` de `~/.gui-skills/config.json`, o dos carpetas arriba de esta skill.

## Qué es el slop (definición de trabajo)

**Slop** = contenido digital de baja calidad producido con IA, normalmente en cantidad, que nadie pidió y que
nadie revisó con criterio. Es la palabra de moda para esto (el diccionario Merriam-Webster la eligió palabra del año
2025) y se parece al *spam*: no toda promoción es spam ni todo contenido con IA es slop. **Lo que lo vuelve slop no
es la herramienta, es la combinación de falta de propósito para el lector, falta de sustancia propia y falta de
revisión humana.** Detalle y fuentes verificadas: [`references/01-que-es-slop-y-evidencia.md`](references/01-que-es-slop-y-evidencia.md).

## Principios no negociables

1. **La herramienta no es el problema; el resultado sí.** Se puede usar IA para investigar, ordenar, redactar un
   borrador o producir una pieza. Lo que se publica lleva la firma y la credibilidad de una persona que lo revisó.
2. **Arreglar la causa, no el síntoma.** Si falta algo propio que decir, cambiar sinónimos, quitar «delve» o
   mezclar la longitud de las frases no arregla nada: hay que añadir sustancia o no publicar. Los patrones de
   lenguaje son **síntomas**; ninguno prueba que algo sea IA y los humanos también los usan.
3. **Cada pieza se justifica sola.** Nada se publica porque «toca esta semana» o porque «hay que llenar el
   calendario». Calidad antes que cantidad; si no pasa la puerta, no sale.
4. **Nada inventado.** Ni casos, ni clientes, ni cifras, ni citas, ni reseñas, ni autores, ni fotos de personas
   que no existen. Cada dato verificable lleva su fuente abierta y su fecha.
5. **Transparencia proporcional.** Explicar cómo se hizo (incluida la IA) donde el lector se lo preguntaría,
   sobre todo si el contenido es en gran parte generado.
6. **Los detectores de IA no deciden.** Tienen errores; no se usa un «porcentaje de IA» para aprobar ni para
   rechazar. Se evalúa el valor para el lector.
7. **Sin ingeniería lingüística forzada.** No introducir errores para «parecer humano», no fijar densidades ni
   cuotas de palabras o conectores: es slop de otro tipo y empeora el texto.

## La puerta anti-slop (5 pasos, en este orden)

Se aplica a cualquier pieza antes de entregarla. Los pasos 1 a 3 pesan más que el 4.

### 1. Pedido y propósito

- ¿Quién lo va a leer, ver o escuchar, y qué problema suyo resuelve? ¿Lo pidió o lo buscaría?
- ¿El propósito es ayudar a esa persona o solo «tener contenido», rellenar un calendario o posicionar?
- Si el propósito principal es manipular el posicionamiento o producir volumen, **parar**: es lo que las políticas
  de Google llaman abuso de contenido a escala, con IA o sin ella.

### 2. Sustancia (lo que solo esta pieza puede aportar)

Una pieza pasa si cumple **al menos estos cinco**:

1. **Algo propio y comprobable:** una experiencia real de la persona o marca firmante (de su banco de experiencia
   aprobado, nunca inventada), un dato propio, un caso real con permiso.
2. **Datos con fuente:** cada cifra, estudio o afirmación verificable con enlace y fecha; fuentes primarias antes
   que blogs comerciales.
3. **Un ejemplo concreto** que no sirva igual en cualquier otro tema.
4. **Un criterio defendible:** una recomendación con sus límites y su «depende de…», no una lista neutra.
5. **Lo que NO cubre** y para quién no es.

Pruebas rápidas: **(a) quitar el nombre**: si la pieza la podría haber publicado cualquier otra marca sin cambiar
nada, es genérica; **(b) marcar y compartir**: ¿alguien la guardaría o se la pasaría a un colega?; **(c) reducir a la
mitad**: si se puede resumir a la mitad sin perder información, sobra la mitad; **(d) lo obvio**: si cada
afirmación ya está en los diez primeros resultados, no aporta.

### 3. Procedencia y revisión humana

- **Quién:** persona real con nombre y perfil verificable; nunca autores, fotos de perfil, reseñas o casos inventados.
- **Cómo:** qué se hizo con IA y qué con personas; qué revisó quién; en qué fecha. Divulgar cuando el contenido es
  en gran parte generado o el lector se preguntaría cómo se hizo. Anotar la revisión en el registro del trabajo.
- **Hechos verificados:** abrir cada fuente, comprobar que dice lo que se le atribuye, que el enlace responde y
  que no hay parámetros de seguimiento (`utm_*`).
- **Revisión humana real:** alguien leyó la pieza completa, cambió lo que no es suyo y asumió el resultado.

### 4. Síntomas (ayuda diagnóstica)

Correr el detector (`python <skill>/scripts/slop_lint.py <archivo> [--idioma es|en]`) y leer su reporte con
criterio. Distingue tres niveles: **restos objetivos** (marcadores de posición, frases de chatbot, `utm_source`;
siempre se corrigen), **síntomas con fuente** (patrones descritos en la guía de Wikipedia o en estudios) y
**síntomas candidatos** (observaciones aún sin fuente, sobre todo en español). Tabla de síntomas → causa → arreglo
en [`references/02-sintomas-de-texto.md`](references/02-sintomas-de-texto.md). Para revisar un contenido párrafo por párrafo, ver «Semáforo por párrafo» más abajo (`--semaforo`).

### 5. Decisión y registro

- **Publicar** si pasa 1 a 3 y no quedan restos objetivos.
- **Reescribir** (volver al paso 2) si falta sustancia: se añade lo propio, se quita lo genérico, se reduce.
- **Descartar** si no hay nada propio que decir ni fuente para decirlo: esa pieza no se publica.
- Dejar en el registro del trabajo: qué falló, qué se añadió, quién revisó, cuántas piezas se descartaron.

## Semáforo por párrafo (modo revisión)

Para **revisar un contenido ya hecho** se usa el semáforo: cada párrafo recibe 🔴 / 🟡 / 🟢 según cinco preguntas
(**P1 novedad, P2 especificidad, P3 respaldo, P4 lo propio, P5 función**) y no según cómo suena. Los criterios
salen de ocho fuentes (HubSpot, WeComm, Redactor Freelance, Salesforce, OpenArt, ImpactoTIC, BrandCrops y un video de
YouTube); la rúbrica completa, lo que se exige a cada tipo de párrafo y lo que se rechazó de las fuentes están en
[`references/06-semaforo-por-parrafo.md`](references/06-semaforo-por-parrafo.md).

| Luz | Significa | Ejemplos |
|---|---|---|
| 🔴 Rojo | Se arregla de fondo o se borra | Resto objetivo (marcador, frase de chatbot, `utm_*`); hecho que no se sostiene; ni nuevo ni propio (P1 y P2 fallan); contenido ajeno reescrito para disimularlo |
| 🟡 Amarillo | Falta algo debajo | Falla una pregunta; es correcto pero intercambiable; cifra sin fuente; síntoma de lenguaje sin sustancia que lo sostenga |
| 🟢 Verde | Pasa | Cumple las preguntas de su tipo; un síntoma aislado en un párrafo que sí aporta solo se anota |

Cómo se corre:

1. `python -I <skill>/scripts/slop_lint.py <archivo> --semaforo` → luz **provisional** por párrafo, con evidencia y qué falta.
2. Leer cada rojo y amarillo (y también los verdes) con las cinco preguntas y fijar el color **final**. El detector ve
   pistas, no novedad ni verdad.
3. Entregar el informe del §7 de la referencia: tabla párrafo → tipo → luz → pregunta que falla → qué falta, el
   semáforo del documento y la decisión (publicar / reescribir / descartar).

Qué **no** hace el semáforo: no dice si lo escribió una IA (un párrafo humano vacío sale amarillo o rojo igual), no impone
longitudes ni cuotas de palabras, y no sustituye a la puerta: el propósito, la procedencia, la promesa cumplida y la
verdad de los hechos se evalúan a mano. Los umbrales son iniciales y se ajustan con casos reales.

## Reglas por formato

| Formato | Regla clave | Detalle |
|---|---|---|
| Artículo / guía | Pasa la puerta completa; mínimo de sustancia (5 puntos del paso 2) | [`references/02-sintomas-de-texto.md`](references/02-sintomas-de-texto.md) |
| Imagen | Foto real (propia o de stock con licencia) con una razón de estar; sin personas, productos, reseñas o lugares generados que parezcan reales; crédito | [`references/03-imagen-video-redes.md`](references/03-imagen-video-redes.md) |
| Video con IA | Cada video con concepto y perspectiva propios; no plantillas repetidas; divulgar contenido sintético realista; revisar el guion y los datos | [`references/03-imagen-video-redes.md`](references/03-imagen-video-redes.md) |
| Redes / carruseles | Cada lámina aporta una idea o dato nuevo, no reciclar el mismo resumen; autoría visible | [`references/03-imagen-video-redes.md`](references/03-imagen-video-redes.md) |
| PDF / recursos | Utilidad práctica (se usa, se marca, se imprime); contenido solo del artículo o de fuentes citadas | [`references/03-imagen-video-redes.md`](references/03-imagen-video-redes.md) |

## Cuándo se llama desde otras skills

- `seo-content-system` (modos `write`, `brief`, `on-page`, `programmatic`): antes de entregar el paquete SEO.
- `direct-visual-design` y `canva-design`: antes de entregar imágenes y piezas que irán a redes o blog.
- `video-editing-ai-agent` y `video-aprender`: antes de publicar un video o un resumen hecho con IA.
- Flujos automáticos (calendarios de blog, publicación programada): la puerta es **obligatoria** antes de cada
  publicación y puede bloquearla. Cómo conectarla: [`references/04-integracion.md`](references/04-integracion.md).

## Lo que esta skill NO hace

- No certifica que un texto es humano ni calcula «porcentajes de IA».
- No reescribe por sistema para «sonar humano»: devuelve lo que falta (sustancia, fuente, revisión) y deja que la
  persona decida.
- No sustituye la revisión legal, de marca ni de hechos de un especialista cuando el tema lo exige (salud, finanzas,
  legal).

## Referencias

- [`references/01-que-es-slop-y-evidencia.md`](references/01-que-es-slop-y-evidencia.md): definición, políticas de plataformas y evidencia con nivel.
- [`references/02-sintomas-de-texto.md`](references/02-sintomas-de-texto.md): síntomas en español e inglés, causa y arreglo.
- [`references/03-imagen-video-redes.md`](references/03-imagen-video-redes.md): imagen, video, redes y PDF.
- [`references/04-integracion.md`](references/04-integracion.md): cómo conectarla con las demás skills y con un flujo de publicación.
- [`references/05-fuentes.md`](references/05-fuentes.md): fuentes con fecha de verificación y nivel de evidencia.
- [`references/06-semaforo-por-parrafo.md`](references/06-semaforo-por-parrafo.md): rúbrica del semáforo por párrafo (cinco preguntas, tipos de párrafo, reglas, informe).
- `scripts/slop_lint.py`: detector de síntomas (ayuda, no juez; con `--semaforo`, luz provisional por párrafo) y `scripts/test_slop_lint.py`: sus pruebas.
