# Panel de detalle de sitio: varias gráficas para Flujos

**Estado:** implementado, pendiente de validación visual con datos reales
**Creada:** 2026-09-24
**A cargo:** Viviana
**Sesión de Claude Code:** <https://claude.ai/code/session_xxxxx — actualizar
cada vez que una sesión nueva retoma la tarea; borrar/marcar "cerrada" si la
sesión ya no es recuperable>

## Objetivo

Hoy el tab "Gráficas" del panel de detalle de sitio (`SiteDetailPanel.tsx`, categoría `flujos`) muestra una sola serie de tiempo (`EmissionTrendChart.tsx`), porque el gas, la condición de luz y el analizador ya vienen aplicados como filtro global antes de llegar al gráfico. Se quiere ampliar esa sección a varias gráficas que aprovechen los ejes de datos que ya existen, para dar más contexto sin depender solo del filtro global.

## Contexto

Revisión hecha en sesión 2026-09-24 sobre `frontend/src/components/detalle/SiteDetailPanel.tsx` y `frontend/src/components/charts/EmissionTrendChart.tsx` + `frontend/src/hooks/useSeries.ts`. El backend de series (`/api/series` vía `geoService.getSeries`) ya soporta filtrar por `gas`, `condicion_luz` y `analizador`, y existe una vista `clima` separada con variables meteorológicas del sitio.

## Plan

- [x] Propuesta 1 — CO2 vs CH4 en paralelo: implementada y luego retirada (ver Historial).
- [x] Propuesta 2 — Día vs noche (condición de luz): implementada y luego retirada.
- [x] Propuesta 3 — Comparación por analizador/equipo: implementada y luego retirada.
- [x] Propuesta 4 — Flujo vs. variable climática: `FlujoClimaChart.tsx` (eje dual, cruza `/api/geo/series/` con la vista `clima` de `MuestraAmbiental` vía `/api/proyectos/<id>/datos/`). Es la única que quedó en el panel final.
- [x] Propuesta 5 — Resumen mensual (promedio + rango min-máx): implementada y luego retirada.
- [ ] Validar visualmente con datos reales en el navegador (no se pudo levantar el backend con datos en esta sesión) y con el equipo.

## Entregables

Las 5 propuestas se implementaron primero en un panel con pestañas (`FlujosGraficasPanel.tsx`) y luego, apiladas todas en una sola vista. Después de ver el resultado, se decidió que ocupaba demasiado espacio: se retiraron CO2 vs CH4, Día vs noche, Por analizador y Resumen mensual (se borraron sus componentes), dejando solo **Flujo vs. clima** junto a la tendencia original (`EmissionTrendChart.tsx`, que respeta el filtro global de gas/día-noche/analizador). El gráfico de clima quedó en tamaño compacto (130px de alto) para no agrandar la sección.

Cambio de backend que se mantiene aunque ya no se use para las 3 gráficas retiradas: `/api/geo/series/` (`series_co2` en `backend/app/api/geo/views.py`) ahora también devuelve `condicion_luz`, `analizador_id` y `analizador` en cada registro. No se revirtió porque no genera ningún problema y puede servir si se retoma alguna de esas gráficas más adelante -queda como referencia en `SerieLectura` (`frontend/src/types/index.ts`)-.

Verificado tras cada iteración: `tsc --noEmit` y `vite build` sin errores; `eslint` no introduce errores nuevos. Falta abrir la app con datos reales y confirmar visualmente el gráfico de clima (esta sesión no tenía el backend con base de datos disponible).

## Referencias

- `frontend/src/components/detalle/SiteDetailPanel.tsx`
- `frontend/src/components/charts/FlujosGraficasPanel.tsx`
- `frontend/src/components/charts/EmissionTrendChart.tsx`
- `frontend/src/components/charts/FlujoClimaChart.tsx`
- `frontend/src/hooks/useSeries.ts`
- `backend/app/api/geo/views.py` (`series_co2`)

## Historial

| Fecha | Descripción |
|---|---|
| 2026-09-24 | Se crea la tarea con 5 propuestas de gráficas adicionales para el panel de detalle, pendientes de validar con el equipo. |
| 2026-09-24 | Se implementan las 5 propuestas en un solo panel (`FlujosGraficasPanel.tsx`), con un cambio de backend en `/api/geo/series/` para exponer `condicion_luz` y `analizador` por registro. Falta validación visual con datos reales. |
| 2026-09-24 | Se ajusta el panel a pedido: todas las gráficas apiladas en una sola sección (sin pestañas). Luego, por espacio, se retiran CO2 vs CH4, Día vs noche, Por analizador y Resumen mensual (se borran esos componentes); queda solo Flujo vs. clima en tamaño compacto junto a la tendencia original. Falta validación visual con datos reales. |
