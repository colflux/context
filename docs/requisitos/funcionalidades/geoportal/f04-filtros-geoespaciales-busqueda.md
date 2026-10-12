# F04 — Filtros geoespaciales y búsqueda

**Categoría:** Geoportal

## Objetivo

Filtrar por región/municipio, lluvia, temperatura y cobertura vegetal, más una barra de
búsqueda propia del geoportal.

## Contexto

Combina filtros administrativos (región/municipio) con filtros ambientales
(lluvia/temperatura/cobertura).

## Qué hay

Filtro jerárquico región→departamento→municipio→vereda en
`frontend/src/features/filters/FilterPanel.tsx`. El backend soporta filtrado por esos
niveles en `/api/geo/series/` y `/api/geo/resumen/` (incluye nivel vereda, `views.py:
516-519,540-547,583-584`).

## Qué hace falta

- Los filtros de "Ecosistema/Cobertura" y "Estado de conservación" existen en la UI
  pero están deshabilitados (`FilterPanel.tsx:298-309`, opción única "Próximamente").
- No hay filtro por lluvia/precipitación ni temperatura en ningún endpoint geo
  (temperatura solo existe como dato medido, no como filtro, en `app/models/co2.py:
  118-123` y `app/models/torre.py:150`).
- Existe el modelo `Vegetacion` (`app/models/cobertura.py:55`) pero no está expuesto
  como filtro geo.
- No existe barra de búsqueda propia del geoportal.
