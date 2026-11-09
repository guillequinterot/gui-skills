# STYLE.md — el estilo de la pieza escrito como números (de charlie947/motion-graphics-skills, MIT, y awesomeclaude)

> Un archivo por proyecto. Se lee completo antes de diseñar o animar; **todo valor sale de aquí**. Donde no se sepa algo se escribe `ASK ME`
> y se pregunta (una vez, junto con lo demás); **nunca se rellena con una suposición**. Los hex tecleados por el usuario ganan a los muestreados
> de un JPEG. «El archivo fija el aspecto, no la ambición»: si el usuario pide ir a por todas, se va a por todas dentro de este aspecto.
> Al terminar, comparar la hoja de contacto de la pieza contra este archivo y corregir antes de mostrar.

**Marca** (< 300 palabras, solo hechos): qué hace · audiencia en una frase · qué se promociona (con enlace real) · la sensación en el primer segundo (hasta 3: calmada, premium, juguetona, urgente, técnica, cálida, audaz) · activos (hex, fuentes, archivos de logo reales; jamás redibujados de memoria) · **una cosa que el movimiento nunca debe hacer**.

## 1. Medio y referencia
Una cláusula (p. ej. «dos tintas planas sobre papel cálido»). Referencias por nombre real, no adjetivos. Máx. 3–5 fotogramas de referencia: si dan looks distintos, **elegir un look maestro** o mapear look → tipo de pieza.

## 2. Color (con rol)
| Rol | Hex | Origen | % de superficie |
|---|---|---|---|
| fondo | | marca / producto / inventado | |
| superficie | | | ~20 % |
| tinta | | | |
| tinta secundaria | | | |
| acento (UN significado) | | | pocos % |
| inundación (opcional, 1–2 veces) | | | |
Qué elemento lleva el color de señal en cada plano: ______ . Texto pequeño ≥ 4.5:1 (gancho y llamada a la acción 7:1). Valor primero: ¿el sujeto se lee en gris?

## 3. Tipografía
Fuentes (solo pesos que existen) · tamaños a 1080 px (gancho ≥ 84, llamada a la acción y términos ≥ 48, etiquetas ≥ 34, nada legible bajo 24) · cómo llegan las palabras · ≤ 5 palabras en pantalla.

## 4. Tiempo
Entradas 0.5–0.9 s · salidas 0.25–0.4 s · escalonado UI 30–60 ms / letras 15–25 ms · hold ≥ 1.2 s en el estado final · algo pequeño siempre vivo en el hold · fps elegido a propósito (12 a dos para imprenta/dibujo, 24 cine, 60 UI limpia) · reloj de la pieza (cuándo se mueve, cuándo se mantiene, cuándo vuelve).

## 5. Movimiento
Curva de easing como `cubic-bezier(...)` concreto por rol (entrada, salida, entre estados) · cómo se conectan los planos (y qué se descarta: fundidos) · acciones de cámara permitidas (tabla de `motion-recetas-y-camara.md` §1) · textura y acabado con parámetros medibles (desplazamientos en px, grano %, viñeta).

## 6. Nunca (5, con nombre)
1. ______ 2. ______ 3. ______ 4. ______ 5. ______
Por defecto prohibidos: ráfagas de partículas, lens flare, neón/brillo, RGB split, glitch, rebote en todo, degradados decorativos, texto que repite lo que enseña la imagen, azul-violeta, texto tipo máquina de escribir (salvo dentro de una caja de entrada real).

## 7. Un ejemplo descrito plano a plano hecho bien
(2–4 líneas del plano de referencia: qué se ve, cuánto dura, cómo entra y cómo sale.)
