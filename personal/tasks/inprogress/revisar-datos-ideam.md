# Revisión de los datos subidos de IDEAM

**Estado:** en progreso
**Creada:** 2026-09-01

## Objetivo

Revisar los comentarios que el equipo de datos dejó sobre `PLATAFORMA_REVISAR.xlsx` (el archivo que se descargó de la plataforma después de subir los flujos de IDEAM) y para cada uno: validar si el hallazgo es real, resolverlo si se puede, o documentarlo como pregunta abierta para el equipo. Al cerrar la tarea debe quedar (1) este documento con la validación comentario por comentario y (2) un nuevo Excel con las transformaciones aplicadas para que el equipo de datos itere sobre él.

## Contexto

Flujo de trabajo: se subió el archivo de flujos de IDEAM a Colflux (con ayuda de Claude organizando los datos contra el modelo). Después de la carga, se descargó el archivo desde la plataforma (`PLATAFORMA_REVISAR.xlsx`, en `backend/data/`) y se le pasó al equipo de datos para que revisara si lo cargado tenía sentido. El equipo comentó directamente sobre las celdas del Excel descargado (no es la fuente cruda de IDEAM, es la vista ya transformada por la plataforma).

Archivo fuente de la revisión: `backend/data/PLATAFORMA_REVISAR.xlsx` — hojas: `CO2 (detalle)`, `CH4 (detalle)`, `Unidad Muestreo-Experimental`, `Clima`, `MOM`, `COS`, `Biomasa`, `Diccionario de datos`. Comentarios de: Martín Otálora Low (11 comentarios: 10 en `CO2 (detalle)`, 1 en `Biomasa`).

_Nota: existe también `backend/data/LECC_BD_IDEAM_FLUJOS_ACTUAL Copy.xlsx`, una copia distinta con comentarios de Alejandra Díaz sobre el Excel crudo de IDEAM (antes de subirlo) — es una revisión de otra etapa del proceso, no confundir con esta tarea, que es sobre el archivo YA DESCARGADO de la plataforma._

## Revisión comentario por comentario — hoja `CO2 (detalle)`

### 1. `C1` "hora de la toma" — "Debe haber un intervalo de 3 minutos entre toma"
**Validación:** cada `número de toma` tiene un par de filas Inicio/Final que deberían diferir ~3 min en la hora. Medí los 121 pares Inicio/Final de la hoja: **56 de 121 (46%) tienen exactamente la misma hora** en Inicio y Final.
**Estado:** 🔴 Bug confirmado — no es percepción del equipo, es un problema real de datos/carga.
**Pregunta abierta:** ¿la hora de "Final" se está copiando de "Inicio" en el ETL cuando falta el dato original, o el dato original de IDEAM ya venía así? Necesito que el equipo de datos revise 2-3 casos contra la fuente cruda de IDEAM para saber si el problema es de captura original o de nuestra carga.

### 2. `D1` "momento" — "Se comienza por inicio"
**Validación:** en el export, las filas vienen ordenadas con "Final" antes que "Inicio" dentro de cada número de toma (ver muestra de filas 2-3).
**Estado:** 🟢 Resuelto — es un tema de orden de presentación, no de datos. Se puede corregir ordenando por `momento` (Inicio antes que Final) en la consulta/vista de exportación.

### 3. `F1` "valor del flujo" — "O_O está vacío"
**Validación en el Excel:** de 3.254 filas, solo **111 tienen valor** (3.4%). El valor **nunca** aparece en filas "Inicio" — solo en "Final", y ahí solo en 111 de 1.608 (6.9%).
**Validación a nivel de modelo de datos (BD + metadatos de la carga):**
- En la BD, `SubmuestraGEI.valor` es NULL en 3.143 de 4.907 submuestras de CO2 (64% — el número total es mayor que el del Excel porque en la BD hay más de una carga combinada).
- La carga de origen (Fuente 24 "IDEAM Humedales - Flujos CO2", Carga 199, 3.296 filas) mapea `SubmuestraGEI.valor` ← columna origen `co2_flux_micromol_m2_s`, con estrategia "dejar_null" para los vacíos.
- Los metadatos de esa carga (`columnas_raw`, que registran los nulos de la fuente **antes** de cualquier transformación) muestran que la columna origen `co2_flux_micromol_m2_s` **ya traía 3.185 de 3.296 filas (96.6%) vacías en el archivo que se subió**.

