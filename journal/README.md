# Seguimiento de actividades del equipo

Zona de seguimiento de actividades, no publicada en el sitio (no está en `mkdocs.yml`). Pensada para que cualquier persona del equipo pueda llevar su propio registro.

Tres piezas con propósitos distintos:

- **[journal/<nombre>/](journal/)** — una carpeta por persona del equipo (por ejemplo [journal/vivi/](vivi/)) con su bitácora mensual y su propio `TODAY.md`. Lo que vive en la carpeta de una persona es su seguimiento personal; no se mezcla con el de otras.
  - **bitácora mensual** (`AAAA-MM.md`) — lo que se hizo (no un plan de lo que se va a hacer). Sirve de insumo para el informe de actividades: cada entrada debe poder copiarse casi directo a un reporte.
  - **`TODAY.md`** — lista corta y priorizada de lo pendiente ahora mismo para esa persona, para no tener que releer todos los archivos de `tasks/` para saber qué sigue. No duplica el detalle (eso vive en la tarea de origen, enlazada con `[[nombre-archivo]]`) — solo evita que se mezclen o se pierdan pendientes entre tareas.
- **[tasks/](../tasks/)** — seguimiento tarea por tarea, compartido por todo el equipo. Un archivo por tarea, con objetivo y pasos, independiente del mes en que se creó o se cierre.

## Uso de journal/<nombre>/

Cada persona tiene su propia carpeta (ej. [journal/vivi/](vivi/)). Dentro, el log está dividido por mes en archivos `AAAA-MM.md` (por ejemplo [journal/vivi/2026-09.md](vivi/2026-09.md)) y hay un `TODAY.md` propio (ej. [journal/vivi/TODAY.md](vivi/TODAY.md)).

Si alguien nuevo del equipo empieza a usar esta carpeta, crea `journal/<su-nombre>/` con su propia bitácora mensual y su propio `TODAY.md`, siguiendo el mismo formato.

Agregar una entrada nueva por fecha (`## AAAA-MM-DD`) en el archivo del mes correspondiente
(crear el archivo si el mes aún no existe), con lo que se hizo.

## Uso de tasks/

Un archivo por tarea (`kebab-case.md`), a partir de [tasks/_template.md](../tasks/_template.md):
objetivo, pasos como checklist, y notas. Vincular tareas relacionadas con `[[nombre-archivo]]`.

Cada tarea lleva **`A cargo`** (quién la pidió o la está trabajando) y
**`Sesión de Claude Code`** (link a la sesión activa que tiene todo el
contexto). La idea: si la ventana/sesión se cierra, la forma más rápida de
retomar es reabrir esa sesión con el link; si ya no está disponible, el
`## Historial` de la tarea es el respaldo — por eso cada entrada del
Historial debe quedar lo bastante completa para reconstruir el estado sin la
sesión original. Actualizar el link de sesión cada vez que una sesión nueva
retoma la tarea.

El estado de la tarea lo da la carpeta donde vive el archivo, no un campo dentro del archivo:

- **[tasks/backlog/](tasks/backlog/)** — todo lo pendiente que aún no es prioridad de la semana.
- **[tasks/inprogress/](tasks/inprogress/)** — solo las tareas que sí o sí se tienen que
  desarrollar esta semana para cumplir el objetivo actual. Mover aquí desde `backlog/`
  al arrancar la semana o al empezar a trabajar en la tarea. Mantener esta carpeta corta
  a propósito — si todo está "en progreso" deja de servir como filtro.
- **[tasks/done/](tasks/done/)** — tareas terminadas. Mover aquí desde `inprogress/` al cerrarlas.
