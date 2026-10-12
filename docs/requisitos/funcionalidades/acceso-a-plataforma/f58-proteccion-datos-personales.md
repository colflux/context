# F58 — Cumplimiento de protección de datos personales

**Categoría:** Acceso a Plataforma (transversal)

## Objetivo

Validar los requisitos de Habeas Data (Ley 1581 de 2012) en el manejo de datos de
usuarios y comunidades.

## Contexto

Requisito transversal de cumplimiento normativo, no ligado a un módulo funcional
específico.

## Qué hay

No se encontró evidencia de implementación en el código actual — ninguna referencia a
Habeas Data, Ley 1581, consentimiento o manejo diferenciado de datos personales en
`backend`, `ia-functions` ni prototipos. Las únicas menciones están en documentación de
planeación: `context/docs/requisitos/funcionalidades/index.md` y
`context/docs/roadmap/roadmap-3-6-12-meses.md:73`, que la agrupan junto con F57 como
trabajo pendiente a futuro.

## Qué hace falta

Todo: no hay política de privacidad, mecanismo de consentimiento,
anonimización/seudonimización de datos de usuarios o comunidades, ni auditoría de qué
datos personales se capturan (vía formularios, chat, o futura integración de WhatsApp
en [F54](../inteligencia-artificial/f54-chatbot-whatsapp-territorial.md)). Está
explícitamente planeado para después de formalizar la matriz de RBAC de
[F57](f57-rbac-control-acceso-roles.md), no antes.
