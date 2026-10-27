"""generar_biblioteca.py — genera la «biblioteca de módulos» de un sistema de diseño (una sola página HTML) desde un manifiesto JSON.

  python -I generar_biblioteca.py manifiesto.json salida/        # entrega completa (carpeta)
  python -I generar_biblioteca.py manifiesto.json salida/index.html

Qué produce (modo `documentar`, referencia 04 §13). La ENTREGA es una carpeta: la página para personas (index.html) más la capa para IA
(sistema.json, llms.txt, AGENTS.md, modulos/<id>.json y logo.svg) para que, dándole solo la URL, una IA documente todo y construya a partir de ahí.
Qué produce:
  - Menú lateral izquierdo tipo panel (sticky) con el logo arriba a la izquierda, buscador y módulos agrupados.
  - Un módulo por pieza del sistema: cabecera, estado, descripción, «Ver CSS del módulo» y variantes.
  - Cada variante tiene su REFERENTE VISUAL (el componente real aislado en Shadow DOM, o un bloque visual de datos)
    y sus acciones: Copiar HTML · Copiar CSS · Copiar JSON · Copiar prompt (para que una IA lo duplique) · Ver código.
  - Aviso (toast) al copiar, código con pestañas, diálogo nativo para el CSS del módulo, menú que se pliega en móvil.
  - `noindex` por defecto (una página de documentación no debe indexarse; referencia 04 §11).

Manifiesto (resumen; ver templates/biblioteca-manifiesto.json):
  meta    {titulo, subtitulo, version, fecha, idioma, noindex, descripcion, base_preview, home_url, home_etiqueta, pie_enlace}
          base_preview = CSS que SOLO se usa para pintar la previsualización (tipografía base, reset del sitio); no se copia.
          home_url / home_etiqueta = botón «Volver al sitio» (menú lateral y barra móvil).
  marca   {nombre, logo_svg (texto SVG), logo_alto, acento, tinta, fondo, fuentes: [{familia, peso, url}], fuente_ui, fuente_mono}
  reglas_ia [texto, ...]                      # reglas que se pegan al inicio de cada prompt
  grupos  [{etiqueta, modulos: [id, ...]}]
  resumen {kpis: [{valor, etiqueta, nota, tono(ok|mal|aviso|info), barra(0-100)}], leyenda: bool}
  modulos [{id, n, titulo, estado, version, descripcion, css, tokens{--x: valor}, variantes: [...]}]
  variante {id, nombre, uso, tema, tipo(componente|doc), ancho(px|"100%"), html, css, json, nota, escenario(tight|normal)}
  - tipo «componente»: `html` se pinta en Shadow DOM con `tokens` + `css` del módulo (+ `css` de la variante).
  - tipo «doc»: `html` se pinta directamente con las clases b-* de esta página (ver funciones bloque_* abajo).

Solo biblioteca estándar. Acepta el HTML tal como lo emite el sitio; no lo modifica (el HTML que se copia es el real).
Límites: la previsualización no puede forzar :hover/:focus (se prueban pasando el ratón o con Tab); no hay tema oscuro salvo
que el manifiesto lo declare en `tema`. No valida el HTML del módulo.
"""
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _comun as c  # noqa: E402
import contraste as ct  # noqa: E402

esc = html.escape


# ============================================================================ bloques visuales (tipo «doc»)
def bloque_swatches(items):
    """items: [(nombre, valor, nota?)] → cuadrícula de muestras de color."""
    out = '<ul class="b-swatches">'
    for it in items:
        nombre, valor = it[0], it[1]
        nota = it[2] if len(it) > 2 else ""
        out += (f'<li class="b-swatch"><span class="b-swatch__c" style="background:{esc(valor)}" aria-hidden="true"></span>'
                f'<span class="b-swatch__n"><code>{esc(nombre)}</code></span><span class="b-swatch__v">{esc(valor)}</span>'
                + (f'<span class="b-swatch__t">{esc(nota)}</span>' if nota else "") + "</li>")
    return out + "</ul>"


def bloque_escala(items, maximo=None, unidad="px"):
    """items: [(nombre, px)] → barras proporcionales."""
    mx = maximo or max(v for _, v in items)
    out = '<div class="b-escala" role="list">'
    for nombre, v in items:
        w = max(2, round(v / mx * 100))
        out += (f'<div class="b-escala__f" role="listitem"><code>{esc(nombre)}</code>'
                f'<span class="b-escala__b"><span style="width:{w}%"></span></span><span class="b-escala__v">{v}{unidad}</span></div>')
    return out + "</div>"


def bloque_comparar(izq, der, flecha="→"):
    """izq/der: (etiqueta, html_interior) → dos tarjetas lado a lado (antes/después, A/B)."""
    return (f'<div class="b-comp"><figure class="b-comp__c"><figcaption>{esc(izq[0])}</figcaption><div>{izq[1]}</div></figure>'
            f'<span class="b-comp__f" aria-hidden="true">{esc(flecha)}</span>'
            f'<figure class="b-comp__c"><figcaption>{esc(der[0])}</figcaption><div>{der[1]}</div></figure></div>')


def bloque_contraste(fg, bg, nombre, tipo="normal", muestra="Aa texto de ejemplo"):
    """Tarjeta de contraste: muestra real + razón + veredicto (sin redondear antes de comparar)."""
    ratio = ct.contraste(fg, bg)
    ok = ct.evaluar(tipo, ratio)
    minimo = ct.UMBRALES[tipo]
    estado = "pasa" if ok else "falla"
    return (f'<div class="b-contr b-contr--{estado}"><div class="b-contr__m" style="color:{esc(fg)};background:{esc(bg)}">{esc(muestra)}</div>'
            f'<div class="b-contr__d"><strong>{esc(nombre)}</strong><span>{ratio:.2f}:1 · mínimo {minimo:g}:1</span>'
            f'<span class="b-pill b-pill--{"ok" if ok else "mal"}">{"Pasa" if ok else "Falla"} AA</span></div></div>')


def bloque_antes_despues(hoy, propuesta, etiqueta_hoy="Hoy", etiqueta_prop="Propuesta"):
    """Dos filas apiladas (sirve en columnas estrechas): lo que se usa hoy (tachado) y lo que se propone."""
    return (f'<div class="b-ad"><div><span class="b-ad__e">{esc(etiqueta_hoy)}</span>{bloque_chips(hoy, "mal")}</div>'
            f'<div><span class="b-ad__e">{esc(etiqueta_prop)}</span>{bloque_chips(propuesta, "ok")}</div></div>')


def bloque_chips(items, tono=""):
    return '<div class="b-chips">' + "".join(f'<span class="b-chip {tono}">{c_}</span>' for c_ in items) + "</div>"


def bloque_tarjeta(titulo, cuerpo, etiqueta="", tono=""):
    return (f'<article class="b-card {tono}"><header><h3>{esc(titulo)}</h3>'
            + (f'<span class="b-pill b-pill--{tono or "info"}">{esc(etiqueta)}</span>' if etiqueta else "")
            + f"</header><div>{cuerpo}</div></article>")


