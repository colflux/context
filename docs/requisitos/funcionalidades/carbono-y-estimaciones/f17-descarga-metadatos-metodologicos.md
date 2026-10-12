# F17 — Descarga de metadatos metodológicos

**Categoría:** Carbono y Estimaciones

## Objetivo

Que cada dato se pueda acompañar de su metodología, protocolo de medición, instrumento,
fecha y nivel de confianza, descargables junto con (o aparte de) el dato en sí.

## Contexto

El catálogo original dejó pendiente: ¿estándar de metadatos a usar (Dublin Core, ISO
19115)? ¿se descarga junto al dato o aparte?

## Qué hay

Hay campos de metodología dispersos por modelo, sin un estándar unificado:
`SubmuestraSuelo.metodologia_tipo_muestreo`/`metodologia_distancia_m`/
`metodologia_azimut`/`metodologia_analisis` y `MonitoreoSuelo.protocolo`
(`backend/app/models/suelo.py:40-49,95-100`), `ResultadoPublicacion.metodologia` (texto
libre). El Excel exportado por `exportar_carga`/`exportar_proyecto`
(`backend/app/api/etl/views.py:3593-3677`) incluye una hoja de "diccionario de datos"
(`_agregar_hoja_diccionario_datos`) con los nombres/verbose de columnas, pero no
instrumento, fecha de calibración ni nivel de confianza como bloque de metadatos aparte.

## Qué hace falta

- No hay adopción de un estándar de metadatos (Dublin Core/ISO 19115).
- No hay campo de "nivel de confianza" por dato, ni instrumento/equipo salvo casos
  puntuales (`IndividuoArboreo.equipo` en biomasa).
- No existe descarga separada de metadatos metodológicos — solo el diccionario de
  columnas embebido en el mismo Excel de datos.
