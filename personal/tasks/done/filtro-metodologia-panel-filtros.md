# Agregar selector de metodología al panel de filtros (Mapas/Dashboard)

**Estado:** hecho
**Creada:** 2026-09-21
**A cargo:** Viviana
**Sesión de Claude Code:** https://claude.ai/code/session_01JCdJiAGLgZESxua7VMpRkK

## Objetivo

En `FilterPanel` (usado en `/mapas` y compartido vía `useAppStore` con
`/dashboard`), agregar un recuadro "Metodología" (General/Biomasa/COS/Flujos)
que, según la elección, muestra un recuadro adicional de filtros propios de
esa metodología — según el mockup que trajo el equipo (ver Contexto).

## Contexto

Viviana pidió, con una captura del panel actual (`/mapas`) y una lista de
"variables asociadas": un recuadro transversal (Proyecto/Entidad, Región,
Departamento, Municipio, Vereda/Casco-urbano — más Ecosistema/Cobertura,
Estado de conservación y Fecha marcados como deshabilitados/próximamente) y,
debajo, un recuadro condicional según la metodología elegida: Biomasa
(Familia, Género, Especie, DAP), COS (Profundidad de muestra), Flujos
(Analizador, day/night).

Alcance acordado explícitamente con Viviana: **solo frontend**, sin cambios
de backend. Esto importa porque el backend no expone estos campos como
filtros reales (búsqueda previa en `frontend` confirmó que Familia/Género/
Especie, Profundidad y Analizador/día-noche solo existen hoy como
*dimensiones de agrupación* para gráficas puntuales — `dimension=` en
`/api/reportes/biomasa/` y `/api/geo/resumen-categorico/` —, no como
parámetros que acoten resultados a un valor específico). Por eso los
selectores condicionales no filtran datos vía API: reutilizan mecanismos ya
existentes en el frontend (dimensión activa de un chart, `selectedId` de
`CategoricalChart`, resaltado client-side) para que la interacción sea real
sin inventar soporte de backend que no existe.

## Entregables (todo en `frontend`)

- `src/types/index.ts`: nuevo tipo `Metodologia`.
- `src/store/useAppStore.ts`: estado `metodologia` + filtros condicionales
  (`biomasaDimension`, `cosProfundidad`, `flujosAnalizadorId`,
  `flujosCondicionLuzId`) y nivel `region` agregado al drill-down geográfico
  existente (región → departamento → municipio → vereda). Cambiar de
  metodología resetea los filtros condicionales de la anterior.
- `src/components/common/Select.tsx`: soporte para `disabled` (antes solo
  existía `disabled` por opción, no por selector completo) — usado en los
  campos "Próximamente".
- `src/features/filters/FilterPanel.tsx`: reestructurado con recuadros
  "Metodología", "Filtros" (transversales, incluye Región nueva y los 3
  campos deshabilitados) y un recuadro condicional por metodología.
- `src/components/charts/BiomasaTaxonChart.tsx`: el toggle interno
  Familia/Género/Especie se reemplazó por el estado del store
  (`biomasaDimension`), controlado ahora desde el panel de filtros.
- `src/components/charts/CosProfundidadChart.tsx`: la barra del rango de
  profundidad seleccionado en el panel se resalta (opacidad) sobre el resto.
- `src/pages/DashboardIndicadores.tsx`: las gráficas "Flujo por analizador" y
  "Flujo por condición de luz" quedan conectadas (`selectedId`/`onSelect`) al
  `flujosAnalizadorId`/`flujosCondicionLuzId` del store — seleccionar en el
  panel resalta la barra correspondiente, y viceversa.

## Verificado

`tsc --noEmit` limpio, `vite build` exitoso, y probado en el navegador
(`npm run dev`) en `/mapas`: el recuadro "Metodología" cambia correctamente
entre General/Biomasa/COS/Flujos mostrando el recuadro condicional esperado,
con Región/Vereda-Casco-urbano renombrados y Ecosistema/Cobertura, Estado de
conservación y Fecha como "Próximamente". No se pudo verificar el resaltado
cruzado con datos reales porque no había backend local corriendo (puerto
8001) — la lógica se revisó por código, no por datos en pantalla.

## Pendiente para una futura sesión

Si el equipo pide que estos filtros condicionales realmente acoten los datos
(no solo resalten/agrupen), hace falta trabajo de backend: exponer
Familia/Género/Especie, rango de profundidad y Analizador/condición de luz
como parámetros de filtro (no solo `dimension=`) en los endpoints de
`/api/reportes/` y `/api/geo/`. DAP tampoco tiene un endpoint que devuelva
valores individuales (solo promedios por taxón), así que quedó deshabilitado
sin alternativa frontend-only.

## Referencias

- [[reportes-modulo-graficas]] — tarea original de los charts que estos
  filtros terminan afectando (Biomasa, COS, Flujos ya viven en `/dashboard`).

## Historial

| Fecha | Descripción |
|---|---|
| 2026-09-21 | Se implementa el selector de metodología y los recuadros condicionales en `frontend` (alcance acordado: solo frontend). Verificado con `tsc`, `vite build` y navegador. |
| 2026-09-21 | Viviana pide quitar las cards "Resumen" y "Por proyecto" del panel lateral de `/mapas` (`MapaInteractivo.tsx`), dejando solo "Filtros" — se elimina también `EmissionSummary.tsx` por quedar sin uso en ningún lado. Luego pide reorganizar el panel en grupos plegables: "Metodología" (Gas + selector de metodología + su recuadro condicional) siempre expandido y sin colapsar, y "Temporal" (Año, Fecha), "Espacial" (Proyecto, Región, Departamento, Municipio, Vereda) y "Ambiental" (Ecosistema/Cobertura, Estado de conservación) como acordeones colapsados por defecto. Se crea `src/components/common/Collapsible.tsx` (colapsable simple reusable) y se reestructura `FilterPanel.tsx` con este orden. Verificado con `tsc` y en el navegador: solo "Metodología" aparece abierto al cargar, y "Espacial" se expande correctamente al hacer clic. |
