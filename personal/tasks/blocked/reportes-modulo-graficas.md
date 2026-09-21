# Crear/revisar el módulo de gráficas en el front

**Estado:** blocker — implementado y desplegado en producción, depende de la revisión del ecólogo sobre los 3 puntos marcados abajo
**Creada:** 2026-09-01

## Objetivo

Tener el módulo de visualizaciones gráficas (líneas, series temporales, tablas de métricas) funcionando en el front, según la propuesta de gráficas del equipo (ver Notas). El link original a `docs/requisitos/funcionalidades.md` y las referencias HU-002/HU-003 quedaron rotos desde que esa carpeta se vació el 2026-09-06 (ver [arquitectura-lista-funcionalidades.md](../backlog/arquitectura-lista-funcionalidades.md)) — esta tarea ya no depende de esos requisitos, sino de la tabla de gráficas que pegó el equipo el 2026-09-18.

## Pasos

- [x] Revisar qué parte del módulo ya existe en el front
- [x] Definir qué gráficas faltan según la propuesta del equipo
- [x] Implementar/completar las gráficas pendientes

## Notas

### Gráficas propuestas por el equipo

Propuesta del equipo (2026-09-18) de gráficas por variable, organizada por bloque.

#### General

| Variable | Variables asociadas | Filtro | Gráfico | Notas |
|---|---|---|---|---|
| Title | Proyecto/Entidad | Sí | Torta / Barras | Todo el carbono por entidad, o por cada metodología. Deben estar en las mismas unidades |
| Región Natural | Región | Sí | Torta | Todo el carbono por región, o por cada metodología. Deben estar en las mismas unidades |
| Departamento | Departamento | Sí | Mapa de calor | |
| Municipio | Municipio | Sí | Mapa de calor | |
| Vereda | Sector | Sí | Mapa de calor | |
| Site name | Sitio de medición | Sí | Mapa de calor | |
| Ecosistema / Cobertura | Ecosistema / Cobertura | Sí | Barras | Todo el carbono por ecosistema, o por cada metodología. Deben estar en las mismas unidades |
| Estado de conservación | Estado de conservación | Sí | Torta | % de participación |
| Fecha instalación unidad de muestreo | Fecha | Sí | Tendencia | Filtro por año/mes |

#### Biomasa

| Variable | Variables asociadas | Filtro | Gráfico | Notas |
|---|---|---|---|---|
| Producción biomasa | Crecimiento biomasa | | Dispersión / Mapa de calor | |
| Familia | Familia | | — | Acumulación de biomasa por familia |
| Género | Género | | — | Acumulación de biomasa por género |
| Especie | Especie | | — | Acumulación de biomasa por especie |

#### COS

| Variable | Variables asociadas | Filtro | Gráfico | Notas |
|---|---|---|---|---|
| Profundidad (cm) | Profundidad de muestra | | — | % de carbono por rango de profundidad |
| — | % carbono | | | |

#### MOM

| Variable | Notas |
|---|---|
| Contenido de carbono en hojarasca | Gráfico en g/m² |

#### Flujos

| Variable | Notas |
|---|---|
| Analizador | Flujo por analizador |
| Day/night | Flujo por día-noche |
| CO2 original | Unidades por definir |
| CH4 original | Unidades por definir |
| N2O original | Unidades por definir |

### Implementación (2026-09-18)

Repos: `frontend` (React + recharts) y `backend` (Django). Resumen de qué se hizo y qué quedó pendiente de validar con el equipo.

**Decisión de unidades para Flujos**: no se fija una unidad estándar por gas. El modelo ya guarda la unidad como dato (`MuestraGEI.unidad_medida`, catálogo `UnidadMedida` con símbolo configurable), así que las gráficas usan `unidad_medida.simbolo` tal cual viene de cada muestra, agrupando por gas — es como ya funcionaba `EmissionTrendChart` antes de esta tarea.

