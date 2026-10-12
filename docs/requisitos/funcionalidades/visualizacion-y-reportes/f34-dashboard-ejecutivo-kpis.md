# F34 — Dashboard ejecutivo con KPIs + reportes automáticos

**Categoría:** Visualización y Reportes

## Objetivo

Dar a un tomador de decisiones un dashboard con KPIs y recomendaciones automáticas, más
la posibilidad de generar reportes periódicos.

## Contexto

Distinto de los dashboards de datos crudos: aquí el foco es la síntesis ejecutiva.

## Qué hay

Existe un dashboard de KPIs: `frontend/src/pages/DashboardIndicadores.tsx` muestra
tarjetas con indicadores agregados (muestras totales, sitios monitoreados, proyectos
activos, % de cobertura del territorio) más gráficas por sección. Hay un botón de
descarga de archivos (`frontend/src/components/chat/BotonDescarga.tsx`) ligado al
asistente de chat, pero es descarga de un archivo ya preparado, no generación de reporte
periódico desde el dashboard.

## Qué hace falta

No hay recomendaciones automáticas basadas en datos, ni generación/programación de
reportes periódicos (nada de scheduling, cron, ni plantillas de reporte exportable)
conectado al dashboard ejecutivo.
