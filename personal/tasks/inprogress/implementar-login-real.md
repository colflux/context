# Implementar login real (reemplazar el selector de sesión simulada)

**Estado:** completada
**Creada:** 2026-09-14

## Objetivo

Reemplazar el `SesionSelector` (dropdown "actuar como" cualquier usuario,
construido durante la migración de `data.html`/`team.html` como paso
intermedio sin login real) por un sistema de autenticación real:
usuario + contraseña, vinculado a un `Usuario` real de la base de datos.

## Contexto

El proyecto no tenía ningún sistema de auth hasta ahora. `django.contrib.auth`
está instalado pero sin usarse (no hay `REST_FRAMEWORK` en `settings.py`, los
viewsets usan `DataPortalModelViewSet` con `permission_classes = [AllowAny]`).
El modelo `Usuario` (`app/models/datos.py`) no tiene contraseña ni relación
con `auth.User`.

Se preguntó al usuario y se confirmaron 3 decisiones de diseño:

1. **Mecanismo:** usuario + contraseña (no link mágico por correo, no
   SSO/Google — ambos requerían infraestructura que no existe, como SMTP
   configurado o credenciales OAuth).
2. **Identificador de login:** correo (`correo` o `correo_institucional`),
   no un username nuevo separado. Implica que un `Usuario` sin correo no
   puede tener login hasta que se le complete ese dato.
3. **Sesión en el SPA:** token simple vía `rest_framework.authtoken`
   (`Authorization: Token <token>`), guardado en `localStorage` vía zustand
   `persist` — igual patrón que `useFuenteDrawerStore`/`useSesionStore` ya
   usan. Se descartó sesión con cookie por la fricción de CSRF entre
   `localhost:3000` (frontend) y `localhost:8000` (backend) en dev, y en
   general para una SPA desacoplada.

## Gap de seguridad explícito (documentado, no se resuelve en esta tarea)

El login solo controla qué ve la UI (gate de `/team`, botón de borrar en
`FuentesTable`). **La API del backend sigue siendo pública** —
`permission_classes = [AllowAny]` en todos los viewsets existentes, sin
cambios. Un cliente que llame a la API directamente (curl, Postman) puede
seguir haciendo todo sin token. Bloquear la API a nivel de backend es una
tarea aparte, mucho más grande (afecta cada endpoint), fuera de alcance
aquí — se señala para que quede claro que este login es una mejora de UX/
control de acceso en el frontend, no un endurecimiento de seguridad del
backend.

## Diseño

### Backend

- `Usuario` (`app/models/datos.py`): nuevo campo
  `auth_user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True,
  blank=True, on_delete=models.SET_NULL, related_name="usuario")`. Un
  `Usuario` sin `auth_user` no puede loguearse (no tiene contraseña
  asignada todavía).
- `rest_framework.authtoken` agregado a `INSTALLED_APPS` (trae el modelo
  `Token`, requiere migración de ese app — no crea migración propia
  nuestra).
- Nuevo módulo `app/api/auth/`:
  - `views.py`: `LoginView` (POST correo+password → token + usuario),
    `LogoutView` (POST, borra el token del usuario autenticado),
    `MeView` (GET, revalida el token y devuelve el usuario actual — se
    usa al cargar la app para restaurar sesión sin volver a pedir
    contraseña).
  - Login busca `Usuario` por `correo` o `correo_institucional`
    (case-insensitive), valida contra `usuario.auth_user.check_password()`.
    Mensaje de error genérico ("Credenciales inválidas") en cualquier
    fallo, sin distinguir "no existe" de "contraseña incorrecta" (evita
    enumeración de correos).
- `UsuarioSerializer` (`app/api/usuario/serializers.py`) extendido con un
  campo `password` (`write_only`, opcional). Si se envía en el
  create/update de un `Usuario` (vía `/api/usuarios/`), crea o actualiza
  el `auth.User` vinculado (`username`/`email` = correo del usuario) y le
  asigna esa contraseña con `set_password`. Esto es lo que permite a un
  administrador (desde `/team`, una vez logueado) asignar o resetear la
  contraseña de acceso de otro usuario, sin una pantalla separada de
  "gestión de credenciales".
- Rutas nuevas en `app/api/urls.py`: `POST /api/auth/login/`,
  `POST /api/auth/logout/`, `GET /api/auth/me/`.

### Frontend

- `services/auth.service.ts`: `login(correo, password)`, `logout()`,
  `me()`.
- `store/useAuthStore.ts` (zustand + `persist`, reemplaza
  `useSesionStore.ts` que se elimina): `{ token, usuario, setSesion,
  cerrarSesion }`, persistido bajo la key `colflux-auth`.
