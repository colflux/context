# Implementar recuperación de contraseña por correo

**Estado:** completada
**Creada:** 2026-09-18
**Cerrada:** 2026-09-20
**A cargo:** Viviana Bautista
**Sesión de Claude Code:** https://claude.ai/code/session_01NSAELkQ8eyUGzuTRTRcz7T
(para retomar esta misma sesión si se cierra la ventana — tiene todo
el contexto de lo avanzado hasta el 2026-09-20)
**PRs:** backend https://github.com/colflux/backend/pull/19 · frontend
https://github.com/colflux/frontend/pull/22 (ambos abiertos desde la
rama `feat/recuperar-contrasena-correo`, código listo y probado
end-to-end; pendiente el merge en sí, que queda fuera del alcance de
esta tarea)

## Objetivo

Reemplazar el procedimiento manual de reseteo de contraseña vía SSH
([[users-admin-credenciales]]) por un flujo self-service de "olvidé mi
contraseña" con envío de correo, para que ningún usuario (admin o no)
dependa de acceso al servidor de producción para recuperar su cuenta.

## Contexto

Surge directamente de [[users-admin-credenciales]]: Viviana (admin, ID
3) perdió el acceso más de una vez y cada vez requirió `docker exec` en
`backend-web` en producción. Se decidió implementar el flujo real en
vez de seguir dependiendo del procedimiento manual.

Repo real del código: `/Users/vivianabautista.xyz/colflux/backend`
(Django 5.0.7 + DRF 3.15.2, con PostGIS). El frontend está en
`/Users/vivianabautista.xyz/colflux/frontend` (React + Vite).

### Hallazgos de la exploración del backend (2026-09-18)

- La app de dominio es simplemente `app` (no está separada en
  `users`/`accounts`). Modelo `Usuario` en `app/models/datos.py:22`,
  ligado 1-a-1 a `auth.User` vía el campo `auth_user` (líneas 52-59).
- Serializer `UsuarioSerializer` en
  `app/api/usuario/serializers.py:35-139`, con un método
  `_sincronizar_login()` (líneas 67-100) que ya sincroniza cambios
  hacia `auth.User` — hay que reutilizarlo o replicar su patrón al
  cambiar la contraseña desde el nuevo flujo.
- Auth es 100% custom vía DRF, **no** usa
  `django.contrib.auth.views` (nada de `PasswordResetView` de
  Django). Autenticación por `TokenAuthentication`
  (`rest_framework.authtoken`).
- Vistas de auth existentes en `app/api/auth/views.py`: `LoginView`
  (L16), `RegistroView` (L41), `LogoutView` (L88), `MeView` (L97).
  Patrón: `APIView` + `AllowAny` + throttling por scope
  (`"login"`, `"registro"`).
- URLs en `app/api/urls.py:38-41`, bajo el prefijo `/api/auth/`.
- Campos de contacto disponibles en `Usuario`: `correo` (personal) y
  `correo_institucional` (`app/models/datos.py:39-40`).
- **No hay configuración de email** en `colflux/settings.py` (sin
  `EMAIL_BACKEND`, `EMAIL_HOST`, etc.) ni en `.env.example`. Hay que
  configurarlo desde cero.
- **No hay suite de tests** en el proyecto (sin `pytest`/`unittest`),
  así que el nuevo flujo tampoco tendrá tests automáticos a menos que
  se decida introducir la suite como parte de esta tarea (fuera de
  alcance por ahora).

### Pendiente de decisión: proveedor de correo

Al 2026-09-18 no hay proveedor de email definido ni credenciales SMTP.
Opciones típicas para un proyecto de este tamaño:

- **Desarrollo/local:** `django.core.mail.backends.console.EmailBackend`
  (imprime el correo en consola, no requiere credenciales).
- **Producción:** un SMTP real. Opciones comunes: Gmail SMTP con
  contraseña de aplicación (rápido de configurar, límites bajos),
  SendGrid o Mailgun (mejor para producción, requieren cuenta y
  dominio verificado), o Amazon SES (barato, requiere verificar
  dominio/salir de sandbox).

  Esto lo debe decidir el equipo/Viviana antes de desplegar a
  producción. El diseño del flujo es independiente del proveedor
  elegido (solo cambian las variables de entorno de `EMAIL_*`).

