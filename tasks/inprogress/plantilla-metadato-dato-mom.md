# Plantilla metadato/dato para MOM (materia orgánica muerta)

**Estado:** implementado (2026-11-19) y carga real habilitada (2026-11-24) — `subidaDisponible: true` en `Participacion.tsx`, validado end-to-end con el archivo real de IDEAM (48 `UnidadMuestreo` / 1176 `MuestraMOM` promovidas sin error)
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
- [x] Transformar el archivo real (`context/data/MOM.xlsx`) al formato de la
      plantilla descargable y probar la carga real end-to-end (2026-11-24):
      se generó `context/data/MOM_plantilla.xlsx` (hojas "MOM Metadato" 48
      filas / "MOM Dato" 1176 filas, encabezados exactos de
      `plantilla_vacia?metodologia=mom`). Antes de transformar se encontraron
      y corrigieron (con confirmación de la usuaria) 4 problemas de calidad
      de datos reales de la fuente IDEAM, ninguno de la plantilla: (1) la
      columna `ID` de "BD MOM" usa el prefijo `IDEAM_MOM_` mientras
      `codigo_metadatos` de "Metadatos MOM" usa `IDEAM__` — normalizado
      quitando `_MOM_`→`__`, cruza 100% (48/48); (2) la columna `sitio` de
      "Metadatos MOM" está vacía en las 48 filas y el nombre real del sitio
      (ej. "PNN Chingaza") quedó cargado por error en la columna vecina
      "Tipo de localización" — se tomó de ahí; (3)
      `nombre_unidad_experimental`/`nombre_unidad_muestreo` no tienen
      columna directa en Metadatos, pero "BD MOM" trae `Site`
      (ej. "Palacios", es la unidad experimental, no el sitio pese al
      nombre) y `# Unidad de Muestre` (ej. "P1") — verificado 100%
      consistente con el desglose de `codigo_metadato` en las 1176 filas;
      (4) en las columnas geográficas, `departamento` siempre repetía
      `region_natural` ("Andes") y los valores reales de
      departamento/municipio habían quedado corridos una columna a la
      derecha (en `Municipio`/`Vereda`) — corregido el corrimiento,
      `Vereda.nombre` queda sin dato (no sobrevive ningún valor tras el
      corrimiento). Subido contra el backend real (proyecto
      `TEST-bronce-temporal-borrar`, mismo usado para COS): el mapeo
      automático y la carga a la capa bronce funcionaron sin problemas
      (1224 filas de `FilaBronce` creadas, carga 371). Al promover de
      bronce a los modelos reales, la carga falló con
      `null value in column "latitud" of relation "app_sitio" violates
      not-null constraint` — causa: a diferencia de Flujos (que no lleva
      `Sitio.nombre` en la hoja Dato, solo `UnidadMuestreo.codigo_metadato`
      como llave de referencia, ver `_LLAVE_REFERENCIA_GEI`), la vista
      `mom_dato` sí incluye la columna `sitio` (`Sitio.nombre`) — el motor
      de importación genérico intenta `get_or_create` un `Sitio` nuevo solo
      con ese nombre (sin lat/long, que si vienen en Metadato) y choca
      contra el NOT NULL de `latitud`. **No se tocó el modelo/motor de
      importación** (mismo criterio ya aplicado a COS el mismo día, ver
      [[plantilla-metadato-dato-cos]]): se revierte `subidaDisponible` a
      `false` en `Participacion.tsx` hasta resolver. Es además muy probable
      que, resuelto ese bloqueo, aparezca el mismo choque de
      `Vereda.codigo_dane` único que bloqueó a COS (acá hay 2 municipios
      distintos sin código DANE en los datos reales). La capa bronce quedó
      cargada en el proyecto de prueba (fuente 89, carga 371) — no se borró,
      el proyecto es justamente para este tipo de prueba descartable.
