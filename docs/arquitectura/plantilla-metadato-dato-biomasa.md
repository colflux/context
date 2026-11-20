# Plantilla de carga/descarga: metadato y dato de Biomasa (producción de biomasa aérea)

**Estado: implementado (2026-11-19), pendiente de validar con el equipo
las decisiones marcadas abajo.** Repite el ejercicio hecho para Flujos
CO2/CH4 ([plantilla-metadato-dato-co2-camaras.md](plantilla-metadato-dato-co2-camaras.md))
para la metodología de Biomasa (`MuestraBiomasa`/`IndividuoArboreo` en
`backend/app/models/biomasa.py`). Implementado como dos vistas nuevas
`"biomasa_metadato"`/`"biomasa_dato"` en `_VISTAS_DESNORMALIZADAS`
(`backend/app/api/etl/views.py`), sumadas a `_HOJAS_PLANTILLA` — la
plantilla descargable, el modal "Ver detalle de la plantilla" y el mapeo
automático de columnas al subir un archivo ya cubren Biomasa, igual que
Flujos CO2. La vista genérica previa `"biomasa"` (compartida con MOM/COS,
solo 4 columnas) se deja intacta — la siguen usando `exportar_carga`/
`datos_carga`/el tab "Biomasa" de `DatosTabs.tsx`, no se tocó.

Este documento parte del Excel real que trae el equipo de datos
(`context/data/Biomasa.xlsx`, hoja "Metadatos BM" + hoja "BD Biomasa").

## Hoja "Biomasa - Metadato" (propuesta)

Mismo bloque de contexto (sitio, geografía, cobertura, disturbio) que Flujos
CO2 — son los mismos modelos (`Sitio`, `UnidadMuestreo`, `Cobertura`,
`Disturbio`, `EcosistemaManual`), así que la mayoría de columnas ya existen y
se pueden reutilizar tal cual. Se marca entre paréntesis cuando el nombre de
columna del Excel de Biomasa difiere del usado en Flujos.

