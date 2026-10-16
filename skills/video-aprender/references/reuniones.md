# Reuniones grabadas: de la grabación a cambios concretos

Una reunión es **confidencial y ambigua por naturaleza**: la gente dice "sí, más o menos", interrumpe y se corrige. El objetivo no es resumir bonito sino **no inventar ningún acuerdo** y dejar cada cambio trazable a una frase.

## Antes de empezar
- **Todo en local.** La transcripción usa Whisper local; **no** se sube audio ni video a ningún servicio (ni `video_analyze` ni `media_summarize` ni nada parecido) sin permiso explícito del usuario.
- Los archivos quedan en la carpeta del proyecto (`<proyecto>/referencias/reunion-<fecha>/`), no en carpetas compartidas ni dentro de la skill.
- Pregunta (una vez) qué se quiere sacar: ¿cambios a ejecutar?, ¿acuerdos para confirmar por escrito?, ¿pendientes?, ¿un resumen para otra persona?
- Una reunión de 1 h tarda ~1 h en transcribirse (modelo `small`): avisa, corre **en segundo plano** y ofrece `--rapido` o empezar por un tramo con `--section`.

## Lectura
1. `video_aprender.py GRABACION --modo reunion --goal "…" [--lang es] [--sin-pantalla]` (`--sin-pantalla` si es solo cámara de personas; si hubo pantalla compartida, déjalo: captura cada diapositiva o documento mostrado).
2. Lee `contenido.md` **entero y en orden**. Si hubo pantalla compartida, lee cada imagen y relaciónala con lo que se decía en ese momento (un precio en una tabla + "ese es el plan" es una decisión; la tabla sola, no).
3. Completa `analisis.md` (plantilla de reunión) sección por sección.

## Qué extraer y cómo citarlo
| Qué | Regla |
|---|---|
| **Decisión** | Algo que se acordó explícitamente (alguien propone y otro acepta, o se dice "entonces hacemos X"). Cita: `[mm:ss] "frase corta"`. Una opinión o una idea suelta **no** es decisión |
| **Cambio solicitado** | Lo que el cliente pidió modificar, con sus palabras exactas y el minuto. Si pidió algo vago ("que se vea más moderno"), anótalo como pedido **ambiguo** y propone la pregunta que lo aclara |
| **Compromiso / pendiente** | Qué, **responsable y fecha solo si se dijeron**. Si nadie se comprometió, no inventes un responsable |
| **Cifras, precios, plazos, nombres** | Contrástalas con la imagen (si se mostró algo) y márcalas para que el usuario las confirme: Whisper confunde números y nombres propios |
| **Riesgos y objeciones** | Lo que el cliente dudó, con cita |

## Lo que NO se puede hacer
- **No sé quién habla** (no hay diarización). Si el usuario necesita atribución, que la confirme o aporte los nombres y el orden; no la deduzco por el contenido.
- El **tono, la duda, el silencio incómodo, el humor** no se pueden verificar con texto.
- Lo dicho **fuera de cámara o sin audio** no existe para el análisis.
- Un acuerdo "implícito" no se convierte en decisión: se pregunta.

## De la reunión a la ejecución
1. **Plan de ejecución** (`analisis.md` §8): cada acción apunta al **cambio solicitado** que la origina (número de la sección 3), con riesgo y reversibilidad.
2. **Confirmación del usuario** acción por acción o en bloque. Sin confirmación no se ejecuta nada.
3. **Ejecutar con las puertas normales:** copia de respaldo antes de tocar archivos; proyectos de diseño, video o web con el flujo de su skill (`direct-visual-design`, `video-editing-ai-agent`, etc.); **enviar correos o mensajes, crear o mover tareas, invitar a alguien, publicar o editar un documento compartido exige permiso explícito** aparte.
4. **Registrar** en `video-handoff.md` del proyecto (y en la nota de Obsidian si el usuario la usa): qué se pidió (con minuto), qué se hizo, qué quedó pendiente y qué se dejó sin aclarar. Si aún no existe el proyecto, en una carpeta temporal con una nota candidata. El caso se nombra solo con código (`caso-<tipo>-<NN>`) en el repo.
5. Al entregar, **mapea cada cambio ejecutado a su cita** de la reunión para que el usuario pueda mostrárselo al cliente.