## Diseño propuesto

1. **Modelo `PasswordResetToken`** (nuevo, en `app/models/`):
   - `usuario` (FK a `auth.User` o a `Usuario`, a definir según cuál
     conviene más dado el patrón de sincronización existente)
   - `token` (UUID, único)
   - `creado_en`, `expira_en` (ej. válido 1 hora)
   - `usado` (bool, default `False`)

2. **`POST /api/auth/forgot-password/`** (`ForgotPasswordView`, mismo
   patrón `APIView` + `AllowAny` + throttling que `LoginView`):
   - Recibe `email` (buscar contra `correo` o `correo_institucional`
     de `Usuario`, o contra `auth.User.email`, a confirmar cuál es la
     fuente de verdad).
   - Si existe, crea un `PasswordResetToken` y envía correo con link
     `FRONTEND_URL/reset-password?token=<uuid>`.
   - **Responde siempre 200 igual exista o no el correo**, para no
     filtrar qué correos están registrados (enumeration attack).

3. **`POST /api/auth/reset-password/`** (`ResetPasswordView`):
   - Recibe `token` + `nueva_contraseña` (+ confirmación).
   - Valida que el token exista, no esté usado y no haya expirado.
   - Actualiza la contraseña reutilizando el patrón de
     `_sincronizar_login()` del serializer.
   - Marca el token como `usado`.

4. **Frontend** (`colflux/frontend`): pantalla "olvidé mi contraseña"
   (formulario de email) + pantalla "nueva contraseña" (recibe el
   `token` por query param). Fuera de alcance de la exploración inicial
   — falta revisar el repo de frontend para ver dónde encaja con el
   router y el login actual.

5. **Configuración de email en `colflux/settings.py`**: agregar
   `EMAIL_BACKEND`, `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`,
   `EMAIL_HOST_PASSWORD`, `EMAIL_USE_TLS`, `DEFAULT_FROM_EMAIL` como
   variables de entorno (`.env` / `.env.example`), no hardcodeadas.

## Plan

- [x] Ubicar el código real (repo `backend`) y confirmar que no existe
      ya un flujo de reset ni configuración de email
- [x] Diseñar el flujo (modelo, endpoints, reutilización de
      `_sincronizar_login()`)
- [x] Decidir proveedor de correo para el prototipo: **Gmail SMTP**
      con contraseña de aplicación, remitente `colflux.plataforma@gmail.com`
      (gratis, ~500 correos/día, sin tarjeta). Migrar a un proveedor
      transaccional (ej. Brevo, 300/día gratis) cuando crezca el
      volumen — el código no cambia, solo las variables `EMAIL_*`.
- [x] Implementar `PasswordResetToken` + migración en `backend`
      (`app/migrations/0091_passwordresettoken.py`, aplicada
      2026-09-18 contra la RDS compartida — migración puramente
      aditiva, `CREATE TABLE`, sin riesgo para datos existentes)
- [x] Implementar `ForgotPasswordView` y `ResetPasswordView` en
      `app/api/auth/views.py`, registradas en `app/api/urls.py` como
      `POST /api/auth/forgot-password/` y `POST /api/auth/reset-password/`
- [x] Configurar `EMAIL_*` en `colflux/settings.py` + `.env.example`
      (cae al backend de consola en local si `EMAIL_HOST_USER` está
      vacío, no requiere credenciales para desarrollar)
- [x] Agregar las variables `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`,
      `DEFAULT_FROM_EMAIL` al bloque `environment:` del servicio `web`
      en `docker-compose.yml` (2026-09-20, una vez Viviana resolvió el
      conflicto de merge que no tenía relación con esta tarea)
- [x] Generar la contraseña de aplicación de Gmail para
      `colflux.plataforma@gmail.com` — requirió activar verificación
      en 2 pasos primero; la opción estuvo bloqueada un rato por ser
      cuenta creada el mismo día (restricción antifraude típica de
      Google en cuentas nuevas), se destrabó sola sin esperar tanto
