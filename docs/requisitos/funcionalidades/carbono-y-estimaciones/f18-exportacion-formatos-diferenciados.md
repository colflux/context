# F18 — Exportación en formatos diferenciados

**Categoría:** Carbono y Estimaciones

## Objetivo

Exportar datos tabulares en CSV/Excel y datos geoespaciales en Shapefile, GeoJSON y
GeoTIFF, según el tipo de dato.

## Contexto

Cada tipo de dato (tabular vs. geoespacial) necesita un formato de salida distinto para
ser útil fuera de la plataforma.

## Qué hay

Exportación tabular a Excel implementada y funcionando: `exportar_carga`/
`exportar_proyecto` (`backend/app/api/etl/views.py:3593,3639`) generan `.xlsx`
multi-hoja con `pandas.ExcelWriter`/`openpyxl`, descargado desde el frontend vía
`downloadFile` (`frontend/src/utils/download.ts:7-36`) y componentes
`BotonExcel.tsx`/`BotonDescarga.tsx`. GeoJSON existe como formato de **respuesta de
API** para mapas (`sitios_geojson`, `backend/app/api/geo/views.py:113`), no como
exportación descargable de archivo. `FuenteDatos.TIPO_CHOICES`
(`backend/app/models/datos.py:144-150`) reconoce `shapefile`/`geojson` solo como tipos
de **entrada** (ETL de carga), no de salida.

## Qué hace falta

- No hay endpoint de exportación a CSV, Shapefile ni GeoTIFF.
- GeoJSON no se ofrece como descarga de archivo (solo como payload de API para el
  mapa).
- Toda la exportación "de archivo" real está limitada hoy a un único formato (Excel).
