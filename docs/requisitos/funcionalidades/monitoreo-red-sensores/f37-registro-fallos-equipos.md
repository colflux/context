# F37 — Registro de fallos de equipos

**Categoría:** Monitoreo de Red y Sensores

## Objetivo

Generar alertas de desconexión cuando una estación queda offline.

## Contexto

Depende de tener primero un estado de operatividad por estación
([F36](f36-dashboard-estado-red.md)).

## Qué hay

No se encontró evidencia de implementación en el código actual. No existe modelo de
alertas, fallos ni notificaciones de desconexión en `backend/app`. El roadmap del repo
`context` (`docs/roadmap/roadmap-3-6-12-meses.md:69`) marca F36-F38 como "infraestructura
nueva, requiere decisión de hardware/proveedor... antes de estimar".

## Qué hace falta

Modelo de evento/alerta de fallo, lógica de detección de desconexión (depende de
[F38](f38-ingesta-iot-tiempo-real.md)/heartbeat), canal de notificación y vista en
frontend para gestionarlas.
