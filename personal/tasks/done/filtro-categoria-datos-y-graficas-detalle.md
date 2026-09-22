# Filtrar el mapa por categoría de dato (Flujos/Biomasa/COS) en vez de por gas, y agregar pestaña de gráficas al detalle de sitio

**Estado:** hecho
**Creada:** 2026-09-21
**A cargo:** Viviana
**Sesión de Claude Code:** https://claude.ai/code/session_01TYg7etVaMiGXYvKYJuMYyQ

## Objetivo

Hoy el filtro principal del mapa (`FilterPanel`) es "Gas" (CO2/CH4/N2O), porque
todo el pipeline geo (`/api/geo/sitios`, `/api/geo/series`, `/api/geo/resumen`)
solo agrega datos de flujo de GEI (`MuestraGEI`). La idea de Viviana es que el
filtro de primer nivel sea la **categoría/metodología de dato** — Flujos,
Biomasa, COS (carbono orgánico del suelo), y potencialmente más — y que el
mapa (choropleth, resumen, pines) se recalcule según esa categoría. Dentro de
"Flujos" seguiría existiendo el sub-filtro por gas que ya existe hoy.

Adicionalmente, en el panel de detalle de un sitio (el que se abre con "Ver
detalle" — `SiteDetailPanel.tsx`), agregar una pestaña "Gráficas" que muestre
visualizaciones (no solo la tabla cruda actual) de los datos filtrados, según
la metodología/categoría seleccionada.

## Contexto

- El backend **sí tiene** modelos para las otras categorías —
  `backend/app/models/biomasa.py` (`MuestraBiomasa`, `IndividuoArboreo`) y
  `backend/app/models/suelo.py` (`CaracterizacionMuestreoSuelo`,
  `MonitoreoSuelo` con `tipo_monitoreo="COS"`) — pero **ninguno de los dos se
  expone hoy por `backend/app/api/geo/views.py`**. Ese archivo (622 líneas)
  está construido enteramente alrededor de `MuestraGEI`/gas
  (`resumen_por_sitio_y_gas`, filtros `?gas=`, etc.). Este es el bloqueador
  principal de alcance: no es solo un cambio de UI, hay que decidir y
  construir la agregación geográfica de biomasa y COS en el backend primero.
- En frontend, el modelo de datos también es 100% "gas-céntrico":
  `GasType`, `FilterState.gas`, `SitioProperties.resumen_por_gas`,
  `GAS_COLORS`/`GAS_LABELS` en `frontend/src/utils/formatters.ts`. Cambiar el
  filtro implica generalizar estos tipos a algo como una "categoría de dato"
  con sub-opciones (Flujos → gas; Biomasa/COS → sin sub-filtro, o con su
  propio: profundidad de perfil, protocolo, etc.).
- Captura de referencia visual que pasó Viviana (mockup, no estado actual):
  arriba del filtro de Gas se ve un selector tipo chips numerados
  "2 Flujos", "3 COS — Carbono orgánico en suelo" (y aparentemente "1" con
  un color, cortado en la imagen — probablemente Biomasa).
- El panel de detalle (`frontend/src/components/detalle/SiteDetailPanel.tsx`)
  hoy tiene pestañas `CO2`, `CH4`, `Unidad de Muestreo/Experimental`, `Clima`
  (`DETALLE_TABS`), todas mostrando la misma tabla cruda vía
  `datosService.getDatosProyecto`. No hay gráficas ahí — las gráficas que sí
  existen (`EmissionBarChart`, `EmissionTrendChart`, `CategoricalChart` en
  `frontend/src/components/charts/`) viven en el panel lateral general del
  mapa, no en el detalle de sitio, y también son 100% de gas/flujos.

## Plan

- [x] **Diseño de datos (backend):** decidir cómo se agregan biomasa y COS
      por sitio/región, análogo a `resumen_por_sitio_y_gas` en
      `app/api/geo/views.py` (¿`prom_tonc_ha` de `MuestraBiomasa` agregado
      por sitio? ¿último valor de COS por `MonitoreoSuelo`?). Validar con
      Viviana qué métricas resumen cada categoría antes de programar.
- [x] **Backend:** extender `sitios_geojson`, `resumen_geografico` (y
      quizás `series_co2`) para aceptar un parámetro de categoría
      (`?categoria=flujos|biomasa|cos`) y devolver el resumen correspondiente,
      sin romper los consumidores actuales (gas sigue siendo el default /
      sub-filtro de "flujos").
- [x] **Frontend — tipos y estado:** generalizar `GasType`/`FilterState` a
      una categoría de dato (`frontend/src/types/index.ts`,
      `frontend/src/store/useAppStore.ts`), manteniendo el gas como
      sub-filtro solo visible cuando la categoría es "Flujos".
- [x] **Frontend — `FilterPanel.tsx`:** reemplazar/anteponer el selector de
      Gas por el selector de categoría (chips o similar al mockup), y ajustar
      el resumen (`EmissionSummary.tsx`) y el choropleth (`GeoMap.tsx`) para
      que lean el dato de la categoría activa en vez de asumir siempre gas.
- [x] **Frontend — pestaña "Gráficas" en `SiteDetailPanel.tsx`:** agregar una
      pestaña que renderice gráficas (reusar patrones de
      `EmissionTrendChart`/`CategoricalChart`) con los datos de la
      metodología y filtros activos del sitio seleccionado, en vez de solo
      la tabla. Definir con Viviana qué gráficas tienen sentido por
      categoría (ej. Flujos → tendencia temporal por gas; Biomasa → TonC/ha
      por individuo/fecha; COS → por profundidad de perfil).
- [x] Probar en navegador (claro/oscuro) el flujo completo: elegir categoría
      → mapa y resumen se actualizan → abrir detalle de un sitio → pestaña
      Gráficas muestra algo coherente con la categoría elegida.

## Entregables

- **Backend (commits previos, ya en `main`):** `52e3a09` generaliza
  `resumen_geografico` (`app/api/geo/views.py`) a `?categoria=flujos|biomasa|cos`
  vía el diccionario `_CATEGORIA_CONFIG`, y agrega `resumen_biomasa`/`resumen_cos`
  a cada sitio en `sitios_geojson`. Commit `4a3547a` en `frontend` generaliza
  `GasType`→`CategoriaDato`/`Metodologia`, `FilterPanel.tsx` (selector de
  Metodología reemplaza al de Gas como filtro principal, Gas queda como
  sub-filtro solo de "Flujos"), y `GeoMap.tsx` (choropleth/pines coloreados
  según la categoría activa).
- **Backend (esta sesión, sin commit):** `backend/app/api/reportes/views.py`
  — se agregó `?sitio=` a `biomasa_produccion` y `cos_por_profundidad` (antes
  solo filtraban por `?proyecto=`), necesario para poder graficar un sitio
  puntual en el panel de detalle.
- **Frontend (esta sesión, sin commit):** pestaña "Gráficas" en
  `SiteDetailPanel.tsx`, arriba de "Datos detallados", que renderiza según la
  metodología activa: `EmissionTrendChart` (flujos, tendencia por gas),
  `BiomasaProduccionScatter` (biomasa, producción vs. fecha) o
  `CosProfundidadChart` (COS, % carbono por rango de profundidad) — los tres
  componentes se extendieron con una prop opcional `sitioId` para poder
  acotar sus hooks (`useSeries`, `useBiomasaProduccion`,
  `useCosPorProfundidad`) al sitio seleccionado en vez de traer todo el
  dataset.
- Verificado en navegador (Docker, datos reales de RDS): al reiniciar
  `backend-web-1` (gunicorn no tiene `--reload`, hace falta `docker compose
  restart web` tras cambios de código) se confirmó `GET
  /api/reportes/biomasa/produccion/?sitio=152` → `count: 0` (sitio sin datos
  de biomasa, coincide con "Sin datos" en la UI) vs. `?sitio=173` → `count:
  49`; mismo patrón confirmado para `/api/reportes/cos/` y
  `/api/geo/series/`.

## Referencias

- `backend/app/api/geo/views.py` — toda la agregación geográfica actual (gas-céntrica).
- `backend/app/models/biomasa.py`, `backend/app/models/suelo.py` — datos de biomasa y COS aún no expuestos por la API geo.
- `frontend/src/features/filters/FilterPanel.tsx` — filtro actual por Gas.
- `frontend/src/components/map/GeoMap.tsx` — choropleth y pines, hoy coloreados por `filters.gas`.
- `frontend/src/components/detalle/SiteDetailPanel.tsx` — panel de "Ver detalle", pestañas actuales (`DETALLE_TABS`).
- `frontend/src/components/charts/` (`EmissionBarChart.tsx`, `EmissionTrendChart.tsx`, `CategoricalChart.tsx`) — gráficas existentes a reusar/adaptar para la pestaña nueva.
- Mockup de referencia pasado por Viviana en esta sesión (chips de categoría sobre el filtro de Gas).

## Historial

| Fecha | Descripción |
|---|---|
| 2026-09-21 | Se crea la tarea a partir de una idea de Viviana: cambiar el filtro del mapa de "por gas" a "por metodología/categoría de dato" (Flujos/Biomasa/COS), y agregar una pestaña de gráficas al panel de detalle de sitio según la metodología y datos filtrados. Se investiga el estado actual en `backend` (API geo 100% gas-céntrica; biomasa y COS existen como modelos pero no se exponen geográficamente) y `frontend` (tipos, `FilterPanel`, `GeoMap`, `SiteDetailPanel`, componentes de gráficas existentes). Queda en backlog: requiere diseño de agregación en backend antes de tocar UI. |
| 2026-09-21 | Sesión completa el alcance: (1) backend — `resumen_geografico`/`sitios_geojson` generalizados a `?categoria=` (commit `52e3a09`, hecho en otra sesión/ventana en paralelo); (2) frontend — `Metodología` reemplaza a `Gas` como filtro principal, mapa/choropleth ya leen la categoría activa (commit `4a3547a`, ídem); (3) esta sesión agrega la pestaña "Gráficas" al `SiteDetailPanel.tsx` (flujos/biomasa/COS según metodología), con soporte de `?sitio=` nuevo en `/api/reportes/biomasa/produccion/` y `/api/reportes/cos/` para poder acotar esas gráficas a un solo sitio — verificado en Docker con datos reales de RDS. Cambios de esta sesión (backend `app/api/reportes/views.py` + los archivos de frontend listados en Entregables) quedan **sin commit**, a la espera de que Viviana lo pida explícitamente. Tarea se mueve a `done/`. |
