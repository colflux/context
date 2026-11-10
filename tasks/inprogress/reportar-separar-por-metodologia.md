# Rediseñar "Reportar": una card por metodología en vez de tres cards genéricas

**Estado:** pendiente
**Creada:** 2026-11-01
**A cargo:** Viviana
**Sesión de Claude Code:** <https://claude.ai/code/session_xxxxx>

## Objetivo

Cambiar la vista `Reportar` del frontend (hoy tres cards: "Gestión de Datos", "Formulario
web", "Plantilla de datos") para que, en cambio, muestre **una card por metodología**:
**Biomasa**, **COS** (carbono orgánico del suelo), **MOM** (materia orgánica muerta /
necromasa) y **Flujos** — 4 metodologías de primer nivel, no 3: aunque
`docs/conocimiento/como-se-mide-el-carbono.md` menciona MOM dentro de la sección de
Biomasa, en la literatura de contabilidad de carbono (reservorios IPCC) y en el catálogo
real del backend (`app/catalogo/generator.py`) MOM es un reservorio/grupo separado de la
biomasa viva, así que tiene su propia card. **Flujos** es la metodología con más de una
técnica de medición (cámaras de gases manuales y torres de covarianza de remolinos), así
que su card despliega la opción de cuál de las dos cargar: **equipo** (cámaras,
`MuestraGEI`/`SubmuestraGEI`) o **torres** (eddy covariance,
`MuestraTorre`/`SubmuestraEddy`/`SubmuestraReddy`). Importante: torres no es una
metodología aparte, es una técnica dentro de Flujos — no debería tener su propia card de
primer nivel.

## Contexto

Surge mientras se diseñaba la carga de datos de torres EC (ver
[[cargar-datos-torre-guatavita-eddypro]]) y conecta directo con la tarea ya existente
[[subida-descarga-formato-metadato-dato-por-metodologia]], que viene separando metadato/dato
por metodología del lado del archivo de carga/descarga. Esta tarea es la contraparte de
**interfaz**: una vez que cada metodología tiene su propio formato, tiene sentido que la
vista de entrada también se organice por metodología en vez de por mecanismo genérico
(Gestión de Datos / Formulario web / Plantilla).

Mockup de referencia (adjuntado en la sesión que originó esta tarea): la vista actual de
`Reportar` en `frontend/src/pages/Participacion.tsx` (o el componente que la reemplace),
con 3 cards horizontales. La propuesta es reemplazarlas por cards de metodología, y que la
de CO2/CH4 abra la elección equipo vs. torres.

Pendiente de resolver antes de implementar:

- Confirmar con el equipo que el mapeo de 4 cards (Biomasa, COS, MOM, Flujos) es correcto
  y que no faltan más técnicas dentro de cada una (ej. ¿hay más de una forma de medir COS?).
- Qué pasa con los 3 mecanismos actuales (Gestión de Datos, Formulario web, Plantilla) —
  ¿se mantienen como sub-opciones dentro de cada card de metodología, o se reemplazan?
- Depende de que la carga de datos de torre EC tenga su modelo de datos definido primero
  (ver [[cargar-datos-torre-guatavita-eddypro]], en curso — ahí se está decidiendo si se
  guarda solo el promedio diario o también el detalle semihorario).

## Plan

- [x] Confirmar con el equipo la lista completa de metodologías y cómo se agrupan en cards — 4 cards: Flujos (con sub-opción equipo vs. torre), COS, Biomasa, MOM.
- [x] Definir qué pasa con los mecanismos actuales (Gestión de Datos / Formulario web /
      Plantilla) dentro del nuevo esquema por metodología — se reemplazan por solo 2:
      "Subir datos" (modal) y "Plantilla" (activa solo en Flujos por ahora).
- [x] Diseñar el flujo de Flujos (card con sub-opción equipo vs. torres) a nivel de UI
- [x] Implementar en `frontend/src/pages/Participacion.tsx`
- [x] Simplificar el modal "Subir datos" (`FuenteDrawer.tsx`): quitar Nombre/Tipo/Estado/
      Responsable manuales, inferir nombre y tipo del archivo/enlace, asignar responsable
      automáticamente al usuario autenticado (backend).
- [x] Agregar selector de Entidad en el modal "Subir datos", predeterminado a la institución
      del usuario autenticado pero editable (nuevo campo `FuenteDatos.institucion`).
- [x] Reordenar el modal (Entidad antes que Proyecto), filtrar Proyecto por la entidad
      elegida y agregar botones "+" para crear entidad/proyecto sin salir del modal.
- [x] Agregar selector de Metodología en el modal "Subir datos" (nuevo campo
      `FuenteDatos.metodologia`), predeterminado a la card desde la que se abrió pero
      editable; el modal sigue siendo compartido con Gestión de Datos, donde no hay
      card de origen y el campo queda vacío por defecto.
- [ ] Conectar cada card con el backend correspondiente filtrado por metodología (hoy "Subir
      datos" y la plantilla son los mismos endpoints genéricos para todas las cards — depende
      de que `importar_carga`/`plantilla_vacia` distingan metodología, y de que la carga de
      torres esté resuelta — ver [[cargar-datos-torre-guatavita-eddypro]])

## Entregables

- `frontend/src/pages/Participacion.tsx` — vista `Reportar` rediseñada: una card por
  metodología (Flujos, COS, Biomasa, MOM), cada una expandible con solo 2 opciones:
  **Subir datos** (abre el modal `FuenteDrawer`) y **Descargar plantilla** (activa solo
  en Flujos; inactiva — "Próximamente" — en COS/Biomasa/MOM hasta que tengan su propia
  plantilla). La card de Flujos además tiene un selector de técnica (Equipo / Torre EC),
  con Torre EC deshabilitada hasta que se cierre su modelo de datos agregados.
- `frontend/src/components/admin/fuentes/FuenteDrawer.tsx` — modal "Nueva/Editar fuente
  de datos" simplificado (decisión de equipo, 2026-11-02, ver captura adjunta en la
  sesión): ya no pide Nombre, Tipo, Estado ni Responsable a mano.
  - **Nombre**: se infiere del archivo subido (`archivo.name`) o del último segmento de
    la URL/ruta.
  - **Tipo**: se infiere de la extensión (`xlsx`/`xls`→excel, `csv`→csv, `shp`→shapefile,
    `geojson`/`json`→geojson; si no hay extensión reconocida y es una URL http(s)→`api`;
    si no, `otro`).
  - **Estado**: ya no se elige — el backend lo deja en su default (`pendiente`); el ETL
    lo actualiza solo a `completo` al terminar de importar (`backend/app/api/etl/views.py:2915`),
    así que nunca fue algo que el usuario debiera elegir a mano.
  - **Responsable**: se quita del formulario — `FuenteDatosViewSet.perform_create`
    (`backend/app/api/datos/views.py`) ahora asigna `reportador` automáticamente al
    usuario autenticado (`request.user.usuario`), sin depender de lo que mande el
    frontend. Probado end-to-end con `curl` + token real: el campo `responsable_id`
    queda poblado con el usuario del token, sin que el payload lo incluya.
  - **Entidad**: se agrega como único campo que sí se elige a mano (select con las
    instituciones del catálogo, `GET /api/instituciones/`), predeterminado a la
    institución del usuario autenticado (`useAuthStore().usuario.institucion`) pero
    editable antes de guardar. Requirió agregar el campo `institucion` (FK a
    `Institucion`, nullable) a `FuenteDatos` (`backend/app/models/datos.py`,
    migración `0099_fuentedatos_institucion`), exponerlo en `FuenteDatosSerializer`
    (`institucion` read + `institucion_id` write) y que `perform_create` lo
    defaultee a `usuario.institucion` solo si el payload no lo trae. Probado con
    `curl` + token real: sin `institucion_id` en el payload queda la del usuario;
    con `institucion_id` explícito respeta lo elegido.
  - **Metodología**: nuevo campo `FuenteDatos.metodologia` (choices: `flujos`/`cos`/
    `biomasa`/`mom`, blank permitido), migración `0100_fuentedatos_metodologia`.
    Expuesto en el serializer como `metodologia` (escritura) y `metodologia_label`
    (lectura). `Participacion.tsx` pasa la metodología de la card (vía
    `metodologiaContext` en `useFuenteDrawerStore`) para preseleccionarlo al abrir
    "Subir datos" desde una card — queda editable. Es la base para el filtrado real
    por metodología que sigue pendiente (ver limitación abajo).
  **Limitación conocida:** "Subir datos" y "Plantilla" siguen siendo los mismos
  endpoints genéricos sin importar qué metodología se eligió — el campo
  `FuenteDatos.metodologia` ya queda guardado, pero el backend (`importar_carga`/
  `plantilla_vacia`) todavía no lo usa para enrutar o validar el archivo. Filtrar de
  verdad por metodología queda pendiente, ligado a
  [[subida-descarga-formato-metadato-dato-por-metodologia]]. Tampoco se puede, desde
  este modal, renombrar una fuente ya creada (el campo Nombre se quitó también del modo
  edición) — si hace falta volver a permitirlo, es una iteración futura.

