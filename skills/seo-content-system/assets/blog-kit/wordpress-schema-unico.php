<?php
/**
 * Plugin Name: Schema en un solo bloque (fusión con Rank Math)
 * Description: Funde los nodos de schema que el artículo trae en su cuerpo (un bloque <script type="application/ld+json" data-schema="unico">
 *              con @graph: FAQPage, VideoObject…) dentro del único @graph que emite Rank Math y quita ese bloque del cuerpo.
 *              Resultado: cada entrada tiene UN solo script JSON-LD (regla obligatoria de seo-content-system).
 *
 * INSTALAR = CAMBIO EN VIVO: copiar a wp-content/mu-plugins/ solo con aprobación escrita del dueño del sitio; respaldo = no hay nada que
 * respaldar (archivo nuevo); reversión = borrar el archivo (el cuerpo vuelve a mostrar su bloque).
 *
 * Cómo funciona
 *  1) Filtro `rank_math/json_ld`: Rank Math arma un array de entidades indexado por clave y lo imprime como un @graph. Se lee el
 *     contenido CRUDO de la entrada, se busca el bloque marcado y se añaden sus nodos a ese array (sin duplicar @id).
 *     Los nodos traen `isPartOf: {"@id": "{url}#webpage"}`, que apunta al WebPage de Rank Math.
 *  2) Filtro `the_content` (prioridad 99): quita del HTML mostrado el bloque marcado para que no salga un segundo script.
 * Solo actúa en entradas individuales. Si Rank Math no está activo, no hace nada. Con otro plugin de SEO hay que cambiar el filtro
 * del paso 1 (Yoast: `wpseo_schema_graph_pieces`).
 * Después de instalarlo: `python scripts/check_schema_single_block.py <URL de una entrada>` debe dar PASA, y probar en el
 * «Prueba de resultados enriquecidos» de Google que FAQPage y VideoObject siguen detectándose.
 */
if (!defined('ABSPATH')) { exit; }

const SCHEMA_UNICO_RE = '~<script\b[^>]*type=["\']application/ld\+json["\'][^>]*data-schema=["\']unico["\'][^>]*>(.*?)</script>~is';

add_filter('rank_math/json_ld', function ($data, $jsonld) {
    if (!is_singular('post')) { return $data; }
    $post = get_post();
    if (!$post || !preg_match(SCHEMA_UNICO_RE, $post->post_content, $m)) { return $data; }
    $json = json_decode(html_entity_decode($m[1], ENT_QUOTES | ENT_HTML5, 'UTF-8'), true);
    if (!is_array($json) || empty($json['@graph']) || !is_array($json['@graph'])) { return $data; }
    $ya = [];
    foreach ($data as $nodo) { if (is_array($nodo) && !empty($nodo['@id'])) { $ya[$nodo['@id']] = true; } }
    foreach ($json['@graph'] as $nodo) {
        if (!is_array($nodo) || empty($nodo['@id']) || isset($ya[$nodo['@id']])) { continue; }
        $tipo = isset($nodo['@type']) && is_string($nodo['@type']) ? $nodo['@type'] : 'nodo';
        $data['schema_unico_' . $tipo] = $nodo;
        $ya[$nodo['@id']] = true;
    }
    return $data;
}, 99, 2);

add_filter('the_content', function ($contenido) {
    return is_singular('post') ? preg_replace(SCHEMA_UNICO_RE, '', $contenido) : $contenido;
}, 99);
