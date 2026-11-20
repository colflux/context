# Plantilla metadato/dato para MOM (materia orgánica muerta)

**Estado:** implementado (2026-11-19), pendiente de validar con el equipo y de probar con el archivo real
**Creada:** 2026-11-19
**A cargo:** Vivi
**Sesión de Claude Code:** sesión actual (ver transcript local)

## Objetivo

Repetir para MOM el mismo ejercicio hecho para Flujos CO2/CH4 y Biomasa:
diseñar y luego implementar (1) la plantilla descargable separada en hojas
Metadato/Dato con diccionario de datos, (2) el modal "Ver detalle de la
plantilla" desplegado en `/participacion`, y (3) el mapeo visual/automático
de columnas en el flujo de carga — los 3 entregables acordados con la
usuaria para este tipo de metodología.

## Contexto

Reutiliza el plan marco de
[[subida-descarga-formato-metadato-dato-por-metodologia]] (que ya listaba a
MOM como metodología pendiente de relevar) en vez de crear un proceso nuevo
desde cero — mismo patrón ya aplicado a Biomasa
([[plantilla-metadato-dato-biomasa]]): tarea de implementación puntual que
cuelga del mismo plan general, en vez de una tarea-plan distinta.

Punto de partida: Excel real con datos de IDEAM (`context/data/MOM.xlsx`) que
la usuaria compartió, con hojas "Metadatos MOM" (metadato) y "BD MOM" (dato)
— además trae "Hoja1"/"BMORI sin Duplicados"/"MOM ORI sin duplicados", datos
de trabajo/duplicados de la fuente, no estructura de plantilla.

A diferencia de Flujos, **MOM hoy no tiene plantilla separada
Metadato/Dato** — se sacó explícitamente de `_HOJAS_PLANTILLA` el 2026-11-02
(ver Historial del plan marco) junto con CH4/COS/Biomasa. El diccionario de
datos completo (análogo al de Flujos) queda documentado en
[docs/arquitectura/plantilla-metadato-dato-mom.md](../../docs/arquitectura/plantilla-metadato-dato-mom.md).

## Plan

- [x] Relevar el Excel real (`MOM.xlsx`) y cruzar cada columna contra el
      modelo de datos (`backend/app/models/mom.py` — `MuestraMOM` —, más los
      modelos compartidos con Flujos/Biomasa: `Sitio`, `UnidadMuestreo`,
      `CoberturaManual`, `DisturbioManual`, `EcosistemaManual`,
      `MonitoreoParcela`) — documentado en
      [plantilla-metadato-dato-mom.md](../../docs/arquitectura/plantilla-metadato-dato-mom.md).
      De 49 columnas de Metadato, todas salvo `TEAM_MEMBER_NAME`/
      `TEAM_MEMBER_EMAIL`/`Periodicidad de muestreo` ya tienen modelo
      (mismos 3 gaps ya conocidos de Flujos); de 21 de Dato, las 21 ya
      tienen modelo en `MuestraMOM`.
- [x] Resolver las preguntas abiertas del documento (resuelto con la
      usuaria, 2026-11-19): `DOM_DIST_MGMT` es el mismo campo que
      `disturbio_dominante` de Flujos (`DisturbioManual.es_dominante`, ya
      trabajado ahí); se agregan `cobertura_vegetal_primaria`/`secundaria`
      (+ sus porcentajes) por paralelismo con Flujos, aunque el Excel
      puntual solo traiga terciaria; `Tamaño unidad de muestreo (área en
      cm2)` corresponde a `Parcela.area` (queda pendiente de validar la
      discrepancia de unidad: la columna dice cm² pero `Parcela.area` es
      m²). Falta todavía validar con Andrea/equipo de datos el resto del
      documento (columnas ambiguas como "Ecosistema / Cobertura").
