# F30 — Generador de gráficos configurables

**Categoría:** Visualización y Reportes

## Objetivo

Que cualquier usuario pueda generar gráficos (línea, barra, pie, etc.) sobre cualquier
variable de la plataforma.

## Contexto

Herramienta self-service, distinta de los gráficos fijos por sección que ya existen.

## Qué hay

Hay una librería de gráficos basada en `recharts` (`frontend/package.json`) con
componentes reutilizables (`CategoricalChart.tsx` soporta tipo `'torta' | 'barras'` y
métrica `'total_muestras' | 'promedio'` sobre una dimensión elegida; `DonaChart.tsx`,
`BarrasHorizontalesChart.tsx`, `BoxplotTendenciaChart.tsx`). El prototipo viejo
(`PrototipoCOLFLUX/Frontend-Colflux/dashboard.js`) usaba Chart.js de forma similar
(gráfica única re-renderizada con `graficaFlujos`).

## Qué hace falta

No es un generador configurable por el usuario final sobre "cualquier variable de la
plataforma": cada chart está hardcodeado a una dimensión/endpoint específico del
backend (`/api/reportes/...`, `/api/geo/resumen-categorico/`); no hay UI para que el
usuario elija eje X/Y, tipo de gráfico y variable libremente.
