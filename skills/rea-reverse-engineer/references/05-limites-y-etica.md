# 05 · Límites, legalidad y privacidad

Esta skill sirve para **entender**. Las reglas siguientes aplican a todo nivel (N0–N3) y a todo consumidor.

## Alcance legítimo
- Referencias **públicas** (lo que ve cualquier visitante) o software **propio / autorizado** por su dueño.
- Fines: aprendizaje, benchmarking, interoperabilidad, preservación, análisis de lo que el usuario posee o está autorizado a examinar (así lo limita también el `DISCLAIMER.md` de REA).
- Lo entendido se usa para **diseñar y construir algo propio**: estructura, principios, patrones, medidas aproximadas, comportamiento.

## Nunca
1. **Copiar** código, textos, imágenes, iconos, fuentes con licencia, marca ni contenido de terceros a un proyecto, aunque técnicamente se pueda extraer (`rendered.html`, scripts exportados, assets de red).
2. **Saltar** autenticación, muros de pago, CAPTCHA, límites de uso o bloqueos de bot; ni usar credenciales ajenas.
3. **Rastrear masivamente** ni sobrecargar un sitio: una página por llamada, con pausa; para un sitio completo existe `screaming-frog-seo` sobre sitios propios o autorizados.
4. Analizar **sesiones con datos personales** de terceros, ni conservar datos sensibles en fichas (cookies, tokens, correos, cabeceras de autenticación).
5. Descompilar o modificar software **comercial protegido** para eludir licencias o producir un clon. REA no concede licencias de IDA/Hopper/JEB; el usuario debe tenerlas legalmente.
6. Presentar una **inferencia** como hecho, o decir que algo «se ejecuta» cuando solo se vio en código estático.
7. Instalar REA, motores (Ghidra, JADX, Chrome headless-shell…) o registrar MCP **sin aprobación** del usuario.

## Privacidad
- Los resultados de REA y de la sonda **llegan al modelo**: aplica la política de datos del proveedor del modelo. No pasar por ellos nada que el usuario no pueda compartir con él.
- Fichas y capturas viven en la carpeta del proyecto; nunca en una carpeta compartida suelta ni subidas a servicios externos sin autorización.
- Las capturas de REA omiten valores de cabeceras de credenciales y cuerpos privados; aun así, revisar antes de archivar.

## Cuando hay duda
Si la referencia tiene términos de uso restrictivos visibles, o el objetivo parece clonar, **señalarlo al usuario** y proponer la alternativa: entender el principio y diseñar propio. No emitir veredictos legales.

## Reglas de las skills que llaman (siguen vigentes)
- `direct-visual-design`: referencias → mantener / adaptar / evitar; texto del cliente literal.
- `seo-content-system`: no inventar datos de herramientas no conectadas; aprendizajes a `Inbox`, no a regla.
- `video-editing-ai-agent`: autorización permanente de `yt-dlp` con sus protecciones; sin skills de terceros en `~/.claude`.
