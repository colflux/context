# Subir directo a la base de datos un archivo que ya tiene la plantilla (sin pasar por el asistente de mapeo)

**Estado:** en curso — implementado, falta desplegar al contenedor compartido y probar en vivo
**Creada:** 2026-11-09
**A cargo:** Viviana
**Sesión de Claude Code:** https://claude.ai/code/session_019pTWH1XKsvNNawB2zGYDNo

## Objetivo

Cuando un archivo ya trae los encabezados exactos de la plantilla descargable
("Descargar plantilla" en Reportar → Flujos CO2/CH4), evitar el asistente
manual de mapeo de columnas (`EtlUpload.tsx` paso 4): mapear automático y
subir directo a la base de datos, con una casilla "Ya tiene el formato de la
plantilla" en el drawer "Nueva fuente de datos".

## Contexto

Surgió al transformar un archivo real de IDEAM a la estructura de la
plantilla (`datos-test/IDEAM CO2 - plantilla.xlsx`, ver sesión): una vez que
un archivo ya calza exacto con la plantilla, pasar por el asistente manual
(elegir modelo/campo por columna, uno por uno) es trabajo repetido e
innecesario — la plantilla ya ES literalmente la lista de `modelo.campo` de
cada columna (`_hojas_plantilla_vacia()`, `backend/app/api/etl/views.py`).

**No se salta la validación**: solo se salta el paso manual de asignar
modelo/campo a cada columna. El archivo sigue pasando por
`validar_carga`/`previsualizar_carga` (vía `_preparar_importacion` dentro de
`importar_carga`) antes de guardar cualquier fila — igual que el asistente
manual, que tampoco tiene un paso de previsualización separado antes de
"Validar y guardar": valida e importa en el mismo click, mostrando errores
inline si algo falla. El mapeo automático sigue ese mismo patrón ya
establecido en el código, no inventa uno nuevo.

**Alcance actual: solo Flujos CO2.** Es la única metodología con hojas
Metadato/Dato separadas en `_HOJAS_PLANTILLA` (ver
`tasks/backlog/subida-descarga-formato-metadato-dato-por-metodologia.md`,
pendiente para COS/Biomasa/MOM/CH4/torre EC). Para esas metodologías la
casilla no aparece — el archivo sigue el asistente manual de siempre.

**Columnas que no se pueden auto-mapear (caen al asistente manual):**
algunas columnas de la hoja Metadato comparten `modelo.campo` pero se
distinguen por un dato extra que no está en el nombre de la columna
(`MapeoColumna.tipo_cobertura`, ver `docs/arquitectura/modelo-cobertura.md`):
`ecosistema_IDEAM` SÍ es única (auto-mapeable), pero `cobertura_IPCC` /
`cobertura_CLC` / `cobertura_IGBP` / `cobertura_Nombre_Local` /
`uso_suelo_IPCC` / `tipo_disturbio` / `cobertura_vegetal_primaria` /
`cobertura_vegetal_secundaria` / `cobertura_vegetal_terciaria` (las 9
columnas que usan `ValorClasificacionTipo.valor`), más
`porc_cobertura_vegetal_*` (`CoberturaManual.porcentaje`, 3 columnas) y
`distancia_*` (`ExposicionExterna.distancia_m`, 4 columnas) quedan **sin
auto-mapear** — 16 columnas de las 44 de Metadato (verificado en vivo contra
el contenedor, 2026-11-09). La hoja Dato (19 columnas) es enteramente
auto-mapeable: ninguna de sus columnas repite `modelo.campo`.

Si una hoja trae alguna columna sin match exacto de nombre, o alguna de esas
16 ambiguas, esa hoja completa queda sin auto-mapear (todo o nada por hoja)
y el usuario la completa a mano en el asistente — las demás hojas del mismo
archivo que sí calzaron ya quedan importadas.

## Plan

- [x] Backend: `_sugerir_mapeos_automaticos(carga)` en
      `backend/app/api/etl/views.py` — compara encabezados del archivo
      contra `_hojas_plantilla_vacia()` por hoja, detecta columnas sin
      match y columnas ambiguas (mismo `modelo.campo` repetido).