# ============================================================================ CSS y JS de la página
CSS = r"""
@font-face-placeholder
:root{
  --acento:%%ACENTO%%; --acento-texto:%%ACENTO_TEXTO%%; --tinta:%%TINTA%%; --texto:#1E2939; --suave:#4B5565;
  --fondo:%%FONDO%%; --sup:#FFFFFF; --sup2:#F2F4F7; --borde:#E4E7EC; --borde2:#CBD2DC; --ok:#067647; --mal:#B42318; --aviso:#B54708; --info:#175CD3;
  --ok-f:#ECFDF3; --mal-f:#FEF3F2; --aviso-f:#FFFAEB; --info-f:#EFF8FF; --acento-f:%%ACENTO_F%%;
  --sobre-acento:%%SOBRE_ACENTO%%;--ui:%%FUENTE_UI%%; --mono:%%FUENTE_MONO%%; --r1:4px; --r2:8px; --r3:12px; --pill:999px; --rail:288px;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:24px}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}*{transition:none!important;animation:none!important}}
body{margin:0;background:var(--fondo);color:var(--texto);font:16px/24px var(--ui);-webkit-font-smoothing:antialiased}
a{color:var(--acento-texto);text-underline-offset:3px}
code,pre,kbd{font-family:var(--mono)}
code{font-size:.9em;background:var(--sup2);border:1px solid var(--borde);border-radius:var(--r1);padding:0 4px;overflow-wrap:anywhere}
pre code{background:none;border:0;border-radius:0;padding:0;font-size:inherit;color:inherit;overflow-wrap:normal}
:focus-visible{outline:2px solid var(--tinta);outline-offset:2px;border-radius:var(--r1)}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.salto{position:absolute;left:-9999px;top:8px;background:var(--tinta);color:#fff;padding:8px 16px;border-radius:var(--r2);z-index:100}
.salto:focus{left:16px}
.app{display:grid;grid-template-columns:var(--rail) minmax(0,1fr);min-height:100vh}
/* ---------- menú lateral (panel) ---------- */
.rail{position:sticky;top:0;align-self:start;height:100vh;display:flex;flex-direction:column;background:var(--sup);border-right:1px solid var(--borde);z-index:30}
.rail__top{padding:24px 20px 16px;border-bottom:1px solid var(--borde)}
.rail__logo{display:block;height:%%LOGO_ALTO%%px;width:auto;max-width:100%}
.rail__logo svg{display:block;height:100%;width:auto}
.rail__home{display:inline-flex;align-items:center;gap:8px;margin-top:16px;min-height:36px;padding:0 12px;border:1px solid var(--borde2);border-radius:var(--r2);color:var(--tinta);font:600 13px/20px var(--ui);text-decoration:none;background:var(--sup)}
.rail__home:hover{border-color:var(--tinta)}.rail__home svg{width:16px;height:16px}
.rail__t{margin:16px 0 0;font-weight:700;font-size:15px;line-height:20px;color:var(--tinta)}
.rail__v{margin:4px 0 0;font-size:13px;line-height:20px;color:var(--suave)}
.rail__buscar{margin-top:16px}
.rail__buscar input{width:100%;height:36px;padding:0 12px;border:1px solid var(--borde2);border-radius:var(--r2);background:var(--fondo);font:inherit;font-size:14px;color:var(--texto)}
.rail__buscar input::placeholder{color:var(--suave)}
.rail__nav{flex:1;overflow-y:auto;overscroll-behavior:contain;padding:8px 12px 24px}
.rail__g{margin:16px 0 4px;padding:0 8px;font:600 12px/16px var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--suave)}
.rail__l{list-style:none;margin:0;padding:0}
.rail__i{display:grid;grid-template-columns:32px 1fr auto;align-items:center;gap:8px;min-height:36px;padding:4px 8px;border-radius:var(--r2);color:var(--texto);text-decoration:none;font-size:14px;line-height:20px;border-left:3px solid transparent}
.rail__i:hover{background:var(--sup2)}
.rail__i[aria-current=true]{background:var(--acento-f);color:var(--acento-texto);font-weight:600;border-left-color:var(--acento)}
.rail__n{font:500 12px/16px var(--mono);color:var(--suave)}
.rail__i[aria-current=true] .rail__n{color:var(--acento-texto)}
.dot{width:8px;height:8px;border-radius:var(--pill);background:var(--borde2)}
.dot--ok{background:var(--ok)}.dot--mal{background:var(--mal)}.dot--aviso{background:var(--aviso)}.dot--info{background:var(--info)}
.rail__vacio{padding:8px;font-size:13px;color:var(--suave)}
.rail__pie{padding:12px 20px 16px;border-top:1px solid var(--borde);font-size:12px;line-height:16px;color:var(--suave)}
.rail__ley{display:flex;flex-wrap:wrap;gap:4px 12px;list-style:none;margin:0 0 8px;padding:0}.rail__ley li{display:flex;align-items:center;gap:6px}.rail__pie p{margin:0}
.topbar{display:none}
/* ---------- contenido ---------- */
.main{min-width:0;padding:48px 56px 96px}
.main__in{max-width:1120px}
.mod{scroll-margin-top:24px}.mod+.mod{margin-top:96px}
.mod__eye{display:flex;align-items:center;gap:12px;padding-bottom:12px;border-bottom:1px solid var(--acento);font:600 12px/16px var(--mono);letter-spacing:.14em;text-transform:uppercase;color:var(--acento-texto)}
.mod__head{display:flex;flex-wrap:wrap;gap:16px 24px;justify-content:space-between;align-items:flex-start;margin-top:24px}
.mod__tit{display:flex;flex-wrap:wrap;align-items:center;gap:12px}
h1,h2,h3,h4{color:var(--tinta);margin:0}
h1{font-size:40px;line-height:48px;letter-spacing:-.015em}
h2{font-size:32px;line-height:40px;letter-spacing:-.01em}
h3{font-size:20px;line-height:28px}
h4{font-size:16px;line-height:24px}
.b-card h3{font-size:16px;line-height:24px}
.leyenda h2{font-size:20px;line-height:28px}
.mod__desc{margin:16px 0 0;max-width:68ch;color:var(--suave);font-size:18px;line-height:28px}
.pill,.b-pill{display:inline-flex;align-items:center;min-height:24px;padding:0 12px;border-radius:var(--pill);font-size:13px;line-height:20px;font-weight:600;background:var(--sup2);color:var(--suave)}
.pill--ok,.b-pill--ok{background:var(--ok-f);color:var(--ok)}.pill--mal,.b-pill--mal{background:var(--mal-f);color:var(--mal)}
.pill--aviso,.b-pill--aviso{background:var(--aviso-f);color:var(--aviso)}.pill--info,.b-pill--info{background:var(--info-f);color:var(--info)}
.btn{display:inline-flex;align-items:center;gap:8px;min-height:36px;padding:0 12px;border:1px solid var(--borde2);border-radius:var(--r2);background:var(--sup);color:var(--tinta);font:600 13px/20px var(--ui);cursor:pointer;white-space:nowrap}
.btn:hover{border-color:var(--tinta)}
.btn svg{width:16px;height:16px;flex:none}
.btn--ia{background:var(--acento-texto);border-color:var(--acento-texto);color:var(--sobre-acento)}
.btn--ia:hover{background:var(--tinta);border-color:var(--tinta)}
.btn[aria-expanded=true]{background:var(--tinta);border-color:var(--tinta);color:#fff}
.btn[disabled]{opacity:.5;cursor:not-allowed}
/* ---------- variante ---------- */
.vars{display:flex;flex-direction:column;gap:48px;margin-top:40px}
.demo{background:var(--sup);border:1px solid var(--borde);border-radius:var(--r3);overflow:hidden;scroll-margin-top:24px}
.demo__bar{display:flex;flex-wrap:wrap;align-items:center;gap:12px 16px;padding:16px 24px;border-bottom:1px solid var(--borde)}
.demo__i{display:grid;place-items:center;width:28px;height:28px;border-radius:var(--r2);background:var(--tinta);color:#fff;font:700 12px/16px var(--mono)}
.demo__nom{font-weight:700;font-size:16px;line-height:20px;display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.demo__uso{font-size:14px;line-height:20px;color:var(--suave)}
.chip{display:inline-flex;align-items:center;gap:6px;padding:2px 10px;border:1px solid var(--borde2);border-radius:var(--pill);font:600 12px/16px var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--suave)}
.chip::before{content:"";width:8px;height:8px;border-radius:var(--pill);border:1px solid var(--borde2);background:#fff}
.chip--dark{background:var(--tinta);color:#fff;border-color:var(--tinta)}.chip--dark::before{background:var(--tinta);border-color:#fff}
.demo__acc{display:flex;flex-wrap:wrap;gap:8px;margin-left:auto}
.demo__stage{padding:40px 32px;background:linear-gradient(var(--sup2) 0 0) padding-box,conic-gradient(from 90deg at 1px 1px,transparent 25%,var(--borde) 0) 0 0/24px 24px;overflow-x:auto}
.demo__stage--tight{padding:24px}
.demo__stage--doc{background:var(--sup);}
.demo__fit{margin:0 auto}
.demo__nota{margin:0;padding:12px 24px;border-top:1px solid var(--borde);font-size:14px;line-height:20px;color:var(--suave);background:var(--sup)}
.code{border-top:1px solid var(--borde);background:#0B1220;color:#E5E7EB}
.code[hidden]{display:none}
.code__bar{display:flex;flex-wrap:wrap;align-items:center;gap:8px;padding:8px 16px;border-bottom:1px solid #1F2937}
.code__tabs{display:flex;gap:4px;flex:1;flex-wrap:wrap}
.code__tab{min-height:32px;padding:0 12px;border:0;border-radius:var(--r2);background:transparent;color:#C7CEDA;font:600 12px/16px var(--mono);cursor:pointer}
.code__tab[aria-selected=true]{background:#1F2937;color:#fff}
.code__tab:focus-visible,.code .btn:focus-visible{outline-color:#fff}
.code .btn{background:transparent;border-color:#475467;color:#E5E7EB}
.code .btn:hover{border-color:#fff}
.code pre{margin:0;padding:16px 24px;max-height:420px;overflow:auto;font-size:13px;line-height:20px;white-space:pre;tab-size:2}
.code .t{color:#7DD3FC}.code .a{color:#FDBA74}.code .v{color:#86EFAC}
dialog{border:1px solid var(--borde2);border-radius:var(--r3);padding:0;width:min(880px,calc(100vw - 32px));max-height:calc(100vh - 48px);background:#0B1220;color:#E5E7EB}
dialog::backdrop{background:rgba(15,23,42,.6)}
dialog .code__bar{justify-content:space-between}
dialog h3{color:#fff;font-size:16px;line-height:24px;margin:0;flex:1}
dialog pre{margin:0;padding:16px 24px;overflow:auto;max-height:calc(100vh - 160px);font-size:13px;line-height:20px;white-space:pre}
.paraia{margin-top:24px;background:var(--sup);border:1px solid var(--borde);border-left:4px solid var(--acento);border-radius:var(--r3);padding:24px}
.paraia p{margin:8px 0 0;max-width:70ch}
.paraia__url{display:flex;flex-wrap:wrap;gap:8px 12px;align-items:center;margin-top:16px}
.paraia__l{margin:16px 0 0;padding-left:20px;display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:4px 24px;font-size:14px}
.toast{position:fixed;right:24px;bottom:24px;z-index:80;max-width:min(360px,calc(100vw - 48px));padding:12px 16px;border-radius:var(--r2);background:var(--tinta);color:#fff;font-size:14px;line-height:20px;opacity:0;transform:translateY(8px);pointer-events:none;transition:opacity .2s,transform .2s}
.toast[data-v=true]{opacity:1;transform:none}
/* ---------- resumen ---------- */
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px;margin-top:32px}
.kpi{background:var(--sup);border:1px solid var(--borde);border-radius:var(--r3);padding:20px}
.kpi__v{font-size:40px;line-height:48px;font-weight:700;color:var(--tinta);letter-spacing:-.02em}
.kpi__e{margin:4px 0 0;font-weight:600;font-size:14px;line-height:20px}
.kpi__n{margin:4px 0 0;font-size:13px;line-height:20px;color:var(--suave)}
.kpi__b{height:8px;margin-top:12px;border-radius:var(--pill);background:var(--sup2);overflow:hidden}
.kpi__b span{display:block;height:100%;border-radius:var(--pill);background:var(--acento-texto)}
.kpi--ok .kpi__b span{background:var(--ok)}.kpi--mal .kpi__b span{background:var(--mal)}.kpi--aviso .kpi__b span{background:var(--aviso)}.kpi--info .kpi__b span{background:var(--info)}
.leyenda{margin-top:40px;background:var(--sup);border:1px solid var(--borde);border-radius:var(--r3);padding:24px}
.leyenda dl{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px 24px;margin:16px 0 0}
.leyenda dt{display:flex;align-items:center;gap:8px;font-weight:600}.leyenda dd{margin:4px 0 0;font-size:14px;line-height:20px;color:var(--suave)}
/* ---------- bloques visuales ---------- */
.b-swatches{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(168px,1fr));gap:12px}
.b-swatch{display:grid;grid-template-columns:1fr;gap:4px;padding:8px;border:1px solid var(--borde);border-radius:var(--r3);background:var(--sup)}
.b-swatch__c{display:block;height:56px;border-radius:var(--r2);border:1px solid var(--borde)}
.b-swatch__n{font-size:13px;line-height:20px;margin-top:4px}.b-swatch__v{font:500 12px/16px var(--mono);color:var(--suave);overflow-wrap:anywhere}.b-swatch__t{font-size:12px;line-height:16px;color:var(--suave)}
.b-escala{display:flex;flex-direction:column;gap:8px}
.b-escala__f{display:grid;grid-template-columns:128px 1fr 64px;align-items:center;gap:12px;font-size:13px}
.b-escala__b{height:16px;border-radius:var(--r1);background:var(--sup2)}.b-escala__b span{display:block;height:100%;border-radius:var(--r1);background:var(--acento-texto)}
.b-escala__v{font:500 12px/16px var(--mono);color:var(--suave);text-align:right}
.b-comp{display:grid;grid-template-columns:1fr auto 1fr;gap:16px;align-items:stretch}
.b-comp__c{margin:0;border:1px solid var(--borde);border-radius:var(--r3);background:var(--sup);overflow:hidden}
.b-comp__c figcaption{padding:8px 16px;border-bottom:1px solid var(--borde);font:600 12px/16px var(--mono);letter-spacing:.1em;text-transform:uppercase;color:var(--suave);background:var(--sup2)}
.b-comp__c>div{padding:16px}
.b-comp__f{align-self:center;font-size:24px;color:var(--suave)}
.b-chips{display:flex;flex-wrap:wrap;gap:8px}.b-chip{display:inline-flex;align-items:center;max-width:100%;min-height:28px;padding:2px 12px;border-radius:var(--r3);overflow-wrap:anywhere;border:1px solid var(--borde2);background:var(--sup);font:500 13px/20px var(--mono)}
.b-chip.mal{border-color:var(--mal);color:var(--mal);background:var(--mal-f);text-decoration:line-through}.b-chip.ok{border-color:var(--ok);color:var(--ok);background:var(--ok-f)}
.b-contr{display:grid;grid-template-columns:136px 1fr;border:1px solid var(--borde);border-radius:var(--r3);overflow:hidden;background:var(--sup)}
.b-contr__m{display:grid;place-items:center;padding:16px;font-weight:600;font-size:16px;line-height:24px;text-align:center}
.b-contr__d{display:flex;flex-direction:column;align-items:flex-start;gap:4px;padding:12px 16px;font-size:13px;line-height:20px}.b-contr__d span:not(.b-pill){color:var(--suave)}
.b-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px}
.b-card{border:1px solid var(--borde);border-radius:var(--r3);background:var(--sup);padding:16px}
.b-card header{display:flex;flex-wrap:wrap;gap:8px 12px;justify-content:space-between;align-items:flex-start;margin-bottom:8px}
.b-card>div{font-size:14px;line-height:20px;color:var(--suave)}
.b-card.mal{border-left:4px solid var(--mal)}.b-card.aviso{border-left:4px solid var(--aviso)}.b-card.info{border-left:4px solid var(--info)}.b-card.ok{border-left:4px solid var(--ok)}
.b-vis{margin:12px 0 0;padding:12px;border:1px dashed var(--borde2);border-radius:var(--r2);background:var(--fondo)}
.b-ad{display:flex;flex-direction:column;gap:12px}.b-ad__e{display:block;margin-bottom:4px;font:600 12px/16px var(--mono);letter-spacing:.1em;text-transform:uppercase;color:var(--suave)}
.b-tabla{width:100%;border-collapse:collapse;font-size:14px}.b-tabla th,.b-tabla td{padding:8px 12px;text-align:left;border-bottom:1px solid var(--borde);vertical-align:top}.b-tabla th{background:var(--sup2);font-weight:600}
.b-tabla-w{overflow-x:auto}
.b-lista{margin:0;padding-left:20px}.b-lista li{margin:4px 0}
/* ---------- responsive ---------- */
@media (max-width:1024px){
  .app{grid-template-columns:minmax(0,1fr)}
  .topbar{display:flex;position:sticky;top:0;z-index:40;align-items:center;justify-content:space-between;gap:12px;padding:12px 16px;background:var(--sup);border-bottom:1px solid var(--borde)}
  .topbar .rail__logo{height:%%LOGO_ALTO_M%%px}
  .rail{position:fixed;inset:0 auto 0 0;width:min(320px,86vw);height:100dvh;transform:translateX(-100%);transition:transform .2s;box-shadow:none}
  .rail[data-open=true]{transform:none}
  .scrim{position:fixed;inset:0;background:rgba(15,23,42,.5);z-index:25;display:none}
  .scrim[data-open=true]{display:block}
  .main{padding:32px 16px 64px}
  .b-comp{grid-template-columns:1fr}.b-comp__f{transform:rotate(90deg);justify-self:center}
  h1{font-size:32px;line-height:40px}h2{font-size:28px;line-height:36px}
}
@media (max-width:600px){
  .demo__bar{padding:16px}.demo__acc{margin-left:0;width:100%}
  .demo__stage{padding:24px 16px}.b-escala__f{grid-template-columns:96px 1fr 56px}
  .b-contr{grid-template-columns:1fr}
}
"""

