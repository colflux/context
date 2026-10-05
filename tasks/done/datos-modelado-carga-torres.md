# Validar el modelado de datos para la carga de datos de torres

**Estado:** hecha
**Creada:** 2026-09-30
**A cargo:** Viviana
**Participantes:** Viviana
**Sesión de Claude Code:** https://claude.ai/code/session_015orBkh6stAo8qWMr6sp28t

## Objetivo

Confirmar si el modelo de datos actual (categoría "Torre EC y Flujos" / "Muestras GEI" del catálogo, ver `backend/app/models/torre.py` y `backend/app/models/co2.py`) puede recibir correctamente los datos reales de salida de una torre de covarianza de remolinos (eddy covariance), o si hace falta ajustarlo antes de cargar esos datos a la plataforma.

## Contexto

Surge del pendiente "analizar archivos de torres" en `journal/vivi/TODAY.md` (2026-10-01): Alejandro Delgado (Javeriana) compartió por correo el 2026-09-29 dos archivos de la torre Guatavita ST2 (en `files/archivos-torres/`):

- `eddypro_Guatavita_2_2024_full_output_2025-04-27T022924_adv.csv` — salida de preprocesamiento (Eddypro).
- `Guatavita_2_ReddyProc_2023_2024_output (1).csv` — salida de postprocesamiento (ReddyProc), pendiente de descargar del correo.

Revisando el modelo de datos existente:

- `TorreEc` / `ConfiguracionSensorGas` (`backend/app/models/torre.py`) modelan metadatos **fijos** de la torre (alturas, frecuencia de adquisición, separaciones del sensor) — no series de tiempo.
- `MuestraGEI` / `SubmuestraGEI` (`backend/app/models/co2.py`) modelan mediciones **manuales por cámara**: una muestra = un tubo conectado a un analizador, con ~4 "tomas" (`n_toma`) y condición de luz día/noche/noche simulada. Este modelo no calza obviamente con la salida típica de Eddypro/ReddyProc, que es una serie continua de datos cada 30 minutos (NEE, H, LE, ustar, flags de calidad, gap-filling, decenas de columnas) por torre.

No está claro todavía si `MuestraGEI`/`SubmuestraGEI` se puede reutilizar (p. ej. cada fila de 30 min como una "muestra" sin tomas múltiples) o si se necesita un modelo nuevo para series de tiempo de torre EC.

## Plan

- [x] Descargar y abrir `Guatavita_2_ReddyProc_2023_2024_output (1).csv` (ReddyProc) y revisar su estructura de columnas junto con el `eddypro_..._adv.csv` ya guardado. *(solo se pudo hacer con el de Eddypro — el de ReddyProc no se encontró descargado en `files/archivos-torres/`, sigue pendiente)*
- [x] Entender qué significa cada atributo/columna de esos archivos y de dónde puede venir — documentado en [docs/conocimiento/datos-torres-eddypro-reddyproc.md](../../docs/conocimiento/datos-torres-eddypro-reddyproc.md) (pendiente de completar la sección de ReddyProc cuando se tenga el archivo).
- [x] Mapear esas columnas contra las entidades existentes para saber qué ya se puede subir hoy — ver tabla abajo.
- [x] Con ese mapeo claro, decidir: reutilizar el modelo actual con ajustes, o proponer un modelo nuevo para series de tiempo de torre EC. **Decisión: modelo nuevo** — ver diseño abajo.
- [x] Documentar la decisión en `docs/arquitectura/` si implica un cambio de modelo — ver [docs/arquitectura/modelo-datos-torre-ec.md](../../docs/arquitectura/modelo-datos-torre-ec.md).

## Mapeo: columnas de Eddypro vs. modelo actual

El archivo de Eddypro trae 169 columnas, una fila cada 30 minutos (6848 filas = todo 2024). Resultado de cruzarlas contra las entidades existentes:

| Grupo de columnas Eddypro | ¿Calza con algo del modelo actual? |
|---|---|
| `file_info` (fecha, hora, DOY, daytime) | Parcial — `MuestraAmbiental.fecha`/`hora` ya soportan timestamp único por `(fecha, hora, fuente_datos)`, que sí es compatible con una serie continua semihoraria (no requiere `momento` inicio/final). |
| `air_properties` (air_temperature, RH, VPD, air_pressure) | Parcial — `MuestraAmbiental` tiene `air_temp`, `relat_humid`, `atm_press`, `dew_point`. Faltarían `VPD`, `air_density`, `specific_humidity`, etc. |
| `corrected_fluxes_and_quality_flags` (co2_flux, ch4_flux, h2o_flux, H, LE, Tau + sus `qc_*`) | **No calza.** `MuestraGEI`/`SubmuestraGEI` esperan una muestra manual por cámara con ~4 tomas y día/noche discreto, no un valor de flujo continuo con su propio flag de calidad por timestamp. No hay dónde guardar `qc_co2_flux`, `rand_err_*`, ni el valor de `H`/`LE`/`Tau`. |
| `turbulence`, `footprint`, `rotated_wind`/`unrotated_wind` | **No calza.** No existe ningún campo para `u*`, huella (`x_peak`, `x_50%`, etc.) ni viento — son específicos del método EC y no se contemplaron al diseñar `TorreEc` (que solo guarda metadatos fijos de instalación, no mediciones). |
| `diagnostic_flags_LI-7200` / `diagnostic_flags_LI-7700`, `spikes`, `statistical_flags` | **No calza.** Son diagnósticos de calidad propios del método EC, sin equivalente en el modelo. |
| `variances`/`covariances`, `storage_fluxes`, `uncorrected_fluxes` | **No calza.** Sin lugar en el modelo actual. |

