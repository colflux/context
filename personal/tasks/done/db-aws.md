# Conectar la base de datos de AWS (colflux-DB) al backend

**Estado:** cerrada
**Creada:** 2026-09-15
**Cerrada:** 2026-09-15 (segunda vez, tras corregir la migración incompleta)

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
- [x] **Reabierto (2026-09-15):** crear el `Usuario` de dominio faltante y vincularlo a `lviviana13@gmail.com` — se creó `app_usuario` id 3 (`nivel: admin`) vinculado a `auth_user_id=10` (`colflux-admin`); se eliminó la cuenta duplicada `viviana` (`auth_user_id=2`, sin `Usuario` de dominio ni otras dependencias salvo un `authtoken_token` también eliminado), para no dejar dos `auth_user` con el mismo correo
- [x] **Pendiente de verificar:** login real en el frontend con `colflux-admin` + su contraseña, ahora que existe el vínculo — confirmado por Viviana, ya funciona
- [x] **Reabierto (2026-09-15):** `app_rolusuario` — se confirma que **sí hace falta**, la afirmación original del documento era imprecisa. Lo que se eliminó en `0088_usuario_nivel_acceso.py` fue el M2M `Usuario.roles` (tabla intermedia `app_usuario_roles`), no el catálogo `RolUsuario`/`app_rolusuario`, que sigue en uso activo para `ProyectoUsuario.rol` (rol de cada usuario dentro de un proyecto — coordinador/investigador/técnico —, concepto distinto al nivel de acceso global). No se toca.
- [x] **Reabierto (2026-09-15):** `auth_user_id=7` (`vivianabautista.xyz@gmail.com`) — sin `Usuario` de dominio, sin `last_login`, sin ninguna dependencia (grupos, permisos, admin log, token). Se elimina la cuenta por no tener uso.

## Entregables

