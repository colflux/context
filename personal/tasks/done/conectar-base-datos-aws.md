# Conectar la base de datos de AWS (colflux-DB) al backend

**Estado:** cerrada
**Creada:** 2026-09-15
**Cerrada:** 2026-09-15

## Objetivo

Conectar el backend de COLFLUX (Django) a la instancia gestionada de PostgreSQL/PostGIS en AWS (Lightsail managed database "colflux-DB", endpoint `*.rds.amazonaws.com`), tanto en el entorno local como en producción (`44.213.47.34`), reemplazando el Postgres que corría suelto en un contenedor Docker.

## Contexto

La tarea ya se había empezado en una sesión anterior: el `.env` local de `~/colflux/backend` ya apuntaba a `colflux-DB` y existía un archivo `personal/tasks/inprogress/.credenciales` (gitignoreado) con las credenciales del RDS y de las cuentas de prueba. Esta sesión retomó desde ahí.

En el camino aparecieron varios problemas de infraestructura no previstos que se resolvieron como parte de la misma tarea:
- El deploy automático (GitHub Actions → Lightsail vía SSH) estaba **completamente roto** desde hacía días: el secret `LIGHTSAIL_APP_PATH` tenía un valor inválido, así que cada deploy fallaba en el primer `cd` y no hacía nada — pero el workflow igual quedaba en verde porque no usa `set -e` y el smoke test pasaba contra el contenedor viejo que ya estaba corriendo.
- El `.env` de producción tenía la `DATABASE_URL` del RDS corrupta (truncada a la mitad, probablemente por un problema de wrap al pegar en `nano`).
- `create_admin_from_env` (comando que crea el superusuario desde variables de entorno) existía pero **nunca se invocaba** en `docker-compose.yml`.
- El superusuario creado por ese comando solo podía loguearse en `/admin/` (login por username), no en el frontend (login por correo, contra un modelo `Usuario` de dominio separado) — no había vínculo entre ambos.
- Durante la revisión de roles de usuario, se decidió rediseñar el sistema de roles múltiples (M2M, sin jerarquía) a un nivel único en cascada: `ciudadano < investigador < reportador < admin`.

## Plan

- [x] Verificar/completar la conexión del backend local a `colflux-DB`
- [x] Quitar el fallback silencioso de `DATABASE_URL` en `docker-compose.yml` (fallaba en silencio a una db local vacía si faltaba la variable)
- [x] Agregar smoke test post-deploy al workflow de GitHub Actions
- [x] Quitar el Postgres local de Docker Compose (servicio `db`, ya no se usa) y limpiar el contenedor/volumen viejo en el servidor
- [x] Invocar `create_admin_from_env` en el comando de arranque del contenedor (antes no se ejecutaba nunca)
- [x] Vincular un `Usuario` de dominio al superusuario del `.env`, para que pueda loguearse también por el frontend (no solo por `/admin/`)
- [x] Diagnosticar y corregir el secret roto `LIGHTSAIL_APP_PATH` (causa raíz de que el deploy automático no actualizara nada en el servidor)
- [x] Rediseñar roles de usuario a un nivel único en cascada (ciudadano/investigador/reportador/admin), con permisos reales aplicados en los endpoints de subir/descargar datos y gestión de usuarios
- [x] Adaptar el frontend al nuevo shape de la API (`nivel` en vez de `roles`)
- [x] Aplicar la migración de datos en `colflux-DB` (mapea los roles existentes al nivel más alto correspondiente)
- [ ] **Pendiente (no bloqueante, seguimiento en `TODAY.md`):** probar end-to-end en producción tras el último deploy — login de `colflux-admin` en `/admin/` y en el frontend, `/team` con el selector de nivel nuevo, y que subir/descargar datos respete la cascada

## Entregables

**Backend (`colflux/backend`):**
- [PR #10](https://github.com/colflux/backend/pull/10) — Conectar backend a RDS (colflux-DB) y blindar el deploy: fix de `unquote()` para contraseñas con caracteres especiales, fallback fuerte en `docker-compose.yml`, smoke test en `deploy.yml`, quitar Postgres local de Docker Compose.
- [PR #11](https://github.com/colflux/backend/pull/11) — Invocar `create_admin_from_env` en cada deploy (antes no se llamaba) y vincular un `Usuario` de dominio al superusuario, para que pueda loguearse también por `/api/auth/login/` (correo), no solo por `/admin/` (username).
- [PR #12](https://github.com/colflux/backend/pull/12) — Reemplazar roles múltiples (M2M `Usuario.roles`) por `Usuario.nivel` en cascada (`ciudadano < investigador < reportador < admin`). Nuevo `app/api/permisos.py` con `requiere_nivel`/`EscrituraRequiereNivel`, aplicado a: subir datos (reportador+), descargar (investigador+), gestión de usuarios/roles (admin). Migración `0088_usuario_nivel_acceso.py` aplicada en `colflux-DB`.
- Secret `LIGHTSAIL_APP_PATH` corregido en GitHub (`colflux/backend` → Settings → Secrets) a `/home/ubuntu/colflux/backend` — el deploy automático ya funciona de punta a punta, verificado con un re-run real que sí actualizó código en el servidor.
- Superusuario `colflux-admin` con contraseña segura generada (guardada por Viviana, no queda en este documento ni en el historial de chat más allá de su generación).

**Frontend (`colflux/frontend`):**
- [PR #12](https://github.com/colflux/frontend/pull/12) — Adaptar la UI al nuevo shape `nivel` (string) en vez de `roles` (lista): tipos, `useRolActual` (con `tieneNivel`/`puedeDescargar`/`puedeSubirDatos`), menú de usuario, tabla y drawer de gestión de usuarios.

**Estado final de `colflux-DB`:** los 3 usuarios existentes al momento de migrar quedaron en `nivel: admin` (tenían `admin_datos` o eran superusuarios de Django). Tabla `UsuarioRol` eliminada.

## Referencias

- `personal/tasks/inprogress/.credenciales` — credenciales del RDS y cuentas de prueba (gitignoreado, no versionado)
- [[automatizar-deploy-ecosistema-colflux]] — tarea previa que dejó documentado el pipeline de deploy que se terminó de arreglar aquí (el bug de `LIGHTSAIL_APP_PATH` es la causa raíz de la nota pendiente de esa tarea sobre confirmar el disparo 100% automático)
- `docs/arquitectura/repositorios.md` — inventario de repos (`backend`, `frontend`, `context`)

## Historial

| Fecha | Descripción |
|---|---|
| 2026-09-15 | Se retoma la tarea de una sesión anterior. Se confirma la conexión local a RDS, se resuelven en cadena: fallback silencioso de `DATABASE_URL`, limpieza del Postgres local en Docker, invocación faltante de `create_admin_from_env`, vínculo Usuario↔superusuario para login por correo, y el bug del secret `LIGHTSAIL_APP_PATH` que tenía roto el deploy automático desde hacía días. Se rediseñan los roles a un nivel único en cascada (ciudadano/investigador/reportador/admin) con permisos reales, en backend y frontend. Se aplica la migración en `colflux-DB`. Los 4 PRs (`backend` #10, #11, #12; `frontend` #12) quedan mergeados. Se cierra la tarea con la verificación end-to-end en producción como pendiente de seguimiento, no bloqueante. |
