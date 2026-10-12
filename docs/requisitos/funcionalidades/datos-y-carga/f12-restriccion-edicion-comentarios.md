# F12 — Restricción de edición + comentarios comunitarios

**Categoría:** Datos y Carga

## Objetivo

Que un Actor Territorial no pueda editar un dato ajeno (modo solo lectura), pero sí
pueda dejar comentarios/aportes sobre él.

## Contexto

El catálogo original dejó pendiente: ¿esos comentarios se notifican al autor original?

## Qué hay

Existe restricción de edición pero a nivel de `FuenteDatos`/`CargaArchivo`, no de
"Actor Territorial vs. dato ajeno": `FuenteDatosViewSet.perform_update`
(`app/api/datos/views.py:25-28`) bloquea edición si `estado == "completo"` ("Esta
fuente ya tiene datos cargados: no se puede editar"), y el frontend muestra ese bloqueo
con el tooltip correspondiente (`frontend/src/components/data/FuentesTable.tsx:274`).
No hay ningún modelo, tabla ni componente de "comentarios" o "aportes comunitarios" en
backend ni frontend.

## Qué hace falta

Todo el sistema de comentarios/aportes sobre un dato ajeno: modelo de comentarios,
endpoint de creación/listado, UI, y el concepto de "Actor Territorial" como rol
distinto de los niveles actuales (`ciudadano/investigador/reportador/admin`) — hoy el
control de acceso es por nivel jerárquico de usuario, no por "autoría de un dato
específico". Tampoco hay lógica de notificación al autor original (que no puede
implementarse sin antes tener comentarios).