**Backend (`colflux/backend`):**
- [PR #10](https://github.com/colflux/backend/pull/10) — Conectar backend a RDS (colflux-DB) y blindar el deploy: fix de `unquote()` para contraseñas con caracteres especiales, fallback fuerte en `docker-compose.yml`, smoke test en `deploy.yml`, quitar Postgres local de Docker Compose.
- [PR #11](https://github.com/colflux/backend/pull/11) — Invocar `create_admin_from_env` en cada deploy (antes no se llamaba) y vincular un `Usuario` de dominio al superusuario, para que pueda loguearse también por `/api/auth/login/` (correo), no solo por `/admin/` (username).
- [PR #12](https://github.com/colflux/backend/pull/12) — Reemplazar roles múltiples (M2M `Usuario.roles`) por `Usuario.nivel` en cascada (`ciudadano < investigador < reportador < admin`). Nuevo `app/api/permisos.py` con `requiere_nivel`/`EscrituraRequiereNivel`, aplicado a: subir datos (reportador+), descargar (investigador+), gestión de usuarios/roles (admin). Migración `0088_usuario_nivel_acceso.py` aplicada en `colflux-DB`.
- Secret `LIGHTSAIL_APP_PATH` corregido en GitHub (`colflux/backend` → Settings → Secrets) a `/home/ubuntu/colflux/backend` — el deploy automático ya funciona de punta a punta, verificado con un re-run real que sí actualizó código en el servidor.
- Superusuario `colflux-admin` con contraseña segura generada (guardada por Viviana, no queda en este documento ni en el historial de chat más allá de su generación).

**Frontend (`colflux/frontend`):**
- [PR #12](https://github.com/colflux/frontend/pull/12) — Adaptar la UI al nuevo shape `nivel` (string) en vez de `roles` (lista): tipos, `useRolActual` (con `tieneNivel`/`puedeDescargar`/`puedeSubirDatos`), menú de usuario, tabla y drawer de gestión de usuarios.

**Estado final de `colflux-DB` (corregido 2026-09-15):** 3 `auth_user` en producción — `colflux-admin` (`lviviana13@gmail.com`, `nivel: admin`, ahora con `Usuario` de dominio vinculado), `malejandragonzalez@javeriana.edu.co` y `ubaques.daniel@javeriana.edu.co`. Se eliminaron 2 cuentas sin uso real: `viviana` (duplicada de `colflux-admin`, mismo correo) y `vivianabautista.xyz@gmail.com` (sin `Usuario` vinculado, sin `last_login`). El M2M `Usuario.roles` fue eliminado por la migración `0088`, pero el catálogo `RolUsuario`/`app_rolusuario` **no** se eliminó — sigue en uso para `ProyectoUsuario.rol` (rol dentro de un proyecto, distinto al nivel de acceso global).

## Referencias

- `personal/tasks/inprogress/.credenciales` — credenciales del RDS y cuentas de prueba (gitignoreado, no versionado)
- [[automatizar-deploy-ecosistema-colflux]] — tarea previa que dejó documentado el pipeline de deploy que se terminó de arreglar aquí (el bug de `LIGHTSAIL_APP_PATH` es la causa raíz de la nota pendiente de esa tarea sobre confirmar el disparo 100% automático)
- `docs/arquitectura/repositorios.md` — inventario de repos (`backend`, `frontend`, `context`)

## Historial

| Fecha | Descripción |
|---|---|
| 2026-09-15 | Se retoma la tarea de una sesión anterior. Se confirma la conexión local a RDS, se resuelven en cadena: fallback silencioso de `DATABASE_URL`, limpieza del Postgres local en Docker, invocación faltante de `create_admin_from_env`, vínculo Usuario↔superusuario para login por correo, y el bug del secret `LIGHTSAIL_APP_PATH` que tenía roto el deploy automático desde hacía días. Se rediseñan los roles a un nivel único en cascada (ciudadano/investigador/reportador/admin) con permisos reales, en backend y frontend. Se aplica la migración en `colflux-DB`. Los 4 PRs (`backend` #10, #11, #12; `frontend` #12) quedan mergeados. Se cierra la tarea con la verificación end-to-end en producción como pendiente de seguimiento, no bloqueante. |
| 2026-09-15 (reapertura) | Al intentar loguearse con `lviviana13@gmail.com` en producción, falla con 401. Se consulta `colflux-DB` directamente (vía `psycopg`, usando `dbmasteruser`, ya que el ORM local no levanta por falta de GDAL) y se confirma que la migración quedó **incompleta**: `auth_user` tiene 5 filas (`viviana` id 2, `vivianabautista.xyz@gmail.com` id 7, `malejandragonzalez@...` id 9, `colflux-admin` id 10, `ubaques.daniel@...` id 14), pero `app_usuario` (el modelo de dominio que usa el login del frontend, `POST /api/auth/login/` busca por `Usuario.correo`) solo tiene 2 filas, vinculadas a los `auth_user` 14 y 9. **No existe `Usuario` de dominio para `viviana`/`colflux-admin` (id 2 y 10) ni para el id 7** — de ahí el 401, aunque el `auth_user` y su contraseña sí existan. Además, `app_rolusuario` sigue existiendo con 5 filas en `colflux-DB`, contradiciendo la afirmación de este documento de que la tabla se había eliminado. Se reabre la tarea con estos 3 pendientes. |
| 2026-09-15 (corrección) | Se crea el `Usuario` de dominio faltante (`app_usuario` id 3, `nivel: admin`) vinculado a `colflux-admin` (`auth_user_id=10`), correo `lviviana13@gmail.com`. Se elimina la cuenta Django duplicada `viviana` (`auth_user_id=2`, mismo correo, sin `Usuario` de dominio propio) junto con su `authtoken_token`, para dejar una sola cuenta por correo. Queda pendiente confirmar el login real desde el frontend con `colflux-admin`. |
| 2026-09-15 (cierre de hallazgos) | Se revisa `app_rolusuario`: la afirmación original de este documento ("Tabla UsuarioRol eliminada") era imprecisa — lo que se eliminó fue el M2M `Usuario.roles` (tabla intermedia), no el catálogo `RolUsuario`, que sigue en uso para `ProyectoUsuario.rol` (rol dentro de un proyecto, no nivel de acceso global). No se elimina la tabla. Se elimina la cuenta `auth_user_id=7` (`vivianabautista.xyz@gmail.com`): sin `Usuario` de dominio, sin `last_login`, sin dependencias. Solo queda pendiente confirmar el login end-to-end de `colflux-admin` en el frontend. |
