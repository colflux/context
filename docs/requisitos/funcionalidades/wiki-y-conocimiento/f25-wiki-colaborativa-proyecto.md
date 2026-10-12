# F25 — Wiki colaborativa del proyecto

**Categoría:** Wiki y Conocimiento

## Objetivo

Página editable por varios usuarios, con historial de versiones y comentarios, para
documentar metodología, infraestructura y gobernanza del proyecto.

## Contexto

Distinta de [F24](f24-wiki-glosario-carbono.md), que es sobre carbono para el público
general — esta es documentación interna/institucional del propio proyecto COLFLUX.

## Qué hay

No se encontró evidencia de implementación en el código actual (backend ni frontend) —
no hay modelo de páginas editables, versionado ni comentarios. En `PrototipoCOLFLUX`
existe un `WikiController`/`WikiService` (ver F24), pero es de solo lectura sobre un CSV
estático, sin edición colaborativa, historial de versiones ni comentarios, por lo que
tampoco cubre esta funcionalidad ni siquiera como referencia cercana.

## Qué hace falta

Todo lo esencial: modelo de contenido editable, control de versiones, sistema de
comentarios, permisos de edición multiusuario, y distinguirla claramente de F24 (ya que
ninguna de las dos existe hoy).
