# Editar/eliminar proyectos y asociar instituciones

**Estado:** cerrada — mergeado y desplegado
**Creada:** 2026-09-22
**A cargo:** Viviana
**Sesión de Claude Code:** https://claude.ai/code/session_01M7sC4mxBtg46EAE2Ns6Pky

## Objetivo

Desde "Gestión de Datos" (`/data`), poder editar y eliminar proyectos (antes
solo se podían crear), y asociar una o más instituciones (Universidad
Javeriana, etc.) a cada proyecto.

## Contexto

Pedido directo de Viviana a partir de una captura de la tabla "Administración
de proyectos": *"quiero que se puedan borrar proyectos y que se puedan
editar y agregar una entidad asociada al proyecto"*. Al preguntar qué
significaba "entidad asociada", se confirmó que era institución (no
responsable/usuario ni sitio de monitoreo).

Al revisar el backend se encontró que `ProyectoViewSet` no tenía **ninguna**
restricción de escritura — cualquiera podía crear/editar/borrar proyectos
sin login, a diferencia de `FuenteDatosViewSet` y `UsuarioViewSet` que ya
exigían rol reportador+/admin. Se corrigió como parte de esta tarea.

También existía ya `Proyecto.instituciones` (M2M a `Institucion`, a través
de `ProyectoInstitucion`) en el modelo, pero nunca se había expuesto en el
serializer ni en el frontend.

## Plan

- [x] Backend: exponer `instituciones` (escribible, lista de IDs) e
      `instituciones_detalle` (solo lectura, anidado) en `ProyectoSerializer`
- [x] Backend: agregar `TokenAuthentication` + `EscrituraRequiereReportador`
      a `ProyectoViewSet` (antes sin ninguna protección de escritura)
- [x] Backend: manejar `ProtectedError` en `destroy()` (un proyecto con
      `UnidadExperimental` asociada no se puede borrar — `on_delete=PROTECT`)
- [x] Frontend: extender tipos `Proyecto`/`ProyectoPayload` con
      `instituciones`/`instituciones_detalle`
- [x] Frontend: `proyectos.service.ts` — mandar token en
      crear/actualizar/eliminar (mismo patrón que `usuarios.service.ts`)
- [x] Frontend: botones editar (✎) y eliminar (✕) en `ProyectosTable`, con
      `ConfirmModal` que avisa cuántas fuentes quedarán sin proyecto
      (`FuenteDatos.proyecto` es `SET_NULL`, no se borran)
- [x] Frontend: `ProyectoDrawer` en modo edición (prefill) + selector de
      instituciones (checkboxes)
- [x] Abrir PRs y mergear (backend primero, por dependencia del campo
      `instituciones`)
- [x] Verificar en producción

## Entregables

- Backend: [colflux/backend#24](https://github.com/colflux/backend/pull/24)
  — mergeado 2026-09-23
- Frontend: [colflux/frontend#36](https://github.com/colflux/frontend/pull/36)
  — mergeado 2026-09-23

## Referencias

- `backend/app/api/proyecto/serializers.py`, `views.py`
- `backend/app/api/permisos.py` — `EscrituraRequiereReportador`
- `frontend/src/services/proyectos.service.ts`,
  `frontend/src/hooks/useProyectoMutations.ts`,
  `frontend/src/components/admin/proyectos/ProyectoDrawer.tsx`,
  `frontend/src/components/data/ProyectosTable.tsx`
- Patrón replicado de `usuarios.service.ts`/`useUsuarioMutations.ts` y de
  `FuenteDrawer.tsx`/`FuentesTable.tsx`

## Historial

| Fecha | Descripción |
|---|---|
| 2026-09-22 | Se crea la tarea a partir de un pedido directo de Viviana (captura de la tabla de proyectos). Se detecta que `ProyectoViewSet` no tenía ninguna restricción de escritura — gap de seguridad real, se corrige junto con la funcionalidad pedida. Se implementa edición/borrado de proyectos y asociación de instituciones en backend y frontend. Se abren PRs `colflux/backend#24` y `colflux/frontend#36` (backend debe ir primero por la dependencia del campo `instituciones` en el serializer). |
| 2026-09-23 | Ambos PRs se mergean a `main` (deploy automático a `44.213.47.34`). Se cierra la tarea. |