- [x] Backend: endpoint `GET
      /api/fuentes-datos/<fuente_id>/carga/<carga_id>/mapeo-automatico/`
      (`mapeo_automatico`, solo lectura) + ruta en `backend/app/api/urls.py`.
- [x] Frontend: casilla "Ya tiene el formato de la plantilla" en
      `FuenteDrawer.tsx`, visible solo para metodología Flujos (CO2/CH4) y
      no-torre. Al guardar con la casilla marcada, navega a
      `/etl/upload?fuente=<id>&auto=1` en vez de cerrar el drawer sin más.
- [x] Frontend: `EtlUpload.tsx` — con `?auto=1`, en cuanto termina el
      análisis automático del archivo (mismo auto-análisis que ya existía
      para fuentes con archivo registrado) pide la sugerencia, postea el
      mapeo de cada hoja que matcheó exacto (`postMapeo` existente,
      `transformacion: "directo"`), y dispara la importación de todas las
      secciones (`iniciarImportarSeccion` + polling de
      `estadoImportacion`, reutilizando el mismo patrón que
      `useImportarSeccion`). Aterriza directo en el paso 4 con un banner de
      estado (aplicando / parcial / error); si alguna hoja quedó sin
      matchear, deja esa hoja activa en el asistente normal para
      completarla a mano, sin perder lo ya importado de las demás.
- [x] `npx tsc --noEmit` y `npx eslint` limpios en los archivos tocados.
- [ ] Desplegar al contenedor compartido (`docker compose cp` + `restart
      web` en `backend/`, mismo mecanismo que el resto de la sesión) —
      pendiente de confirmación explícita antes de tocar el RDS compartido.
- [ ] Probar en vivo con un archivo real (ej. `datos-test/IDEAM CO2 -
      plantilla.xlsx`, que calza con la hoja Dato completa pero NO con
      Metadato — trae varias de las 16 columnas ambiguas, así que esa hoja
      caería al asistente manual con este archivo en particular).
- [ ] Evaluar si vale la pena resolver las 16 columnas ambiguas de Metadato
      (requeriría mapear el sufijo de cada `clave` a un
      `ClasificacionTipo.nombre` real vía `tipo_cobertura` — fuera de
      alcance de esta iteración).

## Entregables

- `backend/app/api/etl/views.py`: `_sugerir_mapeos_automaticos`, `mapeo_automatico`.
- `backend/app/api/urls.py`: ruta `mapeo-automatico`.
- `frontend/src/components/admin/fuentes/FuenteDrawer.tsx`: casilla + navegación.
- `frontend/src/pages/EtlUpload.tsx`: flujo de mapeo automático + banners de estado.
- `frontend/src/services/etl.service.ts`, `frontend/src/types/index.ts`: `getMapeoAutomatico`, `MapeoAutomaticoResponse`.

## Referencias

- [Plantilla de carga/descarga: metadato y dato de CO2/CH4](../../docs/arquitectura/plantilla-metadato-dato-co2-camaras.md)
- [Rediseñar vista de subida/descarga: separar metadato y dato por metodología](../backlog/subida-descarga-formato-metadato-dato-por-metodologia.md)
- [Opción de incluir Clima en la misma hoja de Flujos CO2](../backlog/plantilla-flujos-co2-clima-misma-hoja.md)
- `docs/arquitectura/modelo-cobertura.md` — por qué las 16 columnas de clasificación quedan ambiguas.

## Historial

| Fecha | Descripción |
|---|---|
| 2026-11-09 | Se crea la tarea a partir del pedido de usuario ("casilla de seleccionar si ya tiene la plantilla... suba los datos directo a la base de datos sin necesidad de ETL"). Implementado backend (endpoint de sugerencia) y frontend (casilla + flujo automático en EtlUpload.tsx), con `tsc`/`eslint` limpios. Queda pendiente desplegar al contenedor compartido y probar con un archivo real antes de dar la tarea por cerrada. |
