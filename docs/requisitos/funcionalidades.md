# Funcionalidades (extraídas de los casos de uso)

Lista de funcionalidades extraídas de los criterios de aceptación de las 5 historias de usuario del Anexo 1 (HU-001 a HU-005), agrupadas por tipo en vez de por historia para evitar duplicados. Cada ítem referencia la(s) historia(s) de la que sale.

_Ver también: [Entender el problema y los usuarios](problema-usuarios.md)._

## Registro y carga de datos

- Registrar datos de monitoreo en campo con coordenadas geográficas — *HU-001*
- Ingresar variables ambientales por región (deforestación, biodiversidad, calidad de agua) — *HU-002*
- Registrar reporte de carbono vía carga de archivo (CSV/Excel) o formulario manual — *HU-003*
- Ingresar datos cualitativos/cuantitativos de capacidad climática vía formulario o archivo plano — *HU-005*
- Cargar reportes/hallazgos científicos externos (Investigador Externo) — *HU-001*

## Validación y estados de los datos

- Validar formato de los datos al guardar — *HU-001, HU-002, HU-003, HU-005*
- Asignar estado "Pendiente de Validación" o "Publicado" según el perfil — *HU-001, HU-003*
- Registrar autoría y fecha automáticamente — *HU-002, HU-003*
- Etiquetar automáticamente el origen del dato como "Externo" cuando aplique — *HU-005*
- Restringir edición a solo los registros creados por el usuario (Investigador Externo) — *HU-005*
- Bloquear edición de datos duros para Actor Territorial, mostrar "Solo Lectura" y habilitar comentarios — *HU-002*

## Consulta y visualización

- Búsqueda avanzada por región o tipo de recurso — *HU-001*
- Mapa interactivo con selección de zona geográfica — *HU-001, HU-004*
- Filtros por ecosistema, tipo de recurso, región, rango de fechas, tipo de cobertura vegetal — *HU-002, HU-003*
- Tablero de control (dashboard) con resumen visual del estado de recursos — *HU-001, HU-003, HU-005*
- Visualizaciones gráficas (líneas, series temporales, tablas de métricas) — *HU-002, HU-003*
- Mapas interactivos y resúmenes ejecutivos en lenguaje no técnico (para Actor Territorial) — *HU-004*
- Consultar datos históricos y metodologías aplicadas (para validar rigurosidad científica) — *HU-004*

## Alertas

- Generar alertas automáticas cuando indicadores críticos superan límites permitidos — *HU-001*
- Resaltar visualmente variaciones drásticas/críticas en métricas de carbono — *HU-003*

## Exportación / descarga

- Descargar datos en formatos estándar: CSV, JSON — *HU-001*
- Exportar en formatos abiertos: Shapefile/GeoJSON (mapas), CSV (tablas) — *HU-003*
- Descargar reporte resumen en PDF o CSV — *HU-002*
- Descargar reporte simplificado en PDF — *HU-003*
- Descargar metadatos — *HU-004*
- Generar reporte consolidado descargable en PDF, Excel o GeoJSON, filtrado por fecha/región/indicador — *HU-004, HU-005*
- Exportar bases de datos completas y cruzar variables complejas — *HU-004*
- Publicar modelos predictivos para consulta de otros actores — *HU-004*

## Seguridad y control de acceso

- Control de acceso basado en roles (RBAC) para los perfiles de usuario — *HU-004, y transversal en el Anexo 2*

## No funcionales (mencionados explícitamente)

- Interfaz adaptativa/responsive con capa de visualización geográfica (Leaflet, OpenLayers o ArcGIS) — *Anexo 1, notas técnicas*
- Consultas georreferenciadas deben cargar en menos de 3 segundos — *Anexo 1, notas técnicas*

## Pendiente

- Priorizar cuáles de estas funcionalidades son parte del **primer prototipo** (ver discusión sobre usuarios de entrada en [problema-usuarios.md](problema-usuarios.md)) vs. cuáles llegan en iteraciones posteriores hacia TRL 6.

Ver también: [Validación contra el Anexo 2](validacion-anexo2.md) — cuáles de estas funcionalidades están respaldadas por el documento técnico.
