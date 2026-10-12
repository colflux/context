# F07 — Captura de coordenadas GPS en formularios

**Categoría:** Geoportal

## Objetivo

Georreferenciar automáticamente los registros hechos desde campo.

## Contexto

Distinto de la ubicación fija de un sitio de monitoreo: aquí se busca capturar GPS por
cada registro/medición individual.

## Qué hay

`Sitio.latitud/longitud` son campos fijos del sitio (editable a nivel de sitio, no de
registro), usados directamente en `sitios_geojson` (`views.py:264`). El único uso de
`navigator.geolocation` en todo el frontend está en el chatbot
(`frontend/src/hooks/useChat.ts:56-65`, función `pedirUbicacion`), no en un formulario
estructurado de campo.

## Qué hace falta

No hay georreferenciación automática de registros de campo — el formulario real de
reporte (`frontend/src/pages/ReportarFormulario.tsx`) solo sube archivos
`.xlsx/.xls/.csv`, sin captura de lat/lon. No hay coordenadas a nivel de
submuestra/medición individual, solo a nivel de Sitio (fijo), ni validación de GPS en
tiempo de captura.
