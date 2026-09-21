# Rendimiento de la API geográfica del backend

**Estado:** hecha
**Creada:** 2026-09-18
**Cerrada:** 2026-09-20

## Objetivo

Que los endpoints geográficos del backend (`/api/geo/sitios/`, `/api/geo/series/`, `/api/geo/resumen/`) agreguen los datos en la base de datos en vez de traer todas las mediciones a Python, para que el tiempo de respuesta y el consumo de memoria dejen de crecer linealmente con el volumen de datos cargados.

## Contexto

Daniel (`DanielUbaque`) abrió el PR `colflux/backend#15` (rama `fix/rendimiento-geo`) tras revisar el geoportal con los datos ya cargados. El diagnóstico ya estaba registrado en `ROADMAP.md` del backend, en "Ideas mencionadas, no decididas": `sitios_geojson` y `resumen_geografico` traían **todas** las `SubmuestraCO2`/`SubmuestraGEI` filtradas a Python y agregaban a mano (conteos, min/max, última medición) en vez de usar `.values().annotate()` y `DISTINCT ON` de Postgres. Faltaba medir el impacto real, y el PR lo trae junto con la corrección.

Medido sobre la copia de producción (113 sitios, 7.048 `SubmuestraGEI`, 2 proyectos):

```
                                        antes     después
/api/geo/series/                       14,07 s     0,13 s
/api/geo/resumen/?nivel=departamento   12,63 s     0,12 s
/api/geo/resumen/?nivel=sitio          13,05 s     0,44 s
/api/geo/sitios/                        1,23 s     0,89 s
```

La página de Mapas del frontend hace cuatro llamadas a la API: en producción sumaban ~37 segundos, ahora menos de 2. Más que el tiempo, preocupaba la memoria: el contenedor pasaba de 191 MB sin datos a 864 MB con estos 7.048 registros, con costo creciendo en línea recta.

De paso, el PR corrige un bug encontrado: `CLAUDE.md` documentaba `/api/geo/resumen/` con "mismos filtros que `series`" (lista que incluye `sitio`), pero la vista no implementaba ese filtro — `?nivel=sitio&sitio=105` devolvía los 94 sitios agrupados en vez de uno solo, sin error visible. Se detectó porque el servidor MCP de `ia-functions` usa ese filtro.

**Revisión de impacto en frontend (2026-09-18):** antes de aprobar, se revisó si el cambio rompía algún contrato consumido por `colflux/frontend`. Se comparó el diff contra `src/types/index.ts` del frontend:
- `series_co2`: respuesta idéntica byte a byte, confirmado por el autor.
- `resumen_geografico`: los campos que consume el frontend (`total_muestras`, `promedio`, `minimo`, `maximo`, `rango_fechas`, `ultima_medicion`, ids de departamento/municipio según nivel) no cambian de forma. El PR agrega un campo nuevo `excluidos` en la raíz (aditivo, no lo lee el frontend) y soporte para `?sitio=` y `nivel=region`/`nivel=sitio`, que el frontend **no usa** — solo pide `departamento`, `municipio`, `vereda` (ver `GeoMap.tsx`, `FilterPanel.tsx`, `DashboardIndicadores.tsx`).
- `sitios_geojson`: `SitioProperties` no cambia de forma.
- Único cambio de comportamiento observable: el desempate de `ultima_medicion` cuando hay varias lecturas con la misma fecha pasa de no determinista (ganaba lo último que devolviera la base) a determinista (gana el `id` mayor). No afecta el contrato de tipos del frontend.

Conclusión: sin riesgo para el frontend. Se aprobó y mergeó el PR.

## Plan

- [x] Revisar si Daniel tenía PRs abiertos en backend/frontend
- [x] Analizar el diff de `backend#15` en detalle
- [x] Verificar contra el código del frontend que no rompe ningún contrato consumido
- [x] Aprobar y mergear `backend#15`
- [ ] Evaluar si vale la pena que el frontend empiece a usar el filtro `?sitio=` de `resumen_geografico` ahora que está implementado correctamente
- [ ] Evaluar `ResumenGeoMensual` (tabla materializada, mencionada como "decisión tomada" en `ROADMAP.md` del backend) — el PR la deja opcional, no la reemplaza ni la bloquea

## Entregables

- PR mergeado: https://github.com/colflux/backend/pull/15 (mergeado 2026-09-18)
- `backend/specs/rendimiento-geo.md` — spec detallada del autor con mediciones y verificación de equivalencia
- `backend/scripts/medir_resumen_geo.py` — script de medición (solo lectura) que compara agregar en Python vs. en SQL

## Referencias

- `colflux/backend#15` — https://github.com/colflux/backend/pull/15
- `ROADMAP.md` del backend, sección "Ideas mencionadas, no decididas" — origen del diagnóstico
- `colflux/frontend` — `src/types/index.ts`, `src/components/map/GeoMap.tsx`, `src/hooks/useResumenGeo.ts`, `src/features/filters/FilterPanel.tsx` — código revisado para confirmar que no hay ruptura de contrato

## Historial

| Fecha | Descripción |
|---|---|
| 2026-09-18 | Se crea la tarea. Se detecta el PR `backend#15` de Daniel al preguntar por PRs abiertos del equipo. Se analiza el diff completo, se compara contra los tipos y hooks del frontend para confirmar que no rompe ningún contrato consumido, se aprueba y se mergea. Quedan pendientes dos ideas de seguimiento, sin decidir todavía: usar el filtro `?sitio=` desde el frontend, y evaluar la tabla materializada `ResumenGeoMensual` mencionada en el `ROADMAP.md` del backend. |
| 2026-09-20 | Se cierra la tarea y se mueve a `done`. Las dos ideas de seguimiento (filtro `?sitio=` en frontend, tabla materializada `ResumenGeoMensual`) quedan sin decidir, registradas aquí como referencia futura si se retoman. |