## Referencias

- [[subida-descarga-formato-metadato-dato-por-metodologia]] — separación metadato/dato por
  metodología del lado de archivo/backend, contraparte de esta tarea.
- [[cargar-datos-torre-guatavita-eddypro]] — carga de datos de torre EC, de donde salió esta
  idea; define el modelo de datos que esta card va a necesitar.
- `frontend/src/pages/Participacion.tsx` — vista `Reportar` actual.

## Historial

| Fecha | Descripción |
|---|---|
| 2026-11-01 | Se crea la tarea a partir de una idea surgida mientras se diseñaba la carga de datos de torre EC: reemplazar las 3 cards genéricas de `Reportar` por una card por metodología, con CO2/CH4 abriendo la opción equipo vs. torres. Queda pendiente confirmar el mapeo completo de metodologías y qué pasa con los mecanismos de carga actuales. |
| 2026-11-01 | Se precisa el mapeo contra `docs/conocimiento/como-se-mide-el-carbono.md`: las metodologías de primer nivel son Biomasa, COS y Flujos (no "CO2/CH4" suelto); torres y cámaras son dos técnicas dentro de Flujos, no metodologías aparte. La card de Flujos es la que despliega equipo vs. torres. |
| 2026-11-01 | Se implementa el rediseño en `frontend/src/pages/Participacion.tsx`: 4 cards expandibles (Flujos, COS, Biomasa, MOM), cada una con sus 3 mecanismos (Gestión de Datos, Formulario web, Plantilla) como sub-opciones. Flujos agrega selector de técnica Equipo/Torre EC, con Torre EC deshabilitada hasta cerrar su modelo de datos. `tsc --noEmit` limpio. No se pudo probar en navegador con sesión real (la vista exige rol "reportador" autenticado); queda pendiente verificación visual manual. Queda pendiente conectar cada mecanismo al backend filtrado por metodología — hoy todas las cards usan los mismos endpoints genéricos. |
| 2026-11-02 | Decisión de equipo: el mecanismo "Plantilla de datos" por ahora solo se ofrece para Flujos (y dentro de Flujos, solo CO2) — se agrega `tienePlantilla` a `Metodologia` en `Participacion.tsx` y el botón ya no aparece en las cards COS/Biomasa/MOM. Ver detalle del acotamiento en [[subida-descarga-formato-metadato-dato-por-metodologia]]. |
| 2026-11-02 | Se reducen las 3 opciones de cada card a 2: "Subir datos" (abre el modal `FuenteDrawer`, reemplaza los links a "Gestión de Datos" y "Formulario web") y "Descargar plantilla" (activa solo en Flujos; en COS/Biomasa/MOM queda visible pero inactiva — "Próximamente" — hasta que cada una tenga su propia plantilla, en vez de ocultarse). Aplica a las 4 cards por igual. Se simplifica además `FuenteDrawer.tsx` (compartido con Gestión de Datos): se quitan los campos Nombre/Tipo/Estado/Responsable del formulario — nombre y tipo se infieren del archivo/enlace, estado queda en su default y el backend (`FuenteDatosViewSet.perform_create`) asigna el responsable automáticamente al usuario autenticado. Probado con `curl` contra la API real (token de usuario admin): el `responsable_id` queda poblado sin que el payload lo mande. `manage.py check` y `tsc --noEmit` sin errores. |
| 2026-11-02 | Se agrega selector de Entidad al modal `FuenteDrawer` (a partir de una captura anotada a mano del modal), predeterminado a la institución del usuario autenticado pero editable. Requirió sumar el campo `FuenteDatos.institucion` (FK a `Institucion`) con migración propia `0099_fuentedatos_institucion` — se generó manualmente para no arrastrar los modelos de torre EC (`MuestraTorre`/`SubmuestraEddy`/`SubmuestraReddy`) que ya están en el código pero cuya migración pertenece a [[cargar-datos-torre-guatavita-eddypro]] y sigue pendiente. Serializer expone `institucion` (lectura) e `institucion_id` (escritura); `perform_create` defaultea a `usuario.institucion` solo si el payload no manda `institucion_id`. Probado con `curl` + token real en ambos casos (sin campo → default; con campo → respeta lo elegido). `manage.py check` y `tsc --noEmit` sin errores. |
| 2026-11-02 | Segundo ajuste del modal (nueva captura anotada): Entidad pasa a mostrarse antes que Proyecto, y al elegir Entidad el desplegable de Proyecto se filtra a solo los proyectos asociados a esa entidad (`Proyecto.instituciones`, vía `useProyectos()` en vez del endpoint de dropdown genérico que no traía esa relación). Se agregan botones "+" junto a cada select: el de Proyecto reutiliza el `ProyectoDrawer`/`useProyectoDrawerStore` ya existente (se monta también en `Participacion.tsx`); el de Entidad abre un mini-formulario inline (nombre + `useCrearInstitucion`) que, al guardar, selecciona automáticamente la entidad recién creada. Si el proyecto ya elegido deja de pertenecer a la entidad seleccionada, se limpia la selección. `tsc --noEmit` sin errores. |
| 2026-11-02 | Tercer ajuste del modal: se agrega selector de Metodología (primero en el formulario), con las mismas 4 opciones que las cards de `Reportar` (Flujos/COS/Biomasa/MOM). Requirió sumar `FuenteDatos.metodologia` (choices, blank permitido) con migración `0100_fuentedatos_metodologia`, expuesto en el serializer como `metodologia`/`metodologia_label`. `useFuenteDrawerStore` gana `metodologiaContext` para que `Participacion.tsx` preseleccione la metodología de la card desde la que se abrió el modal (en Gestión de Datos, que no tiene card de origen, queda vacío por defecto); sigue siendo editable en ambos casos. Probado con `curl` + token real: el campo se guarda y se refleja en la respuesta (`metodologia_label`). `manage.py check` y `tsc --noEmit` sin errores. |
