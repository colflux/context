# Quitar el HTTP Basic Auth de nginx en las rutas de escritura de /api/

**Estado:** pendiente
**Creada:** 2026-09-15

## Objetivo

Que un admin pueda editar el nivel de acceso (u otros campos) de un usuario
desde `/team` en producción (`44.213.47.34`) sin que el navegador muestre
un popup nativo de "Acceder" (usuario/contraseña) al guardar.

## Contexto

Sale de verificar en producción la tarea de "admin cambia el rol de
cualquier persona desde el front" (ya implementada en código, ver
[[implementar-login-real]] y `UsuarioDrawer.tsx`).

Durante la prueba end-to-end aparecieron dos problemas distintos:

1. **Bug de frontend (ya corregido, sin commitear):** `usuarios.service.ts`
   no mandaba el header `Authorization: Token ...` en `crearUsuario` /
   `actualizarUsuario` / `eliminarUsuario`, aunque el backend
   (`EscrituraRequiereAdmin` en `UsuarioViewSet`) lo exige. Esto se probó y
   corrigió contra el backend en Docker local (`localhost:8000`, sin
   nginx delante) — `PATCH`/`DELETE` funcionaron con `200`. Cambios en
   `colflux/frontend`: `src/services/usuarios.service.ts`,
   `src/hooks/useUsuarioMutations.ts`.

2. **HTTP Basic Auth a nivel de nginx en producción (este archivo):** al
   probar el mismo flujo contra `http://44.213.47.34/team` (producción
   real, con Alejandra Gonzalez como usuario de prueba), Viviana reportó
   un popup nativo del navegador ("Acceder — Nombre de usuario /
   Contraseña", con el aviso "Tu conexión con este sitio no es privada")
   al hacer clic en "Guardar cambios". Esto **no es el login de la app**:
   es un `401` con `WWW-Authenticate: Basic`, que solo puede venir de
   nginx (`/etc/nginx/sites-available/colflux` en el servidor, ver
   [[automatizar-deploy-ecosistema-colflux]]) o de alguna capa
   intermedia — el backend Django/DRF usa `TokenAuthentication`, no
   `Basic`. Las peticiones GET (cargar la tabla de usuarios) sí
   funcionan sin prompt, así que la protección parece aplicar solo a
   métodos de escritura (`PATCH`/`POST`/`DELETE`), probablemente un
   `limit_except GET { auth_basic ...; }` agregado como mitigación
   temporal de cuando el bug (1) dejaba las escrituras de `/api/`
   efectivamente abiertas a cualquiera.

No se tiene acceso SSH al servidor desde este entorno para confirmar/editar
la config directamente — Viviana lo hará mañana.

## Plan

- [ ] SSH al servidor (`44.213.47.34`, usuario probablemente `ubuntu`,
      misma llave que `LIGHTSAIL_SSH_KEY` en GitHub Actions)
- [ ] Revisar `/etc/nginx/sites-available/colflux` (o el archivo vigente,
      ver histórico de renombres en
      [[automatizar-deploy-ecosistema-colflux]]) y localizar el bloque
      `auth_basic`/`limit_except` sobre `/api/`
- [ ] Confirmar que el propio backend ya protege escritura de usuarios vía
      `EscrituraRequiereAdmin` + `Authorization: Token` (ya verificado en
      local) antes de quitar la capa de nginx, para no dejar el endpoint
      sin protección real en el intervalo
- [ ] Quitar (o acotar) el `auth_basic` de esa ruta, `nginx -t` y
      `systemctl reload nginx`
- [ ] Desplegar el fix de frontend (commitear y mergear los cambios
      pendientes en `usuarios.service.ts`/`useUsuarioMutations.ts`) antes
      o junto con este cambio, para no reabrir la ventana de escritura sin
      auth real
- [ ] Reprobar en producción: admin edita el nivel de otro usuario desde
      `/team` sin ningún popup de credenciales, sin tocar el campo
      contraseña

## Entregables

(Pendiente.)

## Referencias

- [[implementar-login-real]]
- [[automatizar-deploy-ecosistema-colflux]] — historial de la config de
  nginx en el servidor
- `backend/app/api/permisos.py` — `EscrituraRequiereAdmin`
- `frontend/src/services/usuarios.service.ts`,
  `frontend/src/hooks/useUsuarioMutations.ts` — fix del bug (1), sin
  commitear todavía en el working tree de `colflux/frontend`

## Historial

| Fecha | Descripción |
|---|---|
| 2026-09-15 | Se crea la tarea al encontrar el Basic Auth de nginx bloqueando el guardado en producción, durante la verificación del flujo de cambio de rol de usuario desde `/team`. Se pospone para mañana por falta de acceso SSH en este entorno. |
