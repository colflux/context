# Cargar datos reales de la torre Guatavita ST2 (Eddypro) a la plataforma

**Estado:** pendiente
**Creada:** 2026-09-30
**A cargo:** Viviana
**Participantes:** Viviana
**Sesión de Claude Code:** https://claude.ai/code/session_015orBkh6stAo8qWMr6sp28t

## Objetivo

Implementar el modelo nuevo diseñado en [[datos-modelado-carga-torres]] y cargar el archivo real de Eddypro de la torre Guatavita ST2 a la plataforma, dejando los datos visibles en el frontend.

## Contexto

Sigue directamente de [[datos-modelado-carga-torres]], donde se validó que el modelo actual (`MuestraGEI`/`SubmuestraGEI`) no sirve para datos de torre EC y se diseñó una propuesta de 3 entidades nuevas (documentada en `docs/arquitectura/modelo-datos-torre-ec.md`, pendiente de validar con el equipo de backend).

Solo se tiene descargado el archivo de **Eddypro** (`files/archivos-torres/eddypro_Guatavita_2_2024_full_output_2025-04-27T022924_adv.csv`). El de **ReddyProc** (`Guatavita_2_ReddyProc_2023_2024_output (1).csv`, compartido por Alejandro Delgado el 2026-09-29) sigue sin descargarse del correo — por eso esta tarea cubre solo `SubmuestraEddy`; `SubmuestraReddy` queda sin poblar para esta torre hasta tener ese archivo.

## Plan

- [x] ~~Crear los modelos nuevos (`MuestraTorre`, `SubmuestraEddy`, `SubmuestraReddy`) y su migración~~ — hecho (commit `5a31897`), pero se reemplazan por la revisión diaria del siguiente ítem.
- [ ] Crear `MuestraTorreDiaria`/`SubmuestraEddyDiaria`/`SubmuestraReddyDiaria` y su migración en `backend/app/models/`, reemplazando a las 3 semihorarias (sin datos cargados), siguiendo el diseño en "Revisión (2026-11-01)" de `docs/arquitectura/modelo-datos-torre-ec.md`.
- [ ] Conectar torre EC al motor ETL genérico (`CargaArchivo`/`MapeoColumna` en `backend/app/api/etl/views.py`) en vez de un script ad-hoc: leer el CSV de Eddypro (y de ReddyProc si está disponible), calcular el promedio diario por torre (descartando filas `qc_* = 2`) y guardarlo en las entidades diarias.
- [ ] Definir y cargar el 3er archivo (metadata de la carga) — formato todavía sin definir, pendiente de un ejemplo real.
- [ ] Exponer esos datos en la API (serie diaria por torre).
- [ ] Crear la vista en el frontend para visualizar los datos de la torre (selector de torre → variable → gráfica de serie de tiempo) — conecta con [[reportar-separar-por-metodologia]].

## Entregables

(Pendiente — se completa al cerrar la tarea.)

## Referencias

- [[datos-modelado-carga-torres]] — validación del modelo y diseño de las entidades nuevas.
- [docs/arquitectura/modelo-datos-torre-ec.md](../../docs/arquitectura/modelo-datos-torre-ec.md) — diseño detallado, pendiente de validar con el equipo.
- [docs/conocimiento/datos-torres-eddypro-reddyproc.md](../../docs/conocimiento/datos-torres-eddypro-reddyproc.md) — qué significan las columnas del archivo.
- `files/archivos-torres/eddypro_Guatavita_2_2024_full_output_2025-04-27T022924_adv.csv`
- `backend/app/models/torre.py`, `backend/app/models/co2.py`
- [[subida-descarga-formato-metadato-dato-por-metodologia]] — separación metadato/dato por metodología, pendiente de repetir para torre EC.
- [[reportar-separar-por-metodologia]] — rediseño de la vista `Reportar` por metodología (equipo vs. torres para CO2/CH4), depende del modelo de datos que se defina acá.

## Historial

| Fecha | Descripción |
|---|---|
| 2026-09-30 | Se crea la tarea, como continuación de [[datos-modelado-carga-torres]], para implementar el modelo propuesto y cargar el archivo real de Eddypro de Guatavita ST2. |
| 2026-11-01 | Se revisa el estado real del backend: los modelos `MuestraTorre`/`SubmuestraEddy`/`SubmuestraReddy` ya existen (commit `5a31897`), pero nada los carga, expone en API ni en catálogo todavía — el primer paso del plan está hecho de facto aunque seguía sin marcar. Se empieza a redefinir el alcance: en vez de un script ad-hoc, conectar torre EC al motor ETL genérico (`CargaArchivo`/`MapeoColumna`), y se abre la duda de si en BD se guarda el detalle semihorario, solo el promedio diario, o ambos — **se define que solo se guarda el promedio diario** por torre+día, calculado a partir de los archivos Eddypro (dato primario) y ReddyProc (opcional). Queda pendiente definir el modelo de datos concreto para esa agregación diaria (reemplazando o adaptando las 3 entidades semihorarias ya creadas) y el formato del tercer archivo (metadata de la carga), todavía sin un ejemplo real para diseñarlo. Surge también [[reportar-separar-por-metodologia]], como rediseño de interfaz relacionado. |
| 2026-11-01 | Se cierra el diseño del modelo diario: 3 entidades nuevas (`MuestraTorreDiaria`, `SubmuestraEddyDiaria`, `SubmuestraReddyDiaria`) que reemplazan a las semihorarias — documentado en la sección "Revisión (2026-11-01)" de `docs/arquitectura/modelo-datos-torre-ec.md`. Cambios clave respecto al diseño semihorario: ancla por torre+fecha (no hora), `MuestraTorreDiaria` suma FK a `CargaArchivo` para trazabilidad y `n_registros_validos`, y los flags `qc_*` por fila se resumen en un único `pct_calidad_buena` por día. Se anota como tensión abierta (no bloqueante) que esto choca con el principio de "guardar siempre el dato bronze/crudo" de la propuesta `calidad-datos-zonas.md`, todavía no decidida. Queda pendiente implementar los modelos/migración en el backend, el formato del archivo de metadata (sin ejemplo real) y conectar todo al motor ETL genérico. |