JS = r"""
(function(){'use strict';
var D=JSON.parse(document.getElementById('datos').textContent);
var V={};D.modulos.forEach(function(m){m.variantes.forEach(function(v){v._m=m;V[v.id]=v;});});
function $(s,r){return (r||document).querySelector(s);} function $$(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s));}
/* ---- previsualización aislada (Shadow DOM) ---- */
function tokensCss(m,sel){var t=m.tokens||{},o=sel+' {\n';Object.keys(t).forEach(function(k){o+='  '+k+': '+t[k]+';\n';});return o+'}';}
$$('[data-shadow]').forEach(function(h){if(h.shadowRoot)return;var v=V[h.getAttribute('data-shadow')];if(!v)return;var r=h.attachShadow({mode:'open'});
  r.innerHTML='<style>:host{display:block}'+(D.meta.base_preview||'')+tokensCss(v._m,':host')+'\n'+(v._m.css||'')+'\n'+(v.css||'')+'</style>'+v.html;});
/* ---- texto copiable ---- */
function cssCompleto(v){var m=v._m;return '/* '+m.titulo+' · '+v.nombre+' */\n'+(m.tokens&&Object.keys(m.tokens).length?tokensCss(m,':root')+'\n\n':'')+(m.css||'')+(v.css?'\n\n'+v.css:'');}
function jsonDe(v){return v.json==null?'':JSON.stringify(v.json,null,2);}
function promptDe(v){var m=v._m,p=[];
  p.push('Actúa como desarrollador front-end que trabaja DENTRO de un sistema de diseño ya existente ('+D.meta.titulo+').');
  if(D.reglas_ia&&D.reglas_ia.length){p.push('Reglas del sistema:\n'+D.reglas_ia.map(function(r){return '- '+r;}).join('\n'));}
  p.push('Módulo: '+m.n+' · '+m.titulo+' · variante «'+v.nombre+'»'+(v.uso?' (uso: '+v.uso+')':'')+'.');
  if(v.json!=null)p.push('Contrato / datos (JSON):\n```json\n'+jsonDe(v)+'\n```');
  if(v.html)p.push('HTML de referencia (real, no lo reinterpretes):\n```html\n'+snippet(v)+'\n```');
  if(m.css||v.css)p.push('CSS del módulo:\n```css\n'+cssCompleto(v)+'\n```');
  p.push('Tarea: duplica este módulo y adáptalo así → [ESCRIBE AQUÍ QUÉ CAMBIAR: texto, imagen, tamaño, variante nueva…]');
  p.push('Condiciones: usa SOLO las clases y variables CSS de arriba; no inventes colores, medidas ni nombres de props; conserva los estados (hover, foco visible, deshabilitado si existe); respeta el contraste AA. Entrega HTML y CSS, y dime qué NO pudiste verificar.');
  return p.join('\n\n');}
/* ---- HTML legible ---- */
function snippet(v){return v.html_copia!=null?v.html_copia:v.html;}
function esc(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function hl(s){return esc(s).replace(/(&lt;\/?)([a-zA-Z0-9-]+)|([a-zA-Z-:]+)="([^"]*)"/g,function(m,o,t,a,val){if(o!==undefined)return o+'<span class="t">'+t+'</span>';return '<span class="a">'+a+'</span>="<span class="v">'+val+'</span>"';});}
var CONT={html:function(v){return snippet(v);},css:cssCompleto,json:jsonDe,prompt:promptDe};
var ETQ={html:'HTML',css:'CSS',json:'JSON',prompt:'Prompt'};
/* ---- portapapeles ---- */
function baseUrl(){var u=D.meta.url_publica||location.href.split('#')[0].split('?')[0].replace(/index\.html$/,'');return u.slice(-1)==='/'?u:u+'/';}
var toast=$('.toast'),tt;function aviso(t){toast.textContent=t;toast.setAttribute('data-v','true');clearTimeout(tt);tt=setTimeout(function(){toast.setAttribute('data-v','false');},2400);}
function copiar(t){if(navigator.clipboard&&window.isSecureContext)return navigator.clipboard.writeText(t);return new Promise(function(ok,no){var a=document.createElement('textarea');a.value=t;a.setAttribute('readonly','');a.style.cssText='position:fixed;opacity:0';document.body.appendChild(a);a.select();try{document.execCommand('copy')?ok():no();}catch(e){no(e);}finally{document.body.removeChild(a);}});}
function hacerCopia(texto,etq){if(!texto){aviso('No hay '+etq+' para este módulo');return;}copiar(texto).then(function(){aviso(etq+' copiado');},function(){aviso('No se pudo copiar: usa «Ver código»');});}
/* ---- código con pestañas ---- */
function pintar(panel,v,tipo){var t=CONT[tipo](v);var pre=$('pre code',panel);pre.innerHTML=tipo==='html'?hl(t):esc(t);panel.setAttribute('data-tipo',tipo);$$('.code__tab',panel).forEach(function(b){b.setAttribute('aria-selected',b.getAttribute('data-tipo')===tipo?'true':'false');});}
document.addEventListener('click',function(e){
  var b=e.target.closest('[data-accion]');if(!b)return;var a=b.getAttribute('data-accion'),demo=b.closest('.demo'),v=demo&&V[demo.getAttribute('data-id')];
  if(a==='copiar'){hacerCopia(CONT[b.getAttribute('data-tipo')](v),ETQ[b.getAttribute('data-tipo')]);}
  else if(a==='codigo'){var p=$('.code',demo),abierto=!p.hidden;p.hidden=abierto;b.setAttribute('aria-expanded',abierto?'false':'true');b.querySelector('.lbl').textContent=abierto?'Ver código':'Ocultar código';if(!abierto&&!p.getAttribute('data-tipo')){pintar(p,v,p.getAttribute('data-primero'));}}
  else if(a==='tab'){pintar($('.code',demo),v,b.getAttribute('data-tipo'));}
  else if(a==='copiar-panel'){var pn=$('.code',demo);hacerCopia(CONT[pn.getAttribute('data-tipo')](v),ETQ[pn.getAttribute('data-tipo')]);}
  else if(a==='css-modulo'){var m=D.modulos.filter(function(x){return x.id===b.getAttribute('data-modulo');})[0];var dl=$('#dlg-css');dl.setAttribute('data-modulo',m.id);$('h3',dl).textContent='CSS del módulo · '+m.n+' '+m.titulo;$('pre code',dl).textContent=(m.tokens&&Object.keys(m.tokens).length?tokensCss(m,':root')+'\n\n':'')+(m.css||'/* Este módulo no define CSS propio: usa los tokens de la página. */');dl.showModal();}
  else if(a==='copiar-css-modulo'){var mm=D.modulos.filter(function(x){return x.id===$('#dlg-css').getAttribute('data-modulo');})[0];hacerCopia((mm.tokens&&Object.keys(mm.tokens).length?tokensCss(mm,':root')+'\n\n':'')+(mm.css||''),'CSS del módulo');}
  else if(a==='cerrar'){$('#dlg-css').close();}
  else if(a==='copiar-url'){hacerCopia(baseUrl(),'URL');}
  else if(a==='copiar-maestro'){hacerCopia((D.maestro||'').split('{URL}').join(baseUrl()),'Prompt maestro');}
  else if(a==='menu'){var r=$('.rail'),o=r.getAttribute('data-open')!=='true';r.setAttribute('data-open',o);$('.scrim').setAttribute('data-open',o);b.setAttribute('aria-expanded',o);}
});
/* ---- menú: activo según scroll, buscador, plegado en móvil ---- */
var items=$$('.rail__i'),ents=items.map(function(a){return {a:a,t:document.getElementById(a.getAttribute('href').slice(1))};}).filter(function(x){return x.t;});
function sync(){var act=ents[0]&&ents[0].t;ents.forEach(function(x){if(x.t.getBoundingClientRect().top<=140)act=x.t;});ents.forEach(function(x){x.a.setAttribute('aria-current',x.t===act?'true':'false');});}
var tick=false;window.addEventListener('scroll',function(){if(!tick){tick=true;requestAnimationFrame(function(){tick=false;sync();});}},{passive:true});window.addEventListener('resize',sync);sync();
$$('.rail__i').forEach(function(a){a.addEventListener('click',function(){var r=$('.rail');r.setAttribute('data-open','false');$('.scrim').setAttribute('data-open','false');var bt=$('.topbar [data-accion=menu]');if(bt)bt.setAttribute('aria-expanded','false');});});
var q=$('#buscar');if(q){q.addEventListener('input',function(){var s=q.value.trim().toLowerCase(),n=0;$$('.rail__l li').forEach(function(li){var ok=!s||li.textContent.toLowerCase().indexOf(s)>-1;li.hidden=!ok;if(ok)n++;});$$('.rail__g').forEach(function(g){var ul=g.nextElementSibling;g.hidden=!$$('li:not([hidden])',ul).length;});$('.rail__vacio').hidden=n>0;});}
document.addEventListener('keydown',function(e){if(e.key==='Escape'){var r=$('.rail');if(r.getAttribute('data-open')==='true'){r.setAttribute('data-open','false');$('.scrim').setAttribute('data-open','false');var bt=$('.topbar [data-accion=menu]');if(bt){bt.setAttribute('aria-expanded','false');bt.focus();}}}});
})();
"""

