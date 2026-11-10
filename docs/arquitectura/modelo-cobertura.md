# Modelo de datos: cobertura de una unidad de muestreo

**Estado:** implementado (2026-11-03), y migrado de nuevo (2026-11-09) a `ClasificacionTipo`/
`ValorClasificacionTipo` ([Modelo de datos relacional](modelo-datos.md)) — `TipoCobertura`/
`ValorCobertura` quedaron huérfanos de una migración anterior sin terminar (quedaba el
paso 3/3 del patrón expand/contract sin aplicar: `CoberturaManual.tipo`/`.valor` ya
apuntaban al catálogo genérico, pero las tablas viejas y el ETL seguían vivos). Se
detectó porque el ETL (`_procesar_fila_cobertura`) todavía intentaba guardar
`CoberturaManual.tipo`/`.valor` con instancias de `TipoCobertura`/`ValorCobertura` — un
type mismatch que habría roto la carga de cobertura por el wizard en cuanto se probara
(no hay evidencia de que se haya usado después de la migración del modelo). Se completó
la migración (`0121`/`0122` en `backend/app/migrations/`, con `RenameField` para no
perder el backfill ya hecho en `0120`), se borraron `TipoCobertura`/`ValorCobertura`, se
repuntó `MapeoColumna.tipo_cobertura` a `ClasificacionTipo`, y se arregló el mismo bug en
`_procesar_fila_disturbio` (resolvía/creaba contra el catálogo `Disturbio` viejo en vez
de `ClasificacionTipo`/`ValorClasificacionTipo`, con `UnidadMuestreoDisturbio.disturbio`
que ya no existe en el modelo). `TipoClasificacionEcosistema`/`ValorClasificacionEcosistema`
quedan en el mismo estado huérfano (fuera de alcance de esta sesión, ver modelo-ecosistema.md) —
pendiente la misma limpieza.

Historial previo de implementación (2026-11-03): `Cobertura` renombrado a `CoberturaManual` y
rediseñado tal como se propuso: `ValorCobertura` creado, nivel de granularidad movido de
`Sitio` a `UnidadMuestreo`. Las ~98 filas existentes se migraron (texto libre →
`ValorCobertura` catalogado, fan-out de `Sitio` a cada `UnidadMuestreo` del sitio); 5
filas del sitio "Trillizas" (sin ninguna `UnidadMuestreo` cargada) se descartaron por
decisión explícita del usuario. `Vegetacion.tipo_cobertura` se absorbió como
`TipoCobertura(codigo="Vegetacion_funcional")` — sin filas que migrar, no había ningún
`Sitio.vegetacion` cargado en ese momento. El modelo `CoberturaArea` (área real,
geometría) sigue sin implementarse — trabajo futuro, no bloqueante. Mismo patrón que
[Modelo de datos: ecosistema/zonificación de un sitio](modelo-ecosistema.md), aplicado a
cobertura de la tierra.

## El problema

El modelo actual (`Cobertura`/`TipoCobertura` en `backend/app/models/cobertura.py`) ya
cubre el concepto — varios sistemas de clasificación de cobertura (uso_actual_IPCC, CLC,
IGBP, Suelo_IPCC, nombre común) por sitio — pero con dos limitaciones:

1. **Técnica:** `Cobertura` tiene una FK **hacia** `Sitio` (relación inversa desde
   `Sitio`, `related_name="coberturas"`). El mecanismo que arma las columnas de la
   plantilla (`_campos_planos`/`cadena` en `_VISTAS_DESNORMALIZADAS`,
   `backend/app/api/etl/views.py`) solo sigue relaciones FK hacia adelante desde el
   modelo base, así que hoy el dato no puede exportarse a la plantilla sin lógica nueva.
2. **De diseño:** `Cobertura.nombre` es texto libre ("nombre reportado"), sin catálogo de
   valores permitidos — mismo problema que se identificó para Ecosistema, y misma
   solución: separar el catálogo de valores posibles del dato digitado.

## Decisión de diseño

Se aplica el mismo patrón de tres piezas que para Ecosistema (catálogo de tipo + catálogo
de valores permitidos + instancia digitada + área real como trabajo futuro), y el mismo
cambio de nivel: de `Sitio` a `UnidadMuestreo`, por consistencia con
[Ecosistema](modelo-ecosistema.md) y [Disturbio](modelo-disturbio.md) — la cobertura
vegetal también puede variar entre unidades de muestreo de un mismo sitio.

## Esquema (vigente desde 2026-11-09)

