# F31 — Mapas temáticos automáticos

**Categoría:** Visualización y Reportes

## Objetivo

Generar heatmaps y mapas cloropléticos de forma automática, exportables en PNG, PDF y
SVG.

## Contexto

Complementa al geoportal ([F01](../geoportal/f01-mapa-carbono-nacional.md)) con salidas
pensadas para compartir fuera de la plataforma.

## Qué hay

Hay mapa coroplético implementado con `maplibre-gl`:
`frontend/src/components/map/GeoMap.tsx` (funciones `syncChoropleth`,
`removeChoropleth`, fuente `resumen-choropleth`) y
`frontend/src/components/map/ChoroplethLegend.tsx` para la leyenda.

## Qué hace falta

No hay heatmaps (solo coropléticos), y no se encontró ninguna librería de exportación
(`jspdf`, `html2canvas`, `file-saver`) ni funcionalidad de exportar el mapa a PNG/PDF/SVG
en el código actual.