ICONOS = {
    "html": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m8 7-5 5 5 5M16 7l5 5-5 5"/></svg>',
    "css": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="4" width="16" height="16" rx="3"/><path d="M8 9h8M8 13h5"/></svg>',
    "json": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 4C6 4 6 7 6 9s0 3-3 3c3 0 3 1 3 3s0 5 3 5M15 4c3 0 3 3 3 5s0 3 3 3c-3 0-3 1-3 3s0 5-3 5"/></svg>',
    "prompt": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m12 3 1.8 4.7L18.5 9.5l-4.7 1.8L12 16l-1.8-4.7L5.5 9.5l4.7-1.8zM19 15l.8 2.2L22 18l-2.2.8L19 21l-.8-2.2L16 18l2.2-.8z"/></svg>',
    "ver": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/></svg>',
    "casa": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 18l-6-6 6-6"/></svg>',
    "menu": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>',
}


# ============================================================================ utilidades
def _mezclar(hex_a, hex_b, t):
    a, b = ct.parsear_color(hex_a), ct.parsear_color(hex_b)
    return "#%02X%02X%02X" % tuple(round(a[i] * (1 - t) + b[i] * t) for i in range(3))


def acento_texto_seguro(acento, fondo, minimo=4.5):
    """Oscurece el acento hasta que cumpla `minimo`:1 contra el fondo (texto pequeño). Devuelve (hex, ratio)."""
    cand, t = acento.upper(), 0.0
    while ct.contraste(cand, fondo) < minimo and t < 1:
        t += 0.02
        cand = _mezclar(acento, "#000000", t)
    return cand, ct.contraste(cand, fondo)


