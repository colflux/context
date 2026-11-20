# Plantilla de carga/descarga: metadato y dato de MOM (materia orgánica muerta)

Diccionario de datos reconstruido a partir del Excel real de la fuente IDEAM
(`data/MOM.xlsx`, hojas "Metadatos MOM" y "BD MOM" — las otras tres hojas del
archivo, "Hoja1"/"BMORI sin Duplicados"/"MOM ORI sin duplicados", son datos de
trabajo/duplicados de la fuente, no la estructura de la plantilla), mapeado
contra el modelo de datos actual (`backend/app/models/mom.py` —
`MuestraMOM` — y las entidades compartidas de `UnidadMuestreo`/`Sitio` que ya
usa Flujos CO2). Igual que [Flujos CO2](plantilla-metadato-dato-co2-camaras.md)
y Biomasa/COS, MOM ya tiene sus propias vistas `mom_metadato`/`mom_dato` en
`_HOJAS_PLANTILLA` (`backend/app/api/etl/views.py`, implementado
2026-11-19) — los 3 entregables (plantilla descargable, modal "Ver detalle",
mapeo automático) están activos en `/participacion`.

## Hoja "Metadatos MOM" (metadato)

49 columnas en el Excel original. `Site`/`sitio` y `codigo_metadatos`/`ID` son
las llaves que unen esta hoja con "BD MOM" (equivalente a `codigo_metadato` en
Flujos Metadato/Dato).

