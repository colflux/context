# Plantilla de carga/descarga: metadato y dato de COS (carbono orgánico del suelo)

**Estado: implementado, probado de punta a punta con el archivo real y carga real
habilitada en el frontend (`subidaDisponible: true`) desde 2026-11-24 — ver "Prueba
de carga real" más abajo.**
Repite el ejercicio hecho
para Flujos CO2/CH4 ([plantilla-metadato-dato-co2-camaras.md](plantilla-metadato-dato-co2-camaras.md))
y para Biomasa ([plantilla-metadato-dato-biomasa.md](plantilla-metadato-dato-biomasa.md))
pero para la metodología de COS (`CaracterizacionMuestreoSuelo`/`MonitoreoSuelo`/
`SubmuestraSuelo` en `backend/app/models/suelo.py`). Punto de partida: el Excel real
que trae el equipo de datos (`context/data/Metadatos y BD COS.xlsx`, hoja
"Metadatos COS" + hoja "BD COS").

**Diferencia clave con Biomasa:** a diferencia de esa metodología (donde 7 columnas
de Metadato no tenían ningún campo en el modelo), el modelo de COS
(`backend/app/models/suelo.py`) ya existe y sus nombres/`help_text` coinciden casi
literalmente con los encabezados de este Excel (ej. `barreno_vol`, `soil_chem_c_org`,
`metodologia_distancia_m`) — probablemente se diseñó ya mirando esta misma fuente en
una sesión anterior. El pendiente aquí no es mayormente de **campos faltantes**, sino
de **plantilla separada Metadato/Dato** (hoy COS usa la vista genérica compartida con
MOM/Biomasa, `_CAMPOS_METODOLOGIA`/`_ORDEN_COLUMNAS_METODOLOGIA` en
`backend/app/api/etl/views.py`, solo 4 columnas de contexto) y de **lógica de pivoteo**
para los campos que cuelgan de `Sitio`/`UnidadMuestreo` por FK inversa (cobertura,
disturbio, ecosistema, caracterización de suelo) — mismo pendiente ya documentado para
Flujos CO2.

## Hoja "COS - Metadato" (propuesta)

Mismo bloque de contexto (sitio, geografía, cobertura, disturbio, ecosistema) que
Flujos CO2 y Biomasa — son los mismos modelos compartidos (`Sitio`, `UnidadMuestreo`,
`CoberturaManual`, `DisturbioManual`, `EcosistemaManual`, `ClasificacionTipo`/
`ValorClasificacionTipo`), así que esas columnas ya existen y se pueden reutilizar tal
cual. Las columnas propias de COS (`tipo_de_suelo` en adelante) son nuevas frente a
Flujos/Biomasa, mapeadas a `CaracterizacionMuestreoSuelo`/`MonitoreoSuelo`.