def _logo(svg, clase_prefijo="lg"):
    """Quita el prólogo XML y vuelve únicos los estilos de clase para poder incrustar el SVG sin choques."""
    s = re.sub(r"<\?xml[^>]*\?>", "", svg).strip()
    estilos = {}
    for m in re.finditer(r"\.(cls-\d+)\s*\{([^}]*)\}", s):
        estilos[m.group(1)] = " ".join(m.group(2).split())
    s = re.sub(r"<defs>.*?</defs>", "", s, flags=re.S)
    for k, v in estilos.items():
        s = s.replace(f'class="{k}"', f'style="{v}"')
    s = re.sub(r'\s(id|data-name)="[^"]*"', "", s)
    s = s.replace("<svg ", '<svg role="img" aria-label="" focusable="false" ', 1)
    return s


def _json_seguro(obj):
    t = json.dumps(obj, ensure_ascii=False)
    return t.replace("</", "<\\/").replace("<!--", "<\\!--")


def _fuentes_css(fuentes):
    out = ""
    for f in fuentes or []:
        out += (f'@font-face{{font-family:"{f["familia"]}";font-style:normal;font-weight:{f.get("peso", 400)};font-display:swap;'
                f'src:url("{f["url"]}") format("woff2")}}\n')
    return out


def _estado_pill(estado):
    e = (estado or "").lower()
    tono = "ok" if e in ("estable", "pasa") else "mal" if e in ("hallazgo", "falla") else "aviso" if e in ("propuesta", "parcial") else "info"
    return tono


# ============================================================================ render

# ============================================================================ capa para IA (mismo contenido que los botones de la página)
def _tokens_css(m, sel):
    tk = m.get("tokens") or {}
    return sel + " {\n" + "".join(f"  {k}: {v};\n" for k, v in tk.items()) + "}"


def _html_copia(v):
    return v["html_copia"] if v.get("html_copia") is not None else v.get("html", "")


def _css_completo(m, v):
    return ("/* " + m["titulo"] + " · " + v["nombre"] + " */\n" + (_tokens_css(m, ":root") + "\n\n" if m.get("tokens") else "")
            + (m.get("css") or "") + ("\n\n" + v["css"] if v.get("css") else ""))


def _json_de(v):
    return "" if v.get("json") is None else json.dumps(v["json"], ensure_ascii=False, indent=2)


def prompt_de(man, m, v):
    """Prompt para que una IA duplique una variante. Es el MISMO texto que genera el botón «Copiar prompt»."""
    p = [f"Actúa como desarrollador front-end que trabaja DENTRO de un sistema de diseño ya existente ({man['meta']['titulo']})."]
    if man.get("reglas_ia"):
        p.append("Reglas del sistema:\n" + "\n".join("- " + r for r in man["reglas_ia"]))
    p.append(f"Módulo: {m['n']} · {m['titulo']} · variante «{v['nombre']}»" + (f" (uso: {v['uso']})" if v.get("uso") else "") + ".")
    if v.get("json") is not None:
        p.append("Contrato / datos (JSON):\n```json\n" + _json_de(v) + "\n```")
    if v.get("html"):
        p.append("HTML de referencia (real, no lo reinterpretes):\n```html\n" + _html_copia(v) + "\n```")
    if m.get("css") or v.get("css"):
        p.append("CSS del módulo:\n```css\n" + _css_completo(m, v) + "\n```")
    p.append("Tarea: duplica este módulo y adáptalo así → [ESCRIBE AQUÍ QUÉ CAMBIAR: texto, imagen, tamaño, variante nueva…]")
    p.append("Condiciones: usa SOLO las clases y variables CSS de arriba; no inventes colores, medidas ni nombres de props; conserva los estados (hover, foco visible, deshabilitado si existe); respeta el contraste AA. Entrega HTML y CSS, y dime qué NO pudiste verificar.")
    return "\n\n".join(p)


