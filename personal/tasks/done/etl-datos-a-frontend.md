# Migrar páginas del prototipo ETL/admin (docs/pages) al frontend oficial

**Estado:** en revisión — migración a React completa y prototipo retirado del backend; falta abrir el PR del frontend
**Creada:** 2026-09-14

## Objetivo

Migrar la funcionalidad de las páginas estáticas del prototipo
(`backend/docs/pages/*.html`) al frontend oficial en React
(`colflux/frontend`), empezando por `etl-datos.html`, para dejar de mantener
dos implementaciones (HTML/JS vanilla vs. React/TS) de la sección
ETL/administración.

## Contexto

`backend/docs/pages/` es un prototipo estático (HTML + CSS inline + JS
vanilla, sin build) que hoy cubre el flujo de carga y administración de
datos: subida de fuentes, mapeo de columnas, vista de datos cargados,
reglas de autollenado/validación, gestión de equipo y explorador de BD.
Consume la API Django (`/api/...`) directamente con `fetch`.

El frontend oficial (`colflux/frontend`) es React 19 + TypeScript + Vite +
Tailwind + react-router-dom v7 + @tanstack/react-query v5 + zustand, y hoy
solo tiene las páginas públicas del geoportal (Home, MapaInteractivo,
DashboardIndicadores, Participacion, InsightsIA, Educacion). La sección
ETL/admin no existe ahí todavía.

Páginas a migrar (orden sugerido, de más independiente a más acoplada):

1. `etl-datos.html` — vista desnormalizada de datos cargados: tabs por
   modelo (CO2/CH4/unidad_muestreo/clima/mom/cos/biomasa), filtros por
   columna, paginación, export a Excel, dropdown de fuentes del proyecto.
2. `reglas-campo.html`, `regla-detalle.html`, `regla-validacion.html` —
   reglas de autollenado y validación de campos.
3. `etl-mapeo.html` — mapeo de columnas del archivo a campos del modelo.
4. `etl-upload.html` — wizard de carga de fuentes (la más grande, 2900+
   líneas; dejarla para el final una vez resueltos los patrones de
   drawer/dropdown en las páginas anteriores).
5. `data.html` — gestión de datos/fuentes por proyecto.
6. `db.html` — explorador de la base de datos.
7. `team.html` — gestión de equipo/usuarios.

Ya se redactó un prompt detallado con el encuadre completo (contexto de
ambos repos, convenciones del frontend a respetar, endpoints que consume
`etl-datos.html`, y el criterio de "migración de plataforma, no rediseño")
— ver sección Referencias.

## Decisiones tomadas

- **Prefijo de ruta:** `/etl/...` (espejo directo de los nombres del
  prototipo, no `/admin/...`). `etl-datos.html` → `/etl/datos`.
- **Layout:** las páginas `/etl/*` se montan dentro del `AppLayout` público
  existente (mismo Navbar/Footer/ChatWidget), sin agregarlas a
  `SIDEBAR_ROUTES`. No se crea un `AdminLayout` separado.
- **Punto de entrada:** en `Participacion.tsx` (`/reportar`), se agrega una
  card nueva al grid `CANALES` existente (junto a "Reporte rápido",
  "Formulario web", etc.) — algo como "🔄 ETL de Datos" — que navega a
  `/etl/datos`.
- **Header de página:** `EtlDatos` NO usa el hero de banda verde del
  prototipo (`.hero` con badge/título/subtítulo a ancho completo). Usa un
  header compacto (título + subtítulo dinámico) consistente con el resto
  de páginas del frontend oficial (mismo patrón que `Participacion`/
  `DashboardIndicadores`).
- **Tabs de vista** (CO₂/CH₄/Unidad de Muestreo/Clima/MOM/COS/Biomasa):
  igual al prototipo — fila de tabs pegada arriba de la tabla, activo con
  fondo verde claro, pero con clases Tailwind en vez de CSS inline (no se
  usa un `<Select>`).
- **Toolbar** (info de resultados + Limpiar filtros + Cargar ▾ + Descargar
  Excel + Volver): una sola fila horizontal, igual al prototipo (info a la
  izquierda, acciones a la derecha).
- **Colores por modelo en el thead** (`COLORES_MODELO`: SubmuestraGEI,
  MuestraGEI, UnidadMedida, etc.): se mantienen los hex exactos del
  prototipo, no se mapean a los design tokens del frontend (brand-teal,
  etc.) — paleta propia solo para esta tabla.
- **Paginación:** barra separada, centrada, debajo de la tabla — igual al
  prototipo (no se integra en la toolbar superior).
- **Drawer "Nueva fuente":** se monta dentro de `EtlDatos` (no
  globalmente en `AppLayout`). Cuando se migren `data.html`/
  `etl-upload.html` cada página monta su propia instancia; el estado
  (`useFuenteDrawerStore`) es lo único global/compartido.
- **Botón "🛡️ Validación" por columna:** navega a una ruta stub
  `/etl/reglas/campo?campo=&fuente=&carga=` con un componente placeholder
  ("Próximamente — en migración") registrado ya en `App.tsx`. Se reemplaza
  el placeholder cuando se migre el paso 2 del plan
  (`reglas-campo.html`), sin tocar el link que lo genera.
- **Dropdown "Cargar" + drawer "Nueva fuente"** se construyen como piezas
  **compartidas** desde el arranque (no acopladas solo a `etl-datos`),
  porque el prototipo ya los reutiliza en `data.html` y `etl-upload.html`:
  - `src/store/useFuenteDrawerStore.ts` (zustand) — estado global
    `{ open, editingFuente, proyectoContextId }`, porque el drawer se abre
    desde un componente hijo (el dropdown) y controla un overlay a nivel
    de página.
  - `src/components/admin/fuentes/FuenteDrawer.tsx` — formulario de
    alta/edición de fuente.
  - `src/components/admin/fuentes/CargarDropdown.tsx` — dropdown de
    fuentes del proyecto + acceso a "Agregar nueva fuente".
  - El resto del estado de `EtlDatos` (tab activo, filtros por columna,
    offset) es local vía `useReducer`, no zustand — no se comparte fuera
    de esa página.
- **Simplificación real vs. el prototipo:** el hack de "restaurar foco +
  cursor tras re-render" del input de filtro (necesario en el HTML vanilla
  porque `innerHTML` remonta el DOM) desaparece solo con inputs controlados
  de React — no hace falta portarlo.

## Diseño — `etl-datos.html` → `/etl/datos`

### Mapeo de endpoints (todos ya existen en el backend Django, sin gaps)

| Endpoint | Uso | Estado en frontend React |
|---|---|---|
| `GET /api/proyectos/{id}/datos/` | tabla por proyecto | ya existe en `datos.service.ts` (`getDatosProyecto`) |
| `GET /api/fuentes-datos/{id}/carga/{id}/datos/` | tabla por carga puntual | falta agregar `getDatosCarga` |
| `GET /api/reglas-autollenado/` | badges de validación pendiente por columna | falta, nuevo `reglas.service.ts` |
| `GET /api/fuentes-datos/?proyecto=` | dropdown "Cargar" (fuentes + proyectos) y resolver nombre de proyecto | falta, nuevo `fuentes.service.ts` |
| `GET /api/proyectos/{id}/exportar/` | descargar Excel | ya existe (`getExportarProyectoUrl`) |
| `GET /api/fuentes-datos/{id}/carga/{id}/exportar/` | descargar Excel por carga | ya existe (`getExportarCargaUrl`) |
| `POST/PATCH /api/fuentes-datos-crud/`, `POST /api/fuentes-datos/{id}/archivo/`, `GET /api/responsables/` | drawer "Nueva fuente" | falta, todo nuevo |

### Estructura de archivos propuesta

```
src/pages/EtlDatos.tsx                     ← lee ?proyecto= / ?fuente=&carga= de useSearchParams
src/components/etl-datos/
  DatosTabs.tsx           ← CO2/CH4/unidad_muestreo/clima/mom/cos/biomasa
  DatosToolbar.tsx        ← info + botones (limpiar filtros, cargar, exportar, volver)
  DatosTable.tsx          ← thead agrupado por modelo (color), fila de campos, fila de validación, fila de filtros, tbody
  DatosTableFilterInput.tsx  ← input controlado con debounce (400ms) por columna
src/components/admin/fuentes/
  CargarDropdown.tsx      ← compartido (ver Decisiones)
  FuenteDrawer.tsx         ← compartido (ver Decisiones)
src/components/common/Paginacion.tsx       ← genérico, candidato a reusarse en db.html/data.html
src/store/useFuenteDrawerStore.ts          ← zustand, compartido
src/services/datos.service.ts              ← + getDatosCarga(fuenteId, cargaId, filters)
src/services/fuentes.service.ts            ← listFuentesDropdown, createFuente, updateFuente, uploadArchivoFuente
src/services/reglas.service.ts             ← listReglasAutollenado
src/services/responsables.service.ts       ← listResponsables
src/hooks/useDatosCarga.ts
src/hooks/useFuentesDropdown.ts
src/hooks/useReglasAutollenado.ts
src/hooks/useCrearFuente.ts / useActualizarFuente.ts / useSubirArchivoFuente.ts
```

