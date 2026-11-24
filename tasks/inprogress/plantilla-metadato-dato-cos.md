# Plantilla metadato/dato para COS (carbono orgánico del suelo)

**Estado:** implementado, probado de punta a punta con el archivo real y carga real habilitada (2026-11-24)
**Creada:** 2026-11-19
**A cargo:** Vivi
**Sesión de Claude Code:** sesión actual (ver transcript local)

## Objetivo

Repetir para COS el mismo ejercicio hecho para Flujos CO2/CH4 y para Biomasa: diseñar
y luego implementar (1) la plantilla descargable separada en hojas Metadato/Dato con
diccionario de datos, (2) el modal "Ver detalle de la plantilla" en `/participacion`,
y (3) el mapeo visual/automático de columnas en el flujo de carga.

## Contexto

Reutiliza el plan marco de
[[subida-descarga-formato-metadato-dato-por-metodologia]] (que ya listaba a COS como
metodología pendiente de relevar), mismo patrón ya usado para Biomasa
([[plantilla-metadato-dato-biomasa]], misma sesión).

Punto de partida: Excel real con datos de IDEAM (`context/data/Metadatos y BD
COS.xlsx`), hojas "Metadatos COS" (41 columnas, 52 filas) y "BD COS" (13 columnas,
1795 filas).

A diferencia de Biomasa (7 columnas de Metadato sin modelo) y de lo esperado antes de
relevar, **el modelo de COS ya existe y casi no tiene campos faltantes**:
`backend/app/models/suelo.py` (`CaracterizacionMuestreoSuelo`, `MonitoreoSuelo`,
`SubmuestraSuelo`) ya tiene nombres y `help_text` que coinciden casi literalmente con
las columnas de este Excel — da la impresión de haberse diseñado ya mirando esta misma
fuente. El pendiente real es de **plantilla separada** (hoy COS usa la vista genérica
compartida con MOM/Biomasa, `_CAMPOS_METODOLOGIA`) y de **lógica de pivoteo** para los
campos que cuelgan de `Sitio`/`UnidadMuestreo` por FK inversa (cobertura, disturbio,
ecosistema, caracterización de suelo) — mismo pendiente ya documentado para Flujos.
Diccionario de datos completo en
[docs/arquitectura/plantilla-metadato-dato-cos.md](../../docs/arquitectura/plantilla-metadato-dato-cos.md).

## Plan

- [x] Relevar el Excel real (`Metadatos y BD COS.xlsx`) y cruzar cada columna contra
      el modelo de datos (`backend/app/models/suelo.py`, más los modelos compartidos
      con Flujos/Biomasa: `Sitio`, `UnidadMuestreo`, `CoberturaManual`,
      `DisturbioManual`, `EcosistemaManual`) — documentado en
      [plantilla-metadato-dato-cos.md](../../docs/arquitectura/plantilla-metadato-dato-cos.md).
      De 41 columnas de Metadato, 39 ya tienen modelo; de 13 de Dato, las 13 ya
      tienen modelo.
- [x] Resolver las 4 preguntas abiertas del documento con la usuaria (2026-11-19):
      (1) `Suelo IPCC`/`tipo_de_suelo` son el mismo dato duplicado — se adopta
      `ValorClasificacionTipo` (Suelo_IPCC) como fuente de verdad, `tipo_de_suelo`
      queda para deprecar; (2) investigado por qué `CaracterizacionMuestreoSuelo` no
      tiene FK a `UnidadMuestreo` — artefacto histórico del import de `colfux-db`
      (commit `9110b9c`, 2026-07-01, previo a la convención de `UnidadMuestreo.nombre`
      como identificador natural); cruzando el Excel real se confirma que
      `muestreo_id` es el mismo dato que `UnidadMuestreo.nombre` — se recomienda
      agregar la FK directa al implementar; (3) se quita "Fecha instalación unidad de
      muestreo" de la hoja Dato (estaba mal rotulada); (4) sí aplican a COS las mismas
      decisiones de Flujos (excluir `nombre_proyecto`, hoja "Responsables" para
      `TEAM_MEMBER_*`).
