# Rediseñar el proceso de carga de Flujos CO2: capa staging/bronce + vista tipo Excel con validación inline

**Estado:** en curso — backend y frontend implementados y probados en vivo (navegador), incluido el selector de columnas ambiguas con un bug real de validación encontrado y corregido; falta el flujo de campos obligatorios restantes (nombre/tipo/unidad_experimental) para que una hoja de Metadato promueva de punta a punta
**Creada:** 2026-11-16
**A cargo:** Viviana
**Sesión de Claude Code:** (completar con el link de esta sesión)

## Objetivo

Rediseñar el paso final de carga de Flujos CO2 (hoy el asistente manual de
mapeo atributo por atributo, `EtlUpload.tsx` paso 4) para que, cuando el
archivo ya trae la plantilla, los datos se carguen **completos tal cual
vienen** (sin bloquear por errores de validación) a una capa intermedia
("bronce"/staging), y la validación/estructuración hacia el modelo
relacional actual sea un paso posterior y visible, no una condición previa
a guardar.

## Contexto

Surgió al revisar `tasks/inprogress/mapeo-automatico-plantilla-flujos-co2.md`
(mapeo automático cuando el archivo ya calza con la plantilla). Esa tarea
mantiene el patrón actual: `validar_carga`/`previsualizar_carga` corre
**antes** de insertar en el modelo estructurado — si una fila tiene un
error, no se guarda. Eso bloquea poder "ver todo lo que traía el archivo,
bueno y malo, y corregir después" (lo que se busca acá).

### Flujo deseado (visto en capturas del asistente actual, pasos 1-3 sin cambios)

1. **Nueva fuente de datos**: se sube/referencia el archivo (confirmar si
   hoy queda guardado en S3 u otro storage — pendiente de verificar).
2. **Analizar fuente** (ya existe).
3. **Análisis EDA** (ya existe) → **Qué encontramos** (ya existe).
4. **Nuevo paso 4**, en reemplazo del asistente de mapeo manual cuando el
   archivo ya trae la plantilla: vista tipo "Excel" con pestañas
   Metadato/Dato (igual que las hojas de la plantilla), filtros por
   columna, y badges de validación inline por columna (ejemplo visto:
   `hora_toma` con "⚠ Validación 22" — 22 filas con problema en esa
   columna, sin que eso impida ver/cargar el resto).

### Propuesta de arquitectura (a validar punto por punto)

- Capa bronce/staging: dos entidades (Metadato, Dato) que guardan las
  columnas del archivo tal cual, literal, sin tipar ni resolver relaciones
  (equivalente 1:1 a las hojas de la plantilla).
- Un proceso de validación posterior promueve de bronce al modelo
  estructurado actual (`UnidadExperimental`, `UnidadMuestreo`, `SubmuestraGEI`,
  etc. — ver `docs/arquitectura/modelo-datos.md`), dejando marcadas (no
  bloqueadas) las filas que no pasan validación para corregirlas in situ.

## Plan

Puntos a resolver, uno por uno, antes de pasar a implementación:

- [x] Confirmar qué pasa hoy con el archivo subido en el drawer "Nueva
      fuente de datos" (¿se guarda en S3? ¿dónde queda la ruta/referencia?
      — verificar contra `backend/app/api/etl/views.py` y el modelo
      `FuenteDatos`/`CargaArchivo`). **Resuelto:** no hay S3. Se guarda en
      el filesystem local del contenedor, bajo `MEDIA_ROOT`
      (`colflux/settings.py`): archivo subido directo →
      `media/fuentes_datos/fuente_<id>.<ext>` (`_guardar_archivo_subido`,
      `backend/app/api/etl/views.py:415`), con la ruta relativa guardada en
      `FuenteDatos.url`; archivo por URL remota → cacheado en
      `media/fuentes_datos_cache/fuente_<id>.<ext>`
      (`_descargar_archivo_remoto`, línea 388). Sin `STORAGES`/`AWS_*` en
      settings — `FileSystemStorage` implícito de Django. Importa para el
      diseño: si algún día se migra a S3, cambia dónde vive el archivo
      fuente que alimentaría la capa bronce.