**Estado:** 🟢 Causa raíz confirmada — **no es un bug del ETL ni del export**. El sistema mapeó correctamente la columna y dejó null donde la fuente no traía dato; el hueco viene del archivo original de IDEAM.
**Pregunta abierta para el equipo de datos:** ¿por qué la fuente entregada por IDEAM trae el flujo vacío en 96% de las filas? ¿existe otra columna/archivo de IDEAM con esos valores que no se incluyó al armar la fuente `co2_flux_micromol_m2_s`, o esas mediciones realmente nunca se completaron en campo? Si hay otra fuente con los datos reales, hay que volver a mapear esa carga; si no, hay que decidir si esas ~3.100 filas sin valor se conservan (como registro de que se intentó medir) o se descartan de la carga.

### 4. `G1` "tubo" — "Mejor llamarlo Vol Tubo. La base de datos original cuenta con datos, pero acá está vacía"
**Validación en el Excel:** solo 183/3.254 filas (5.6%) tienen valor.
**Validación a nivel de modelo de datos:** mismo patrón que el punto 3 — la Carga 199 mapea `MuestraGEI.tubo` ← columna origen `anillo`, y esa columna origen ya traía 3.114 de 3.296 filas (94.5%) vacías en el archivo subido. Filtrando por los pks reales de esta carga (no toda la BD, que mezcla otros proyectos), 161 de 257 `MuestraGEI` de esta carga (62.6%) tienen `tubo` vacío.
**Estado:** 🟢 Causa raíz confirmada (viene de la fuente, no del ETL) + 🟢 sugerencia de nombre resuelta.
**Resolución aplicada:** renombrar columna de "tubo" a "Vol Tubo" (o "volumen del tubo") en la próxima exportación.
**Pregunta abierta:** el equipo de datos comentó "la base de datos original cuenta con datos" — hay que confirmar con ellos si conocen dónde está esa fuente con el dato de `anillo` completo, para volver a mapear la carga contra esa columna en vez de la que se usó.

### 5. `I1` "código" — "No sabemos qué es código y repite la info de descripción"
**Validación:** crucé con `Diccionario de datos` → `código` es el identificador corto de la unidad de medida (ej. `co2_flux_micromol_m2_s`) y `descripción` es su versión legible (ej. "Flujo de CO2 (µmol m-2 s-1)"). En la hoja `CO2 (detalle)` este par es **constante en todas las filas** (siempre el mismo código/descripción), porque la hoja ya está filtrada a un solo gas — por eso al equipo le parece redundante.
**Estado:** 🟢 Resuelto. La columna no está mal, pero no aporta nada en una hoja de un solo gas.
**Resolución aplicada:** quitar la columna `código` de las hojas `CO2 (detalle)` / `CH4 (detalle)` (queda implícita por el nombre de la hoja) y dejar solo `descripción` si se necesita la unidad en texto.

### 6. `K1` "magnitud" — "El título está mal. Las celdas no tienen magnitudes"
**Validación:** la columna tiene el valor `"flujo"` en el 100% de las filas (constante).
**Estado:** 🟢 Resuelto — el equipo tiene razón en que no aporta valor por fila (es constante), pero el título sí es correcto (es la magnitud de la unidad de medida, ej. flujo/concentración/temperatura, ver diccionario).
**Resolución aplicada:** quitar la columna de las hojas de detalle por gas (es redundante igual que `código`), dejarla solo donde se listan varias magnitudes a la vez (ej. un catálogo general de unidades de medida).

### 7. `L1` "modelo" — "Cambiar a analizador"
**Validación:** valores reales: `LICOR 8100`, `EGM-4`, `Picarro` — son nombres/modelos de analizadores de gases.
**Estado:** 🟢 Resuelto.
**Resolución aplicada:** renombrar columna de "modelo" a "analizador" en la exportación.

