# Agregar opción de registro (crear cuenta) además del login

**Estado:** pendiente
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

## Plan

- [ ] Decidir con el usuario el modelo de registro (abierto vs. completar
      cuenta existente, datos mínimos, verificación de correo sí/no)
- [ ] Backend: `RegistroView` en `app/api/auth/views.py` + ruta
      `POST /api/auth/registro/` en `app/api/urls.py`
- [ ] Backend: throttle scope para registro (evitar abuso)
- [ ] Frontend: `authService.registro(...)` en `auth.service.ts`
- [ ] Frontend: `useRegistro` (mutation) en `hooks/useAuth.ts`
- [ ] Frontend: opción "Registrarse" en `LoginModal.tsx` (o modal nuevo
      `RegistroModal.tsx`) enlazada desde `LoginButton.tsx`
- [ ] Verificación end-to-end con backend real

## Entregables

(Pendiente — tarea aún no iniciada.)

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
