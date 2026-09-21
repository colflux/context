# Tour de onboarding: asistente que explica los botones al entrar

**Estado:** hecha
**Creada:** 2026-09-21
**A cargo:** Viviana
**Sesión de Claude Code:** https://claude.ai/code/session_01XMt1YwkN27metgCqy6RoFY

## Objetivo

Agregar un tour guiado (tipo "asistente") que aparezca la primera vez que un usuario entra a una página del frontend, explicando qué hace cada botón/sección clave. Busca reducir la curva de aprendizaje para usuarios nuevos (investigadores, personal de la Javeriana) que no conocen la plataforma.

## Contexto

Surge de una conversación exploratoria: la idea es replicar el patrón común de "product tour" (tooltips secuenciales sobre elementos de la UI), similar a lo que se ve en otras plataformas al entrar por primera vez.

No hay ninguna decisión de arquitectura ni mención previa en `docs/roadmap/` ni en otras tareas — es una idea nueva, sin validar con el equipo todavía.

### Revisión de alcance (2026-09-21)

Se revisó `../frontend/src` para definir alcance de implementación:

- **Stack:** React 19 + Vite + react-router-dom 7 + zustand. Ya existe el patrón de persistencia en `store/useThemeStore.ts` (lee/escribe `localStorage`) — mismo patrón sirve para "¿ya vio el tour?", sin tocar backend.
- **Páginas existentes (15):** `Home`, `MapaInteractivo`, `DashboardIndicadores`, `DataGestion`, `EtlDatos` + flujo (`EtlUpload`, `EtlMapeo`, `EtlReglasCampo`, `EtlReglaDetalle`, `EtlReglaValidacion`, `EtlProximamente`), `DbModelo`, `InsightsIA` (deshabilitada), `GuiaReporte`, `ReportarFormulario`, `Participacion`, `Team`, `Educacion`.
- **Ya existe `components/chat/`** (`ChatWidget`, `ChatBubble`, etc.) — es el chatbot de IA (`ia-functions/`), no un tour. El tour debe ser visualmente distinto (tooltips/spotlight) para no confundirse con el chat ya presente.
- **No hay código ni librería de onboarding/tour hoy.**

**Alcance acotado decidido:**

1. No cubrir las 15 páginas de una vez. Empezar por 2-3 páginas de mayor fricción para un usuario nuevo: `Home`, `MapaInteractivo`, `EtlDatos` (el flujo ETL es el más complejo).
2. Librería: `driver.js` (sin dependencia de React, ligero, overlay/spotlight) sobre `react-joyride` (más pesado, menos mantenimiento activo).
3. Persistencia: localStorage por página (`tour_seen_home`, `tour_seen_mapa`, etc.), siguiendo el patrón de `useThemeStore`. No requiere cambios en backend ni en el modelo de usuario.
4. Trigger: botón "?" o "Ver tour" visible permanentemente, además del auto-inicio en primera visita.

## Plan

- [x] Validar prioridad frente al roadmap — no hay nada en `docs/roadmap/roadmap-3-6-12-meses.md`, se decide avanzar como iniciativa nueva y acotada.
- [x] Definir alcance: por página, empezando por `Home`, `MapaInteractivo`, `EtlDatos`.
- [x] Evaluar librería: se elige `driver.js`.
- [x] Definir persistencia: localStorage por página, patrón de `useThemeStore`.
- [x] Diseñar el copy de cada paso (qué explica cada botón) para las 3 páginas piloto.
- [x] Instalar `driver.js` e implementar en `frontend/` (piloto: `Home`, `MapaInteractivo`, `EtlDatos`).
- [x] Agregar botón "Ver tour" para relanzar manualmente.
- [x] Probar en navegador (primera visita vs. visitas siguientes, claro/oscuro).
- [x] Evaluar extender a las páginas restantes — se extendió a las 12 páginas restantes (ver abajo).

### Implementación (2026-09-21)

- `npm install driver.js` en `../frontend`.
- Nuevo hook `src/hooks/useOnboardingTour.ts`: envuelve `driver()`, marca `localStorage['tour_seen_<tourId>']` al cerrarse el tour (`onDestroyed`), y filtra automáticamente los pasos cuyo selector `element` no existe en el DOM (soporta el caso condicional de "Limpiar filtros").
- Nuevo componente `src/components/common/TourButton.tsx`: botón flotante "?" para relanzar el tour manualmente. Se posicionó en `bottom-24 right-5` — **importante**: el `ChatWidget` ya existente ocupa `bottom-5 right-5`, así que el `TourButton` debe ir siempre por encima de esa posición para no solaparse.
- Se agregaron atributos `data-tour="..."` como anchors en los elementos reales: `Home.tsx` (4), `MapaInteractivo.tsx` (2 con anchor + 1 paso sin anchor para el panel de detalle, que no existe hasta seleccionar un sitio), `DatosTabs.tsx` / `DatosToolbar.tsx` / `DatosTable.tsx` / `Paginacion.tsx` (6, con "Limpiar filtros" condicional).
- En `EtlDatos.tsx` el auto-inicio del tour se gatea explícitamente a `!faltaOrigen && !isError && !isLoading && columnas.length` — de lo contrario el tour arrancaría antes de que la tabla exista.
- Estilos de `driver.js` adaptados a modo oscuro en `src/index.css` (`.dark .driver-popover*`), reusando las variables CSS existentes (`--color-panel`, `--color-fg`, etc.).
- Verificado en navegador (Chrome, vía `npm run dev`): tour automático en primera visita en las 3 páginas, no se repite tras recargar (persistencia en localStorage confirmada), botón "?" relanza el tour manualmente, y en `EtlDatos` sin proyecto/fuente el tour se acota correctamente a los pasos cuyos elementos sí existen (3 de 6). `npx tsc -b` sin errores.

