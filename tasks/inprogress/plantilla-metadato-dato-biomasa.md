# Plantilla metadato/dato para Biomasa (producción de biomasa aérea)

**Estado:** en curso
**Creada:** 2026-11-19
**A cargo:** Vivi
**Sesión de Claude Code:** sesión actual (ver transcript local)

## Objetivo

Repetir para Biomasa el mismo ejercicio hecho para Flujos CO2/CH4: diseñar y
luego implementar (1) la plantilla descargable separada en hojas
Metadato/Dato con diccionario de datos, (2) el modal "Ver detalle de la
plantilla" desplegado en `/participacion`, y (3) el mapeo visual/automático
de columnas en el flujo de carga — los 3 entregables acordados con la
usuaria para este tipo de metodología.

## Contexto

Reutiliza el plan marco de
[[subida-descarga-formato-metadato-dato-por-metodologia]] (que ya listaba a
Biomasa como metodología pendiente de relevar) en vez de crear un proceso
nuevo desde cero — decisión explícita de la usuaria (2026-11-19): no separar
en una tarea-plan distinta, sino abrir una tarea de implementación puntual
para Biomasa que cuelga del mismo plan general, igual que se hizo con Flujos
(`reportar-plantilla-vacia-descarga`, el modal de detalle, y
`mapeo-automatico-plantilla-flujos-co2`).

Punto de partida: Excel real con datos de IDEAM (`context/data/Biomasa.xlsx`)
que la usuaria compartió, con hojas "Metadatos BM" (metadato) y "BD
Biomasa"/"BMORI sin Duplicados" (dato) — además trae una hoja "MOM ORI sin
duplicados" (metodología MOM, fuera de alcance de esta tarea) y una hoja
"Hoja1" con datos de Flujos de otra fuente IDEAM (tampoco es de esta tarea).

A diferencia de Flujos, **Biomasa hoy no tiene plantilla separada
Metadato/Dato** — usa la vista genérica compartida con MOM/COS
(`_CAMPOS_METODOLOGIA`, solo 4 columnas de contexto). El diccionario de
datos completo (análogo al de Flujos) queda documentado en
[docs/arquitectura/plantilla-metadato-dato-biomasa.md](../../docs/arquitectura/plantilla-metadato-dato-biomasa.md).

## Plan

- [x] Relevar el Excel real (`Biomasa.xlsx`) y cruzar cada columna contra el
      modelo de datos (`backend/app/models/biomasa.py`, más los modelos
      compartidos con Flujos: `Sitio`, `UnidadMuestreo`, `Cobertura`,
      `Disturbio`, `EcosistemaManual`) — documentado en
      [plantilla-metadato-dato-biomasa.md](../../docs/arquitectura/plantilla-metadato-dato-biomasa.md).
      De 45 columnas de Metadato, 38 ya tienen modelo; de 24 de Dato, las 24
      ya tienen modelo (el pendiente ahí es de arquitectura de vista, no de
      campos — ver siguiente punto).
