# F44 — Mensajería y red de investigadores

**Categoría:** Colaboración Interinstitucional

## Objetivo

Sistema de mensajería, propuestas de alianzas y red de investigadores con transparencia
de autoría (quién aporta cada dato).

## Contexto

Pensado para conectar actores entre sí, no solo con la plataforma.

## Qué hay

No se encontró evidencia de implementación en el código actual. No hay modelos de
mensajes, conversaciones ni propuestas de alianza. Solo existe `FuenteDatos.reportador`
y `CargaArchivo.revisado_por` (`backend/app/models/datos.py:229`), trazabilidad interna
de carga, no transparencia de autoría pública entre instituciones. Tampoco hay nada
similar en PrototipoCOLFLUX.

## Qué hace falta

Sistema de mensajería/inbox, modelo de red de investigadores, flujo de propuestas de
alianza, y vista de autoría por dato visible a otras instituciones.
