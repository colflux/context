# F41 — Integración y sincronización de datos externos

**Categoría:** Colaboración Interinstitucional

## Objetivo

API para conectar sistemas externos (IDEAM, Ecopetrol), ETL de datos de partners,
sincronización automática y versionado por institución de origen.

## Contexto

Todo lo que conecta a COLFLUX con otras instituciones o conecta actores entre sí.

## Qué hay

`FuenteDatos.TIPO_CHOICES` incluye `"api"` ("API externa") en
`backend/app/models/datos.py:151`, y existe un wizard ETL
(`backend/app/api/etl/views.py`) para mapear e importar archivos Excel/CSV, con
`MapeoColumna` registrando transformaciones y origen (`origen_mapeo`,
`app/models/datos.py:222`). Es ETL manual de archivos subidos por un "reportador", no
integración con sistemas externos reales; no hay ninguna mención de IDEAM/Ecopetrol en
ningún repo.

## Qué hace falta

Conectores/clientes a APIs externas, jobs de sincronización automática, y versionado
explícito por institución de origen (solo existe `FuenteDatos.proyecto`/`reportador`,
sin modelo de "institución de origen del dato" ni historial de versiones).