- [x] Agregar FK `unidad_muestreo` a `CaracterizacionMuestreoSuelo` (reemplaza
      `sitio`+`muestreo_id`) y deprecar `CaracterizacionMuestreoSuelo.tipo_de_suelo`
      (2026-11-19): como las tablas de suelo estaban vacías en el contenedor
      compartido (`CaracterizacionMuestreoSuelo`/`MonitoreoSuelo`/`SubmuestraSuelo`,
      0 filas), no hizo falta migración de datos — se removieron `sitio`,
      `muestreo_id` y `tipo_de_suelo` del modelo y se agregó `unidad_muestreo`
      directo (migración `0130_caracterizacion_suelo_fk_unidad_muestreo.py`); el tipo
      de suelo se sigue resolviendo con `ValorClasificacionTipo`/`CoberturaManual`
      (tipo=Suelo_IPCC), como cualquier otra clasificación de `UnidadMuestreo`.
      `app/admin.py` actualizado al nuevo campo.
- [x] Diseñar `_VISTAS_DESNORMALIZADAS["cos_metadato"/"cos_dato"]` con hojas
      Metadato/Dato separadas (análogo a `biomasa_metadato`/`biomasa_dato`, no
      `submuestra_gei`: COS no usa el patrón `seccion`), agregadas a
      `_HOJAS_PLANTILLA` en `backend/app/api/etl/views.py`. `cos_metadato` usa
      `CaracterizacionMuestreoSuelo` como base (1:1 con la unidad de muestreo en los
      datos reales) y reutiliza el subconjunto relevante de
      `_COLUMNAS_PIVOTE_METADATO_GEI` (sin veg_pri/sec/ter ni exposición externa, no
      están en el Excel de COS) más las columnas propias de
      `MonitoreoSuelo` (`_COLUMNAS_PIVOTE_METADATO_COS_MONITOREO`, mismo tratamiento
      de columna fija que cobertura/disturbio — la vista pivoteo real sigue
      pendiente). La vista genérica `"cos"` (compartida con MOM/Biomasa) no se tocó.
- [x] Entregable 1: plantilla descargable con hojas "COS Metadato" (37 columnas) /
      "COS Dato" (13 columnas) + diccionario de datos (`plantilla_vacia`) — verificado
      generando el Excel real (7 hojas en total) y con `manage.py check`.
- [x] Entregable 2: el modal "Ver detalle de la plantilla" (`plantilla_detalle`) ya
      era genérico sobre `_HOJAS_PLANTILLA` (sin cambios desde Biomasa) — verificado
      vía el endpoint (37+13 atributos de COS).
- [x] Entregable 3: mapeo automático de columnas en la carga —
      `_sugerir_mapeos_automaticos`/`_poblar_bronce` ya eran genéricos. Se habilitó la
      casilla "Ya tiene el formato de la plantilla" para COS en `FuenteDrawer.tsx`
      (`soportaMapeoAutomatico`) y `plantillaDisponible: true` en `Participacion.tsx`.
      Verificado con un archivo sintético (encabezados generados por la propia
      plantilla): COS Dato mapea 13/13 automático; COS Metadato 23/37 (14 columnas
      ambiguas: cobertura_IPCC/CLC/IGBP/Nombre_Local/uso_suelo_IPCC comparten
      `ValorClasificacionTipo.valor`, y los 4 pares `monitoreo_*`/`protocolo_*`
      comparten `MonitoreoSuelo.activo`/`.protocolo` — mismo límite ya conocido en
      Flujos/Biomasa, caen al asistente manual).
- [x] Parsear "Profundidad cm" (texto tipo rango "0-10") en
      `profundidad_desde_cm`/`profundidad_hasta_cm`: no fue necesario tocar el
      backend — se resuelve en la transformación del archivo real a formato
      plantilla (ver siguiente punto), separando el texto en las dos columnas ya
      existentes antes de subirlo.