- [x] Diseñar el modelo de datos de la capa bronce (Metadato/Dato): ¿tablas
      nuevas por metodología, columnas dinámicas/JSON, o algo más genérico?
      Debe poder recibir cualquier valor (incluido inválido) sin romper.
      **Resuelto — diseño propuesto:**

      Se descarta una tabla de columnas fijas (`MetadatoBronceGEI(col1,
      col2, ...)` 1:1 con la plantilla): el historial de
      `docs/arquitectura/plantilla-metadato-dato-co2-camaras.md` muestra
      más de 10 cambios de columnas en 9 días (altas, bajas, renombres,
      reordenamientos) — una tabla de columnas fijas obligaría a migrar la
      capa bronce cada vez que cambia la plantilla, además del resto del
      código. Tampoco hay hoy ninguna capa persistente de filas crudas:
      `CargaArchivo.columnas_raw`/`hojas` (`backend/app/models/datos.py`)
      guardan solo el *snapshot de encabezados* (nombre de columna, total
      de filas), no los valores; los valores de cada fila solo viven en
      `cache.set(f"etl_carga_df_{carga_id}_{hoja}", df, timeout=None)`
      (`backend/app/api/etl/views.py:374`) — y sin `CACHES` configurado en
      `settings.py`, eso es `LocMemCache`: memoria de un solo proceso, no
      compartido entre workers, se pierde al reiniciar. Es un gap incluso
      para el flujo actual, no solo para este diseño.

      **Decisión del usuario:** no usar JSON para los valores — dificulta
      consultas directas (SQL/admin/BI: sin índice simple por columna, sin
      `WHERE columna = x` nativo). Se descarta también columnas fijas por
      hoja (migración en cada cambio de plantilla, ver arriba). Se elige
      un esquema **EAV** (una fila por **celda**, no por fila del Excel):
      consultable con `WHERE` normal e indexable por columna, sin requerir
      migración cuando la plantilla cambia (una columna nueva es,
      simplemente, más filas con ese valor de `columna`, no una migración
      de esquema).

      ```python
      class FilaBronce(TimestampedModel):
          carga = models.ForeignKey(CargaArchivo, on_delete=models.CASCADE, related_name="filas_bronce")
          hoja = models.CharField(max_length=255)       # "Flujos CO2 - Metadato" / "Flujos CO2 - Dato"
          fila_idx = models.IntegerField()               # posición original en el archivo, para orden/trazabilidad
          estado = models.CharField(max_length=20, choices=[
              ("pendiente", "Pendiente de validar"),
              ("valido", "Válido — listo para promover"),
              ("invalido", "Con errores — necesita corrección"),
              ("promovido", "Promovido al modelo estructurado"),
          ], default="pendiente")
          promovido_a = models.JSONField(null=True, blank=True)  # {"SubmuestraGEI": 123, "UnidadMuestreo": 45} — pk creados/reusados al promover esta fila; bookkeeping de resultado, no dato de la fuente, no necesita ser consultable por columna

          class Meta:
              ordering = ["hoja", "fila_idx"]
              unique_together = [("carga", "hoja", "fila_idx")]


      class CeldaBronce(TimestampedModel):
          fila = models.ForeignKey(FilaBronce, on_delete=models.CASCADE, related_name="celdas")
          columna = models.CharField(max_length=255, db_index=True)  # encabezado literal del archivo, ej. "hora_toma"
          valor = models.TextField(blank=True, null=True)            # literal, sin tipar — puede ser "25:70"
          error = models.TextField(blank=True, null=True)            # mensaje de validación de ESTA celda, si lo tiene

          class Meta:
              ordering = ["fila", "columna"]
              unique_together = [("fila", "columna")]
      ```

      Por qué este diseño:
      - **Una fila por celda, no por fila de Excel:** permite `CeldaBronce.objects.filter(columna="hora_toma", error__isnull=False)`
        directo, sin tocar JSON — exactamente lo que necesita el badge
        "⚠ Validación 22" de la vista tipo Excel (conteo de celdas con
        error por columna) y cualquier auditoría/consulta posterior.
      - **Sin migración cuando cambia la plantilla:** una columna
        nueva/renombrada es solo un valor distinto de `columna` en filas
        nuevas de `CeldaBronce`, no un `ALTER TABLE`. Sigue sirviendo para
        cualquier metodología futura (MOM/COS/Biomasa/CH4) sin tocar el
        esquema.
      - **Error por celda, no por fila:** más preciso que un solo blob de
        errores por fila — permite saber exactamente qué celda falló sin
        parsear nada.
      - **Costo asumido:** reconstruir una fila completa del Excel (para
        mostrarla en la vista o promoverla) requiere agrupar varias filas
        de `CeldaBronce` por `fila_id` — un `prefetch_related`/`GROUP BY`
        en vez de leer un solo registro. Y hay bastantes más filas en la
        tabla (45 columnas × N filas de Metadato, 19 × N de Dato) que con
        una fila por fila de Excel. Se acepta ese costo a cambio de poder
        consultar como SQL normal.
      - **`promovido_a` se mantiene JSON:** es resultado/bookkeeping (qué
        PKs se crearon), no dato de la fuente — no hay necesidad de
        consultarlo por columna, mismo patrón que
        `CargaArchivo.pks_importados` ya existente.

      Sigue pendiente (puntos siguientes del plan): el proceso que llena
      `FilaBronce`/`CeldaBronce` al momento de la carga, el proceso de
      validación/promoción que las lee, y cómo la vista "tipo Excel" las
      consume con filtros/paginación sin traer todas las celdas de una
      carga grande en una sola respuesta.