def prompt_maestro(man, base):
    """Prompt que el usuario pega en una IA junto con la URL de la biblioteca: documentar todo y construir a partir de ahí."""
    meta = man["meta"]
    reglas = "\n".join("- " + r for r in man.get("reglas_ia", [])) or "- Usa solo lo que está en la biblioteca."
    return (f"Te doy la URL de la biblioteca de módulos de un sistema de diseño ({meta['titulo']}): {base}\n\n"
            f"1) Lee primero {base}llms.txt y después {base}sistema.json (contiene todos los módulos, tokens, CSS, HTML real y contratos). "
            f"Si no puedes abrir archivos, usa la propia página {base}.\n"
            f"2) DOCUMENTA el sistema: tokens (color, espaciado, forma, tipografía), cada componente con su propósito, estados, props y reglas, "
            f"lo que está marcado como propuesta u hallazgo, y lo que NO está verificado.\n"
            f"3) Reglas que debes respetar al construir:\n{reglas}\n"
            f"4) CONSTRUYE lo que te pida a continuación usando SOLO los módulos y variables del sistema: copia el HTML tal cual y su CSS; "
            f"si algo falta, dilo y propón la pieza nueva sin inventar valores.\n"
            f"5) Termina con una lista de qué comprobaste y qué no.\n\n"
            f"LO QUE QUIERO CONSTRUIR: [ESCRIBE AQUÍ]")


def _base_url(meta):
    u = (meta.get("url_publica") or "").strip()
    return u if not u or u.endswith("/") else u + "/"


def sistema_json(man):
    meta, marca = man["meta"], man["marca"]
    base = _base_url(meta)
    mods = []
    for m in man["modulos"]:
        vs = []
        for v in m["variantes"]:
            vs.append({"id": v["id"], "nombre": v["nombre"], "uso": v.get("uso", ""), "tipo": v.get("tipo", "componente"), "tema": v.get("tema", "Light"),
                       "nota": v.get("nota", ""), "html": _html_copia(v), "css": _css_completo(m, v) if (m.get("css") or v.get("css") or m.get("tokens")) else "",
                       "json": v.get("json"), "prompt": prompt_de(man, m, v)})
        mods.append({"id": m["id"], "n": m["n"], "titulo": m["titulo"], "estado": m.get("estado", ""), "version": m.get("version", ""),
                     "descripcion": m.get("descripcion", ""), "archivo": f"{base}modulos/{m['id']}.json", "ancla": f"{base}#{m['id']}",
                     "tokens": m.get("tokens") or {}, "css": m.get("css") or "", "variantes": vs})
    return {"esquema": "design-system-ia/biblioteca@1", "titulo": meta["titulo"], "version": meta.get("version", ""), "fecha": meta.get("fecha", ""),
            "url": base, "indexable": not meta.get("noindex", True),
            "marca": {"nombre": marca["nombre"], "logo": f"{base}logo.svg", "acento": marca.get("acento"), "tinta": marca.get("tinta"), "fondo": marca.get("fondo"),
                      "fuente_ui": marca.get("fuente_ui", "")},
            "reglas_ia": man.get("reglas_ia", []),
            "como_usar": ["Lee llms.txt y este archivo.", "Documenta tokens, componentes, estados y hallazgos.", "Construye copiando el HTML y el CSS reales de cada variante.",
                          "Declara lo que no se comprobó."],
            "prompt_maestro": prompt_maestro(man, base or "<URL de esta biblioteca>/"), "modulos": mods}


def llms_txt(man):
    meta, base = man["meta"], _base_url(man["meta"])
    t = [f"# {meta['titulo']}", "", f"> {meta.get('descripcion') or meta.get('subtitulo', '')}".rstrip(), "",
         "Biblioteca de módulos de un sistema de diseño, pensada para que una IA la lea, la documente y construya a partir de ella. "
         "Cada módulo trae su HTML real, su CSS real, su contrato en JSON y un prompt listo. Las reglas que debes respetar están en `reglas_ia` de sistema.json.", "",
         "## Empezar aquí", "",
         f"- [Sistema completo (JSON)]({base}sistema.json): todos los módulos, tokens, CSS, HTML, contratos y prompts.",
         f"- [Instrucciones para agentes]({base}AGENTS.md): cómo documentar y construir con esta biblioteca.",
         f"- [Logo de la marca]({base}logo.svg)", "", "## Módulos", ""]
    for m in man["modulos"]:
        t.append(f"- [{m['n']} · {m['titulo']}]({base}modulos/{m['id']}.json): {m.get('descripcion', '')} Estado: {m.get('estado', '')}.")
    t += ["", "## Optional", "", f"- [Página para personas]({base}): la misma información con vista previa, menú y botones de copia."]
    return "\n".join(t) + "\n"


def agents_md(man):
    meta, base = man["meta"], _base_url(man["meta"])
    reglas = "\n".join("- " + r for r in man.get("reglas_ia", []))
    return (f"# {meta['titulo']} · instrucciones para agentes\n\n"
            "Esta carpeta es una biblioteca de módulos. Sirve para dos trabajos: **documentar** el sistema y **construir** a partir de él.\n\n"
            "## Orden de lectura\n\n1. `llms.txt` (índice).\n2. `sistema.json` (todo el contenido; cada módulo también está en `modulos/<id>.json`).\n"
            "3. `index.html` solo si necesitas ver la presentación.\n\n"
            "## Qué hay en cada variante de `sistema.json`\n\n- `html`: el marcado real, para copiar tal cual.\n- `css`: las reglas del módulo y las variables que usa.\n"
            "- `json`: el contrato (o los datos) del módulo.\n- `prompt`: el prompt que usa la persona para duplicar esa variante.\n- `nota`, `estado`: lo que no se verificó y si es propuesta u hallazgo.\n\n"
            f"## Reglas\n\n{reglas}\n\n"
            "## Prompt maestro (la persona lo pega junto con la URL)\n\n```text\n" + prompt_maestro(man, base or "<URL de esta biblioteca>/") + "\n```\n\n"
            "## Límites\n\nLa biblioteca refleja el estado del sistema en su fecha; lo marcado como propuesta no está aprobado. "
            "Sin acceso al código del proyecto no puedes comprobar que el HTML siga siendo el publicado.\n")


def escribir_paquete(man, carpeta, nombre_index="index.html"):
    """Escribe la entrega completa: página para personas + capa para IA. Devuelve la lista de archivos escritos."""
    os.makedirs(os.path.join(carpeta, "modulos"), exist_ok=True)
    sj = sistema_json(man)
    archivos = {
        nombre_index: render(man),
        "sistema.json": json.dumps(sj, ensure_ascii=False, indent=2) + "\n",
        "llms.txt": llms_txt(man),
        "AGENTS.md": agents_md(man),
        "logo.svg": re.sub(r"<\?xml[^>]*\?>", "", man["marca"]["logo_svg"]).strip() + "\n",
    }
    for m in sj["modulos"]:
        archivos[f"modulos/{m['id']}.json"] = json.dumps({"esquema": sj["esquema"], "titulo": sj["titulo"], "reglas_ia": sj["reglas_ia"], "modulo": m}, ensure_ascii=False, indent=2) + "\n"
    for rel, contenido in archivos.items():
        with open(os.path.join(carpeta, rel), "w", encoding="utf-8", newline="\n") as f:
            f.write(contenido)
    return sorted(archivos)