- [x] Transformar el archivo real (`context/data/Metadatos y BD COS.xlsx`) al
      formato de la plantilla descargable y probar la carga real end-to-end
      (2026-11-24): se generó `context/data/COS_plantilla_transformada.xlsx`
      (hojas "COS Metadato" 50 filas / "COS Dato" 1795 filas, encabezados exactos
      de `plantilla_vacia?metodologia=cos`) y se probó contra el backend real
      (upload → mapeo automático → capa bronce). Mapeo automático: 13/13 en Dato,
      23/37 en Metadato (mismo límite de ambigüedad ya conocido). Al intentar
      promover filas de bronce a los modelos reales aparecieron 2 problemas:
      1. **Bloqueaba toda la carga** (`UnidadMuestreo.tipo`/`.unidad_experimental`
         obligatorios, sin columna en la plantilla de COS para resolverlos, a
         diferencia de Biomasa) — **corregido**: se agregaron `UnidadMuestreoTipo`
         y `UnidadExperimental` a la cadena/campos de `cos_metadato` en
         `backend/app/api/etl/views.py`, con 2 columnas nuevas en la plantilla:
         `tipo_unidad_muestreo` y `nombre_unidad_experimental`. Decisión tomada
         con la usuaria (2026-11-24): `nombre_unidad_experimental` = mismo valor
         que `codigo_metadato` (una unidad experimental por codigo_metadato, más
         granular que por sitio); `tipo_unidad_muestreo` sin valor por defecto
         claro del equipo — se usó `"parcela"` como constante en el archivo de
         prueba, pendiente de confirmar con el equipo de datos si corresponde.
      2. `Vereda.codigo_dane` es `unique=True` sin default, pero ninguna plantilla
         (Flujos/Biomasa/COS) trae ese código — solo el nombre de la vereda, que en
         los datos reales de COS viene vacío. El importador genérico intentaba crear
         una `Vereda` nueva por cada `municipio` distinto sin código DANE, y la
         segunda vereda chocaba contra la primera (`codigo_dane=''` repetido).
         **Corregido** (decisión de la usuaria, 2026-11-24): se sacan
         `Vereda`/`Municipio`/`Departamento`/`Region` de la `cadena` de
         `cos_metadato` — por ahora COS no sube esa geografía (`Sitio.vereda` es
         nullable). Mismo patrón expone `biomasa_metadato`, sin tocar todavía.
      3. Tras corregir lo anterior, apareció un `IntegrityError` distinto:
         `UnidadMuestreo.tipo_id` null al crear la unidad desde la hoja "COS Dato".
         Causa: "COS Dato" mapeaba `UnidadMuestreo.nombre` además de
         `codigo_metadato`, y como la hoja "COS Metadato" no mapeaba `nombre`
         (quedaba `''`), el filtro de búsqueda no encontraba la unidad ya creada e
         intentaba crear una nueva sin `tipo`. **Corregido**: se sacó `nombre` del
         mapeo de `UnidadMuestreo` en `cos_dato` (mismo patrón que ya usa
         `biomasa_dato`: solo `codigo_metadato` identifica la fila). Se pierde la
         columna "No. unidad de muestreo" de esa hoja.
      4. Con las filas de "COS Dato" promoviendo limpio, "COS Metadato" seguía
         bloqueada por 4 columnas: `sistema_referencia`/`tipo_localizacion` con
         valores del archivo transformado que no coincidían con las choices del
         modelo (corregido ajustando `COS_plantilla_transformada.xlsx`:
         "EPSG:4326"→"EPSG_4326", "Localización exacta"→"exacta"); y
         `disturbio_dominante`/`ecosistema_IDEAM`, obligatorios en el modelo pero
         vacíos en las 50 filas reales (mismo patrón que Vereda: la fuente no trae
         ese dato). Decisión de la usuaria (2026-11-24): hacerlos opcionales —
         `DisturbioManual.es_dominante` y `ValorClasificacionEcosistema.valor` pasan
         a `blank=True` (migraciones `0132`/`0133`), válido para todas las
         metodologías, no solo COS.
      5. Último bloqueo: "COS Metadato" no mapeaba `UnidadMuestreo.nombre` en
         absoluto (obligatorio, validado como "campo obligatorio sin mapear").
         **Corregido** (decisión de la usuaria, 2026-11-24): se agrega
         `UnidadMuestreo.nombre` a `cos_metadato`, alias `nombre_unidad_muestreo`
         = mismo valor que `codigo_metadato` (mismo criterio ya usado para
         `nombre_unidad_experimental`).
      Con los 5 ajustes aplicados, se repitió la prueba completa contra el archivo
      transformado: **1845/1845 filas promovidas, sin hojas bloqueadas**
      (`"hojas_bloqueadas": [], "filas_promovidas": 1845`). Se decide dejar esos
      datos de prueba en la base (decisión de la usuaria) y habilitar
      `subidaDisponible: true` para COS en `Participacion.tsx`.
- [ ] Confirmar con el equipo de datos el valor de `tipo_unidad_muestreo` para COS
      (hoy "parcela" por defecto en la prueba, sin confirmar).
- [ ] Validar con Andrea/equipo de datos las demás decisiones tomadas (FK nueva,
      deprecación de `tipo_de_suelo`, columnas de Metadato/Dato elegidas, no subir
      Vereda/Municipio/Departamento/Region por ahora).