- [x] Diseñar `_VISTAS_DESNORMALIZADAS["mom_metadato"/"mom_dato"]` (vistas
      nuevas, no se tocó la vista genérica `"mom"` que ya usan
      `exportar_carga`/`datos_carga`), agregadas a `_HOJAS_PLANTILLA` en
      `backend/app/api/etl/views.py`. Se reutilizó
      `_PIVOTE_EXTRA_POR_VISTA`/`_ORDEN_EXTRA_POR_VISTA` (mecanismo
      generalizado para Biomasa/COS) con una columna de pivoteo nueva propia
      de MOM (`_COLUMNAS_PIVOTE_METADATO_MOM_MONITOREO`, análoga a
      `MonitoreoSuelo` en COS) para los 4 pares `monitoreo_*`/`protocolo_*`
      (`MonitoreoParcela`).
- [x] Entregable 1: plantilla descargable con hojas "MOM Metadato" (51
      columnas) / "MOM Dato" (21 columnas) + diccionario de datos
      (`plantilla_vacia`) — verificado generando el Excel real (8 hojas en
      total entre Flujos/Biomasa/COS/MOM) y con `manage.py check` en el
      contenedor compartido (`backend-web-1`).
- [x] Entregable 2: el modal "Ver detalle de la plantilla"
      (`PlantillaDetalleModal.tsx` + endpoint `plantilla_detalle`) ya era
      genérico sobre las hojas que devuelve el backend (filtrado por
      `?metodologia=`) — no hizo falta tocarlo. Verificado vía
      `_hojas_plantilla_vacia(metodologia="mom")`.
- [x] Entregable 3: mapeo automático de columnas en la carga —
      `_sugerir_mapeos_automaticos`/`_poblar_bronce` ya eran genéricos sobre
      `_HOJAS_PLANTILLA`, no hizo falta tocarlos. Se habilitó la casilla
      "Ya tiene el formato de la plantilla" para MOM en `FuenteDrawer.tsx`
      (`soportaMapeoAutomatico`). Muchas columnas de "MOM Metadato" quedan
      "ambiguas" por compartir `modelo.campo` (`ValorClasificacionTipo.valor`,
      `MonitoreoParcela.activo`/`protocolo`, `CoberturaManual.porcentaje`,
      `ExposicionExterna.distancia_m`) — mismo límite ya conocido en
      Flujos/Biomasa/COS, caen al asistente manual.
- [ ] Validar con Andrea/equipo de datos las decisiones tomadas sin
      preguntar (exclusión de `nombre_proyecto`/"Periodicidad de muestreo",
      columnas ambiguas como "Ecosistema / Cobertura") y, si corresponde,
      resolver la discrepancia de unidad de `Parcela.area` (cm² en el
      Excel vs. m² en el modelo).
- [ ] Probar con un archivo real de MOM subido tal cual (hoy solo se probó
      con encabezados generados por la propia plantilla, no con
      `context/data/MOM.xlsx`).

## Entregables

- [Diccionario de datos — MOM](../../docs/arquitectura/plantilla-metadato-dato-mom.md)
  (implementado; decisiones de diseño documentadas, pendiente de validar
  con el equipo).
- `backend/app/api/etl/views.py`: `_VISTAS_DESNORMALIZADAS["mom_metadato"/"mom_dato"]`,
  `_HOJAS_PLANTILLA`, `_ORDEN_COLUMNAS_METADATO_MOM_PLANTILLA`,
  `_ORDEN_COLUMNAS_DATO_MOM_PLANTILLA`, `_COLUMNAS_PIVOTE_METADATO_MOM_MONITOREO`,
  `_PIVOTE_EXTRA_POR_VISTA`, `_ORDEN_EXTRA_POR_VISTA`.
- `frontend/src/pages/Participacion.tsx` (`plantillaDisponible: true` para MOM;
  `subidaDisponible: false` desde 2026-11-20, "Subir datos" deshabilitado a propósito),
  `frontend/src/components/admin/fuentes/FuenteDrawer.tsx` (`soportaMapeoAutomatico`).

## Referencias

