# CLAUDE.md

Contexto persistente para trabajar desde este repo. Se carga automáticamente al inicio de cada sesión.

## Qué es este repo

`context` es la documentación transversal del componente de plataforma (OE2) de Colflux (monitoreo de carbono en páramos, humedales y sabanas de Colombia, proyecto de la Pontificia Universidad Javeriana). **No tiene código ejecutable de la plataforma** — es la fuente de verdad de arquitectura, decisiones y estado para que las sesiones de IA (aquí o en los repos de código) trabajen con contexto real y no con supuestos desactualizados.

## Repos hermanos (código real)

Viven junto a este repo, en `/Users/vivianabautista.xyz/colflux/`:

- `backend/` — Django + DRF + PostGIS. Tiene su propio `CLAUDE.md`.
- `frontend/` — React + Vite.
- `ia-functions/` — funciones de IA (chatbot, insights).
- `wiki/` — wiki del proyecto.
- `PrototipoCOLFLUX/`, `colflux-backend-ia/`, `ia/` — prototipos/exploraciones previas, no necesariamente vigentes.

Como las sesiones suelen arrancar desde `context`, cuando una tarea implique editar código en alguno de esos repos: leer/escribir ahí usando su ruta absoluta (`../backend/...`, etc.), sin asumir que su documentación interna (si la tiene) está actualizada respecto a lo que hay aquí.

## Antes de programar algo no trivial

Revisar en este repo:

- `docs/arquitectura/` — decisiones técnicas, distinguiendo lo ya validado de lo marcado como "propuesta pendiente de validar con el equipo" (patrón usado en `git-flow.md`, por ejemplo).
- `docs/roadmap/` — plan de ejecución 3/6/12 meses y funcionalidades priorizadas.
- `personal/tasks/{inprogress,blocked,backlog,done}/` — tareas activas, con bitácora de sesiones anteriores (Historial). Antes de asumir que algo no existe o no se ha intentado, buscar aquí. Cada tarea lleva `A cargo` y `Sesión de Claude Code` (link a la sesión con todo el contexto) — al trabajar una tarea existente, actualizar ese link a la sesión actual; al crear una nueva, usar `personal/tasks/_template.md` y llenar ambos campos.
- `personal/TODAY.md` — pendientes inmediatos ya priorizados.

## Al terminar

Si el trabajo de la sesión cambió una decisión de arquitectura, avanzó/cerró algo del roadmap, o resolvió (parcial o totalmente) una tarea documentada en `personal/tasks/`, reflejarlo aquí antes de cerrar la sesión:

- Mover el archivo de tarea entre carpetas (`inprogress/` → `done/`, etc.) y agregar una entrada en su `## Historial`.
- Actualizar `docs/arquitectura/*.md` si cambió una decisión técnica.
- Agregar una entrada en `personal/journal/AAAA-MM.md` si aplica al reporte de actividades.

No dejar el cambio solo en el repo de código — `context` es lo que la siguiente sesión (en cualquier repo) va a leer primero.
