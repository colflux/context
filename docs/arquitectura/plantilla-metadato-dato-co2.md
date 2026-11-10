# Plantilla de carga/descarga: metadato y dato de CO2 (torre EC)

**Estado:** propuesta, pendiente de validar con el equipo — primera metodología concreta
de la decisión general en [[subida-descarga-formato-metadato-dato-por-metodologia]].

## Contexto

Metodología: **torre de covarianza de remolinos (eddy covariance, EC)**, dato primario
Eddypro + dato derivado opcional ReddyProc — ver
[Datos de torres EC: de Eddypro a ReddyProc](../conocimiento/datos-torres-eddypro-reddyproc.md)
y el modelo de datos propuesto en [modelo-datos-torre-ec.md](modelo-datos-torre-ec.md)
(`MuestraTorre` + `SubmuestraEddy` obligatoria + `SubmuestraReddy` opcional).

Esta plantilla separa explícitamente dos archivos/hojas: **metadato** (una fila por
torre/carga, describe cómo se midió) y **dato** (una fila por instante semihorario,
los valores medidos). Antes todo salía junto en el mismo Excel con un diccionario de
columnas embebido (ver [[f17-descarga-metadatos-metodologicos]]).

## Hoja/archivo "metadato" (una fila por torre + carga)

| Campo | Fuente | Notas |
|---|---|---|
| `torre_id` / `nombre_torre` | `TorreEc` | Identifica la torre |
| `sitio`, `lat`, `lon` | `TorreEc` | Ubicación |
| `altura_instalacion_m` | `TorreEc` | Altura de sensores sobre el dosel |
| `instrumento_viento` | `ConfiguracionSensorGas` | Modelo de anemómetro sónico 3D |
| `instrumento_gas` | `ConfiguracionSensorGas` | Modelo de analizador (ej. LI-7200 para CO₂/H₂O, LI-7700 para CH₄) |
| `frecuencia_adquisicion_hz` | `ConfiguracionSensorGas` | Frecuencia del dato crudo (10-20 Hz), agregado a ventanas de 30 min |
| `separacion_sensores_m` | `ConfiguracionSensorGas` | Separación física entre anemómetro y analizador |
| `metodologia` | fijo | `"Eddy covariance"` |
| `software_procesamiento` | nuevo | `"Eddypro"` + versión (y `"ReddyProc"` + versión si aplica) |
| `protocolo_correcciones` | nuevo | Correcciones aplicadas por Eddypro: rotación de coordenadas, corrección espectral, WPL |
| `rango_fechas_cubierto` | nuevo | Fecha inicio–fin de la serie que trae el archivo |
| `fecha_procesamiento` | nuevo | Cuándo se corrió Eddypro/ReddyProc sobre el crudo |
| `fuente_responsable` | nuevo | Quién entregó el dato (ej. "Alejandro Delgado, Javeriana") |
| `criterio_nivel_confianza` | nuevo | Qué significan los flags de calidad: `qc_*` 0=bueno, 1=aceptable, 2=descartar |
| `pct_datos_calidad_buena` | nuevo | % de filas con `qc_co2_flux=0` en el rango cargado — resumen rápido de confiabilidad |
| `filtro_ustar_usado` | solo si hay ReddyProc | Umbral de u* usado en el filtrado de ReddyProc |
| `modelo_gapfilling` | solo si hay ReddyProc | Qué modelo de relleno de huecos usó ReddyProc |

## Hoja/archivo "dato" (una fila por torre + fecha + hora)

Mapea directo a `MuestraTorre` + `SubmuestraEddy` (+ `SubmuestraReddy` si existe):

| Grupo | Campos |
|---|---|
| Identidad | `torre_id`, `fecha`, `hora` |
| Flujos + calidad | `co2_flux`, `qc_co2_flux`, `rand_err_co2_flux`, igual para `ch4_flux`, `h2o_flux`, `h_flux`, `le_flux`, `tau` |
| Turbulencia | `ustar`, `tke`, `monin_obukhov_length`, `bowen_ratio` |
| Footprint | `footprint_x_peak`, `footprint_x_70`, `footprint_x_90` |
| Aire/viento | `air_temperature`, `air_pressure`, `relative_humidity`, `vpd`, `air_density`, `wind_speed`, `wind_dir` |
| ReddyProc (opcional, solo si existe para esa torre) | `nee_f`, `nee_fqc`, `reco`, `gpp_f`, `ustar_used` |
| Resto sin modelar | `datos_extra` (JSON) — varianzas/covarianzas, spikes, diagnósticos LI-7200/LI-7700 |

El nivel de confianza por fila ya viaja en el dato mismo (`qc_co2_flux` etc.), no hace
falta repetirlo en el metadato — el metadato solo explica qué significan esos flags
(`criterio_nivel_confianza`) y da un resumen agregado (`pct_datos_calidad_buena`).

## Por qué esta separación

- El metadato no cambia fila a fila (es fijo por torre/carga); meterlo en cada fila del
  dato (como hace el Excel actual con el diccionario embebido) duplica información y
  no permite comparar metodologías entre torres de un vistazo.
- `datos_extra` sigue sin modelar columna por columna — mismo criterio que
  [modelo-datos-torre-ec.md](modelo-datos-torre-ec.md): se promueve a columna explícita
  solo si se necesita filtrar/agregar por ella.

## Pendiente

- Validar esta plantilla con el equipo antes de implementar en `exportar_carga`/
  `exportar_proyecto` (backend) y en la vista de subida (frontend).
- Definir el formato de archivo final (¿dos hojas de un mismo Excel, o dos archivos
  separados metadato.csv/dato.csv?) — no decidido todavía.
- Repetir este mismo ejercicio para las demás metodologías (suelo, biomasa, cámaras
  GEI manuales) — ver [[subida-descarga-formato-metadato-dato-por-metodologia]].

## Referencias

- [[subida-descarga-formato-metadato-dato-por-metodologia]] — tarea general de la que
  esta plantilla es el primer caso concreto.
- [modelo-datos-torre-ec.md](modelo-datos-torre-ec.md)
- [Datos de torres EC: de Eddypro a ReddyProc](../conocimiento/datos-torres-eddypro-reddyproc.md)
- `docs/requisitos/funcionalidades/carbono-y-estimaciones/f17-descarga-metadatos-metodologicos.md`