### Tipos a extender en `types/index.ts`

- `VistaDatos` le faltan `'mom' | 'cos' | 'biomasa'` (hoy solo tiene
  `'submuestra_gei' | 'unidad_muestreo' | 'clima'`).
- Agregar: `ReglaAutollenado`, `FuenteDatos`, `Proyecto` (forma reducida
  para el dropdown), `Responsable`, `FuenteDatosPayload`.

## Diseño — `reglas-campo.html` / `regla-detalle.html` / `regla-validacion.html`

Solo existen 2 reglas configuradas en el backend hoy (`hora_submuestra_gei`
y `colision_hora_inicio_final`, ambas sobre `SubmuestraGEI.hora`), y solo
la primera tiene validación de rangos — feature acotada.

- **Rutas:** `/etl/reglas/campo` (reemplaza el stub `EtlProximamente` que
  había quedado ahí), `/etl/reglas/detalle`, `/etl/reglas/validacion`.
- **Histograma de horas:** se usa `recharts` (BarChart agrupado, una serie
  por condición de luz), no Chart.js — ya es la librería de charts del
  resto del frontend (`EmissionBarChart`), sin agregar dependencia nueva.
- **Confirmación de "Aplicar regla" y "Deshacer lote":** modal centrado
  nuevo (`src/components/common/ConfirmModal.tsx`), no el patrón inline
  del prototipo — decisión explícita del usuario aunque introduce un
  componente sin precedente en el frontend; queda como pieza reutilizable
  para futuras confirmaciones destructivas.
- **Simplificación real vs. el prototipo:** la tarjeta "Validación de
  valores" en `regla-detalle.html` tenía texto hardcodeado ("hora de la
  toma") en vez de derivarse de datos — en React se condiciona a
  `d.validacion != null` y el texto usa `d.campo_destino` dinámicamente,
  más robusto si en el futuro otra regla también tiene validación.
- Servicios: `reglas.service.ts` se extiende con `getDetalleRegla`,
  `actualizarParametrosRegla`, `aplicarRegla`, `deshacerLoteRegla`.
  Hooks: `useReglaDetalle`, `useReglasAutollenadoLista` (lista cruda,
  comparte queryKey/caché con `useReglasAutollenado` que ya expone el
  Record indexado), `useActualizarParametrosRegla`, `useAplicarRegla`,
  `useDeshacerLoteRegla`.

## Diseño — `etl-upload.html` → `/etl/upload` (wizard, en curso)

La página más grande del prototipo (2941 líneas, todo el JS inline, sin
compartir `fuente-drawer.js` con las páginas ya migradas). Un fork analizó
el archivo completo antes de diseñar, para no cargar el HTML crudo en el
contexto de la conversación principal. Se acordó con el usuario: fidelidad
completa pero en sub-entregas, y estado del wizard en un store zustand
dedicado (`useEtlUploadStore`) porque es profundo y se comparte entre
muchos componentes hermanos (no `useReducer` local como en `EtlDatos`).

Solo **2 pasos** reales (el "paso 3" del CSS es un relicto sin sección
asociada): **Paso 1** analiza una fuente subiendo/detectando su archivo;
**Paso 2** es un mapeo de columnas por "secciones" de modelos donde **cada
sección se guarda e importa a la BD antes de pasar a la siguiente** (no
hay un paso 3 de importación final separado).

Endpoints nuevos identificados (ninguno estaba migrado): `POST
/api/fuentes-datos/{f}/upload/`, `GET /api/etl/campos-destino/?fuente=`,
`GET /api/etl/regex-sugerido/?fuente=&modelo=&campo=`, `POST
/api/etl/verificar-existencia/`, `POST
/api/fuentes-datos/{f}/carga/{c}/mapeo/` (el GET ya existía de
`etl-mapeo.html`), `POST .../previsualizar/`, `POST .../importar/`.

### Sub-entrega 1 — Paso 1 (completada)

- Stepper visual (① Analizar → ② Mapear), confirmado con el usuario en vez
  de solo un título de sección.
- `types/index.ts`: `ColumnaOrigen`, `MapeoColumnaPrevio`,
  `AnalizarFuenteResponse`, `ChoiceCampo`, `CampoDestino`,
  `GrupoModeloInfo`, `TipoCobertura`, `CamposDestinoResponse`.
- `etl.service.ts`: `analizarFuente(fuenteId, archivo?)`,
  `getCamposDestino(fuenteId)`.
- `useEtlUploadStore` (zustand): `step`, `fuenteId`, `cargaId`, `columnas`,
  `sheets`, `hojaActiva`, `totalFilas`, `mapeosPrevios`, `camposDestino` —
  se extiende en la sub-entrega 2 con `mapeoSeleccion`/`mapeoValores`/
  `atributosManuales`/`seccionesGuardadas`/`seccionIdx`.
- Hooks `useAnalizarFuente` (mutation que combina `upload` + `campos-destino`
  porque el wizard no puede mostrar el Paso 2 sin ambos) y
  `useCamposDestino`.
- Página `EtlUpload.tsx` reemplaza el stub `EtlProximamente` en
  `/etl/upload`: select de fuentes (sin filtro de proyecto, igual al
  prototipo), estado bloqueado si la fuente ya está completa (con links a
  `/etl/datos` y `/etl/mapeo`, ya migrados), archivo registrado, input de
  archivo, botón "Analizar archivo". El Paso 2 queda como placeholder
  informativo (columnas/filas detectadas) hasta la sub-entrega 2.
- **Verificación:** se creó una fuente de prueba temporal (`TEST_temporal_verificacion_ui`,
  id=33) vía API porque las 7 fuentes reales del proyecto IDEAM ya estaban
  todas en estado "completo" (bloqueadas) — se probó el flujo real de
  análisis contra el backend (`curl` con `multipart/form-data`, confirmando
  que la respuesta real coincide con los tipos, incluyendo la corrección de
  `sugerencias_hora`/`interpretaciones_hora`: son objetos `{valor: sugerencia}`,
  no arrays como se había tipado inicialmente) y se eliminó la fuente de
  prueba al terminar (`DELETE /api/fuentes-datos-crud/33/`, 204).

### Sub-entrega 2 — Paso 2 básico (completada)

Delegado a otra lectura directa del archivo (esta vez sin fork, leyendo
tramos puntuales: `seccionesDisponibles`/`seccionBloqueada`,
`renderMapeoRow` básico, `construirMapeos`/`guardarSeccion`/preview) para
confirmar shapes exactos de los endpoints nuevos contra el código real del
backend (`_columnas_desde_dataframe`, `campo_to_catalogo`, `previsualizar_carga`,
`importar_carga`, `mapeo_carga` POST).

- Nuevos pure-helpers en `utils/etlMapeo.ts`: `sugerirMapeo`/`normalizarNombre`
  (sugerencia por similitud), `seccionesDisponibles`/`seccionesReales`/
  `seccionBloqueada`/`contarColumnasSinMapear` (navegación de secciones),
  `construirMapeos` (payload del POST), `valoresDetectadosParaCampo`/
  `unidadExperimentalYaMapeada`/`origenUnidadExperimentalMapeada` (mensajes
  de vínculo automático UnidadMuestreo/Parcela/Transecto).
- `useEtlUploadStore` extendido: `mapeoSeleccion`, `atributosManuales`,
  `seccionIdx`, `seccionesGuardadas`, más `aplicarMapeosGuardados`/
  `aplicarSugerencias` internos al `setAnalisis`.
- `etl.service.ts` extendido: `postMapeo`, `previsualizarSeccion`,
  `importarSeccion` — estas dos últimas devuelven el error de validación
  (400 con `ok:false`) como valor normal en vez de excepción, porque es un
  resultado "esperado" del formulario, no una falla de red.
- Componentes nuevos en `components/etl-upload/`: `SeccionNav`, `MapeoRow`
  (select modelo/campo/tipo_cobertura), `AtributoManualRow`, `MapeoList`
  (agrupación por entidad + mensajes de vínculo + "Todos los atributos"),
  `PreviewModal` (tabla nuevo/existente antes de importar).
- Integrado en `EtlUpload.tsx`: nav de secciones, "Guardar avance"
  (parcial), "Validar y guardar sección" → preview → confirmar → importar
  → avanza automáticamente, "🚫 No tengo datos de esta sección" (con
  `window.confirm` nativo, igual que el prototipo — no se justificaba un
  modal nuevo para esa confirmación de bajo riesgo), banner de carga
  completa, "Volver al paso 1" (se agregó `setStep` al store para esto:
  el prototipo solo cambia de vista sin perder el progreso del mapeo, así
  que NO se podía reusar `setFuenteId`, que sí resetea todo).