| Campo | Tipo de dato | Descripción | Entidad.atributo (Modelo de Datos COLFLUX) | Estado |
|---|---|---|---|---|
| nombre_proyecto | Texto | Nombre del proyecto/fuente. | Proyecto.nombre | ✅ existe (excluido de la hoja final de Flujos por decisión de equipo 2026-11-09 — confirmar si aplica igual aquí) |
| TEAM_MEMBER_NAME | Texto | Nombre de quien reportó los datos. | — | ⚠️ sin campo en el modelo (mismo pendiente que en Flujos) |
| TEAM_MEMBER_EMAIL | Texto | Correo de quien reportó los datos. | — | ⚠️ sin campo en el modelo (mismo pendiente que en Flujos) |
| codigo_metadatos | Texto | Identificador de la unidad de muestreo en el sistema de metadatos externo de la fuente. | UnidadMuestreo.codigo_metadato | ✅ existe |
| region_natural | Texto | Región natural del sitio. | Region.nombre | ✅ existe |
| departamento | Texto | Departamento del sitio. | Departamento.nombre | ✅ existe |
| Municipio | Texto | Municipio del sitio. | Municipio.nombre | ✅ existe |
| Vereda | Texto | Vereda del sitio. | Vereda.nombre | ✅ existe |
| sitio | Texto | Nombre del sitio. | Sitio.nombre | ✅ existe |
| Tipo de localización | Texto | Precisión espacial de la ubicación. | Sitio.tipo_localizacion | ✅ existe |
| latitud / longitud | Numérico (decimal) | Coordenadas del sitio (WGS84). | Sitio.latitud / Sitio.longitud | ✅ existe |
| sistema_referencia | Texto | Sistema de referencia de coordenadas. | SistemaReferencia.nombre | ✅ existe |
| altitud | Numérico (decimal) | Altitud sobre el nivel del mar, en metros. | Sitio.altitud | ✅ existe |
| pendiente | Texto | Categoría de pendiente del terreno. | Sitio.pendiente | ✅ existe |
| topografia | Texto | Posición topográfica. | Sitio.topografia | ✅ existe |
| Ecosistema / Cobertura | Texto | Sistema de clasificación IDEAM. | ValorClasificacionEcosistema.valor | ✅ existe (`ecosistema_IDEAM` en Flujos) |
| cobertura_IPCC / cobertura_CLC / cobertura_IGBP / cobertura_nom_comun | Texto | Sistemas de clasificación de cobertura. | ValorClasificacionTipo.valor | ✅ existen (mismos 4 catálogos que Flujos) |
| Suelo IPCC | Texto | Mineral / Orgánico. | ValorClasificacionTipo.valor | ✅ existe (`uso_suelo_IPCC` en Flujos) |
| tipo_disturbio | Texto | Sistema de clasificación: Disturbio. | ValorClasificacionTipo.valor | ✅ existe |
| anios_disturbio | Numérico (entero) | Años que duró/lleva el disturbio. | DisturbioManual.anios_disturbio | ✅ existe |
| anios_desde_fin_disturbio | Numérico (entero) | Años desde que terminó el disturbio. | DisturbioManual.anios_desde_fin | ✅ existe |
| uso_actual | Texto | Uso actual del suelo. | Sitio.uso_actual | ✅ existe |
| Estado conservación | Texto | Taxonomía IDEAM de manejo humano. | EcosistemaManual.estado_conservacion | ✅ existe |
| proteccion_legal | Texto largo | Figura de reserva/parque/santuario. | EcosistemaManual.proteccion_legal | ✅ existe |
| DOM_DIST_MGMT | Texto | **Sin confirmar qué representa.** En el Excel real los valores observados son categorías tipo "Grazing" (no Sí/No) — no parece ser lo mismo que `disturbio_dominante` (Sí/No) de Flujos. | — | ❓ aclarar con el equipo de datos antes de mapear |
| Tipo muestreo | Texto | Probabilístico / No probabilístico. | UnidadMuestreo.tipo_muestreo | ✅ existe |
| Tipo unidad de muestreo | Texto | Parcela, transecto, etc. | UnidadMuestreoTipo.nombre | ✅ existe |
| Tamaño unidad de muestreo (área en cm2) | Numérico (decimal) | Área de la parcela. | Parcela.area (en **m², no cm²** — requiere conversión al importar/exportar) | ✅ existe, distinta unidad |
| Forma unidad de muestreo | Texto | Cuadrada / Rectangular / Circular. | Parcela.forma | ✅ existe (a diferencia de Flujos, acá además hace falta `medida_largo`/`medida_ancho`/`distancia`/`diametro` según la forma para que el área se calcule — ver `Parcela.clean()`) |
| Periodicidad de muestreo | Texto | Frecuencia del muestreo. | — | ⚠️ sin campo (se descartó para Flujos el 2026-11-02 — confirmar si aplica igual aquí) |
| monitoreo_biomasa_aerea / protocolo_biomasa_aerea | Sí/No + Texto | Si se monitorea biomasa aérea y con qué protocolo. | — | ⚠️ sin campo en el modelo |
| monitoreo_biomasa_subterranea / protocolo_biomasa_subterranea | Sí/No + Texto | Si se monitorea biomasa subterránea (raíces) y con qué protocolo. | — | ⚠️ sin campo ni metodología modelada — Biomasa subterránea no existe hoy en `backend/app/models/biomasa.py` |
| monitoreo_flora / protocolo_flora | Sí/No + Texto | Si se monitorea composición florística y con qué protocolo. | — | ⚠️ sin campo en el modelo |
| monitoreo_rasgos_funcionales / protocolo_rasgos_funcionales | Sí/No + Texto | Si se monitorean rasgos funcionales y con qué protocolo. | — | ⚠️ sin campo en el modelo |
| cobertura_vegetal_terciaria | Texto | Sistema de clasificación: Vegetacion_funcional. | ValorClasificacionTipo.valor | ✅ existe (igual que en Flujos; el Excel de Biomasa solo trae la terciaria, no primaria/secundaria — confirmar si es un recorte intencional de la plantilla o falta en el Excel) |
| porcentaje_cob_veg_ter | Numérico (decimal) | % de cobertura de esa vegetación. | CoberturaManual.porcentaje | ✅ existe |
| distancia_drenaje / distancia_fuego / distancia_pastoreo / distancia_cultivo | Numérico (decimal) | Distancia en metros a la fuente externa indicada. | ExposicionExterna.distancia_m | ✅ existen (mismos 4 que Flujos) |

**Resumen:** de 45 columnas relevadas, 38 ya tienen modelo (reutilizando lo
construido para Flujos CO2 — mismo `Sitio`/`UnidadMuestreo`/catálogos), 7 no
tienen campo todavía (`TEAM_MEMBER_*`, `Periodicidad de muestreo`, los 4
pares `monitoreo_*`/`protocolo_*`) y 1 queda sin aclarar (`DOM_DIST_MGMT`).

## Hoja "Biomasa - Dato" (propuesta)