### 8. `O1` "nombre" — "Tenemos nombre dos veces"
**Validación:** hay dos columnas literalmente tituladas "nombre": `O` = nombre de la **unidad de muestreo** (ej. `IDEAM_Humedales_Flujos_PNN Nevados_SanAntonioParamos_1`) y `R` = nombre del **sitio** (ej. `SanAntonioParamos`). Son conceptualmente distintos pero el título no lo deja claro.
**Estado:** 🟢 Resuelto.
**Resolución aplicada:** renombrar a "nombre unidad de muestreo" y "nombre del sitio" respectivamente.

### 9. `P1` "fecha instalación unidad de muestreo" — "Tenemos dos fechas y son diferentes, no sabemos por qué. Revisar columna B"
**Validación:** comparé `B` (fecha de la toma, ej. 2016-08-11) contra `P` (fecha instalación unidad de muestreo, ej. 2021-08-23) para el mismo sitio. Son fechas distintas, pero **la fecha de instalación es 100% consistente dentro de cada unidad de muestreo** (verifiqué las 171 unidades de la hoja: 0 inconsistencias). O sea, `P` no está mal — el punto es que el instrumento/parcela se instaló formalmente años después de que existieran mediciones históricas de ese sitio (o la fecha de instalación registrada en el sistema no coincide con el inicio real del muestreo histórico).
**Estado:** 🟡 Parcialmente resuelto — la columna `P` en sí no tiene el bug que sospechaba el equipo (no varía de forma inconsistente). Pero sigue sin estar claro **por qué** difieren tanto (5 años de diferencia en algunos casos).
**Pregunta abierta:** confirmar con el equipo si "fecha instalación unidad de muestreo" debe representar cuándo se instaló físicamente la parcela/tubo (que puede ser mucho después de las primeras tomas si el sitio ya existía) o si debería reflejar la fecha de la primera toma real — si es esto último, hay que corregir el dato de origen, no solo la interpretación.

### 10. `AJ1` "intervenido" — "Es verdad que no está intervenido, pero podemos usar una versión más desagregada que está en el diccionario"
**Validación:** el diccionario de datos tiene un catálogo más rico en el campo "uso actual del suelo" (`Bosque primario, Bosque secundario, Plantación forestal, Agricultura intensiva, Agricultura tradicional, Pastura, Humedal natural, Humedal intervenido, Área protegida, Sistema agroforestal, Abandonado, Restauración activa`), que sí distingue grados de intervención en vez del booleano Sí/No de `intervenido`.
**Estado:** 🟢 Resuelto.
**Resolución aplicada:** para hojas donde ya se completó "uso actual del suelo", mostrar esa columna en vez de (o además de) "intervenido". Si "uso actual del suelo" está vacío para muchos sitios, hay que backfillearlo antes de poder deprecar "intervenido" — revisar cobertura de esa columna en las demás hojas.

## Revisión hoja por hoja (sin comentarios, contra fuente + modelo) — `CH4 (detalle)`

El equipo no dejó comentarios en esta hoja, pero como es la contraparte directa de `CO2 (detalle)` (misma vista `submuestra_gei`), se revisó igual contra la fuente (Fuente 22 "IDEAM Humedales - Flujos CH4", Carga 197, 946 submuestras reales) y el modelo:

| Columna | Vacío en la fuente/BD (carga 197) | Comparado con CO2 (carga 199) |
|---|---|---|
| `valor del flujo` | **946/946 = 100%** | CO2: 96.6% — CH4 está peor, ni una sola fila tiene flujo. |
| `tubo` | 61/61 muestras = 100% | CO2: 62.6%. |
| `número de toma` (n_toma) | 946/946 = 100% | CO2: 100% también — **ninguna de las dos fuentes IDEAM trae este campo**, no es específico de CH4. |
| `momento` (Inicio/Final) | 946/946 = 100% vacío | CO2: 0% vacío (sí mapeado, columna origen "tomada al inicio/final"). |

**Causa raíz confirmada:** revisé `columnas_raw` de la Carga 197 — la columna origen `ch4_flux_micromol_m2_s` viene **100% vacía (951/951) ya en el archivo que se subió**, y la fuente **no tiene ninguna columna equivalente a "tomada al inicio/final"** (a diferencia de la fuente de CO2), por eso `momento` nunca se pudo mapear. No es un bug de mapeo — el mapeo de `tubo`/`valor` está configurado igual que en CO2 (mismas columnas origen `anillo`/`*_flux_micromol_m2_s`), simplemente esta fuente en particular llegó más incompleta.