### Extensión a las 12 páginas restantes (2026-09-21)

Se extendió el mismo patrón (`useOnboardingTour` + `TourButton` + atributos `data-tour`) a las 12 páginas que quedaban fuera del piloto — el placeholder `EtlProximamente` (rutas `/etl/*` aún no migradas del prototipo) se dejó fuera a propósito, no tiene UI real que explicar:

- **`DashboardIndicadores`** (`/dashboard`, tour `dashboard`, 4 pasos): indicadores generales, distribución de sitios, sección General, Flujos de GEI.
- **`DataGestion`** (`/data`, tour `data-gestion`, 4 pasos): estado de la API, resumen de fuentes, tabla de proyectos, tabla de fuentes.
- **`DbModelo`** (`/db`, tour `db-modelo`, 3 pasos): diagrama ERD, explorador de relaciones, catálogo de campos.
- **`Educacion`** (`/educacion`, tour `educacion`, 2 pasos): pestañas y contenido.
- **`EtlUpload`** (`/etl/upload`, tour `etl-upload`, 5 pasos): selector de fuente y botón "Analizar" (paso 1); navegación de secciones, lista de mapeo y botón "Validar y guardar" (paso 2) — los pasos de cada estado se filtran automáticamente porque el elemento del otro estado no existe en el DOM.
- **`EtlMapeo`** (`/etl/mapeo`, tour `etl-mapeo`, 2 pasos): acciones (descargar JSON / ver datos) y tabla de mapeo.
- **`EtlReglasCampo`** (`/etl/reglas/campo`, tour `etl-reglas-campo`, 1 paso): grid de tarjetas de reglas.
- **`EtlReglaDetalle`** (`/etl/reglas/detalle`, tour `etl-regla-detalle`, 4 pasos): parámetros de cálculo, ejemplo por caso, aplicar, historial.
- **`EtlReglaValidacion`** (`/etl/reglas/validacion`, tour `etl-regla-validacion`, 2 pasos): resumen por condición de luz, histograma de distribución.
- **`Participacion`** (`/reportar`, tour `participacion`, 1 paso): grid de canales de reporte.
- **`ReportarFormulario`** (`/reportar/formulario`, tour `reportar-formulario`, 2 pasos): campos del formulario, botón enviar.
- **`Team`** (`/team`, tour `team`, 3 pasos): solicitudes de nivel, instituciones, usuarios registrados.

En páginas cuyo componente reutilizable no acepta `className`/props arbitrarios (p. ej. `Card`), el anchor `data-tour` se puso en un `<div>` envolvente en vez de tocar el componente compartido. En `EtlReglaDetalle` y `EtlReglaValidacion`, el hook `useOnboardingTour` se declara antes de los `return` tempranos (falta `?codigo=`, cargando) para respetar las reglas de hooks de React.

Verificado: `npx tsc -b` sin errores (exit 0). Probado en navegador (Chrome vía `npm run dev`) en `/dashboard` (auto-inicio, avance de pasos, sin solape con `ChatWidget`), `/team` (relanzado manual, filtra "Sin solicitudes" correctamente) y `/reportar/formulario` en modo oscuro (popover y botones con buen contraste).

**Tarea cerrada** con las 15 páginas del frontend cubiertas (excepto `EtlProximamente`, que es un placeholder temporal sin UI real).

### Copy de los pasos (2026-09-21)

Redactado contra los componentes reales (`pages/Home.tsx`, `pages/MapaInteractivo.tsx`, `pages/EtlDatos.tsx` + `components/etl-datos/DatosToolbar.tsx`). Pendiente de validar tono/wording con el equipo antes de implementar.

**`Home`**
1. Botón "Explora los datos" (`Link` a `/mapas`) → *"Aquí entras al mapa interactivo con todos los sitios monitoreados."*
2. Botón "Reportar información" → *"Si tienes una observación de campo, repórtala aquí (te pedirá iniciar sesión)."*
3. Tarjetas de estadísticas (sitios / datos / usuarios) → *"Estos números se actualizan con la información real de la plataforma."*
4. Sección "Explora COLFLUX" (las 3 tarjetas: Monitoreo / Comunidades / Datos) → *"Tres rutas rápidas para entender cómo funciona COLFLUX."*