A diferencia de Flujos (una sola entidad `SubmuestraGEI` por fila), el Excel
real de Biomasa mezcla **dos niveles de granularidad en una sola fila**: el
agregado de carbono por parcela y, cuando existe, el detalle por individuo
arbóreo. Esto refleja la relación real del modelo:
`MuestraBiomasa` (1) → `IndividuoArboreo` (N) — FK inversa, igual que el caso
ya documentado de Cobertura/Disturbio en
[plantilla-metadato-dato-co2-camaras.md](plantilla-metadato-dato-co2-camaras.md).
**Hoy la vista `biomasa` (`_VISTAS_DESNORMALIZADAS`) usa `MuestraBiomasa`
como base y no aplana `IndividuoArboreo`** (ver comentario en
`backend/app/api/etl/views.py` línea ~3537): en los datos reales de IDEAM,
`IndividuoArboreo` siempre viene vacío, así que no se ha necesitado resolver
el aplanado todavía. Si se adopta este Excel como plantilla, hay que decidir
si se mantiene así (parcela agregada, sin detalle por árbol) o se agrega una
segunda hoja/vista con `IndividuoArboreo` como base (análoga a
`submuestra_gei`).

### Nivel parcela — `MuestraBiomasa`

| Campo (Excel) | Tipo de dato | Descripción | Entidad.atributo | Estado |
|---|---|---|---|---|
| ID | Texto | Identificador de la fila en la fuente original. | — (no es un campo propio, se resuelve vía `codigo_metadato`) | ✅ sin acción |
| # Unidad de Muestre | Texto | Identificador de la unidad de muestreo (P1, P2, ...). | UnidadMuestreo.nombre | ✅ existe |
| Fecha instalación unidad de muestreo | Fecha | Fecha de instalación. | UnidadMuestreo.fecha_instalacion | ✅ existe — **ver nota**: este mismo campo se quitó de la plantilla de Flujos por pedido de Andrea Chaparro ([[ajustes-plantilla-flujos-co2-feedback-andrea]], 2026-11-17); confirmar si para Biomasa se mantiene o se quita igual |
| Site | Texto | Nombre del grupo de parcelas (ej. "Palacios"). | UnidadExperimental.nombre | ✅ existe |
| Fecha (medición) | Fecha | Fecha de la medición de biomasa. | MuestraBiomasa.fecha | ✅ existe (no viene como columna separada en el Excel de ejemplo, pero el modelo la tiene) |
| Prod. Biomasa (g) | Numérico (decimal) | Producción de biomasa aérea. | MuestraBiomasa.prod_biomasa_g | ✅ existe |
| Contenido de carbono | Numérico (decimal) | Contenido de carbono de la muestra. | MuestraBiomasa.contenido_carbono | ✅ existe |
| Prom_TonC_ha | Numérico (decimal) | Promedio de carbono en biomasa aérea, TonC/ha. | MuestraBiomasa.prom_tonc_ha | ✅ existe |
| SD_TonC_ha | Numérico (decimal) | Desviación estándar, TonC/ha. | MuestraBiomasa.sd_tonc_ha | ✅ existe |
| min_TonC_ha / max_TonC_ha | Numérico (decimal) | Mínimo/máximo, TonC/ha. | MuestraBiomasa.min_tonc_ha / max_tonc_ha | ✅ existe |

### Nivel individuo arbóreo — `IndividuoArboreo` (reverse FK, no aplanado hoy)

| Campo (Excel) | Tipo de dato | Descripción | Entidad.atributo | Estado |
|---|---|---|---|---|
| Tipo | Texto | Tipo de individuo. | IndividuoArboreo.tipo | ✅ existe |
| N_ind | Numérico (entero) | Número de individuo. | IndividuoArboreo.n_ind | ✅ existe |
| Condicion | Texto | Condición del individuo. | IndividuoArboreo.condicion | ✅ existe |
| Nº. Fuste | Texto | Identificador del fuste. | IndividuoArboreo.numero_fuste | ✅ existe |
| muLtiples | Texto | Si el individuo tiene múltiples fustes. | IndividuoArboreo.multiples | ✅ existe |
| DAP.1 / DAP.2 | Numérico (decimal) | Diámetro a la altura del pecho, dos mediciones. | IndividuoArboreo.dap_1 / dap_2 | ✅ existe |
| dap_analisis_cm | Numérico (decimal) | DAP usado para el análisis. | IndividuoArboreo.dap_analisis_cm | ✅ existe |
| EQUIPO | Texto | Equipo usado para medir. | IndividuoArboreo.equipo | ✅ existe |
| POM (m) | Numérico (decimal) | Altura de medición del DAP. | IndividuoArboreo.pom_m | ✅ existe |
| Altura.Fuste_m / Altura.Total_m | Numérico (decimal) | Altura del fuste / total. | IndividuoArboreo.altura_fuste_m / altura_total_m | ✅ existe |
| diff_aLturas | Numérico (decimal) | Diferencia entre alturas. | IndividuoArboreo.diff_alturas | ✅ existe |
| Familia / genero / especie | Texto | Taxonomía del individuo. | IndividuoArboreo.familia / genero / especie | ✅ existe |