- **Gap conocido (documentado, no bloqueante):** `aplicarMapeosGuardados`
  todavía no restaura `extrasDestino` ni `mapeoValores` (choices) de cargas
  previas — esos conceptos son de la sub-entrega 3. Si una fuente ya tenía
  esos mapeos guardados desde el prototipo original y el usuario hace
  "Guardar avance"/"Guardar sección" en esta versión antes de que la
  sub-entrega 3 esté lista, el backend los borra (diff por ausencia). Bajo
  riesgo hoy: ninguna fuente real del proyecto tiene ese tipo de mapeo
  guardado todavía.
- **Verificación:** se creó otra fuente de prueba temporal
  (`TEST_temporal_paso2`, id=34) con un CSV real subido por `curl -F`
  (columnas `nombre_unidad_experimental`, `fecha`, `hora`, `valor_flujo`),
  y se probó en navegador contra Docker: la sugerencia automática mapeó
  las 4 columnas correctamente por similitud de nombre; "Guardar avance"
  hizo un POST real; el primer intento de "Validar y guardar sección" dio
  el error real esperado (la fuente no tenía proyecto asignado, un caso
  de validación genuino, no un bug); tras asignarle proyecto vía
  `PATCH /api/fuentes-datos-crud/34/`, el flujo completo funcionó: preview
  con datos reales (1 nuevo, 1 reutilizado), confirmar e importar escribió
  de verdad en la base, avanzó automáticamente a "Unidad de Muestreo" con
  su mensaje de vínculo automático correcto. Se limpiaron los datos de
  prueba al terminar (`UnidadExperimental` creada, `CargaArchivo` y
  `FuenteDatos` de ambas fuentes de prueba) vía shell de Django dentro del
  contenedor Docker del backend. `tsc -b` (modo build, más estricto que
  `--noEmit`) detectó dos errores de tipado propios en `etlMapeo.ts`
  (narrowing de `mejor` en un closure anidado, y un array de payload sin
  tipo de retorno explícito) — corregidos antes de dar por buena la
  sub-entrega.

### Sub-entrega 3a — nulos + choices (completada)

Se dividió la sub-entrega 3 original en 3a/3b por acuerdo con el usuario
(6 piezas bastante distintas era demasiado para una sola verificación).
Otro fork leyó las funciones puntuales del prototipo
(`construirPanelHoras`, `construirPanelNulos`, `columnaEsCompleja`,
`abrirModalRevision`, el sub-panel de choices, `renderExtraRow`, helpers
de regex) para tener el detalle exacto de las 6 piezas antes de planear —
confirmó además que `factor_escala` (existe en el modelo `MapeoColumna`
del backend) **no tiene ninguna UI en el prototipo**, así que se sigue
omitiendo en la migración sin pérdida de funcionalidad.

- `MapeoSeleccion` extendido con `estrategiaNulos`/`valorRellenoManual`;
  store con `mapeoValores: Record<idx, Record<valorOrigen, valorDestino>>`
  y acciones `setEstrategiaNulos`/`setValorRellenoManual`/`setValorChoice`.
- `etlMapeo.ts`: `sugerirValor`/`normalizarUnidad` (sugerencia de valor
  discreto por similitud, igual algoritmo que `sugerirMapeo` pero contra
  choices) y `aplicarSugerenciasValores` (se corre en `setAnalisis`, como
  `aplicarSugerencias` con modelo/campo). `construirMapeos` actualizado
  para usar los valores reales en vez de los placeholders `'dejar_null'`/`{}`
  de la sub-entrega 2.
- **Se cerró parte del gap documentado en la sub-entrega 2:**
  `aplicarMapeosGuardados` ahora sí restaura `mapeo_valores` de cargas
  previas (seguía pendiente solo `extrasDestino`, que es de 3b).
- Componentes nuevos: `NulosPanel.tsx` (4 radios + input condicional),
  `ChoicesPanel.tsx` (select por valor único). Integrados en `MapeoRow.tsx`
  con las mismas condiciones de mutua exclusión que el prototipo (un
  campo con choices nunca es `TimeField`, así que no hace falta chequear
  el tipo explícitamente — ya es exclusivo por construcción).
- **Verificación:** fuente de prueba temporal (`TEST_temporal_paso3a`,
  id=35) con CSV real (`nombre_unidad_experimental`, `tipo`, `descripcion`
  con una fila vacía) subido por `curl -F`. En navegador vía Docker: la
  sugerencia automática de valores mapeó "parcela"→"Parcela" y
  "transecto"→"transecto" correctamente contra las choices reales del
  campo, y el panel de nulos detectó la fila vacía de `descripcion`. Hard
  refresh + verificación de consola limpia. Se limpiaron los datos de
  prueba (`CargaArchivo`, `FuenteDatos`) vía shell de Django.

### Sub-entrega 3b — horas ambiguas + modal + regex + extras (completada)

La pieza más grande del plan de migración. Se leyeron directamente las
funciones restantes del prototipo (`construirPanelHoras`,
`construirPanelNulos`, `columnaEsCompleja`, `abrirModalRevision`, el
sub-panel de choices, `renderExtraRow`, `aplicarRegexValor`,
`advertenciaLookbehindPython`, `crearVistaPreviaRegex`) y del backend
(`verificar_existencia`, `regex_sugerido`) para tener el detalle exacto.

- **Corrección de fidelidad respecto a la sub-entrega 3a:** en el
  prototipo, cualquier columna con `nulls > 0` ya cuenta como "compleja"
  (`columnaEsCompleja`), lo que significa que el panel de nulos **nunca**
  se muestra inline solo — siempre va detrás del botón "🔍 Revisar" +
  modal. La 3a lo mostraba inline siempre (simplificación deliberada de
  esa entrega). Se corrigió acá: `NulosPanel`/`HorasPanel` ahora solo se
  renderizan dentro de `ReviewModal`, gatillado por `columnaEsCompleja`
  (horas ambiguas OR nulos por resolver OR errores previos de la última
  validación).
- Tipos: `ExtraDestino`, `RegexSugeridoResponse`, `VerificarExistenciaResponse`;
  `MapeoSeleccion` con `aplicarRegex`/`regexPatron`.
- `etl.service.ts`: `getRegexSugerido`, `verificarExistencia`.
- Store: `extrasDestino[]`, `ultimosErroresPorColumna` (poblado automáticamente
  desde `usePrevisualizarSeccion`/`useImportarSeccion` cuando la respuesta
  es un error de validación); acciones de regex/extras. Se cerró el gap
  restante de la sub-entrega 2: `aplicarMapeosGuardados` ahora también
  restaura `extrasDestino` de cargas previas.
- `etlMapeo.ts`: `columnaEsCompleja`, `aplicarSugerenciasHora` (siembra
  `mapeoValores` con las sugerencias de hora del backend, igual patrón que
  `aplicarSugerenciasValores`), `muestraAleatoria`/`aplicarRegexValor`/
  `advertenciaLookbehindPython` (vista previa de regex, mismo algoritmo
  que el backend), `construirMapeos` extendido con `regex_patron` y los
  `extrasDestino`.
- Componentes nuevos: `HorasPanel`, `ReviewModal` (errores + horas + nulos +
  tabla de interpretación final o lista de valores únicos), `RegexPreview`
  (5 valores al azar, recalculo en vivo, aviso de lookbehind Python,
  verificación de existencia vía `useVerificarExistencia` — el
  "secuenciamiento" del prototipo para descartar respuestas obsoletas se
  resuelve gratis con el cacheo por queryKey de react-query, sin guarda
  manual), `ExtraRow` (destino extra ya resuelto, vive en la sección de su
  modelo). `MapeoRow` extendido con toggle de regex + filas de destino
  extra pendientes. `MapeoList` extendido para agrupar extras resueltos
  junto con las columnas de cada entidad.
- Hooks: `useRegexSugerido` (mutation, bajo demanda al activar el toggle),
  `useVerificarExistencia` (query).
- **Verificación:** fuente de prueba temporal (`TEST_temporal_paso3b`,
  id=36) con CSV real (`codigo_completo` con valores tipo
  `SWAMP_CO2_ParcelaA_001`, `descripcion` con una fila vacía). En
  navegador vía Docker: el botón "🔍 Revisar (1 fila vacía)" reemplazó
  correctamente al panel inline; el modal mostró nulos + lista de valores
  únicos; se agregó un destino extra (`codigo_completo` → también
  `UnidadExperimental.nombre`) que se agrupó correctamente en esa sección
  ("1 columna + 1 extra"); al activar regex sobre ese extra con el patrón
  `^SWAMP_CO2_(.+?)_\d+$`, la vista previa extrajo "ParcelaA"/"ParcelaB" en
  vivo y la verificación de existencia contra el backend real confirmó
  "＋ se crearía nuevo" para ambos (correcto, no existían aún). Consola
  limpia tras hard-refresh. Datos de prueba eliminados.
  **Gap de verificación (no de código):** no se probó en navegador el
  panel de horas ambiguas con un campo `TimeField` real por límite de
  tiempo — comparte exactamente el mismo patrón de siembra/gate que
  `ChoicesPanel`/`NulosPanel` (ambos sí verificados), así que el riesgo
  residual es bajo, pero queda pendiente de una verificación futura si
  aparece un caso real.

