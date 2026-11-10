# Opción de incluir Clima (MuestraAmbiental) en la misma hoja de Flujos CO2

**Estado:** pendiente
**Creada:** 2026-11-09
**A cargo:** Viviana
**Sesión de Claude Code:** https://claude.ai/code/session_019pTWH1XKsvNNawB2zGYDNo

## Objetivo

Hoy la carga de datos de clima (`MuestraAmbiental`: `soil_temp`, `air_temp`,
`atm_press`, `relat_humid`, `dew_point`, `water_level`, `ph`) es independiente de
la de Flujos CO2 (`MuestraGEI`/`SubmuestraGEI`), vía la vista `clima` de
`_VISTAS_DESNORMALIZADAS` — sin hoja propia en la plantilla descargable (no está en
`_HOJAS_PLANTILLA`).

En la práctica, algunas fuentes miden flujo y contexto ambiental al mismo tiempo, en
el mismo archivo/fila (confirmado con un archivo real: columnas `hour`, `chamber_vol`,
`day/night`, `co2_ori` (= valor de flujo), `Unidades`, `soil_temp`, `air_temp`,
`atm_press`, `relat_humid`, `dew_point`, `water_level_cm` todas en la misma hoja).

Se quiere dar la **opción** de subir ambos juntos en una sola hoja/carga cuando la
fuente los trae así, sin fusionar las entidades: `MuestraAmbiental` y
`MuestraGEI`/`SubmuestraGEI` siguen siendo modelos separados — el enlace es solo a
nivel de fila de origen (misma `unidad_muestreo`/`fecha`/`hora`). La carga de clima
por separado (como hoy) se mantiene funcionando igual.

## Contexto

- Confirmado en sesión: `co2_ori` no es un campo nuevo — mapea a
  `SubmuestraGEI.valor` (columna `valor_flujo`), la columna `Unidades` junto a ella
  ya es `unidad_flujo`. No hay gap de modelo ahí.
- Los 7 campos biomet (`soil_temp`...`ph`) SÍ están modelados (`MuestraAmbiental`,
  `backend/app/models/co2.py`), con `help_text` completo — el gap es solo que no
  aparecen como columnas opcionales de la hoja "Flujos CO2 - Dato".
- `MuestraAmbiental` tiene su propia FK a `UnidadMuestreo`, paralela a `MuestraGEI`
  (no cuelga de `SubmuestraGEI`) — por eso no se puede agregar por la cadena de FKs
  hacia adelante que usa `_campos_planos`/`cadena` como el resto de columnas de
  `submuestra_gei`. Necesita su propia lógica de fila, no una columna más de la
  cadena existente.
- Precedente de modelos "evento" con fecha/hora propia en la misma fila de import:
  `_MODELOS_EVENTO = {"MuestraAmbiental", "MuestraMOM", "SubmuestraGEI"}`
  (`backend/app/api/etl/views.py`).

## Plan

- [x] Agregar las columnas biomet (`soil_temp`, `air_temp`, `atm_press`,
      `relat_humid`, `dew_point`, `water_level_cm`, `pH`) a la hoja "Flujos CO2 -
      Dato" — implementado 2026-11-09 vía `_COLUMNAS_PIVOTE_DATO_GEI` en
      `backend/app/api/etl/views.py`, apendizadas al final de la hoja (mismo patrón
      que `_COLUMNAS_PIVOTE_METADATO_GEI`). Solo encabezados — sin datos reales
      todavía, ver siguiente paso.
- [ ] En `importar_carga`/el mapeo de columnas: si esas columnas vienen con dato en
      una fila, crear (o encontrar) un `MuestraAmbiental` con el mismo
      `unidad_muestreo`/`fecha`/`hora` de esa fila, sin tocar la creación de
      `MuestraGEI`/`SubmuestraGEI`. Si vienen vacías, no crear nada — la carga de
      Clima aparte sigue funcionando igual que hoy.
- [ ] Definir qué pasa si una `MuestraAmbiental` ya existe para esa
      `unidad_muestreo`/`fecha`/`hora` (¿actualiza, ignora, error?) — mismo criterio
      de duplicados que ya usa `_MODELOS_EVENTO` para otros modelos evento.
- [ ] Actualizar `docs/arquitectura/plantilla-metadato-dato-co2-camaras.md` con el
      resultado.

## Entregables

(Pendiente — tarea no iniciada.)

## Referencias

- `backend/app/models/co2.py` — `MuestraAmbiental`
- `backend/app/api/etl/views.py` — `_VISTAS_DESNORMALIZADAS["clima"]`,
  `_HOJAS_PLANTILLA`, `_MODELOS_EVENTO`
- [Plantilla de carga/descarga: metadato y dato de CO2/CH4](../../docs/arquitectura/plantilla-metadato-dato-co2-camaras.md)

## Historial

| Fecha | Descripción |
|---|---|
| 2026-11-09 | Se crea la tarea a partir de la revisión de 20 columnas de un archivo fuente real de cámaras: se confirma que `co2_ori` no es un gap (mapea a `valor_flujo` existente) y que los 7 campos biomet sí están modelados pero sin hoja/columnas en la plantilla de Flujos CO2. Usuario confirma: mantener `MuestraAmbiental` como entidad separada, pero dar la opción de incluir sus atributos en la misma hoja/carga que Flujos CO2 para poder enlazarlos por fila. |
| 2026-11-09 | Usuario pide avanzar solo con la parte de la plantilla por ahora: se agregan las 7 columnas biomet a la hoja "Flujos CO2 - Dato" (18 columnas en total), verificado en vivo contra `_hojas_plantilla_vacia()`. Queda pendiente la lógica de `importar_carga`/`exportar_carga` para crear/completar el `MuestraAmbiental` enlazado — hoy las columnas solo reservan el lugar en la plantilla descargable, sin datos reales. |
| 2026-11-09 | Usuario da el listado final de 20 atributos para la hoja Dato: agrega `codigo_metadato` (reemplaza a `nombre_unidad_muestreo` como llave de referencia a Metadato) y `anillo`/`microtopo` como columnas nuevas y separadas de `tubo`/Metadato (antes se asumía `anillo`≈`tubo`, corregido: `anillo` es `UnidadMuestreo.diametro_anillo_cm`, distinto de `MuestraGEI.tubo`). Implementado y verificado en vivo — la hoja queda con 20 columnas en el orden exacto pedido. Sigue pendiente la lógica de enlace de `importar_carga`/`exportar_carga` (sin cambios en este punto). |
| 2026-11-09 | Usuario pide sacar `microtopo` de Dato (queda solo en Metadato). La hoja "Flujos CO2 - Dato" queda en 19 columnas. Verificado en vivo. |
