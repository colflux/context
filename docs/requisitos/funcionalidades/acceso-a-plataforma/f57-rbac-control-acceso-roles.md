# F57 — Control de acceso basado en roles (RBAC)

**Categoría:** Acceso a Plataforma (transversal)

## Objetivo

Definir qué puede ver, editar o subir cada perfil según su rol, no usuario por usuario.

## Contexto

El catálogo original dejó pendiente: roles finales sobre los que aplica (el catálogo
ampliado tiene ~18 actores) y matriz de permisos por rol.

## Qué hay

Hay RBAC funcional en el backend vigente: `Usuario.NIVELES_ACCESO = ("ciudadano",
"investigador", "reportador", "admin")` con cascada
(`backend/app/models/datos.py:32-74`, método `tiene_nivel`), aplicado vía
`backend/app/api/permisos.py` (`EscrituraRequiereNivel`, decorador `requiere_nivel`)
tanto en vistas DRF como planas. También existe `RolUsuario` como catálogo adicional de
roles de proyecto (coordinador, investigador, técnico — `datos.py:10-22`, usado en
`ProyectoUsuario.rol`). En el prototipo viejo
(`colflux-backend-ia/docs/assets/js/role-guard.js`) había un selector de rol en
localStorage para la UI, con el comentario explícito de que "no hay validación de rol
en el backend" — ya superado por el `permisos.py` actual.

## Qué hace falta

Los 4 niveles de acceso (`ciudadano`/`investigador`/`reportador`/`admin`) son una
jerarquía simple de cascada, no una matriz de permisos por rol sobre un catálogo
ampliado de ~18 actores territoriales — el pendiente explícito de "roles finales +
matriz de permisos" sigue abierto (confirmado en
`context/docs/roadmap/roadmap-3-6-12-meses.md:73`: "RBAC completo con matriz de ~18
actores... formalizar la matriz de permisos ahora que hay más roles reales en uso").
`RolUsuario` (roles de proyecto) y `Usuario.nivel` (niveles de plataforma) son dos
sistemas paralelos sin matriz unificada todavía.
