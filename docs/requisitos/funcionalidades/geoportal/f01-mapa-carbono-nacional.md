# F01 — Mapa de carbono nacional interactivo

**Categoría:** Geoportal

## Objetivo

Visualizar datos de carbono en un mapa nacional interactivo.

## Contexto

El catálogo original dejó pendiente: ¿niveles de visualización (calor, puntos,
regiones)?

## Qué hay

Implementado con MapLibre GL (`frontend/package.json`,
`frontend/src/components/map/GeoMap.tsx`), montado en
`frontend/src/pages/MapaInteractivo.tsx`. El backend sirve GeoJSON a 5 niveles
(sitio/vereda/municipio/departamento/región) vía `app/api/geo/views.py:113-317`
(`sitios_geojson`, puntos) y `views.py:496-685` (`resumen_geografico`, polígonos).
Visualización real: choropleth (polígonos, `GeoMap.tsx:261-283`) y puntos/markers
(`GeoMap.tsx:352-409`), con drill-down departamento→municipio→vereda→sitio.

## Qué hace falta

No hay heatmap ni clustering de puntos, ni en backend ni en frontend — "heatmap" solo
aparece como comentario docstring en `app/api/geo/views.py:504`. Los niveles de
visualización reales son solo 2 (puntos y regiones/choropleth), no 3.
