# Para hoy / próximos días

Lista corta de lo que está pendiente **ya priorizado**, para no tener que releer cada archivo de `tasks/` para saber qué sigue. Se actualiza a mano; cuando algo se resuelve, se borra de aquí (el detalle completo queda en la tarea de origen, no aquí).

## Reunión martes 2026-09-15

- Mostrar al equipo `docs/arquitectura/git-flow.md` (GitHub Flow + protección de ramas) y validar en conjunto los acuerdos: quién aprueba, cuántas aprobaciones, si aplica igual a todos los repos.
- Resolver la discrepancia: el documento dice "propuesta pendiente de validar", pero las *branch protection rules* ya se activaron el 2026-09-11 en los 5 repos antes de esa validación (ver [[automatizar-deploy-ecosistema-colflux]]).

## De [[automatizar-deploy-ecosistema-colflux]]

- **Migración IDEAM/SWAMP:** el script de migración quedó en un scratchpad de sesión (`/private/tmp/.../scratchpad/migrar_remoto.py`) que puede haberse perdido — hay que rehacerlo o pedir que se regenere.
- **Documentar la decisión final de despliegue** — falta consolidar lo que ya está repartido en Entregables/Historial de la tarea en un documento único.

### Riesgos técnicos en el servidor `44.213.47.34` (no bloqueantes, pero crecen con el tiempo)

- Servidor con **1.9GB RAM y 0 swap** corriendo `backend` + `frontend` + `ia-functions` a la vez — ya causó un OOM kill en `ia-functions`. Agregar swap o subir el plan de Lightsail antes de que se repita.
- Contraseña débil del superusuario del backend (`colflux123`) — cambiar desde `/admin`. (El nuevo superusuario `colflux-admin` de [[conectar-base-datos-aws]] ya tiene contraseña segura; falta revisar si el usuario `viviana` original todavía tiene la débil.)
- Contenedor viejo `colflux-backend` sigue corriendo como respaldo — apagarlo cuando el stack nuevo lleve unos días estable.
- Bug menor en `ia-functions`: `answer` puede quedar vacío si el modelo agota `MAX_TURNS` llamando herramientas sin redactar el texto final.
- El chat flotante del frontend se mergeó a producción sin revisión de código ni pruebas — falta una pasada de QA normal.

## De [[conectar-base-datos-aws]]

- **Verificar end-to-end en producción** tras el último deploy: login de `colflux-admin` en `/admin/` y en el frontend (por correo), `/team` con el selector de nivel nuevo, y que subir/descargar datos respete la cascada (ciudadano < investigador < reportador < admin).

## De [[prototipo-evaluar-portar-diccionario-campo]]

- `PrototipoCOLFLUX` ya se revisó (2026-09-20): tiene diccionario de campo inverso, semáforo de aceptación comunitaria, motor de inferencia dato↔diccionario y análisis exploratorio en Python — documentados como F59-F62 en [funcionalidades-addendum.md](../docs/roadmap/funcionalidades-addendum.md).
- Falta decidir con el equipo si se portan al backend/frontend reales (stack distinto: Spring Boot vs. Django/DRF).

## Referencias

- [[automatizar-deploy-ecosistema-colflux]] — tarea de origen con el detalle completo (Entregables, Notas de mejora, Historial).
- [[conectar-base-datos-aws]] — conexión a `colflux-DB` (RDS), fix del deploy automático (`LIGHTSAIL_APP_PATH`), y rediseño de roles a nivel en cascada.
