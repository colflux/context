# F11 — Flujo de validación/moderación de datos + semáforo de calidad

**Categoría:** Datos y Carga

## Objetivo

Que cada dato tenga un estado automático "Publicado" (perfil de confianza) o
"Pendiente de Validación" (perfil externo), con un indicador visual de
calidad/confiabilidad.

## Contexto

El catálogo original dejó pendiente: ¿quién aprueba/rechaza? ¿visibilidad de un dato
pendiente? ¿se notifica a alguien?

## Qué hay

Existe un flujo de validación pero a nivel de *carga de archivo completa*, no de
dato/registro individual: `CargaArchivo.estado` (`subido/mapeado/validado/importado`),
`CargaArchivo.origen_mapeo` (`manual` vs `ia_chat`) y campos
`validado_por`/`fecha_validacion` que registran qué persona del equipo confirmó un
mapeo propuesto por IA (`app/models/datos.py`, endpoint `validar_carga` en
`app/api/urls.py:61`). No hay un estado "Publicado"/"Pendiente de Validación" a nivel de
registro individual (p. ej. por `SubmuestraGEI`), ni un indicador visual de
calidad/semáforo en ningún modelo o componente de frontend encontrado.

## Qué hace falta

- El estado automático publicado/pendiente según perfil de confianza vs. externo.
- El semáforo visual de calidad/confiabilidad.
- Definir quién aprueba/rechaza un dato individual (hoy solo hay `validado_por` a nivel
  de carga completa, hecho por "alguien del equipo" sin rol definido como aprobador).
- Lógica de notificación ni de visibilidad diferenciada de un dato pendiente — no
  existe tampoco.

Nota: distinto de [F60](../addendum-prototipo/f60-semaforo-aceptacion-terminos.md), que
es un semáforo de consenso sobre **definiciones del diccionario**, no sobre datos
medidos.