- [x] Resolver las 4 preguntas abiertas del documento sin bloquear en el
      equipo (decisión: avanzar con el criterio más conservador y dejarlo
      documentado para revisar después — ver "Decisiones tomadas al
      implementar" en el diccionario de datos): `DOM_DIST_MGMT` y los 4
      pares `monitoreo_*`/`protocolo_*` quedan fuera de la plantilla (sin
      campo claro en el modelo); la hoja Dato queda a nivel parcela, sin
      `IndividuoArboreo`; se aplican a Biomasa las mismas exclusiones que a
      Flujos (fecha de instalación, periodicidad, nombre_proyecto).
- [x] Diseñar `_VISTAS_DESNORMALIZADAS["biomasa_metadato"]` y
      `["biomasa_dato"]` (vistas nuevas, no se tocó la vista genérica
      `"biomasa"` que ya usan `exportar_carga`/`datos_carga`), agregadas a
      `_HOJAS_PLANTILLA` en `backend/app/api/etl/views.py`. Se generalizó
      `_hojas_plantilla_vacia()` (antes hardcoded a la lógica de pivoteo de
      GEI) con `_PIVOTE_EXTRA_POR_VISTA`/`_ORDEN_EXTRA_POR_VISTA` para que
      cualquier vista nueva pueda reusar las columnas de pivoteo
      (cobertura/disturbio/ecosistema/exposición externa) sin duplicar
      código — Biomasa reutiliza `_COLUMNAS_PIVOTE_METADATO_GEI` tal cual
      (son genéricas a `UnidadMuestreo`, no específicas de GEI).
- [x] Entregable 1: plantilla descargable con hojas "Biomasa Metadato" (47
      columnas) / "Biomasa Dato" (8 columnas) + diccionario de datos
      (`plantilla_vacia`) — verificado generando el Excel real (5 hojas en
      total) y con `manage.py check`.
- [x] Entregable 2: el modal "Ver detalle de la plantilla"
      (`PlantillaDetalleModal.tsx` + endpoint `plantilla_detalle`) ya era
      genérico sobre las hojas que devuelve el backend — solo hubo que
      quitar el título hardcodeado "— Flujos CO2". Verificado vía el
      endpoint (47+8 atributos de Biomasa).
- [x] Entregable 3: mapeo automático de columnas en la carga —
      `_sugerir_mapeos_automaticos`/`_poblar_bronce` ya eran genéricos sobre
      `_HOJAS_PLANTILLA`, no hizo falta tocarlos. Se habilitó la casilla
      "Ya tiene el formato de la plantilla" para Biomasa en
      `FuenteDrawer.tsx` (`soportaMapeoAutomatico`). Verificado en vivo:
      Biomasa Dato mapea 8/8 automático; Biomasa Metadato 31/47 (16
      columnas de cobertura/disturbio/exposición externa quedan ambiguas,
      mismo límite ya conocido en Flujos — caen al asistente manual).
- [ ] Validar con Andrea/equipo de datos las decisiones tomadas sin
      preguntar (punto 1 de este plan) y, si corresponde, resolver
      `DOM_DIST_MGMT` y evaluar si biomasa subterránea/flora/rasgos
      funcionales necesitan metodología propia.
- [ ] Desplegar al contenedor compartido y probar con un archivo real de
      Biomasa (hoy solo se probó con encabezados generados por la propia
      plantilla, no con `context/data/Biomasa.xlsx` subido tal cual).

## Entregables

- [Diccionario de datos — Biomasa](../../docs/arquitectura/plantilla-metadato-dato-biomasa.md)
  (implementado; decisiones de diseño documentadas, pendiente de validar
  con el equipo).
- `backend/app/api/etl/views.py`: `_VISTAS_DESNORMALIZADAS["biomasa_metadato"/"biomasa_dato"]`,
  `_HOJAS_PLANTILLA`, `_ORDEN_COLUMNAS_METADATO_BIOMASA_PLANTILLA`,
  `_ORDEN_COLUMNAS_DATO_BIOMASA_PLANTILLA`, `_PIVOTE_EXTRA_POR_VISTA`, `_ORDEN_EXTRA_POR_VISTA`.
- `frontend/src/pages/Participacion.tsx` (`plantillaDisponible: true` para Biomasa),
  `frontend/src/components/admin/fuentes/FuenteDrawer.tsx` (`soportaMapeoAutomatico`),
  `frontend/src/components/common/PlantillaDetalleModal.tsx` (título genérico),
  `frontend/src/pages/EtlUpload.tsx` (mensaje de error genérico).

## Referencias

- [[subida-descarga-formato-metadato-dato-por-metodologia]] — plan marco del que cuelga esta tarea.
- [plantilla-metadato-dato-co2-camaras.md](../../docs/arquitectura/plantilla-metadato-dato-co2-camaras.md) — mismo ejercicio para Flujos, modelo a seguir.
- [[mapeo-automatico-plantilla-flujos-co2]] — referencia para el entregable 3.
- `backend/app/models/biomasa.py`, `backend/app/models/sitio.py` (`Parcela`).
- `backend/app/api/etl/views.py` — `_VISTAS_DESNORMALIZADAS["biomasa"]` (genérica, no tocada), `["biomasa_metadato"]`, `["biomasa_dato"]`.
- `context/data/Biomasa.xlsx` — Excel fuente (IDEAM) usado para el relevamiento.

## Historial

| Fecha | Descripción |
|---|---|
| 2026-11-19 | Se crea la tarea: la usuaria confirma reutilizar el plan marco de Flujos ([[subida-descarga-formato-metadato-dato-por-metodologia]]) en vez de un proceso nuevo. Se releva el Excel real (`Biomasa.xlsx`) y se documenta el diccionario de datos propuesto para Biomasa, cruzando cada columna contra el modelo. |
| 2026-11-19 | Se implementan los 3 entregables sin esperar validación del equipo (instrucción explícita de la usuaria): vistas `biomasa_metadato`/`biomasa_dato` nuevas en `_VISTAS_DESNORMALIZADAS`, generalización de `_hojas_plantilla_vacia()` para reusar el mecanismo de pivoteo de columnas (cobertura/disturbio/ecosistema/exposición externa) fuera de GEI, y habilitación de los botones/casillas correspondientes en frontend. Verificado en vivo contra el contenedor compartido: Excel real de 5 hojas, modal de detalle con 47+8 atributos de Biomasa, mapeo automático 8/8 en Dato y 31/47 en Metadato (mismo límite de columnas ambiguas que Flujos). `manage.py check`, `npx tsc --noEmit` y `npx eslint` limpios. Quedan pendientes: validar con Andrea/equipo las decisiones tomadas sin preguntar (`DOM_DIST_MGMT`, monitoreo_*/protocolo_*, nivel parcela sin individuo, exclusiones heredadas de Flujos) y probar con el archivo real `Biomasa.xlsx` subido tal cual (hoy solo se probó con encabezados generados por la propia plantilla). |
| 2026-11-19 | A partir de una captura del modal "Ver detalle de la plantilla", se detecta que 5 de las 8 columnas de "Biomasa Dato" (`prod_biomasa_g`, `contenido_carbono`, `sd_tonc_ha`, `min_tonc_ha`, `max_tonc_ha`) no tenían `help_text` en `MuestraBiomasa`, por lo que esas filas salían sin descripción en el modal. Se agregó `help_text` corto a los 5 campos y se aplicó la migración `0131_alter_muestrabiomasa_contenido_carbono_and_more`. Verificado en vivo: las 8 columnas de "Biomasa Dato" ya traen descripción. |
| 2026-11-19 | Pedido explícito de la usuaria: separar la descarga/detalle de plantilla por metodología (antes "Descargar plantilla"/"Ver detalle" en cualquier tarjeta traían Flujos+Biomasa+COS juntos). Se agregó `metodologia` a cada `hoja_def` de `_HOJAS_PLANTILLA` y un filtro opcional `?metodologia=<key>` en `plantilla_vacia`/`plantilla_detalle` (`_hojas_plantilla_vacia(metodologia=...)`); el mapeo automático de carga sigue sin filtro (necesita reconocer cualquier metodología). Frontend: `Participacion.tsx` pasa `m.key` a la descarga y al modal (con `key={m.key}` para forzar refetch al cambiar de tarjeta), `PlantillaDetalleModal.tsx` acepta `metodologia`/`titulo`. Verificado en vivo (`RequestFactory`): `?metodologia=biomasa` trae solo 2 hojas + diccionario de 8 filas, sin filtro trae las 8 hojas de todas las metodologías. `manage.py check`, `tsc`, `eslint` limpios. |
| 2026-11-20 | La usuaria reporta "sigue sin funcionar al ver detalle de plantilla": en el navegador (`localhost:3000/reportar`, la ruta real no es `/participacion`), el modal de Biomasa seguía trayendo las 4 hojas (Flujos+Biomasa) pese al fix del día anterior. Causa: el contenedor compartido corre `gunicorn --workers 4` sin `--reload` — los workers tenían el código viejo cargado en memoria desde antes del cambio; las verificaciones anteriores con `manage.py shell`/`RequestFactory` daban falso positivo porque reimportan el módulo en cada corrida. `curl` directo a `localhost:8001` confirmó el síntoma (devolvía las 4 hojas pese al query param). Se resolvió con `docker compose restart web`; confirmado con `curl` y en el navegador (Biomasa ya muestra solo "Biomasa Metadato"/"Biomasa Dato"). Documentado el gotcha en el diccionario de datos para no repetir el susto: a futuro, verificar cambios de `views.py` con una petición HTTP real, no solo `manage.py shell`. |
| 2026-11-20 | Pedido explícito de la usuaria: deshabilitar por ahora el botón "Subir datos" en la tarjeta de Biomasa (`Participacion.tsx`, nuevo flag `subidaDisponible: false`) — la plantilla descargable/modal de detalle/mapeo automático quedan activos, pero la carga real no. "Descargar plantilla"/"Ver detalle" siguen sin cambios. |
