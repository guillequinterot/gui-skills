---
title: Preferencias generales aprobadas
scope: global
status: approved
updated: 2026-10-09
---

# Preferencias generales aprobadas

La instrucción actual del usuario y el brief del proyecto siempre tienen prioridad sobre esta lista.

## Heredadas (copiadas el 2026-10-09 desde el vault privado del mantenedor, sin cambios)

Fuente original: nota "Preferencias generales aprobadas" del vault de Obsidian del mantenedor (actualizada 2026-07-22). Esta lista es su copia en el repo.

- Entregar primero el resultado o recomendación y después la justificación necesaria.
- Mantener alta definición, realismo físico, materiales creíbles y acabado profesional.
- Preservar rostros, gestos, productos, etiquetas, textos y elementos declarados intocables.
- Reservar espacio negativo útil cuando la imagen será base para añadir texto.
- Mantener protagonistas en la zona solicitada y controlar el fondo.
- Crear imágenes base sin logos ni textos nuevos cuando el diseño final se añadirá después.
- Respetar dimensiones y relación de aspecto; adaptar por composición.
- Corregir solo lo pedido y evitar cambios colaterales.
- Diferenciar fotografía editorial realista de pieza gráfica terminada.
- Trabajar habitualmente en español y producir copy en inglés cuando la marca o campaña lo requiera.
- No inventar una marca nueva cuando existen logo, redes o website; basar decisiones en activos entregados.
- Si falta información, proponer una solución razonable y señalar qué validar después.

## Nueva — Método de entrega HTML → Figma (aprobada 2026-10-09)

Evidencia: aprobación explícita del usuario en conversación ("estas son reglas de mi método, generales").

- Primero HTML, aprobación del usuario, luego Figma.
- 1920 px de ancho, alto Hug; contenido con 240 px de padding lateral.
- 80 px de padding superior e inferior en cada sección.
- Paddings, gaps y margins en múltiplos de 4 (8, 16, 24, 32, 40, 80, 120).
- Secciones como Auto Layout width Fill / height Hug.
- Evitar clip content / overflow hidden salvo carruseles o necesidad real.
- Colores, tipografías y demás desde los Styles/Variables del Figma del proyecto; preguntar siempre antes de inventar uno.
- En Figma: aplicar/anidar estilos existentes como primarios y crear solo los que falten.
- Reutilizar como componente el header/menú y demás componentes existentes; el HTML los replica fielmente.
- Exportar imágenes desde Figma cuando se necesiten y colocarlas en Figma al construir.

Detalle: `../conocimiento/01-reglas-metodo-html-figma.md`.

Precisión aprobada el mismo día: el padding de 80/80 aplica a las **secciones de contenido**; el **menú/header y el footer quedan exentos** del 80/80 (el hero también, según la instrucción de ajuste del validador; confirmar), pero todo su espaciado sigue siendo múltiplo de 4.

## Nuevas — aprendizajes de los ejemplos (aprobado explícitamente por el usuario, 2026-10-09)

Antes estaban como candidatos en `inbox-aprendizajes.md`; el usuario los aprobó como regla general.

- Separar con `gap`/`padding` del contenedor padre, no con `margin` entre hijos (Figma Auto Layout no tiene margins).
- Tipografía y line-height en px enteros; sin rem fraccionarios.
- Resetear el padding por defecto de `button` (el navegador añade 1 px / 6 px).
- Un solo acento de color usado con disciplina; sin sombras: profundidad por color de superficie + borde de 1 px.
- Secuencia de landing: hero → prueba cuantitativa → diferenciador → prueba cualitativa → caminos/CTA → contenido → FAQ → cierre.
- Escala corta de radios (máximo 6 valores).
- Revelado al entrar en viewport: fade + translateY 16–24 px, ~400 ms, ease-out, escalonado; siempre con `prefers-reduced-motion`.

## Límites

Una guía de marca o una instrucción actual distinta prevalece. Valores concretos de marca → `../proyectos/`.