- `hooks/useAuth.ts`: `useLogin` (mutation), `useLogout` (mutation),
  `useMe` (query habilitada solo si hay `token`, revalida al cargar la
  app y limpia el store si el token ya no es válido).
- `hooks/useRolActual.ts`: se simplifica para leer directo de
  `useAuthStore` (usuario + roles ya vienen del login/me, no hay que
  cruzar con `useUsuarios()` como antes).
- `components/layout/SesionSelector.tsx` → se reemplaza por
  `components/layout/LoginButton.tsx` (botón "Iniciar sesión" que abre
  `LoginModal`) + `components/layout/UserMenu.tsx` (nombre + roles debajo,
  igual visual que antes, con acción "Cerrar sesión").
- `components/layout/LoginModal.tsx`: formulario correo + contraseña,
  mensaje de error del backend, cierra al loguear con éxito.
- `components/admin/usuarios/UsuarioDrawer.tsx`: nuevo campo opcional
  "Nueva contraseña" (placeholder "Dejar en blanco para no cambiarla" en
  edición), solo se envía si el admin lo completa.
- `Navbar.tsx`: reemplaza `SesionSelector` por el par
  `LoginButton`/`UserMenu` según haya sesión o no.

## Plan

- [x] Backend: modelo `Usuario.auth_user` + migración
- [x] Backend: `rest_framework.authtoken` en `INSTALLED_APPS` + migrar
- [x] Backend: endpoints `/api/auth/login|logout|me/`
- [x] Backend: `password` en `UsuarioSerializer` (create/update)
- [x] Frontend: `auth.service.ts`, `useAuthStore`, `useAuth.ts`
- [x] Frontend: simplificar `useRolActual`
- [x] Frontend: `LoginModal`, `LoginButton`, `UserMenu`, retirar `SesionSelector`/`useSesionStore`
- [x] Frontend: campo de contraseña en `UsuarioDrawer`
- [x] Verificación end-to-end contra backend real (con credenciales de prueba temporales, no reales)

## Historial

| Fecha | Descripción |
|---|---|
| 2026-09-14 | Se crea la tarea a partir del pedido del usuario de reemplazar el selector de "actuar como" por un login real. Se confirman 3 decisiones de diseño (usuario+contraseña, login por correo, token simple vía DRF TokenAuthentication) y se documenta el gap de seguridad (la API sigue siendo pública sin auth backend, el login solo controla la UI). |
| 2026-09-14 | Se implementa y verifica el login real completo, cerrando la tarea. Backend: campo `Usuario.auth_user` (OneToOne a `auth.User`) + migración; `rest_framework.authtoken` habilitado; módulo `app/api/auth/` con `LoginView`/`LogoutView`/`MeView` (login busca por `correo`/`correo_institucional` case-insensitive, mensaje de error genérico para evitar enumeración de correos); `UsuarioSerializer` extendido con campo `password` write-only que crea/actualiza el `auth.User` vinculado vía `set_password` al crear o editar un usuario desde `/api/usuarios/`. Frontend: `auth.service.ts`, `useAuthStore` (zustand+persist, reemplaza `useSesionStore`), `useAuth.ts` (`useLogin`/`useLogout`/`useMe`, esta última revalida el token al cargar la app); `useRolActual` simplificado para leer directo del store; `LoginModal`/`LoginButton`/`UserMenu` reemplazan `SesionSelector` en `Navbar.tsx` (archivo y store viejos eliminados); campo "Contraseña de acceso" opcional agregado a `UsuarioDrawer` para que un admin asigne/resetee credenciales desde `/team`. Se aprovechó que el correo del usuario real de esta sesión (`lviviana13@gmail.com`, "Viviana Bautista", `admin_datos`+`coordinador`) ya estaba en la base para bootstrapear el primer login de prueba vía shell de Django, con una contraseña temporal que el usuario debe cambiar desde `/team` → editar su propio usuario → "Contraseña de acceso". Verificado en navegador vía Docker con credenciales temporales: login exitoso muestra nombre+roles en el navbar; mensaje "Credenciales inválidas." ante contraseña incorrecta; la sesión persiste tras recargar (`useMe` revalida el token); `/team` accesible logueado como admin y con redirect a `/data` tanto al cerrar sesión estando en `/team` como logueado con un usuario de prueba sin rol `admin_datos`; se creó un usuario de prueba con contraseña desde `UsuarioDrawer` y se confirmó que pudo loguearse con esas credenciales; cerrar sesión invalida el token en el backend (`/api/auth/me/` responde 401 después). Se limpiaron los datos de prueba (usuario temporal + su `auth.User` huérfano, ya que `UsuarioViewSet.destroy` no lo borra en cascada) vía shell de Django. Sin errores de consola. **Gap de seguridad ya documentado:** este login controla la UI, no la API — los endpoints del backend siguen siendo públicos (`AllowAny`) sin cambios. |
