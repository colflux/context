# Coherencia entre filtros, puntos del mapa y datos/gráficas del panel

**Estado:** hecho
**Creada:** 2026-09-23
**A cargo:** Viviana
**Sesión de Claude Code:** https://claude.ai/code/session_50fa4b98-a8de-490b-a3d0-a4c879ee8aa9

## Objetivo

En el Mapa Interactivo (`frontend/src/pages/MapaInteractivo.tsx`), los filtros del panel izquierdo (Metodología, Gas, Analizador, Día/Noche, Año, Proyecto, Región, Departamento, Municipio, Vereda) deben producir resultados coherentes entre sí: los puntos/regiones que se ven en el mapa y los datos que trae el resumen geográfico deben reflejar exactamente la misma combinación de filtros.

## Contexto

Diagnóstico inicial (agentes de investigación en frontend y backend): existían 4 fuentes de datos independientes en esta vista que no compartían el set completo de filtros — Mapa/Regiones, Mapa/Sitios (pines), Gráficas y Datos Detallados (estas dos últimas viven en `SiteDetailPanel.tsx`, panel que aparece al clicar un sitio). En particular:

- `/api/geo/sitios/` no aceptaba ningún query param — el frontend filtraba client-side solo por proyecto y gas, ignorando año/departamento/municipio/vereda/región/analizador/día-noche.
- `flujosAnalizadorId` y `flujosCondicionLuzId` ya existían en el store (`useAppStore.ts`) y alimentaban los selects de Analizador/Día-Noche, pero nunca se propagaban a ningún fetch.
- El campo `region` de `GeoResumenFilters` existía en el tipo pero nunca se asignaba.
- Los campos de analizador (`MuestraGEI.analizador` → `Equipo.modelo`) y día/noche (`SubmuestraGEI.condicion_luz`) ya existían en el modelo de backend y ya se usaban como dimensión de agrupación en `/api/geo/resumen-categorico/`, pero no estaban expuestos como filtro en `/api/geo/resumen/`, `/api/geo/series/` ni `/api/geo/sitios/`.

**Por qué importa:** sin esto, un usuario podía filtrar por ejemplo por Departamento X y seguir viendo en el mapa (modo Sitios) puntos de otros departamentos, o elegir un Analizador/Día-Noche sin que eso afectara nada — la razón por la que se abrió esta tarea.

## Qué se hizo

Backend (`/Users/vivianabautista.xyz/colflux/backend/app/api/geo/views.py`):
- `_aplicar_filtros_comunes` (usada por `resumen_geografico` y `resumen_categorico`): agrega filtros `analizador` y `condicion_luz`, solo quando `categoria == "flujos"`.
- `series_co2`: agrega los mismos dos filtros.
- `sitios_geojson`: antes no aceptaba ningún filtro. Ahora acepta `proyecto`, `vereda`, `municipio`, `departamento`, `region` (acotan qué `Sitio` se devuelve) y `desde`, `hasta`, `analizador`, `condicion_luz` (acotan las mediciones usadas para calcular el resumen de cada sitio; `desde`/`hasta` también aplican a biomasa/cos, analizador/condicion_luz solo a flujos).

Frontend (`/Users/vivianabautista.xyz/colflux/frontend`):
- `types/index.ts`: `GeoResumenFilters` gana `analizador`/`condicion_luz`; nuevo tipo `SitiosFilters` (igual a `GeoResumenFilters` sin `categoria`); `SeriesFilters` gana `vereda`/`region`/`analizador`/`condicion_luz`.
- `utils/geoFilters.ts`: `buildGeoResumenBaseFilters` acepta un tercer parámetro opcional con `analizadorId`/`condicionLuzId` (solo aplica si `categoria === 'flujos'`).
- `services/geo.service.ts` + `hooks/useSitios.ts`: `getSitios`/`useSitios` ahora aceptan filtros y los mandan como query params.
- `components/map/GeoMap.tsx`: arma `sitiosFilters` con los mismos filtros geográficos/temporales/analizador/día-noche que ya usaba el choropleth de regiones (`resumenFilters`, que ahora también incluye `region`), y se los pasa a `useSitios`. Se eliminó el filtrado client-side redundante por proyecto (ya lo hace el backend).
- `features/filters/FilterPanel.tsx`: las opciones de Departamento/Municipio/Vereda ahora se acotan también por Región seleccionada (antes `region` no se usaba para nada); `baseGeoFilters` ahora incluye analizador/día-noche.

