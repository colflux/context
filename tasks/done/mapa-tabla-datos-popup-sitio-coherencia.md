# Mapa: colores de tabla y popup de sitio coherentes con el ETL

**Estado:** cerrada
**Creada:** 2026-09-23
**A cargo:** Viviana
**Sesión de Claude Code:** https://claude.ai/code/session_01HJZ2Lg8Y2Awbc22HWXqKuQ
**Participantes:** Viviana

## Objetivo

La tabla "Datos detallados" del panel de sitio en `/mapas` pintaba los
grupos de columnas (UNIDADEXPERIMENTAL, UNIDADMUESTREO, SITIO, EQUIPO, etc.)
con una paleta local asignada por orden de aparición, distinta de la que usa
la tabla del ETL (`/etl/datos`) — mismos datos, colores distintos según por
dónde se entrara. Además, el popup de un sitio en el mapa mostraba "Sitio
&lt;id&gt;" como título y un conteo plano de "Unidades de muestreo: N" en vez
de los nombres reales de la unidad experimental/de muestreo.

## Contexto

Surgió al comparar visualmente la tabla de `/mapas` (`SiteDetailPanel.tsx`)
contra la de `/etl/datos` (`DatosTable.tsx`) para la misma carga de datos.

## Plan

- [x] Tabla "Datos detallados" (`SiteDetailPanel.tsx`): usar `ENTIDAD_MAP`
      (colores fijos por modelo, vía `catalogo.json`) en vez de la paleta
      `MODELO_COLORS` asignada por índice de aparición — mismo criterio que
      `DatosTable.tsx` del ETL.
- [x] Backend (`app/api/geo/views.py`, endpoint de sitios): agregar
      `unidad_experimental` (nombre) a cada item de `unidades_muestreo` en
      el GeoJSON de sitios.
- [x] Frontend (`types/index.ts`, `GeoMap.tsx`): tipar el nuevo campo y
      reemplazar el popup del sitio — se quita el título "Sitio &lt;id&gt;",
      y en vez del conteo se listan pares `Unidad experimental: <nombre>` /
      `Unidad de muestreo: <nombre>` por cada unidad, en texto plano (sin
      negrilla).
- [x] Reiniciar `backend-web-1` para que el serializer nuevo entre en efecto.
- [x] Detectada y quitada `VITE_MAP_STYLE` fija a estilo oscuro en
      `frontend/.env` — anulaba el cambio de estilo claro/oscuro según tema
      que ya hacía `GeoMap.tsx` (`isDark ? DARK_STYLE : LIGHT_STYLE`).

## Entregables

PR abierto con los cambios en `frontend/` y `backend/` (ver Historial).

## Referencias

- `SiteDetailPanel.tsx`, `DatosTable.tsx`, `GeoMap.tsx`,
  `app/api/geo/views.py`, `utils/catalogoModel.ts`

## Historial

| Fecha | Descripción |
|---|---|
| 2026-09-23 | Se identifica y corrige la inconsistencia de colores entre la tabla de `/mapas` y la del ETL. Se agrega el nombre de unidad experimental/muestreo al popup del sitio en el mapa (antes solo mostraba un conteo). Se quita el override de estilo de mapa oscuro fijo en `.env` que impedía ver el mapa en claro. Tarea cerrada, PR abierto. |
