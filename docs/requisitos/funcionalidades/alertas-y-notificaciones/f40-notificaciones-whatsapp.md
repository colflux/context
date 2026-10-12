# F40 — Notificaciones proactivas vía WhatsApp

**Categoría:** Alertas y Notificaciones

## Objetivo

Avisar por WhatsApp sobre actualización de datos, tendencias o respuestas a consultas
previas — distinto del chatbot conversacional de
[F54](../inteligencia-artificial/f54-chatbot-whatsapp-territorial.md).

## Contexto

Es notificación de salida iniciada por el sistema, no una respuesta a una pregunta del
usuario.

## Qué hay

No se encontró evidencia de implementación en el código actual. No hay rastro de
`whatsapp`, `twilio` ni webhooks de WhatsApp Business API en ningún repo. Existe un
chatbot conversacional vía API HTTP/RAG+tool-calling en `ia-functions/` (rutas `/chat` y
`/chat/historial` en `app/api/routes.py`, documentado en `ia-functions/arquitectura.md`),
que responde preguntas por request-response, sin envío proactivo ni conexión a canal
WhatsApp.

## Qué hace falta

Integración con WhatsApp Business API/Twilio, lógica de notificación proactiva
disparada por eventos (nueva data, tendencia, alerta de
[F39](f39-alertas-automaticas-umbral.md), o respuesta diferida), y mecanismo de
scheduling/trigger para envíos salientes.
