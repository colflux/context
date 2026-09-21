# Definir paleta de colores por categoría del modelo de datos

**Sesión de Claude:** session_01YUBhkSM9LKVCC5CYhFzgSf
**Estado:** en progreso
**Creada:** 2026-09-17

## Objetivo

Definir una paleta de colores única (sin repetidos) para las 12 categorías del
modelo de datos, y usarla para colorear el Excel exportado desde
[[etl-datos]] (`/etl/datos`) por categoría de columna — sale de la tarea
[[datos-swap]], donde primero se arregló el bug de permisos al descargar y
ahora se quiere mejorar el formato de la descarga.

## Contexto

El modelo de datos ya está agrupado en 12 categorías, definidas en
`backend/app/catalogo/generator.py` (`GRUPOS_CATALOGO`) y coloreadas en
`frontend/src/utils/catalogoModel.ts` (`GRUPO_PALETTE`) para el diagrama ERD
de `/db` (Modelo de Base de Datos). El problema: `GRUPO_PALETTE` solo tiene
9 colores para 12 categorías, así que se reciclan por índice
(`idx % 9`) — y una de esas repeticiones sí afecta al Excel exportado:
"Muestras GEI" (Equipo, MuestraGEI, UnidadMedida, MuestraAmbiental — usados
en las hojas CO2/CH4/Clima) cae en el mismo color que "Publicaciones" (que
no aparece en el export).

## Categorías (`GRUPOS_CATALOGO`) y sus entidades

| # | Categoría | Entidades |
|---|---|---|
| 0 | Publicaciones | PublicacionType, Publicacion, Autor |
| 1 | Geografía | Region, Departamento, Municipio, Sitio |
| 2 | Unidad de Muestreo y Experimental | UnidadMuestreoTipo, UnidadMuestreo, UnidadExperimental, Parcela, Transecto |
| 3 | Cobertura y Vegetación | TipoCobertura, Cobertura, Vegetacion, Disturbio |
| 4 | Suelo | CaracterizacionMuestreoSuelo, MonitoreoSuelo |
| 5 | Carbono Orgánico del Suelo (COS) | SubmuestraSuelo |
| 6 | Biomasa | MuestraBiomasa, IndividuoArboreo |
| 7 | Materia Orgánica Muerta (MOM) | MuestraMOM |
| 8 | Torre EC y Flujos | TorreEc, ConfiguracionSensorGas |
| 9 | Muestras GEI | UnidadMedida, Equipo, TipoMuestra, MuestraAmbiental, MuestraGEI, SubmuestraGEI |
| 10 | Proyecto | Proyecto, Institucion, ProyectoInstitucion, ProyectoUsuario |
| 11 | Usuarios, Roles y ETL | Usuario, RolUsuario, FuenteDatos, CargaArchivo, MapeoColumna |

De estas, las que hoy aparecen como columnas en el Excel exportado (hojas
CO2, CH4, Unidad Muestreo-Experimental, Clima, MOM, COS, Biomasa) son:
**Geografía** (Sitio), **Unidad de Muestreo y Experimental**, **Muestras
GEI**, **MOM**, **COS**, **Biomasa**. Suelo, Cobertura y Vegetación,
Publicaciones, Torre EC y Flujos, Proyecto y Usuarios/Roles/ETL no aparecen
en el export actual.

## Plan

- [x] Localizar la fuente de colores existente (`catalogoModel.ts` +
      `generator.py`) y confirmar el problema de reciclado de paleta