def render(man):
    meta, marca = man["meta"], man["marca"]
    fondo = marca.get("fondo", "#F9FAFB")
    acento = marca.get("acento", "#FF2D46")
    texto_seguro, _ = acento_texto_seguro(acento, fondo)
    acento_f = _mezclar(acento, "#FFFFFF", 0.9)
    tinta = marca.get("tinta", "#0F172A")
    sobre_acento = "#FFFFFF" if ct.contraste("#FFFFFF", texto_seguro) >= 4.5 else tinta
    logo = _logo(marca["logo_svg"]) if marca.get("logo_svg") else ""
    nombre_marca = marca.get("nombre", "")
    logo = logo.replace('aria-label=""', f'aria-label="{esc(nombre_marca)}"')

    css = (CSS.replace("@font-face-placeholder", _fuentes_css(marca.get("fuentes")))
              .replace("%%ACENTO_TEXTO%%", texto_seguro).replace("%%ACENTO_F%%", acento_f).replace("%%ACENTO%%", acento)
              .replace("%%SOBRE_ACENTO%%", sobre_acento).replace("%%TINTA%%", tinta).replace("%%FONDO%%", fondo)
              .replace("%%FUENTE_UI%%", marca.get("fuente_ui", 'system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif'))
              .replace("%%FUENTE_MONO%%", marca.get("fuente_mono", 'ui-monospace,SFMono-Regular,Consolas,"Liberation Mono",monospace'))
              .replace("%%LOGO_ALTO_M%%", str(int(marca.get("logo_alto_movil", max(16, int(marca.get("logo_alto", 22)) - 2))))).replace("%%LOGO_ALTO%%", str(marca.get("logo_alto", 22))))

    modulos = {m["id"]: m for m in man["modulos"]}
    # ---- menú
    rail = ""
    for g in man["grupos"]:
        rail += f'<p class="rail__g" id="g-{esc(g["etiqueta"].lower())}">{esc(g["etiqueta"])}</p><ul class="rail__l">'
        for mid in g["modulos"]:
            m = modulos[mid]
            rail += (f'<li><a class="rail__i" href="#{esc(m["id"])}" aria-current="false"><span class="rail__n">{esc(m["n"])}</span>'
                     f'<span>{esc(m["titulo"])}</span><span class="dot dot--{_estado_pill(m.get("estado"))}" title="{esc(m.get("estado", ""))}"></span></a></li>')
        rail += "</ul>"

    # ---- resumen
    hay_resumen = "resumen" in man
    res = man.get("resumen") or {}
    kp = ""
    for k in res.get("kpis", []):
        barra = f'<div class="kpi__b" aria-hidden="true"><span style="width:{int(k["barra"])}%"></span></div>' if k.get("barra") is not None else ""
        kp += (f'<div class="kpi kpi--{esc(k.get("tono", "info"))}"><div class="kpi__v">{esc(str(k["valor"]))}</div>'
               f'<p class="kpi__e">{esc(k["etiqueta"])}</p><p class="kpi__n">{esc(k.get("nota", ""))}</p>{barra}</div>')
    leyenda = ""
    if res.get("leyenda", True):
        def fila(icono, titulo, desc, extra=""):
            return f'<div><dt><span class="btn {extra}" style="min-height:28px;padding:0 8px;pointer-events:none">{ICONOS[icono]}</span>{esc(titulo)}</dt><dd>{esc(desc)}</dd></div>'
        leyenda = ('<section class="leyenda" aria-labelledby="ley-t"><h2 id="ley-t">Cómo usar cada módulo</h2><dl>'
                   + fila("html", "Copiar HTML", "El marcado real del componente, listo para pegar.")
                   + fila("css", "Copiar CSS", "Las reglas del módulo y las variables que usa.")
                   + fila("json", "Copiar JSON", "El contrato (o los datos) del módulo, legible por una IA.")
                   + fila("prompt", "Copiar prompt", "Un prompt completo con reglas, HTML, CSS y contrato para que una IA lo duplique.", "btn--ia")
                   + fila("ver", "Ver código", "Despliega HTML, CSS, JSON y prompt en pestañas.")
                   + "</dl></section>")
    base_ia = _base_url(meta)
    para_ia = ('<section class="paraia" aria-labelledby="ia-t"><h2 id="ia-t">Para una IA: entrégale esta URL</h2>'
               '<p>Esta biblioteca también es legible por una IA. Con la URL puede <strong>documentar todo el sistema</strong> y <strong>construir a partir de él</strong>, '
               'sin que le copies nada a mano.</p>'
               f'<div class="paraia__url"><code>{esc(base_ia or "(la URL donde publiques esta carpeta)")}</code>'
               f'<button class="btn" type="button" data-accion="copiar-url">Copiar URL</button>'
               f'<button class="btn btn--ia" type="button" data-accion="copiar-maestro">{ICONOS["prompt"]}Copiar prompt maestro</button></div>'
               '<ul class="paraia__l"><li><code>llms.txt</code> · índice</li><li><code>sistema.json</code> · todo el sistema</li>'
               '<li><code>AGENTS.md</code> · instrucciones</li><li><code>modulos/&lt;id&gt;.json</code> · un módulo</li><li><code>logo.svg</code> · logo de la marca</li></ul></section>')
    cuerpo = "" if not hay_resumen else (f'<section class="mod" id="resumen" aria-labelledby="t-resumen"><div class="mod__eye">{esc(res.get("etiqueta", "Resumen"))}</div>'
              f'<div class="mod__head"><div class="mod__tit"><h1 id="t-resumen">{esc(meta["titulo"])}</h1></div></div>'
              f'<p class="mod__desc">{esc(meta.get("subtitulo", ""))}</p><div class="kpis">{kp}</div>{leyenda}{para_ia}</section>')

    # ---- módulos
    datos_mod = []
    for m in man["modulos"]:
        tono = _estado_pill(m.get("estado"))
        cab = (f'<section class="mod" id="{esc(m["id"])}" aria-labelledby="t-{esc(m["id"])}">'
               f'<div class="mod__eye"><span>{esc(m["n"])} · {esc(m["titulo"])} · {len(m["variantes"])} {"variante" if len(m["variantes"]) == 1 else "variantes"}</span></div>'
               f'<div class="mod__head"><div><div class="mod__tit"><h2 id="t-{esc(m["id"])}">{esc(m["titulo"])}</h2>'
               f'<span class="pill pill--{tono}">{esc(m.get("estado", ""))}</span>' + (f'<span class="pill">{esc(m["version"])}</span>' if m.get("version") else "") + "</div>"
               f'<p class="mod__desc">{esc(m.get("descripcion", ""))}</p></div>'
               f'<button class="btn" type="button" data-accion="css-modulo" data-modulo="{esc(m["id"])}">{ICONOS["css"]}Ver CSS del módulo</button></div><div class="vars">')
        vs = ""
        for i, v in enumerate(m["variantes"], 1):
            vid = v["id"]
            tipo = v.get("tipo", "componente")
            tema = (v.get("tema") or "Light")
            chip = f'<span class="chip{" chip--dark" if tema.lower() == "dark" else ""}">{esc(tema)}</span>'
            hay = {"html": bool(v.get("html")), "css": bool(m.get("css") or v.get("css") or m.get("tokens")), "json": v.get("json") is not None, "prompt": True}
            acc = ""
            for t, etq, extra in (("html", "Copiar HTML", ""), ("css", "Copiar CSS", ""), ("json", "Copiar JSON", ""), ("prompt", "Copiar prompt", " btn--ia")):
                if hay[t]:
                    acc += f'<button class="btn{extra}" type="button" data-accion="copiar" data-tipo="{t}">{ICONOS[t]}{etq}</button>'
            primero = next(t for t in ("html", "css", "json", "prompt") if hay[t])
            acc += f'<button class="btn" type="button" data-accion="codigo" aria-expanded="false">{ICONOS["ver"]}<span class="lbl">Ver código</span></button>'
            tabs = "".join(f'<button class="code__tab" role="tab" type="button" data-accion="tab" data-tipo="{t}" aria-selected="false">{ {"html": "HTML", "css": "CSS", "json": "JSON", "prompt": "Prompt"}[t] }</button>' for t in ("html", "css", "json", "prompt") if hay[t])
            ancho = v.get("ancho")
            fit = f' style="max-width:{esc(str(ancho))}{"px" if str(ancho).isdigit() else ""}"' if ancho else ""
            if tipo == "componente":
                prev = ":host{display:block}" + meta.get("base_preview", "") + _tokens_css(m, ":host") + "\n" + (m.get("css") or "") + "\n" + (v.get("css") or "")
                interior = (f'<div class="demo__fit"{fit}><div data-shadow="{esc(vid)}"><template shadowrootmode="open"><style>{prev}</style>'
                            f'{v["html"]}</template></div></div>')
            else:
                interior = f'<div class="demo__fit"{fit}>{v.get("html", "")}</div>'
            clase_stage = "demo__stage" + (" demo__stage--tight" if v.get("escenario") == "tight" else "") + (" demo__stage--doc" if tipo == "doc" else "")
            nota = f'<p class="demo__nota">{esc(v["nota"])}</p>' if v.get("nota") else ""
            vs += (f'<article class="demo" id="{esc(vid)}" data-id="{esc(vid)}"><div class="demo__bar"><span class="demo__i" aria-hidden="true">{i:02d}</span>'
                   f'<div><div class="demo__nom">{esc(v["nombre"])}{chip}</div><div class="demo__uso">{esc(v.get("uso", ""))}</div></div>'
                   f'<div class="demo__acc" role="toolbar" aria-label="Acciones de {esc(v["nombre"])}">{acc}</div></div>'
                   f'<div class="{clase_stage}">{interior}</div>{nota}'
                   f'<div class="code" hidden data-primero="{primero}"><div class="code__bar"><div class="code__tabs" role="tablist" aria-label="Formato">{tabs}</div>'
                   f'<button class="btn" type="button" data-accion="copiar-panel">Copiar</button></div><pre><code></code></pre></div></article>')
        cuerpo += cab + vs + "</div></section>"
        dm = {k: m.get(k) for k in ("id", "n", "titulo", "css", "tokens")}
        dm["variantes"] = [{k: v.get(k) for k in ("id", "nombre", "uso", "html", "html_copia", "css", "json")} for v in m["variantes"]]
        datos_mod.append(dm)

    datos = {"meta": {"titulo": meta["titulo"], "base_preview": meta.get("base_preview", ""), "url_publica": _base_url(meta)}, "reglas_ia": man.get("reglas_ia", []),
             "maestro": prompt_maestro(man, "{URL}"), "modulos": datos_mod}
    robots = '<meta name="robots" content="noindex, nofollow">\n' if meta.get("noindex", True) else ""
    pie = esc(meta.get("pie", ""))
    home = ""
    home_top = ""
    if meta.get("home_url"):
        et = esc(meta.get("home_etiqueta", "Volver al sitio"))
        home = f'<a class="rail__home" href="{esc(meta["home_url"])}">{ICONOS["casa"]}{et}</a>'
        home_top = f'<a class="btn" href="{esc(meta["home_url"])}">{ICONOS["casa"]}{et}</a>' 
    item_resumen = ('<ul class="rail__l"><li><a class="rail__i" href="#resumen" aria-current="true"><span class="rail__n">00</span><span>Resumen</span><span class="dot"></span></a></li></ul>' if hay_resumen else "")
    leyenda_estados = ('<ul class="rail__ley" aria-label="Significado de los puntos"><li><span class="dot dot--ok"></span>Estable</li><li><span class="dot dot--aviso"></span>Propuesta</li>'
                       '<li><span class="dot dot--mal"></span>Hallazgo</li></ul>')
    return f"""<!doctype html>
<html lang="{esc(meta.get("idioma", "es"))}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{robots}<meta name="color-scheme" content="light">
<title>{esc(meta.get("titulo_pagina", meta["titulo"]))}</title>
<meta name="description" content="{esc(meta.get("descripcion", ""))}">
<link rel="alternate" type="application/json" href="{esc(base_ia)}sistema.json" title="Sistema completo (JSON)">
<link rel="alternate" type="text/plain" href="{esc(base_ia)}llms.txt" title="Índice para IA">
<style>{css}</style>
</head>
<body>
<a class="salto" href="#contenido">Saltar al contenido</a>
<div class="topbar"><a class="rail__logo" href="#resumen" aria-label="{esc(nombre_marca)}">{logo}</a><div style="display:flex;gap:8px">{home_top}<button class="btn" type="button" data-accion="menu" aria-expanded="false" aria-controls="rail">{ICONOS["menu"]}Menú</button></div></div>
<div class="scrim" data-open="false"></div>
<div class="app">
<aside class="rail" id="rail" data-open="false" aria-label="Menú de módulos">
<div class="rail__top"><a class="rail__logo" href="#resumen" aria-label="{esc(nombre_marca)}">{logo}</a>
{home}<p class="rail__t">{esc(meta.get("rail_titulo", "Biblioteca del sistema de diseño"))}</p><p class="rail__v">{esc(meta.get("version", ""))}{" · " if meta.get("version") and meta.get("fecha") else ""}{esc(meta.get("fecha", ""))}</p>
<div class="rail__buscar"><label class="sr" for="buscar">Buscar módulo</label><input id="buscar" type="search" placeholder="Buscar módulo…" autocomplete="off"></div></div>
<nav class="rail__nav" aria-label="Módulos">{item_resumen}{rail}<p class="rail__vacio" hidden>Ningún módulo coincide.</p></nav>
<div class="rail__pie">{leyenda_estados}<p>{pie}</p></div>
</aside>
<main class="main" id="contenido"><div class="main__in">{cuerpo}</div></main>
</div>
<dialog id="dlg-css" aria-labelledby="dlg-t"><div class="code__bar"><h3 id="dlg-t">CSS del módulo</h3><button class="btn" type="button" data-accion="copiar-css-modulo">Copiar CSS</button><button class="btn" type="button" data-accion="cerrar">Cerrar</button></div><pre><code></code></pre></dialog>
<div class="toast" role="status" aria-live="polite" data-v="false"></div>
<script type="application/json" id="datos">{_json_seguro(datos)}</script>
<script>{JS}</script>
</body>
</html>
"""