Verificado con `tsc --noEmit` y `eslint` sobre los archivos tocados (sin errores nuevos) y `ast.parse` sobre el archivo de Python. No se pudo levantar el backend localmente para una verificación end-to-end en navegador porque requiere Postgres vía Docker (`DATABASE_URL` no seteada) — pendiente de que alguien lo pruebe contra un entorno con la base de datos disponible.

## Segunda ronda: Gráficas, Datos Detallados y página de Indicadores

Se retomó la tarea para cerrar el pendiente de "Gráficas y Datos Detallados", y se vinculó con una necesidad relacionada del usuario: la página `/dashboard` ("Indicadores", ícono de barras en el sidebar) no tenía panel de filtros en absoluto, a pesar de tener varias gráficas que dependían implícitamente de filtros globales (`flujosAnalizadorId`/`flujosCondicionLuzId` ya se usaban ahí solo para resaltar barras, no para filtrar).

Diagnóstico (2 agentes de investigación en paralelo, backend + frontend): de los 8 componentes de gráficas de la plataforma, solo 3 (`EmissionTrendChart`, `EmissionBarChart`, `CategoricalChart`) pegaban a endpoints ya coherentes (`/api/geo/series/`, `/api/geo/resumen-categorico/`, `/api/geo/resumen/`); los otros 5 (`BiomasaProduccionScatter`, `CosProfundidadChart`, `BiomasaTaxonChart`, `InstalacionTrendChart`, `MomHojarascaChart`) pegan a `/api/reportes/*` y `/api/geo/tendencia-instalacion/`, que solo aceptaban `proyecto`/`sitio` (o ni eso). Aparte, `/api/proyectos/{id}/datos/` (Datos Detallados) no tenía filtro de fecha ni geográfico, solo el genérico `filtros` (JSON, matching `icontains` por columna) y `sitio` (match exacto).

### Qué se hizo

Backend:
- `app/api/reportes/views.py`: nuevo helper `_aplicar_filtros_geo` (proyecto/sitio/vereda/municipio/departamento/region/fecha, parametrizado por la cadena de FKs de cada modelo), aplicado a `biomasa_por_taxon` (antes sin ningún filtro), `biomasa_produccion`, `cos_por_profundidad` y `mom_tendencia` (esta última también gana filtro por `sitio`, que no tenía).
- `app/api/geo/views.py`: `tendencia_instalacion` gana filtros `sitio`/`vereda`/`municipio`/`departamento`/`region` (sin `desde`/`hasta` — su propio eje ya es la fecha de instalación).
- `app/api/etl/views.py` (`datos_proyecto` / `_preparar_vista_pks`): nuevo parámetro `geo_filtros` (vereda/municipio/departamento/region/desde/hasta) genérico para las 6 vistas desnormalizadas, reutilizando la ruta a `Sitio` que la función ya calculaba para el filtro exacto de `sitio_id`. `desde`/`hasta` solo se aplican si el modelo base de la vista tiene un campo `fecha` propio (se detecta dinámicamente, no todas lo tienen — ej. `unidad_muestreo` usa `fecha_instalacion`).