| Campo (Excel) | Tipo de dato | Entidad.atributo (Modelo de Datos COLFLUX) | Notas |
|---|---|---|---|
| nombre_proyecto | Texto | Proyecto.nombre | Excluida de la hoja "MOM Metadato" implementada (`mom_metadato`): mismo criterio ya aplicado a Flujos/Biomasa, `Proyecto` solo queda en la cadena para el join, no como columna. |
| TEAM_MEMBER_NAME | Texto | — sin campo en el modelo | Mismo gap ya documentado en Flujos CO2: no existe "quién reportó" en el modelo actual. |
| TEAM_MEMBER_EMAIL | Texto | — sin campo en el modelo | Idem. |
| codigo_metadatos | Texto | UnidadMuestreo.codigo_metadato | Llave hacia "BD MOM" (columna `ID`). |
| region_natural | Texto | Region.nombre | |
| departamento | Texto | Departamento.nombre | |
| Municipio | Texto | Municipio.nombre | |
| Vereda | Texto | Vereda.nombre | |
| sitio | Texto | Sitio.nombre | Llave hacia "BD MOM" (columna `Site`). |
| Tipo de localización | Texto | Sitio.tipo_localizacion | Choices: Localización exacta, Aproximada a nivel de vereda/municipio, Inferida. |
| latitud | Numérico (decimal) | Sitio.latitud | |
| longitud | Numérico (decimal) | Sitio.longitud | |
| sistema_referencia | Texto | SistemaReferencia.nombre | |
| altitud | Numérico (decimal) | Sitio.altitud | |
| pendiente | Texto | Sitio.pendiente | |
| topografia | Texto | Sitio.topografia | |
| Ecosistema / Cobertura | Texto | EcosistemaManual.valor (ValorClasificacionEcosistema, sistema IDEAM) | Columna combinada/ambigua en el Excel original — igual que las 16 columnas ambiguas de Flujos (ver `mapeo-automatico-plantilla-flujos-co2.md`), necesita desambiguar si es ecosistema o cobertura antes de mapear. |
| cobertura_IPCC | Texto | ValorClasificacionTipo.valor (ClasificacionTipo=IPCC) | |
| cobertura_CLC | Texto | ValorClasificacionTipo.valor (ClasificacionTipo=CLC) | |
| cobertura_IGBP | Texto | ValorClasificacionTipo.valor (ClasificacionTipo=IGBP) | |
| cobertura_nom_comun | Texto | ValorClasificacionTipo.valor (ClasificacionTipo=Coloquial) | Equivalente a `cobertura_Nombre_Local` en Flujos. |
| Suelo IPCC | Texto | ValorClasificacionTipo.valor (ClasificacionTipo=Suelo_IPCC) | Choices: Mineral, Organico. |
| tipo_disturbio | Texto | ValorClasificacionTipo.valor (ClasificacionTipo=Disturbio) | |
| anios_disturbio | Numérico (entero) | DisturbioManual.anios_disturbio | |
| anios_desde_fin_disturbio | Numérico (entero) | DisturbioManual.anios_desde_fin | |
| uso_actual | Texto | Sitio.uso_actual | |
| Estado conservación | Texto | EcosistemaManual.estado_conservacion | |
| proteccion_legal | Texto largo | EcosistemaManual.proteccion_legal | |
| DOM_DIST_MGMT | Sí/No | DisturbioManual.es_dominante | Confirmado: mismo atributo que `disturbio_dominante` en Flujos Metadato ("Si es el disturbio/manejo principal reportado para la unidad de muestreo, cuando hay varios registrados") — ya resuelto ahí, acá es solo un nombre de columna distinto para el mismo campo. |
| Tipo muestreo | Texto | UnidadMuestreo.tipo_muestreo | Choices: Probabilístico, No probabilístico. |
| Tipo unidad de muestreo | Texto | UnidadMuestreoTipo.nombre | |
| Tamaño unidad de muestreo (área en cm2) | Numérico (decimal) | Parcela.area | Confirmado: corresponde a la parcela, no a `UnidadMuestreo.area_cm2` (ese campo es específico de cámaras de gases, derivado de `diametro_anillo_cm`, que no existe en MOM). **Ojo con la unidad:** el Excel la nombra "área en cm2" pero `Parcela.area` está en m² (`_calcular_area()`, `backend/app/models/sitio.py`) — a validar si es un error de rótulo en la fuente o si hace falta una conversión en el importador. |
| Forma unidad de muestreo | Texto | Parcela.forma | Choices: Cuadrada, Rectangular, Circular. |
| Periodicidad de muestreo | Texto | — sin campo en el modelo | Mismo gap pendiente que "Periodicidad de muestreo" de Flujos (ver backlog 2026-11-06); también excluida de `mom_metadato` por falta de campo. |
| monitoreo_biomasa_aerea | Sí/No | MonitoreoParcela.activo (tipo_monitoreo=Biomasa_Aerea) | |
| protocolo_biomasa_aerea | Texto | MonitoreoParcela.protocolo (tipo_monitoreo=Biomasa_Aerea) | Choices: Alometría destructiva/no destructiva, LiDAR terrestre/aerotransportado. |
| monitoreo_biomasa_subterranea | Sí/No | MonitoreoParcela.activo (tipo_monitoreo=Biomasa_Subterranea) | |
| protocolo_biomasa_subterranea | Texto | MonitoreoParcela.protocolo (tipo_monitoreo=Biomasa_Subterranea) | |
| monitoreo_flora | Sí/No | MonitoreoParcela.activo (tipo_monitoreo=Flora) | |
| protocolo_flora | Texto | MonitoreoParcela.protocolo (tipo_monitoreo=Flora) | |
| monitoreo_rasgos_funcionales | Sí/No | MonitoreoParcela.activo (tipo_monitoreo=Rasgos_Funcionales) | |
| protocolo_rasgos_funcionales | Texto | MonitoreoParcela.protocolo (tipo_monitoreo=Rasgos_Funcionales) | |
| cobertura_vegetal_primaria | Texto | CoberturaManual.valor (tipo=Vegetacion_funcional, orden_dominancia=Primaria) | No está en el Excel original (hueco de columna real entre `protocolo_rasgos_funcionales` y `cobertura_vegetal_terciaria`, confirmado leyendo el `.xlsx`) — se agrega acá por paralelismo con Flujos Metadato, que sí trae las 3 (primaria/secundaria/terciaria). Si se implementa, agregarla a la plantilla de descarga de MOM aunque la fuente IDEAM no la haya traído en este archivo puntual. |
| porcentaje_cob_veg_prim | Numérico (decimal) | CoberturaManual.porcentaje (orden_dominancia=Primaria) | Idem — agregada por paralelismo con Flujos. |
| cobertura_vegetal_secundaria | Texto | CoberturaManual.valor (tipo=Vegetacion_funcional, orden_dominancia=Secundaria) | Idem. |
| porcentaje_cob_veg_sec | Numérico (decimal) | CoberturaManual.porcentaje (orden_dominancia=Secundaria) | Idem. |
| cobertura_vegetal_terciaria | Texto | CoberturaManual.valor (tipo=Vegetacion_funcional, orden_dominancia=Terciaria) | Única de las 3 que sí trae el Excel original. |
| porcentaje_cob_veg_ter | Numérico (decimal) | CoberturaManual.porcentaje (orden_dominancia=Terciaria) | |
| distancia_drenaje | Numérico (decimal) | ExposicionExterna.distancia_m (fuente=Drenaje) | |
| distancia_fuego | Numérico (decimal) | ExposicionExterna.distancia_m (fuente=Fuego) | |
| distancia_pastoreo | Numérico (decimal) | ExposicionExterna.distancia_m (fuente=Pastoreo) | |
| distancia_cultivo | Numérico (decimal) | ExposicionExterna.distancia_m (fuente=Cultivo) | |