- [[subida-descarga-formato-metadato-dato-por-metodologia]] — plan marco del que cuelga esta tarea.
- [plantilla-metadato-dato-co2-camaras.md](../../docs/arquitectura/plantilla-metadato-dato-co2-camaras.md) — mismo ejercicio para Flujos, modelo a seguir.
- [[plantilla-metadato-dato-biomasa]] — mismo ejercicio recién hecho para Biomasa, metodología hermana en el mismo Excel original.
- [[mapeo-automatico-plantilla-flujos-co2]] — referencia para el entregable 3.
- `backend/app/models/mom.py`, `backend/app/models/sitio.py` (`Parcela`, `MonitoreoParcela`).
- `backend/app/api/etl/views.py` — `_VISTAS_DESNORMALIZADAS["biomasa_metadato"]`/`["cos_metadato"]` (patrón replicado), `["mom_metadato"]`, `["mom_dato"]`.
- `context/data/MOM.xlsx` — Excel fuente (IDEAM) usado para el relevamiento.

## Historial

| Fecha | Descripción |
|---|---|
| 2026-11-19 | Se crea la tarea, mismo patrón que [[plantilla-metadato-dato-biomasa]]: reutiliza el plan marco de Flujos ([[subida-descarga-formato-metadato-dato-por-metodologia]]) en vez de un proceso nuevo. Se releva el Excel real (`MOM.xlsx`) y se documenta el diccionario de datos propuesto para MOM, cruzando cada columna contra el modelo (`MuestraMOM` + modelos compartidos con Flujos/Biomasa). Quedan preguntas abiertas para validar con el equipo antes de diseñar la plantilla final e implementar los 3 entregables (descarga con diccionario, modal de detalle, mapeo en la carga). |
| 2026-11-19 | La usuaria resuelve las 3 preguntas abiertas de ese primer relevamiento: `DOM_DIST_MGMT` es el mismo `disturbio_dominante` ya trabajado en Flujos (`DisturbioManual.es_dominante`); se agregan a la plantilla `cobertura_vegetal_primaria`/`secundaria` (con sus porcentajes) por paralelismo con Flujos, aunque este Excel puntual solo traiga terciaria; `Tamaño unidad de muestreo (área en cm2)` corresponde a `Parcela.area`, no a `UnidadMuestreo.area_cm2` (específico de cámaras GEI) — queda pendiente de validar la discrepancia de unidad (columna en cm², `Parcela.area` en m²). Actualizado `docs/arquitectura/plantilla-metadato-dato-mom.md`. |
| 2026-11-19 | Se implementan los 3 entregables: vistas `mom_metadato`/`mom_dato` nuevas en `_VISTAS_DESNORMALIZADAS` (reutilizando el mecanismo `_PIVOTE_EXTRA_POR_VISTA`/`_ORDEN_EXTRA_POR_VISTA` ya generalizado para Biomasa/COS), más una columna de pivoteo nueva propia de MOM para `MonitoreoParcela` (`_COLUMNAS_PIVOTE_METADATO_MOM_MONITOREO`, análoga a `MonitoreoSuelo` en COS). Habilitados los botones/casillas correspondientes en frontend (`Participacion.tsx`, `FuenteDrawer.tsx`). Verificado contra el contenedor compartido (`backend-web-1`): `manage.py check` limpio, Excel real de 2 hojas ("MOM Metadato" 51 columnas, "MOM Dato" 21 columnas) generado sin errores, `plantilla_detalle` filtrado por `?metodologia=mom` devuelve solo esas 2 hojas. `npx tsc --noEmit` limpio; `npx eslint` sin errores nuevos (los 2 errores preexistentes de `FuenteDrawer.tsx` no están relacionados con este cambio). Quedan pendientes: validar con Andrea/equipo las decisiones tomadas sin preguntar y probar con el archivo real `MOM.xlsx` subido tal cual. |
| 2026-11-20 | Pedido explícito de la usuaria: deshabilitar por ahora el botón "Subir datos" en la tarjeta de MOM (`Participacion.tsx`, nuevo flag `subidaDisponible: false`) — la plantilla descargable/modal de detalle/mapeo automático quedan activos, pero la carga real no. "Descargar plantilla"/"Ver detalle" siguen sin cambios. |
