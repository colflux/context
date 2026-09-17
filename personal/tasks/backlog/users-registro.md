# Agregar opción de registro (crear cuenta) además del login

**Estado:** completada
**Creada:** 2026-09-14

## Objetivo

Permitir que un usuario pueda crear su propia cuenta de acceso (registro
self-service), en vez de depender de que un admin le asigne una contraseña
manualmente desde `/team` → `UsuarioDrawer`. Complementa el login real ya
implementado en [[implementar-login-real]] (`context/personal/tasks/inprogress/implementar-login-real.md`).

## Contexto

Al revisar el backend (`colflux/backend`, proyecto Django) para agregar el
registro se confirmó que **no existe ningún endpoint de registro hoy**: solo
`POST /api/auth/login/`, `POST /api/auth/logout/`, `GET /api/auth/me/`
(`app/api/auth/views.py`). El único camino actual para que alguien tenga
credenciales es que un admin le asigne una contraseña vía el campo
"Contraseña de acceso" en `UsuarioDrawer` (que llama a
`UsuarioSerializer` con `password` write-only).

Preguntas de diseño pendientes de decidir con el usuario antes de
implementar (mismo patrón de decisiones que se tomó para el login real):

- ¿Registro abierto a cualquier correo, o solo para completar una cuenta de
  un `Usuario` que ya existe en la base (nombre/institución ya cargados por
  un admin, pero sin `auth_user`/contraseña todavía)? Esto último es
  consistente con cómo está modelado `Usuario` hoy (ver
  `app/models/datos.py`, campo `auth_user` opcional).
- Si es registro abierto: ¿qué datos mínimos se piden (nombre, correo,
  institución, rol) y quién aprueba/asigna rol después — se crea sin roles
  y un admin se los asigna manualmente?
- ¿Verificación de correo (requiere SMTP, no configurado todavía — mismo
  problema que se descartó para login por link mágico) o registro directo
  sin verificación?
- ¿Rate limiting / throttle en el endpoint de registro (como ya tiene
  `LoginView` con `ScopedRateThrottle`), para evitar creación masiva de
  cuentas?

## Decisiones de diseño (2026-09-15)

- **Registro abierto**, no "completar cuenta existente": cualquiera crea su
  `Usuario` desde cero con nombre, correo y contraseña. Institución/cargo
  quedan vacíos y el usuario o un admin los completa después.
- **Rol por defecto: `basico`** (rol nuevo, no existía — hoy el catálogo
  es `reportador`/`coordinador`/`investigador`/`admin_datos`). El registro
  self-service **no permite elegir rol**; siempre asigna `basico`. Un admin
  sube el rol después desde `/team` → `UsuarioDrawer` (ya soportado, el
  `UsuarioSerializer.roles` acepta reasignar roles en `update`).
- **Sin verificación de correo**: mismo motivo que se descartó para login
  por link mágico (no hay SMTP configurado). Registro queda activo de
  inmediato tras crear la cuenta (auto-login, como el login normal).
- **Throttle** en el endpoint de registro (`ScopedRateThrottle`, scope
  `registro`), mismo patrón que `LoginView` con scope `login`, para evitar
  creación masiva de cuentas.
- El endpoint de registro es uno **nuevo y separado** de
  `POST /api/usuarios/` (que ya bloquea a anónimos setear `password` vía
  `BloquearPasswordAnonima`, ver `app/api/usuario/views.py`) — no se toca
  ese endpoint ni su gate existente. `RegistroView` es `AllowAny` pero
  fuerza el rol `basico` sin importar qué mande el cliente, así no sirve
  como vía alterna para auto-asignarse roles con privilegios.

## Plan

- [x] Decidir con el usuario el modelo de registro (registro abierto, rol
      básico por defecto, admin sube roles después, sin verificación de
      correo)
- [x] Backend: migración que agrega el rol `basico` al catálogo
      `RolUsuario`
- [x] Backend: `RegistroView` en `app/api/auth/views.py` + ruta
      `POST /api/auth/registro/` en `app/api/urls.py`
- [x] Backend: throttle scope `registro` en `settings.py`
- [x] Frontend: `authService.registro(...)` en `auth.service.ts`
- [x] Frontend: `useRegistro` (mutation) en `hooks/useAuth.ts`
- [x] Frontend: opción "Registrarse" en `LoginModal.tsx` (toggle
      login/registro en el mismo modal) enlazada desde `LoginButton.tsx`
