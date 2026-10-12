# F06 — Dashboard geoespacial multi-módulo

**Categoría:** Geoportal

## Objetivo

Mostrar biomasa aérea/subterránea, flujos de GEI, carbono orgánico del suelo,
vegetación y GPP en un dashboard geoespacial integrado.

## Contexto

El catálogo original dejó pendiente: ¿cómo se relacionan estos 5 módulos con el resto
del catálogo? ¿GPP es dato capturado o calculado?

## Qué hay

Biomasa (aérea/subterránea) con modelo completo `app/models/biomasa.py:7`
(`MuestraBiomasa`), choices en `app/models/sitio.py:193-194`; flujos GEI
(CO2/CH4/N2O) vía `MuestraGEI`/`SubmuestraGEI`; carbono orgánico del suelo vía
`SubmuestraSuelo.carbono_pct` (`views.py:55-58`). El backend expone estas 3 categorías
agregables en `_CATEGORIA_CONFIG` (`views.py:20-67`). El frontend tiene gráficos
dedicados: `BiomasaTaxonChart.tsx`, `BiomasaProduccionScatter.tsx`, hooks
`useBiomasaPorTaxon.ts`, `useCosPorProfundidad.ts`.

## Qué hace falta

GPP existe como dato **capturado** (no calculado) en `app/models/torre.py:178`
(`gpp_f`, de torre de flujo/eddy covariance) — responde la pregunta pendiente del
catálogo —, pero no está expuesto en el geoportal: falta integrarlo a
`_CATEGORIA_CONFIG`, y no hay módulo de GPP ni de vegetación en el frontend.
