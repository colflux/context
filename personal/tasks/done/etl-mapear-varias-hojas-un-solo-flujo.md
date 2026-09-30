# ETL: mapear y cargar varias hojas de un Excel en un solo flujo

**Estado:** hecho
**Creada:** 2026-09-24
**A cargo:** Viviana
**Sesión de Claude Code:** https://claude.ai/code/session_01HJZ2Lg8Y2Awbc22HWXqKuQ

## Objetivo

Antes, `CargaArchivo` mapeaba una sola hoja de Excel a la vez (`hoja_activa`
era un `CharField` único): para cargar otra pestaña del mismo archivo (fuente
testvivi: "Unidad Muestreo-Experimental", "CO2 (detalle)", "CH4 (detalle)",
"Clima", "MOM", "COS", "Biomasa") había que repetir todo el asistente
(Analizar → EDA → Mapear por secciones → Guardar) desde cero, creando una
`CargaArchivo` nueva por hoja. Se pidió que un solo flujo permita mapear e
importar todas las hojas del archivo sin repetir el asistente.

## Contexto

También se agrupó la tabla del paso "Análisis EDA" por hoja (antes era una
tabla plana con una columna "Hoja"), en `AnalisisEDA.tsx`.

Decisión de diseño (ver plan de sesión para el detalle completo): se agregó
un campo `hoja` a `MapeoColumna` y un `JSONField hojas` a `CargaArchivo`, en
vez de crear un modelo `CargaHoja` con FK re-apuntada — aditivo, sin
repuntear FKs sobre la base remota de producción, y aprovechando que cada
sección de mapeo ya vive naturalmente en una sola hoja del archivo.

## Plan

- [x] Migración aditiva `0096_mapeocolumna_hoja_carga_hojas` (con backfill
  para cargas existentes) — verificado contra la DB remota.
- [x] `_leer_dataframe_carga(carga, hoja)`, `upload_archivo` analiza todas
  las hojas no-"diccionario" en un solo llamado.
- [x] `mapeo_carga` GET/POST scoped por `hoja` (además de `carga`).
- [x] `_validar_seccion`/`previsualizar_carga`/`importar_carga` procesan
  cada sección agrupando sus mapeos por hoja (una sección puede tener
  columnas mapeadas desde más de una hoja).
- [x] Store del frontend (`useEtlUploadStore.ts`): caché `hojas` por nombre
  de hoja + `setHojaActiva` (swap de slice activo, sin volver a llamar al
  backend al cambiar de hoja).
- [x] `EtlUpload.tsx`: pestañas de hoja en el paso 4 (mapeo), cada una con
  su propio avance de mapeo; `seccionIdx`/`seccionesGuardadas` se mantienen
  compartidos entre hojas (igual que en el backend, donde `hasta_grupo` ya
  agrupa mapeos de todas las hojas de la carga).

## Entregables

Cambios en `backend/app/models/datos.py`, `backend/app/api/etl/views.py`,
migración `0096_mapeocolumna_hoja_carga_hojas.py`, y en
`frontend/src/store/useEtlUploadStore.ts`, `EtlUpload.tsx`,
`AnalisisEDA.tsx`, `useAnalizarFuente.ts`, `useSeccionMutations.ts`,
`useGuardarAvance.ts`, `etl.service.ts`, `types/index.ts`.

Verificado contra la DB remota con la fuente 43 (testvivi): `upload_archivo`
analiza las 7 hojas no-diccionario en un solo llamado; `mapeo_carga`
aísla correctamente los mapeos de cada hoja (guardar/vaciar una hoja no
afecta a las demás); `previsualizar_carga` corre bien sobre el nuevo camino
multi-hoja incluso con una sola hoja mapeada (regresión). `npx tsc --noEmit`
sin errores. Pendiente: probar el flujo completo en el navegador (mapear y
guardar dos hojas distintas de testvivi en una misma carga).

## Referencias

Plan de implementación completo (decisión de diseño A vs B, riesgos, orden
de ejecución) quedó en el plan de la sesión de Claude Code.

## Historial

| Fecha | Descripción |
|---|---|
| 2026-09-24 | Se implementa el rediseño completo (backend + frontend). Verificado por API directa contra la DB remota; falta prueba manual en navegador. |