- [x] Cargar las credenciales en `.env` local de `backend` (2026-09-20)
- [x] Implementar pantallas en `frontend`
      (`/Users/vivianabautista.xyz/colflux/frontend`):
      - `LoginModal.tsx` — nuevo modo `olvide` (mismo modal de
        login/registro, sin modal aparte). El link a recuperar
        contraseña **no es fijo**: solo aparece junto al mensaje de
        error cuando el login falla ("¿Olvidaste tu contraseña?
        Recupérala aquí") — se probó primero con un link fijo debajo
        del campo contraseña y se quitó por quedar duplicado con el
        de después del error.
      - `pages/ResetPassword.tsx` (nueva), ruta `/reset-password` en
        `App.tsx` — lee `token` de query param, pide contraseña nueva
        + confirmación.
      - `services/auth.service.ts` y `hooks/useAuth.ts` — métodos
        `forgotPassword`/`resetPassword` y hooks
        `useForgotPassword`/`useResetPassword`, mismo patrón que
        login/registro existentes.
- [x] Probar el flujo en local — confirmado que el backend arma bien
      el correo (se vio completo en los logs del backend de consola
      antes de configurar SMTP real)
- [x] Confirmar que el correo real llega a la bandeja (SMTP de Gmail
      configurado, contenedor reiniciado, desajuste de puertos
      corregido — Viviana confirmó "listo" 2026-09-20)
- [x] Subir la versión de ambos proyectos: `BACKEND_VERSION` y
      `package.json`/footer del frontend a `1.3.0`
- [x] Traer `main` a la rama de trabajo en ambos repos antes de abrir
      PR (se descartó trabajo local viejo del frontend sobre el mapa
      de ecosistemas del home, ya superado por el PR #21 ya mergeado
      en `main`)
- [x] Commit + push + PR en ambos repos, desde una rama nueva
      (`feat/recuperar-contrasena-correo`, no se reusó
      `feat/reportes-modulo-graficas` porque ya estaba mergeada como
      otra cosa)
- [ ] Probar en producción con Gmail SMTP (solo se probó en local; el
      despliegue a producción queda fuera de esta tarea, depende de
      que se mergeen los PRs)
- [ ] Retirar/actualizar el procedimiento manual de
      [[users-admin-credenciales]] una vez este flujo esté en
      producción

## Entregables

**Backend** (`/Users/vivianabautista.xyz/colflux/backend`):

- `app/models/datos.py` — modelo `PasswordResetToken`
- `app/models/__init__.py` — export del modelo nuevo
- `app/migrations/0091_passwordresettoken.py` — migración generada y
  **aplicada** (2026-09-18) contra la RDS compartida (aditiva,
  `CREATE TABLE`, sin riesgo para datos existentes)
- `app/api/auth/views.py` — `ForgotPasswordView`, `ResetPasswordView`
- `app/api/urls.py` — rutas `forgot-password/` y `reset-password/`
- `colflux/settings.py` — config `EMAIL_*` y throttle rates nuevos
- `.env.example` — variables `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`,
  `DEFAULT_FROM_EMAIL` documentadas
- `docker-compose.yml` — variables `EMAIL_*` pasadas al contenedor
  `web`
- `.env` local — credenciales de Gmail cargadas (colflux.plataforma@gmail.com)

**Frontend** (`/Users/vivianabautista.xyz/colflux/frontend`):

- `src/components/layout/LoginModal.tsx` — modo `olvide`
- `src/pages/ResetPassword.tsx` (nuevo)
- `src/App.tsx` — ruta `/reset-password`
- `src/services/auth.service.ts`, `src/hooks/useAuth.ts` — métodos y
  hooks nuevos
- `.env` — se corrigió `VITE_API_BASE_URL`/`VITE_GEO_API_BASE_URL`/
  `VITE_REPORTES_API_BASE_URL` de `localhost:8000` a `localhost:8001`
  (el backend local corre en 8001 por `WEB_PORT=8001` en su `.env`;
  ese desajuste ya existía antes de esta tarea y no era exclusivo del
  flujo de recuperación — cualquier llamada del frontend al backend
  local estaba fallando con "Failed to fetch"). Nota: 8001 también
  está reservado para `ia-functions` en `VITE_API_URL`; no es
  problema hoy porque ese servicio no está desplegado, pero si algún
  día corre localmente en paralelo, habrá que reasignar puertos.

Verificado con `docker exec backend-web-1 python manage.py check` (sin
errores), `showmigrations` (0091 aplicada), `tsc -b` y `eslint` en el
frontend (sin errores). El correo de prueba se vio completo en los
logs del backend de consola (asunto, remitente, link con token) antes
de tener SMTP real configurado, y luego se confirmó recepción real en
Gmail una vez cargadas las credenciales y corregido el desajuste de
puertos local.

**PRs abiertos (código listo, pendiente merge):**
- Backend: https://github.com/colflux/backend/pull/19
- Frontend: https://github.com/colflux/frontend/pull/22

## Riesgos / cosas a vigilar

- **Cuenta `colflux.plataforma@gmail.com` es nueva** (creada
  2026-09-18): Gmail limita ~500 correos/día y puede tener
  restricciones adicionales las primeras semanas por ser cuenta
  nueva. Si el volumen crece o hay problemas de entrega, migrar a
  Brevo (300/día gratis, sin este tipo de fricción) — el código no
  cambia, solo las variables `EMAIL_*`.
- El conflicto de merge que apareció en `backend` a mitad de esta
  tarea (en `app/api/geo/views.py` y `docker-compose.yml`, por un
  `git pull` automático de fondo) no tenía relación con este trabajo;
  Viviana lo resolvió por su cuenta y quedó commiteado como
  `feat(reportes): endpoints agregados para el módulo de gráficas del
  geoportal` (`8e2f249`).

## Referencias

- [[users-admin-credenciales]]
- [[asignar-contrasenas-usuarios-reales]]

## Historial

| Fecha | Descripción |
|---|---|
| 2026-09-18 | Se crea la tarea a partir de la necesidad de reemplazar el procedimiento manual de reseteo por SSH. Se explora el repo `backend` (modelo `Usuario`, auth vía DRF/Token, ausencia de config de email) y se documenta el diseño propuesto del flujo (modelo `PasswordResetToken`, endpoints `forgot-password`/`reset-password`, proveedor de correo pendiente de decidir). Se decide Gmail SMTP (`colflux.plataforma@gmail.com`) como proveedor para el prototipo. Se implementa el backend completo (modelo, migración aplicada, vistas, urls, settings) y se verifica con `manage.py check`/`showmigrations`. Durante la sesión un `git pull` de fondo (probablemente autosync del editor) generó un conflicto de merge en `backend` ajeno a esta tarea, que se dejó para que Viviana lo resolviera por su cuenta. |
| 2026-09-20 | Viviana activa verificación en 2 pasos y genera la contraseña de aplicación de Gmail (bloqueada un rato por ser cuenta creada el mismo día). Se implementan las pantallas del flujo en `frontend` (modo `olvide` en `LoginModal`, página `ResetPassword`, servicios y hooks nuevos), verificadas con `tsc`/`eslint`. Se agrega el link de recuperación condicionado al error de login (no fijo, para evitar duplicidad visual). Se cargan las credenciales de Gmail en el `.env` de `backend` y se agregan las variables `EMAIL_*` a `docker-compose.yml`. Al probar el flujo real aparece "Failed to fetch": se detecta un desajuste preexistente de puertos (backend en 8001 por `WEB_PORT`, frontend apuntando a 8000) y se corrige el `.env` del frontend para apuntar a 8001. Viviana confirma que el correo llegó y el flujo funciona. Se sube la versión a `1.3.0` en ambos proyectos, se trae `main` a las ramas de trabajo (descartando trabajo local viejo del frontend ya superado por otro PR mergeado) y se abren los PRs finales: [backend#19](https://github.com/colflux/backend/pull/19) y [frontend#22](https://github.com/colflux/frontend/pull/22). Tarea cerrada — queda pendiente solo el merge de esos PRs y, ya en producción, retirar el procedimiento manual documentado en [[users-admin-credenciales]]. |
