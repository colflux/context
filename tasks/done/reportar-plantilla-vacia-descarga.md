# Botón de descarga de plantilla vacía para reporte de datos

**Estado:** hecho
**Creada:** 2026-10-05
**A cargo:** Viviana Bautista
**Sesión de Claude Code:** sesión actual (ver transcript local)

## Objetivo

Agregar una tercera opción en el hub de reporte (`/reportar`) para que un actor
territorial descargue un Excel vacío con los campos del modelo de datos
(metodologías Flujos, MOM, COS y Biomasa), lo llene, y lo suba por el
formulario web existente — reduciendo el trabajo de mapeo manual/IA porque las
columnas ya coinciden con los nombres de campo reales.

## Contexto

Idea de Viviana: en vez de depender solo del mapeo asistido por IA al subir un
archivo arbitrario (`ReportarFormulario.tsx` → `iaCargaService`), dar una
plantilla con las columnas ya nombradas igual que el modelo. Requisitos
pedidos:

1. Que la plantilla se actualice sola conforme cambia el modelo de datos (no
   un archivo estático mantenido a mano).
2. Que incluya el diccionario de datos y los colores de categoría que ya se
   usan en el diagrama ERD (`/db`).
3. Que por ahora cubra las metodologías Flujos, MOM, COS y Biomasa (no series
   temporales todavía).

Al explorar `backend/app/api/etl/views.py` se encontró que `exportar_carga` /
`exportar_proyecto` ya arman un Excel con hoja "Diccionario de datos"
coloreada por categoría (`COLOR_POR_MODELO`, derivado de `GRUPOS_CATALOGO` en
`app/catalogo/generator.py`) a partir de datos reales ya cargados. La pieza
que faltaba era una versión "solo encabezados, sin filas" reutilizando la
misma definición de columnas (`_VISTAS_DESNORMALIZADAS` /
`_columnas_de_vista`), que no depende de que existan datos — así el requisito
1 queda resuelto gratis: si un campo se agrega/renombra en Django, la próxima
descarga ya sale actualizada sin tocar la plantilla.

## Plan

- [x] Backend: nueva vista `plantilla_vacia` en `app/api/etl/views.py` — una
      hoja por metodología (Unidad Muestreo-Experimental, Flujos CO2, Flujos
      CH4, MOM, COS, Biomasa) con encabezados coloreados por categoría, más
      hoja "Diccionario de datos" (reutiliza `_agregar_hoja_diccionario_datos`,
      `_colorear_encabezados`). Protegida con `@requiere_nivel("reportador")`.
- [x] Registrar ruta `GET /api/etl/plantilla/` en `app/api/urls.py`.
- [x] Frontend: nueva card "Plantilla de datos" en `Participacion.tsx`, botón
      que llama `datosService.getPlantillaVaciaUrl()` + `downloadFile()` (ya
      existía ese helper para `exportar_carga`/`exportar_proyecto`).
- [x] Verificar en navegador real (clic → request a `/api/etl/plantilla/` →
      200 OK) y por curl (estructura de hojas/encabezados del `.xlsx`
      generado).

## Entregables

- `backend/app/api/etl/views.py`: `_HOJAS_PLANTILLA`, `plantilla_vacia`.
- `backend/app/api/urls.py`: ruta `etl-plantilla-vacia`.
- `frontend/src/services/datos.service.ts`: `getPlantillaVaciaUrl`.
- `frontend/src/pages/Participacion.tsx`: card "Plantilla de datos".

## Referencias

- `backend/app/api/etl/views.py` (`_VISTAS_DESNORMALIZADAS`,
  `_columnas_de_vista`, `exportar_carga`/`exportar_proyecto` como precedente)
- `backend/app/catalogo/generator.py` (`GRUPOS_CATALOGO`, `COLOR_POR_MODELO`)
- `frontend/src/utils/download.ts` (`downloadFile`)
- [[wiki-manual-usuario]] — la guía de "cómo reportar datos" ya documentada en
  la wiki; la plantilla es un atajo adicional, no reemplaza esa guía.

## Historial

| Fecha | Descripción |
|---|---|
| 2026-10-05 | Se crea e implementa: endpoint de plantilla vacía dinámica + card de descarga en el hub de reporte. Pendiente como posible mejora futura (no pedida en esta sesión): al subir el Excel ya llenado con esta plantilla, detectar que los encabezados coinciden exactamente con el modelo y saltar/acelerar el paso de mapeo con IA en `ReportarFormulario.tsx` — hoy ese archivo pasa por el mismo flujo de mapeo asistido que cualquier archivo arbitrario. |
