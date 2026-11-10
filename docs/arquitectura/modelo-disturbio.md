# Modelo de datos: disturbio de una unidad de muestreo

**Estado:** implementado (2026-11-03) — catálogo `Disturbio` (antes `TipoDisturbio`
temporal durante la migración) + instancia `UnidadMuestreoDisturbio` creados tal como se
diseñó. Las 30 filas de `Sitio.disturbio` existentes se migraron: catálogo resuelto por
nombre (`get_tipo_display()` del viejo campo `tipo`), fan-out a 175
`UnidadMuestreoDisturbio` (una por cada `UnidadMuestreo` de cada sitio con disturbio),
todas con `es_dominante=True` porque el modelo viejo solo trackeaba uno por sitio. El
campo `fecha_reporte` quedó sin poblar (no existía en el modelo viejo). Contexto
conceptual en [¿Qué es un disturbio?](../conocimiento/que-es-un-disturbio.md).

## El problema

El modelo viejo (`Disturbio` en `backend/app/models/cobertura.py`, ya reemplazado — ver
Estado arriba) tenía una FK directa desde `Sitio` a un único `Disturbio` — solo se podía
registrar **un** disturbio por sitio. Ecológicamente un sitio puede acumular varios disturbios a lo largo del tiempo
(incendio en 2015, pastoreo desde 2018, otro incendio en 2023), así que esa cardinalidad
se queda corta apenas el equipo necesite registrar historial, no solo el estado actual.

Además, `DOM_DIST_MGMT` (ver
[El estándar BADM/AmeriFlux](../conocimiento/estandar-badm-ameriflux.md)) pide
específicamente **cuál es el disturbio/manejo dominante**, lo cual solo tiene sentido
como pregunta si puede haber más de uno registrado — reforzando que la relación debe ser
uno a muchos, no una FK simple.

## Decisión de diseño

Mismo patrón catálogo + instancia usado para
[Ecosistema](modelo-ecosistema.md): se separa el **tipo de disturbio** (catálogo
reutilizable) de **cada evento reportado** (instancia, con sus propios datos
temporales/de estado).

### Nivel de granularidad: `UnidadMuestreo`, no `Sitio`

Igual que con `EcosistemaManual`, el disturbio se reporta por **unidad de muestreo**, no
por sitio — consistente con que distintas unidades dentro de un mismo sitio pueden tener
historiales de disturbio distintos, y con el resto de campos de Metadato que ya viven a
ese nivel.

## Esquema implementado

Nombres reales en código (`backend/app/models/cobertura.py`) — distintos a los usados en el
diseño original de este documento:

```
Disturbio (catálogo, vía ClasificacionTipo/ValorClasificacionTipo categoría "Disturbio")
  - nombre                  ej. "Fuego", "Pastoreo", "Agricultura", "Sin disturbio"

DisturbioManual (instancia reportada)
  - unidad_muestreo         FK → UnidadMuestreo
  - disturbio               FK → ValorClasificacionTipo (catálogo Disturbio)
  - fecha_reporte
  - anios_disturbio
  - anios_desde_fin
  - es_dominante             bool — cuál de varios se reporta como `disturbio_dominante`
```

`estado_conservacion` y `proteccion_legal` **no** viven en `DisturbioManual` — se movieron a
`EcosistemaManual` en la migración `0124_mover_estado_conservacion_a_ecosistema` (anterior a
este documento). Ver [Modelo de datos: ecosistema](modelo-ecosistema.md).

