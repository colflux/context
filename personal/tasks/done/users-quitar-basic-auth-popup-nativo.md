# Quitar el popup nativo de Basic Auth al guardar cambios de usuario

**Estado:** cerrada — mergeado y verificado en producción
**Creada:** 2026-09-15
**A cargo:** Viviana
**Sesión de Claude Code:** https://claude.ai/code/session_01M7sC4mxBtg46EAE2Ns6Pky

## Objetivo

Que un admin pueda editar el nivel de acceso (u otros campos) de un usuario
desde `/team` en producción (`44.213.47.34`) sin que el navegador muestre
un popup nativo de "Acceder" (usuario/contraseña) al guardar.

## Contexto

Sale de verificar en producción la tarea de "admin cambia el rol de
cualquier persona desde el front" (ya implementada en código, ver
[[implementar-login-real]] y `UsuarioDrawer.tsx`).

Durante la prueba end-to-end aparecieron dos problemas distintos:

1. **Bug de frontend:** `usuarios.service.ts` no mandaba el header
   `Authorization: Token ...` en `crearUsuario` / `actualizarUsuario` /
   `eliminarUsuario`, aunque el backend (`EscrituraRequiereAdmin` en
   `UsuarioViewSet`) lo exige. **Ya resuelto y en producción**: el commit
   `ef30fcc` ("Autenticar mutaciones de usuarios y descargas del ETL con
   token", rama `feat/autenticar-usuarios-y-descarga-etl`) ya está
   mergeado a `main` de `colflux/frontend`.

2. **Popup nativo de Basic Auth (este archivo):** al probar el mismo flujo
   contra `http://44.213.47.34/team` (producción real, con Alejandra
   Gonzalez como usuario de prueba), Viviana reportó un popup nativo del
   navegador ("Acceder — Nombre de usuario / Contraseña") al hacer clic en
   "Guardar cambios". Es un `401` con `WWW-Authenticate: Basic`.

   **Diagnóstico inicial (descartado):** se sospechaba de un `auth_basic`
   a nivel de nginx (`/etc/nginx/sites-available/colflux`), agregado como
   mitigación temporal del bug (1). Con acceso SSH al servidor
   (`ubuntu@44.213.47.34`, llave nueva generada y agregada a
   `~/.ssh/authorized_keys` para esta sesión) se confirmó que **nginx no
   tiene ningún bloque `auth_basic` ni `limit_except`** — la config vigente
   (`sites-available/colflux`) solo hace `proxy_pass` plano a
   `backend_activo`/`frontend_activo`.

   **Causa real, en el backend:** `curl -D-` contra
   `http://44.213.47.34/api/usuarios/1/` (`PATCH` sin token) devuelve
   `401` con `WWW-Authenticate: Basic realm="api"`, pero con
   `Content-Type: application/json` y headers de seguridad de Django
   (`X-Frame-Options`, `Cross-Origin-Opener-Policy`) — es decir, el 401 lo
   arma Django/DRF, no nginx. `app/api/base.py::DataPortalModelViewSet`
   (clase base de casi todos los ViewSets, incluyendo `UsuarioViewSet`)
   tenía `authentication_classes = [BasicAuthentication]`, y los
   ViewSets concretos la extendían con
   `[*DataPortalModelViewSet.authentication_classes, TokenAuthentication]`
   — es decir, `BasicAuthentication` siempre quedaba primera en la lista.
   DRF arma el header `WWW-Authenticate` de un 401 a partir del primer
   autenticador configurado, así que siempre mandaba `Basic`, aunque
   nadie autentique realmente vía HTTP Basic en la app (no hay ningún uso
   real de esas credenciales en el código). El navegador interpreta ese
   header como invitación a mostrar su popup nativo.

## Plan

- [x] SSH al servidor (`44.213.47.34`, usuario `ubuntu`) — se generó una
      llave nueva para esta sesión (no se tenía la original ni el secret
      `LIGHTSAIL_SSH_KEY` a mano) y se agregó a `~/.ssh/authorized_keys`
      manualmente vía la consola SSH del navegador de Lightsail
- [x] Revisar `/etc/nginx/sites-available/colflux` — sin `auth_basic`, se
      descarta la hipótesis de nginx
- [x] Confirmar con `curl -D-` que el 401 con `WWW-Authenticate: Basic`
      viene del backend Django/DRF, no de nginx
- [x] Ubicar la causa: `BasicAuthentication` en
      `app/api/base.py::DataPortalModelViewSet.authentication_classes`
- [x] Fix: quitar `BasicAuthentication` de la clase base (queda
      `authentication_classes = []`; los ViewSets concretos ya agregan
      `TokenAuthentication` explícitamente)
- [x] Abrir PR (`colflux/backend` #23,
      `fix/quitar-basic-auth-popup-nativo`)
- [x] Mergear el PR (dispara el deploy automático a `44.213.47.34`)
- [x] Verificar tras el deploy: `curl -D-` a `PATCH /api/usuarios/<id>/`
      sin token ya no debe traer `WWW-Authenticate: Basic` — ahora responde
      `WWW-Authenticate: Token`
- [x] Reprobar en producción: se hizo el flujo completo de carga de datos
      sin que apareciera el popup nativo de credenciales
- [ ] Quitar del servidor la llave SSH agregada para esta sesión
      (`~/.ssh/authorized_keys` de `ubuntu@44.213.47.34`) una vez cerrada
      la tarea, por higiene de accesos

## Entregables

- `backend/app/api/base.py` — se quita `BasicAuthentication` de
  `DataPortalModelViewSet.authentication_classes` (PR
  [colflux/backend#23](https://github.com/colflux/backend/pull/23)).

## Referencias

- [[implementar-login-real]]
- [[automatizar-deploy-ecosistema-colflux]] — historial de la config de
  nginx en el servidor (confirmado que este bug no está ahí)
- `backend/app/api/base.py` — `DataPortalModelViewSet`
- `backend/app/api/usuario/views.py` — `UsuarioViewSet`,
  `EscrituraRequiereAdmin`
- `frontend/src/services/usuarios.service.ts`,
  `frontend/src/hooks/useUsuarioMutations.ts` — fix del bug (1), ya en
  `main`

## Historial

| Fecha | Descripción |
|---|---|
| 2026-09-15 | Se crea la tarea al encontrar un popup nativo de Basic Auth bloqueando el guardado en producción, durante la verificación del flujo de cambio de rol de usuario desde `/team`. Hipótesis inicial: `auth_basic` de nginx agregado como mitigación temporal. Se pospone por falta de acceso SSH. |
| 2026-09-22 | Se retoma la tarea. Se confirma que el fix de frontend (bug 1) ya estaba mergeado a `main` desde antes (commit `ef30fcc`). Para el punto de nginx: no se tenía la llave SSH original ni el secret `LIGHTSAIL_SSH_KEY`, así que se genera una llave nueva y Viviana la agrega manualmente a `~/.ssh/authorized_keys` vía la consola del navegador de Lightsail. Con acceso al servidor se descarta la hipótesis de nginx (sin `auth_basic` en su config) y, probando con `curl -D-`, se identifica que el 401 con `WWW-Authenticate: Basic` lo arma el propio backend Django/DRF: `DataPortalModelViewSet` (clase base de casi todos los ViewSets) tenía `BasicAuthentication` primera en `authentication_classes`, sin que nada la use realmente para autenticar — solo generaba el header que dispara el popup del navegador. Se corrige quitándola de la clase base y se abre el PR `colflux/backend#23`. Queda pendiente mergear, verificar tras el deploy automático y reprobar end-to-end en `/team`. |
| 2026-09-23 | El PR `colflux/backend#23` se mergea a `main` (deploy automático a `44.213.47.34`). Se verifica con `curl -D-` que el `401` de `PATCH /api/usuarios/1/` ahora trae `WWW-Authenticate: Token` en vez de `Basic`. Viviana reproduce el flujo completo de carga de datos en producción sin que aparezca el popup nativo de credenciales. Se cierra la tarea. Queda pendiente solo quitar la llave SSH temporal del servidor. |