Con esto, **`etl-upload.html` queda migrado por completo** (Paso 1 +
Paso 2 básico + paneles avanzados) — cierra el ítem más grande del plan
de migración original.

## Diseño — `data.html` → `/data` (completado)

`data.html` en el prototipo delega casi toda la lógica a 7 módulos JS
(`data-page/*.js`) que no se habían leído todavía. Un fork los analizó
para reportar estructura, endpoints, drawers y acciones antes de diseñar.

### Decisiones tomadas con el usuario

- **Restricción "solo admin puede borrar fuentes completas":** el
  prototipo la implementa con un selector de rol temporal en localStorage
  (`role-guard.js`, sin auth real) que no migramos. El usuario pidió
  **omitirla por ahora** y resolverla como parte de una futura
  funcionalidad de gestión de perfiles (cuando exista login, mostrar el
  rol debajo del nombre de la persona) — no se porta `role-guard.js`.
- **Paginación:** el prototipo tiene paginación decorativa (siempre
  "Página 1 de 1", botones deshabilitados — sin paginación real, todo se
  trae de una vez y se pagina/filtra en el cliente). El usuario pidió
  **paginación real client-side** — mejora sobre el original, usando el
  componente `Paginacion` ya existente con slice sobre el array filtrado.
- **Confirmación de borrado:** se reusa `ConfirmModal` (ya construido
  para reglas de autollenado) en vez del `window.confirm()` nativo del
  prototipo.

### Endpoints nuevos (todos verificados contra `app/api/urls.py`)

`POST /api/proyectos/crear/`, `GET /api/instituciones/`,
`GET /api/roles-usuario/`, `POST /api/usuarios/`,
`PATCH /api/usuarios/{id}/`, `DELETE /api/fuentes-datos-crud/{id}/`.
`GET /api/fuentes-datos/` (fuentes+proyectos juntos) ya estaba migrado
como `fuentesService.listFuentesDropdown` — se reusa tal cual, sin
paginación de servidor (igual que el prototipo).

### Implementado

- Tipos: `Proyecto`/`ProyectoPayload`, `Institucion`, `RolUsuario`,
  `UsuarioPayload` (reusa el tipo `Responsable` ya existente para la
  entidad usuario, mismo serializer que `/api/responsables/`).
- Servicios: `proyectos.service.ts` (`crearProyecto`), `usuarios.service.ts`
  (`listInstituciones`, `listRolesUsuario`, `crearUsuario`,
  `actualizarUsuario`), `fuentes.service.ts` extendido con
  `eliminarFuente`.
- Stores nuevos: `useProyectoDrawerStore` (solo crear, como el
  prototipo), `useUsuarioDrawerStore` (crear + editar, aunque `data.html`
  solo dispara "crear" — se construyó soporte de edición completo porque
  el módulo original `responsable-drawer.js` ya lo soporta y `team.html`,
  el próximo paso del plan, previsiblemente lo va a necesitar).
- Componentes: `ProyectoDrawer`, `UsuarioDrawer` (mismo patrón visual que
  `FuenteDrawer`), `ProyectosTable` (búsqueda + paginación real +
  "Ver fuentes" cruzado + link a `/etl/datos?proyecto=`), `FuentesTable`
  (búsqueda + filtros tipo/estado/proyecto incluyendo "sin proyecto" +
  paginación real + acciones editar/eliminar/ETL, reusando
  `FuenteDrawer`/`useFuenteDrawerStore` ya existentes para editar).
  `ApiStatusCard`/`StatsBar` como componentes locales pequeños dentro de
  `DataGestion.tsx` (single-use, sin abstraer a archivos aparte).
- Página `DataGestion.tsx` en `/data`, con el filtro de proyecto
  compartido entre ambas tablas vía estado local + scroll automático a
  la tabla de fuentes (igual que `filterByProject` del prototipo).
- **Corrección de navegación:** se descubrió que en el prototipo
  `data.html` (no `etl-datos.html`) es el punto de entrada real del nav
  (`layout.js` → `NAV_LINKS`: Equipo, Base de datos, "📂 Datos"). Se
  actualizó la card de `/reportar` (antes "ETL de Datos" → `/etl/datos`)
  para apuntar a `/data` y se renombró a "Gestión de Datos", más fiel al
  prototipo — `/etl/datos` sin parámetros no es una página de aterrizaje
  útil (pide fuente/proyecto). También se cerró el gap documentado en
  `etl-datos.html`/`etl-mapeo.html`/`etl-upload.html`: sus links
  "← Volver" (cuando no hay contexto de fuente) ahora apuntan a `/data`
  en vez del `/reportar` provisional.
- **Verificación:** en navegador vía Docker con datos reales (7 fuentes,
  2 proyectos: IDEAM con 5 fuentes, SWAMP con 2): "Ver fuentes" filtró
  correctamente y con scroll automático; se creó un proyecto de prueba
  real (`TEST_temporal_proyecto_ui`, id=10) vía el drawer, apareció
  correctamente en la tabla con "0 fuentes", y se eliminó al terminar
  (`DELETE /api/proyectos/10/`, 204 — confirma que `ProyectoViewSet`
  soporta borrado aunque el prototipo no lo expone); el modal de
  confirmación de borrado de fuente mostró el mensaje correcto (cancelado
  sin confirmar, para no borrar datos reales); el drawer de usuario cargó
  los roles reales del backend (Administrador de datos, Coordinador,
  Investigador, Reportador) con "Reportador" premarcado. Sin errores de
  consola. `tsc -b`/`npm run build` limpios.

## Diseño — Sistema de roles (post-`data.html`, completado)

Al cerrar `data.html` había quedado pendiente la restricción "solo
`admin_datos` borra fuentes completas" (se había omitido porque dependía
de `role-guard.js`, un selector de rol suelto en localStorage sin
relación con ningún dato real). El usuario pidió integrarla para cerrar
esa parte de la migración, pero explícitamente **no** replicar el hack
del prototipo — pidió algo "más robusto".

**Diseño elegido:** en vez de un selector de rol abstracto, la sesión
simulada se ata a un **Usuario real** de `/api/usuarios/` — esos usuarios
ya tienen roles asignados de verdad en la base de datos (se verificó con
`curl`: p. ej. "Alejandra Diaz" tiene `admin_datos` entre sus roles). Es
más robusto porque los roles no se inventan client-side, se leen del
dato real, y sienta la base para `team.html` (directorio de usuarios) sin
duplicar catálogos.

- `useSesionStore` (zustand + middleware `persist`, ya disponible en el
  proyecto) — `usuarioActualId` persistido en localStorage bajo la key
  `colflux-sesion`. Reemplaza el `localStorage.getItem/setItem` manual
  del prototipo por el middleware estándar de zustand.
- `usuarios.service.ts` + `useUsuarios`: `GET /api/usuarios/` (lista
  completa, no solo reportadores — endpoint ya existía, solo no se había
  consumido para un listado general).
- `useRolActual`: combina el store + `useUsuarios`, deriva
  `{ usuario, roles, isAdmin }` (`isAdmin` = tiene `admin_datos` entre
  sus roles).
