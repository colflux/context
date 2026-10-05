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

- [ ] Crear los modelos nuevos (`MuestraTorre`, `SubmuestraEddy`, `SubmuestraReddy`) y su migración en `backend/app/models/`, siguiendo el diseño de `docs/arquitectura/modelo-datos-torre-ec.md`.
- [ ] Escribir un script/management command que lea el CSV de Eddypro y mapee cada fila a `MuestraTorre` + `SubmuestraEddy` para la torre Guatavita ST2.
- [ ] Crear una vista agregada diaria en Postgres (`VIEW` o `MATERIALIZED VIEW`) que promedie los flujos por torre+día, descartando filas con `qc_* = 2` (calidad "descartar").
- [ ] Exponer esos datos en la API (serie diaria agregada, y detalle semihorario si se necesita).
- [ ] Crear la vista en el frontend para visualizar los datos de la torre (selector de torre → variable → gráfica de serie de tiempo).

## Entregables

(Pendiente — se completa al cerrar la tarea.)

## Referencias

- [[datos-modelado-carga-torres]] — validación del modelo y diseño de las entidades nuevas.
- [docs/arquitectura/modelo-datos-torre-ec.md](../../docs/arquitectura/modelo-datos-torre-ec.md) — diseño detallado, pendiente de validar con el equipo.
- [docs/conocimiento/datos-torres-eddypro-reddyproc.md](../../docs/conocimiento/datos-torres-eddypro-reddyproc.md) — qué significan las columnas del archivo.
- `files/archivos-torres/eddypro_Guatavita_2_2024_full_output_2025-04-27T022924_adv.csv`
- `backend/app/models/torre.py`, `backend/app/models/co2.py`

## Historial

| Fecha | Descripción |
|---|---|
| 2026-09-30 | Se crea la tarea, como continuación de [[datos-modelado-carga-torres]], para implementar el modelo propuesto y cargar el archivo real de Eddypro de Guatavita ST2. |
