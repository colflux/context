# Modelo de datos: series de tiempo de torre EC (propuesta)

**Estado:** propuesta revisada (2026-11-01) — reemplaza el diseño semihorario original de
abajo por uno de **promedio diario**. El semihorario se implementó en el backend
(`MuestraTorre`/`SubmuestraEddy`/`SubmuestraReddy`, commit `5a31897`) pero sin datos
cargados todavía, así que se reemplaza en vez de migrar. Ver la sección "Revisión: promedio
diario en vez de detalle semihorario" más abajo para el diseño vigente — el resto del
documento (decisión Eddypro vs. ReddyProc, por qué 3 entidades) sigue aplicando igual, solo
cambia la granularidad del dato guardado.

## Contexto

El modelo actual del catálogo GEI (`backend/app/models/co2.py`, `backend/app/models/torre.py`) tiene dos piezas relacionadas con torres, pero ninguna cubre datos de flujo en serie de tiempo:

- `TorreEc` / `ConfiguracionSensorGas` — metadatos **fijos** de instalación (alturas, frecuencia de adquisición, separaciones del sensor). No son mediciones.
- `MuestraGEI` / `SubmuestraGEI` — mediciones **manuales por cámara**: una sesión (`MuestraGEI`, un tubo conectado a un analizador en una unidad de muestreo) con ~4 tomas (`SubmuestraGEI`), cada una con momento inicio/final y condición de luz día/noche/noche simulada.

Al revisar un archivo real de salida de Eddypro de la torre Guatavita ST2 (169 columnas, una fila cada 30 minutos — ver [Datos de torres EC: de Eddypro a ReddyProc](../conocimiento/datos-torres-eddypro-reddyproc.md)) se encontró que `MuestraGEI`/`SubmuestraGEI` no tiene dónde guardar los flujos (`co2_flux`, `ch4_flux`, `h2o_flux`, `H`, `LE`), sus flags de calidad, la turbulencia (`u*`) ni el footprint — son datos de otra naturaleza (serie continua semihoraria, sin "tomas" ni condición de luz discreta). Detalle completo del mapeo columna por columna en la tarea [[datos-modelado-carga-torres]].

**Decisión ya tomada:** se sube a la plataforma la salida de **Eddypro** como dato primario y obligatorio por torre; la salida de **ReddyProc** (gap-filling + partición NEE/Reco/GPP) se trata como un dato derivado y opcional, porque no todas las torres necesariamente la van a tener corrida de forma comparable. Justificación completa en la sección "Integración en Colflux" de [Datos de torres EC: de Eddypro a ReddyProc](../conocimiento/datos-torres-eddypro-reddyproc.md).

## Entidades propuestas

Tres entidades nuevas, inspiradas en el patrón sesión/toma de `MuestraGEI`/`SubmuestraGEI`, pero adaptadas: aquí no hay tomas repetidas, sino dos niveles de procesamiento (Eddypro y ReddyProc) del mismo instante semihorario.

```mermaid
erDiagram
    TorreEc ||--o{ MuestraTorre : tiene
    MuestraTorre ||--|| SubmuestraEddy : "obligatoria"
    MuestraTorre ||--o| SubmuestraReddy : "opcional"
```

### `MuestraTorre`

Ancla de identidad del registro semihorario: torre + instante de tiempo.

| Campo | Tipo | Notas |
|---|---|---|
| `torre` | FK → `TorreEc` | `on_delete=CASCADE` |
| `fecha` | DateField | |
| `hora` | TimeField | |

`unique_together = [("torre", "fecha", "hora")]`.

### `SubmuestraEddy`

Obligatoria (1:1 con `MuestraTorre`): los datos de salida de Eddypro para ese instante.

| Grupo | Campos |
|---|---|
| Flujos + calidad | `co2_flux`/`qc_co2_flux`/`rand_err_co2_flux`, igual para `ch4_flux`, `h2o_flux`, `h_flux` (calor sensible), `le_flux` (calor latente), `tau` |
| Turbulencia | `ustar`, `tke`, `monin_obukhov_length`, `bowen_ratio` |
| Footprint | `footprint_x_peak`, `footprint_x_70`, `footprint_x_90` |
| Aire / viento | `air_temperature`, `air_pressure`, `relative_humidity`, `vpd`, `air_density`, `wind_speed`, `wind_dir` |
| Resto | `datos_extra` (JSONField, opcional) — varianzas/covarianzas, spikes, diagnósticos propios de LI-7200/LI-7700, sin modelar columna por columna todavía |

### `SubmuestraReddy`

Opcional (0:1 con `MuestraTorre`) — puede no existir si la torre no tiene ReddyProc corrido.

| Campo | Notas |
|---|---|
| `nee_f` | NEE con gap-filling |
| `nee_fqc` | flag de calidad del gap-filling |
| `reco` | respiración del ecosistema |
| `gpp_f` | productividad primaria bruta |
| `ustar_used` | umbral de u* usado en el filtrado |
| `datos_extra` | JSONField, opcional, resto de columnas |

## Por qué esta forma