- [ ] Evaluar si conviene resolver `Vereda.codigo_dane` en el motor genérico (ahora
      evitado en COS, pero sigue latente en `biomasa_metadato` si sus datos reales
      llegan a tocar más de un municipio).

## Entregables

- [Diccionario de datos — COS](../../docs/arquitectura/plantilla-metadato-dato-cos.md)
  (implementado; decisiones de diseño documentadas, pendiente de validar con el
  equipo).
- `backend/app/models/suelo.py`: `CaracterizacionMuestreoSuelo.unidad_muestreo` (FK
  nueva), `.tipo_de_suelo` removido; migración
  `0130_caracterizacion_suelo_fk_unidad_muestreo.py`.
- `backend/app/api/etl/views.py`: `_VISTAS_DESNORMALIZADAS["cos_metadato"/"cos_dato"]`
  (incluye ahora `UnidadMuestreoTipo`/`UnidadExperimental`), `_HOJAS_PLANTILLA`,
  `_ORDEN_COLUMNAS_METADATO_COS_PLANTILLA`, `_ORDEN_COLUMNAS_DATO_COS_PLANTILLA`,
  `_COLUMNAS_PIVOTE_METADATO_COS`, `_COLUMNAS_PIVOTE_METADATO_COS_MONITOREO`.
- `frontend/src/pages/Participacion.tsx` (`plantillaDisponible: true`,
  `subidaDisponible: true` para COS desde 2026-11-24),
  `frontend/src/components/admin/fuentes/FuenteDrawer.tsx` (`soportaMapeoAutomatico`).
- `backend/app/models/cobertura.py` (`DisturbioManual.es_dominante` → `blank=True`,
  migración `0132`), `backend/app/models/ecosistema.py`
  (`ValorClasificacionEcosistema.valor` → `blank=True`, migración `0133`) — afecta a
  todas las metodologías, no solo COS.
- `context/data/COS_plantilla_transformada.xlsx` — archivo real de IDEAM
  transformado al formato de la plantilla, usado para probar la carga real de punta
  a punta (1845/1845 filas promovidas).

## Referencias

- [[subida-descarga-formato-metadato-dato-por-metodologia]] — plan marco del que cuelga esta tarea.
- [plantilla-metadato-dato-co2-camaras.md](../../docs/arquitectura/plantilla-metadato-dato-co2-camaras.md) — mismo ejercicio para Flujos, modelo a seguir.
- [[plantilla-metadato-dato-biomasa]] — mismo ejercicio para Biomasa, hecho en esta misma sesión.
- `backend/app/models/suelo.py` — `CaracterizacionMuestreoSuelo`, `MonitoreoSuelo`, `SubmuestraSuelo`.
- `backend/app/api/etl/views.py` — `_VISTAS_DESNORMALIZADAS["cos"]`.
- `context/data/Metadatos y BD COS.xlsx` — Excel fuente (IDEAM) usado para el relevamiento.

## Historial

