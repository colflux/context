# Opción para que un usuario pida subir de nivel de acceso

**Estado:** completada
**Creada:** 2026-09-15

## Objetivo

Complementar el registro self-service ([[agregar-opcion-registro]], ya
implementado: cualquiera se registra y queda con nivel `ciudadano`) con una
forma de que ese usuario pida que le suban el nivel (`investigador`,
`reportador` o `admin`), sin que un admin tenga que ir a buscarlo
manualmente en `/team`.

## Contexto

El modelo de acceso ya no es "roles múltiples" sino **nivel en cascada**
(`app/models/datos.py::Usuario.NIVELES_ACCESO` = `ciudadano < investigador
< reportador < admin`, ver commit `74a0f4d` "Reemplazar roles múltiples por
nivel de acceso en cascada"). El registro (`RegistroView`) ya asigna
`ciudadano` por defecto y no deja elegir nivel. Hoy la única forma de subir
de nivel es que un admin edite el `Usuario` desde `/team` →
`UsuarioDrawer`. No existía ningún mecanismo de "solicitud".

## Decisiones de diseño (2026-09-15)

- **Con registro en BD** (no solo un mailto ni un campo de texto suelto):
  nuevo modelo `SolicitudNivel` con estado (`pendiente` / `aprobada` /
  `rechazada`), para tener trazabilidad e historial.
- **Puede pedir cualquier nivel** por encima de `ciudadano`
  (`investigador`, `reportador` o `admin`), no solo el siguiente escalón en
  la cascada — el admin decide si aprueba tal cual.
- **Una solicitud pendiente a la vez**: si ya tiene una sin resolver, no
  puede crear otra hasta que el admin la resuelva.
- Aprobar una solicitud actualiza `Usuario.nivel` automáticamente al nivel
  solicitado; rechazarla solo cambia el estado (no toca el nivel actual).
- Solo un admin puede resolver (aprobar/rechazar) solicitudes ajenas; un
  usuario no-admin solo ve y crea las suyas propias.

## Plan

- [x] Backend: modelo `SolicitudNivel` (usuario FK, nivel_solicitado,
      motivo, estado, resuelta_por FK) + migración
- [x] Backend: `SolicitudNivelSerializer`
- [x] Backend: `SolicitudNivelViewSet` (list/create/retrieve/partial_update,
      sin destroy) con permisos: cualquier autenticado ve/crea las suyas,
      admin ve/resuelve todas
- [x] Backend: ruta `api/solicitudes-nivel/` en el router
- [x] Frontend: tipos `SolicitudNivel` / `SolicitudNivelPayload`
- [x] Frontend: `solicitudesNivel.service.ts` (con `Authorization: Token`,
      igual que `auth.service.ts` — los demás servicios no mandan token,
      gap ya señalado en [[agregar-opcion-registro]])
- [x] Frontend: hooks `useSolicitudesNivel`, `useCrearSolicitudNivel`,
      `useResolverSolicitudNivel`
- [x] Frontend: modal "Solicitar otro nivel" enlazado desde `UserMenu.tsx`
      (solo visible si no es admin)
- [x] Frontend: sección de solicitudes pendientes en `/team` para que el
      admin apruebe/rechace
- [x] Verificación (backend checks + `tsc --noEmit` + prueba end-to-end
      vía Docker)

## Entregables

- `backend/app/models/datos.py` — modelo `SolicitudNivel` (usuario,
  nivel_solicitado, motivo, estado, resuelta_por).
- `backend/app/migrations/0089_merge_0087_seed_rol_basico_0088_usuario_nivel_acceso.py` —
  migración merge que resolvió un conflicto **preexistente** de dos hojas
  paralelas en el grafo de migraciones (0087 y 0088, ambas dependientes de
  0086), detectado al correr `makemigrations`. No relacionado con esta
  tarea, pero bloqueaba aplicar cualquier migración nueva.
- `backend/app/migrations/0090_solicitudnivel.py` — migración del modelo
  nuevo.
- `backend/app/api/usuario/serializers.py` — `SolicitudNivelSerializer`.
- `backend/app/api/usuario/views.py` — `SolicitudNivelViewSet` (mixins
  create/retrieve/list/update, sin destroy; `perform_create` fuerza
  `usuario` al dueño del token y bloquea pendientes duplicadas o niveles no
  superiores; `perform_update` exige `admin` y sincroniza `Usuario.nivel`
  al aprobar).
- `backend/app/api/urls.py` — ruta `api/solicitudes-nivel/` en el router.
- `frontend/src/types/index.ts` — `SolicitudNivel`, `SolicitudNivelPayload`,
  `EstadoSolicitudNivel`.
- `frontend/src/services/solicitudesNivel.service.ts`,
  `frontend/src/hooks/useSolicitudesNivel.ts` — `listar`/`crear`/`resolver`
  con token, hooks de react-query.
- `frontend/src/components/layout/SolicitarNivelModal.tsx` — modal para
  pedir un nivel superior al actual (bloqueado si ya hay una pendiente),
  enlazado desde `UserMenu.tsx` (oculto si el usuario ya es `admin`).
- `frontend/src/components/admin/team/SolicitudesNivelAdmin.tsx` — lista de
  solicitudes pendientes con botones Aprobar/Rechazar, agregada a
  `pages/Team.tsx`.

## Verificación (2026-09-15)

Vía Docker (`docker compose up -d --build`) contra backend real:

- Registro de usuario nuevo → nivel `ciudadano` (comportamiento ya
  existente, sin cambios).
- Solicitud de nivel `reportador` con motivo → `HTTP 201`, estado
  `pendiente`.
- Segunda solicitud mientras hay una pendiente → rechazada con "Ya tienes
  una solicitud pendiente de resolver."
- Solicitar `ciudadano` (no superior al actual) → `HTTP 400`, choices del
  modelo ya lo excluyen.
- Usuario no-admin intenta aprobar su propia solicitud (`PATCH`) → `HTTP
  403` "Solo un administrador puede resolver solicitudes."
- Admin lista todas las solicitudes (no solo las propias) y aprueba la
  pendiente → `HTTP 200`; el `Usuario.nivel` del solicitante pasó de
  `ciudadano` a `reportador` automáticamente.
- `tsc --noEmit` sin errores en frontend.
- Datos de prueba (usuarios, `auth.User`, `SolicitudNivel`) limpiados antes
  de bajar los contenedores.

**No se hizo commit**: los cambios quedan en el working tree de
`colflux/backend` y `colflux/frontend` para que el usuario revise antes de
confirmar.

## Referencias

- [[agregar-opcion-registro]] — registro self-service con nivel `ciudadano`
  por defecto, mismo patrón de decisiones de diseño antes de implementar.
- `backend/app/models/datos.py` — `Usuario.NIVELES_ACCESO`, `tiene_nivel`.
- `backend/app/api/permisos.py` — `EscrituraRequiereNivel` y variantes.
- `frontend/src/components/layout/UserMenu.tsx`,
  `frontend/src/pages/Team.tsx` — puntos de extensión en frontend.

## Historial

| Fecha | Descripción |
|---|---|
| 2026-09-15 | Se crea la tarea a partir del pedido del usuario de agregar la opción de pedir permiso de roles (complemento al registro, que ya asigna `ciudadano` por defecto). Se revisó el modelo actual (nivel en cascada, ya migrado desde roles múltiples) y se acordaron las decisiones de diseño: modelo `SolicitudNivel` con estado pendiente/aprobada/rechazada, cualquier nivel superior es pedible, una solicitud pendiente a la vez, solo admin resuelve. |