| Campo (Excel) | Tipo de dato | Descripción | Entidad.atributo (Modelo de Datos COLFLUX) | Estado |
|---|---|---|---|---|
| nombre_proyecto | Texto | Nombre del proyecto/fuente. | Proyecto.nombre | 🚫 excluido de la hoja final (misma decisión que Flujos, 2026-11-09 — confirmado para COS, ver nota debajo de la tabla) |
| TEAM_MEMBER_NAME | Texto | Nombre de quien reportó los datos. | — | 🚫 no va como columna de Metadato — se resuelve en hoja aparte "Responsables" (ver nota debajo de la tabla), mismo mecanismo ya implementado para Flujos |
| TEAM_MEMBER_EMAIL | Texto | Correo de quien reportó los datos. | — | 🚫 idem, misma hoja "Responsables" |
| codigo_metadatos | Texto | Identificador de la unidad de muestreo en el sistema de metadatos externo de la fuente (ej. `IDEAM_COS_NN Nevados_SanAntonioBInt_2`). | UnidadMuestreo.codigo_metadato | ✅ existe |
| region_natural | Texto | Región natural del sitio. | Region.nombre | ✅ existe (vía Sitio → Vereda → Municipio → Departamento → Region) |
| departamento | Texto | Departamento del sitio. | Departamento.nombre | ✅ existe |
| Municipio | Texto | Municipio del sitio. | Municipio.nombre | ✅ existe |
| Vereda | Texto | Vereda del sitio. | Vereda.nombre | ✅ existe |
| sitio | Texto | Nombre del sitio. | Sitio.nombre | ✅ existe |
| Tipo de localización | Texto | Precisión espacial de la ubicación. | Sitio.tipo_localizacion | ✅ existe |
| latitud / longitud | Numérico (decimal) | Coordenadas del sitio (WGS84). | Sitio.latitud / Sitio.longitud | ✅ existe |
| sistema_referencia | Texto | Sistema de referencia de coordenadas. | SistemaReferencia.nombre | ✅ existe |
| altitud | Numérico (decimal) | Altitud sobre el nivel del mar, en metros. | Sitio.altitud | ✅ existe |
| pendiente | Texto | Categoría de pendiente del terreno. | Sitio.pendiente | ✅ existe (en el Excel real, vacío en las 52 filas relevadas) |
| topografia | Texto | Posición topográfica. | Sitio.topografia | ✅ existe (idem, vacío en los datos reales) |
| Ecosistema / Cobertura | Texto | Sistema de clasificación IDEAM. | ValorClasificacionEcosistema.valor | ✅ existe (`ecosistema_IDEAM` en Flujos) |
| cobertura_IPCC / cobertura_CLC / cobertura_IGBP / cobertura_nom_comun | Texto | Sistemas de clasificación de cobertura. | ValorClasificacionTipo.valor | ✅ existen (mismos 4 catálogos que Flujos/Biomasa) |
| Suelo IPCC | Texto | Mineral / Orgánico, según clasificación IPCC — condiciona cuánto carbono puede almacenar el suelo (ver [¿Qué es la cobertura?](../conocimiento/que-es-la-cobertura.md)). | ValorClasificacionTipo.valor (tipo=Suelo_IPCC) | ✅ existe (`uso_suelo_IPCC` en Flujos) — **fuente de verdad decidida** (ver nota debajo de la tabla): es el mismo dato que `tipo_de_suelo`, se resuelve con este catálogo |
| tipo_disturbio | Texto | Sistema de clasificación: Disturbio. | ValorClasificacionTipo.valor | ✅ existe |
| anios_disturbio | Numérico (entero) | Años que duró/lleva el disturbio. | DisturbioManual.anios_disturbio | ✅ existe |
| anios_desde_fin_disturbio | Numérico (entero) | Años desde que terminó el disturbio. | DisturbioManual.anios_desde_fin | ✅ existe |
| uso_actual | Texto | Uso actual del suelo. | Sitio.uso_actual | ✅ existe |
| Estado conservación | Texto | Taxonomía IDEAM de manejo humano. | EcosistemaManual.estado_conservacion | ✅ existe |
| proteccion_legal | Texto largo | Figura de reserva/parque/santuario (en los datos reales, "Parque Nacional Natural" para las 52 filas de IDEAM). | EcosistemaManual.proteccion_legal | ✅ existe |
| DOM_DIST_MGMT | Texto | Disturbio/manejo dominante — vocabulario oficial BADM/AmeriFlux (11 valores cerrados). | fila de `DisturbioManual` con `es_dominante=True` | ✅ resuelto — a diferencia de la misma columna en [plantilla-metadato-dato-biomasa.md](plantilla-metadato-dato-biomasa.md) (marcada ahí como sin confirmar), ya se verificó contra [el estándar BADM/AmeriFlux](../conocimiento/estandar-badm-ameriflux.md) y se documentó en [modelo-disturbio.md](modelo-disturbio.md) — mismo mapeo, se renombró `disturbio_dominante` en la plantilla de Flujos |
| Compartimentos | Texto | Reservorio de carbono que mide la unidad (para COS: "Carbono orgánico del suelo"). | UnidadMuestreo.compartimento | ✅ existe (`COMPARTIMENTO_CHOICES` ya incluye `carbono_organico_suelo`) |
| tipo_de_suelo | Texto | Mineral / Orgánico — tipo de suelo de la caracterización de muestreo. | ~~CaracterizacionMuestreoSuelo.tipo_de_suelo~~ | 🗑️ **deprecado y removido del modelo (2026-11-19)** — mismo dato que `Suelo IPCC`; no se mapea como columna propia, se resuelve con `ValorClasificacionTipo` |
| profundidad_perfil | Numérico (decimal) | Profundidad del perfil de suelo muestreado, en cm. | CaracterizacionMuestreoSuelo.profundidad_perfil | ✅ existe |
| intervalos_perfil | Numérico (decimal) | Tamaño de los intervalos de profundidad del perfil, en cm. | CaracterizacionMuestreoSuelo.intervalos_perfil | ✅ existe |
| monitoreo_macrofosiles | Sí/No | Si se monitorean macrofósiles en esta caracterización. | MonitoreoSuelo.activo (tipo_monitoreo=Macrofosiles) | ✅ existe |
| protocolo_macrofosiles | Texto | Protocolo usado para macrofósiles. | MonitoreoSuelo.protocolo (tipo_monitoreo=Macrofosiles) | ✅ existe |
| monitoreo_datacion | Sí/No | Si se monitorea datación en esta caracterización. | MonitoreoSuelo.activo (tipo_monitoreo=Datacion) | ✅ existe |
| protocolo_datacion | Texto | Protocolo usado para datación. | MonitoreoSuelo.protocolo (tipo_monitoreo=Datacion) | ✅ existe |
| monitoreo_densidad_aparente | Sí/No | Si se monitorea densidad aparente en esta caracterización. | MonitoreoSuelo.activo (tipo_monitoreo=Densidad_Aparente) | ✅ existe |
| protocolo_densidad_aparente | Texto | Protocolo usado para densidad aparente. | MonitoreoSuelo.protocolo (tipo_monitoreo=Densidad_Aparente) | ✅ existe |
| monitoreo_COS | Sí/No | Si se monitorea COS en esta caracterización. | MonitoreoSuelo.activo (tipo_monitoreo=COS) | ✅ existe |
| protocolo_cos | Texto | Protocolo de análisis de COS. | MonitoreoSuelo.protocolo (tipo_monitoreo=COS) | ✅ existe — `PROTOCOLO_COS_CHOICES`: Combustión seca, Pérdida por ignición (LOI), Oxidación húmeda (Walkley-Black) |