**Backend — nuevos endpoints**:
- `GET /api/geo/resumen-categorico/?dimension=proyecto|ecosistema|estado_conservacion|analizador|condicion_luz` — cubre General (por entidad/ecosistema/estado de conservación) y Flujos (por analizador/día-noche).
- `GET /api/geo/tendencia-instalacion/?agrupar=mes|anio` — instalación de unidades de muestreo en el tiempo.
- `GET /api/reportes/biomasa/?dimension=familia|genero|especie` y `GET /api/reportes/biomasa/produccion/`.
- `GET /api/reportes/cos/` — % de carbono por rango de profundidad (0-10, 10-20, 20-30, 30-50, 50-100, 100+ cm).
- `GET /api/reportes/mom/?agrupar=mes|anio` — tendencia de carbono en hojarasca.
- Todos agregan en el servidor (nunca devuelven filas crudas), a diferencia de `/api/geo/series/` que ya existía sin paginar.

**Frontend**: componente genérico `CategoricalChart` (torta/barras parametrizado por dimensión) cubre 6 de las filas de General + Flujos, evitando duplicar componentes casi idénticos. Los mapas de calor de Departamento/Municipio/Vereda ya existían (`GeoMap.tsx` + `/api/geo/resumen/`); se extendió un nivel más para cubrir "Site name" (drill-down hasta sitio, con capa de puntos). Nuevos componentes solo donde la forma de los datos es distinta: `BiomasaTaxonChart`, `BiomasaProduccionScatter`, `CosProfundidadChart`, `MomHojarascaChart`, `InstalacionTrendChart`. Todo se integró en `/dashboard` (`DashboardIndicadores.tsx`), con una sección por bloque.

**Estilo**: se agregó un total centrado en las gráficas de torta/dona (overlay HTML sobre el SVG — el `<Label position="center">` nativo de recharts no inyecta `viewBox` de forma confiable en esta versión) y etiquetas de valor sobre las barras (`LabelList`), siguiendo una referencia visual que trajo el equipo, sin cambiar la paleta ni el layout existente.

**Pendiente — único bloqueante: validación del ecólogo** sobre estos 3 puntos (todo lo demás ya está implementado, mergeado y confirmado funcionando en producción en `44.213.47.34`):
1. **Ecosistema/Cobertura**: un sitio puede tener varias filas de `Cobertura` (una por sistema de clasificación CLC/IPCC/IGBP/etc., o duplicados en conflicto entre fuentes). Se está tomando la primera en orden estable como aproximación — falta un criterio de vigencia si el equipo lo necesita más preciso.
2. **Biomasa por familia/género/especie**: el carbono (`contenido_carbono`, `prom_tonc_ha`) vive a nivel de parcela (`MuestraBiomasa`), no por individuo/especie (`IndividuoArboreo`). No hay forma exacta de calcular "acumulación de carbono por especie" con el esquema actual — se usa conteo de individuos como proxy. Si el equipo quiere carbono real por taxón, hay que revisar si el modelo debería trackearlo por individuo.
3. **Unidades de Flujos (CO2/CH4/N2O)**: se decidió usar `unidad_medida.simbolo` tal cual viene de cada muestra en vez de forzar una unidad estándar por gas (ver "Decisión de unidades" arriba) — el equipo había dejado esto "por definir" en la propuesta original, falta que lo confirmen.

Rendimiento y despliegue: ya resuelto (2026-09-18/19) — se corrigieron las vistas de `geo/` para agregar en la base de datos en vez de recorrer en Python (trayendo el PR de rendimiento del equipo desde `main` y aplicando el mismo patrón a los endpoints nuevos), se subió a 4 workers de gunicorn en dev, y se corrigió un bug de configuración de `.env` en frontend. Durante el despliegue a producción se encontró y resolvió además un `ImportError` no relacionado con esta tarea (rutas de un feature de recuperación de contraseña que quedaron mezcladas en el merge sin sus vistas commiteadas) — ya resuelto directamente en el servidor. Verificado end-to-end: todos los endpoints nuevos responden 200 en `http://44.213.47.34/`.