- [x] Definir el proceso de validación/promoción bronce → modelo
      estructurado: cuándo corre (¿automático al cargar, o manual con
      botón "Validar"?), qué marca exactamente como inválido, y qué pasa
      con una fila que nunca se corrige. **Resuelto — proceso propuesto:**

      Se confirmó en `_ejecutar_importacion_async`
      (`backend/app/api/etl/views.py:3169-3185`) el bloqueo exacto que
      motivó esta tarea: `_leer_y_validar_multihoja` valida **toda la
      sección completa** (todas las hojas/filas involucradas) y si
      `total_errores > 0`, la importación corta ahí — no escribe
      absolutamente nada, ni siquiera las filas que sí estaban limpias.
      Es all-or-nothing a nivel de sección, no de fila.

      La buena noticia: `_leer_y_validar_multihoja`/`_validar_seccion` ya
      devuelven el detalle que se necesita — cada resultado de columna
      trae `errores: [{"fila": i, "mensaje": "..."}]` por fila. No hace
      falta rediseñar la validación en sí, solo qué se hace con su
      resultado:

      1. **Al terminar la carga a bronce** (justo después de poblar
         `FilaBronce`/`CeldaBronce` desde el archivo, sin esperar acción
         manual): correr `_leer_y_validar_multihoja` (o su equivalente)
         sobre **todas** las filas de la carga, igual que hoy. En vez de
         cortar si `total_errores > 0`, escribir cada error directo en su
         `CeldaBronce` correspondiente (`fila_idx` + `columna` del error
         ya identifican la celda exacta) — no hace falta un paso de
         "invertir por columna a por fila", el error queda en la celda
         que lo originó.
      2. **Promoción selectiva:** `FilaBronce.objects.filter(celdas__error__isnull=False)`
         distingue directo las filas con algún error (consulta normal,
         sin parsear JSON). De las filas sin ningún error, correr
         `_procesar_filas_multihoja` (la escritura real a BD, ya existente)
         **solo con ese subconjunto** — incluye la resolución de FKs
         (crear/reusar `UnidadExperimental`/`UnidadMuestreo`/etc.) que ya
         hace hoy. Cada fila promovida pasa a `estado="promovido"` con su
         `promovido_a` (pks creados/reusados); las que tenían error quedan
         en `estado="invalido"`, con el detalle ya en sus `CeldaBronce`,
         sin tocar la BD estructurada para ellas.
      3. **Disparo:** automático al terminar de poblar bronce (no un botón
         "Validar" aparte) — así la vista tipo Excel aparece ya con los
         badges de validación calculados, sin un paso intermedio en
         blanco. Reusa el mismo mecanismo de polling en background que ya
         existe (`CargaArchivo.progreso_*` + `estado_importacion`), solo
         que ahora corre sobre bronce en vez de sobre el archivo crudo.
      4. **Corrección de una fila:** al editar un valor en la vista tipo
         Excel (`CeldaBronce.valor`, limpiando su `error` previo), se
         re-corre la validación acotada a esa hoja (mismo mecanismo del punto 1, sobre el subconjunto
         `pendiente`/`invalido` de esa hoja — a los volúmenes actuales,
         revalidar la hoja completa en vez de solo la fila es aceptable y
         evita construir un camino de validación "de una fila sola"
         aparte del que ya existe). Si queda sin errores, se promueve en
         el mismo paso.
      5. **Fila que nunca se corrige:** queda indefinidamente en
         `estado="invalido"`, visible en la vista con su error, sin
         bloquear ni retrasar la promoción de las demás filas de la misma
         carga. La carga queda "parcialmente completa" en vez de
         "bloqueada" — ese es justamente el cambio de comportamiento que
         se buscaba. Esas filas no aparecen en el modelo estructurado
         (`/etl/datos`, exportaciones) hasta que se promuevan.
      6. **Reemplaza, no convive, con el `total_errores > 0` → corte
         total de `_ejecutar_importacion_async`** para el flujo nuevo —
         ver punto de "relación con `mapeo-automatico-plantilla-flujos-co2.md`"
         más abajo para decidir si el flujo viejo (asistente manual) se
         toca o sigue como está para los casos que no usan plantilla.
- [x] Diseñar la vista "tipo Excel" del nuevo paso 4: pestañas
      Metadato/Dato, filtros por columna (ya existe un patrón similar en
      `EtlDatos.tsx`/`DatosTable.tsx`, reusable), badge de validación por
      columna con el conteo de filas con problema y acceso a corregirlas.
      **Resuelto — diseño propuesto:**

      Se reusa casi literal el patrón de `DatosTable.tsx`
      (`frontend/src/components/etl-datos/DatosTable.tsx`): encabezado
      agrupado por modelo con color (`colorDeModelo`), fila de nombre de
      columna, fila de badge "🛡️ Validación N" (ya existe tal cual en
      `DatosTable.tsx:80-98` para reglas de autollenado — mismo
      componente visual, ahora alimentado por el conteo de `CeldaBronce`
      con error en vez de `ReglaAutollenado.pendientes`), fila de filtro
      por columna (`DatosTableFilterInput`, reusado sin cambios), y filas
      de datos. La diferencia real es la fuente de datos y que las celdas
      son editables.

      - **Pestañas:** una por cada `hoja` presente en `carga.hojas`
        (p. ej. "Flujos CO2 - Metadato"/"Flujos CO2 - Dato"), mismo patrón
        que el selector de hoja que ya existe en el paso 4 actual del
        asistente (`EtlUpload.tsx`).
      - **Endpoint nuevo** `GET /api/fuentes-datos/<f>/carga/<c>/bronce/?hoja=&<filtros-por-columna>&offset=&limit=`:
        pagina por `FilaBronce` (no trae todas las celdas de la carga de
        una vez), devuelve por fila sus `celdas` (columna → valor/error) y
        un resumen por columna (`errores_count`, y si la columna ya tiene
        mapeo resuelto — ver abajo). Filtrar por valor de una columna es
        un `CeldaBronce.objects.filter(columna=X, valor__icontains=Y)`
        normal gracias al esquema EAV, sin tocar JSON.
      - **Edición de celda:** `PATCH /api/fuentes-datos/<f>/carga/<c>/bronce/celda/`
        con `{fila_idx, hoja, columna, valor}` — actualiza `CeldaBronce.valor`,
        limpia su `error`, re-corre la validación de esa hoja (punto 3) y
        devuelve la fila actualizada (si quedó limpia, ya viene
        `estado="promovido"` en la respuesta).
      - **Celda con error:** se resalta (borde/fondo rojo, mismo lenguaje
        visual que ya usan los paneles de validación del asistente
        actual) con tooltip del mensaje — editable inline, sin modal
        aparte (a diferencia de `ReviewModal` del asistente manual, que sí
        necesita modal porque resuelve varias cosas a la vez: acá cada
        celda es una corrección puntual).