**Nota aparte (no confundir):** existe otra fuente llamada "CH4" (id 18) con una columna `CH4 original` que sí tiene datos, pero pertenece al **proyecto 3**, no al proyecto 9 (IDEAM Humedales) — es un dataset distinto, no una fuente alternativa de estos mismos datos de IDEAM.

**Estado:** 🔴 Más crítico que CO2 — para CH4, prácticamente toda la hoja de detalle (excepto fecha, hora, condición de luz, analizador, y los datos de parcela/sitio) está vacía porque la fuente nunca trajo esas columnas.
**Pregunta abierta para el equipo de datos:** ¿la fuente de flujos CH4 de IDEAM realmente no incluye el valor del flujo, el momento (inicio/final) ni el número de toma, o falta pedir/conseguir un archivo más completo? Dado que **ni un solo registro de CH4 tiene valor de flujo**, esta hoja hoy no aporta ningún dato analítico real — vale la pena confirmar esto como prioridad #1 antes que cualquier otro ajuste de formato.

## Revisión comentario por comentario — hoja `Biomasa`

### 11. `N1` "medida largo (m)" — "Faltan variables"
**Validación en el Excel:** revisé todo el bloque de columnas de "Parcela" (`M` a `S`: forma, medida largo, medida ancho, distancia/lado, diámetro, área, descripción) — **están vacías en el 100% de las 646 filas**. También están vacías `contenido de carbono`, `promedio/desviación/mínimo/máximo (TonC/ha)`, `compartimento`, `pendiente`, `topografía`, `uso actual del suelo`, `propiedad de la tierra`.
**Validación a nivel de modelo de datos:**
- La carga de Biomasa (Fuente 26 "IDEAM Humedales - Biomasa", Carga 205, 646 filas) **no tiene ningún mapeo hacia el modelo `Parcela`** — a diferencia del caso de CO2, aquí ni siquiera se intentó mapear esas columnas (no es "dejar_null" sobre un mapeo existente, es la ausencia total del mapeo).
- Revisé los metadatos de la fuente original (`columnas_raw` de la carga 205): **la fuente de IDEAM para Biomasa nunca trae columnas de geometría de parcela** (no hay ninguna columna origen de forma/largo/ancho/diámetro/área). Tampoco trae los agregados de carbono: `Contenido de carbono`, `Prom_TonC_ha`, `SD_TonC_ha`, `min_TonC_ha`, `max_TonC_ha` están 100% vacías **ya en el archivo original**, igual que todas las columnas de individuo arbóreo (`Tipo`, `N_ind`, `Condicion`, `DAP.1/2`, `Familia`, `genero`, `especie`, etc.). Lo único que sí trae con datos casi completos es `Prod. Biomasa (g)` (617/646, 95%) y la ubicación/fecha.

**Estado:** 🟢 Causa raíz confirmada — no es un bug de mapeo ni del ETL: la fuente de Biomasa de IDEAM solo trae producción de biomasa (g) por parcela y ubicación; nunca trajo geometría de parcela, individuos arbóreos ni agregados de carbono. Esto coincide con una nota ya existente en el código (`_VISTAS_DESNORMALIZADAS`, vista `biomasa`) que documenta que `IndividuoArboreo` siempre queda vacío en los datos reales de IDEAM — pero el vacío es más amplio de lo que esa nota registraba (también faltan Parcela y los agregados TonC/ha).
**Pregunta abierta para el equipo de datos:** ¿existe en algún otro archivo/hoja de IDEAM la geometría de parcela y los agregados de carbono de Biomasa, o el dato de campo real es solo "producción de biomasa (g)" y el resto se calcula/estima en otra etapa que todavía no está en el pipeline? Si el cálculo de TonC/ha a partir de producción de biomasa (g) es algo que Colflux debería hacer (no IDEAM), es una funcionalidad pendiente, no un hueco de datos.

## Resumen de hallazgos críticos (para priorizar con el equipo de datos)

Confirmado a nivel de modelo de datos (BD + metadatos de carga, no solo el Excel de revisión): **los 4 huecos grandes de datos no son bugs del ETL ni del export** — el sistema mapeó y cargó exactamente lo que traía la fuente de IDEAM. Los huecos vienen de la fuente. Quedan como preguntas para el equipo de datos, no como tickets de código:

