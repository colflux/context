# Catálogo de funcionalidades

!!! warning "Borrador — pendiente de validación"

Las funcionalidades se agrupan en 12 categorías por módulo/área técnica del producto
(no por caso de uso ni por actor), para que cada una pueda construirse y mantenerse de
forma relativamente independiente. Cada una tiene su propia página con Objetivo,
Contexto, Qué hay (evidencia real en el código) y Qué hace falta.

## Geoportal

- [F01 — Mapa de carbono nacional interactivo](geoportal/f01-mapa-carbono-nacional.md). Visualización de datos de carbono en un mapa nacional.
- [F02 — Sistema de capas activables](geoportal/f02-sistema-capas-activables.md). Checkbox por capa (carbono, biodiversidad, satélite, imágenes satelitales), con transparencia ajustable y leyenda dinámica.
- [F03 — Superposición y comparación de capas](geoportal/f03-superposicion-comparacion-capas.md). Ver varias capas a la vez para encontrar correlaciones.
- [F04 — Filtros geoespaciales y búsqueda](geoportal/f04-filtros-geoespaciales-busqueda.md). Por región/municipio, lluvia, temperatura y cobertura vegetal.
- [F05 — Mapa de calor por zonas](geoportal/f05-mapa-calor-zonas.md). Emisiones cruzando variables ambientales, con tendencia temporal.
- [F06 — Dashboard geoespacial multi-módulo](geoportal/f06-dashboard-geoespacial-multimodulo.md). Biomasa, flujos de GEI, carbono orgánico del suelo, vegetación y GPP.
- [F07 — Captura de coordenadas GPS en formularios](geoportal/f07-captura-gps-formularios.md). Georreferenciación automática de registros de campo.
- [F08 — Geoportal integrado con IA generativa](geoportal/f08-geoportal-ia-generativa.md). Preguntas en lenguaje natural sobre el mapa/dashboard.

## Datos y Carga

- [F09 — Ingreso de datos de carbono (formulario)](datos-y-carga/f09-ingreso-datos-carbono.md). Carga manual de mediciones con validaciones por campo.
- [F10 — Formulario "Capacidad de Cambio Climático"](datos-y-carga/f10-formulario-capacidad-cambio-climatico.md). Amenaza, vulnerabilidad, infraestructura, presupuesto.
- [F11 — Flujo de validación/moderación + semáforo de calidad](datos-y-carga/f11-validacion-semaforo-calidad.md). Estado "Publicado" o "Pendiente de Validación" con indicador de confiabilidad.
- [F12 — Restricción de edición + comentarios comunitarios](datos-y-carga/f12-restriccion-edicion-comentarios.md). Modo solo lectura sobre datos ajenos, con comentarios.
- [F13 — Descarga de datos de flujo filtrable](datos-y-carga/f13-descarga-datos-filtrable.md). Por unidad experimental, proyecto y zona geográfica.
- [F14 — Protocolo de validación por comité científico](datos-y-carga/f14-validacion-comite-cientifico.md). Curaduría institucional de fuentes externas.

## Carbono y Estimaciones

- [F15 — Cálculo de estimaciones de carbono](carbono-y-estimaciones/f15-calculo-estimaciones-carbono.md). Backend calcula estimaciones y factores de emisión por ecosistema.
- [F16 — Publicación de modelos predictivos](carbono-y-estimaciones/f16-publicacion-modelos-predictivos.md). Un investigador publica un modelo consultable por otros.
- [F17 — Descarga de metadatos metodológicos](carbono-y-estimaciones/f17-descarga-metadatos-metodologicos.md). Metodología, protocolo, instrumento, fecha y confianza por dato.
- [F18 — Exportación en formatos diferenciados](carbono-y-estimaciones/f18-exportacion-formatos-diferenciados.md). Tabular (CSV/Excel) y geoespacial (Shapefile, GeoJSON, GeoTIFF).
- [F19 — Niveles de acceso graduados por resolución del dato](carbono-y-estimaciones/f19-niveles-acceso-resolucion.md). Mayor resolución para usuarios acreditados.
- [F20 — Cálculo automático de toneladas de carbono almacenadas por región/ecosistema](carbono-y-estimaciones/f20-calculo-toneladas-carbono.md).

## Wiki y Conocimiento

- [F24 — Wiki de conocimiento sobre carbono + glosario no técnico](wiki-y-conocimiento/f24-wiki-glosario-carbono.md). Para público ciudadano.
- [F25 — Wiki colaborativa del proyecto](wiki-y-conocimiento/f25-wiki-colaborativa-proyecto.md). Editable, con historial de versiones y comentarios.
- [F26 — Espacio para publicar papers/estudios](wiki-y-conocimiento/f26-espacio-papers-estudios.md). Repositorio de estudios externos.
- [F27 — Sección de autoría/metodología por dato o fuente](wiki-y-conocimiento/f27-autoria-metodologia-dato.md).
- [F28 — Portal de acceso e investigación avanzada](wiki-y-conocimiento/f28-portal-investigacion-avanzada.md). Búsqueda por período/región.

## Visualización y Reportes

