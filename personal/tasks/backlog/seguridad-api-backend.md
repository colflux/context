# Endurecer la seguridad de la API del backend (permission_classes reales)

**Estado:** pendiente
**Creada:** 2026-09-14

## Objetivo

Que la API Django (`/api/...`) exija autenticación/autorización real en los
endpoints que mutan datos, en vez de estar completamente abierta.

## Contexto

Sale de [[implementar-login-real]]: se construyó login real (usuario +
contraseña, token vía DRF `TokenAuthentication`) para el frontend, pero
**a propósito quedó fuera de alcance** endurecer el backend — se documentó
explícitamente como gap de seguridad conocido.

Hoy `DataPortalModelViewSet` (`app/api/base.py`) usa
`permission_classes = [AllowAny]` para todos los ViewSets (`fuentes-datos`,
`proyectos`, `instituciones`, etc.), así que cualquier cliente que llame a
la API directamente (curl, Postman) puede crear/editar/borrar datos sin
token, sin importar lo que la UI del frontend restrinja. La única
excepción ya implementada es `UsuarioViewSet`: el campo `password` (que
habilita loguearse como ese usuario) sí exige sesión autenticada vía
`BloquearPasswordAnonima` (`app/api/usuario/views.py`).

## Plan

- [ ] Decidir el criterio: ¿todos los endpoints mutantes requieren token
      (`IsAuthenticated`), o solo los que tocan datos sensibles
      (usuarios, instituciones, eliminar fuentes/proyectos)?
- [ ] Decidir si se necesita un esquema de permisos por rol (ej. solo
      `admin_datos` puede eliminar) replicado en el backend, no solo en
      el frontend (`useRolActual`/`isAdmin`) como hoy
- [ ] Implementar `permission_classes` por ViewSet/endpoint según el
      criterio definido
- [ ] Verificar que el frontend siga funcionando (manda `Authorization:
      Token` donde haga falta) sin romper flujos ya migrados

## Referencias

- [[implementar-login-real]]