- [x] Verificación end-to-end con backend real

## Entregables

- `backend/app/migrations/0087_seed_rol_basico.py` — agrega el rol
  `basico` al catálogo `RolUsuario`.
- `backend/app/api/auth/views.py` — `RegistroView` (`AllowAny`, throttle
  `registro`, ignora cualquier `roles` que mande el cliente y siempre
  asigna `basico`).
- `backend/app/api/urls.py`, `backend/colflux/settings.py` — ruta
  `POST /api/auth/registro/` y rate `registro: 5/min`.
- `frontend/src/services/auth.service.ts`, `hooks/useAuth.ts` —
  `authService.registro(...)`, `useRegistro`.
- `frontend/src/components/layout/LoginModal.tsx` — toggle
  "¿No tienes cuenta? Regístrate" / "¿Ya tienes cuenta? Inicia sesión" en
  el mismo modal (evita crear un `RegistroModal.tsx` separado).

## Verificación (2026-09-15)

Vía Docker (`docker compose up -d --build`) contra backend real:

- Registro crea el `Usuario` + `auth.User` + token, con rol `basico`
  únicamente (`HTTP 201`).
- Login inmediato con las credenciales recién creadas funciona
  (`HTTP 200`).
- Registro con correo ya usado responde `HTTP 400` ("Ya existe una cuenta
  con este correo.").
- Registro sin nombre/correo/contraseña responde `HTTP 400`.
- Enviar `"roles": ["admin_datos"]` en el body del registro se ignora — la
  cuenta queda igual con solo `basico` (confirma que el endpoint no sirve
  como vía de escalada de privilegios).
- Throttle `registro` (5/min) confirmado: el 6º intento en la misma
  ventana responde `HTTP 429`.
- `tsc --noEmit` sin errores en frontend.
- Datos de prueba limpiados (usuarios + `auth.User` huérfanos) vía shell
  de Django antes de bajar los contenedores.

**Pendiente para una tarea aparte:** el gap de seguridad ya documentado en
[[implementar-login-real]] sigue aplicando — la API de `UsuarioViewSet`
sigue siendo `AllowAny` salvo el campo `password`; un usuario con rol
`basico` no tiene hoy ninguna restricción real a nivel de backend más allá
de lo que el frontend le muestre en la UI.

## Referencias

- [[implementar-login-real]] — login real ya implementado, mismo módulo
  `app/api/auth/` y mismo patrón de store/hooks en frontend.
- `app/api/auth/views.py` (backend) — endpoints actuales de auth.
- `src/components/layout/LoginModal.tsx`,
  `src/components/layout/LoginButton.tsx`,
  `src/hooks/useAuth.ts`,
  `src/services/auth.service.ts` (frontend) — puntos de extensión.

## Historial

| Fecha | Descripción |
|---|---|
| 2026-09-14 | Se crea la tarea a partir del pedido del usuario de agregar una opción de registro. Se revisó el backend y se confirmó que no existe endpoint de registro; se documentan las preguntas de diseño pendientes antes de implementar. |
| 2026-09-15 | El usuario confirma las decisiones de diseño pendientes: registro abierto (no completar cuenta existente), rol `basico` fijo por defecto (nuevo rol, no elegible por el usuario), admin sube el rol después desde `/team`, sin verificación de correo. Se implementa y verifica de punta a punta: migración que agrega `basico` al catálogo `RolUsuario`; `RegistroView` (`AllowAny`, throttle `registro` 5/min, ignora cualquier `roles` recibido) en `app/api/auth/`; ruta `POST /api/auth/registro/`; frontend `authService.registro`, `useRegistro`, toggle "Regístrate"/"Inicia sesión" agregado dentro de `LoginModal.tsx` (sin crear un modal separado). Verificado vía Docker contra backend real: registro exitoso con rol único `basico`, login inmediato con las credenciales creadas, rechazo de correo duplicado y de campos faltantes, intento de inyectar `roles: ["admin_datos"]` en el body ignorado, throttle confirmado (6º intento en la ventana da 429). `tsc --noEmit` sin errores. Datos de prueba limpiados. Se cierra la tarea; queda señalado (no en alcance) que el gap de seguridad de `implementar-login-real` sigue vigente: la API de `UsuarioViewSet` sigue siendo pública salvo el campo `password`. |
