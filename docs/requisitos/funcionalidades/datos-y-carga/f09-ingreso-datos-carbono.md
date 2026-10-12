# F09 — Ingreso de datos de carbono (formulario)

**Categoría:** Datos y Carga

## Objetivo

Permitir la carga manual de mediciones de carbono, con validaciones por campo
(obligatoriedad, tipo, tamaño de archivo).

## Contexto

El catálogo original dejó pendiente: ¿fuentes de datos (archivos de aliados, tomas de
campo, reporte ciudadano)? ¿qué usuarios pueden ingresar? ¿formatos de carga? ¿dónde se
almacenan? ¿hay datos de reservas de carbono? ¿se pueden medir factores de emisión
directamente?

## Qué hay

El ingreso de datos no es un formulario de campos individuales por medición, sino un
flujo de carga de archivos (Excel/CSV) vía ETL: `FuenteDatos` (`app/models/datos.py`)
con `tipo` (excel/csv/shapefile/geojson/api/base_de_datos) y `estado`, `CargaArchivo`
con estados `subido→mapeado→validado→importado`, y `MapeoColumna` que define cómo cada
columna se transforma al modelo destino. El frontend
(`frontend/src/pages/ReportarFormulario.tsx:13-45`) valida extensión de archivo
(`.xlsx/.xls/.csv`) antes de subir, y conversa con un asistente de IA
(`app/api/ia_carga/views.py`) que propone el mapeo. Los modelos de dato real son
`MuestraGEI`/`SubmuestraGEI` (`app/models/co2.py`) para flujos CO2/CH4/N2O, más
`MuestraBiomasa`, `SubmuestraSuelo` (COS), `MuestraMOM` — no hay un modelo explícito de
"reservas de carbono" ni de "factor de emisión" como entidad propia. Solo usuarios con
`nivel >= reportador` pueden escribir (`app/api/permisos.py: EscrituraRequiereReportador`).

## Qué hace falta

- No hay distinción explícita de "fuente" como aliado/campo/reporte ciudadano más allá
  del tipo de archivo; el nivel `ciudadano` es solo lectura, así que el "reporte
  ciudadano" como fuente de ingreso de datos no está implementado.
- No existe un modelo de "reserva de carbono" (stock) separado de flujo, ni un
  campo/flujo para capturar directamente un "factor de emisión" (coeficiente) — solo se
  cargan mediciones crudas (`SubmuestraGEI.valor`).
- El almacenamiento es Postgres/PostGIS vía los modelos ya descritos (eso sí está
  resuelto).