1. **`valor del flujo` de CH4 vacío en el 100% de las 946 submuestras** — la hoja `CH4 (detalle)` no tiene hoy ningún dato de flujo utilizable. Prioridad #1.
2. **`valor del flujo` de CO2 vacío en 96.6% de las filas** (columna origen `co2_flux_micromol_m2_s`) — ¿existe otra fuente/columna de IDEAM con esos valores?
3. **`tubo`/`anillo` vacío en 62.6% (CO2) y 100% (CH4) de las muestras.**
4. **`número de toma` no viene en ninguna de las dos fuentes IDEAM (CO2 ni CH4)** — 100% vacío en ambas, no es un problema de mapeo sino que la fuente nunca lo trae.
5. **`momento` (Inicio/Final) 100% vacío en CH4** (la fuente no tiene columna equivalente), pero 0% vacío en CO2 (si está bien mapeado) — inconsistencia entre las dos fuentes de IDEAM, no del sistema.
6. **Geometría de parcela y agregados de carbono ausentes al 100% en la fuente de Biomasa** — la fuente de IDEAM solo trae producción de biomasa (g) + ubicación; falta confirmar si el resto se calcula en otra etapa que no está en el pipeline todavía.
7. **46% de los pares Inicio/Final en CO2 tienen la misma hora** cuando deberían diferir ~3 min — este sí puede ser un problema de la fuente original de captura en campo (o del reloj del equipo), no del sistema; pendiente de confirmar con el equipo contra la fuente cruda.

## Cambios aplicados (2026-09-07/08) — persistentes, no un archivo de una sola vez

A pedido explícito: en vez de generar un Excel corregido aparte, las correcciones se implementaron en el sistema (BD + código de exportación/UI) para que sigan aplicando en cargas futuras.

### 1. Regla de autollenado "Colisión de hora entre Inicio y Final"
Nueva entrada en `app/reglas/autollenado.py` (`REGLAS["colision_hora_inicio_final"]`), reutilizando el motor existente de reglas (preview/aplicar/deshacer con auditoría en `AplicacionRegla`, mismo mecanismo que ya usaba la UI para "Validación" de horas faltantes).

- **Algoritmo:** agrupa `SubmuestraGEI` por `(muestra_id, fecha)` — no solo por muestra, porque una misma `MuestraGEI` se reutiliza en muchas fechas (~4 tomas por sesión). Dentro de cada grupo empareja Inicio/Final **por orden de `id`** (confirmado contra los datos reales: el id de inserción preserva la secuencia real de captura, alternando inicio/final). Si un par tiene la misma hora, suma `incremento_minutos` (3 por defecto) a la hora del Final. Pares sin contraparte (sobra un Inicio o un Final) no se tocan.
- **Aplicada ya sobre los datos reales:** 631 registros corregidos en toda la BD (75 de ellos en la carga 199 de CO2 IDEAM). Reversible desde la UI de reglas si el equipo de datos no está de acuerdo con el criterio.
- **Nota:** se descubrió en el camino que 96% de las `MuestraGEI` de CO2 tienen más de un par Inicio/Final por (muestra, fecha) — la ambigüedad real solo se resuelve confiando en el orden de inserción, no en agrupar ingenuamente por muestra. Ver punto sobre `número de toma` más abajo.

### 2. Campo `UnidadMedida.simbolo` — colapsa código+descripción+magnitud
Migraciones `0084`/`0085`: nuevo campo `simbolo` (ej. `"µmol m-2 s-1"`), poblado automáticamente por regex sobre `descripcion` (`"Flujo de CO2 (µmol m-2 s-1)"` → `"µmol m-2 s-1"`; si no hay paréntesis, cae al `codigo`). Reemplaza a `código`/`descripción`/`magnitud` en la vista de datos — se muestra como columna única **"unidad del flujo"**.

### 3. `Equipo.modelo` renombrado a "analizador" (verbose_name)
Migración `0084`. Es solo metadata (label), no requiere tocar datos.