- [x] Resolver el choque de `Sitio.latitud` NOT NULL y, después, los 2
      bloqueos que aparecieron a continuación — mismo día, 2026-11-24, misma
      sesión que pidió explícitamente "habilitar el botón, no solo
      documentar y dejar pendiente" (a diferencia del criterio usado antes
      ese mismo día para COS, que sí quedó deferido):
      1. **`Sitio.latitud` NOT NULL**: se sacó `Sitio` de la cadena/campos
         de `mom_dato` (ya no trae `Sitio.nombre`) — mismo patrón que
         `biomasa_dato`, que nunca incluyó `Sitio`. `UnidadMuestreo.codigo_metadato`
         ya es la llave que cruza con Metadato (que sí crea/completa el
         `Sitio` real).
      2. **`tipo_id` (`UnidadMuestreo`) NOT NULL**: aun saliendo `Sitio`, el
         mismo error reapareció — causa real: `mom_dato`'s `UnidadMuestreo`
         también traía `nombre`/`fecha_instalacion` de más, que no
         satisfacen `_CAMPOS_IDENTIDAD["UnidadMuestreo"]`
         (`nombre`+`tipo`+`unidad_experimental`) y por lo tanto no
         matcheaban la fila que creó "MOM Metadato", creando una
         `UnidadMuestreo` duplicada sin `tipo`. Se redujo a solo
         `codigo_metadato` (patrón `biomasa_dato`), y se le sacaron las 2
         columnas de más a `_ORDEN_COLUMNAS_DATO_MOM_PLANTILLA` (21→18
         columnas).
      3. **`Vereda.codigo_dane` único sin valor**: exactamente el bloqueo ya
         documentado para COS. Se sacó `Vereda`/`Municipio`/`Departamento`/`Region`
         de la cadena/campos de `mom_metadato` (`Sitio.vereda` es nullable),
         mismo fix ya aplicado a `cos_metadato` el mismo día — sin tocar el
         modelo ni el motor de importación genérico.
      4. **"Campo requerido vacío" bloqueaba las 48 filas de "MOM
         Metadato" enteras** (nunca llegaban a promover, por eso el bug de
         arriba ni se veía resuelto): `disturbio_dominante`/`ecosistema_IDEAM`
         (ya resueltos sin tocar MOM — otra sesión en paralelo les agregó
         `blank=True` a `DisturbioManual.es_dominante`/
         `ValorClasificacionEcosistema.valor` el mismo día), más
         `intervenido` (`Sitio`, vacío en las 48 filas) y `sistema_referencia`
         (`SistemaReferencia.nombre`, vacío en las 48 filas) y
         `tipo_unidad_muestreo` (`UnidadMuestreoTipo.nombre`, vacío en 16/48).
         Decisión de la usuaria para `sistema_referencia`: en vez de
         bloquear o sacar la columna, rellenarla con el default genérico
         EPSG_4326 (WGS84, el srid de `Sitio.geom`) y dejarlo como aviso no
         bloqueante — se implementó un mecanismo nuevo y reutilizable en
         `_crear_mapeos_automaticos_bronce` (`_DEFAULTS_CAMPOS_CATALOGO_BRONCE`,
         también cubre `Sitio.intervenido`→"no") que, al auto-mapear una
         columna de este diccionario, la crea con `estrategia_nulos='manual'`
         + `valor_relleno_manual` en vez de `'dejar_null'` — reusa el
         mecanismo YA existente de "rellenar manualmente", así que la fila
         nunca llega a "Campo requerido vacío", **sin tocar ningún modelo**
         (`Sitio.intervenido`/`SistemaReferencia.nombre` siguen sin
         `blank=True`). Se agregó además `advertencia_relleno` en
         `_validar_columna` para que el conteo de filas rellenadas con el
         default quede visible (no silencioso) en la vista tipo Excel.
         `tipo_unidad_muestreo` (16/48 vacías, 32/48 ya con "Parcela") se
         resolvió aparte, en el dato: se completó `MOM_plantilla.xlsx` con
         "Parcela" en las 16 filas vacías (mismo valor que las otras 32) —
         decisión de dato puntual de MOM, no un default global del motor.
      Resultado final (carga 381, mismo proyecto `TEST-bronce-temporal-borrar`):
      `_validar_y_promover_bronce` devuelve `{"ok": True, "hojas_bloqueadas": [],
      "filas_promovidas": 1224, ...}` — 48 `UnidadMuestreo`/`UnidadExperimental`,
      1176 `MuestraMOM`, más `Sitio`/`EcosistemaManual`/`Parcela`/`UnidadMuestreoTipo`/
      `SistemaReferencia` creados sin error.
- [x] Pasar `subidaDisponible: true` para MOM en `Participacion.tsx`
      (ya estaba en `true` de una iteración anterior de esta sesión; se
      actualizó el comentario de la interfaz `Metodologia` para dejar claro
      que ahora solo COS queda bloqueada, no MOM). `npx tsc --noEmit` limpio.

## Entregables

- [Diccionario de datos — MOM](../../docs/arquitectura/plantilla-metadato-dato-mom.md)
  (implementado; decisiones de diseño documentadas, pendiente de validar
  con el equipo).
- `backend/app/api/etl/views.py`: `_VISTAS_DESNORMALIZADAS["mom_metadato"/"mom_dato"]`,
  `_HOJAS_PLANTILLA`, `_ORDEN_COLUMNAS_METADATO_MOM_PLANTILLA`,
  `_ORDEN_COLUMNAS_DATO_MOM_PLANTILLA`, `_COLUMNAS_PIVOTE_METADATO_MOM_MONITOREO`,
  `_PIVOTE_EXTRA_POR_VISTA`, `_ORDEN_EXTRA_POR_VISTA`.
- `frontend/src/pages/Participacion.tsx` (`plantillaDisponible: true` y
  `subidaDisponible: true` para MOM — "Subir datos" habilitado),
  `frontend/src/components/admin/fuentes/FuenteDrawer.tsx` (`soportaMapeoAutomatico`).
- `backend/app/api/etl/views.py`: `_DEFAULTS_CAMPOS_CATALOGO_BRONCE` (mecanismo
  nuevo y reutilizable para otras metodologías: default + aviso no bloqueante en
  vez de bloquear la fila cuando un campo obligatorio de catálogo viene vacío),
  `advertencia_relleno` en `_validar_columna`.