- `SesionSelector.tsx`, montado en `Navbar.tsx` junto al botón "Iniciar
  sesión" (placeholder ya existente, sin auth real): dropdown para
  "actuar como" un usuario real, con sus roles mostrados debajo del
  nombre — replica literalmente el pedido del usuario ("que debajo del
  nombre de la persona exista el rol") aunque todavía sin login de
  verdad.
- `FuentesTable.tsx`: el botón "eliminar" de una fuente con
  `estado === 'completo'` ahora usa `useRolActual().isAdmin` con el mismo
  criterio que `fuentes-section.js` del prototipo (`!completa || isAdmin`).
  La restricción de **edición** de fuentes completas sigue sin excepción
  de admin (igual que el prototipo — ahí no hay bypass por rol).
- **Verificación:** en navegador vía Docker, sesión "sin sesión" bloquea
  el botón eliminar de una fuente completa (atenuado, con tooltip);
  seleccionar "Alejandra Diaz" (rol real `admin_datos` en la BD) muestra
  sus 4 roles debajo del nombre y habilita el botón eliminar
  inmediatamente; la selección persiste tras recargar la página (confirma
  que el middleware `persist` funciona). Sin errores de consola.
  `tsc -b`/`npm run build` limpios.

## Diseño — `db.html` → `/db` (completado)

`db.html` es distinto de las páginas anteriores: no tiene backend real. Su
diagrama ERD, explorador de relaciones y catálogo de campos leen todos de
`window.CATALOGO`, cargado desde `../assets/data/catalogo.js` (un archivo
estático generado por `app/catalogo/generator.py` vía el management
command `generate_catalogo`). Se confirmó leyendo `generator.py` que
`generar_catalogo_data()` **nunca se expone por `/api/...`** — solo se
escribe a disco (`catalogo.json`/`catalogo.js`) con
`escribir_catalogo_assets()`.

### Decisiones tomadas con el usuario (fuente de datos)

Se plantearon tres opciones y se iteró con el usuario hasta la decisión
final:

1. **Endpoint nuevo `/api/catalogo/` + cache** — descartada: el usuario
   señaló que el catálogo solo cambia cuando se despliega una versión
   nueva del backend con cambios de modelo, no quería "estar importando
   ese archivo cada nada" con una llamada de red en cada visita.
2. **Embeber la página del prototipo vía `<iframe>` desde el backend**
   (propuesta intermedia del usuario para evitar reconstruir el ERD) —
   evaluada y finalmente descartada por el propio usuario ("creo que
   mejor reconstruirlo"), volviendo al alcance original de migración
   completa en React.
3. **Archivo estático empaquetado en el proyecto frontend** (elegida) —
   el usuario confirmó: "tendría sentido hacer la carga cuando se
   despliega la app y se guarda como archivo del proyecto". Se copió
   `backend/docs/assets/data/catalogo.json` →
   `frontend/src/assets/data/catalogo.json` (145 KB, 12 grupos, 40
   entidades) como snapshot versionado, importado directamente con
   `import catalogoJson from '@/assets/data/catalogo.json'`
   (requirió agregar `resolveJsonModule: true` a `tsconfig.app.json`,
   no estaba habilitado).

**Gap de despliegue documentado (no bloqueante hoy):** este archivo debe
resincronizarse manualmente cada vez que cambia el esquema de modelos en
el backend — no hay automatización todavía. Candidato natural: agregar un
paso al pipeline de `automatizar-deploy-ecosistema-colflux.md` que corra
`generate_catalogo` y copie el JSON resultante al repo del frontend antes
de buildear. No se implementó en esta tarea (fuera de alcance).

### Alcance confirmado con el usuario

"Migrar todo junto: ERD + explorador + catálogo" (se descartó dividir en
sub-entregas porque el ERD, aunque es un patrón de renderizado nuevo
—líneas SVG medidas por posición DOM—, no es tan grande: 40 nodos).

### Estructura implementada

```
src/utils/catalogoModel.ts     ← import del JSON estático + modelo derivado
                                  una sola vez (ENTIDAD_MAP, RELACIONES,
                                  color por grupo con la misma paleta que
                                  ya usaba MapeoList.tsx para mapeo de
                                  columnas — GRUPO_PALETTE compartida)
src/components/db/
  ErdDiagram.tsx    ← columnas por grupo, nodos expandibles (toggle),
                        conectores SVG (bezier + flechas + etiquetas N/1)
                        recalculados con getBoundingClientRect tras cada
                        toggle/resize (mismo algoritmo que el prototipo,
                        portado a refs + useLayoutEffect en vez de
                        manipulación directa del DOM)
  EntityExplorer.tsx ← tarjeta central + relaciones salientes/entrantes,
                        controlado por el mismo estado "abierta" del ERD
  CatalogoCampos.tsx ← sidebar agrupado + tabla de campos con búsqueda,
                        resaltado de coincidencias, toggle de choices,
                        botón copiar, tabla de datos semilla
src/pages/DbModelo.tsx  ← compone las 3 secciones, registrado en /db
```

Tipos nuevos en `types/index.ts`: `EntidadCatalogo`, `GrupoCatalogo`,
`CatalogoData` (reusan `CampoDestino`/`ChoiceCampo`, ya existentes desde
la migración de `etl-upload.html`, porque `campo_to_catalogo()` en el
backend genera exactamente la misma forma que `campos-destino`).

No se creó un hook `useCatalogo()` — al ser datos estáticos importados en
build-time (no async, no hay fetch), el modelo derivado se computa una
sola vez a nivel de módulo en `catalogoModel.ts` en vez de envolverlo en
`useQuery`/`useMemo` sin necesidad real.

### Verificación

`tsc -b` y `npm run build` limpios. En navegador vía Docker
(`localhost:3000/db`): el ERD renderiza 40 entidades / 45 relaciones en
12 columnas por grupo con los colores esperados; clic en `UnidadMuestreo`
expande el nodo mostrando sus 7 campos con badges FK y dispara el
explorador de relaciones abajo (4 salientes, 5 entrantes, tarjeta central
con los mismos campos); "Ver en catálogo →" navega y hace scroll al
catálogo seleccionando la entidad correcta; la búsqueda "sitio"/"gas"
filtra la sidebar y resalta coincidencias en la tabla; el toggle de
choices del campo `gas` en `MuestraGEI` abre correctamente mostrando
CO2/CH4/N2O. Sin errores de consola. Ajuste visual menor durante la
verificación: el nombre del grupo en el header de la tarjeta central del
explorador se solapaba con el nombre de la entidad para grupos con
nombres largos — corregido con `truncate`/`whitespace-nowrap`.

## Diseño — `team.html` → `/team` (completado)

Última página del plan de migración original. A diferencia del prototipo
(que no restringe el acceso — `role-guard.js` solo se usa para
mostrar/ocultar acciones puntuales en otras páginas, nunca para bloquear
`team.html` completa), el usuario pidió explícitamente: "esa página de
team solo está disponible para rol de administradores".

### Decisión tomada con el usuario (comportamiento del gate)

Se preguntó qué debía ver un usuario sin sesión `admin_datos`
seleccionada: el usuario eligió **redirigir silenciosamente a `/data`**
(sin mensaje de "acceso restringido" en `/team`), en vez de mostrar una
tarjeta de acceso denegado. Implementado con `<Navigate to="/data"
replace />` de `react-router-dom`, gateado por `useRolActual().isAdmin`
(el mismo hook ya construido para la restricción de borrado en
`FuentesTable.tsx`) — primera vez que se usa ese hook para restringir una
página completa en vez de una sola acción.

### Bug encontrado y corregido antes de migrar

Al revisar `useUsuarioMutations.ts` para reusarlo en `team.html`, se
detectó que `useCrearUsuario`/`useActualizarUsuario` solo invalidaban la
query `['responsables']` (usada por el dropdown de `FuenteDrawer`), nunca
`['usuarios']` (usada por `useUsuarios`/`useRolActual`, y por la tabla
nueva de `team.html`) — un usuario creado o editado no se habría
reflejado en la tabla sin recargar la página. Se corrigió agregando la
invalidación de `['usuarios']` en ambos hooks, y también en los tres
hooks nuevos de instituciones (`useEliminarUsuario` invalida ambas
queries; `useCrearInstitucion`/`useActualizarInstitucion` invalidan
`['instituciones']`; `useEliminarInstitucion` invalida `['instituciones']`
y `['usuarios']`, porque borrar una institución afecta el nombre mostrado
en la tabla de usuarios).

### Endpoints nuevos (ModelViewSets completos, ya soportan CRUD sin cambios en el backend)

`DELETE /api/usuarios/{id}/`, `POST /api/instituciones/`,
`PATCH /api/instituciones/{id}/`, `DELETE /api/instituciones/{id}/`.
(`GET /api/usuarios/`, `GET /api/instituciones/`, `POST/PATCH
/api/usuarios/{id}/` ya estaban migrados desde `data.html`/el sistema de
roles.)

### Implementado

- Tipo `InstitucionPayload` nuevo en `types/index.ts`.
- `usuarios.service.ts` extendido: `eliminarUsuario`, `crearInstitucion`,
  `actualizarInstitucion`, `eliminarInstitucion`.
- `useUsuarioMutations.ts` extendido: `useEliminarUsuario`,
  `useCrearInstitucion`, `useActualizarInstitucion`,
  `useEliminarInstitucion` (más el fix de invalidación descrito arriba).
- `components/admin/team/InstitucionesAdmin.tsx` — form inline
  crear/editar (sin drawer, igual que el prototipo: institución es una
  entidad simple de 2 campos) + lista de chips con acciones editar/borrar,
  `ConfirmModal` para el borrado.
- `components/admin/team/UsuariosTable.tsx` — búsqueda + tabla, reusa
  `UsuarioDrawer`/`useUsuarioDrawerStore` ya construidos (desde
  `data.html`) para crear/editar, `ConfirmModal` para borrar en vez del
  `confirm()` nativo del prototipo.
- Página `Team.tsx` en `/team`: gate de admin al inicio del componente
  (retorna `null` mientras `useRolActual().cargando`, `<Navigate
  to="/data" />` si no es admin), luego secciones de Instituciones y
  Usuarios registrados + botón "＋ Nuevo usuario" + `UsuarioDrawer`
  montado localmente (mismo patrón que las demás páginas admin).
- Sin card de entrada en `/reportar` ni link en `Navbar` — igual que
  `/data`/`/db`, es una URL interna de administración, no de navegación
  pública.

### Verificación

`tsc -b`/`npm run build` limpios. En navegador vía Docker: con "Sin
sesión" seleccionada, navegar directamente a `/team` redirige de
inmediato a `/data` (confirmado tanto cambiando la sesión estando ya en
`/team` como cargando la URL directamente sin sesión de admin). Con
"Alejandra Diaz" (`admin_datos` real) se ve la página completa. Se probó
el CRUD contra el backend real con datos de prueba: institución
`TEST_temporal_institucion` creada (POST), editada con correo (PATCH,
reflejado sin recargar) y eliminada (DELETE + `ConfirmModal`); usuario
`TEST_temporal_usuario` creado desde el drawer (apareció de inmediato en
la tabla, confirmando el fix de invalidación de cache) y eliminado
(`ConfirmModal`). Sin errores de consola.

Con esto se cierran las 7 páginas del plan original de migración.

## Plan

- [x] Migrar `etl-datos.html` a React siguiendo el diseño de arriba
      (servicios + hooks + store del drawer + tipos + componentes),
      registrar ruta `/etl/datos` en `App.tsx`
- [x] Migrar `reglas-campo.html`, `regla-detalle.html`, `regla-validacion.html`
- [x] Migrar `etl-mapeo.html`
- [x] Migrar `etl-upload.html` (completo, por sub-entregas — ver Diseño arriba)
  - [x] Sub-entrega 1: Paso 1 — analizar fuente (select, subir archivo, estado bloqueado)
  - [x] Sub-entrega 2: Paso 2 — mapeo básico por sección + modal de previsualizar/importar
  - [x] Sub-entrega 3a: paneles inline simples (estrategia de nulos + mapeo de valores discretos/choices)
  - [x] Sub-entrega 3b: horas ambiguas + modal de revisión unificado + regex con vista previa/verificación de existencia + destinos extra
- [x] Migrar `data.html`
- [x] Migrar `db.html`
- [x] Migrar `team.html`
- [x] Retirar las páginas del prototipo (`backend/docs/pages/`) — hecho de
      una sola vez (no página por página como preveía este plan) en el
      commit `cb2942e` del backend, ya mergeado a `main` vía PR #9
- [ ] Abrir el PR del frontend con el commit de migración (`48b46da`, en la
      rama `feature/migrar-etl-admin-y-login`, ya pusheada a origin pero
      sin PR todavía) y mergearlo a `main`

## Entregables

- Backend: [PR #9](https://github.com/colflux/backend/pull/9) (mergeado) —
  incluye, además del login real, el commit `cb2942e` que retira por
  completo `backend/docs/pages/` y actualiza la landing (`/`) del backend
  para mostrar versión + botón al frontend.
- Frontend: commit `48b46da` ("migrar páginas ETL/admin del prototipo a
  React y agregar login real") en la rama `feature/migrar-etl-admin-y-login`,
  ya pusheado a origin — **falta abrir el PR** en `colflux/frontend` antes
  de mergear a `main`. Esa rama tiene además 2 cambios sin commitear
  (bump de versión a `1.1.0` en `package.json` y `Footer.tsx`) pendientes
  de decidir si van en el mismo PR.

## Referencias

- Prototipo: `backend/docs/pages/` (HTML/JS vanilla), config de API en
  `backend/docs/config/services.js`, JS compartido en
  `backend/docs/assets/js/` (`layout.js`, `role-guard.js`,
  `fuente-drawer.js`, `reglas-comun.js`)
- Frontend oficial: `colflux/frontend/src/` — mirar `pages/MapaInteractivo.tsx`
  y `pages/DashboardIndicadores.tsx` como referencia de patrón
  service→hook→página antes de escribir código nuevo
- Endpoints que consume `etl-datos.html`: `/api/reglas-autollenado/`,
  `/api/proyectos/{id}/datos/`, `/api/fuentes-datos/{id}/carga/{id}/datos/`,
  `/api/fuentes-datos/`, `/api/proyectos/{id}/exportar/`,
  `/api/fuentes-datos/{id}/carga/{id}/exportar/`

## Historial

| Fecha | Descripción |
|---|---|
| 2026-09-14 | Se crea la tarea, a partir de discusión sobre migrar `etl-datos.html` (y el resto de `docs/pages`) al frontend oficial en React. |
| 2026-09-14 | Se define el diseño detallado de `etl-datos.html`: se lee el HTML completo del prototipo y los servicios/hooks/tipos ya existentes en el frontend oficial; se confirma con el usuario el prefijo de ruta `/etl/...` y la decisión de construir el dropdown "Cargar" + drawer "Nueva fuente" como piezas compartidas (zustand) desde el arranque, ya que se reutilizan en páginas posteriores del plan de migración. |
| 2026-09-14 | Se completa la migración de `etl-datos.html` → `/etl/datos`, confirmando punto por punto con el usuario cada decisión de UI (layout, entrada desde `/reportar`, header, tabs, toolbar, colores de tabla, paginación, montaje del drawer, link de validación) antes de codear. Implementado: tipos nuevos en `types/index.ts`; servicios `fuentes.service.ts`, `reglas.service.ts`, `responsables.service.ts` y `getDatosCarga` en `datos.service.ts`; hooks `useDatosCarga`, `useFuentesDropdown`, `useReglasAutollenado`, `useResponsables`, `useFuenteMutations`; store `useFuenteDrawerStore` (zustand); componentes `CargarDropdown`/`FuenteDrawer` (compartidos, en `components/admin/fuentes/`), `DatosTabs`/`DatosToolbar`/`DatosTable`/`DatosTableFilterInput` (en `components/etl-datos/`), `Paginacion` (común); página `EtlDatos.tsx` con estado local vía `useReducer`; rutas stub `EtlProximamente` para `/etl/reglas/campo` y `/etl/upload`; card "ETL de Datos" agregada a `Participacion.tsx`. Verificado con `tsc --noEmit`, `npm run build`, y probado en el navegador contra el backend real (proyecto IDEAM id=9): tabs, filtros con debounce, paginación, dropdown de fuentes, drawer de nueva fuente, modo oscuro y el link de validación al stub, todo sin errores de consola. Gap conocido: cuando solo hay `?proyecto=` (sin fuente/carga), el botón "Volver" apunta a `/reportar` en vez de a `data.html` migrado, porque esa página todavía no existe en React (paso 5 del plan). |
| 2026-09-14 | El usuario pide quitar del grid de `Participacion.tsx` las cards "Desde la app" y "Reporte rápido" (no se explicitó el motivo) — hecho. Se levanta el contenedor Docker `frontend-dev-1` (estaba detenido) con `docker compose --profile dev up -d dev` para que el usuario vea los cambios en `localhost:3000`; el backend (`backend-web-1`) ya estaba arriba. |
| 2026-09-14 | Se completa la migración de `reglas-campo.html` / `regla-detalle.html` / `regla-validacion.html` → `/etl/reglas/campo`, `/etl/reglas/detalle`, `/etl/reglas/validacion` (esta última reemplaza el stub `EtlProximamente` que había quedado en `/etl/reglas/campo`), confirmando punto por punto con el usuario: histograma con recharts (no Chart.js, sin dependencia nueva) y confirmación de "Aplicar"/"Deshacer" vía modal centrado nuevo (`ConfirmModal`, decisión explícita pese a no tener precedente en el frontend). Implementado: tipos `DetalleRegla`/`ParametroSchema`/`CasoRegla`/`EjemploCandidato`/`ValidacionFila`/`HistorialAplicacion`; `reglas.service.ts` extendido con `getDetalleRegla`/`actualizarParametrosRegla`/`aplicarRegla`/`deshacerLoteRegla`; hooks `useReglaDetalle`, `useReglasAutollenadoLista`, `useReglaMutations`; componente común `ConfirmModal`; páginas `EtlReglasCampo`, `EtlReglaDetalle`, `EtlReglaValidacion`. Verificado con `tsc --noEmit`, `npm run build`, y probado en navegador vía Docker contra datos reales: hub de tarjetas (2 reglas de autollenado + 1 de validación, dedupe por campo igual que el prototipo), detalle con parámetros/casos/historial, modal de "Aplicar regla" (cancelado a propósito sin confirmar para no mutar los 978 registros pendientes reales), y la vista de validación con tabla + histograma (detectó una anomalía real: condición "Día" con horas fuera de 06:00–18:00). Sin errores de consola. |
| 2026-09-14 | Se completa la migración de `etl-mapeo.html` → `/etl/mapeo` (página de solo lectura, más simple que las anteriores: sin preguntas de diseño adicionales, reutiliza los patrones de header/toolbar ya establecidos). Implementado: tipos `MapeoColumna`/`MapeoCarga`; `mapeo.service.ts` (`getMapeoCarga`); hook `useMapeoCarga`; util `downloadJson` agregado a `utils/download.ts` (complementa `downloadFile`, que pide el archivo al backend — este descarga un objeto ya en memoria); página `EtlMapeo.tsx` con tabla de columnas (pills modelo/transformación), botón de descarga del mapeo como JSON, y link cruzado a `/etl/datos?fuente=&carga=`. Mismo gap ya conocido: "Volver" apunta a `/reportar` porque `data.html` no está migrado. Verificado con `tsc --noEmit`, `npm run build`, y en navegador vía Docker contra una carga real (fuente=26 "IDEAM Humedales - Biomasa", carga=211): tabla de mapeo completa con transformaciones y reglas de valor mapeado, y el link "Ver datos cargados" navega correctamente a `/etl/datos?fuente=26&carga=211` (que a su vez muestra el estado vacío correcto en CO₂ porque esa carga es de Biomasa, confirmando la integración cruzada entre ambas páginas). Sin errores de consola. |
| 2026-09-14 | Empieza la migración de `etl-upload.html` (la más grande, 2941 líneas). Se delega el análisis completo del archivo a un fork para no cargar el HTML crudo en el contexto principal; el fork reporta 2 pasos reales, el estado del wizard, los endpoints nuevos, y que no reutiliza el drawer/dropdown ya migrados. Se acuerda con el usuario: fidelidad completa pero en sub-entregas, y `useEtlUploadStore` (zustand) en vez de `useReducer` local por lo profundo/compartido del estado. Se completa la **sub-entrega 1 (Paso 1 — analizar fuente)**: tipos nuevos, `etl.service.ts` (`analizarFuente`, `getCamposDestino`), store `useEtlUploadStore`, hooks `useAnalizarFuente`/`useCamposDestino`, página `EtlUpload.tsx` (reemplaza el stub `EtlProximamente`) con stepper visual confirmado con el usuario, select de fuentes, estado bloqueado, subida de archivo. Verificado con `tsc --noEmit`/`npm run build`; como las 7 fuentes reales del proyecto ya estaban "completo" (bloqueadas), se creó una fuente de prueba temporal vía API (id=33) para probar el `POST .../upload/` real con `curl -F` — esto detectó y corrigió un error de tipado propio (`sugerencias_hora`/`interpretaciones_hora` son objetos, no arrays) — y se eliminó la fuente de prueba al terminar. Nota técnica: tras el cambio en `App.tsx`, el HMR del contenedor Docker quedó con una referencia obsoleta a `EtlProximamente` (ya no importado) hasta hacer hard-refresh del navegador — no es un bug del código, es un artefacto de hot-reload. |
| 2026-09-14 | Se completa la **sub-entrega 2 (Paso 2 básico — mapeo por sección + preview/import)** de `etl-upload.html`. Se leyeron directamente los tramos clave del prototipo (navegación de secciones, fila básica de mapeo, `construirMapeos`/`guardarSeccion`/preview) y del backend (`_columnas_desde_dataframe`, `campo_to_catalogo`, `previsualizar_carga`, `importar_carga`) para tipar con precisión. Implementado: helpers puros en `utils/etlMapeo.ts` (sugerencia por similitud, navegación/bloqueo de secciones, `construirMapeos`, mensajes de vínculo automático); `useEtlUploadStore` extendido con `mapeoSeleccion`/`atributosManuales`/`seccionIdx`/`seccionesGuardadas` y `setStep` (agregado porque "Volver al paso 1" del prototipo NO resetea el progreso, a diferencia de `setFuenteId`); `etl.service.ts` extendido con `postMapeo`/`previsualizarSeccion`/`importarSeccion` (estas devuelven el error 400 de validación como valor, no excepción); componentes `SeccionNav`/`MapeoRow`/`AtributoManualRow`/`MapeoList`/`PreviewModal`; todo integrado en `EtlUpload.tsx`. Gap documentado: `aplicarMapeosGuardados` aún no restaura `extrasDestino`/`mapeoValores` (sub-entrega 3) — riesgo bajo porque ninguna fuente real tiene ese tipo de mapeo guardado todavía. Verificado con `tsc -b` (más estricto que `--noEmit`, detectó y permitió corregir dos errores de tipado propios) y `npm run build`, y probado end-to-end en navegador vía Docker con una fuente de prueba temporal (id=34, CSV real subido por `curl -F`): sugerencia automática mapeó las 4 columnas correctamente, "Guardar avance" hizo un POST real, el primer intento de guardar sección dio un error de validación genuino (fuente sin proyecto asignado) que se mostró correctamente, y tras corregirlo el flujo completo (preview con datos reales → confirmar → importar → avance automático a la siguiente sección con su mensaje de vínculo) escribió de verdad en la base de datos. Se limpiaron todos los datos de prueba (`UnidadExperimental`, `CargaArchivo`, `FuenteDatos`) vía shell de Django en el contenedor Docker. |
| 2026-09-14 | Se divide la sub-entrega 3 restante de `etl-upload.html` (6 piezas: nulos, choices, horas ambiguas, modal de revisión, regex con preview/verificación de existencia, destinos extra) en 3a/3b por acuerdo con el usuario. Se completa **3a (nulos + choices)**: otro fork leyó las 6 funciones puntuales del prototipo y confirmó que `factor_escala` no tiene UI en el prototipo (se sigue omitiendo, sin pérdida). Implementado: `MapeoSeleccion.estrategiaNulos`/`.valorRellenoManual`; store con `mapeoValores` y sus acciones; `sugerirValor`/`normalizarUnidad`/`aplicarSugerenciasValores` en `etlMapeo.ts`; `construirMapeos` ya usa los valores reales en vez de los placeholders de la sub-entrega 2; componentes `NulosPanel`/`ChoicesPanel` integrados en `MapeoRow`. Se cerró parte del gap de la sub-entrega 2: `aplicarMapeosGuardados` ahora restaura `mapeo_valores` de cargas previas (falta solo `extrasDestino`, que es 3b). Verificado con `tsc -b`/`npm run build` y en navegador vía Docker con una fuente de prueba temporal (id=35): la sugerencia automática de valores mapeó "parcela"→"Parcela" y "transecto"→"transecto" contra choices reales, y el panel de nulos detectó correctamente una fila vacía real. Consola limpia tras hard-refresh; datos de prueba eliminados. |
| 2026-09-14 | Se completa **3b (horas ambiguas + modal de revisión + regex + destinos extra)**, cerrando la migración completa de `etl-upload.html` — la página más grande del prototipo. Se leyeron directamente las funciones restantes del archivo original y del backend (`verificar_existencia`, `regex_sugerido`) para el detalle exacto. Se corrigió una desviación de fidelidad introducida en 3a: cualquier columna con `nulls > 0` cuenta como "compleja" en el prototipo y nunca muestra el panel de nulos inline solo, siempre detrás de "🔍 Revisar" + modal — 3a lo mostraba inline siempre; ahora `NulosPanel`/`HorasPanel` solo viven dentro de `ReviewModal`. Implementado: tipos `ExtraDestino`/`RegexSugeridoResponse`/`VerificarExistenciaResponse`; `etl.service.ts` con `getRegexSugerido`/`verificarExistencia`; store con `extrasDestino`/`ultimosErroresPorColumna` (se cerró el gap final de la sub-entrega 2: `aplicarMapeosGuardados` ya restaura `extrasDestino`); `columnaEsCompleja`/`aplicarSugerenciasHora`/helpers de regex en `etlMapeo.ts`; componentes `HorasPanel`/`ReviewModal`/`RegexPreview`/`ExtraRow`; `MapeoRow`/`MapeoList` extendidos. La "guarda de secuencia" del prototipo para descartar verificaciones de existencia obsoletas se resolvió gratis con el cacheo por queryKey de react-query, sin código manual. Verificado con `tsc -b`/`npm run build` y en navegador vía Docker con una fuente de prueba temporal (id=36): el botón "Revisar" reemplazó correctamente al panel inline; el destino extra se agrupó bien en su sección ("1 columna + 1 extra"); el regex `^SWAMP_CO2_(.+?)_\d+$` extrajo "ParcelaA"/"ParcelaB" en vivo y la verificación de existencia contra el backend real confirmó "se crearía nuevo" para ambos. Consola limpia, datos de prueba eliminados. Gap de verificación (no de código): no se probó en navegador el panel de horas ambiguas con un `TimeField` real por límite de tiempo — comparte el mismo patrón ya verificado en `ChoicesPanel`/`NulosPanel`, riesgo residual bajo. |
| 2026-09-14 | Se completa la migración de `data.html` → `/data`. Un fork leyó los 7 módulos JS de los que depende la página (`data-state.js`, `etl-actions.js`, `proyectos-section.js`, `fuentes-section.js`, `data-main.js`, `proyecto-drawer.js`, `responsable-drawer.js`) para reportar estructura, endpoints y acciones antes de diseñar. Decisiones con el usuario: se omite por ahora la restricción "solo admin borra fuentes completas" (el prototipo la resuelve con un selector de rol temporal sin auth real) — queda para una futura funcionalidad de gestión de perfiles con login real; se implementa paginación client-side real (el prototipo la tenía decorativa/deshabilitada) con el componente `Paginacion` ya existente; se reusa `ConfirmModal` en vez de `window.confirm()`. Implementado: tipos `Proyecto`/`ProyectoPayload`/`Institucion`/`RolUsuario`/`UsuarioPayload`; servicios `proyectos.service.ts`/`usuarios.service.ts` y `eliminarFuente` en `fuentes.service.ts`; stores `useProyectoDrawerStore`/`useUsuarioDrawerStore`; componentes `ProyectoDrawer`/`UsuarioDrawer` (mismo patrón que `FuenteDrawer`), `ProyectosTable`/`FuentesTable` (reusan `FuenteDrawer`/`useFuenteDrawerStore` para editar); página `DataGestion.tsx`. Se descubrió que en el prototipo `data.html` (no `etl-datos.html`) es el punto de entrada real del nav global — se actualizó la card de `/reportar` para apuntar a `/data` en vez de `/etl/datos`, y se cerraron los gaps de navegación documentados en `etl-datos.html`/`etl-mapeo.html`/`etl-upload.html` (sus "← Volver" ahora apuntan a `/data` en vez del `/reportar` provisional). Verificado con `tsc -b`/`npm run build` y en navegador vía Docker contra datos reales (7 fuentes, 2 proyectos): "Ver fuentes" filtra con scroll automático; se creó y eliminó un proyecto de prueba real vía el drawer (confirmando que `ProyectoViewSet` soporta DELETE aunque el prototipo no lo expone); el modal de confirmación de borrado se probó y canceló sin confirmar (dato real); el drawer de usuario cargó los roles reales del backend. Sin errores de consola. |
| 2026-09-14 | El usuario pide cerrar la restricción de roles que había quedado pendiente en `data.html`, pero explícitamente **no** replicar el hack del prototipo (`role-guard.js`, selector de rol suelto en localStorage) — pide algo "más robusto". Se diseña una sesión simulada atada a un Usuario real de `/api/usuarios/` (roles ya asignados de verdad en la BD, verificado con `curl`) en vez de un rol abstracto. Implementado: `useSesionStore` (zustand + middleware `persist`, primera vez que se usa en el proyecto), `usuarios.service.ts`/`useUsuarios` (`GET /api/usuarios/`, lista completa), `useRolActual` (deriva `{usuario, roles, isAdmin}`), `SesionSelector.tsx` montado en `Navbar.tsx` (dropdown "actuar como" con el rol mostrado debajo del nombre, tal como lo había pedido el usuario originalmente). Se reactivó la restricción en `FuentesTable.tsx`: eliminar una fuente completa requiere `isAdmin` (edición sigue sin excepción de admin, igual que el prototipo). Verificado en navegador vía Docker: sin sesión el botón queda bloqueado; seleccionando "Alejandra Diaz" (admin_datos real) se habilita y muestra sus 4 roles reales; la sesión persiste tras recargar (confirma el middleware `persist`). Sin errores de consola. `tsc -b`/`npm run build` limpios. |
| 2026-09-14 | Se completa la migración de `team.html` → `/team`, cerrando las 7 páginas del plan original. El usuario pide explícitamente que la página solo esté disponible para el rol `admin_datos` (el prototipo no restringía el acceso). Se confirma con el usuario el comportamiento del gate: redirigir en silencio a `/data` (sin mensaje de acceso restringido), usando `<Navigate to="/data" replace />` gateado por `useRolActual().isAdmin` — primer uso de ese hook para restringir una página completa en vez de una sola acción. Al revisar `useUsuarioMutations.ts` para reusarlo se detectó un bug: `useCrearUsuario`/`useActualizarUsuario` solo invalidaban `['responsables']`, nunca `['usuarios']` (la query que usa la nueva tabla y `useRolActual`) — corregido, más las invalidaciones correctas en los 4 hooks nuevos de instituciones/eliminar usuario. Implementado: tipo `InstitucionPayload`; `usuarios.service.ts` extendido con `eliminarUsuario`/`crearInstitucion`/`actualizarInstitucion`/`eliminarInstitucion`; hooks correspondientes; `InstitucionesAdmin.tsx` (form inline + chips, como el prototipo, sin drawer) y `UsuariosTable.tsx` (búsqueda + tabla, reusa `UsuarioDrawer`/`useUsuarioDrawerStore` ya construidos desde `data.html`, `ConfirmModal` para borrar en vez de `confirm()` nativo); página `Team.tsx` con el gate de admin al inicio. Verificado con `tsc -b`/`npm run build` limpios y en navegador vía Docker: sin sesión admin redirige a `/data` tanto al cambiar sesión estando en `/team` como al cargar la URL directamente; con "Alejandra Diaz" (`admin_datos` real) se ve el CRUD completo — se creó/editó/eliminó una institución de prueba (POST/PATCH/DELETE reales) y un usuario de prueba (creado desde el drawer, apareció de inmediato en la tabla confirmando el fix de invalidación de cache, luego eliminado). Sin errores de consola. |
| 2026-09-14 | En paralelo, en otra sesión sobre el repo backend: se implementa login real (`LoginView`/`LogoutView`/`MeView`, `auth_user` en `Usuario`) en el PR #9, se detecta y corrige un hueco de toma de cuenta anónima en `UsuarioViewSet`, y se agrega a la landing del backend (`/`) un mensaje "Colflux · Backend · Version X.x.x" con botón a `FRONTEND_URL`. Sobre ese mismo PR, se retira **todo** `backend/docs/pages/` de una sola vez (commit `cb2942e`) en vez de ir borrando página por página a medida que cada una se migraba en el frontend — esto quedó desalineado con el plan original de este archivo, que asumía retirar el prototipo al final y por partes. El PR #9 se mergeó a `main` y el deploy a producción corrió con éxito. |
| 2026-09-14 | Se completa la migración de `db.html` → `/db`. Al analizar el prototipo se descubrió que no tiene backend real: el ERD/explorador/catálogo leen de `window.CATALOGO`, generado por `app/catalogo/generator.py` pero nunca expuesto vía `/api/...`. Se iteró con el usuario sobre la fuente de datos: se descartó un endpoint nuevo con cache (el usuario no quería llamadas de red para algo que solo cambia en cada deploy), se evaluó y descartó embeber la página del prototipo vía `<iframe>` (propuesta intermedia del propio usuario, revertida con "creo que mejor reconstruirlo"), y se confirmó la opción elegida: empaquetar `catalogo.json` como archivo estático del proyecto frontend, copiado de `backend/docs/assets/data/catalogo.json` (145 KB, 12 grupos, 40 entidades), importado en build-time (requirió `resolveJsonModule: true` en `tsconfig.app.json`). Queda documentado como gap de despliegue no bloqueante: este archivo debe resincronizarse manualmente en cada cambio de esquema — candidato para `automatizar-deploy-ecosistema-colflux.md`, no implementado en esta tarea. Implementado: tipos `EntidadCatalogo`/`GrupoCatalogo`/`CatalogoData`; `utils/catalogoModel.ts` (modelo derivado — mapa de entidades, relaciones FK, color por grupo reusando la paleta `GRUPO_PALETTE` ya usada en `MapeoList.tsx` — computado una sola vez a nivel de módulo, sin hook, por ser datos estáticos); componentes `ErdDiagram.tsx` (nodos expandibles por grupo + conectores SVG bezier medidos por posición DOM vía refs y `useLayoutEffect`, portando el algoritmo del prototipo), `EntityExplorer.tsx` (relaciones salientes/entrantes + tarjeta central), `CatalogoCampos.tsx` (sidebar + tabla de campos con búsqueda/resaltado/choices/semillas); página `DbModelo.tsx` en `/db`. Alcance confirmado con el usuario: "todo junto" (ERD + explorador + catálogo), sin dividir en sub-entregas. Verificado con `tsc -b`/`npm run build` limpios y en navegador vía Docker: 40 entidades/45 relaciones renderizadas correctamente, expansión de nodo + explorador de relaciones sincronizados, "Ver en catálogo →" navega con scroll a la entidad correcta, búsqueda y toggle de choices funcionando contra datos reales. Se corrigió un solape visual menor (nombre de grupo largo pisando el nombre de la entidad en la tarjeta central del explorador) detectado durante la verificación. Sin errores de consola. |