```
ClasificacionTipo (catálogo genérico — reemplaza TipoCobertura, ver modelo-datos.md)
  - nombre              ej. "uso_actual_IPCC", "CLC", "IGBP", "Suelo_IPCC", "Coloquial", "Vegetacion_funcional"
  - categoria           "Cobertura Vegetal" para los tipos de cobertura

ValorClasificacionTipo (catálogo de valores permitidos por tipo — reemplaza ValorCobertura)
  - tipo                FK → ClasificacionTipo
  - valor                ej. "Forest Land" (uso_actual_IPCC), "Bosque denso" (CLC)

CoberturaManual (dato digitado — reemplaza el Cobertura.nombre en texto libre actual)
  - unidad_muestreo     FK → UnidadMuestreo      (antes: FK → Sitio en el modelo Cobertura)
  - tipo                FK → ClasificacionTipo
  - valor               FK → ValorClasificacionTipo
  - valor_texto         CharField — texto tal como llegó en el import
  - porcentaje          DecimalField, null/blank   (% de cobertura que ocupa este valor)
  - orden_dominancia    choices: Primaria/Secundaria/Terciaria, null/blank

ClasificacionArea (área real, geometría — trabajo futuro, reemplaza CoberturaArea)
  - tipo                FK → ClasificacionTipo
  - valor               FK → ValorClasificacionTipo
  - geom                PolygonField (PostGIS)
```

`CoberturaManual` reemplaza al modelo `Cobertura` original (no conviven ambos).
`MapeoColumna.tipo_cobertura` (selector de "sistema de clasificación" por columna
mapeada en el wizard ETL) también apunta a `ClasificacionTipo`.

### Vegetación funcional se absorbe como un `TipoCobertura` más

`Vegetacion.tipo_cobertura` (Árbol caducifolio/perennifolio, Gramínea C3/C4, Arbusto,
etc. — ver [¿Qué es la cobertura?](../conocimiento/que-es-la-cobertura.md)) es
conceptualmente otro sistema de clasificación de cobertura (*Plant Functional Type*), no
un concepto aparte. Se agrega como una fila más de `TipoCobertura` (código
`Vegetacion_funcional`), con sus valores (`TIPO_CHOICES` actuales de `Vegetacion`) como
`ValorCobertura`. Los campos `cobertura_vegetal_primaria/secundaria/terciaria` +
`porcentaje_cob_veg_*` de la plantilla se resuelven con tres filas de `CoberturaManual`
(`tipo=Vegetacion_funcional`, `orden_dominancia` 1/2/3, `porcentaje` propio).

Los campos de `Vegetacion` que no son cobertura (`especies_dominantes`, `altura_dosel`,
`edad_cobertura`, `estado_sucesional`) no forman parte de este rediseño — no están en la
lista de 49 atributos de la plantilla, se quedan en `Vegetacion` sin cambios.

## Pendiente

- Confirmar con el equipo/Martín la lista cerrada de valores permitidos por cada
  `TipoCobertura` (CLC, IGBP tienen nomenclaturas oficiales publicadas; nombre común
  y Suelo IPCC a confirmar) — los `ValorCobertura` ya cargados vienen del texto libre
  histórico, no de una lista oficial verificada.
  - **uso_actual_IPCC: decidido (2026-11-09).** Se usa como catálogo cerrado de
    `ValorClasificacionTipo` para `tipo=uso_actual_IPCC` la clasificación de uso de la
    tierra de las
    [Directrices del IPCC 2006 para inventarios nacionales de GEI, Vol. 4 AFOLU](https://www.ipcc-nggip.iges.or.jp/public/2006gl/spanish/pdf/4_Volume4/V4_03_Ch3_Representation.pdf)
    (Agriculture, Forestry and Other Land Use): Tierras Forestales, Tierras de Cultivo,
    Pastizales, Humedales, Asentamientos, Otras Tierras. El nombre `uso_actual_IPCC`
    (en vez de `IPCC` a secas) lo distingue de `Suelo_IPCC`, que es otro tipo de
    clasificación (de suelo, no de uso de la tierra).
- Lógica de pivoteo (una fila por `TipoCobertura` → una columna por tipo) al agregar
  `CoberturaManual` a `_VISTAS_DESNORMALIZADAS["submuestra_gei"]` — fuera de alcance de
  la implementación de 2026-11-03, sin esto el dato no aparece todavía en la plantilla
  descargable.

## Referencias

- [Modelo de datos: ecosistema/zonificación de un sitio](modelo-ecosistema.md)
- [Modelo de datos: disturbio de una unidad de muestreo](modelo-disturbio.md)
- [Plantilla de carga/descarga: metadato y dato de CO2/CH4](plantilla-metadato-dato-co2-camaras.md)
- `backend/app/models/cobertura.py` — `CoberturaManual`, `TipoCobertura`, `ValorCobertura`