**Resumen / decisión implementada:** la hoja "Biomasa Dato" quedó a nivel
parcela (`MuestraBiomasa`, 8 columnas) — **no** se agregó el detalle por
individuo arbóreo (`IndividuoArboreo`, FK inversa 1:N, mismo problema de
aplanado ya documentado para Cobertura/Disturbio en Flujos; además en los
datos reales de IDEAM siempre viene vacío). Si en el futuro llega un archivo
real con detalle de individuos, hace falta una vista nueva tipo
`submuestra_gei` con `IndividuoArboreo` como base — fuera de alcance de esta
sesión.

## Decisiones tomadas al implementar (2026-11-19, sin volver a preguntar)

Las 4 preguntas abiertas de la primera versión de este documento se
resolvieron así para poder implementar sin bloquear en el equipo —
quedan documentadas para poder revisarlas después:

1. **`DOM_DIST_MGMT`**: no se incluyó en la plantilla — no está claro qué
   representa (los valores de ejemplo, "Grazing", no calzan con
   `disturbio_dominante` Sí/No de Flujos) y agregar una columna mal mapeada
   es peor que omitirla. Pendiente de aclarar con el equipo de datos.
2. **`monitoreo_*`/`protocolo_*`** (biomasa subterránea, flora, rasgos
   funcionales): no se incluyeron — no tienen campo en el modelo y crear
   metodologías/migraciones nuevas para 4 pares de columnas es un alcance
   mayor que el de esta sesión. Quedan como backlog si el equipo confirma
   que se necesitan.
3. **Hoja Dato a nivel parcela** (sin individuo arbóreo) — ver resumen
   arriba.
4. **Mismas exclusiones que Flujos** (`nombre_proyecto`, fecha de
   instalación, periodicidad de muestreo): se aplicó el mismo criterio por
   consistencia entre metodologías, sin volver a preguntar. Si el equipo
   decide que Biomasa sí necesita alguna de estas tres, es un cambio
   acotado (agregar la columna a `orden_columnas`/`campos` de
   `biomasa_metadato`/`biomasa_dato`).

Además, `Parcela.area` está en **m²** (no cm² como pedía el Excel original)
— se expone tal cual el modelo, con el nombre `tamano_unidad_muestreo_m2`;
convertir unidades en la plantilla sería más confuso que claro.

## Verificado en vivo (2026-11-19)

`docker compose exec web python manage.py check` limpio; `_hojas_plantilla_vacia()`
genera "Biomasa Metadato" (47 columnas) y "Biomasa Dato" (8 columnas);
`plantilla_vacia()` descarga un Excel real con 5 hojas (Flujos Metadato/Dato,
Biomasa Metadato/Dato, Diccionario de datos); `plantilla_detalle()` devuelve
las 47+8 filas correspondientes; `_sugerir_mapeos_automaticos()` mapea
Biomasa Dato 8/8 automático y Biomasa Metadato 31/47 (las 16 columnas de
cobertura/disturbio/exposición externa quedan ambiguas, mismo límite ya
conocido en Flujos). `npx tsc --noEmit` y `npx eslint` limpios en los
archivos de frontend tocados (`Participacion.tsx`, `FuenteDrawer.tsx`,
`PlantillaDetalleModal.tsx`, `EtlUpload.tsx`).

Ajuste posterior (mismo día): `MuestraBiomasa.prod_biomasa_g`, `contenido_carbono`,
`sd_tonc_ha`, `min_tonc_ha` y `max_tonc_ha` no tenían `help_text` en el modelo, así
que en el modal "Ver detalle de la plantilla" esas filas salían sin descripción
(se veían más cortas que el resto). Se les agregó `help_text` corto a los 5 campos
(migración `0131_alter_muestrabiomasa_contenido_carbono_and_more`) para que las 8
columnas de "Biomasa Dato" queden con descripción, igual que Flujos.

