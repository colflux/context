# F13 — Descarga de datos de flujo filtrable

**Categoría:** Datos y Carga

## Objetivo

Descargar datos de flujo filtrados por unidad experimental, proyecto y zona geográfica.

## Contexto

El catálogo original dejó pendiente: ¿"proyecto" es una entidad propia del modelo de
datos?

## Qué hay

Sí implementado y filtrable. Endpoints
`exportar_carga`/`exportar_proyecto`/`datos_proyecto`/`datos_carga`
(`app/api/etl/views.py:3426-3677`, rutas en `app/api/urls.py:63-68`) generan un Excel
descargable con una hoja por tipo de dato (Flujos CO2/CH4, MOM, COS, Biomasa, Unidad
Muestreo-Experimental). `_preparar_vista_proyecto` filtra explícitamente por
`proyecto_id` (vía cadena de FKs hasta `UnidadExperimental.proyecto`) y acepta
`sitio_id` y `geo_filtros` adicionales (`_aplicar_filtros_vista`), cubriendo filtro por
proyecto, sitio/unidad experimental y zona geográfica. En frontend,
`BotonDescarga.tsx` restringe la descarga a niveles `reportador`/`admin` vía el chat de
IA.

## Qué hace falta

"Proyecto" es, confirmado, una entidad propia del modelo de datos: `Proyecto` en
`app/models/proyecto.py` (con `escala_espacial`, `UnidadExperimental` relacionada,
instituciones y usuarios M2M). No se identificó un endpoint de descarga de datos crudos
"de flujo" standalone fuera del contexto de un proyecto/carga específica; la descarga
siempre cuelga de `proyecto_id` o `carga_id` — falta un endpoint de exportación
"global" con filtros libres de unidad experimental + zona sin pasar por un proyecto.