## Hoja "BD MOM" (dato)

21 columnas, una fila por unidad de muestreo (no hay granularidad temporal
submuestreada como en Flujos — `MuestraMOM` no tiene equivalente a
`SubmuestraGEI`).

| Campo (Excel) | Tipo de dato | Entidad.atributo (Modelo de Datos COLFLUX) | Notas |
|---|---|---|---|
| ID | Texto | UnidadMuestreo.codigo_metadato | Llave hacia "Metadatos MOM" (`codigo_metadatos`). |
| # Unidad de Muestre | Texto | UnidadMuestreo.nombre | |
| Fecha instalación unidad de muestreo | Fecha | UnidadMuestreo.fecha_instalacion | No es `MuestraMOM.fecha` (fecha de la medición) — ver nota abajo. |
| Site | Texto | Sitio.nombre | Llave hacia "Metadatos MOM" (`sitio`). |
| Contenido de Carbono MOM valor reportado | Numérico (decimal) | MuestraMOM.carbono_mom_valor_reportado | |
| Contenido de Carbono en MOM total (tC/ha) | Numérico (decimal) | MuestraMOM.carbono_mom_tc_ha | |
| Medida de error MOM (SD;EE;U%) | Texto | MuestraMOM.error_mom | |
| Contenido de Carbono en Árboles Muertos en Pie (AMP) Y Tocones Muertos (TM) (tC/ha) | Numérico (decimal) | MuestraMOM.carbono_amp_tm_tc_ha | |
| Medida de error AMP_TM (SD;EE;U%) | Texto | MuestraMOM.error_amp_tm | |
| Contenido de Carbono en Detritos Finos de Madera (DFM) (tC/ha) | Numérico (decimal) | MuestraMOM.carbono_dfm_tc_ha | |
| Medida de error DFM (SD;EE;U%) | Texto | MuestraMOM.error_dfm | |
| Contenido de Carbono en Detritos Gruesos de Madera (DGM) (tC/ha) | Numérico (decimal) | MuestraMOM.carbono_dgm_tc_ha | |
| Medida de error DGM (SD;EE;U%) | Texto | MuestraMOM.error_dgm | |
| Contenido de Carbono en Hojarasca (g/m2) | Numérico (decimal) | MuestraMOM.carbono_hojarasca_g_m2 | |
| Contenido de Carbono en Hojarasca (tC/ha) | Numérico (decimal) | MuestraMOM.carbono_hojarasca_tc_ha | |
| Medida de error (SD;EE;U%)23 | Texto | MuestraMOM.error_hojarasca | El "23" en el nombre viene del Excel original (probable resto de autollenado de Excel al duplicar la columna de error anterior), no es parte del dato — confirmar con la fuente, pero mapea por posición/contexto a error de hojarasca. |
| Metodología Muestreo MOM | Texto | MuestraMOM.metodologia_muestreo_mom | |
| Metodología Muestreo DFM-DGM | Texto | MuestraMOM.metodologia_muestreo_dfm_dgm | |
| Metodología Tamaño | Texto | MuestraMOM.metodologia_tamano | |
| Metodología AMP y TO | Texto | MuestraMOM.metodologia_amp_to | |
| Metodología Hojasrasca | Texto | MuestraMOM.metodologia_hojarasca | |

**`MuestraMOM.fecha`** (fecha de la medición, distinta de la fecha de
instalación de la unidad) existe en el modelo pero no tiene columna
equivalente en este Excel — mismo tipo de gap que `TEAM_MEMBER_NAME`/
`TEAM_MEMBER_EMAIL` en Metadatos, solo que en la dirección contraria (campo
de sobra en el modelo, no columna de sobra en la fuente).

## Comparación con Flujos CO2 — qué se puede reusar tal cual

La mayoría de los campos de "Metadatos MOM" son **exactamente los mismos**
atributos de `Sitio`/`UnidadMuestreo`/`EcosistemaManual`/`CoberturaManual`/
`DisturbioManual`/`ExposicionExterna` que ya usa la hoja "Flujos Metadato"
(ver [plantilla-metadato-dato-co2-camaras.md](plantilla-metadato-dato-co2-camaras.md)) —
tiene sentido: son atributos de la unidad de muestreo/sitio, no de la
metodología de medición. Lo específico de MOM es solo la hoja de dato
(`MuestraMOM`) y la sección "Diseño" de monitoreo (`MonitoreoParcela`,
sin equivalente en Flujos porque las cámaras GEI no tienen ese concepto).

