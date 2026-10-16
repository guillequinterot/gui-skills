# Ejemplos — rea-reverse-engineer

- `rea-tools/probe.md` y `probe.json`: salida real de la sonda N1 (`scripts/web_probe.py`) sobre el sitio público de REA (`rea.tools`, el proyecto upstream de esta skill), usada como prueba de la skill el 2026-10-15. Sirven de **ejemplo del formato** de la sonda.
- Las capturas de pantalla (`shot-1440.png`, `shot-390.png`) de ese sitio de terceros **no se incluyen** en el repo (regla de privacidad/derechos: no se archivan capturas de sitios ajenos). Para verlas, vuelve a correr la sonda: `python -I scripts/web_probe.py https://rea.tools/ --out <carpeta-del-proyecto>/referencias/rea-tools --widths 1440,390`.
