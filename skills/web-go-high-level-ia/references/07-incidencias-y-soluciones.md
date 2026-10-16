# 07 · Incidencias y soluciones (registro vivo)

Formato: **síntoma → causa → solución → prevención**. Añadir al final cada incidencia nueva con fecha y proyecto.

## A. Plataforma y límites
| # | Síntoma | Causa | Solución / prevención |
|---|---|---|---|
| A1 | La API de GHL no crea páginas | Solo expone CRM/medios, no el sitio | Plan B: HTML + kit + «partes» para el constructor |
| A2 | No se puede pegar el diseño completo | Chat: ≤ 50 000 caracteres y solo imágenes (≤ 5) | Sistema de partes contiguas verificadas ([02](02-partes-para-el-constructor.md)) |
| A3 | No se pueden re-subir archivos al proyecto | El constructor solo deja editar | Editar en local → pegar por portapapeles en el editor ([04](04-transferencia-editor-portapapeles.md)) |
| A4 | El código del editor no se lee con herramientas | Editor en iframe de otro origen | «Descargar base de código» y leer en local |
| A5 | Claude in Chrome no controla Arc | Solo funciona en Chrome | Usar Chrome; `tabs_context_mcp {createIfEmpty:true}` para crear el grupo de pestañas |
| A6 | Pestañas en segundo plano pausan animaciones/captura | rAF pausado | Probar en primer plano; capturas con reintento |

## B. Estilos
| # | Síntoma | Causa | Solución / prevención |
|---|---|---|---|
| B1 | Todo el contenido pegado a la izquierda en la vista previa | `.container` de Tailwind (`max-width` + `margin`) pisa el `.container` del kit | `.container { padding-inline: var(--gutter); max-width: none; width: 100%; margin-inline: 0; }` |
| B2 | Clases propias que «no hacen nada» | Nombre igual a utilidad de Tailwind (`hidden`, `block`, `flex`, `grid`, `fixed`, `relative`) | Nombres propios únicos; documentado en `AGENTS.md` §3 |
| B3 | Páginas provisionales con estilo distinto al de marca | La IA usó Tailwind con colores hexadecimales | Reescribir con clases del kit; prohibirlo en `AGENTS.md` |

## C. Código generado por la IA
| # | Síntoma | Causa | Solución / prevención |
|---|---|---|---|
| C1 | `AGENTS.md` casi vacío | El constructor solo pone el bloque VIBE | Escribirlo completo ([03](03-agents-md-y-readme-vivos.md)) |
| C2 | Imágenes rotas en rutas anidadas | Rutas relativas `imagenes/x.jpg` | `img()` con base única + `IMG_URLS` |
| C3 | Metadatos con afirmaciones inventadas | La IA rellenó `__root.tsx` por su cuenta | Reescribir neutro; regla «no inventar» en `AGENTS.md` |
| C4 | Formulario duplicado con campos/IDs inventados (`LeadForm.tsx`) | Plantilla de la IA | Reexportar el formulario aprobado; prohibir otro formulario |
| C5 | 404/error en inglés | Plantilla por defecto | Componentes en español con clases del kit |
| C6 | Shell repetido en cada página; páginas provisionales sin header/footer | Cada ruta compone su propio layout | Shell en `__root.tsx` (`<main id="contenido"><Outlet/></main>`) |
| C7 | `data-track` no mide nada | Atributos sin listener (el listener estaba en el JS del kit original) | `initTracking()` global en `__root.tsx` |
| C8 | Carrusel falla si no hay referencia | `if (!track) return track.clientWidth…` | Devolver 0 |
| C9 | `aria-expanded` fijo en el botón del menú | Port literal | Ligarlo al estado del drawer |
| C10 | Enlaces internos recargan la página | `<a href>` | `<Link>`; para rutas inexistentes aún, `<a>` con comentario |
| C11 | La IA pide «sube tú los archivos a `public/imagenes/`» | No ve Medios | Darle las URL («Insertar enlaces») ([05](05-imagenes-medios-cdn.md)) |

## D. Medios / CDN
| # | Síntoma | Causa | Solución / prevención |
|---|---|---|---|
| D1 | La URL no contiene el nombre del archivo | **El CDN renombra al subir y no se puede cambiar** | Mapa en `IMG_URLS`; emparejar por SHA-256 con `match_cdn.py` |
| D2 | La IA recibe URL sin nombres | «Insertar enlaces» pega solo URL | Manifiesto + emparejar por contenido; contrastar |
| D3 | Archivos sueltos de pruebas en Medios | Subidas previas | No seleccionarlos |