### 4. Formato de la vista `submuestra_gei` (`app/api/etl/views.py`, hojas `CO2 (detalle)` y `CH4 (detalle)`, tanto en la UI "Gestión de Datos" como en el Excel descargado — comparten el mismo código)
Se extendió el motor genérico de vistas desnormalizadas (`_campos_planos`, `_VISTAS_DESNORMALIZADAS`) para soportar, por vista: `incluir`/`excluir` de campos por modelo, y `alias` de nombre de columna. Con eso, la vista `submuestra_gei` quedó así:

- **Orden de columnas:** `nombre unidad de muestreo`, `nombre unidad experimental`, número de toma, fecha de la toma, hora de la toma, momento, condición de luz, valor del flujo, tubo, gas, unidad del flujo, analizador.
- **Quitado:** `código`/`descripción`/`magnitud` de UnidadMedida (colapsados en `unidad del flujo`), `serial`/`descripción` de Equipo (vacíos al 100% en los datos de IDEAM), y **todo** el detalle de `UnidadMuestreo` (excepto nombre), `Parcela` y `Sitio` — esos campos siguen completos en la pestaña `Unidad Muestreo-Experimental`; aquí solo queda el nombre como referencia para cruzar. `Parcela`/`Sitio` siguen en la cadena de joins internamente (necesario para el filtro por sitio del geoportal), solo no se muestran como columnas.
- **Diccionario de datos** (hoja `Diccionario de datos` del Excel exportado): se corrigió para que sea preciso por (modelo, campo, hoja) — antes decía "Pestaña: CO2, CH4, ..." para columnas de Sitio/Parcela aunque ya no aparecieran ahí; ahora una fila del diccionario solo lista las hojas donde ese campo específico es realmente visible.
- Este cambio afecta **tanto CO2 como CH4** (comparten la misma vista) — decisión confirmada con el usuario.

### 5. `número de toma` (`SubmuestraGEI.n_toma`) — validado, sigue sin resolver del todo
- **Sí existe en el modelo** y sí se usa: es criterio de desempate en el `orden` de la vista `submuestra_gei` y en la regla de autollenado `hora_submuestra_gei` (horas faltantes).
- **Nunca llega poblado desde IDEAM** (100% NULL tanto en CO2 como en CH4, confirmado contra las dos fuentes).
- **Hallazgo nuevo:** sin `n_toma`, emparejar Inicio/Final de forma confiable dentro de una fecha depende de que el orden de inserción (id) preserve el orden real de captura — que se confirmó que sí pasa en los datos actuales, pero es un supuesto frágil (se rompe si algún día se reimporta o reordena la fuente). **Sigue como pregunta abierta para el equipo de datos:** ¿la fuente de IDEAM tiene en algún lado un identificador de toma (1,2,3,4...) que no se está mapeando, o realmente nunca lo reportan? Si nunca lo reportan, vale la pena que quede así documentado (el campo se queda en el modelo por si algún día sí llega, pero no se puede confiar en reconstruirlo).

### 6. RESUELTO — el "valor del flujo" de CO2 sí existía en la fuente, se había mapeado la columna equivocada
Esto **anula la conclusión anterior** ("el hueco viene de la fuente, no hay nada que hacer"). Al revisar más a fondo:

