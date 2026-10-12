# F32 — Plantillas prediseñadas de reportes

**Categoría:** Visualización y Reportes

## Objetivo

Ofrecer diseños profesionales de reporte, adaptados a distintos públicos.

## Contexto

Complementa la exportación de datos crudos con una presentación lista para compartir.

## Qué hay

No se encontró evidencia de implementación en el código actual. El backend tiene un
módulo `backend/app/api/reportes/` pero son endpoints de datos agregados (biomasa, COS,
MOM) consumidos por `frontend/src/services/reportes.service.ts`, no plantillas de
documento/reporte con diseño. Tampoco hay nada similar en PrototipoCOLFLUX más allá de
un archivo estático `reportes/analisis_correlaciones_guatavita.html` (notebook
exportado a HTML, análisis exploratorio puntual, no una plantilla reutilizable).

## Qué hace falta

Todo: no existen plantillas con diseño profesional por público objetivo, ni mecanismo
de selección/aplicación de plantillas.