**Resumen:** de 41 columnas relevadas, 38 se mapean a un campo del modelo (reutilizando
lo construido para Flujos CO2/Biomasa más lo específico de suelo,
`CaracterizacionMuestreoSuelo`/`MonitoreoSuelo`), 2 no van como columna de Metadato
(`TEAM_MEMBER_NAME`/`TEAM_MEMBER_EMAIL`, se resuelven en la hoja "Responsables"), 1 se
excluye (`nombre_proyecto`) y 1 se deprecó por redundante (`tipo_de_suelo`, ver nota).

**Decisiones tomadas (2026-11-19):**

- **`Suelo IPCC` vs. `tipo_de_suelo`: es el mismo dato, reportado dos veces por el
  diseño original del esquema.** Según
  [¿Qué es la cobertura?](../conocimiento/que-es-la-cobertura.md), "Suelo IPCC" es la
  clasificación Mineral/Orgánico del suelo bajo el estándar IPCC — ya forma parte de
  la familia de catálogos de clasificación (`ClasificacionTipo`/
  `ValorClasificacionTipo`, misma familia que `cobertura_IPCC`/`CLC`/`IGBP`) que se usa
  en todas las metodologías, no es propio de COS. `CaracterizacionMuestreoSuelo.tipo_de_suelo`
  tiene exactamente los mismos dos valores (`Mineral`/`Organico`) y llegó así porque el
  modelo de suelo se importó tal cual de un diagrama externo (`colfux-db`, commit
  `9110b9c`, 2026-07-01) sin pasar por el catálogo genérico, que no existía en ese
  momento. **Se adopta `ValorClasificacionTipo` (tipo=Suelo_IPCC) como única fuente de
  verdad** — consistente con el resto de columnas de clasificación — y
  `CaracterizacionMuestreoSuelo.tipo_de_suelo` queda marcado para deprecar cuando se
  implemente (migración de datos + remover el campo, fuera de alcance de este
  documento).
- **`nombre_proyecto` se excluye** y **`TEAM_MEMBER_NAME`/`TEAM_MEMBER_EMAIL` van en
  hoja "Responsables"** — mismas decisiones ya tomadas para Flujos
  ([[ajustes-plantilla-flujos-co2-feedback-andrea]]), confirmadas por la usuaria para
  COS: la plantilla de descarga trae una hoja aparte "Responsables" (`FuenteDatos.proyecto`/
  `.institucion`/`.reportador`), igual que en `exportar_bronce` para Flujos.
