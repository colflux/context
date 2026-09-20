# Deshabilitar temporalmente la página de Insights (IA)

**Estado:** cerrada
**Creada:** 2026-09-18
**Cerrada:** 2026-09-20

## Objetivo

Deshabilitar la página "Insights" (`/insights` en `frontend`) mientras se
define el análisis real — hoy muestra datos de ejemplo hardcodeados
(análisis inteligente, predicción a 2030) que no deben quedar expuestos
como si fueran reales.

## Plan

- [x] Retirar la ruta `/insights` de `App.tsx`
- [x] Mover "Insights" de `ITEMS` a `SOON_ITEMS` en `AppSidebar.tsx`
      (mismo patrón "próximamente" que Sensores/Capas/Descargas/Favoritos:
      atenuado, sin link activo)
- [x] Quitar `/insights` de `SIDEBAR_ROUTES` en `AppLayout.tsx`
- [x] Dejar `InsightsIA.tsx` intacto para reactivarlo cuando el análisis
      real esté listo

## Entregables

PR [colflux/frontend#20](https://github.com/colflux/frontend/pull/20),
mergeado a `main`. Cambio aislado en rama nueva desde `main` (sin mezclar
con el trabajo en curso de `feat/reportes-modulo-graficas`). `tsc -b &&
vite build` limpios antes del merge.

## Historial

| Fecha | Descripción |
|---|---|
| 2026-09-18 | Se crea la tarea a partir de una captura de pantalla de la página; se implementa el cambio. |
| 2026-09-20 | Se compila, se abre y se mergea el PR #20. Se cierra la tarea. |