- [x] Decidir qué pasa con las 16 columnas ambiguas de Metadato (ver
      `mapeo-automatico-plantilla-flujos-co2.md`) y con archivos que no
      calzan exacto con la plantilla, dentro de este nuevo flujo.
      **Resuelto:**

      Simplificación importante que surge del propio diseño EAV: la capa
      bronce **nunca necesita saber a qué `modelo.campo` corresponde una
      columna para guardarla** — guarda el encabezado literal tal cual
      viene en el archivo, matchee o no con la plantilla. Eso significa
      que "archivo que no calza exacto" deja de ser un caso especial: todo
      archivo se carga a bronce igual, sin importar si sus columnas
      coinciden con `_hojas_plantilla_vacia()`.

      El mapeo (`_sugerir_mapeos_automaticos`, confirmado en
      `backend/app/api/etl/views.py:4376` que compara **columna por
      columna**, no archivo completo) solo importa en el momento de la
      **promoción** (punto 3), y puede ser parcial dentro de una misma
      hoja: las columnas que matchean exacto se auto-promueven; las 16
      ambiguas (`cobertura_IPCC`/`tipo_disturbio`/etc., que comparten
      `modelo.campo` y necesitan `tipo_cobertura` para desambiguar) y las
      columnas que no matchean ningún nombre de la plantilla quedan
      "sin mapear" **a nivel de columna, no de hoja ni de archivo** — se
      muestran igual en la vista tipo Excel con sus valores, pero con un
      selector inline junto al encabezado ("¿a qué campo corresponde esta
      columna?", reutilizando el combo modelo/campo/tipo_cobertura de
      `MapeoRow.tsx` del asistente actual) en vez de bloquear la hoja
      entera como hace hoy el "todo o nada por hoja" de
      `mapeo-automatico-plantilla-flujos-co2.md`. Una vez resuelto ese
      mapeo de columna, sus celdas entran al mismo ciclo de
      validación/promoción que las demás.
- [x] Definir la relación con `mapeo-automatico-plantilla-flujos-co2.md`:
      ¿este diseño la reemplaza (el paso 4 que esa tarea deja pendiente de
      implementar), la extiende, o conviven como dos casos distintos?
      **Resuelto:** este diseño **reemplaza** el paso 4 que esa tarea
      dejaba pendiente de implementar (la vista con banner
      aplicando/parcial/error) — no hace falta la casilla "Ya tiene el
      formato de la plantilla" como bifurcación previa, porque con bronce
      **todo archivo sigue el mismo camino** (cargar completo → mapear
      columna por columna, automático donde matchea → promover lo que
      queda limpio). Se mantiene de esa tarea: el backend de sugerencia
      por columna (`_sugerir_mapeos_automaticos`) y el endpoint
      `mapeo-automatico`, que se reusan tal cual para la promoción
      automática. Se dejan sin usar: la casilla del drawer y el flujo
      `?auto=1` de `EtlUpload.tsx` (innecesarios si este diseño se
      implementa) — no se tocan todavía, se marcan para retirar cuando
      se implemente este diseño, no antes.
- [x] Alcance: ¿aplica solo a Flujos CO2 (como la tarea de mapeo
      automático) o se piensa desde el inicio para las demás metodologías
      (COS/Biomasa/MOM/CH4/torre EC)?
      **Resuelto:** el modelo de datos (`FilaBronce`/`CeldaBronce`) ya
      queda genérico sin costo extra — no depende de columnas fijas por
      metodología, así que no hay razón de diseño para acotarlo. Lo que
      sí está acotado hoy a Flujos CO2 es el motor que lo rodea:
      `_HOJAS_PLANTILLA`/`_sugerir_mapeos_automaticos`/
      `_leer_y_validar_multihoja` (vía `SECCIONES_ETL`) solo conocen Flujos
      CO2/CH4 con hojas Metadato/Dato separadas (ver
      `subida-descarga-formato-metadato-dato-por-metodologia.md`, pendiente
      para COS/Biomasa/MOM). **Decisión:** implementar primero acotado a
      Flujos CO2 (mismo alcance que la tarea que reemplaza), y extender a
      las demás metodologías cuando esa tarea de backlog se resuelva — sin
      rediseñar bronce en ese momento, solo sumar sus hojas a
      `_HOJAS_PLANTILLA`.

## Entregables

**Backend implementado y probado end-to-end** (sesión 2026-11-16, segunda
mitad):

- `backend/app/models/datos.py`: `FilaBronce`, `CeldaBronce` (con
  `CeldaBronce.editado`, agregado durante la implementación — ver abajo).
  Migraciones `0127_agregar_fila_bronce_celda_bronce` y
  `0128_agregar_editado_celda_bronce`, **aplicadas** contra la RDS
  compartida (aditivas: 2 tablas nuevas + 1 columna nueva, nada existente
  tocado).