**`MapaInteractivo`**
1. Panel "Filtros" (`FilterPanel`, izquierda) → *"Filtra los sitios por ecosistema, región o variable antes de explorarlos en el mapa."*
2. El mapa (`GeoMap`) → *"Haz clic en un punto para ver el detalle de ese sitio de monitoreo."*
3. Panel inferior de detalle (`SiteDetailPanel`, aparece al seleccionar un sitio) → *"Aquí ves las mediciones y tendencias del sitio seleccionado."*

**`EtlDatos`**
1. Pestañas de gas (`DatosTabs`) → *"Cambia entre CO₂ y CH₄ para ver los datos de cada gas."*
2. Botón "✕ Limpiar filtros" (solo visible si hay filtros activos) → *"Quita los filtros aplicados en la tabla."*
3. `CargarDropdown` (selector de proyecto/fuente) → *"Elige de qué proyecto o fuente quieres ver los datos cargados."*
4. Botón "⬇ Descargar Excel" → *"Descarga la tabla actual (con los filtros aplicados) en Excel."*
5. Tabla de datos con filtros por columna (`DatosTable`) → *"Puedes filtrar directamente por columna, haciendo clic en el encabezado."*
6. Paginación (`Paginacion`) → *"Navega entre páginas si hay más de 200 registros."*

Nota de implementación: en `EtlDatos`, el botón "Limpiar filtros" solo se renderiza si `hayFiltrosExtra` es true — el paso del tour debe saltarse o quedar condicionado a que el elemento exista en el DOM (driver.js soporta pasos opcionales/`onHighlightStarted` para verificar existencia).

## Entregables

Tour de onboarding funcional en `../frontend/` para las 15 páginas del frontend (todas menos `EtlProximamente`): hook `src/hooks/useOnboardingTour.ts`, componente `src/components/common/TourButton.tsx`, atributos `data-tour` en los componentes involucrados. Commits: `fe8c664` (piloto: `Home`, `MapaInteractivo`, `EtlDatos`) y el commit de esta sesión (extensión a las 12 páginas restantes).

## Referencias

(Ninguna aún.)

## Historial

| Fecha | Descripción |
|---|---|
| 2026-09-21 | Se crea la tarea a partir de una idea exploratoria: agregar un asistente/tour que explique los botones al entrar a la página. Sin implementación aún — queda en backlog pendiente de validar prioridad y alcance. |
| 2026-09-21 | Se revisa el alcance de implementación contra el estado real de `../frontend/`. Se decide arrancar acotado: 3 páginas piloto (`Home`, `MapaInteractivo`, `EtlDatos`), librería `driver.js`, persistencia en localStorage siguiendo el patrón de `useThemeStore`. Se mueve la tarea a `inprogress/`. |
| 2026-09-21 | Se redacta el copy de los pasos del tour para las 3 páginas piloto, contra los componentes reales (`Home.tsx`, `MapaInteractivo.tsx`, `EtlDatos.tsx`, `DatosToolbar.tsx`). Se detecta caso especial: en `EtlDatos` el botón "Limpiar filtros" solo existe si hay filtros activos, el paso debe manejarlo condicionalmente. Pendiente: implementar con `driver.js`. |
| 2026-09-21 | Se implementa el piloto en `../frontend/`: hook `useOnboardingTour`, componente `TourButton`, atributos `data-tour` en `Home`, `MapaInteractivo`, `EtlDatos` y sus subcomponentes. Se detecta y corrige solape entre `TourButton` y el `ChatWidget` existente (ambos flotantes en la esquina inferior derecha). Verificado en navegador: auto-inicio en primera visita, persistencia tras recarga, relanzado manual, y manejo correcto de pasos condicionales en `EtlDatos`. `tsc -b` sin errores. Queda pendiente decidir si se extiende a las demás páginas o se cierra el piloto como entrega. |
| 2026-09-21 | Se commitea el piloto (`fe8c664`) tras corregir un commit inicial que incluyó de forma no intencional 4 archivos ajenos (trabajo en curso de otra sesión en la misma rama) — corregido con `git reset --soft` + `git restore --staged` selectivo, sin pérdida de datos. Se decide extender el tour a las 12 páginas restantes del frontend: `DashboardIndicadores`, `DataGestion`, `DbModelo`, `Educacion`, `EtlUpload`, `EtlMapeo`, `EtlReglasCampo`, `EtlReglaDetalle`, `EtlReglaValidacion`, `Participacion`, `ReportarFormulario`, `Team` (se deja fuera `EtlProximamente` por ser un placeholder temporal). Se implementa el mismo patrón en las 12 páginas, se verifica `tsc -b` sin errores y se prueba en navegador (`/dashboard`, `/team`, `/reportar/formulario` en modo oscuro). Tarea cerrada — se mueve a `done/`. |