- **Se quita "Fecha instalación unidad de muestreo" de la hoja Dato** (ver sección
  siguiente) — decisión de la usuaria, mismo criterio que Andrea Chaparro aplicó a
  Flujos.

**Nota de modelo — FK de `CaracterizacionMuestreoSuelo` (implementada, 2026-11-19):**
el modelo referenciaba `Sitio` directo (no `UnidadMuestreo`) y distinguía cada
caracterización dentro del sitio con un `muestreo_id` (entero simple, sin FK) — a
diferencia de Flujos/Biomasa, donde todo cuelga de `UnidadMuestreo`. No había ninguna
decisión de diseño documentada para esta diferencia: venía tal cual del diagrama
externo `colfux-db` importado en el commit `9110b9c` (2026-07-01), **antes** de que
existiera `UnidadMuestreo.codigo_metadato`/la convención de usar `UnidadMuestreo.nombre`
como identificador natural (eso se decidió el 2026-11-06, meses después) — era un
artefacto histórico, no una decisión deliberada.

Cruzando contra el Excel real se confirmó que `muestreo_id` **era el mismo dato** que
`UnidadMuestreo.nombre`: en "BD COS", la columna "No. unidad de muestreo" es constante
para cada `ID` (0 excepciones en 1795 filas / 50 `ID` distintos) y coincide exactamente
con el sufijo numérico del `codigo_metadatos` de "Metadatos COS" (ej.
`IDEAM_COS_NN Nevados_SanAntonioBInt_2` → unidad `2`). Es decir, `(Sitio, muestreo_id)`
identificaba lo mismo que `(Sitio, UnidadMuestreo.nombre)` — un cruce indirecto sobre
datos redundantes, no dos conceptos distintos.

**Implementado:** se reemplazó `CaracterizacionMuestreoSuelo.sitio` + `.muestreo_id` por
una FK directa `unidad_muestreo = FK(UnidadMuestreo)`, igual al patrón que ya usan
`SubmuestraSuelo` y `MonitoreoParcela` (migración
`backend/app/migrations/0130_caracterizacion_suelo_fk_unidad_muestreo.py`). Como la
tabla estaba vacía en el contenedor compartido, no hizo falta migración de datos. Se
depreció `tipo_de_suelo` en la misma migración: el tipo de suelo se sigue resolviendo
con `ValorClasificacionTipo`/`CoberturaManual` (tipo=Suelo_IPCC), ver más arriba.

## Hoja "COS - Dato" (propuesta)

A diferencia de Biomasa (dos niveles de granularidad en una fila), el Excel real de
COS es análogo a Flujos: **una fila por toma de muestra**, acá por unidad de muestreo +
intervalo de profundidad — mapea 1:1 a `SubmuestraSuelo`.

