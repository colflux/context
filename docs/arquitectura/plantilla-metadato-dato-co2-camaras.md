# Plantilla de carga/descarga: metadato y dato de CO2/CH4 (cámaras GEI)

**Estado:** implementado en el botón "Plantilla de datos" (`/participacion`), primer
caso concreto de [[subida-descarga-formato-metadato-dato-por-metodologia]].

## Corrección importante

[plantilla-metadato-dato-co2.md](plantilla-metadato-dato-co2.md) se escribió asumiendo
que "CO2" se refería a **torre EC (Eddypro)**. Al validar los atributos reales que pasó
el equipo de datos (`analizador`, `anillo`/`tubo`, `chamber_vol`, `day/night`,
`co2_ori`), se confirmó que es la metodología de **cámaras de gases manuales**
(`MuestraGEI`/`SubmuestraGEI`/`MuestraAmbiental` en `backend/app/models/co2.py`), no
torre EC. Este documento reemplaza al anterior como la plantilla CO2 real.

## Qué se implementó (2026-11-01)

En `backend/app/api/etl/views.py`, la vista `plantilla_vacia()` (botón "Plantilla de
datos" en `/participacion`, `frontend/src/pages/Participacion.tsx`) ahora separa la
hoja única "Flujos - CO2"/"Flujos - CH4" en dos hojas cada una:

- **Metadato** (`_MODELOS_METADATO_GEI`): `UnidadExperimental.nombre`,
  `UnidadMuestreo.nombre`, `Sitio.latitud/longitud`, `MuestraGEI.tubo`, `MuestraGEI.gas`,
  `Equipo.modelo` (analizador), `UnidadMedida.simbolo`.
- **Dato**: `SubmuestraGEI.fecha/hora/momento/condicion_luz/valor`, más
  `UnidadMuestreo.nombre` y `MuestraGEI.tubo` repetidos como llave de referencia
  (`_LLAVE_REFERENCIA_GEI`) para cruzar cada fila de dato con su fila de metadato.

Solo cambia el reordenamiento de columnas de la plantilla vacía (`plantilla_vacia`);
`exportar_carga`/`exportar_proyecto` (descarga de datos ya cargados) y el parser de
importación (`importar_carga`) **no se tocaron** — siguen esperando una sola hoja por
gas. Eso es deuda intencional para una siguiente iteración.

## Alcance acotado a solo CO2 (2026-11-02)

Decisión de equipo: la plantilla descargable, por ahora, **solo cubre Flujos CO2** — se
sacaron CH4, MOM, COS y Biomasa de `_HOJAS_PLANTILLA`. En el frontend, el botón
"Descargar plantilla" dejó de mostrarse en las cards COS/Biomasa/MOM
(`Metodologia.tienePlantilla` en `Participacion.tsx`) — solo aparece dentro de la card
**Flujos**. Para reactivar CH4 o sumar otra metodología, agregar su entrada a
`_HOJAS_PLANTILLA` (`backend/app/api/etl/views.py`) y poner `tienePlantilla: true` en la
card correspondiente del frontend.

## Se amplía la hoja Metadato con lo que faltaba (2026-11-06)

Al revisar la lista completa de 49 atributos contra la hoja real "Flujos CO2 -
Metadato" se encontraron dos capas de columnas faltantes, más allá de las ya
documentadas en "Pendiente":

1. **Restringidas desde el 2026-11-02** sin querer: al sacar la hoja aparte "Unidad
   Muestreo-Experimental" (ver sección de abajo), `_VISTAS_DESNORMALIZADAS["submuestra_gei"]`
   quedó con `"incluir"` acotado a lo mínimo en `Sitio` (solo latitud/longitud),
   `UnidadMuestreo` y `UnidadExperimental` (solo `nombre`), y `Parcela` (ninguno) — sin
   trasladar el resto de sus atributos a Metadato como se había dejado pendiente.
2. **Nunca conectadas a la cadena de la vista**: `Proyecto` (vía `UnidadExperimental.proyecto`)
   y la jerarquía geográfica `Vereda`/`Municipio`/`Departamento`/`Region` (vía
   `Sitio.vereda`) — existen como modelos pero la cadena de FKs hacia adelante nunca
   llegaba hasta ellos.

Se resolvieron ambas quitando/acotando las restricciones de `"incluir"` y extendiendo la
`cadena` de `submuestra_gei` (`backend/app/api/etl/views.py`) con `Proyecto`,
`UnidadMuestreoTipo`, `Microtopografia`, `SistemaReferencia`, `Vereda`, `Municipio`,
`Departamento`, `Region` — todas FKs hacia adelante legítimas, así que esto aplica
también a `exportar_carga`/`exportar_proyecto`/`datos_carga` (datos reales), no solo a la
plantilla vacía. Ahora la hoja Metadato trae: `nombre_proyecto`, `codigo_metadatos`,
`region_natural`, `departamento`, `Municipio`, `Vereda`, `sitio`, `Tipo de localización`,
`latitud`, `longitud`, `sistema_referencia`, `altitud`, `pendiente`, `topografia`,
`uso_actual`, `Tipo muestreo`, `Tipo unidad de muestreo`,
`Tamaño unidad de muestreo (área en cm2)`, `Forma unidad de muestreo`, `microtopografia`,
`diametro_anillo`, `tratamiento`, `pozo_nivel_freatico`.

Además, **solo en la plantilla vacía descargable** (`plantilla_vacia`, no en
`exportar_carga`/`datos_carga`) se agregaron como encabezados fijos las columnas de
cobertura/disturbio/ecosistema/exposición externa (`_COLUMNAS_PIVOTE_METADATO_GEI`):
`Ecosistema / Cobertura`, `cobertura_IPCC/CLC/IGBP/nom_comun`, `Suelo IPCC`,
`tipo_disturbio`, `anios_disturbio`, `anios_desde_fin_disturbio`, `Estado conservación`,
`proteccion_legal`, `DOM_DIST_MGMT`, `cobertura_vegetal_primaria/secundaria/terciaria` +
`porcentaje_cob_veg_*`, `distancia_drenaje/fuego/pastoreo/cultivo`. Estas referencian
campos reales (para que el diccionario de datos salga correcto) pero **no traen datos
reales todavía** en ninguna descarga con filas (`exportar_carga`/`exportar_proyecto`):
siguen necesitando la lógica de pivoteo de reverse-FK (ver "Pendiente").

Quedan sin resolver (no tienen campo en ningún modelo): `TEAM_MEMBER_NAME`,
`TEAM_MEMBER_EMAIL` — no existe ningún concepto de "quién reportó este archivo" en el
modelo de datos hoy (¿por carga? ¿por proyecto?), decisión de diseño pendiente antes de
agregar un campo nuevo. `Periodicidad de muestreo` y `tipo_de_suelo` para GEI específicamente
siguen sin campo (`tipo_de_suelo` sí existe pero en el modelo de la metodología COS, no
conectado a Flujos CO2).

## Se elimina la hoja aparte "Unidad Muestreo-Experimental" (2026-11-02)

Decisión de equipo: el contexto de dónde/qué unidad (identificador, sitio) es
información de **cómo se midió**, así que es metadato — no tiene sentido como hoja
propia separada de "Flujos CO2 - Metadato". Se saca `unidad_muestreo` de
`_HOJAS_PLANTILLA`; la plantilla ahora trae 3 hojas: "Flujos CO2 - Metadato", "Flujos
CO2 - Dato" y "Diccionario de datos". El identificador de unidad de muestreo/experimental
y las coordenadas del sitio ya estaban en la hoja Metadato (`_MODELOS_METADATO_GEI`), así
que no se perdió esa referencia — lo que sí queda fuera de la plantilla es el detalle
adicional que solo existía en la vista `unidad_muestreo` (`UnidadMuestreo.fecha_instalacion`,
`UnidadMuestreoTipo.nombre`, descripción de parcela, nombre de sitio) — pendiente de
decidir si se agrega a la hoja Metadato o se asume que esa info se gestiona aparte (ej.
en "Gestión de Datos").

## Validación de atributos del equipo de datos

✅ Ya existen en el modelo y están en la plantilla:

| Atributo equipo | Campo real |
|---|---|
| ID Unidad de muestreo | `UnidadMuestreo.nombre` |
| Fecha instalación unidad de muestreo | `UnidadMuestreo.fecha_instalacion` — ya no está en la plantilla (vivía en la hoja "Unidad Muestreo-Experimental", eliminada el 2026-11-02; ver sección de arriba) |
| analizador | `Equipo.modelo` |
| day/night | `SubmuestraGEI.condicion_luz` |
| month/year/date/hour | `SubmuestraGEI.fecha`/`hora` |
| Unidades | `UnidadMedida.simbolo` |
| soil_temp/air_temp/atm_press/relat_humid/dew_point | `MuestraAmbiental.*` — **no están en esta plantilla todavía** (ver pendientes) |
| water_level_cm | `MuestraAmbiental.water_level` — ídem |
| microtopo | `MuestraAmbiental.microtopo` — ídem |

⚠️ Existen pero con nombre/alcance distinto:

- `anillo` → lo más cercano es `MuestraGEI.tubo` (identificador del tubo/cámara) — confirmar con el equipo si es el mismo concepto.
- `co2_ori` → `SubmuestraGEI.valor` no distingue "original" de "corregido".
- `Tamaño unidad de muestreo (cm2)` → `Parcela.area` existe pero en m², no cm².
- `DOM_DIST_MGMT` → `UnidadMuestreoDisturbio.estado_conservacion` de la fila con `es_dominante=True` (mismo vocabulario IDEAM), implementado 2026-11-03.

❌ No existen en el modelo (quedan fuera de esta plantilla, a definir si se agregan):

Periodicidad de muestreo (descartado). El resto de esta lista (`chamber_vol`, `pH`,
tipo_de_suelo, diametro_anillo, tratamiento, pozo_nivel_freatico,
cobertura_vegetal_primaria/secundaria/terciaria, distancia_drenaje/fuego/pastoreo/cultivo,
Cobertura, Disturbio) **ya se implementó** en los modelos (ver sección siguiente) — sigue
sin aparecer en la plantilla descargable porque la vista `submuestra_gei` de
`_VISTAS_DESNORMALIZADAS` todavía no sabe pivotear estas entidades (ver "Pendiente").

## Campos de Metadato resueltos en sesión posterior (2026-11-02, implementados 2026-11-03)

Revisión campo por campo de la lista completa de 49 atributos de Metadato (ver
[[subida-descarga-formato-metadato-dato-por-metodologia]]). Diseño cerrado el 2026-11-02 e
**implementado en modelos/migraciones el 2026-11-03** (decisión explícita del usuario de
avanzar con catálogos tentativos donde todavía falta confirmar con el equipo/Martín — ver
"Pendiente antes de implementar"/"Pendiente" de cada doc de modelo). Lo que sigue
pendiente en todos los casos es la lógica de pivoteo para que el campo aparezca en la
plantilla exportable (ver sección "Pendiente" más abajo), no el modelo en sí:

- **Ecosistema / Cobertura** → ver [Modelo de datos: ecosistema/zonificación de un sitio](modelo-ecosistema.md).
- **cobertura_IPCC/CLC/IGBP/nom_comun/Suelo IPCC** → ver [Modelo de datos: cobertura de una unidad de muestreo](modelo-cobertura.md).
- **tipo_disturbio, anios_disturbio, anios_desde_fin_disturbio, Estado conservación, proteccion_legal, DOM_DIST_MGMT** → ver [Modelo de datos: disturbio de una unidad de muestreo](modelo-disturbio.md).
- **Tipo muestreo** (probabilístico/no probabilístico, distinto de "Tipo unidad de muestreo") → campo nuevo `UnidadMuestreo.tipo_muestreo` (choices: Probabilístico/No probabilístico).
- **microtopografia** → ver [Modelo de datos: microtopografía de una unidad de muestreo](modelo-microtopografia.md).
- **tipo_de_suelo** (Orgánico/Mineral) → mismo campo que `Suelo IPCC`, ya cubierto como `TipoCobertura` código `Suelo_IPCC` en [Modelo de datos: cobertura de una unidad de muestreo](modelo-cobertura.md) — no es un campo nuevo.
- **diametro_anillo / Tamaño y forma de unidad de muestreo (área en cm²)** → el "anillo" (collar) se instala una sola vez por `UnidadMuestreo` y queda fijo toda la campaña — no es un atributo de cada `MuestraGEI` (evento de medición), que solo referencia el anillo vía `tubo`. Campos nuevos en **`UnidadMuestreo`**: `diametro_anillo_cm` (dato crudo) + `area_cm2` (calculado, mismo patrón que `Parcela._calcular_area()`).
- **tratamiento** → campo nuevo `UnidadExperimental.tratamiento` (texto libre), distinto de `nombre`/`descripcion` — qué condición experimental describe (ej. "con pastoreo" vs. "control"). Sin ejemplos de valores reales todavía, pendiente de confirmar con el equipo.
- **pozo_nivel_freatico** → campo nuevo `UnidadMuestreo.tiene_pozo_nivel_freatico` (BooleanField) — indica si existe la infraestructura (pozo/piezómetro). El valor de la medición en sí ya existe: `MuestraAmbiental.water_level`.
- **cobertura_vegetal_primaria/secundaria/terciaria + porcentaje_cob_veg_\*** → `Vegetacion.tipo_cobertura` es, en el fondo, otro sistema de clasificación de cobertura (vegetación funcional) — se absorbe como `TipoCobertura`/`ValorCobertura` dentro de [Modelo de datos: cobertura de una unidad de muestreo](modelo-cobertura.md), con `porcentaje`/`orden_dominancia` nuevos en `CoberturaManual`.
- **distancia_drenaje/fuego/pastoreo/cultivo** → entidad nueva `FuenteExterna`/`ExposicionExterna` (distinta de `Disturbio`: es exposición a algo que pasa cerca, no un evento ocurrido en la unidad), ver [Modelo de datos: exposición externa de una unidad de muestreo](modelo-exposicion-externa.md).

**Revisión completa de los 49 campos de Metadato: cerrada e implementada.** Todos tienen
modelo (implementado, ya existente, o nuevo) o fueron descartados (Periodicidad de
muestreo). Falta la lógica de pivoteo para la plantilla exportable (ver "Pendiente") y
confirmación de valores/listas cerradas con el equipo y con Martín donde se usaron
catálogos tentativos — ver "Pendiente" en cada doc de modelo.

**Periodicidad de muestreo** → decisión de equipo: se descarta, no se agrega a la
plantilla.

## Campos de Dato resueltos en sesión posterior (2026-11-02)

Revisión campo por campo de la lista completa de columnas de Dato (`ID`, `No Unidad de
muestreo`, `Fecha instalación unidad de muestreo`, `analizador`, `id`, `anillo`, `month`,
`year`, `date`, `hour`, `chamber_vol`, `day/night`, `co2_ori`, `Unidades`, `soil_temp`,
`air_temp`, `atm_press`, `relat_humid`, `dew_point`, `water_level_cm`, `microtopo`, `pH`):

- **`ID`/`id`** → decisión de equipo: se descartan, no se agregan a la plantilla.
- **`No Unidad de muestreo`, `analizador`, `anillo`** → no son campos de Dato — son
  identificador de unidad/equipo, ya resueltos en Metadato (`UnidadMuestreo.nombre`,
  `Equipo.modelo`, `MuestraGEI.tubo` respectivamente). `anillo` además es parte de
  `_LLAVE_REFERENCIA_GEI`, la llave que cruza cada fila de Dato con su fila de Metadato.
- **`microtopo`** → mismo caso que `analizador`/`anillo`: es un rasgo del terreno, fijo
  por `UnidadMuestreo` (no cambia de una lectura a otra), así que tampoco es Dato — va a
  Metadato como `UnidadMuestreo.microtopografia`, ver
  [Modelo de datos: microtopografía de una unidad de muestreo](modelo-microtopografia.md).
  Que aparezca repetido en cada fila del Excel crudo del equipo es el mismo patrón que
  `analizador`/`anillo`: dato fijo de la unidad repetido por conveniencia en la
  exportación, no una medición nueva por lectura.
- **`Fecha instalación unidad de muestreo`** → tampoco es Dato — es fija por
  `UnidadMuestreo` (se instala una sola vez, igual que el anillo), va a Metadato como
  campo nuevo `UnidadMuestreo.fecha_instalacion` (ya existe en el modelo, resuelve el
  pendiente dejado al eliminar la hoja "Unidad Muestreo-Experimental", ver más arriba).
- **`month`/`year`/`date`/`hour`** → descomposición de `SubmuestraGEI.fecha`/`hora`, ya existen.
- **`day/night`** → `SubmuestraGEI.condicion_luz`, ya existe.
- **`co2_ori`** → `SubmuestraGEI.valor`, ya existe (⚠️ no distingue original/corregido, ver tabla de validación arriba).
- **`Unidades`** → `UnidadMedida.simbolo`, ya existe.
- **`soil_temp`/`air_temp`/`atm_press`/`relat_humid`/`dew_point`/`water_level_cm`** →
  `MuestraAmbiental.*`, ya existen pero esa vista no está cruzada con `submuestra_gei`
  todavía (pendiente ya listado abajo).
- **`chamber_vol`** → implementado (2026-11-03) como `MuestraGEI.chamber_vol` (propiedad
  de la cámara/anillo, no de cada lectura).
- **`pH`** → implementado (2026-11-03) como `MuestraAmbiental.ph`.

**Revisión completa de los campos de Dato: cerrada e implementada.** `chamber_vol`/`pH`
ya existen en el modelo; igual que el resto de campos de Dato, siguen sin aparecer en la
plantilla exportable porque `MuestraAmbiental` no está cruzada con `submuestra_gei`
todavía (ver "Pendiente").

## Vista de detalle de la plantilla, sin descargar el Excel (2026-11-06)

Se agrega el botón "Ver detalle de la plantilla →" junto a "Descargar plantilla →" en
`Participacion.tsx` (solo visible donde `plantillaDisponible`, hoy Flujos CO2). Abre un
modal (`PlantillaDetalleModal.tsx`) con tabs Metadato/Dato que lista, por hoja, cada
atributo con su descripción y de qué entidad del modelo de datos sale (mismo contenido
que ya existía en la hoja "Diccionario de datos" del Excel, ahora también disponible sin
tener que descargar nada).

Backend: `plantilla_detalle` (`backend/app/api/etl/views.py`, GET
`api/etl/plantilla/detalle/`), reutiliza `_hojas_plantilla_vacia` (nueva función,
extraída de `plantilla_vacia`) y `_dataframe_diccionario_datos` — mismo origen de datos
que el Excel, sin mantenimiento aparte: si se cierra una columna del backlog arriba, el
detalle se actualiza solo.

## `codigo_metadato` se mueve de `Sitio` a `UnidadMuestreo` (2026-11-06)

El campo existía como `Sitio.codigo_metadatos` ("código del sitio en el sistema de
metadatos externo"), pero conceptualmente no es un atributo del sitio: es el
identificador que trae la fuente para una **muestra** (ej.
`IDEAM_Humedales_Flujos_PNN Chingaza_calostros_1`), y varias unidades de muestreo
pueden compartir sitio con códigos de metadato distintos. Se decidió, revisando bases
reales de IDEAM:

- El identificador natural de una unidad de muestreo sigue siendo
  `unidad_experimental` + `unidad_muestreo` cuando la fuente distingue ambos niveles.
- Si la fuente no trae esa distinción pero sí trae un código de metadato propio, se usa
  ese código tal cual (`UnidadMuestreo.codigo_metadato`, antes `Sitio.codigo_metadatos`).
- Si tampoco lo trae, se construye en el importador como
  `"{unidad_experimental}_{unidad_muestreo}"` — **la construcción del fallback en el
  importador queda pendiente**, solo se movió el campo.

Implementado: `Sitio.codigo_metadatos` → `UnidadMuestreo.codigo_metadato` (migración
`0117_mover_codigo_metadato_a_unidad_muestreo.py`, con backfill de
`UnidadMuestreo.proyecto` — campo nuevo, obligatorio, derivado de
`unidad_experimental.proyecto` para las 768 unidades existentes, todas con
`unidad_experimental` asignada). Unicidad: `UniqueConstraint(proyecto,
codigo_metadato)` condicionada a `codigo_metadato != ""` (no aplica a las unidades que
todavía no lo tienen). Plantilla Flujos CO2: la columna pasa de
`Sitio.codigo_metadatos` a `UnidadMuestreo.codigo_metadato` en `_ORDEN_COLUMNAS_METADATO_GEI_PLANTILLA`
y en el `orden_columnas` de `submuestra_gei`, mismo lugar (justo después del nombre de
unidad de muestreo) — 58 columnas en Metadato, sin pérdidas. También se actualizaron
`admin.py` (`UnidadMuestreoAdmin` ahora busca/muestra `codigo_metadato`), `forms.py`
(se saca de `SitioForm`, que de todos modos no se usa en ningún lado) y se
regeneró/sincronizó `docs/assets/data/catalogo.json` → `frontend/src/assets/data/catalogo.json`.

## Se revierte `UnidadMuestreo.proyecto`/`fuente_datos`: `unidad_experimental` vuelve obligatoria (2026-11-06)

Al diseñar el punto anterior se agregó un FK directo `UnidadMuestreo.proyecto` para
cubrir el caso en que la fuente no distingue unidad experimental de unidad de
muestreo (entonces `unidad_experimental` quedaba sin asignar y no había de dónde sacar
el proyecto). Revisando el código existente se identificaron dos problemas con ese
enfoque:

1. **Precedente ya establecido:** `fuente_datos` siempre vive en la entidad de
   *medición* (`MuestraAmbiental.fuente_datos`, `MuestraTorre.fuente_datos`), nunca en
   la unidad física estructural — pero `UnidadMuestreo.fuente_datos` (que ya existía
   antes de esta sesión) rompía esa convención. Se decide sacarlo de ahí.
2. El importador ya resuelve `UnidadExperimental.proyecto` desde
   `carga.fuente.proyecto` (`backend/app/api/etl/views.py`, línea ~2636) cuando no
   viene mapeado — es decir, el camino real para llegar a "proyecto" siempre pasa por
   `FuenteDatos` → `UnidadExperimental`, nunca directo a `UnidadMuestreo`.

Se revierte a la forma original: `UnidadMuestreo.unidad_experimental` vuelve a ser
**obligatoria** (como estaba antes de este punto de diseño). Cuando la fuente no
distingue los dos niveles, el importador debe crear una `UnidadExperimental` igual
(mismo nombre u otra convención — **pendiente de definir** cuál) en vez de dejar el FK
vacío; así `proyecto` siempre sale de `unidad_experimental.proyecto`, sin necesidad de
duplicarlo en `UnidadMuestreo`. Se elimina `UnidadMuestreo.fuente_datos` (campo
existente, sin uso real salvo el `kwargs.setdefault` del importador, que también se
quita).

`codigo_metadato` se queda tal cual, pero la unicidad cambia de
`(proyecto, codigo_metadato)` a `(unidad_experimental, codigo_metadato)` —
`UniqueConstraint` no puede atravesar relaciones (`unidad_experimental__proyecto`), así
que la unicidad a nivel de proyecto completo (entre distintas unidades experimentales)
queda como responsabilidad del importador al resolver/crear por `codigo_metadato`, no
forzada por la base de datos.

Implementado: migración `0118_quitar_proyecto_y_fuente_datos_de_unidad_muestreo.py`.
Verificado con `manage.py check`, `makemigrations --check --dry-run` y regenerando el
Excel real (58 columnas en Metadato, sin cambios — ninguno de los campos removidos
estaba expuesto en la plantilla).

## Se cambia el criterio Metadato/Dato: dueño del modelo, no variabilidad (2026-11-09)

El criterio original (2026-11-01) separaba por "¿varía entre tomas o es fijo por
instalación?" — por eso `tubo`, `gas`, `chamber_vol` (volumen de cámara) vivían en
Metadato pese a ser campos propios de `MuestraGEI`. Decisión de equipo: cambiar a un
criterio más simple — **todo lo que es campo propio de `MuestraGEI`/`SubmuestraGEI`
(incluyendo lo que cuelga de `MuestraGEI` por FK: `Equipo`/analizador,
`UnidadMedida`/unidad_flujo) va en Dato**, sin excepción. Metadato queda a nivel de
unidad de muestreo (no distingue tubo/gas/serie dentro de la misma unidad); cada fila
de Dato se autodescribe completa con su propio tubo/gas/chamber_vol/analizador/unidad.

Implementado en `_MODELOS_METADATO_GEI`/`_LLAVE_REFERENCIA_GEI`
(`backend/app/api/etl/views.py`): se sacaron `MuestraGEI`, `Equipo`, `UnidadMedida` del
set de modelos de Metadato; `_LLAVE_REFERENCIA_GEI` queda solo en
`{"UnidadMuestreo.nombre"}` (ya no necesita repetir `MuestraGEI.tubo` como llave, porque
`MuestraGEI` completo vive en Dato de por sí).

## Reorganización y limpieza de la hoja Metadato (2026-11-09)

El equipo de datos dio un orden cerrado de atributos para la hoja "Flujos CO2 -
Metadato" (`_ORDEN_COLUMNAS_METADATO_GEI_PLANTILLA` en `backend/app/api/etl/views.py`),
en dos rondas: primero un orden de 42, luego una segunda pasada que reubica
`diametro_anillo`/`pozo_nivel_freatico`/`tratamiento` (de `UnidadExperimental`/
`UnidadMuestreo`, antes solo en orden natural) junto al resto de atributos de la
unidad de muestreo, mueve `uso_actual` junto a `propiedad_tierra`, y elimina
`region_natural`/`departamento`/`municipio`/`vereda` de la hoja. `tipo_localizacion`
se mantiene después de `sistema_referencia` (confirmado explícitamente, aunque no
apareció repetido en la segunda lista). Orden final (45 columnas) verificado en vivo
contra `_hojas_plantilla_vacia()`. Cambios de contenido acumulados de ambas rondas:

- **Se quitan de la plantilla** (el campo del modelo no se toca, solo deja de ser
  columna de esta hoja):
  - `Sitio.nombre` (columna `sitio`) — la fila ya se identifica con
    `codigo_metadato`/`nombre_unidad_muestreo`.
  - `Institucion.nombre` (columna `nombre_entidad`).
  - `Proyecto.nombre` (columna `nombre_proyecto`) — `Proyecto` sigue en la cadena
    solo para el join hacia `unidad_experimental.proyecto`.
  - `UnidadMuestreo.compartimento` — campo opcional legítimo (0/768 unidades lo usan
    hoy, pero no está huérfano ni es redundante, a diferencia de `Sitio.intervenido`
    que sí se evaluó y se decidió mantener), se saca de esta hoja por decisión de
    equipo, no por estar en desuso.
  - `Region.nombre`, `Departamento.nombre`, `Municipio.nombre`, `Vereda.nombre`
    (columnas `region_natural`/`departamento`/`municipio`/`vereda`) — siguen en la
    cadena de `submuestra_gei` (por si algo más necesita resolver esa relación), solo
    dejan de mostrarse como columna de esta hoja.
- **Renombres** (solo la etiqueta de columna, `verbose_name` en el código — no son
  campos de modelo, así que no requieren migración):
  - `DOM_DIST_MGMT` → `disturbio_dominante`
  - `ecosistema_cobertura` → ya estaba como `ecosistema_IDEAM` en código, sin cambio real
  - `cobertura_nom_comun` → `cobertura_Nombre_Local`
  - `suelo_IPCC` → `uso_suelo_IPCC`
  - `porcentaje_cob_veg_pri/sec/ter` → `porc_cobertura_vegetal_primaria/secundaria/terciaria`
- **Catálogo duplicado detectado, no agregado a la plantilla**:
  `ClasificacionTipo(categoria="Uso Suelo", nombre="Uso_actual_colflux")` tiene
  exactamente los mismos 12 valores que `Sitio.USO_ACTUAL_CHOICES` (columna
  `uso_actual`) — mismo vocabulario cargado dos veces en el modelo. El equipo pidió
  originalmente una columna `uso_actual_IPCC` para este catálogo; al confirmarse la
  duplicación, se decidió no agregarla. El catálogo `Uso_actual_colflux` queda sin usar
  — candidato a limpieza futura (ver Pendiente).

## Descripciones de atributos completadas (2026-11-09)

Revisión de la vista "Detalle de la plantilla" (`frontend/src/components/etl-upload/MapeoList.tsx`,
vía `AtributoRow.tsx`): la columna "Descripción" sale del `help_text` del campo Django
(`backend/app/api/etl/views.py:_dataframe_diccionario_datos`), con un *fallback* a
"Sistema de clasificación: {nombre}." para las columnas que pivotean sobre el campo
genérico `ValorClasificacionTipo.valor`/`ValorClasificacionEcosistema.valor` (que no
tiene `help_text` propio porque un mismo campo sirve para varios catálogos:
`tipo_disturbio`, `uso_suelo_IPCC`, `ecosistema_IDEAM`, `cobertura_IPCC/CLC/IGBP/
Nombre_Local/vegetal_primaria/secundaria/terciaria`). Ese fallback se considera
descripción suficiente y no se tocó.

De las 45 columnas de "Flujos CO2 - Metadato", 10 tenían el campo real sin `help_text`
y sin ese fallback disponible (campos propios de un solo modelo, sin catálogo detrás).
Se agregó `help_text` en el modelo para cada una (migración
`0126_completar_help_text_diccionario_datos`, solo texto — no cambia columnas ni
datos):

- `Microtopografia.nombre`
- `UnidadMuestreo.diametro_anillo_cm` / `UnidadMuestreo.area_cm2`
- `Parcela.forma`
- `SistemaReferencia.nombre`
- `DisturbioManual.es_dominante` / `anios_disturbio` / `anios_desde_fin`
- `CoberturaManual.porcentaje` (genérico para primaria/secundaria/terciaria, distingue
  por `orden_dominancia`)
- `ExposicionExterna.distancia_m` (genérico para drenaje/fuego/pastoreo/cultivo,
  distingue por `fuente`)

Regenerado y sincronizado `catalogo.json`/`catalogo.js` (`python manage.py
generate_catalogo` + copia a `frontend/src/assets/data/catalogo.json`) para que el
diccionario de datos (`/db`) y el modal de detalle de plantilla reflejen las
descripciones nuevas.

## Columnas de clima agregadas a la hoja Dato (2026-11-09)

Se revisaron 20 columnas de un archivo fuente real de cámaras estáticas (`codigo_metadato`,
`analizador`, `gas`, `anillo`, `month`, `year`, `date`, `hour`, `chamber_vol`,
`day/night`, `co2_ori`, `unidad_flujo`, `soil_temp`, `air_temp`, `atm_press`,
`relat_humid`, `dew_point`, `water_level_cm`, `microtopo`, `pH`) contra el modelo de
datos. Hallazgos:

- `co2_ori` **no es un campo nuevo**: con el archivo real a la vista, la columna
  "Unidades" junto a ella ya es `unidad_flujo` y los valores (decimales con signo, en
  `g m2/h`) son el flujo — mapea a `SubmuestraGEI.valor` (`valor_flujo`), que ya
  existe. El nombre de la columna fuente es confuso pero no hay gap de modelo.
- `anillo` ≈ `MuestraGEI.tubo` (columna `tubo`), `day/night` ≈
  `SubmuestraGEI.condicion_luz`, `microtopo` ≈ `UnidadMuestreo.microtopografia` — ya
  cubiertos con otro nombre.
- `month`/`year` no se guardan por separado, solo como `fecha` combinada — no es un
  gap, es un detalle de cómo se arma `fecha` en el import.
- Los 7 campos biomet (`soil_temp`, `air_temp`, `atm_press`, `relat_humid`,
  `dew_point`, `water_level_cm`, `pH`) sí están modelados (`MuestraAmbiental`,
  `backend/app/models/co2.py`), pero vivían solo en la vista `clima` de
  `_VISTAS_DESNORMALIZADAS`, sin hoja/columnas en la plantilla de Flujos CO2 — la
  fuente real los trae junto con el dato de flujo en la misma fila.

Decisión de equipo: `MuestraAmbiental` sigue siendo una entidad separada de
`MuestraGEI`/`SubmuestraGEI` (no se fusionan), pero se quiere la **opción** de
reportarlas en la misma hoja/carga cuando la fuente las trae juntas, enlazadas por
fila (misma `unidad_muestreo`/`fecha`/`hora`). Implementado en esta sesión, **solo la
parte de la plantilla**: las 7 columnas se agregaron como `_COLUMNAS_PIVOTE_DATO_GEI`
en `backend/app/api/etl/views.py`, apendizadas a la hoja "Flujos CO2 - Dato" (mismo
patrón fijo que `_COLUMNAS_PIVOTE_METADATO_GEI` para Metadato — `MuestraAmbiental`
tiene su propia FK a `UnidadMuestreo`, paralela a `MuestraGEI`, así que no la trae la
cadena de FKs hacia adelante que arma el resto de columnas). La hoja "Flujos CO2 -
Dato" queda con 18 columnas: las 11 de siempre + `soil_temp`, `air_temp`, `atm_press`,
`relat_humid`, `dew_point`, `water_level_cm`, `pH`.

**Pendiente** (ver [[plantilla-flujos-co2-clima-misma-hoja]] en
`context/tasks/backlog/`): hoy estas 7 columnas solo reservan el lugar en la plantilla
descargable — `importar_carga`/`exportar_carga` todavía no crean/completan el
`MuestraAmbiental` enlazado cuando vienen con dato. La carga de Clima por separado
(vista `clima`) sigue funcionando igual que antes.

## Ajuste final de columnas de la hoja Dato (2026-11-09)

El equipo de datos confirmó el listado definitivo de 20 atributos para la hoja
"Flujos CO2 - Dato" (reemplaza el de 18 columnas de la sección anterior):

`codigo_metadato, analizador, gas, volumen_camara, anillo, tubo, fecha_toma,
hora_toma, momento, condicion_luz, valor_flujo, unidad_flujo, soil_temp, air_temp,
atm_press, relat_humid, dew_point, water_level_cm, microtopo, pH`

Dos correcciones respecto al análisis anterior:

- **`anillo` no es lo mismo que `tubo`** — la nota previa ("`anillo` ≈ `MuestraGEI.tubo`")
  quedó corregida: son dos conceptos separados. `tubo` es el identificador del
  tubo/cámara conectado al analizador en esa medición (`MuestraGEI.tubo`); `anillo` es
  el diámetro físico del anillo/collar instalado en la unidad de muestreo
  (`UnidadMuestreo.diametro_anillo_cm`, ya modelado, mismo campo que alimenta
  `area_cm2` y que aparece como `diametro_anillo` en Metadato). Ambos se repiten ahora
  como columnas separadas en Dato.
- **`microtopo` pasa de "ya cubierto" a columna real de Dato** — sigue siendo
  `Microtopografia.nombre` (mismo campo que en Metadato), pero el equipo pidió
  repetirlo también en Dato para no tener que cruzar con Metadato al leer un archivo
  de cámaras.
- **`nombre_unidad_muestreo` se elimina de Dato**, reemplazada por `codigo_metadato`
  como columna de referencia hacia Metadato (`UnidadMuestreo.codigo_metadato`).

Implementación en `backend/app/api/etl/views.py`:

- `_LLAVE_REFERENCIA_GEI` cambió de `{"UnidadMuestreo.nombre"}` a
  `{"UnidadMuestreo.codigo_metadato"}`.
- `_COLUMNAS_PIVOTE_DATO_GEI` ganó dos entradas más (`UnidadMuestreo.diametro_anillo_cm`
  → `anillo`, `Microtopografia.nombre` → `microtopo`), mismo patrón fijo que las 7
  biomet.
- Nueva `_ORDEN_COLUMNAS_DATO_GEI_PLANTILLA` (igual patrón que
  `_ORDEN_COLUMNAS_METADATO_GEI_PLANTILLA`) fuerza el orden exacto de las 20 columnas
  acordado con el equipo; `_hojas_plantilla_vacia()` ahora reordena también la sección
  "dato", no solo "metadato".

Verificado en vivo: la hoja "Flujos CO2 - Dato" devuelve 20 columnas en el orden
exacto de arriba. Sigue pendiente lo mismo que antes: `importar_carga`/`exportar_carga`
no crean todavía el `MuestraAmbiental` enlazado a partir de estas columnas (ver
[[plantilla-flujos-co2-clima-misma-hoja]]).

**Corrección el mismo día:** el equipo sacó `microtopo` de Dato — queda solo en
Metadato (`Microtopografia.nombre`). La hoja "Flujos CO2 - Dato" queda en **19
columnas**: las 20 de arriba menos `microtopo`. Cambio en
`backend/app/api/etl/views.py`: se quitó la entrada `Microtopografia.nombre` de
`_COLUMNAS_PIVOTE_DATO_GEI` y de `_ORDEN_COLUMNAS_DATO_GEI_PLANTILLA`. Verificado en
vivo.

## Pendiente (siguientes iteraciones — "vamos corrigiendo")

- Evaluar si `ClasificacionTipo(categoria="Uso Suelo", nombre="Uso_actual_colflux")`
  (ver arriba) debe borrarse del catálogo — quedó sin ninguna columna de la plantilla
  que lo use, duplica `Sitio.USO_ACTUAL_CHOICES`.

- **Lógica de pivoteo nueva para que `exportar_carga`/`exportar_proyecto`/`datos_carga`
  (descargas CON datos reales) completen las columnas de cobertura/disturbio/ecosistema/
  exposición externa** — hoy esas columnas solo existen como encabezados fijos en la
  plantilla vacía (`_COLUMNAS_PIVOTE_METADATO_GEI`, agregado 2026-11-06), sin datos.
  `_campos_planos`/`cadena` en `_VISTAS_DESNORMALIZADAS["submuestra_gei"]`
  (`backend/app/api/etl/views.py`) solo sigue relaciones FK hacia **adelante** desde
  `SubmuestraGEI`. `CoberturaManual`, `UnidadMuestreoDisturbio`, `EcosistemaManual`,
  `ExposicionExterna` (y `MuestraAmbiental`, para `soil_temp`/`air_temp`/etc.) cuelgan por
  FK **inversa** desde `UnidadMuestreo`, y varias permiten más de una fila por unidad
  (`CoberturaManual`, `UnidadMuestreoDisturbio`, `EcosistemaManual`) — necesitan pivotear a
  columnas (una por tipo/clasificación/fuente) en vez de solo seguir la cadena.
  `UnidadMuestreo.microtopografia`, `Proyecto`, y la jerarquía geográfica
  (`Vereda`/`Municipio`/`Departamento`/`Region`) ya se resolvieron (2026-11-06): eran FK
  hacia adelante simples, solo faltaba sumarlas a la cadena existente.
- Definir dónde vive "quién reportó este archivo" (`TEAM_MEMBER_NAME`/`TEAM_MEMBER_EMAIL`)
  antes de agregar un campo nuevo — no hay ese concepto en el modelo hoy (¿por `CargaArchivo`?
  ¿por `FuenteDatos`? ¿por proyecto?).
- `nombre_entidad` (institución a la que pertenecen los datos, `Institucion.nombre`, agregado
  2026-11-06 como columna de pivoteo header-only) tiene el mismo problema de pivoteo que
  cobertura/disturbio/ecosistema, más uno extra: `Proyecto↔Institucion` es M2M (un proyecto
  puede tener varias instituciones), así que antes de darle datos reales hay que decidir qué
  hacer si hay más de una (¿la primera? ¿una fila por institución? ¿concatenar nombres?).
- Construir en el importador el fallback de `UnidadMuestreo.codigo_metadato` cuando la
  fuente no lo trae (`"{unidad_experimental}_{unidad_muestreo}"`, ver sección de arriba) —
  hoy el campo existe pero nada lo autocompleta.
- Definir qué hace el importador cuando la fuente no distingue unidad experimental de
  unidad de muestreo: `unidad_experimental` es obligatoria (ver sección de arriba), así
  que hay que crear una automáticamente (¿mismo nombre que la unidad de muestreo? ¿una
  por sitio?) en vez de dejarla sin resolver.
- Extender la separación metadato/dato a MOM, COS y Biomasa (hoy siguen en una sola hoja).
- Actualizar `importar_carga` para que pueda re-ensamblar `MuestraGEI`+`SubmuestraGEI`
  a partir de dos hojas (hoy el parser asume una sola hoja por gas) — necesario para que
  la plantilla separada se pueda volver a subir.

## Referencias

- [[subida-descarga-formato-metadato-dato-por-metodologia]]
- `backend/app/api/etl/views.py` — `_HOJAS_PLANTILLA`, `_MODELOS_METADATO_GEI`, `_columnas_seccion_gei`, `plantilla_vacia`, `plantilla_detalle`
- `frontend/src/components/common/PlantillaDetalleModal.tsx`
- `backend/app/models/co2.py` — `MuestraGEI`, `SubmuestraGEI`, `MuestraAmbiental`
- `frontend/src/pages/Participacion.tsx`
