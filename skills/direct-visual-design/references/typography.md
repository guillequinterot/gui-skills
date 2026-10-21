# Tipografía aplicada

## Contenido

1. Ruta de decisión
2. Heurísticas de Chris Do
3. Sistema tipográfico
4. Microtipografía
5. Lectura digital y accesibilidad
6. QA

## 1. Ruta de decisión

Definir primero función, medio, idioma, duración de lectura, audiencia, personalidad, disponibilidad técnica y licencia. Distinguir tipografía funcional de tipografía expresiva. Permitir que la expresiva actúe como imagen, pero proteger la lectura del contenido esencial.

## 2. Heurísticas de Chris Do

Convertir las diez “reglas” del tutorial en puntos de partida:

| Heurística | Aplicación contextual |
|---|---|
| Alinear a la izquierda | Favorecer un inicio estable en textos latinos extensos; permitir centro, derecha o justificado cuando medio, idioma y control tipográfico lo sostengan |
| Usar una familia | Empezar con una superfamilia para controlar coherencia; combinar familias cuando roles y contraste sean claros |
| Saltar un peso | Crear contraste perceptible; comprobar que pesos finos sigan siendo legibles |
| Duplicar tamaño | Usar 2× como ejercicio rápido; elegir escala modular o contraste óptico apropiado al formato |
| Alinear a un eje | Reducir accidentes; admitir varios ejes cuando una retícula los relacione |
| Elegir fuentes probadas | Priorizar calidad, caracteres, licencia y renderizado; no limitarse a una lista histórica |
| Agrupar con filetes | Usar líneas solo si aclaran estructura; probar antes espacio, alineación o región común |
| Evitar esquinas | Respetar margen y zona segura; permitir cortes y tensión intencional |
| Cuidar espacios | Revisar kerning, tracking, leading, párrafos y espacio alrededor |
| Relajarse | Romper una base solo con intención y control |

No imponer una familia, alineación izquierda, saltos de peso ni escala 2× como leyes universales.

## 3. Sistema tipográfico

Documentar:

- familia primaria, secundaria y alternativas;
- roles: display, heading, body, label, data, caption y legal;
- escala y relación con viewport/formato;
- pesos, estilos y variables habilitadas;
- mayúsculas, numerales, signos, moneda y caracteres del idioma;
- ancho de columna y longitud de línea;
- comportamiento responsive;
- licencia y fuentes de respaldo;
- tokens o estilos reutilizables cuando aplique.

Buscar contraste de función, no solo diferencia estética. Evaluar x-height, contraste de trazo, aperturas, anchura y densidad en el tamaño real.

## 4. Microtipografía

- Ajustar kerning ópticamente en titulares y logotipos.
- Usar tracking con moderación; evitar compactar cuerpo para “hacerlo caber”.
- Ajustar leading según tamaño, ancho, x-height, idioma y densidad.
- Controlar viudas, huérfanas, ríos, guiones, particiones y líneas muy cortas.
- **Viudas en web (preferencia aprobada del usuario, 2026-10-21):** que ningún texto termine con una palabra sola en su última línea, siempre que sea posible.
  1. CSS base del sitio: `p, li, dd, dt, blockquote, figcaption, address, summary { text-wrap: pretty; }` y `h1–h4 { text-wrap: balance; }`; los textos cortos centrados (notas bajo un título, cierres, banners) también con `balance`.
  2. `pretty` no siempre resuelve párrafos de 2 líneas ni títulos de 3 palabras: para esos, espacio duro (`&nbsp;`) entre las dos últimas palabras («bone&nbsp;alignment.») o mover el `<br>` manual para repartir mejor («Years of <br>surgical experience», no «Years of surgical <br>experience»). No pegar palabras si juntas no caben en la columna (desbordaría); en palabras con guion, unir después del guion («over-the-counter&nbsp;medication» sigue pudiendo partir en los guiones).
  3. Verificar en 1440, 1024, 768 y 390 con `scripts/check_widows.js` y confirmar que las alturas de las secciones no cambian.
  4. Excepción aceptada: cuando la última palabra sola no cabe junto a la anterior en el ancho disponible (p. ej. un título de tarjeta que termina en una palabra larga). Se informa; no se fuerza.
- Usar un solo espacio tras puntuación salvo convención editorial específica.
- Alinear cifras y columnas numéricas con numerales adecuados.
- Corregir comillas, apóstrofos, guiones y signos del idioma.

## 5. Lectura digital y accesibilidad

Tratar 45-75 caracteres por línea y leading cercano a 1.4-1.6 como rangos frecuentes, no límites universales. Probar con la fuente, tamaño, dispositivo y usuarios reales.

Para web/UI:

- permitir resize y reflow;
- evitar texto esencial como imagen cuando pueda ser texto real;
- comprobar contraste según WCAG aplicable;
- no depender de pesos ultrafinos;
- considerar WCAG 1.4.12 Text Spacing;
- comprobar zoom, localización, textos largos y fuentes de respaldo.

No confundir puntos de impresión con píxeles CSS. Evaluar el tamaño visual real y las métricas de la fuente.

## 6. QA tipográfico

Revisar a tamaño final:

- lectura y jerarquía en 3 segundos;
- coherencia de estilos;
- contraste perceptible entre niveles;
- saltos y wrapping reales;
- caracteres faltantes;
- cifras, fechas, símbolos y diacríticos;
- alineaciones ópticas;
- ríos, viudas y huérfanas;
- responsive y localización;
- licencia y empaquetado/exportación.