Implementado (2026-11-19): `mom_metadato`/`mom_dato` en
`_VISTAS_DESNORMALIZADAS`, con sus propios
`_ORDEN_COLUMNAS_METADATO_MOM_PLANTILLA`/`_ORDEN_COLUMNAS_DATO_MOM_PLANTILLA`
y registradas en `_HOJAS_PLANTILLA` (`backend/app/api/etl/views.py`), mismo
patrón que `biomasa_metadato`/`biomasa_dato` y `cos_metadato`/`cos_dato`. A
diferencia de Biomasa/COS, MOM sí incluye `DOM_DIST_MGMT`
(`DisturbioManual.es_dominante`) y los 4 pares `monitoreo_*`/`protocolo_*`
(`MonitoreoParcela`, FK inversa desde `UnidadMuestreo`, mismo tratamiento de
"columna fija de pivoteo" que `MonitoreoSuelo` en COS —
`_COLUMNAS_PIVOTE_METADATO_MOM_MONITOREO`). La plantilla descargable trae 51
columnas en "MOM Metadato" y 21 en "MOM Dato".

## Pendiente antes de dar este mapeo por cerrado

Resuelto con la usuaria (2026-11-19): `DOM_DIST_MGMT` = `disturbio_dominante`
de Flujos (mismo campo, `DisturbioManual.es_dominante`); se agregan
`cobertura_vegetal_primaria`/`secundaria` (ver arriba); `Tamaño unidad de
muestreo` corresponde a `Parcela.area`, no a `UnidadMuestreo.area_cm2`.

Queda pendiente:

- Validar con Andrea/equipo de datos las decisiones tomadas sin preguntar al
  implementar (exclusión de `nombre_proyecto`/"Periodicidad de muestreo",
  mismo criterio que Flujos/Biomasa).
- Decidir, igual que se hizo para Flujos, qué columnas quedan "ambiguas"
  (ej. "Ecosistema / Cobertura", y en general cualquier columna que comparta
  `modelo.campo` con otra — `ValorClasificacionTipo.valor`,
  `MonitoreoParcela.activo`/`protocolo`, `CoberturaManual.porcentaje`,
  `ExposicionExterna.distancia_m`) y necesitan un selector de desambiguación
  en el momento de mapear/promover, no de cargar a bronce — el mapeo
  automático (`_sugerir_mapeos_automaticos`) ya las detecta y las deja para
  el asistente manual, mismo comportamiento que Flujos/Biomasa/COS.
- Confirmar la discrepancia de unidad en `Tamaño unidad de muestreo (área en
  cm2)` vs. `Parcela.area` (m²) — ver nota en la tabla.
- Probar con el archivo real `context/data/MOM.xlsx` subido tal cual (hoy
  solo se probó con encabezados generados por la propia plantilla).
- Extender el resto del motor de bronce/staging (`FilaBronce`/`CeldaBronce`,
  ya genérico por diseño — ver
  `tasks/inprogress/rediseno-carga-flujos-co2-staging-bronce.md`) a MOM si
  hace falta más allá de lo ya cubierto por el mapeo automático.

## Referencias

- `backend/app/models/mom.py` — `MuestraMOM`.
- `backend/app/models/sitio.py` — `Sitio`, `UnidadMuestreo`, `UnidadExperimental`, `UnidadMuestreoTipo`, `Parcela`, `MonitoreoParcela`.
- `backend/app/models/cobertura.py` — `CoberturaManual`, `DisturbioManual`, `FuenteExterna`, `ExposicionExterna`.
- `backend/app/models/ecosistema.py` — `EcosistemaManual`, `ValorClasificacionEcosistema`.
- `backend/app/models/clasificacion.py` — `ClasificacionTipo`, `ValorClasificacionTipo`.
- `backend/app/models/geo.py` — `Region`, `Departamento`, `Municipio`, `Vereda`, `SistemaReferencia`.
- [Plantilla de carga/descarga: metadato y dato de CO2/CH4 (cámaras GEI)](plantilla-metadato-dato-co2-camaras.md) — mismo ejercicio, metodología hermana.
- [Rediseñar vista de subida/descarga: separar metadato y dato por metodología](../../tasks/backlog/subida-descarga-formato-metadato-dato-por-metodologia.md) — MOM queda pendiente ahí, este documento es insumo para retomarla.
- `data/MOM.xlsx` — archivo fuente analizado (hojas "Metadatos MOM" y "BD MOM").