| Campo (Excel) | Tipo de dato | Descripción | Entidad.atributo | Estado |
|---|---|---|---|---|
| ID | Texto | Identificador de la unidad de muestreo (ej. `IDEAM_COS_NN Nevados_SanAntonioBInt_2`). Llave de referencia hacia la fila de Metadato. | UnidadMuestreo.codigo_metadato | ✅ existe |
| No. unidad de muestreo | Numérico (entero) | Número de la unidad de muestreo (ej. `2`). | UnidadMuestreo.nombre | ✅ existe |
| ~~Fecha instalación unidad de muestreo~~ | ~~Fecha~~ | **Se quita de la plantilla** (decisión de la usuaria, 2026-11-19): en los datos reales el valor cambia entre intervalos de profundidad de la misma unidad (ej. 2019-10-24 para 0-10 cm y 2019-10-22 para 10-20 cm) — no puede ser fecha de instalación (fija por unidad), es en realidad la fecha de la toma (`SubmuestraSuelo.fecha`, ya cubierta sin necesidad de esta columna mal rotulada). Mismo criterio que Andrea Chaparro aplicó a Flujos ([[ajustes-plantilla-flujos-co2-feedback-andrea]]). | — | 🚫 excluida |
| Volumen del barreno | Texto/numérico | Identificador o volumen del barreno/cilindro usado para la toma. En los datos reales, siempre vacío. | SubmuestraSuelo.barreno_vol | ✅ existe |
| Profundidad cm | Texto (rango, ej. "0-10") | Intervalo de profundidad muestreado. | SubmuestraSuelo.profundidad_desde_cm / profundidad_hasta_cm | ✅ existe, pero requiere **parsear** el rango de texto ("0-10") en los dos campos numéricos del modelo — no es una columna 1:1 |
| Densidad Aparente g/cm3 | Numérico (decimal) | Densidad aparente de la muestra. | SubmuestraSuelo.densidad_aparente_g_cm3 | ✅ existe |
| % carbono | Numérico (decimal) | Porcentaje de carbono orgánico medido. | SubmuestraSuelo.carbono_pct | ✅ existe |
| SOIL_CHEM_C_ORG | Numérico (decimal) | Carbono orgánico del suelo reportado por la fuente (vocabulario BADM/AmeriFlux). En los datos reales, siempre vacío. | SubmuestraSuelo.soil_chem_c_org | ✅ existe |
| Medida de error COS (SD;EE;U%) | Texto | Error asociado reportado por la fuente (desviación estándar, error estándar o incertidumbre). | SubmuestraSuelo.medida_error | ✅ existe |
| Metodología Tipo de muestreo | Texto | Tipo de muestreo de suelos usado. | SubmuestraSuelo.metodologia_tipo_muestreo | ✅ existe |
| Metodología Muestreo de suelos-Distancia (m) | Numérico (decimal) | Distancia del punto de muestreo. | SubmuestraSuelo.metodologia_distancia_m | ✅ existe |
| Metodología Muestreo de suelos-Azimut (°) | Numérico (decimal) | Azimut del punto de muestreo. | SubmuestraSuelo.metodologia_azimut | ✅ existe |
| Metodología Metodos de análisis | Texto | Método de análisis de laboratorio usado. | SubmuestraSuelo.metodologia_analisis | ✅ existe |

**Resumen:** de las 13 columnas relevadas, 12 quedan en la plantilla y ya tienen campo
en el modelo; 1 (`Fecha instalación unidad de muestreo`) se excluye por estar mal
rotulada (ver tabla). El único trabajo real pendiente es parsear "Profundidad cm"
(texto tipo rango) en `profundidad_desde_cm`/`profundidad_hasta_cm`.

## Preguntas resueltas (2026-11-19)

Las 4 preguntas originales quedaron resueltas con la usuaria; se documentan acá para
trazabilidad (detalle de cada una en las notas de las secciones de arriba):

1. **`Suelo IPCC` vs. `tipo_de_suelo`: mismo dato, redundante.** Se adopta
   `ValorClasificacionTipo` (tipo=Suelo_IPCC) como fuente de verdad;
   `CaracterizacionMuestreoSuelo.tipo_de_suelo` queda para deprecar.
2. **Por qué `CaracterizacionMuestreoSuelo` no tiene FK a `UnidadMuestreo`: artefacto
   histórico, no decisión deliberada.** El modelo viene del diagrama externo
   `colfux-db` importado el 2026-07-01 (commit `9110b9c`), antes de que existiera la
   convención de `UnidadMuestreo.nombre`/`codigo_metadato` como identificador natural
   (decidida el 2026-11-06). Cruzando el Excel real se confirma que `muestreo_id` es
   el mismo dato que `UnidadMuestreo.nombre` (coincide 1:1 con el sufijo de
   `codigo_metadatos` en las 50 unidades relevadas) — se recomienda agregar la FK
   directa cuando se implemente.
3. **"Fecha instalación unidad de muestreo" en la hoja Dato: se quita.** Decisión de
   la usuaria — la columna está mal rotulada (en los datos reales varía por
   profundidad, es fecha de toma, no de instalación).
4. **Sí, aplican a COS las mismas decisiones de Flujos:** excluir `nombre_proyecto`,
   mover `TEAM_MEMBER_*` a la hoja "Responsables", quitar fecha de instalación mal
   rotulada.

## Prueba de carga real (2026-11-24)

