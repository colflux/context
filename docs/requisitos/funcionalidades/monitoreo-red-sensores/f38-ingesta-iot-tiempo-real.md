# F38 — Ingesta automática de datos IoT en tiempo real

**Categoría:** Monitoreo de Red y Sensores

## Objetivo

Que sensores de campo (ceptómetros, analizadores de gases) transmitan vía
LoRa/Wi-Fi/4G a un sistema DAQ integrado con la plataforma — un canal automatizado,
distinto de la carga manual de [F09](../datos-y-carga/f09-ingreso-datos-carbono.md).

## Contexto

Requiere decisión previa de hardware/proveedor de conectividad, según el roadmap.

## Qué hay

No se encontró evidencia de un canal de ingesta automática de sensores
(LoRa/Wi-Fi/4G/MQTT). El único endpoint llamado "ingest" es
`ia-functions/app/api/routes.py:12-15` (`POST /ingest`), pero sirve para indexar
documentos de texto en el RAG del chatbot, no datos de sensores. La carga de datos de
torres EC (`MuestraTorre`, `SubmuestraEddy`, `SubmuestraReddy` en
`backend/app/models/torre.py:91-189`) sigue el patrón de carga manual vía
ETL/formularios/CSV.

## Qué hace falta

Protocolo/gateway de recepción (MQTT, webhook HTTP, LoRa), modelo de ingestión en
tiempo real que alimente las tablas de muestras automáticamente, y decisión de
hardware/proveedor de conectividad (pendiente según roadmap).