- `backend/app/api/etl/views.py` — funciones nuevas (sección "Capa
  bronce/staging", antes de `plantilla_vacia`):
  - `_poblar_bronce(carga)` — vuelca cada hoja a FilaBronce/CeldaBronce,
    idempotente.
  - `_sugerir_mapeos_columnas_bronce(carga)` / `_crear_mapeos_automaticos_bronce(carga)`
    — como `_sugerir_mapeos_automaticos` pero sin todo-o-nada por hoja: crea
    `MapeoColumna` solo para las columnas que matchean 1:1, deja aparte
    `columnas_sin_match`/`columnas_ambiguas` (punto 5 del diseño). No
    reemplaza `_sugerir_mapeos_automaticos`/`mapeo_automatico` — esa función
    sigue intacta para el flujo viejo.
  - `_aplicar_ediciones_bronce`, `_escribir_errores_en_celdas`,
    `_actualizar_estados_filas_bronce`, `_promover_filas_bronce`,
    `_validar_y_promover_bronce(carga)` — reusan `_validar_seccion`/
    `_procesar_filas_multihoja` tal cual (sin reescribir su lógica),
    escriben cada error en su `CeldaBronce` en vez de cortar la sección
    completa, y promueven selectivamente solo las filas sin ningún error.
    Una hoja con un error "de sección" (campo obligatorio sin mapear, ej.
    'tipo'/'unidad_experimental' de UnidadMuestreo cuando vienen de una
    columna ambigua sin resolver) queda "bloqueada" — ninguna de sus filas
    se promueve hasta que se resuelva ese mapeo, pero no afecta a otras
    hojas de la misma carga.
  - `_ejecutar_bronce_async(carga_id)` — corre el pipeline completo en
    background, reusando `CargaArchivo.progreso_*` (mismo mecanismo de
    polling que la importación clásica, endpoint `estado_importacion`
    reusado sin cambios).
- Endpoints nuevos (`backend/app/api/urls.py`):
  - `POST /api/fuentes-datos/<f>/carga/<c>/bronce/procesar/` — dispara el
    pipeline en background. **Decisión de implementación:** no se dispara
    automáticamente desde `upload_archivo` (como proponía el diseño
    original) para no alterar el comportamiento del asistente manual
    existente antes de que la vista tipo Excel esté lista — lo dispara el
    frontend nuevo cuando el usuario entra al paso 4 rediseñado. Pendiente
    evaluar si conviene automatizarlo una vez que esa vista exista.
  - `GET /api/fuentes-datos/<f>/carga/<c>/bronce/?hoja=&<filtros>&offset=&limit=`
    — paginado por `FilaBronce`, filtros por columna vía `CeldaBronce`.
  - `PATCH /api/fuentes-datos/<f>/carga/<c>/bronce/celda/` — corrige una
    celda, re-valida/promueve toda la carga.
- **Probado end-to-end** contra una fuente/proyecto temporales (copia del
  archivo real de la fuente 63, "IDEAM CO2 - plantilla.xlsx"): pobló 3467
  filas / 70319 celdas en las 2 hojas, mapeó automático 48 columnas,
  corrió validación (4923 celdas con error), bloqueó correctamente ambas
  hojas por campos obligatorios sin mapear ('tipo'/'unidad_experimental'
  de UnidadMuestreo, 'unidad_muestreo' de Clima — vienen de columnas
  ambiguas o no incluidas en el auto-mapeo), **0 filas promovidas** (nada
  escrito en el modelo estructurado, como se esperaba sin el selector
  manual de columnas ambiguas todavía). Proyecto/fuente/carga/filas/celdas
  de prueba borrados al terminar — la RDS compartida quedó sin rastro de la
  prueba, solo con las tablas nuevas (vacías).
- `python manage.py check` y `makemigrations --check` limpios.

**Frontend implementado** (misma sesión, después del backend):

- `frontend/src/components/etl-datos/BronceTable.tsx` — vista tipo Excel
  (variante editable de `DatosTable.tsx`: mismo encabezado agrupado por
  modelo/color, badge "⚠ Validación N" por columna, fila de filtro
  reusando `DatosTableFilterInput`), con celdas clicables para editar
  inline (`input` que commitea con Enter/blur) y resaltado ámbar en celdas
  con error (tooltip = mensaje).
- `frontend/src/pages/EtlUploadBronce.tsx` — página independiente (mismo
  patrón que `EtlUploadTorre.tsx`, no un branch más dentro de
  `EtlUpload.tsx`), ruta `/etl/upload-bronce?fuente=&carga=`: dispara
  `procesarBronce`, hace polling con `estadoImportacion` (reusado tal
  cual), pestañas por hoja (nombres obtenidos de `getMapeoAutomatico`,
  endpoint viejo reusado sin cambios), paginación, filtros por columna y
  edición de celda vía `editarCeldaBronce`.
- `frontend/src/components/etl-upload/ResumenAnalisis.tsx` (paso 3 del
  wizard viejo) — único cambio al flujo existente: un aviso + link
  "Usar vista tipo Excel (beta) →" hacia `/etl/upload-bronce`, visible
  solo cuando las hojas del archivo coinciden exacto con
  `['Flujos CO2 - Metadato', 'Flujos CO2 - Dato']`. El asistente manual de
  abajo sigue intacto y disponible siempre — la vista nueva es opt-in, no
  reemplaza nada todavía.
- `frontend/src/components/etl-datos/MapeoColumnaBronceSelector.tsx` —
  selector inline modelo/campo/clasificación para columnas ambiguas/sin
  match, integrado en `BronceTable.tsx` (fila nueva bajo el badge de
  validación) y en `EtlUploadBronce.tsx` (persiste el mapeo vía `postMapeo`
  reusado y re-dispara el pipeline bronce). Soporta también mapeo de
  valores (`mapeo_valores`) para campos FK/choice que SÍ lo necesiten,
  vía el endpoint nuevo `GET .../bronce/valores-columna/`
  (`valores_columna_bronce` en el backend) — no resultó necesario para
  `CoberturaManual.valor` una vez corregido el bug de validación (ver
  Historial), pero queda disponible para otros campos.
- `backend/app/api/etl/views.py`: fix en `_validar_columna` —
  `CoberturaManual.valor` se trata como texto libre (no como FK con
  choices = pks), igual que `campos_destino` ya lo describe al frontend.
  Bug preexistente (afectaba también al asistente manual), encontrado al
  probar en vivo el mapeo de columnas de cobertura.
- `frontend/src/services/etl.service.ts` / `frontend/src/types/index.ts`:
  `procesarBronce`, `listarBronce`, `editarCeldaBronce` +
  `ListarBronceResponse`/`EditarCeldaBronceResponse`/`FilaBronceDatos`/etc.
- `npx tsc --noEmit`, `npx eslint` y `npx vite build` limpios.

**Selector inline de mapeo implementado** (`MapeoColumnaBronceSelector.tsx`)
y **probado en vivo desde el navegador** (no solo en shell):

- Se creó una fuente/carga de prueba real (proyecto temporal, copia del
  archivo de fuente 63) y se navegó `/etl/upload-bronce` con Claude in
  Chrome, autenticando vía token inyectado en `localStorage` (cuenta de
  prueba creada y borrada al final, nunca una cuenta real).
- **Bug encontrado y corregido durante la prueba:** el servidor Django
  (`backend-web-1`, gunicorn) no recarga código en caliente — los
  endpoints nuevos devolvían 404 por HTTP real aunque funcionaban en
  `manage.py shell` (que sí carga el módulo fresco). Hubo que reiniciar el
  contenedor (`docker restart backend-web-1`) para que gunicorn cargara
  `urls.py`/`views.py` actualizados. **Importante para el despliegue real
  en el contenedor compartido:** un `docker compose cp` sin reiniciar el
  proceso de gunicorn no alcanza.
- Confirmado en vivo: pestañas por hoja, colores/agrupación por modelo,
  badge "⚠ Validación N", columnas ambiguas agrupadas bajo "SIN MAPEAR"
  con el selector modelo/campo/clasificación, botón "Mapear" que persiste
  el `MapeoColumna` (vía `postMapeo` reusado) y dispara una revalidación
  completa.
- **Bug real encontrado, diagnosticado y corregido en esta sesión**
  (afecta también al asistente manual, no solo a bronce): mapear
  `cobertura_CLC` → `CoberturaManual.valor` con el selector dejó
  **todas** las 171 filas de Metadato con error
  ("Valor no permitido. Opciones: ['1', '10', ..., '9']"). Diagnóstico:
  `CoberturaManual.valor` es una FK real a `ValorClasificacionTipo`, pero
  el archivo trae el texto literal reportado ("4.1.2. Turberas"), no el
  pk — `_procesar_fila_cobertura` ya resuelve/crea el
  `ValorClasificacionTipo` a partir de ese texto al momento de **escribir**
  (y `campos_destino` ya lo describe al frontend como `es_fk: False`,
  texto libre), pero `_validar_columna` (la validación) no tenía ese mismo
  trato especial: trataba el campo como una FK normal y comparaba el texto
  contra los pks como "choices", así que **nunca** podía pasar — ni en
  bronce ni en el asistente manual viejo (este bug es anterior a esta
  sesión, solo que nunca se había probado en vivo un archivo con columnas
  de cobertura mapeadas hasta ahora).
  **Corrección:** `_validar_columna` (`backend/app/api/etl/views.py`)
  ahora trata `CoberturaManual.valor` como texto libre (sin choices,
  `max_length=160`), igual que ya hace `campos_destino` — mismo criterio,
  un solo lugar más para mantener sincronizado si cambia. Confirmado en
  vivo: con el fix, `cobertura_CLC` mapea y queda **sin ningún error**
  (antes: 171/171 filas con error).
- Con este fix, la primicia de `MapeoColumnaBronceSelector` (solo
  `transformacion: "directo"`, sin `mapeo_valores`) alcanza para las
  columnas de clasificación — no hacía falta agregar soporte de `lookup`
  después de todo, el problema real era la validación, no el selector.
  (Se agregó igual soporte opcional de `mapeo_valores`/valores únicos por
  si algún campo FUTURO sí lo necesita — `valores_columna_bronce` endpoint
  nuevo — pero no resultó necesario para este caso.)

**Drawer "Nueva fuente de datos" ya no pasa por el asistente manual ni por
una pantalla intermedia** (misma sesión, después del fix de
`CoberturaManual.valor`):

- `frontend/src/components/admin/fuentes/FuenteDrawer.tsx`: al tildar "Ya
  tiene el formato de la plantilla" y dar "Guardar fuente", el drawer ya no
  navega a `/etl/upload?...&auto=1` (asistente manual clásico, todo-o-nada
  por hoja). En vez de eso se queda abierto mostrando un spinner propio
  (`cargarBronceYNavegar`: `analizarFuente` → `procesarBronce` → polling de
  `estadoImportacion`) y solo navega a `/etl/upload-bronce?...` cuando el
  pipeline bronce ya terminó — `EtlUploadBronce.tsx` nunca llega a mostrar
  su propio "Iniciando…" en este camino.
- `frontend/src/pages/EtlUploadBronce.tsx`: ajustado para no re-disparar
  `procesarBronce` si `estadoImportacion` ya informa `completado` (evita
  correr el pipeline completo dos veces cuando se llega ya procesado desde
  el drawer; sigue disparando el pipeline normalmente si se llega
  directo, ej. desde el link de `ResumenAnalisis.tsx`).

**Ícono de "bronce" en Gestión de Datos** (misma sesión):

- `backend/app/api/datos/serializers.py`: nuevo campo computado
  `carga_bronce_pendiente_id` en `FuenteDatosSerializer` — la última
  `CargaArchivo` de la fuente con alguna `FilaBronce` en estado distinto de
  `promovido` (`pendiente`/`valido`/`invalido`). `None` si no hay ninguna
  carga bronce pendiente (incluye el caso "nunca se cargó a bronce" y "ya
  se promovió todo").
- `frontend/src/types/index.ts` / `frontend/src/components/data/FuentesTable.tsx`:
  nueva columna de acción — si la fuente tiene `carga_bronce_pendiente_id`
  (y no tiene ya `ultima_carga_importada_id`, que sigue teniendo prioridad
  porque implica flujo clásico completado), se muestra un ícono 🥉 que
  lleva directo a `/etl/upload-bronce?fuente=&carga=` en vez del botón
  "Iniciar carga" (⬆) — comunica que el dato ya está en la capa bronce y
  solo falta validar/corregir, sin pasar de nuevo por análisis.
- Verificado con `python manage.py check` (en el contenedor `backend-web-1`)
  y `npx tsc --noEmit` — ambos limpios. Falta probar en vivo desde el
  navegador (no se creó fuente/carga de prueba nueva para esto en esta
  vuelta).

**Orden de columnas de la vista tipo Excel corregido** (misma sesión): el
usuario reportó que las columnas no respetaban el orden original de la
plantilla — un mismo grupo de modelo (ej. "MUESTRAAMBIENTAL") aparecía dos
veces en posiciones separadas. Causa: `listar_bronce`
(`backend/app/api/etl/views.py`, cerca de la línea 4850) armaba el dict
`celdas` iterando `fila.celdas.all()` sin `order_by` — `CeldaBronce` es una
tabla EAV sin relación de orden con la posición de columna en el archivo,
así que el orden de las keys del dict (y por lo tanto el orden visual en
`BronceTable.tsx`, que agrupa por modelo de forma *secuencial*) terminaba
siendo esencialmente el de inserción en la BD, no el del archivo.
**Corrección:** `listar_bronce` ahora arma el dict `celdas` siguiendo el
orden de `CargaArchivo.hojas[hoja]["columnas_raw"]` (snapshot de columnas
tomado del `DataFrame` original al analizar el archivo, que sí preserva el
orden de la plantilla), con fallback al final para columnas que por algún
motivo no estén en ese snapshot. Verificado con `manage.py check`;
contenedor `backend-web-1` reiniciado para aplicar el cambio (recordatorio:
gunicorn no recarga código en caliente). Falta confirmar visualmente en el
navegador que el orden ya coincide con la plantilla.

**Descarga de la capa bronce a Excel** (misma sesión, botón pedido por el
usuario viendo la vista tipo Excel):

- `backend/app/api/etl/views.py`: `exportar_bronce(request, fuente_id, carga_id)`
  — nueva vista, mismo patrón que `exportar_carga`/`exportar_proyecto`
  (`pd.ExcelWriter`/openpyxl): una pestaña por `hoja` de la carga, columnas
  en el orden de la plantilla (mismo `columnas_raw` que usa `listar_bronce`
  para el orden visual), valores literales de `CeldaBronce` (sin tipar,
  incluidas las filas con error), encabezados coloreados por
  `modelo_destino` vía `_colorear_encabezados` (mismo criterio visual que
  los grupos de color de `BronceTable.tsx`).
- `backend/app/api/urls.py`: ruta nueva
  `GET /api/fuentes-datos/<f>/carga/<c>/bronce/exportar/` (`exportar-bronce`).
- `frontend/src/services/etl.service.ts`: `getExportarBronceUrl(fuenteId, cargaId)`.
- `frontend/src/pages/EtlUploadBronce.tsx`: botón "⬇ Descargar Excel" en el
  encabezado (visible una vez terminado el procesamiento), reusa
  `downloadFile` (`frontend/src/utils/download.ts`), mismo patrón que el
  botón de descarga de `EtlDatos.tsx`.
- Verificado con `manage.py check`/`tsc --noEmit`; contenedor
  `backend-web-1` reiniciado. Falta probar la descarga real desde el
  navegador.

**Pendiente:**

- Probar de punta a punta la promoción real de una hoja completa de
  Metadato: falta mapear 'nombre'/'tipo'/'unidad_experimental' de
  UnidadMuestreo (quedan como "sin mapear" porque no son columnas 1:1 —
  dependen de atributos constantes o de otra sección) para que
  `hojas_bloqueadas` quede vacío y se vea una fila real pasar a
  `estado="promovido"`.
- Decidir si `POST .../bronce/procesar/` se dispara automático desde
  `upload_archivo` una vez esta vista salga de beta, o sigue siendo un
  paso explícito (el link de `ResumenAnalisis.tsx`).
- Retirar (cuando esta vista salga de beta, no antes): casilla "Ya tiene
  el formato de la plantilla" y flujo `?auto=1` de
  `mapeo-automatico-plantilla-flujos-co2.md`.
- Al desplegar al contenedor compartido: reiniciar gunicorn/el contenedor
  después de copiar el código, no alcanza con `docker compose cp` solo
  (ver bug encontrado arriba).
- `promovido_a` queda igual para todas las filas promovidas en una misma
  corrida (bookkeeping por hoja, no por fila individual) — simplificación
  aceptada, ver docstring de `_promover_filas_bronce`.

## Referencias

- [Subir directo a la base de datos un archivo que ya tiene la plantilla](mapeo-automatico-plantilla-flujos-co2.md) — tarea que este diseño revisa/extiende.
- [Plantilla de carga/descarga: metadato y dato de CO2/CH4](../../docs/arquitectura/plantilla-metadato-dato-co2-camaras.md)
- [Ajustes a la plantilla Flujos CO2 — feedback de Andrea Chaparro](ajustes-plantilla-flujos-co2-feedback-andrea.md)
- [Rediseñar vista de subida/descarga: separar metadato y dato por metodología](../backlog/subida-descarga-formato-metadato-dato-por-metodologia.md)
- `docs/arquitectura/modelo-datos.md` — modelo relacional actual al que debe promoverse la capa bronce.
- `tasks/done/etl-datos-a-frontend.md` — patrón de tabla con filtros por columna (`EtlDatos.tsx`/`DatosTable.tsx`) reutilizable para la vista tipo Excel.

## Historial

| Fecha | Descripción |
|---|---|
| 2026-11-16 | Se crea la tarea a partir de una revisión conjunta del flujo de carga de Flujos CO2 (capturas de pantalla del asistente actual). Queda planteada la propuesta de capa bronce/staging + vista tipo Excel con validación inline, pendiente de resolver punto por punto antes de implementar. |
| 2026-11-16 | Diseño cerrado, los 7 puntos del plan resueltos: sin S3 (archivo en filesystem local); modelo bronce EAV (`FilaBronce`/`CeldaBronce`, no JSON ni columnas fijas, decisión explícita del usuario por facilidad de consulta); proceso de validación/promoción que reusa la validación existente pero promueve selectivamente en vez de cortar todo-o-nada; vista tipo Excel reusando el patrón de `DatosTable.tsx`; las 16 columnas ambiguas y los archivos sin match total dejan de ser casos especiales (bronce no depende de mapeo para guardar, solo para promover, columna por columna); este diseño reemplaza el paso 4 pendiente de `mapeo-automatico-plantilla-flujos-co2.md`; alcance acotado a Flujos CO2 para la implementación, modelo ya generalizado para las demás metodologías. Queda pendiente agendar la implementación. |
| 2026-11-16 | Implementado y probado el backend completo (ver Entregables): modelos + 2 migraciones aplicadas contra la RDS compartida (autorizado explícitamente por el usuario antes de correr `migrate`), funciones de poblar/mapear automático/validar/promover, 3 endpoints nuevos. Probado end-to-end contra una copia aislada de un archivo real (fuente 63), con limpieza completa al terminar (autorizada explícitamente antes de escribir datos de prueba en la RDS compartida) — 0 filas promovidas al modelo estructurado porque el selector manual de columnas ambiguas (frontend) todavía no existe, bloqueo correcto por campos obligatorios sin mapear. Queda pendiente la vista tipo Excel del frontend — sin ella, Metadato nunca promueve ninguna fila. |
| 2026-11-16 | Implementado el frontend: `BronceTable.tsx` (vista tipo Excel editable) + página independiente `EtlUploadBronce.tsx` (`/etl/upload-bronce`), con un link opt-in desde `ResumenAnalisis.tsx` del asistente viejo (visible solo si el archivo trae las hojas exactas de Flujos CO2) — el asistente manual sigue intacto. `tsc`/`eslint`/`vite build` limpios. Falta: probar en vivo desde el navegador, y el selector inline de mapeo para columnas ambiguas (sin eso, Metadato sigue sin poder promover ninguna fila en la práctica). |
| 2026-11-16 | Implementado `MapeoColumnaBronceSelector.tsx` (selector inline modelo/campo/clasificación) y probado end-to-end en el navegador real (Claude in Chrome, cuenta de prueba) contra una fuente/carga de prueba. Encontrado y corregido en el camino: gunicorn no recarga código en caliente, hace falta reiniciar el contenedor tras desplegar (relevante para el despliegue real). Encontrado: mapear `cobertura_CLC` → `CoberturaManual.valor` dejaba las 171 filas de Metadato con error. |
| 2026-11-16 | `FuenteDrawer.tsx` ya no manda al asistente manual ni a una pantalla intermedia: al guardar una fuente con "Ya tiene el formato de la plantilla", el drawer se queda abierto procesando y solo navega a la vista tipo Excel cuando el pipeline bronce terminó (`EtlUploadBronce.tsx` ajustado para no re-disparar el pipeline si ya venía completado). Se agregó además un ícono 🥉 en Gestión de Datos (`FuentesTable.tsx`, campo nuevo `carga_bronce_pendiente_id` en el serializer) para fuentes con datos ya en bronce pendientes de validar, que lleva directo a la vista de validación sin re-analizar. Falta probar en vivo desde el navegador. |
| 2026-11-16 | Agregado link "← Volver a Gestión de Datos" en `EtlUploadBronce.tsx` y corregido el orden de columnas de la vista tipo Excel (ahora sigue el orden original de la plantilla, vía `CargaArchivo.hojas[hoja]["columnas_raw"]`, en vez del orden de inserción en la BD EAV). Backend reiniciado para aplicar ambos fixes de esta sesión. |
| 2026-11-16 | Acortado el título a "Vista tipo Excel — Flujos (beta)" (la columna `gas` ya distingue CO2/CH4). Agregado botón "Descargar Excel" en `EtlUploadBronce.tsx` (endpoint nuevo `exportar_bronce`, una pestaña por hoja con columnas en el orden de la plantilla y encabezados coloreados por modelo, mismo patrón que `exportar_carga`). Backend reiniciado. |
| 2026-11-16 | Diagnosticado y corregido el bug de validación de `CoberturaManual.valor` (bug preexistente, no introducido por esta tarea — afecta también al asistente manual, nunca se había probado en vivo): `_validar_columna` lo trataba como FK normal (choices = pks) en vez de texto libre como ya lo describe `campos_destino`. Corregido en `backend/app/api/etl/views.py`. Reprobado en vivo en el navegador con fuente/carga de prueba nueva: `cobertura_CLC` mapea y queda sin ningún error (antes 171/171). De paso se agregó soporte opcional de `mapeo_valores`/valores únicos (`valores_columna_bronce`) al selector para campos FK que sí lo necesiten en el futuro, aunque no hizo falta para este caso. Datos de prueba borrados al terminar (dos tandas, ambas con autorización explícita previa). Pendiente: mapear los campos obligatorios restantes de UnidadMuestreo para ver una fila de Metadato llegar a `estado="promovido"` de punta a punta. |