## E. Editor del constructor
| # | Síntoma | Causa | Solución / prevención |
|---|---|---|---|
| E1 | «Reemplazar» del editor no aplica | Función del panel | Pegar el archivo completo por portapapeles |
| E2 | Ctrl+S escribe una «s» | No guarda; inserta texto | Botón «Guardar»; `Escape` + `BackSpace` si pasó |
| E3 | Tras «Guardar» la vista cambia y el botón es «Publicar» | Reconstrucción → vista previa | Captura antes de cada clic; no pulsar «Publicar» sin pedido |
| E4 | Se pegó el archivo en la pestaña equivocada | La búsqueda no abrió el archivo esperado | Verificar pestaña + primera línea; `ctrl+z` |
| E5 | Se pegó una URL dentro de un archivo | El constructor abrió pestaña `vibepreview` y pisó el portapapeles | Re-copiar antes de pegar; verificar primera línea; re-pegar el correcto |
| E6 | «Compilación fallida» en el chat | Un archivo quedó mal | Re-pegar; la siguiente compilación reemplaza la tarjeta |
| E7 | Pestañas `vibepreview`/«Untitled» aparecen solas | El constructor las abre | Cerrarlas con `tabs_close_mcp` |
| E8 | `navigate` al proyecto tarda ~20 s | App pesada | No recargar; esperar |
| E9 | Se pega una **ruta de archivo de Windows** (o una URL) en lugar del código | El usuario trabaja a la vez y copia otra cosa: el portapapeles es compartido (pasó 2 veces) | **Pegar y verificar la primera línea en una llamada y guardar en otra** (nunca pegar+guardar en la misma); re-copiar justo antes de pegar. Si ya se guardó: re-pegar el archivo correcto (la compilación fallida se reemplaza) |
| E10 | Aparece el diálogo «Cambios no guardados… ¿Abandonar?» | Se pulsó `</>` cuando el editor ya estaba en código con cambios sin guardar | Pulsar **Cancelar** (no Abandonar) y guardar. Antes de pulsar `</>` confirmar con captura en qué vista se está; las capturas pueden ir un paso atrás |
| E11 | Los clics caen en la vista previa (pegado «perdido») | Tras «Guardar» la vista cambia a Vista previa **con retraso variable** (a veces 10+ s) | Tras guardar, esperar y verificar con captura; si los clics cayeron en la vista previa no pasa nada, pero repetir |
| E12 | La vista previa pública lleva `<meta name="robots" content="noindex">` aunque la ruta no lo declare | El host `vibepreview.app` lo inyecta en todas las rutas | No es del código; al publicar con dominio propio desaparece. Para comprobar `noindex` propio, mirar el código de la ruta, no el HTML de la vista previa |
| E13 | Leer el contenido actual de un archivo del constructor | El editor es un iframe de otro origen | `ctrl+A`, `ctrl+C` en el editor y leer el portapapeles con PowerShell (`Get-Clipboard -Raw`); comparar la longitud con la versión conocida para saber si la IA lo tocó |