- [x] Viviana confirmó por texto los 12 valores hex finales (ver "Paleta
      confirmada" abajo) — incluye 3 pares de categorías con el mismo color
      a propósito
- [x] Choque Geografía / Unidad de Muestreo y Experimental (ambas
      `#0f8139`): primero Viviana pidió dejarlas iguales, pero al ver el
      Excel real confirmó que sí se necesitaba distinguirlas — se le puso
      a "Unidad de Muestreo y Experimental" el color `#ff6f61` (rojo
      camarón / coral)
- [x] `GRUPOS_CATALOGO` en `backend/app/catalogo/generator.py` ahora lleva
      el campo `"color"` por grupo (fuente única de verdad) + se agregó
      `COLOR_POR_MODELO` (modelo → color) derivado del mismo diccionario
- [x] `catalogo.json`/`catalogo.js` regenerados (`python manage.py
      generate_catalogo`) y copiados a `frontend/src/assets/data/catalogo.json`
- [x] `frontend/src/types/index.ts` (`GrupoCatalogo`) y
      `frontend/src/utils/catalogoModel.ts` actualizados: `colorDeGrupo`
      ahora lee `grupo.color` directo del catálogo en vez de derivarlo por
      índice de una paleta cíclica de 9 colores (`GRUPO_PALETTE` eliminado)
- [x] Aplicado el color por categoría a los encabezados del Excel
      exportado: nuevo helper `_colorear_encabezados()` en
      `app/api/etl/views.py`, usado en `exportar_carga` y
      `exportar_proyecto` (vía openpyxl `PatternFill`/`Font`, columna a
      columna según `columnas[i]["modelo"]` → `COLOR_POR_MODELO`)
- [x] Probado: se regeneró el Excel de proyecto 3 desde dentro del
      contenedor (`backend-web-1`) y se verificó con `openpyxl` que la hoja
      "Unidad Muestreo-Experimental" queda toda en `#0f8139` y que en la
      hoja "CO2 (detalle)" se distinguen `#0f8139` (Unidad Experimental /
      Unidad de Muestreo) de `#3c78d8` (Muestras GEI) en la misma fila de
      encabezados. También se probó la descarga real desde
      `/etl/datos?proyecto=3` en el navegador (200 OK).

## Historial de la paleta

**Paleta original (`catalogoModel.ts`, `GRUPO_PALETTE`), 9 colores para 12 categorías (se reciclan):**

```
#475569, #16a34a, #d97706, #db2777, #7c3aed, #2563eb, #ea580c, #0891b2, #dc2626
```

**Propuesta de Claude (extensión a 12 colores únicos, enviada como imagen a Viviana):**

| Categoría | Color |
|---|---|
| Publicaciones | #475569 |
| Geografía | #16a34a |
| Unidad de Muestreo y Experimental | #d97706 |
| Cobertura y Vegetación | #db2777 |
| Suelo | #7c3aed |
| Carbono Orgánico del Suelo (COS) | #2563eb |
| Biomasa | #ea580c |
| Materia Orgánica Muerta (MOM) | #0891b2 |
| Torre EC y Flujos | #dc2626 |
| Muestras GEI (nuevo) | #0d9488 |
| Proyecto (nuevo) | #c026d3 |
| Usuarios, Roles y ETL (nuevo) | #4f46e5 |

**Alternativa de Viviana (pegada como captura de Google Sheets) — pendiente de
confirmar, tiene inconsistencias entre el texto del hex y el color real de
la celda (verificado por Claude muestreando los píxeles de la imagen):**

| Categoría | Hex escrito en la celda | Color real de la celda (muestreado) | Nota |
|---|---|---|---|
| Publicaciones | #475569 | ~#4A5467 | OK, coincide |
| Geografía | #0f8139 | ~#3A7F41 | Tono de verde distinto al escrito, pero es verde |
| Unidad de Muestreo y Experimental | #0f8139 | ~#9650CE (morado) | **No coincide**: el texto dice verde pero la celda es morada |
| Cobertura y Vegetación | #0f8139 | ~#3A7F41 | **Duplicado**: mismo verde que Geografía |
| Suelo | (celda decía "Suelo #7c3aed", texto viejo) | ~#DA954B (naranja) | El nombre de la fila quedó con un hex viejo pegado |
| Carbono Orgánico del Suelo (COS) | #e69138 | ~#DA954B (naranja) | **Duplicado**: mismo naranja que Suelo |
| Biomasa | #88bb72 | ~#93BA7A | OK, coincide |
| Materia Orgánica Muerta (MOM) | #c36c2d | ~#B8703B | OK, coincide |
| Torre EC y Flujos | #3c78d8 | ~#4B76D2 | OK, coincide |
| Muestras GEI | #3c78d8 | ~#4B76D2 | **Duplicado**: mismo azul que Torre EC y Flujos |
| Proyecto | #333faf | ~#5C1C94 (morado) | No coincide bien: texto es azul-morado, celda es morado más oscuro |
| Usuarios, Roles y ETL | #ffd966 (amarillo pálido) | ~#7A611C (oliva oscuro) | **No coincide**: texto es amarillo pálido, celda es oliva oscuro |

Los duplicados de esta alternativa no chocan *hoy* en el Excel porque en
cada par uno de los dos no aparece en el export (Suelo/Cobertura y
Vegetación/Torre EC y Flujos no se exportan todavía) — pero si esas
categorías se agregan al export más adelante, sí habría colisión visual con
Geografía, COS y Muestras GEI respectivamente.

**Pendiente:** que Viviana confirme cuál es el valor real que quiere para
cada una de las filas con inconsistencia (especialmente Unidad de Muestreo y
Experimental, Suelo, y Usuarios/Roles/ETL), antes de fijar la paleta
definitiva.

**Paleta confirmada por Viviana (2026-09-17, por texto en el chat — valores
finales, resuelve las inconsistencias de la captura anterior):**

| Categoría | Color |
|---|---|
| Publicaciones | `#475569` |
| Geografía | `#ff6f61` (rojo camarón / coral) — Viviana pidió invertir: que Sitio/Geografía fuera el rojo y Unidad de Muestreo y Experimental el verde |
| Unidad de Muestreo y Experimental | `#7c3aed` (violeta) — antes verde `#0f8139`, cambiado a pedido de Viviana |
| Cobertura y Vegetación | `#0f8139` |
| Suelo | `#e69138` |
| Carbono Orgánico del Suelo (COS) | `#e69138` (duplicado intencional — Suelo no se exporta hoy) |
| Biomasa | `#88bb72` |
| Materia Orgánica Muerta (MOM) | `#c36c2d` |
| Torre EC y Flujos | `#3c78d8` |
| Muestras GEI | `#3c78d8` (duplicado intencional — Torre EC no se exporta hoy) |
| Proyecto | `#333faf` |
| Usuarios, Roles y ETL | `#ffd966` |

Nota: Geografía y Cobertura y Vegetación también comparten `#0f8139`, pero
Cobertura y Vegetación no se exporta hoy, así que no genera colisión visual
actual (a diferencia del caso con Unidad de Muestreo y Experimental, que sí
se exporta junto con Geografía en la misma hoja).

## Entregables

- `backend/app/catalogo/generator.py`: `GRUPOS_CATALOGO` con `"color"` por
  grupo + `COLOR_POR_MODELO`
- `backend/docs/assets/data/catalogo.json` y
  `frontend/src/assets/data/catalogo.json`: regenerados con el campo `color`
- `frontend/src/types/index.ts`, `frontend/src/utils/catalogoModel.ts`:
  `colorDeGrupo` ahora lee el color directo del catálogo
- `backend/app/api/etl/views.py`: `_colorear_encabezados()` aplicado en
  `exportar_carga`/`exportar_proyecto`
- Efecto colateral relacionado (mismo pedido de "verificar el formato de la
  descarga" en [[datos-swap]]): se reordenó `_HOJAS_EXPORT` y
  `DatosTabs.tsx` (TABS) para que "Unidad Muestreo-Experimental" sea la
  primera hoja/pestaña, y se agregaron alias a las columnas ambiguas de esa
  vista (4 columnas "nombre" y 2 "descripción" que antes no se distinguían)
  vía el mecanismo `campos`/`alias` de `_VISTAS_DESNORMALIZADAS`
- Orden de columnas de la vista `unidad_muestreo` (afecta la página y el
  Excel, comparten la misma definición): nueva clave `"orden_columnas"` en
  `_VISTAS_DESNORMALIZADAS` + helper `_reordenar_columnas()`, para que
  "nombre unidad experimental", "nombre unidad de muestreo", "fecha
  instalación unidad de muestreo" y "tipo de unidad de muestreo" salgan
  primero (en ese orden) y el resto de columnas después
- Columnas vacías fuera de la descarga: nuevo helper
  `_quitar_columnas_vacias()`, aplicado solo en `exportar_carga`/
  `exportar_proyecto` (no en la vista paginada de la página, donde una
  columna puede estar vacía en una página y tener datos en otra) — descarta
  las columnas sin ningún valor en todo el archivo exportado

- Hoja "Diccionario de datos": se reescribió `_dataframe_diccionario_datos()`
  para que las filas queden en el orden real de aparición (hoja por hoja,
  según `_HOJAS_EXPORT`, y dentro de cada hoja por columna según
  `_columnas_de_vista` — antes se ordenaba alfabéticamente por Entidad), y
  se agregó una primera columna vacía pintada fila por fila según la
  categoría del atributo (`_colorear_columna_categoria`, análogo a
  `_colorear_encabezados` pero por fila en vez de por columna). Se extrajo
  `_columnas_de_vista()` como helper compartido (antes esa lógica solo
  vivía inline en `_preparar_vista_pks`, sin poder reusarla sin pks reales)

Pendiente para una próxima sesión: pedir feedback visual del Excel/diagrama
ERD ya con estos colores aplicados (ideal: abrir el archivo real, no solo la
verificación programática que se hizo aquí).

## Referencias

- [[datos-swap]]

## Historial

| Fecha | Descripción |
|---|---|
| 2026-09-17 | Se crea la tarea (como `modelo-categorias.md`), documentando el trabajo de la sesión sobre colores por categoría. |
| 2026-09-17 | Viviana pide, en la página/hoja "Unidad de Muestreo / Experimental": reordenar columnas (unidad experimental → unidad de muestreo → fecha instalación → tipo → resto) y no descargar columnas vacías. Se implementa `orden_columnas` (afecta página + Excel) y `_quitar_columnas_vacias` (solo Excel). Verificado con el Excel del proyecto 3: pasó de 23 a 11 columnas (se quitaron medida largo/ancho, distancia, descripciones, nombre sitio, pendiente, topografía, uso actual, propiedad de la tierra, tipo de localización, código de metadatos — todas vacías para este proyecto), y en la página web se ven las 24 columnas en el nuevo orden, sin filtrar. |
| 2026-09-17 | Viviana pide invertir los colores: que Sitio/Geografía sea el rojo camarón y Unidad de Muestreo y Experimental el verde (al revés de la decisión anterior). Se intercambian en `GRUPOS_CATALOGO`, se regenera `catalogo.json` (backend + frontend) y se reverifica el Excel: ahora "nombre unidad experimental"/"nombre unidad de muestreo"/"tipo"/etc. salen en verde `#0f8139` y "latitud"/"longitud"/"altitud"/"intervenido" (Sitio) en rojo camarón `#ff6f61`. |
| 2026-09-17 | Viviana pide, para la hoja "Diccionario de datos": ordenar las filas como aparecen por hoja y luego por orden de atributo (no alfabético por entidad), y agregar una columna vacía al inicio para el color del atributo. Se implementa y se verifica con el Excel del proyecto 3: las primeras filas son exactamente "Unidad Muestreo-Experimental" en el orden nombre unidad experimental → nombre unidad de muestreo → fecha instalación → tipo → resto, con la columna 1 pintada por fila (verde `#0f8139` para Unidad de Muestreo y Experimental, coral `#ff6f61` para Sitio, azul `#3c78d8` para Muestras GEI). |
| 2026-09-17 | Viviana pide cambiar "Unidad de Muestreo y Experimental" de verde a violeta (`#7c3aed`). Se actualiza `GRUPOS_CATALOGO`, se regenera `catalogo.json` (backend + frontend) y se reverifica el Excel: la hoja "Unidad Muestreo-Experimental" queda en violeta para sus propias columnas y coral `#ff6f61` para las de Sitio. |
| 2026-09-17 | Viviana pide, para "Diccionario de datos": organizar por pestaña y mostrar solo una pestaña por fila (antes se listaban todas las hojas donde repite un atributo, cadenas larguísimas), con este orden de columnas: Pestaña, Campo, Tipo de dato, Descripción, "Entidad.atributo (Modelo de Datos COLFLUX)", Valores permitidos. Se reescribe `_dataframe_diccionario_datos`: cada atributo ahora usa solo la primera hoja (según `_HOJAS_EXPORT`) donde aparece, columnas renombradas/reordenadas, y se agrega la columna combinada "Entidad.atributo" (`Modelo.campo_tecnico`, ej. `UnidadExperimental.nombre`). Verificado con el Excel del proyecto 3: los bloques quedan agrupados por pestaña (Unidad Muestreo-Experimental → CO2 (detalle) → Clima → ...), una sola pestaña por fila, color por fila intacto. |
| 2026-09-17 | Viviana pide que la página de datos (`/etl/datos`) use los mismos colores de categoría que el Excel — hasta ahora `DatosTable.tsx` tenía su propia paleta hardcodeada (`COLORES_MODELO`, distinta de `GRUPOS_CATALOGO`). Se reemplaza por `colorDeModelo()`, que lee `ENTIDAD_MAP[modelo].color` de `catalogoModel.ts` (mismo catálogo que ya usa el Excel y el ERD de `/db`). Verificado en el navegador: la pestaña CO2 y "Unidad de Muestreo / Experimental" muestran los headers agrupados con los colores correctos (violeta para Unidad de Muestreo y Experimental, azul para Muestras GEI). |
| 2026-09-17 | Viviana pide, para cerrar: que todas las hojas de metodología (CO2, CH4, MOM, COS, Biomasa) tengan al inicio "unidad muestral" y coordenadas, y después los datos propios de cada una. Se agrega `_CAMPOS_METODOLOGIA`/`_ORDEN_COLUMNAS_METODOLOGIA` compartidos: alias para "nombre"/"descripción" ambiguos (mismo patrón que la hoja Unidad Muestreo-Experimental) y `Sitio` restringido a solo `latitud`/`longitud` (el detalle completo del sitio ya vive en esa otra hoja). Para `submuestra_gei` (CO2/CH4) además se habilita `Sitio.incluir` (antes era `[]`, sin coordenadas en absoluto). Verificado: CO2 real queda `nombre unidad de muestreo → latitud → longitud → nombre unidad experimental → analizador → fecha... `; MOM/COS/Biomasa (sin datos en el proyecto 3, verificados vía `_columnas_de_vista` directamente) quedan `nombre unidad de muestreo → latitud → longitud → ` + su propia medición. |
| 2026-09-17 | Viviana pide mover "unidad experimental" al inicio de las hojas de metodología, antes de "unidad de muestreo" (en vez de quitarla). Se actualiza `_ORDEN_COLUMNAS_METODOLOGIA` a `["UnidadExperimental.nombre", "UnidadMuestreo.nombre", "Sitio.latitud", "Sitio.longitud"]` y se restringe `UnidadExperimental` a solo `nombre` (antes también traía `descripcion`) en las 4 hojas. Verificado: CO2 real queda `nombre unidad experimental → nombre unidad de muestreo → latitud → longitud → analizador → ...`; MOM/COS/Biomasa (verificados vía `_columnas_de_vista`) con el mismo orden. |
| 2026-09-17 | Viviana detecta que el diccionario solo mostraba 2 pestañas en vez de 3: la deduplicación "solo primera hoja" hacía que CH4 (detalle) desapareciera por completo, porque comparte exactamente las mismas columnas que CO2 (detalle) y esas ya habían sido "reclamadas" por CO2. Pide mostrar todos los atributos de cada pestaña aunque se repitan entre hojas. Se quita la deduplicación de `_dataframe_diccionario_datos`: ahora es una fila por cada columna real de cada hoja, sin dedup. Verificado con el proyecto 3: aparecen las 3 pestañas reales (Unidad Muestreo-Experimental: 11 filas, CO2 (detalle): 9, CH4 (detalle): 9), con "nombre unidad experimental"/"nombre unidad de muestreo" repetidos en cada una. |
| 2026-09-17 | Viviana detecta dos problemas en "Diccionario de datos": (1) mencionaba pestañas como "Clima" que no existen en ese Excel en particular (el diccionario se armaba desde la metadata estática de todas las vistas posibles, no desde las hojas reales que terminaron en el archivo); (2) "Campo" mostraba el nombre base de Django ("nombre") en vez del texto literal del encabezado tal como sale en la hoja ("nombre unidad experimental", con el alias ya aplicado). Se reescribe `_dataframe_diccionario_datos(hojas)` para recibir la misma lista `hojas` ya armada en `exportar_carga`/`exportar_proyecto` (después de saltar hojas sin datos y de `_quitar_columnas_vacias`), y usar `columna["verbose_name"]` para "Campo". Verificado con el proyecto 3: el diccionario solo menciona "Unidad Muestreo-Experimental" y "CO2 (detalle)" (las únicas hojas reales de ese Excel), y "Campo" ya trae "nombre unidad experimental"/"nombre unidad de muestreo"/"tipo de unidad de muestreo" en vez de "nombre" repetido. |
| 2026-09-17 | Viviana confirma (primero) dejar Geografía / Unidad de Muestreo y Experimental con el mismo color. Se implementa todo el plan: color como fuente única de verdad en `GRUPOS_CATALOGO`, propagado a `catalogo.json` (frontend + docs) y al Excel exportado (`_colorear_encabezados`). Verificado generando el Excel del proyecto 3 dentro del contenedor e inspeccionando los `fill` de las celdas con `openpyxl`. También se resolvió, de paso, el orden de hojas/pestañas y la ambigüedad de columnas "nombre"/"descripción" en la vista `unidad_muestreo`. |
| 2026-09-17 | Al ver el Excel real, Viviana pide distinguir "Unidad de Muestreo y Experimental" de "Geografía" con rojo camarón/coral (`#ff6f61`). Se actualiza `GRUPOS_CATALOGO`, se regenera `catalogo.json` (backend + frontend) y se reverifica el Excel: la hoja "Unidad Muestreo-Experimental" ya muestra `#ff6f61` para sus propias columnas y `#0f8139` solo para las de Sitio. |
| 2026-09-17 | Se renombra a `modelo-datos-categorias.md`. Viviana confirma los 12 valores hex finales por texto; queda pendiente resolver el choque Geografía / Unidad de Muestreo y Experimental antes de aplicar la paleta al Excel. |
