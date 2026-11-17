# Ajustes a la plantilla Flujos CO2 (cámaras GEI) — feedback de Andrea Chaparro

**Estado:** en curso
**Creada:** 2026-11-17
**A cargo:** Vivi
**Sesión de Claude Code:** https://claude.ai/code/session_019pTWH1VVV5qHSiima6aXfq

## Objetivo

Aplicar el feedback que Andrea Chaparro envió (WhatsApp, 2026-11-13) sobre la
plantilla de Flujos CO2 (cámaras GEI) — ver
[diccionario de datos](../../docs/arquitectura/plantilla-metadato-dato-co2-camaras.md)
y la implementación en `backend/app/api/etl/views.py`.

## Contexto

Mensajes originales (2026-11-13, 11:11 a.m.):

> Borrar fecha de instalación de unidad de muestreo
> Mes y año se pueden extraer de la fecha -> quitar y solo dejar date
> Datos de la investigación (investigador y su correo) que vayan en su propia
> pestaña; que vayan datos del investigador principal y el investigador pueda
> poner si tuvo colaboradores.
> Quitar periodicidad de muestreo porque se puede calcular solo.
>
> Borrar tubo
> Rellenar con N/A los espacios vacíos
> ———-
> Si no hay dato de carbono/coordenadas, quitar la fila completa
>
> Region, vereda, municipio y departamento que se haga la prueba trayendo las
> coordenadas pero que no se toque el sitio

## Plan

Alcance acotado por la usuaria (2026-11-17): de los puntos originales de
Andrea, se implementan 1/2/3/4 en esta sesión; el punto de región/vereda/
municipio/departamento vía coordenadas queda **fuera de esta tarea**, como
spike aparte (ver [[plantilla-flujos-co2-geocodificacion-inversa]] — crear
cuando se retome).

- [x] **Quitar `fecha_instalacion_unidad_muestreo`** (`UnidadMuestreo.fecha_instalacion`)
  de la hoja Metadato — excluido en `campos["UnidadMuestreo"]["excluir"]` y
  sacado de `_ORDEN_COLUMNAS_METADATO_GEI_PLANTILLA`
  (`backend/app/api/etl/views.py`). El campo del modelo no se toca.
- [x] **Quitar `tubo`** (`MuestraGEI.tubo`) de la hoja Dato — excluido en
  `campos["MuestraGEI"]["excluir"]` y sacado de
  `_ORDEN_COLUMNAS_DATO_GEI_PLANTILLA`. Confirmado que no participaba de
  `_LLAVE_REFERENCIA_GEI` (esa llave es `UnidadMuestreo.codigo_metadato` desde
  el 2026-11-09) ni de ningún otro cruce — sin impacto.
- [x] **Pestaña "Responsables"** — alcance redefinido por la usuaria: no es
  "investigador principal + colaboradores" (eso hubiera requerido modelo
  nuevo/migración), sino exponer lo que ya existe en `FuenteDatos` al momento
  de crearla (`proyecto`, `institucion`, `reportador`). Implementado en
  `exportar_bronce` (descarga "⬇ Descargar Excel" de la vista tipo Excel/
  bronce, `/etl/upload-bronce`) como hoja nueva de una sola fila:
  `nombre_proyecto`, `entidad_encargada`, `persona_responsable`,
  `correo_responsable` (`Usuario.correo_institucional` con fallback a
  `Usuario.correo`). **No se agregó a `plantilla_vacia`** (la plantilla en
  blanco de `/participacion`) porque esa descarga no está atada a ninguna
  `FuenteDatos` todavía.
- [x] **Eliminar columnas completas sin datos al descargar** — ya existía
  `_quitar_columnas_vacias()` (usada en `exportar_carga`/`exportar_proyecto`
  desde antes) pero no se aplicaba en `exportar_bronce`; se agregó ahí mismo,
  por hoja, antes de escribir el Excel.
- [ ] "Periodicidad de muestreo" y "mes/año": sin acción — ya estaban
  resueltos antes de este feedback (periodicidad descartada 2026-11-02,
  mes/año nunca existieron como columnas separadas, solo `fecha_toma`).
  Confirmar con Andrea si "mes/año" se refería a otra plantilla (ej. Torre
  EC) antes de cerrar del todo este punto.
- [ ] Región/vereda/municipio/departamento desde coordenadas — explícitamente
  pospuesto, no se toca en esta tarea.

Verificado en vivo (`docker compose exec web python manage.py shell`,
`manage.py check` limpio, `npx tsc --noEmit` limpio en frontend — no se tocó
frontend en esta tarea): `_hojas_plantilla_vacia()` ya no trae
`fecha_instalacion_unidad_muestreo` ni `tubo`; `exportar_bronce` sobre una
carga real (fuente 74, carga 358) devuelve 3 hojas (`Flujos CO2 - Dato`,
`Flujos CO2 - Metadato`, `Responsables`) con la fila de responsable/proyecto/
entidad correcta.

## Entregables

- [Diccionario de datos actualizado](../../docs/arquitectura/plantilla-metadato-dato-co2-camaras.md)
  (sin las dos columnas, con la sección nueva "Hoja Responsables").
- `backend/app/api/etl/views.py` — cambios en `_VISTAS_DESNORMALIZADAS["submuestra_gei"]["campos"]`,
  `_ORDEN_COLUMNAS_METADATO_GEI_PLANTILLA`, `_ORDEN_COLUMNAS_DATO_GEI_PLANTILLA`, `exportar_bronce`.

## Referencias

- [Diccionario de datos de la plantilla](../../docs/arquitectura/plantilla-metadato-dato-co2-camaras.md)
- `backend/app/api/etl/views.py` — `_ORDEN_COLUMNAS_METADATO_GEI_PLANTILLA`, `_ORDEN_COLUMNAS_DATO_GEI_PLANTILLA`, `_HOJAS_PLANTILLA`, `_LLAVE_REFERENCIA_GEI`
- [[rediseno-carga-flujos-co2-staging-bronce]]

## Historial

| Fecha | Descripción |
|---|---|
| 2026-11-17 | Se crea la tarea con el feedback de Andrea (2026-11-13) desglosado en 4 bloques. Nada implementado todavía. |
| 2026-11-17 | Se acota el alcance con la usuaria e implementan 4 puntos: quitar `fecha_instalacion_unidad_muestreo` y `tubo` de la plantilla, pestaña "Responsables" (proyecto/entidad/reportador, tomados de `FuenteDatos`) en `exportar_bronce`, y eliminar columnas vacías también en `exportar_bronce` (reutilizando `_quitar_columnas_vacias`). Verificado en vivo. Quedan pendientes: confirmar con Andrea el punto "mes/año" (parece ya resuelto de antes), "rellenar vacíos con N/A" (sin definir alcance), "quitar fila completa sin dato/coordenadas" (sin definir alcance) y el spike de geocodificación (explícitamente fuera de esta tarea). |