Frontend:
- Nuevo tipo `ReporteGeoFilters` (`types/index.ts`) y nuevo hook compartido `hooks/useGlobalFilters.ts` con `useReporteFiltros()` (geográficos/proyecto/año, para biomasa/cos/mom/instalación) y `useFlujosFiltros()` (lo mismo + gas/analizador/día-noche, para series/resumen/resumen-categorico). Evita repetir 5 veces la misma lectura del store.
- `services/reportes.service.ts`, `services/geo.service.ts` (`getTendenciaInstalacion`): firmas actualizadas para aceptar `ReporteGeoFilters`.
- Hooks `useBiomasaProduccion`, `useCosPorProfundidad`, `useBiomasaPorTaxon`, `useTendenciaInstalacion`, `useMomTendencia`, `useSeries`: ahora arman sus filtros mezclando el store (vía los hooks de arriba) con overrides explícitos (ej. `{ sitio: sitioId }`) — antes solo aceptaban `proyecto`/`sitio` posicionales.
- `EmissionTrendChart`, `BiomasaProduccionScatter`, `CosProfundidadChart` (usadas dentro de `SiteDetailPanel`) heredan el fix automáticamente, sin tocarlas, porque ahora sus hooks leen el store solos.
- `pages/DashboardIndicadores.tsx`: se agregó `<FilterPanel />` en un `<aside>` (mismo componente que usa el mapa, confirmado sin acoplamiento al layout del mapa) con posición `sticky`; todas las `CategoricalChart` (región/ecosistema/estado_conservación/analizador/día-noche) y `EmissionBarChart` ahora reciben `filters` armados con `useFlujosFiltros()` (excluyendo la propia dimensión que grafican, para no colapsar la barra seleccionada a sí misma); "Sitios monitoreados" y "Cobertura de datos" también quedan acotados por los mismos filtros.
- `components/detalle/SiteDetailPanel.tsx` (Datos Detallados): ahora manda `desde`/`hasta` (derivados del filtro "Año") en todas las vistas, y fuerza `SubmuestraGEI.condicion_luz` (vía el mecanismo genérico de `filtros`, igual que ya se hacía con el gas) cuando la pestaña es CO2/CH4 y hay un Día/Noche seleccionado.

Verificado con `tsc --noEmit` (sin errores) y `eslint` sobre todo `src/` (mismos 11 problemas preexistentes que ya había antes de esta sesión, en archivos no tocados — ninguno nuevo) y `ast.parse` sobre los 3 archivos de Python tocados. Sigue sin poder probarse end-to-end en navegador por falta de Postgres local.

### Analizador en Datos Detallados (cerrado en una tercera pasada)

El salto id→nombre se resolvió: `SiteDetailPanel.tsx` ahora también pide `useResumenCategorico('analizador', {}, flujosAnalizadorId != null)` (misma fuente que ya usa `FilterPanel` para poblar el selector), resuelve el `nombre` (ej. "Picarro G4301") a partir del `flujosAnalizadorId` del store, y lo manda como filtro genérico `"Equipo.modelo"` (`icontains`, igual mecanismo que gas/día-noche) cuando la pestaña activa es CO2/CH4. También se ocultó el input de esa columna cuando el filtro está forzado, y se propagó al chequeo de pestañas visibles (`tabsConDatos`).

### Qué queda pendiente

- Los dropdowns "Analizador" y "Día/Noche" en `FilterPanel.tsx` siguen sin acotarse entre sí ni por Departamento/Municipio/Vereda/Región (muestran todos los valores posibles). Menor prioridad.
- No se verificó en navegador (requiere Postgres vía Docker, no disponible en esta sesión).

## Referencias

- Vistas afectadas: `frontend/src/pages/MapaInteractivo.tsx` y `frontend/src/pages/DashboardIndicadores.tsx`
- Screenshots originales: panel de "Datos Detallados" en el mapa (Metodología=Flujos de GEI, Gas=CO2, Analizador=Picarro G4301, Día/Noche=Noche, Año=2025) y la página de Indicadores sin panel de filtros.

## Historial

| Fecha | Descripción |
|---|---|
| 2026-09-23 | Se crea la tarea, se diagnostica con 2 agentes de investigación (frontend + backend) y se implementa el fix de coherencia para mapa/puntos/choropleth. Gráficas y Datos Detallados quedan pendientes. |
| 2026-09-23 | Segunda ronda: se cierra el pendiente de Gráficas y Datos Detallados, y se extiende el mismo `<FilterPanel />` a la página de Indicadores (`/dashboard`), incluyendo los 5 endpoints de reportes que antes no tenían filtros geográficos/temporales. |
| 2026-09-23 | Tercera ronda: se resuelve el filtro de Analizador en Datos Detallados (desajuste id↔nombre, resuelto vía `useResumenCategorico`). Queda solo pendiente verificar en navegador (requiere Postgres) y, como mejora menor, acotar entre sí los dropdowns Analizador/Día-Noche del panel de filtros. |
