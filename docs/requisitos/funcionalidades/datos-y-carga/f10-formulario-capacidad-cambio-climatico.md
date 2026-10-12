# F10 — Formulario "Capacidad de Cambio Climático"

**Categoría:** Datos y Carga

## Objetivo

Registrar la capacidad de adaptación de un actor territorial al cambio climático: tipo
de amenaza climática, índice de vulnerabilidad, infraestructura disponible, presupuesto
asignado, fecha de toma de datos.

## Contexto

El catálogo original dejó pendiente: tipo de dato de cada campo (¿escala del índice?
¿moneda del presupuesto?); ¿se generaliza este esquema a otros formularios de ingreso?

## Qué hay

No se encontró evidencia de implementación en el código actual. Búsquedas por
"vulnerab", "amenaza", "climatic", "capacidad de cambio climático" en backend y
frontend no arrojaron ningún modelo, serializer, vista ni componente. No hay nada
similar tampoco en PrototipoCOLFLUX.

## Qué hace falta

Todo: el modelo de datos (tipo de amenaza climática, índice de vulnerabilidad,
infraestructura, presupuesto, fecha de toma), el formulario, y la decisión de si se
generaliza a un esquema común de formularios de ingreso (hoy cada "sección" de datos —
GEI, biomasa, COS, MOM, clima— es un modelo Django separado cargado por ETL, no un
formulario dinámico genérico, así que "generalizar" implicaría una decisión de
arquitectura nueva).