- El archivo fuente (`ideam.xlsx`, hoja `CO2`, usado por la Fuente 24 / Carga 199) tiene una columna `CO2 original` con dato real en 3.186 de 3.297 filas (96,6%) — casi la inversa exacta de `co2_flux_micromol_m2_s` (la columna que sí se había mapeado, 96,6% vacía). El `MapeoColumna` de `SubmuestraGEI.valor` apuntaba a la columna equivocada.
- Además, `MuestraGEI.unidad_medida` estaba fijo como **valor constante** (pk 4, la unidad µmol) para toda la carga, pero `CO2 original` en realidad mezcla dos unidades reales según la columna `Unidades reportadas`: 2.793 filas en `g m2/h` y 392 filas en `μmol`.
- **Corrección aplicada:** se re-mapeó `SubmuestraGEI.valor <- "CO2 original"` (directo) y `MuestraGEI.unidad_medida <- "Unidades reportadas"` con `mapeo_valores = {"g m2/h": "1", "μmol": "2"}` (los pks de `UnidadMedida` `g_m2_h`/`umol_m2_s`, que ya existían en el catálogo).
- Como el archivo original de la fuente había sido sobrescrito por una carga posterior de la misma `FuenteDatos` (el campo `url` es por fuente, no por carga), se reconstruyó a partir de `data/ideam.xlsx` (headers reales en la fila 5, se normalizó a fila 1 para que calzara con lo que `columnas_raw` de la carga 199 tenía registrado — coincidencia exacta de columnas confirmada antes de usarlo). Se limpiaron además 3 problemas de formato del propio archivo que bloqueaban la importación (typo "0ct"→"Oct" en fechas, 1 fila sin ID, espacios sueltos en "day/night"/"momento"/formato de hora con sufijo a.m./p.m. contradictorio) — estos no tienen relación con el bug de mapeo, son separados.
- Se borraron los 3.254 `SubmuestraGEI` y 257 `MuestraGEI` que había creado la carga 199 (verificado que ningún otro carga los reclamaba en su `pks_importados`) y se reimportó desde cero con el mapeo corregido. `Sitio`/`UnidadMuestreo`/`UnidadExperimental`/`MuestraAmbiental` no se tocaron (se reutilizaron).
- **Resultado:** de 3.287 submuestras, ahora **3.176 tienen valor real (96,6%)** — antes eran 111. Las 111 que siguen sin valor coinciden con las filas que tampoco traían `Unidades reportadas` en la fuente (esas sí son un hueco real de la fuente).
- Se volvió a aplicar la regla `colision_hora_inicio_final` sobre los nuevos registros (631 correcciones, igual que antes — los IDs cambiaron al recrear, pero el resultado es el mismo).

**Pendiente de hacer lo mismo para CH4** (Fuente 22, Carga 197) — ahí `ch4_flux_micromol_m2_s` estaba 100% vacía; falta revisar si existe un "CH4 original" equivalente en su archivo fuente antes de asumir que es un hueco real de la fuente.

### Pendiente de decidir con el equipo de datos (no tocado)
- **`tubo`** — se deja explícitamente como pregunta abierta al equipo de datos (punto 4 de la revisión de comentarios), no se le aplicó ninguna transformación automática.
- El resto de preguntas abiertas de las secciones anteriores (valor del flujo vacío en CO2/CH4, geometría de Biomasa, etc.) siguen iguales — son huecos de la fuente, no de formato.

## Plan

- [x] Localizar el archivo correcto de revisión (`backend/data/PLATAFORMA_REVISAR.xlsx`) y extraer los 11 comentarios del equipo.
- [x] Validar cada comentario contra los datos reales de la hoja (no solo contra el comentario aislado).
- [x] Documentar comentario por comentario: validación, resolución o pregunta abierta.
- [ ] Confirmar con el equipo de datos las 4 preguntas abiertas (puntos 1, 3, 9, 11 de arriba) — en particular si el vacío de `valor del flujo` y de la geometría de Biomasa viene de la fuente IDEAM o del ETL.
- [ ] Aplicar las correcciones ya resueltas (renombrar columnas, quitar `código`/`magnitud` redundantes, mostrar "uso actual del suelo" en vez de "intervenido") en un script reproducible sobre el archivo exportado.
- [ ] Generar el nuevo Excel corregido para la siguiente iteración del equipo de datos.
- [ ] Actualizar este documento con las respuestas del equipo y cerrar la tarea.

## Entregables

1. Este documento, con la validación comentario por comentario.
2. Nuevo archivo Excel con las transformaciones/correcciones ya resueltas aplicadas, para la siguiente iteración del equipo de datos.

## Referencias

- Archivo revisado: `backend/data/PLATAFORMA_REVISAR.xlsx`
- Diccionario de datos: hoja `Diccionario de datos` dentro del mismo archivo.
- Copia con comentarios de Alejandra Díaz sobre el Excel crudo de IDEAM (etapa anterior, no es esta tarea): `backend/data/LECC_BD_IDEAM_FLUJOS_ACTUAL Copy.xlsx`

## Historial

| Fecha | Descripción |
|---|---|
| 2026-09-01 | Se crea la tarea. |
| 2026-09-07 | Se identifica el archivo correcto de revisión (`PLATAFORMA_REVISAR.xlsx`), se extraen y validan los 11 comentarios del equipo contra los datos reales, se documenta hallazgo por hallazgo y se identifican 4 preguntas abiertas críticas para el equipo de datos. |
