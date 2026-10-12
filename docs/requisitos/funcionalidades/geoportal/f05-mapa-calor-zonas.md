# F05 — Mapa de calor por zonas

**Categoría:** Geoportal

## Objetivo

Visualizar emisiones cruzando variables ambientales, con tendencia temporal
seleccionable.

## Contexto

El catálogo original dejó pendiente: ¿granularidad mínima (vereda para todas las zonas
o solo priorizadas)?

## Qué hay

Series temporales y tendencias existen: `series_co2` (`app/api/geo/views.py:321-431`) y
`tendencia_instalacion` (`views.py:813-862`, agregado mensual/anual). La granularidad
hasta nivel vereda está soportada en el backend (`views.py:516-519`).

## Qué hace falta

No hay heatmap real (ni en frontend ni backend). No se cruzan variables ambientales
(lluvia/temperatura) con emisiones — esos filtros no existen (ver
[F04](f04-filtros-geoespaciales-busqueda.md)). No existe el concepto de "zonas
priorizadas" vs. todas las zonas (sin resultados al buscar "prioritaria" en todo el
backend).
