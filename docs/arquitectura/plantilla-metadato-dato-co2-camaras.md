# Plantilla de carga/descarga: metadato y dato de CO2/CH4/N2O (cámaras GEI)

Diccionario de datos de la plantilla descargable de Flujos CO2 (metodología de
cámaras de gases manuales — `MuestraGEI`/`SubmuestraGEI`/`MuestraAmbiental` en
`backend/app/models/co2.py`), generado desde `_hojas_plantilla_vacia()` /
`_dataframe_diccionario_datos()` en `backend/app/api/etl/views.py` — misma fuente
que usan la hoja "Diccionario de datos" del Excel y el modal "Ver detalle de la
plantilla" en `/participacion`.

## Hoja "Flujos CO2 - Metadato"

| Campo | Tipo de dato | Descripción | Entidad.atributo (Modelo de Datos COLFLUX) | Valores permitidos (si aplica) |
|---|---|---|---|---|
| codigo_metadato | Texto | Identificador de la unidad de muestreo en el sistema de metadatos externo de la fuente, si lo trae. | UnidadMuestreo.codigo_metadato | |
| nombre_unidad_experimental | Texto | Nombre de la unidad experimental (agrupa las unidades de muestreo que reciben el mismo tratamiento). | UnidadExperimental.nombre | |
| descripcion_unidad_experimental | Texto largo | Notas adicionales sobre la unidad experimental. | UnidadExperimental.descripcion | |
| nombre_unidad_muestreo | Texto | Identificador de la unidad de muestreo tal como lo reporta la fuente (ej. el número o código de la parcela/punto). | UnidadMuestreo.nombre | |
| latitud | Numérico (decimal) | Latitud del sitio en grados decimales (WGS84). Fuente de verdad editable; de aquí se deriva la geometría del punto (geom). | Sitio.latitud | |
| longitud | Numérico (decimal) | Longitud del sitio en grados decimales (WGS84). Fuente de verdad editable; de aquí se deriva la geometría del punto (geom). | Sitio.longitud | |
| sistema_referencia | Texto | Sistema de referencia de coordenadas en el que están expresadas latitud/longitud del sitio. | SistemaReferencia.nombre | EPSG:4326 — WGS84, EPSG:4686 — MAGNA-SIRGAS, EPSG:4674 — SIRGAS2000, Otro |
| tipo_localizacion | Texto | Precisión espacial con la que se dispone la ubicación del sitio. | Sitio.tipo_localizacion | Localización exacta, Aproximada a nivel de vereda (centroide DANE), Aproximada a nivel de municipio (centroide IGAC), Inferida (sin coordenadas ni vereda/municipio de referencia) |
| altitud_msnm | Numérico (decimal) | Altitud del sitio sobre el nivel del mar, en metros. | Sitio.altitud | |
| pendiente | Texto | Categoría de pendiente del terreno en el sitio. | Sitio.pendiente | Plano, Ondulado / variable, Valle / fondo, Pendiente suave (<2%), Pendiente media (2–5%), Pendiente significativa (5–10%), Pendiente fuerte (>10%), Cresta / cima |
| topografia | Texto | Posición topográfica del sitio (cresta, ladera, valle, etc.). | Sitio.topografia | Cresta / cima, Ladera superior, Ladera media, Ladera inferior, Valle / fondo, Plano |
| tipo_muestreo | Texto | Si la unidad de muestreo fue seleccionada con un método probabilístico o no. | UnidadMuestreo.tipo_muestreo | Probabilístico, No probabilístico |
| tipo_unidad_muestreo | Texto | Nombre del tipo de unidad de muestreo (ej. parcela, transecto, conglomerado, plot). | UnidadMuestreoTipo.nombre | |
| forma_unidad_muestreo | Texto | Forma geométrica de la parcela/unidad de muestreo, usada para calcular su área. | Parcela.forma | Cuadrada, Rectangular, Circular |
| tamano_unidad_muestreo_cm2 | Numérico (decimal) | Área del anillo/cámara de muestreo, calculada automáticamente a partir de diametro_anillo_cm. | UnidadMuestreo.area_cm2 | |
| microtopografia | Texto | Rasgo de microtopografía del terreno en la unidad de muestreo (ej. Hummock, Hollow, Pool, Lawns, Ditch). | Microtopografia.nombre | |
| diametro_anillo | Numérico (decimal) | Diámetro del anillo/cámara de muestreo de gases, en centímetros. De acá se deriva area_cm2. | UnidadMuestreo.diametro_anillo_cm | |
| pozo_nivel_freatico | Sí/No | Si existe infraestructura (pozo/piezómetro) para medir el nivel freático en esta unidad. El valor de la medición en sí vive en MuestraAmbiental.water_level. | UnidadMuestreo.tiene_pozo_nivel_freatico | |
| tratamiento | Texto | Condición experimental que describe esta unidad (ej. "con pastoreo" vs. "control"), distinta del nombre/descripción. | UnidadExperimental.tratamiento | |
| intervenido | Sí/No | Si el sitio ha sido intervenido/alterado por actividad humana. | Sitio.intervenido | |
| propiedad_tierra | Texto | Si la tierra del sitio es de propiedad pública o privada. | Sitio.propiedad_tierra | Pública, Privada |
| uso_actual | Texto | Uso actual del suelo en el sitio. | Sitio.uso_actual | Bosque primario, Bosque secundario, Plantación forestal, Agricultura intensiva, Agricultura tradicional, Pastura, Humedal natural, Humedal intervenido, Área protegida, Sistema agroforestal, Abandonado, Restauración activa |
| proteccion_legal | Texto largo | Si el sitio está bajo alguna figura de reserva, parque, santuario, etc. | EcosistemaManual.proteccion_legal | |
| tipo_disturbio | Texto | Sistema de clasificación: Disturbio. | ValorClasificacionTipo.valor | Agricultura, Cambio en cobertura del suelo, Evento hidrológico, Extremos de temperatura, Fuego, Pastoreo, Plagas y enfermedades, Sequía, Silvicultura, Sin disturbio, Tormenta o viento |
| disturbio_dominante | Sí/No | Si es el disturbio/manejo principal reportado para la unidad de muestreo, cuando hay varios registrados. | DisturbioManual.es_dominante | |
| anios_disturbio | Numérico (entero) | Cantidad de años que duró o lleva el disturbio. | DisturbioManual.anios_disturbio | |
| anios_desde_fin_disturbio | Numérico (entero) | Cantidad de años transcurridos desde que terminó el disturbio (vacío si sigue activo). | DisturbioManual.anios_desde_fin | |
| uso_suelo_IPCC | Texto | Sistema de clasificación: Suelo_IPCC. | ValorClasificacionTipo.valor | Mineral, Organico |
| ecosistema_IDEAM | Texto | Sistema de clasificación: IDEAM. | ValorClasificacionEcosistema.valor | Bosque, Humedal, Periglaciar, Páramo, Sabana, Turbera |
| estado_conservacion | Texto | Estado del ecosistema frente a la presencia de manejo humano (taxonomía del vocabulario IDEAM). | EcosistemaManual.estado_conservacion | Natural (sin manejo humano significativo), Seminatural (manejo bajo, regeneración natural dominante), Manejado (aprovechamiento, ganadería, agroforestería), Plantación (vegetación establecida y manejada), Artificial / Urbano (superficie no natural) |
| cobertura_IPCC | Texto | Sistema de clasificación: IPCC. | ValorClasificacionTipo.valor | Humedales, Tierras_forestales |
| cobertura_CLC | Texto | Sistema de clasificación: CLC. | ValorClasificacionTipo.valor | 3.1.1.2 Bosque denso bajo, 4.1.2. Turberas |
| cobertura_IGBP | Texto | Sistema de clasificación: IGBP. | ValorClasificacionTipo.valor | Humedales_permanentes |
| cobertura_Nombre_Local | Texto | Sistema de clasificación: Coloquial. | ValorClasificacionTipo.valor | Bosque Alto Andino, Paramo, Turbera |
| cobertura_vegetal_primaria | Texto | Sistema de clasificación: Vegetacion_funcional. | ValorClasificacionTipo.valor | |
| porc_cobertura_vegetal_primaria | Numérico (decimal) | Porcentaje de cobertura que representa este tipo de vegetación dentro de la unidad de muestreo (ver orden_dominancia para distinguir primaria/secundaria/terciaria). | CoberturaManual.porcentaje | |
| cobertura_vegetal_secundaria | Texto | Sistema de clasificación: Vegetacion_funcional. | ValorClasificacionTipo.valor | |
| porc_cobertura_vegetal_secundaria | Numérico (decimal) | Porcentaje de cobertura que representa este tipo de vegetación dentro de la unidad de muestreo (ver orden_dominancia para distinguir primaria/secundaria/terciaria). | CoberturaManual.porcentaje | |
| cobertura_vegetal_terciaria | Texto | Sistema de clasificación: Vegetacion_funcional. | ValorClasificacionTipo.valor | |
| porc_cobertura_vegetal_terciaria | Numérico (decimal) | Porcentaje de cobertura que representa este tipo de vegetación dentro de la unidad de muestreo (ver orden_dominancia para distinguir primaria/secundaria/terciaria). | CoberturaManual.porcentaje | |
| distancia_drenaje | Numérico (decimal) | Distancia en metros desde la unidad de muestreo hasta la fuente externa indicada (ver fuente). | ExposicionExterna.distancia_m | |
| distancia_fuego | Numérico (decimal) | Distancia en metros desde la unidad de muestreo hasta la fuente externa indicada (ver fuente). | ExposicionExterna.distancia_m | |
| distancia_pastoreo | Numérico (decimal) | Distancia en metros desde la unidad de muestreo hasta la fuente externa indicada (ver fuente). | ExposicionExterna.distancia_m | |
| distancia_cultivo | Numérico (decimal) | Distancia en metros desde la unidad de muestreo hasta la fuente externa indicada (ver fuente). | ExposicionExterna.distancia_m | |