## F. Entorno local
| # | Síntoma | Causa | Solución / prevención |
|---|---|---|---|
| F1 | `tsc` marca errores de rutas (`"/" \| "." \| ".."`) | `routeTree.gen.ts` desactualizado en la descarga | Ignorarlos; lo regenera el constructor |
| F2 | `tsc` marca `TS4111`, `exactOptionalPropertyTypes` | Flags estrictos | Tipar los registros (`Partial<Record<…>>`), `| undefined`, acceso con corchetes |
| F3 | `npm install` con `TAR_ENTRY_ERROR` | Antivirus/archivos en Windows | Funciona igual (~5 min); hacerlo en copia aparte |
| F4 | Vite elige otro puerto | Puerto ocupado | Leer el log; usar el que diga |
| F5 | Python por heredoc de bash rompe `\` | Escapes | Escribir el script con la herramienta de archivos |
| F6 | Capturas vacías del panel integrado | Ventana oculta | Edge headless (`shot.sh`) |
| F7 | Edge headless no baja de ~500 px de ancho | Ancho mínimo | Marco `iframe` a 390 |
| F8 | `msedge.exe --headless` no genera la captura (ni con `about:blank`) | El usuario tiene Edge abierto (49 procesos) y el modo headless se enlaza a esa instancia | **Chrome headless con perfil propio:** `chrome.exe --headless=new --user-data-dir=<carpeta> --screenshot=… <url>` (`scripts/cshot.sh`). Móvil: marco `iframe` de 390 px en una ventana de 500 (2026-10-13, `caso-web-universidad-01`) |
| F9 | Los heredoc de bash con comillas/backticks fallan («unexpected EOF») y no aplican nada | Parseo del shell con texto largo | Escribir el script/archivo con la herramienta de archivos y ejecutarlo; comprobar siempre que el cambio se aplicó (2026-10-13) |
| F10 | `python -I install.py` de otra skill falla con `No module named 'paths'` | `-I` bloquea imports del directorio del script | Para scripts propios con imports locales, ejecutar sin `-I` (solo usar `-I` con archivos descargados no confiables) |

## H. Rondas de QA sobre una página ya construida (2026-10-13, caso-web-universidad-01 «qa-home-1»)
- Patrón: esquema de secciones del cliente vs página → tabla «existía / nueva» → cambios en el HTML fuente **y** en el código del constructor → carpeta `qa-<pagina>-<n>/` con `B-REFERENCIA` (capturas), `C-COPIAR-Y-PEGAR` (partes ≤ 50 000: «REEMPLAZA el archivo / AÑADE AL FINAL / BUSCA y REEMPLAZA») y `CAMBIOS-*.md`. Generador: `scripts/make_partes.py` (modos «reemplazar», «anexar», «buscar»).
- **No pisar archivos que la IA esté editando** (p. ej. `<p>-data.ts` con `IMG_URLS`): los datos nuevos van «AÑADIDOS AL FINAL», no como archivo completo.
- Datos largos (FAQ, calendarios) en un JSON fuente único (`datos/*.json` del proyecto) del que salen el HTML y el TS; así los dos destinos no divergen.
- Revisar contradicciones entre fuentes del cliente al cargar datos (caso: la lista de ubicaciones de la FAQ ≠ la del afiche de campaña) y dejarlas como pendiente en el README.

## I. CSS responsive en el constructor (2026-10-13, caso-web-universidad-01 QA visual tablet/móvil)
| # | Síntoma | Causa | Solución / prevención |
|---|---|---|---|
| I1 | La página se desborda unos píxeles a la derecha en móvil; tarjetas pegadas al borde | Rejilla `display:grid` sin columnas definidas: la columna `auto` crece al `min-content` de un hijo (botón con `white-space:nowrap`) | `grid-template-columns: minmax(0,1fr)` y dejar que los botones largos se partan en móvil. Probar el desborde con script (`scrollWidth > clientWidth`), no solo a ojo |
| I2 | Botones cortados dentro de tarjetas en tablet (768) | 3 columnas desde 768 px (columnas de ~190 px) | 3 columnas solo desde 992 px; en tablet 1 columna |
| I3 | Listas numeradas/viñetas sin símbolo | El reseteo de Tailwind (preflight) quita `list-style` | Declarar `list-style: decimal/disc` en los contenedores de texto |
| I4 | Medir en un `iframe` da anchos falsos (375 en vez de 390) | La barra de desplazamiento del iframe ocupa 15 px | Comparar contra `documentElement.clientWidth`, no contra el ancho nominal |
| I5 | Capturas de página completa por tramos salen desalineadas | Tramos > 10 000 px con `margin-top` negativo en iframe | Usar tramos de ≤ 12 000 px y verificar costuras; para medir, usar páginas «puente» en `public/` (mismo origen) |
| I6 | Los cambios «en sitio» al CSS del constructor obligan a pegar el archivo completo | — | Para transferir, añadir **sobrescrituras al final** del CSS (mismo selector, orden posterior) en vez de editar reglas anteriores; así el cambio viaja como bloque «AÑADE AL FINAL» |

## J. Listado con filtros + ficha dinámica en local (2026-10-13, `caso-web-universidad-01`)
| # | Síntoma | Causa | Solución / prevención |
|---|---|---|---|
| J1 | `tsc` marca `slug`/`zona`/`filtro` «no existe» en `<Link params/search>` | `routeTree.gen.ts` de la descarga no conoce las rutas nuevas | Con el servidor de Vite en marcha, tocar el archivo de la ruta nueva (`touch`) para que regenere el árbol y volver a correr `tsc`: debe dar 0 errores. **Ojo:** copiar `src/*` a la copia de pruebas pisa el árbol regenerado |
| J2 | Los datos de ~20 elementos estaban repartidos en CSV, HTML y TS | Varias fuentes | Un generador CSV → `<p>-listado.ts` (patrón en `ejemplos/caso-web-universidad-01/gen_datos_desde_csv.ejemplo.py`); las reglas del cliente (código oficial oculto si no está verificado, cupos sin totales) se aplican al generar, no en el componente |
| J3 | Filtros que no se pueden compartir | Estado en memoria | Filtros en la URL con `validateSearch` + `navigate({ search, replace:true, resetScroll:false })`; probar con eventos reales (cambiar `<select>` con el setter nativo + `dispatchEvent`) |
| J4 | Estado vacío engañoso al filtrar por una categoría sin elementos | La asignación categoría→elemento la hizo la IA a partir de textos del cliente, sin dato firme | Mensaje específico («no hay elementos para esta categoría entre los N») + enlace a la lista completa; validar la asignación con el cliente |
| J5 | Fichas con la misma foto repetida | Fotos de la Home solo para unos pocos elementos | Elegir una foto por elemento de las hojas de contacto (4:3, rostros arriba) y subir la carpeta de la entrega 2 |

## K. Contenido largo desde fuentes oficiales + límite de 50 000 caracteres + acceso al builder (2026-10-13, `caso-web-universidad-01`)
| # | Síntoma | Causa | Solución / prevención |
|---|---|---|---|
| K1 | Un archivo generado (datos + textos de ~20 fichas) pesa 67 mil caracteres y no cabe en una parte del chat | Límite de 50 000 caracteres por mensaje | Separar en dos módulos desde el generador: datos (`<p>-listado.ts`, ~21 mil) y textos largos (`<p>-listado-textos.ts`, ~48 mil, que se pega solo en su parte). Medir **caracteres**, no bytes (las tildes ocupan 2 bytes) |
| K2 | `urllib` recibe 403 en páginas oficiales que en el navegador abren | El sitio filtra por cabeceras | `curl -L` con User-Agent de Chrome + `Accept`, `Accept-Language`, `Sec-Fetch-Mode: navigate` y `Upgrade-Insecure-Requests: 1` |
| K3 | El conector de Drive lee la hoja de cálculo como texto pero **sin los hipervínculos** de la columna de documentos | Solo expone el texto visible de la celda | Sacar los enlaces de las **páginas oficiales** (sus `<a>` a PDF o a Drive) y descargarlos con `uc?export=download&id=…`; comprobar `%PDF` y renombrar lo que no sea lo esperado |
| K4 | PDF de la hoja que no corresponde al elemento (documento de otro; el mismo folleto en dos filas) | Errores de captura del cliente o de la página oficial | Abrir **cada** PDF y comprobar que su portada nombra el elemento antes de citarlo; renombrar con `-ERROR-…` y listarlo en el documento de hallazgos para el cliente |
| K5 | Texto oficial con erratas («favorezvan», «usabiidad») o ítems que son fragmentos de una frase | Copia literal de la fuente | Elegir ítems limpios (no «arreglar» el texto del cliente) y normalizar solo viñetas, códigos y punto final; dejar la regla en el extractor |
| K6 | Capturas «móviles» a 390 px salen con el texto cortado | `chrome --headless` no baja de ~500 px de ancho de ventana: se recorta una página de 500 px | Para móvil, medir y capturar con las páginas puente (`overflow.html`: iframe del ancho exacto), nunca con `--window-size` < 500 |
| K7 | Fotos nuevas aún no subidas a Medios dejan imágenes rotas en la vista previa | `img()` devuelve la ruta base si el archivo no está en `IMG_URLS` | Respaldo en el componente: `onError` cambia a una foto de respaldo una sola vez (`dataset`), con su `alt` (ver `ejemplos/caso-web-universidad-01/ruta-con-filtros.ejemplo.tsx`); se prueba forzando un 404 |
| K8 | No se puede operar el builder (Claude in Chrome sin conexión y el navegador integrado sin sesión) | La extensión no está emparejada; el navegador integrado redirige al login | No escribir credenciales. Dejar la entrega **lista para pegar** (partes ≤ 50 000 + paso de imágenes + capturas) y avisar con claridad qué falta; retomar cuando el usuario reconecte la extensión (`list_connected_browsers` debe mostrar el navegador) |
| K9 | Al reemplazar archivos «completos» (componentes de secciones) se pueden pisar cambios de la IA del builder | El archivo del builder pudo cambiar después de la descarga | Pedir a la IA en las REGLAS: «compara con el actual; si tiene cambios que no están aquí, dímelo y no los pises»; no tocar `<p>-data.ts` (tiene `IMG_URLS`) |

## L. Operar el builder con Claude in Chrome (2026-10-14, `caso-web-universidad-01`, entrega 2 aplicada)
| # | Síntoma | Causa | Solución / prevención |
|---|---|---|---|
| L1 | «Claude in Chrome is not connected» / `list_connected_browsers` vacío | Extensión sin emparejar o Chrome cerrado | No se puede operar el builder ni escribir credenciales. Esperar a que el usuario reconecte; cuando `list_connected_browsers` devuelva el navegador: `tabs_context_mcp {createIfEmpty:true}` crea **su propio** grupo (no controla la pestaña que el usuario dejó abierta) → `navigate` a la URL del proyecto en esa pestaña (la sesión de GHL ya está iniciada) |
| L2 | El builder vive en un iframe de otro origen: `find`/`read_page` no ven el chat | Aislamiento de origen | Operar por **coordenadas** (el marco de captura es 1568×726; el chat abajo a la izquierda, botón de enviar ≈ (356, 691)) |
| L3 | Al pegar en el chat no entra nada, o `ctrl+a` selecciona **toda la página** (se ve azul/gris) | El primer clic no da foco al `textarea` | Patrón fiable: clic → `type "x"` → `zoom` para comprobar que la «x» está en el cuadro → recién ahí `ctrl+a` + `ctrl+v` (portapapeles puesto antes con `Set-Clipboard`). Verificar **inicio y final** del texto pegado (`ctrl+Home` + zoom). Si se seleccionó la página: recargar |
| L4 | Capturas que fallan con «Script injection timed out» o «renderer frozen» | Pestaña en segundo plano o página ocupada (pegar 48 mil caracteres) | Trabajar con **una sola pestaña**; esperar 5–10 s y reintentar; cerrar pestañas extra |
| L5 | La IA del builder aplica las partes pero **cambia la estructura** | Decide sola (divide un componente de 26 KB en 3 módulos + barrel; mueve `IMG_URLS` a `<p>-img.ts` como `IMG_MAP`; formatea con prettier; deja carpetas temporales `tmp-img/`) | Tras aplicar: **descargar la base de código, comparar semánticamente con el local y adoptar la versión del builder como nueva base local** (con copia de respaldo). Pedirle que borre sus temporales. Actualizar AGENTS.md/README.md con la estructura real |
| L6 | «Descargar base de código» no deja un `.zip` visible | Chrome guarda un `.tmp` con nombre de GUID en la carpeta de descargas | Es un zip válido (`PK`): copiarlo a una carpeta de trabajo, **no extraer `.env`**, borrar el `.tmp` y la copia después |
| L7 | Subir fotos a Medios | La página de Medios **sí** es del documento principal | `find` «file input» → `ref` del `input type=file` («Subir») → `file_upload` con rutas absolutas (≤ 10 MB por llamada). Crear carpeta nueva por entrega; para abrirla hay que `find` su tarjeta y `double_click` por `ref` (el clic por coordenadas no la abre) |
| L8 | Obtener las URL de los archivos subidos sin «Insertar enlaces» | — | En la página de Medios: `document.querySelectorAll('img')` con `filesafe` → la URL original está tras `u_` (`https://assets.cdn.filesafe.space/<location>/media/<id>.jpg`). Descargarlas y emparejar por **SHA-256** (`match_cdn.py`: 17/17) y mandar a la IA el mapa **ya verificado** (nombre → URL) en lugar de pedirle que adivine |
| L9 | Verificar páginas en la vista previa real | La URL pública `…vibepreview.app` es un documento normal | Con `javascript_tool`, abrir `iframe`s del mismo origen por ruta y ancho (390/1280) y medir h1, desborde, imágenes rotas y respaldos: 46 comprobaciones en ~5 min. Las rutas del panel de vista previa se eligen de su lista desplegable |

## G. Contenido (caso `caso-web-universidad-01`; reglas de datos que sirven de patrón)
- Fuentes oficiales con **un código oficial contradictorio** (p. ej. registro de un programa) → no mostrarlo hasta confirmarlo con la oficina responsable.
- Oferta vigente = afiche de campaña + hoja del cliente; **sin totales de cupos** (se copia la cifra o rango de cada fila); no prometer admisión ni gratuidad.
- Calendarios: se muestran tal como están en el afiche, con su fecha de consulta, y las discrepancias entre documentos del cliente se anotan como pendiente en el README.