- [F29 — Visualización del ciclo de carbono](visualizacion-y-reportes/f29-visualizacion-ciclo-carbono.md). Gráficos y diagramas de flujo.
- [F30 — Generador de gráficos configurables](visualizacion-y-reportes/f30-generador-graficos-configurables.md). Línea, barra, pie, etc., sobre cualquier variable.
- [F31 — Mapas temáticos automáticos](visualizacion-y-reportes/f31-mapas-tematicos-automaticos.md). Heatmaps y cloropléticos exportables en PNG/PDF/SVG.
- [F32 — Plantillas prediseñadas de reportes](visualizacion-y-reportes/f32-plantillas-reportes.md).
- [F33 — Builder de dashboards personalizados](visualizacion-y-reportes/f33-builder-dashboards-personalizados.md). Arrastrar y soltar, con guardado y permisos de compartir.
- [F34 — Dashboard ejecutivo con KPIs + reportes automáticos](visualizacion-y-reportes/f34-dashboard-ejecutivo-kpis.md).
- [F35 — Directorio de proyectos de carbono cercanos](visualizacion-y-reportes/f35-directorio-proyectos-cercanos.md).

## Monitoreo de Red y Sensores

- [F36 — Dashboard de estado de la red de monitoreo](monitoreo-red-sensores/f36-dashboard-estado-red.md). Puntos activos/inactivos e historial de operatividad.
- [F37 — Registro de fallos de equipos](monitoreo-red-sensores/f37-registro-fallos-equipos.md). Alertas de desconexión.
- [F38 — Ingesta automática de datos IoT en tiempo real](monitoreo-red-sensores/f38-ingesta-iot-tiempo-real.md). Sensores vía LoRa/Wi-Fi/4G.

## Alertas y Notificaciones

- [F39 — Alertas automáticas por umbral](alertas-y-notificaciones/f39-alertas-automaticas-umbral.md).
- [F40 — Notificaciones proactivas vía WhatsApp](alertas-y-notificaciones/f40-notificaciones-whatsapp.md).

## Colaboración Interinstitucional

- [F41 — Integración y sincronización de datos externos](colaboracion-interinstitucional/f41-integracion-sincronizacion-externa.md). API, ETL, sincronización y versionado por institución.
- [F42 — Portal único de datos consolidados](colaboracion-interinstitucional/f42-portal-datos-consolidados.md).
- [F43 — Directorio de instituciones y mapa de investigación](colaboracion-interinstitucional/f43-directorio-instituciones.md).
- [F44 — Mensajería y red de investigadores](colaboracion-interinstitucional/f44-mensajeria-red-investigadores.md).
- [F45 — Calendario de capacitaciones/talleres](colaboracion-interinstitucional/f45-calendario-capacitaciones.md).
- [F46 — Espacio de coordinación colaborativa](colaboracion-interinstitucional/f46-espacio-coordinacion-colaborativa.md). Calendario compartido, board de proyectos, chat/foro.

## Inteligencia Artificial

- [F54 — Chatbot de WhatsApp con IA conversacional territorial](inteligencia-artificial/f54-chatbot-whatsapp-territorial.md). También canal de captura de datos.
- [F55 — Motor de IA para ingesta multi-formato](inteligencia-artificial/f55-motor-ia-ingesta-multiformato.md). OCR, PLN y ML para limpiar y normalizar datos.
- [F56 — Indexación y recomendación automática de contenido](inteligencia-artificial/f56-indexacion-recomendacion-contenido.md).

## Acceso a Plataforma (transversal)

- [F57 — Control de acceso basado en roles (RBAC)](acceso-a-plataforma/f57-rbac-control-acceso-roles.md).
- [F58 — Cumplimiento de protección de datos personales](acceso-a-plataforma/f58-proteccion-datos-personales.md). Habeas Data (Ley 1581 de 2012).

## Addendum — hallazgos del prototipo (F59-F62)

Capacidades ya prototipadas que no encajaban en el catálogo original. Detalle completo en
[funcionalidades-addendum.md](../../roadmap/funcionalidades-addendum.md).

- [F59 — Diccionario de campo con interpretación técnica inversa](addendum-prototipo/f59-diccionario-campo-inverso.md).
- [F60 — Validación colaborativa de términos del diccionario (semáforo de aceptación)](addendum-prototipo/f60-semaforo-aceptacion-terminos.md).
- [F61 — Motor de inferencia dato↔diccionario en tiempo real](addendum-prototipo/f61-motor-inferencia-dato-diccionario.md).
- [F62 — Análisis estadístico exploratorio de datos cargados](addendum-prototipo/f62-analisis-estadistico-exploratorio.md).

## Fuentes

- `files/plataforma/Funcionalidades.pdf` (catálogo original F01-F58, v1.0.0)
- [funcionalidades-addendum.md](../../roadmap/funcionalidades-addendum.md) (F59-F62)
- Tarea de seguimiento: `tasks/backlog/arquitectura-lista-funcionalidades.md`
- Backend, frontend e ia-functions (código vigente), revisados el 2026-10-11 para las
  secciones "Qué hay" de cada página.