Se transformó `context/data/Metadatos y BD COS.xlsx` al formato exacto de la
plantilla descargable (`context/data/COS_plantilla_transformada.xlsx`, hojas "COS
Metadato" 50 filas / "COS Dato" 1795 filas) y se probó contra el backend real:
upload → mapeo automático → capa bronce → intento de promoción a los modelos
estructurados. El mapeo automático se comportó como lo documentado (13/13 en Dato,
23/37 en Metadato). La promoción encontró dos problemas:

1. **Resuelto.** `UnidadMuestreo.tipo` (FK a `UnidadMuestreoTipo`) y
   `.unidad_experimental` son obligatorios en el modelo, pero `cos_metadato` no
   traía ninguna columna para resolverlos (a diferencia de `biomasa_metadato`, que
   sí expone `tipo_unidad_muestreo`/`nombre_unidad_experimental`) — bloqueaba el
   100% de las filas. Se agregaron ambas columnas a `cos_metadato`
   (`backend/app/api/etl/views.py`): `UnidadMuestreoTipo` y `UnidadExperimental` a
   la cadena/campos, más las 2 columnas en
   `_ORDEN_COLUMNAS_METADATO_COS_PLANTILLA`. Decisión tomada con la usuaria sin
   dato real que la respalde en el Excel de IDEAM (no distingue unidad
   experimental de unidad de muestreo, ni trae un tipo): `nombre_unidad_experimental`
   = mismo valor que `codigo_metadato` (una unidad experimental por
   codigo_metadato); `tipo_unidad_muestreo` sin un valor claro del catálogo
   (`conglomerado`/`parcela`/`plot`/`transecto`) — se usó `"parcela"` en el archivo
   de prueba, **pendiente de confirmar con el equipo de datos**.
2. **Resuelto, sin tocar el motor.** `Vereda.codigo_dane` (`backend/app/models/geo.py`)
   es `unique=True` sin valor por defecto, pero ninguna plantilla de metodología
   (Flujos/Biomasa/COS) trae ese código — solo el nombre de la vereda, que en los
   datos reales de COS viene vacío para las 50 unidades. El importador genérico
   (`_procesar_filas`, vía el camino "genérico" de `_CAMPOS_IDENTIDAD` sin entrada
   para `Vereda`) intentaba crear una `Vereda` nueva por cada combinación de FK
   auto-vinculada (`municipio`) sin código DANE; la segunda vereda distinta de la
   carga chocaba contra la primera (`codigo_dane=''` repetido, violación del
   `unique`). Decisión de la usuaria (2026-11-24, "por ahora no subamos ni
   municipio, region ni vereda"): se sacan `Vereda`/`Municipio`/`Departamento`/
   `Region` de la `cadena` de `cos_metadato` por completo (`Sitio.vereda` es
   nullable, así que simplemente queda sin resolver) — sin tocar el modelo ni el
   motor genérico. `biomasa_metadato` expone la misma columna `Vereda.nombre` y en
   teoría tiene el mismo problema latente si sus datos reales llegan a tocar más de
   un municipio; queda sin tocar, pendiente de evaluar si conviene el mismo ajuste.
3. **Resuelto.** Al promover sin el bloqueo de Vereda apareció
   `IntegrityError: null value in column "tipo_id"` creando `UnidadMuestreo` desde
   la hoja "COS Dato". Causa: esa hoja mapeaba `UnidadMuestreo.nombre` además de
   `codigo_metadato` (alias "No. unidad de muestreo"), y como "COS Metadato" nunca
   mapeaba `nombre` (quedaba `''` en la fila creada ahí), el filtro de búsqueda
   `get_or_create(nombre=..., codigo_metadato=...)` de "COS Dato" no encontraba la
   unidad ya creada e intentaba crear una nueva sin `tipo` (obligatorio) → explota.
   `biomasa_dato` no tiene este problema porque solo mapea `codigo_metadato` (sin
   `nombre`) en su hoja Dato — el `get_or_create` de un solo campo matchea directo
   contra lo creado en Metadato. **Fix**: se sacó `nombre` del mapeo de
   `UnidadMuestreo` en `cos_dato`, mismo patrón que `biomasa_dato`. Se pierde la
   columna "No. unidad de muestreo" de la hoja Dato (el dato no se guarda), a
   cambio de no tocar el motor genérico compartido.
4. **Resuelto.** Con "COS Dato" promoviendo limpio, "COS Metadato" seguía
   bloqueada por 4 columnas en el archivo transformado: `sistema_referencia` tenía
   el valor "EPSG:4326" (con `:`) en vez de la choice real del modelo
   (`SistemaReferencia.EPSG_4326`, con `_`); `tipo_localizacion` tenía la etiqueta
   humana "Localización exacta" en vez de la choice `"exacta"`
   (`Sitio.TIPO_LOCALIZACION_CHOICES`) — ambos eran errores de la transformación
   del archivo de prueba, corregidos ahí sin tocar backend. Las otras dos,
   `disturbio_dominante` (`DisturbioManual.es_dominante`) y `ecosistema_IDEAM`
   (`ValorClasificacionEcosistema.valor`), venían obligatorias en el modelo pero
   vacías en las 50 filas reales de IDEAM (mismo patrón que Vereda: el dato
   simplemente no existe en la fuente). Decisión de la usuaria (2026-11-24, "los
   valores de disturbio deberían ser opcionales para todos"): se marcan
   `blank=True` en ambos campos del modelo (migraciones `0132_alter_disturbiomanual_es_dominante`,
   `0133_alter_valorclasificacionecosistema_valor`) — cambio válido para todas las
   metodologías que comparten estos modelos, no solo COS.
5. **Resuelto.** Último bloqueo: "COS Metadato" no mapeaba `UnidadMuestreo.nombre`
   en absoluto (ni columna ni atributo manual), y el validador
   `_validar_obligatorios_unidad_muestreo` lo exige siempre. Decisión de la
   usuaria (2026-11-24): se agrega `UnidadMuestreo.nombre` a `cos_metadato`, alias
   `nombre_unidad_muestreo`, con el mismo valor que `codigo_metadato` (mismo
   criterio ya usado para `nombre_unidad_experimental`) — columna nueva copiada en
   el archivo transformado, no existe en el Excel fuente de IDEAM.

Con los 5 ajustes aplicados se repitió la prueba completa (upload → mapeo
automático → bronce → promoción) sobre el mismo archivo transformado:
**`"hojas_bloqueadas": [], "filas_promovidas": 1845`** — las 50 filas de "COS
Metadato" y las 1795 de "COS Dato" promovieron sin error. Por decisión de la
usuaria esos datos de prueba quedaron en la base (no se revirtieron) y se habilitó
`subidaDisponible: true` para COS en `Participacion.tsx`.

Quedan pendientes de validar con el equipo de datos (no bloquean la carga):
el valor real de `tipo_unidad_muestreo` (hoy `"parcela"` fijo sin confirmar) y, en
general, las decisiones de esta sesión y la anterior (FK nueva, deprecación de
`tipo_de_suelo`, no subir Vereda/Municipio/Departamento/Region por ahora).

## Referencias

- `context/data/Metadatos y BD COS.xlsx` — hojas "Metadatos COS" (metadato propuesto,
  41 columnas, 52 filas IDEAM) y "BD COS" (dato propuesto, 13 columnas, 1795 filas).
- `backend/app/models/suelo.py` — `CaracterizacionMuestreoSuelo`, `MonitoreoSuelo`, `SubmuestraSuelo`.
- `backend/app/models/sitio.py` — `Sitio`, `UnidadMuestreo`, `UnidadExperimental`.
- `backend/app/api/etl/views.py` — `_VISTAS_DESNORMALIZADAS["cos"]`, `_CAMPOS_METODOLOGIA`, `_ORDEN_COLUMNAS_METODOLOGIA`.
- [plantilla-metadato-dato-co2-camaras.md](plantilla-metadato-dato-co2-camaras.md) — mismo ejercicio para Flujos, modelo a seguir.
- [plantilla-metadato-dato-biomasa.md](plantilla-metadato-dato-biomasa.md) — mismo ejercicio para Biomasa, hecho en esta misma sesión.
- [modelo-disturbio.md](modelo-disturbio.md) — resolución de `DOM_DIST_MGMT`.
- [El estándar BADM/AmeriFlux](../conocimiento/estandar-badm-ameriflux.md)
- [[plantilla-metadato-dato-cos]] (tarea)
- [[subida-descarga-formato-metadato-dato-por-metodologia]]