## Hoja "Flujos CO2 - Dato"

| Campo | Tipo de dato | Descripción | Entidad.atributo (Modelo de Datos COLFLUX) | Valores permitidos (si aplica) |
|---|---|---|---|---|
| codigo_metadato | Texto | Identificador de la unidad de muestreo en el sistema de metadatos externo de la fuente, si lo trae. Llave de referencia hacia la fila de Metadato. | UnidadMuestreo.codigo_metadato | |
| analizador | Texto | Modelo del equipo analizador (ej. Picarro G4301, LI-7810). | Equipo.modelo | |
| gas | Texto | Gas medido en esta muestra: CO₂, CH₄ o N₂O. | MuestraGEI.gas | CO₂, CH₄, N₂O |
| volumen_camara | Numérico (decimal) | Volumen de aire encerrado por la cámara/anillo, usado en el cálculo del flujo. Propiedad física de la cámara, no de cada toma. | MuestraGEI.chamber_vol | |
| anillo | Numérico (decimal) | Diámetro del anillo/cámara de muestreo de gases, en centímetros. De acá se deriva area_cm2. | UnidadMuestreo.diametro_anillo_cm | |
| fecha_toma | Fecha | Fecha en la que se realizó esta toma. | SubmuestraGEI.fecha | |
| hora_toma | Hora | Hora en la que se realizó esta toma. | SubmuestraGEI.hora | |
| momento | Texto | Si la toma corresponde al inicio o al final de la medición. | SubmuestraGEI.momento | Inicio, Final |
| condicion_luz | Texto | Condición de luz bajo la que se tomó la muestra. | SubmuestraGEI.condicion_luz | Día, Noche, Noche simulada (cobija) |
| valor_flujo | Numérico (decimal) | Valor medido del flujo de gas, en la unidad reportada por la muestra (MuestraGEI.unidad_medida). | SubmuestraGEI.valor | |
| unidad_flujo | Texto | Símbolo corto para mostrar en las tablas de datos (ej. µmol m-2 s-1), en vez del código interno. | UnidadMedida.simbolo | |
| soil_temp | Numérico (decimal) | Temperatura del suelo, en grados Celsius. | MuestraAmbiental.soil_temp | |
| air_temp | Numérico (decimal) | Temperatura del aire, en grados Celsius. | MuestraAmbiental.air_temp | |
| atm_press | Numérico (decimal) | Presión atmosférica, en hectopascales (hPa). | MuestraAmbiental.atm_press | |
| relat_humid | Numérico (decimal) | Humedad relativa del aire, en porcentaje. | MuestraAmbiental.relat_humid | |
| dew_point | Numérico (decimal) | Punto de rocío, en grados Celsius. | MuestraAmbiental.dew_point | |
| water_level_cm | Numérico (decimal) | Nivel del agua respecto a la superficie, en centímetros: positivo indica encharcamiento, negativo indica nivel freático por debajo de la superficie. | MuestraAmbiental.water_level | |
| pH | Numérico (decimal) | pH del suelo o del agua en el punto de muestreo. | MuestraAmbiental.ph | |