def validar_manifiesto(man):
    errores = []
    for k in ("meta", "marca", "grupos", "modulos"):
        if k not in man:
            errores.append(f"falta «{k}»")
    if errores:
        return errores
    if not (man["marca"].get("logo_svg") or "").strip().startswith(("<svg", "<?xml")):
        errores.append("falta el logo de la marca (marca.logo_svg, texto SVG): la entrega siempre lleva el logo del cliente arriba a la izquierda")
    if not man["marca"].get("nombre"):
        errores.append("falta el nombre de la marca (marca.nombre)")
    ids = [m["id"] for m in man["modulos"]]
    if len(ids) != len(set(ids)):
        errores.append("ids de módulo repetidos")
    vids = [v["id"] for m in man["modulos"] for v in m["variantes"]]
    if len(vids) != len(set(vids)):
        errores.append("ids de variante repetidos")
    enlistados = [i for g in man["grupos"] for i in g["modulos"]]
    for i in enlistados:
        if i not in ids:
            errores.append(f"el grupo menciona el módulo inexistente «{i}»")
    for m in man["modulos"]:
        if m["id"] not in enlistados:
            errores.append(f"el módulo «{m['id']}» no está en ningún grupo del menú")
        if not m["variantes"]:
            errores.append(f"el módulo «{m['id']}» no tiene variantes")
        for v in m["variantes"]:
            if v.get("tipo", "componente") == "componente" and not v.get("html"):
                errores.append(f"la variante «{v['id']}» es de tipo componente y no tiene html")
    return errores


def main(argv=None):
    c.configurar_salida()
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 2:
        print(__doc__)
        return c.SALIDA_USO
    try:
        man = c.leer_json(args[0])
    except Exception as e:  # noqa: BLE001
        print(f"Error de lectura: {e}", file=sys.stderr)
        return c.SALIDA_USO
    errores = validar_manifiesto(man)
    if errores:
        print("Manifiesto inválido:\n  - " + "\n  - ".join(errores), file=sys.stderr)
        return c.SALIDA_HALLAZGOS
    destino = args[1]
    carpeta, nombre = (os.path.dirname(os.path.abspath(destino)), os.path.basename(destino)) if destino.lower().endswith(".html") else (os.path.abspath(destino), "index.html")
    escritos = escribir_paquete(man, carpeta, nombre)
    nvar = sum(len(m["variantes"]) for m in man["modulos"])
    print(f"{carpeta}: {len(man['modulos'])} módulos, {nvar} variantes, {len(escritos)} archivos ({', '.join(escritos[:5])}…).")
    return c.SALIDA_OK


if __name__ == "__main__":
    sys.exit(main())