Nota: la distancia a fuentes externas de disturbio (`distancia_fuego`, `distancia_pastoreo`,
`distancia_cultivo`, `distancia_drenaje`) **no** vive acá — es un concepto distinto
("qué tan cerca está esta unidad de algo que pasa en otro lugar", no "qué disturbio
ocurrió en esta unidad"). Ver
[Modelo de datos: exposición externa de una unidad de muestreo](modelo-exposicion-externa.md).

### Mapeo de campos de la plantilla

| Campo de la plantilla | Campo del modelo |
|---|---|
| `tipo_disturbio` | `ValorClasificacionTipo.valor` (catálogo Disturbio, vía `DisturbioManual.disturbio`) |
| `anios_disturbio` | `DisturbioManual.anios_disturbio` |
| `anios_desde_fin_disturbio` | `DisturbioManual.anios_desde_fin` |
| `estado_conservacion` | `EcosistemaManual.estado_conservacion` (no es de `DisturbioManual`, ver nota arriba) |
| `proteccion_legal` | `EcosistemaManual.proteccion_legal` (idem) |
| `disturbio_dominante` (antes `DOM_DIST_MGMT`, renombrado 2026-11-09 para que el nombre de columna sea autoexplicativo) | fila de `DisturbioManual` con `es_dominante = True` |

`uso_actual` (campo 26 de la lista de Metadato) **no** es parte de este modelo — ya está
resuelto como `Sitio.uso_actual`, un atributo distinto (para qué se usa el sitio hoy, no
qué evento de disturbio tuvo).

## Pendiente

- ~~Confirmar la lista cerrada de valores~~ — **resuelto (2026-11-09)**: los 3
  valores sembrados por el backfill (`Cambio en cobertura del suelo`, `Pastoreo`,
  `Sin disturbio`) son un subconjunto del vocabulario oficial `DOM_DIST_MGMT` de
  AmeriFlux/BADM (11 valores, ver
  [El estándar BADM/AmeriFlux](../conocimiento/estandar-badm-ameriflux.md)),
  recortado porque solo esos 3 estaban presentes en los datos viejos migrados.
  Catálogo completado en la migración `0125_completar_catalogo_disturbio_badm`
  con los 8 valores restantes (Agricultura, Sequía, Fuego, Silvicultura, Evento
  hidrológico, Plagas y enfermedades, Tormenta o viento, Extremos de temperatura).
- Agregar `UnidadMuestreoDisturbio` a `_VISTAS_DESNORMALIZADAS["submuestra_gei"]` en
  `backend/app/api/etl/views.py` para que aparezca en la plantilla descargable — lógica
  de pivoteo nueva (reverse-FK desde `UnidadMuestreo`), fuera de alcance de la
  implementación de 2026-11-03.
- Confirmar el origen/metodología de `Sitio.uso_actual` (campo 26 de la lista de
  Metadato, mencionado arriba). Sus 12 valores (`Bosque_primario`, `Bosque_secundario`,
  `Plantacion_forestal`, `Agricultura_intensiva`, `Agricultura_tradicional`, `Pastura`,
  `Humedal_natural`, `Humedal_intervenido`, `Area_protegida`, `Sistema_agroforestal`,
  `Abandonado`, `Restauracion_activa`) están hardcodeados como `choices` en
  `backend/app/models/sitio.py` desde el commit que introdujo el modelo reestructurado
  (`9110b9c`, 2026-07-01), sin cita de fuente. Búsqueda web (2026-11-09) no encontró un
  estándar único que calce 1:1: no es BADM/AmeriFlux (su único campo de cobertura es
  `IGBP`, con otra taxonomía), tampoco calza con el esquema IGAC-UPRA de vocación de uso
  del suelo en Colombia (5-6 clases más generales: Agrícola, Pecuario, Forestal,
  Agroforestal, Acuícola/Pesquero, Conservación). Parece una lista ad-hoc armada por el
  equipo mezclando terminología forestal/REDD+, agrícola y de conservación — falta
  confirmar con el equipo si está avalada por alguna metodología puntual o si se debe
  reemplazar/ajustar.

## Referencias

- [¿Qué es un disturbio?](../conocimiento/que-es-un-disturbio.md)
- [Plantilla de carga/descarga: metadato y dato de CO2/CH4](plantilla-metadato-dato-co2-camaras.md)
- [Modelo de datos: ecosistema/zonificación de un sitio](modelo-ecosistema.md)
- [El estándar BADM/AmeriFlux](../conocimiento/estandar-badm-ameriflux.md)
- `backend/app/models/cobertura.py` — `Disturbio`, `UnidadMuestreoDisturbio`
