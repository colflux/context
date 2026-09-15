# Seguimiento personal — Viviana

Zona exclusiva para registrar actividades, no publicada en el sitio (no está en `mkdocs.yml`).

Tres piezas con propósitos distintos:

- **[journal/](journal/)** — bitácora por mes de lo que se hizo (no un plan de lo que se va a hacer). Sirve de insumo para el informe de actividades: cada entrada debe poder copiarse casi directo a un reporte.
- **[tasks/](tasks/)** — seguimiento tarea por tarea. Un archivo por tarea, con objetivo y pasos, independiente del mes en que se creó o se cierre.
- **[TODAY.md](TODAY.md)** — lista corta y priorizada de lo pendiente ahora mismo, para no tener que releer todos los archivos de `tasks/` para saber qué sigue. No duplica el detalle (eso vive en la tarea de origen, enlazada con `[[nombre-archivo]]`) — solo evita que se mezclen o se pierdan pendientes entre tareas.

## Uso de journal/

El log está dividido por mes en archivos `AAAA-MM.md` (por ejemplo [journal/2026-09.md](journal/2026-09.md)).

Agregar una entrada nueva por fecha (`## AAAA-MM-DD`) en el archivo del mes correspondiente
(crear el archivo si el mes aún no existe), con lo que se hizo.

## Uso de tasks/

Un archivo por tarea (`kebab-case.md`), a partir de [tasks/_template.md](tasks/_template.md):
objetivo, pasos como checklist, y notas. Vincular tareas relacionadas con `[[nombre-archivo]]`.

El estado de la tarea lo da la carpeta donde vive el archivo, no un campo dentro del archivo:

- **[tasks/backlog/](tasks/backlog/)** — todo lo pendiente que aún no es prioridad de la semana.
- **[tasks/inprogress/](tasks/inprogress/)** — solo las tareas que sí o sí se tienen que
  desarrollar esta semana para cumplir el objetivo actual. Mover aquí desde `backlog/`
  al arrancar la semana o al empezar a trabajar en la tarea. Mantener esta carpeta corta
  a propósito — si todo está "en progreso" deja de servir como filtro.
- **[tasks/done/](tasks/done/)** — tareas terminadas. Mover aquí desde `inprogress/` al cerrarlas.