Segundo ajuste (mismo día, pedido explícito de la usuaria): hasta este punto
"Descargar plantilla"/"Ver detalle de la plantilla" traían SIEMPRE las hojas de
TODAS las metodologías juntas (Flujos + Biomasa + COS + lo que hubiera en
`_HOJAS_PLANTILLA`), sin importar desde qué tarjeta de `/participacion` se
hiciera click — la usuaria pidió separarlas: que la tarjeta de Biomasa descargue
solo sus hojas, no las de Flujos. Se agregó una clave `"metodologia"` a cada
`hoja_def` de `_HOJAS_PLANTILLA` (mismo `key` que usa `METODOLOGIAS` en
`Participacion.tsx`: `"flujos"`, `"biomasa"`, `"cos"`, `"mom"`), y un parámetro
opcional `metodologia` en `_hojas_plantilla_vacia()`/`plantilla_vacia`/
`plantilla_detalle` (query param `?metodologia=<key>`) que filtra a solo esas
hojas. `_sugerir_mapeos_automaticos`/`mapeo_automatico` siguen llamando a
`_hojas_plantilla_vacia()` sin filtro (necesitan reconocer un archivo subido sea
cual sea su metodología). El Excel descargado por metodología también cambia el
nombre de archivo (`plantilla_biomasa.xlsx` en vez de `plantilla_colflux.xlsx`).
Verificado en vivo con `RequestFactory` contra las 2 vistas: sin filtro trae las
8 hojas + diccionario; con `?metodologia=biomasa` trae solo "Biomasa
Metadato"/"Biomasa Dato" + diccionario (2 filas del diccionario en vez de las
~100 de antes). `manage.py check`, `npx tsc --noEmit` y `npx eslint` limpios.

**Gotcha detectado el 2026-11-20:** la verificación de arriba con
`manage.py shell`/`RequestFactory` da falsos positivos sobre si el cambio ya
está "vivo" — reimporta el módulo en cada invocación, así que siempre ve el
código tal cual está en disco. El contenedor compartido corre con
`gunicorn --workers 4` (sin `--reload`, ver `CMD` en `backend/docker-compose.yml`),
así que los 4 procesos worker mantienen en memoria el código que tenían cargado
al arrancar — un cambio en `views.py` no lo ven hasta que el proceso se
reinicia. Por eso la usuaria reportó que "Ver detalle de la plantilla" seguía
trayendo las 4 hojas (Flujos+Biomasa) después de implementado el filtro por
`?metodologia=`, aunque el código en disco y las pruebas por shell ya estaban
bien. Se resolvió con `docker compose restart web`. **Para la próxima vez:**
después de tocar `backend/app/**/*.py` en este contenedor, verificar el cambio
con una petición HTTP real (`curl localhost:8001/...`), no solo con
`manage.py shell`/`RequestFactory` — y si el `curl` no refleja el cambio,
reiniciar el servicio antes de asumir que el código está mal.

## Referencias

- `context/data/Biomasa.xlsx` — hojas "Metadatos BM" (metadato) y
  "BD Biomasa"/"BMORI sin Duplicados" (dato, incluye también MOM en
  la hoja "MOM ORI sin duplicados", fuera de alcance de este documento).
- `backend/app/models/biomasa.py` — `MuestraBiomasa`, `IndividuoArboreo`.
- `backend/app/models/sitio.py` — `Parcela` (forma/área).
- `backend/app/api/etl/views.py` — `_VISTAS_DESNORMALIZADAS["biomasa_metadato"]`,
  `_VISTAS_DESNORMALIZADAS["biomasa_dato"]`, `_HOJAS_PLANTILLA`,
  `_ORDEN_COLUMNAS_METADATO_BIOMASA_PLANTILLA`,
  `_ORDEN_COLUMNAS_DATO_BIOMASA_PLANTILLA`, `_PIVOTE_EXTRA_POR_VISTA`,
  `_ORDEN_EXTRA_POR_VISTA`. La vista previa `_VISTAS_DESNORMALIZADAS["biomasa"]`
  (genérica, compartida con MOM/COS) no se tocó.
- `frontend/src/pages/Participacion.tsx`, `frontend/src/components/admin/fuentes/FuenteDrawer.tsx`,
  `frontend/src/components/common/PlantillaDetalleModal.tsx`, `frontend/src/pages/EtlUpload.tsx`.
- [plantilla-metadato-dato-co2-camaras.md](plantilla-metadato-dato-co2-camaras.md) — mismo ejercicio para Flujos CO2, modelo a seguir.
- [[plantilla-metadato-dato-biomasa]] (tarea)
- [[subida-descarga-formato-metadato-dato-por-metodologia]]
