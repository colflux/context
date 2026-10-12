# F39 — Alertas automáticas por umbral

**Categoría:** Alertas y Notificaciones

## Objetivo

Que el sistema compare valores contra un umbral y genere una alerta de anomalía.

## Contexto

Mecanismo de aviso que puede dispararse desde cualquier otro módulo.

## Qué hay

No se encontró evidencia de implementación en el código actual. En
`backend/app/models/torre.py:179` existe un campo `ustar_used` ("umbral de u* usado en
el filtrado"), pero es un parámetro de filtrado micrometeorológico, no un mecanismo de
alertas. En `frontend/src/components/etl-upload/AnalisisEDA.tsx:103` hay un flag
`hayAlertas` para outliers/nulos/duplicados, pero es validación de calidad de datos en
el flujo ETL, no alertas de anomalía sobre series de monitoreo. En
`PrototipoCOLFLUX/Frontend-Colflux/dashboard.js:684-713` hay un parser de filtros
"mayor que umbral X" para consultas de UI, sin relación con detección de anomalías.

## Qué hace falta

Modelo de `Alerta`/`UmbralConfigurado`, lógica de evaluación periódica (celery
beat/cron) que compare mediciones contra umbrales, persistencia de alertas,
endpoint/serializer, y UI para configurarlas y visualizarlas.