## Hoja "Responsables" (solo en la descarga bronce, no en la plantilla vacía)

El Excel de la **vista tipo Excel/capa bronce** (`exportar_bronce`, botón "⬇
Descargar Excel" en `/etl/upload-bronce`) agrega una tercera hoja
"Responsables" con una sola fila: `nombre_proyecto`, `entidad_encargada`,
`persona_responsable`, `correo_responsable` — datos que ya existen en
`FuenteDatos` (`proyecto`, `institucion`, `reportador`) desde que se crea la
fuente, no se piden de nuevo. No aplica a `plantilla_vacia` (la plantilla en
blanco que se descarga desde `/participacion` antes de crear una fuente):
esa no está atada a ninguna `FuenteDatos` todavía.

## Referencias

- `backend/app/api/etl/views.py` — `_HOJAS_PLANTILLA`, `_MODELOS_METADATO_GEI`, `_ORDEN_COLUMNAS_METADATO_GEI_PLANTILLA`, `_ORDEN_COLUMNAS_DATO_GEI_PLANTILLA`, `_hojas_plantilla_vacia`, `_dataframe_diccionario_datos`, `plantilla_vacia`, `plantilla_detalle`, `exportar_bronce`
- `frontend/src/components/common/PlantillaDetalleModal.tsx`
- `backend/app/models/co2.py` — `MuestraGEI`, `SubmuestraGEI`, `MuestraAmbiental`
- `backend/app/models/datos.py` — `FuenteDatos`, `Usuario`
- `frontend/src/pages/Participacion.tsx`
- [Ajustes a la plantilla Flujos CO2 — feedback de Andrea Chaparro](../../tasks/inprogress/ajustes-plantilla-flujos-co2-feedback-andrea.md)
