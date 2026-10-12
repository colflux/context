# F29 — Visualización del ciclo de carbono

**Categoría:** Visualización y Reportes

## Objetivo

Mostrar gráficos y diagramas de flujo de carbono que ayuden a entender el ciclo como
sistema.

## Contexto

Herramienta genérica de graficación, no ligada a un solo tipo de dato de carbono.

## Qué hay

Existen gráficos específicos de componentes del ciclo de carbono (no un diagrama de
flujo integrado): `frontend/src/components/charts/FlujoClimaChart.tsx` (flujo de GEI
cruzado con variables climáticas, usando recharts `ComposedChart`),
`CosProfundidadChart.tsx` (carbono orgánico del suelo por profundidad),
`MomHojarascaChart.tsx` (carbono en hojarasca/MOM), y
`BiomasaProduccionScatter.tsx`/`BiomasaTaxonChart.tsx` (biomasa). Estos se combinan por
secciones en `frontend/src/pages/DashboardIndicadores.tsx` (Flujos, Biomasa, COS, MOM).

## Qué hace falta

No hay un diagrama de flujo de carbono (Sankey o similar) que muestre el ciclo como
sistema integrado entre reservorios (biomasa → suelo → atmósfera); lo que existe son
gráficos independientes por metodología de muestreo, no una visualización conceptual
del ciclo.
