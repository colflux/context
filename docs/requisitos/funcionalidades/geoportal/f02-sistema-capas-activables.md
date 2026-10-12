# F02 — Sistema de capas activables

**Categoría:** Geoportal

## Objetivo

Checkbox por capa (carbono, biodiversidad, satélite, imágenes satelitales), con
transparencia ajustable y leyenda dinámica según capas activas.

## Contexto

Pensado para que el usuario combine capas libremente, no solo alterne entre vistas
mutuamente excluyentes.

## Qué hay

Leyenda dinámica funcional en `frontend/src/components/map/ChoroplethLegend.tsx:12-37`
(selector de métrica + gradiente). Hay toggles binarios: Mapa/Satélite
(`GeoMap.tsx:450-473`) y Sitios/Regiones (`GeoMap.tsx:475-498`).

## Qué hace falta

No existe un sistema de checkboxes independientes por capa (carbono, biodiversidad,
satélite como capas superponibles); son toggles mutuamente excluyentes, no activables
en combinación. La opacidad es fija (`fill-opacity: 0.75`, `GeoMap.tsx:265`), sin
control de usuario. No hay capa de biodiversidad ni de imágenes satelitales reales (el
"satélite" es solo el basemap, no una capa de datos propia) — el backend no tiene nada
de biodiversidad/satelital/Earth Engine.