- `context/data/MOM_plantilla.xlsx` — archivo real de IDEAM transformado al formato
  de la plantilla (48 filas Metadato / 1176 Dato), usado para la prueba de carga
  real que terminó en éxito.

## Referencias

- [[subida-descarga-formato-metadato-dato-por-metodologia]] — plan marco del que cuelga esta tarea.
- [plantilla-metadato-dato-co2-camaras.md](../../docs/arquitectura/plantilla-metadato-dato-co2-camaras.md) — mismo ejercicio para Flujos, modelo a seguir.
- [[plantilla-metadato-dato-biomasa]] — mismo ejercicio recién hecho para Biomasa, metodología hermana en el mismo Excel original.
- [[plantilla-metadato-dato-cos]] — misma prueba de carga real el mismo día (2026-11-24), mismo criterio de no tocar el motor de importación y dejar `subidaDisponible: false` hasta resolver el bloqueo.
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
| 2026-11-24 | Pedido de la usuaria: habilitar la subida real de MOM, empezando por transformar `context/data/MOM.xlsx` al formato de la plantilla para poder probar la carga. Antes de transformar se detectaron y confirmaron con la usuaria 4 problemas de calidad de datos de la fuente IDEAM (no de la plantilla): IDs de "BD MOM"/"Metadatos MOM" con prefijo distinto (`IDEAM_MOM_` vs `IDEAM__`, normalizado); columna `sitio` vacía con el nombre real del sitio mal cargado en "Tipo de localización"; `nombre_unidad_experimental`/`nombre_unidad_muestreo` sin columna directa pero reconstruibles 100% desde `Site`/`# Unidad de Muestre` de "BD MOM"; columnas geográficas (departamento/municipio/vereda) corridas una posición. Se generó `context/data/MOM_plantilla.xlsx` (48 filas Metadato / 1176 Dato) y se probó la carga real contra el backend compartido (proyecto `TEST-bronce-temporal-borrar`): mapeo automático y carga a bronce exitosos (1224 `FilaBronce`), pero la promoción a modelos reales falló con `null value in column "latitud" of relation "app_sitio" violates not-null constraint` — la vista `mom_dato` incluye `Sitio.nombre` como columna (a diferencia de Flujos, que solo usa `codigo_metadato` como llave de referencia en Dato) y el motor genérico intenta crear un `Sitio` nuevo solo con el nombre, sin coordenadas. Mismo criterio que se usó el mismo día para COS ([[plantilla-metadato-dato-cos]], bloqueo de `Vereda.codigo_dane`): no se tocó el modelo/motor de importación sin más contexto del equipo, se revierte `subidaDisponible` a `false` en `Participacion.tsx`. Pendiente: decidir si `mom_dato` deja de incluir `sitio` como columna de creación (tratarlo solo como llave de referencia) y repetir la prueba. |
| 2026-11-24 | La usuaria corrige el criterio anterior explícitamente: "esta sección es para habilitar el botón de subir datos de MOM", no para documentar y dejar pendiente como COS. Se resuelven, en la misma sesión, los 4 bloqueos reales encontrados probando con los datos de IDEAM: (1) `Sitio.latitud` NOT NULL, sacando `Sitio` de `mom_dato`; (2) `tipo_id` NOT NULL, reduciendo `UnidadMuestreo` en `mom_dato` a solo `codigo_metadato` (mismo patrón que `biomasa_dato`); (3) `Vereda.codigo_dane` único sin valor, sacando `Vereda`/`Municipio`/`Departamento`/`Region` de `mom_metadato` (mismo fix que ya se había aplicado a `cos_metadato` el mismo día); (4) "Campo requerido vacío" bloqueando las 48 filas de "MOM Metadato" por `intervenido`/`sistema_referencia`/`tipo_unidad_muestreo` vacíos — para `sistema_referencia`, decisión explícita de la usuaria de poner por default EPSG_4326 (WGS84) con aviso no bloqueante en vez de bloquear la fila o sacar la columna; se implementó `_DEFAULTS_CAMPOS_CATALOGO_BRONCE` + `advertencia_relleno` en `backend/app/api/etl/views.py` (mecanismo genérico, reusa `estrategia_nulos='manual'` ya existente, sin tocar ningún modelo) y se aplicó el mismo criterio a `Sitio.intervenido`→"no"; `tipo_unidad_muestreo` se resolvió completando el dato (`MOM_plantilla.xlsx`, 16/48 filas sin valor) con "Parcela" (mismo valor que las otras 32). Carga real completa (`carga_id=381`, proyecto `TEST-bronce-temporal-borrar`) terminó con `{"ok": True, "filas_promovidas": 1224}`. `subidaDisponible: true` queda confirmado para MOM en `Participacion.tsx`; el comentario de la interfaz `Metodologia` se actualiza para reflejar que ahora solo COS sigue bloqueada. Pendiente de limpieza menor: las fuentes de prueba (ids 89/91/92/98/99) quedan en el proyecto `TEST-bronce-temporal-borrar`, que es justamente descartable. |