| Fecha | Descripción |
|---|---|
| 2026-11-19 | Se crea la tarea reutilizando el plan marco de Flujos/Biomasa. Se releva el Excel real (`Metadatos y BD COS.xlsx`) y se documenta el diccionario de datos propuesto para COS, cruzando cada columna contra el modelo. Hallazgo principal: a diferencia de Flujos/Biomasa, el modelo de suelo (`CaracterizacionMuestreoSuelo`/`MonitoreoSuelo`/`SubmuestraSuelo`) ya existía casi completo y alineado con este Excel — de 54 columnas relevadas (41 Metadato + 13 Dato), 52 ya tienen campo. Quedan 4 preguntas abiertas para validar con el equipo antes de diseñar la plantilla final e implementar los 3 entregables. |
| 2026-11-19 | Se resuelven las 4 preguntas abiertas con la usuaria: `Suelo IPCC`/`tipo_de_suelo` son el mismo dato duplicado (se adopta el catálogo genérico como fuente de verdad, `tipo_de_suelo` queda para deprecar); se investiga el origen de la falta de FK `CaracterizacionMuestreoSuelo`→`UnidadMuestreo` (artefacto del import de `colfux-db` en julio 2026, previo a la convención de identificador natural de noviembre) y, cruzando el Excel real, se confirma que `muestreo_id` duplica `UnidadMuestreo.nombre` (coincide 1:1 con el sufijo de `codigo_metadatos` en las 50 unidades) — se recomienda agregar la FK directa al implementar; se quita "Fecha instalación unidad de muestreo" de la hoja Dato (mal rotulada); se confirma que aplican a COS las mismas exclusiones de Flujos. Documento actualizado (`plantilla-metadato-dato-cos.md`). Queda pendiente la implementación (vista desnormalizada, FK nueva, deprecar `tipo_de_suelo`, los 3 entregables). |
| 2026-11-19 | Se implementan los 4 pendientes sin esperar validación del equipo (instrucción explícita de la usuaria): migración de `CaracterizacionMuestreoSuelo` (FK `unidad_muestreo` nueva, se quitan `sitio`/`muestreo_id`/`tipo_de_suelo` — tablas de suelo vacías en el contenedor compartido, sin migración de datos necesaria); vistas `cos_metadato`/`cos_dato` nuevas en `_VISTAS_DESNORMALIZADAS` (base `CaracterizacionMuestreoSuelo`, reutiliza el subconjunto relevante de columnas de pivoteo de Flujos/Biomasa más las propias de `MonitoreoSuelo`); habilitación de los botones/casillas correspondientes en frontend. Verificado en vivo contra el contenedor compartido: Excel real de 7 hojas, modal de detalle con 37+13 atributos de COS, mapeo automático 13/13 en Dato y 23/37 en Metadato (mismo límite de columnas ambiguas que Flujos/Biomasa). `manage.py check`, `npx tsc --noEmit` limpios. Quedan pendientes: parsear "Profundidad cm" (texto rango) al importar, validar con Andrea/equipo las decisiones tomadas sin preguntar, y probar con el archivo real `Metadatos y BD COS.xlsx` subido tal cual (hoy solo se probó con encabezados generados por la propia plantilla). |
| 2026-11-20 | Pedido explícito de la usuaria: deshabilitar por ahora el botón "Subir datos" en la tarjeta de COS (`Participacion.tsx`, nuevo flag `subidaDisponible: false`) — la plantilla descargable/modal de detalle/mapeo automático quedan activos, pero la carga real no. "Descargar plantilla"/"Ver detalle" siguen sin cambios. |
| 2026-11-24 | Se transforma el archivo real `Metadatos y BD COS.xlsx` al formato de la plantilla (`context/data/COS_plantilla_transformada.xlsx`) y se prueba la carga real contra el backend (upload → mapeo automático → bronce → promoción). Se encuentra y corrige un bloqueo propio de COS: `UnidadMuestreo.tipo`/`.unidad_experimental` son obligatorios pero `cos_metadato` no traía columna para resolverlos (a diferencia de Biomasa) — se agregan `tipo_unidad_muestreo`/`nombre_unidad_experimental` a la plantilla (decisión: unidad experimental = codigo_metadato; tipo por defecto "parcela", sin confirmar con el equipo). Se encuentra un segundo bloqueo, de alcance mayor a esta tarea (`Vereda.codigo_dane` único sin default); decisión inicial: dejarlo pendiente por hoy. |
| 2026-11-24 | Misma sesión, continuación: por pedido explícito de la usuaria ("por ahora no subamos ni municipio, region ni vereda") se sacan esos 4 modelos de la cadena de `cos_metadato` en vez de tocar el motor genérico — resuelve el choque de `Vereda.codigo_dane`. Al repetir la prueba aparecen 3 bloqueos más, los 3 resueltos en la misma sesión: (a) `UnidadMuestreo.tipo_id` null por mismatch de identidad entre hojas Metadato/Dato — se sacó `nombre` del mapeo de `cos_dato` (mismo patrón de `biomasa_dato`); (b) `sistema_referencia`/`tipo_localizacion` con valores mal transformados en el Excel de prueba — corregidos en el archivo; (c) `disturbio_dominante`/`ecosistema_IDEAM` obligatorios pero vacíos en los datos reales — se hacen opcionales a nivel de modelo (`DisturbioManual.es_dominante`, `ValorClasificacionEcosistema.valor`, migraciones `0132`/`0133`, válido para todas las metodologías); (d) `UnidadMuestreo.nombre` sin mapear en "COS Metadato" — se agrega, alias `nombre_unidad_muestreo` = codigo_metadato. Resultado final: **1845/1845 filas promovidas, sin hojas bloqueadas**. Por pedido de la usuaria se dejan esos datos de prueba en la base (no se revierten) y se habilita `subidaDisponible: true` para COS en `Participacion.tsx`. Queda en `inprogress/` por los 3 pendientes de validación con el equipo (no bloquean la carga, ver Plan). |