- **3 entidades, no 1 ni 4.** Una sola tabla con todo mezclaría dos obligatoriedades distintas (Eddypro siempre, ReddyProc a veces) y dejaría columnas `null` sistemáticamente según el tipo. Cuatro entidades (un par `Muestra`/`Submuestra` independiente por cada software) obligaría a ligar `SubmuestraReddy` a una fila específica de procesamiento de Eddypro, lo cual es más rígido de lo necesario: lo que importa es que ambas describan el mismo instante de la torre, no qué corrida específica de Eddypro se usó.
- **`SubmuestraReddy` opcional, no un segundo registro independiente.** Refleja directamente la regla de negocio: *si existe ReddyProc para un instante, necesariamente existe Eddypro para ese mismo instante* (ReddyProc es postprocesamiento de Eddypro, nunca un dato independiente).
- **`datos_extra` como JSONField.** Evita tener que modelar las ~169 columnas de Eddypro una por una desde el inicio; los campos explícitos son los que ya se identificaron como necesarios para consulta/reportes (flujos, calidad, turbulencia, footprint, meteorología básica). Se puede ir promoviendo campos de `datos_extra` a columnas propias si se vuelven necesarios para filtrar/agregar.
- **`MuestraGEI`/`SubmuestraGEI` no se tocan.** Siguen siendo exclusivamente para mediciones manuales por cámara; no se reutilizan para torres porque la semántica de "toma" día/noche no aplica a una serie continua.

## Revisión (2026-11-01): promedio diario en vez de detalle semihorario

Al retomar la implementación en [[cargar-datos-torre-guatavita-eddypro]] se decidió que la
base de datos **solo guarda el promedio diario** por torre, no el detalle semihorario de
arriba — simplifica el modelo a costa de perder la granularidad de 30 minutos (no se puede
recalcular distinto más adelante sin volver a subir el archivo original). Las 3 entidades
semihorarias de arriba (`MuestraTorre`, `SubmuestraEddy`, `SubmuestraReddy`) ya se habían
implementado en el backend sin datos cargados todavía, así que **se reemplazan** por estas
3 nuevas en vez de migrarlas:

```mermaid
erDiagram
    TorreEc ||--o{ MuestraTorreDiaria : tiene
    CargaArchivo ||--o{ MuestraTorreDiaria : genera
    MuestraTorreDiaria ||--|| SubmuestraEddyDiaria : "obligatoria"
    MuestraTorreDiaria ||--o| SubmuestraReddyDiaria : "opcional"
```

### `MuestraTorreDiaria`

Ancla de identidad: torre + fecha (no hora).

| Campo | Tipo | Notas |
|---|---|---|
| `torre` | FK → `TorreEc` | `on_delete=CASCADE` |
| `fecha` | DateField | |
| `carga` | FK → `CargaArchivo` | trazabilidad: qué carga generó este promedio |
| `n_registros_validos` | IntegerField | cuántas de las ~48 filas semihorarias del día entraron al promedio |

`unique_together = [("torre", "fecha")]`.

### `SubmuestraEddyDiaria`

Obligatoria (1:1 con `MuestraTorreDiaria`): mismas variables que `SubmuestraEddy` arriba
(flujos+calidad, turbulencia, footprint, aire/viento), pero cada campo es el **promedio del
día** en vez del valor de una ventana de 30 min. Cambio respecto al diseño semihorario:
- Los campos `qc_*` (antes un flag 0/1/2 por fila) se resumen en un único
  `pct_calidad_buena` (% de filas usadas en el promedio con `qc_co2_flux=0`) — ya no existe
  "el" flag de calidad de una fila individual cuando se promedian ~48.
- `datos_extra` (JSONField) se mantiene igual.

### `SubmuestraReddyDiaria`

Opcional (0:1 con `MuestraTorreDiaria`): promedio diario de `nee_f`, `reco`, `gpp_f`,
`ustar_used` — mismo criterio que `SubmuestraReddy` arriba.

### Regla de agregación

Antes de promediar, se descartan las filas semihorarias con `qc_*=2` ("descartar") para esa
variable — misma regla que ya estaba anotada en el plan original de
[[cargar-datos-torre-guatavita-eddypro]].

### Tensión abierta con calidad de datos

[[calidad-datos-zonas]] (propuesta en discusión, no decidida) sugiere guardar siempre el
dato **bronze** (crudo tal cual se recibió) como fuente de verdad, incluso si después se
filtra/agrega. Guardar solo el promedio diario rompe ese principio a propósito, por decisión
explícita de simplicidad — si esa propuesta avanza, hay que decidir si torre EC es una
excepción (se descarta el semihorario tras calcular el promedio) o si eventualmente se
vuelve a guardar el detalle crudo también.

## Pendiente

- Validar esta propuesta (la revisión diaria) con el equipo de backend antes de implementarla.
- Completar la sección de ReddyProc en [Datos de torres EC: de Eddypro a ReddyProc](../conocimiento/datos-torres-eddypro-reddyproc.md) cuando se tenga el archivo real de ReddyProc (`Guatavita_2_ReddyProc_2023_2024_output (1).csv`, aún no descargado en `files/archivos-torres/`), para confirmar que `SubmuestraReddyDiaria` cubre sus columnas reales.
- Definir a qué categoría del catálogo (`app/catalogo/generator.py`) pertenecerían estas entidades — probablemente una nueva o una extensión de "Torre EC y Flujos".
- Definir el formato del tercer archivo (metadata de la carga) — todavía sin un ejemplo real para diseñarlo.

## Referencias

- [[datos-modelado-carga-torres]] — tarea donde se originó esta propuesta, con el mapeo columna por columna.
- [Datos de torres EC: de Eddypro a ReddyProc](../conocimiento/datos-torres-eddypro-reddyproc.md) — qué es cada archivo y por qué se sube Eddypro.
- `backend/app/models/torre.py`
- `backend/app/models/co2.py`
