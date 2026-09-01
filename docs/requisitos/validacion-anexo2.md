# Validación de funcionalidades contra el Anexo 2

Cruce de la lista de [Funcionalidades](funcionalidades.md) (extraídas de las historias de usuario del Anexo 1) contra el Anexo 2 (Documento Técnico), para ver cuáles están respaldadas por ambos documentos y cuáles solo aparecen en el Anexo 1.

## ✅ Confirmadas en el Anexo 2

| Funcionalidad | Dónde aparece en el Anexo 2 |
|---|---|
| Dashboard interactivo (gráficos, series temporales, tablas) | Sección "Visualización-dashboard" |
| Geoportal / mapa interactivo (Leaflet, Mapbox, Google Earth Engine) | Descripción de la interfaz de consulta |
| Filtros y búsquedas personalizadas por ecosistema/región | Descripción del acceso a la base de datos |
| Descarga de datos en formatos abiertos | Descripción del acceso a la base de datos — **pero dice CSV, JSON y GeoTIFF**, no Shapefile/GeoJSON como el Anexo 1 (ver discrepancia abajo) |
| Niveles de acceso diferenciados (RBAC) | Mencionado varias veces como requisito de seguridad |
| Modelos predictivos / recomendaciones de IA | Descripción del motor de IA generativa y el flujo ETL |
| Alertas automáticas (a nivel de sistema/datos, y notificaciones vía WhatsApp) | Sección del dashboard y del bot de WhatsApp |
| Exportar en PDF, Excel | Mencionados varias veces |
| API REST para interoperabilidad con otras bases de datos | Descripción de interoperabilidad de la plataforma |

## ❌ No mencionadas en el Anexo 2 (solo están en el Anexo 1)

- **Estados de workflow "Pendiente de Validación" / "Publicado"** — el Anexo 2 solo dice que hay un comité científico que valida, no define estos estados como funcionalidad del sistema.
- **Modo "Solo Lectura" explícito para Actor Territorial** — implícito en el RBAC general, pero no aparece como etiqueta/funcionalidad concreta.
- **Reportar alertas ambientales por el usuario** (tala ilegal, contaminación) — las alertas del Anexo 2 son generadas por el *sistema* (inconsistencias de datos, tendencias), no alertas *reportadas por* el Actor Territorial.
- **Descargar metadatos** para validar rigurosidad científica — no aparece.
- **Exportar bases de datos completas** (para Investigador Interno) — no se menciona explícitamente esa función.
- **Rendimiento <3 segundos** en consultas georreferenciadas — no está en el Anexo 2.
- **Interfaz responsive/adaptativa** — no está en el Anexo 2.

## ⚠️ Discrepancia a resolver con el equipo

**Formato de exportación de datos geoespaciales:**

- Anexo 1 (notas técnicas): **Shapefile / GeoJSON** para mapas, CSV para tablas.
- Anexo 2: **CSV, JSON y GeoTIFF**.

Son formatos distintos (GeoTIFF es raster, Shapefile/GeoJSON son vectoriales) — probablemente aplican a tipos de datos diferentes (ej. GeoTIFF para capas de biomasa/carbono raster, GeoJSON para geometrías de sitios/polígonos), pero no está explícito en ninguno de los dos documentos. Vale la pena confirmarlo con Adriana antes de construir la funcionalidad de exportación.

## Nota

Que una funcionalidad no aparezca en el Anexo 2 no la invalida — el Anexo 1 es más detallado a nivel de historias de usuario, y es normal que tenga granularidad que el documento técnico general no cubre. Esto es solo un mapa de qué está respaldado por ambos documentos vs. qué depende únicamente del criterio de Adriana en las historias de usuario.
