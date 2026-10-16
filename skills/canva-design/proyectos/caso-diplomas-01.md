# caso-diplomas-01 — ficha para Canva

Empresa de materiales para arte y manualidades (marca con décadas de trayectoria). Proyecto: diplomas para el personal. Carpeta del proyecto y nota de Obsidian: en la PC del usuario, fuera del repo.

## Tokens
| Token | Valor | Uso |
|---|---|---|
| Rojo marca | `#DA111C` (C6 M99 Y94 K1) | Primario |
| Negro | `#000000` | Primario |
| Tinta de texto | `#1A1A1A` | Cuerpo (negro suavizado) |
| **Paleta tonal aprobada (2026-10-08)** | vino `#4E0814` · profundo `#8E0F1B` · marca `#DA111C` · vivo `#F2343B` · coral `#FF6B5E` (solo sobre oscuro) | Fondos y textos (idea de una colega del cliente) |
| Soporte del manual (NO usar en piezas de personal) | azul `#2D58FF`, amarillo `#F2E74B`, verde `#428C47` | Líneas de producto |
| Tipografía principal | Montserrat (Light/Regular/Bold/ExtraBold) | Nativa de Canva |
| Serif secundaria | serif propia de la marca (no existe en Canva) → **Playfair Display** (la que ya usan sus posts) | Avisar al usuario |

## Logo
- Origen: el `.ai` del logo de la marca (4 artboards; PDF-compatible). Artboard 0 = plano (fondos claros); artboard 3 = contorno blanco (fondos oscuros o rojos). Extraer con `bake_assets.py logo --src <archivo.ai> --page N`.
- Respetar el manual de marca: no rotar/deformar; área de reserva; versión pequeña (isotipo).

## Assets que se subieron a Canva
Logo plano (SVG), logo contorno blanco (SVG), fondo lienzo (1920×1080 y 2000×1400), fondo negro con luz, fondo vino, trazos rojos sup-der / inf-izq (v1), panel rojo con borde de pincel, pincelada roja tonal, mármol rojo y triángulos rojos tonales. Los ids de asset de Canva dependen de la cuenta: no se guardan en el repo; se reutilizan desde la nota de proyecto del usuario o se vuelven a subir (hechos con `bake_assets.py`, ver `references/05`).

## Lenguaje gráfico (de manual, premios, brochure, calendario, Canva, web e IG)
Blanco limpio + rojo protagonista; trazos de pincel rojos diagonales; manchas de pincel con borde deshilachado como etiqueta de titular; tarjetas redondeadas; titulares en mayúsculas ExtraBold con una palabra clave en rojo/cursiva; lockup "NN AÑOS" de la placa de premios; tono cálido, con metáforas de pintura ("trazo a trazo", "lienzo", "huella").

## Stock usado (Magnific)
Textura de tela blanca `1273386` (→ lienzo) · pintura fluida roja `15644183` (→ mármol; el original de 38 MB no está en la skill: re-descargar) · descartada `4321575` (rosa/vino mate).

## Diseños en Canva
- v1 1920×1080 (A/B/C) y v2 20×14 cm (D/E/F): dos diseños en la cuenta del usuario; un diseño intermedio de la importación v1 quedó en la cuenta. Enlaces e ids: en la nota de proyecto del usuario (fuera del repo).
- Referencias de estilo que aportó el usuario: cuatro diseños de Canva de la propia marca (posts de producto, un encuentro de manualistas, una nota de tendencia de color y una pieza educativa).

## Decisiones aprobadas (por el usuario o su equipo)
- Formato diploma físico **20×14 cm** (marco). Una sola firma: **Director Gerente**. Logo **arriba**.
- Opciones D/E/F presentadas; elección pendiente.
- Texto del cliente literal; "11 años" (título) vs "8 años" (cuerpo) **sin resolver**.

## Pendientes
Elegir D/E/F · nombre del Director Gerente · 11 vs 8 · fecha · versión para otro país · decidir si el resto del personal se produce duplicando la página (cambiar nombre y años).
