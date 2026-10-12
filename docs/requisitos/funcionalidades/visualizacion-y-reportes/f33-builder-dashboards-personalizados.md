# F33 — Builder de dashboards personalizados

**Categoría:** Visualización y Reportes

## Objetivo

Permitir armar dashboards a punta de arrastrar y soltar, con opción de guardar y
compartir con permisos.

## Contexto

Va más allá de los dashboards fijos actuales, dando control total al usuario sobre el
layout.

## Qué hay

No se encontró evidencia de implementación. No hay librerías de drag-and-drop en
`frontend/package.json` (no `react-grid-layout`, `react-dnd`, ni `gridstack`). El
dashboard existente (`DashboardIndicadores.tsx`) es una página fija con secciones
condicionadas por metodología, no editable por el usuario.

## Qué hace falta

Falta todo el mecanismo de arrastrar/soltar widgets, persistencia de layouts por
usuario, y permisos para compartir dashboards guardados.