**Conclusión preliminar:** de las 169 columnas, solo un subconjunto pequeño de variables meteorológicas básicas (temperatura, humedad, presión) tendría dónde ir reutilizando `MuestraAmbiental` — y aun así, perdiendo la asociación directa con la torre (`MuestraAmbiental` cuelga de `UnidadMuestreo`, no de `TorreEc`). **Los flujos en sí (`co2_flux`, `ch4_flux`, `h2o_flux`, `H`, `LE`) y toda la turbulencia/footprint no tienen dónde cargarse hoy.** Esto confirma que se necesita un modelo nuevo (o una extensión significativa) para series de tiempo de torre EC.

**Decisión (2026-09-30):** se define subir la salida de **Eddypro**, no la de ReddyProc — ver justificación completa en la sección "Integración en Colflux" de [docs/conocimiento/datos-torres-eddypro-reddyproc.md](../../docs/conocimiento/datos-torres-eddypro-reddyproc.md) (trazabilidad/control de calidad propio sobre el filtrado y gap-filling, consistencia entre torres que no necesariamente tienen postprocesamiento ReddyProc homogéneo, y porque Eddypro ya trae las correcciones físicas estándar aplicadas). ReddyProc se trata como dato derivado y opcional.

**Diseño del modelo nuevo (2026-09-30):** tres entidades — `MuestraTorre` (ancla de identidad: torre + fecha + hora), `SubmuestraEddy` (obligatoria, 1:1, los campos de Eddypro) y `SubmuestraReddy` (opcional, 0:1, los campos de ReddyProc — solo existe si la torre tiene ese postprocesamiento). Diseño completo, diagrama ER y justificación en [docs/arquitectura/modelo-datos-torre-ec.md](../../docs/arquitectura/modelo-datos-torre-ec.md). Propuesta pendiente de validar con el equipo de backend antes de implementarla.

## Entregables

- [docs/conocimiento/datos-torres-eddypro-reddyproc.md](../../docs/conocimiento/datos-torres-eddypro-reddyproc.md) — explicación del pipeline Eddypro → ReddyProc y las columnas de Eddypro.
- Mapeo de columnas vs. modelo actual (tabla arriba).

## Referencias

- `backend/app/models/torre.py`
- `backend/app/models/co2.py`
- [[modelo-datos-categorias]] — paleta de categorías del catálogo, incluye "Torre EC y Flujos" y "Muestras GEI"
- [[cargar-datos-torre-guatavita-eddypro]] — tarea de continuación: implementar el modelo propuesto y cargar el archivo real de Eddypro.
- [docs/conocimiento/datos-torres-eddypro-reddyproc.md](../../docs/conocimiento/datos-torres-eddypro-reddyproc.md)

## Historial

| Fecha | Descripción |
|---|---|
| 2026-09-30 | Se crea la tarea, a partir de los dos archivos de la torre Guatavita ST2 compartidos por correo (Alejandro Delgado, 2026-09-29) y de la revisión inicial de `TorreEc`/`MuestraGEI` en el backend, que sugiere que el modelo actual está pensado para mediciones manuales por cámara y no para series de tiempo continuas de torre EC. |
| 2026-09-30 | Se revisa a fondo el `eddypro_..._adv.csv` (169 columnas, 6848 filas semihorarias de 2024). Se documenta el significado de cada grupo de columnas en `docs/conocimiento/datos-torres-eddypro-reddyproc.md`. Se mapea contra `TorreEc`, `MuestraGEI`/`SubmuestraGEI` y `MuestraAmbiental`: solo un subconjunto de variables meteorológicas básicas tendría dónde ir reutilizando `MuestraAmbiental`; los flujos (`co2_flux`, `ch4_flux`, `h2o_flux`, `H`, `LE`), la turbulencia y el footprint no tienen dónde cargarse hoy. |
| 2026-09-30 | Se define subir la salida de Eddypro (no la de ReddyProc) a la plataforma. Se documenta la justificación en la sección "Integración en Colflux" de `docs/conocimiento/datos-torres-eddypro-reddyproc.md`. El CSV de ReddyProc sigue sin descargarse en `files/archivos-torres/`, pero deja de ser bloqueante para el diseño del modelo nuevo, ya que ese modelo debe cubrir las columnas de Eddypro. |
| 2026-09-30 | Se decide el modelo nuevo: tres entidades (`MuestraTorre`, `SubmuestraEddy` obligatoria, `SubmuestraReddy` opcional), en vez de reutilizar `MuestraGEI`/`SubmuestraGEI`. Se documenta diseño completo, diagrama ER y justificación en `docs/arquitectura/modelo-datos-torre-ec.md` (propuesta, pendiente de validar con el equipo de backend). Con esto se cierran los pasos 4 y 5 del plan; queda pendiente la implementación real en el backend y completar la sección de ReddyProc en el documento de conocimiento cuando se tenga el archivo. |
| 2026-10-01 | Se cierra la tarea: los 5 pasos del plan quedaron completos (validación del modelo actual, documentación de columnas, mapeo, decisión de modelo nuevo y documentación en `docs/arquitectura/`). La implementación real (modelos, migración, carga, API, frontend) continúa en [[cargar-datos-torre-guatavita-eddypro]]. |
