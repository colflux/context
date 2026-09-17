# Conectar el formulario de "Reportar" a un endpoint real

**Estado:** pendiente
**Creada:** 2026-09-15

## Objetivo

Que el formulario de `Participacion.tsx` (ruta `/reportar` en `frontend`)
envíe los reportes a un endpoint real del `backend`, en vez de solo
guardar el estado `enviado` en memoria como hace hoy.

## Contexto

Sale de [[definir-rol-y-habilitar-reportar]]: al habilitar el gate por
nivel (`reportador` en adelante) se dejó explícitamente pendiente esta
parte por estar fuera de alcance de esa tarea. Hoy `handleSubmit` en
`Participacion.tsx` solo hace `setEnviado(true)` — es un mock, no llama
a ningún servicio ni persiste nada en el `backend`.

## Plan

- [ ] Definir el modelo de datos del reporte en el `backend` (tipo de
      observación/ecosistema, ubicación, descripción, foto opcional,
      usuario que reporta, fecha)
- [ ] Crear el endpoint (Django + PostGIS, dado que hay ubicación
      geoespacial) y el service correspondiente en `frontend`
      (`src/services/`)
- [ ] Conectar `handleSubmit` en `Participacion.tsx` al nuevo servicio,
      con manejo de error (hoy no hay ningún camino de error en la UI)
- [ ] Definir si la foto se sube a almacenamiento (S3/media) o se deja
      fuera de este primer alcance
- [ ] Decidir si los reportes necesitan revisión/moderación antes de
      hacerse visibles en el geoportal, o quedan visibles de inmediato

## Entregables

(Pendiente)

## Referencias

- [[definir-rol-y-habilitar-reportar]]
- `frontend`: `src/pages/Participacion.tsx`

## Historial

| Fecha | Descripción |
|---|---|
| 2026-09-15 | Se crea la tarea, a partir de un pendiente dejado en [[definir-rol-y-habilitar-reportar]]. |
