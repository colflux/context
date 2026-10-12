# F42 — Portal único de datos consolidados

**Categoría:** Colaboración Interinstitucional

## Objetivo

Ver en un solo lugar los datos de todas las instituciones integradas.

## Contexto

Depende de que exista primero integración real con sistemas externos
([F41](f41-integracion-sincronizacion-externa.md)).

## Qué hay

Existe un geoportal/API interno (`backend/app/api/geo/views.py`) con endpoints
`sitios/`, `series/`, `resumen/` que agregan mediciones por nivel geográfico. El modelo
`Proyecto` tiene M2M a `Institucion` vía `ProyectoInstitucion`
(`backend/app/models/proyecto.py:51-58`), permitiendo asociar datos a varias
instituciones participantes.

## Qué hace falta

Un "portal" diferenciado por institución externa (todo es de la propia plataforma);
falta vista/endpoint que agrupe explícitamente "datos por institución integrada" como
entidad externa distinta del proyecto interno.
