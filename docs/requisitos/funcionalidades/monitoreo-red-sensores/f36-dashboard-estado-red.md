# F36 — Dashboard de estado de la red de monitoreo

**Categoría:** Monitoreo de Red y Sensores

## Objetivo

Mostrar un mapa de puntos activos/inactivos (código de colores) e historial de
operatividad por estación.

## Contexto

Es estado de la infraestructura física (sensores/estaciones), distinto de los datos que
esos sensores producen.

## Qué hay

No se encontró evidencia de implementación en el código actual. Los modelos `Sitio`
(`backend/app/models/sitio.py:11`) y `TorreEc` (`backend/app/models/torre.py:34`) no
tienen campos de estado operativo. El endpoint `sitios_geojson`
(`backend/app/api/geo/views.py:108`) ya expone un mapa de sitios consumido por el
frontend (`frontend/src/pages/MapaInteractivo.tsx`,
`frontend/src/components/map/GeoMap.tsx`), pero solo agrega mediciones (conteo, rango
de fechas, último valor), no estado de conectividad/operatividad.

## Qué hace falta

Campo(s) de estado en el modelo o un modelo nuevo tipo `EstadoEstacion`/
`HeartbeatEstacion`, lógica para derivar activo/inactivo, endpoint que lo exponga, y un
componente de mapa/dashboard con código de colores e historial de operatividad.
