# Sacar toda la lista de las funcionalidades

**Estado:** blocker — depende de la revisión de viabilidad y la retroalimentación de los compañeros sobre el catálogo consolidado
**Creada:** 2026-09-01

## Objetivo

Tener una lista completa de funcionalidades de la plataforma, cruzando el Anexo 1, el Anexo 2, los talleres de co-diseño y el Marco Teórico, para saber qué tenemos y planear las siguientes iteraciones.

## Contexto

[`docs/requisitos/`](../../../docs/requisitos/index.md) es la carpeta destino final de esta tarea, pero solo se puebla cuando los requerimientos estén confirmados por el equipo — mientras tanto, todo el trabajo en curso vive en `personal/tasks/`.

El 2026-09-06 se borró todo el contenido de `docs/requisitos/` (quedó solo un `index.md` placeholder). El trabajo inicial de esta tarea se basó únicamente en 5 HU (HU-001 a HU-005), pero al revisar el Google Doc ["Funcionalidades" / Marco Teórico](https://docs.google.com/document/d/1s-TqqYvTXFPStkhGUkONsE5cTTvjER6EhpzKCEVS9lI/edit) se detectó que la arquitecta amplió los casos de uso originales con historias HU-06 a HU-30 y un catálogo F1-F11 + ~50 funcionalidades sin numerar. La lista inicial no reflejaba ese catálogo ampliado, así que la validación se repitió de forma más rigurosa, fuente por fuente, comparando cada una contra el Marco Teórico.

Nota sobre nombres de archivo: en `files/`, el archivo llamado "Resultados visita aliados..." es en realidad el que tiene las fotos de las carteleras/talleres, y "Anexo 06" es el reporte de síntesis ya elaborado — están cruzados respecto a como el equipo los nombró originalmente. No se renombraron los archivos, solo se documentó la discrepancia.

## Plan

- [x] ~~Extraer funcionalidades del Anexo 1 (HU-001 a HU-005)~~
- [x] ~~Conseguir el Anexo 1, el Anexo 2, y los 2 PDFs de resultados con aliados~~
- [x] ~~Comparar fuente por fuente contra el Marco Teórico, archivo por archivo (Anexo 1, Anexo 2, PDF de carteleras/talleres, PDF de resultados con aliados)~~
- [x] ~~Consolidar todos los hallazgos en un catálogo único de funcionalidades~~
- [ ] Revisar cada funcionalidad del catálogo consolidado y evaluar si aplica/es viable para COLFLUX, con el detalle de qué implicaría
- [ ] Armar documento final de 3 pestañas:
  - [ ] Pestaña 1 — Marco teórico (el documento fuente, tal cual)
  - [ ] Pestaña 2 — Mapeo punto por punto de Anexo 1 + Anexo 2 + resultados con aliados, para verificar que todo quedó revisado (similar a la pestaña 2 que ya existe en el Google Doc de Drive)
  - [ ] Pestaña 3 — Lista completa de funcionalidades, con el detalle funcionalidad por funcionalidad de qué debería ser/hacer en la plataforma
- [ ] Validar el resultado final con el equipo
- [ ] Publicar el resultado validado en `docs/requisitos/`

## Entregables

- [Catálogo de funcionalidades COLFLUX (borrador)](catalogo-funcionalidades-borrador.md) — consolida todos los hallazgos de las 4 fuentes vs. el Marco Teórico. Estado: borrador, pendiente de revisión de viabilidad y validación con el equipo antes de pasar a `docs/requisitos/`.

## Referencias

- Marco Teórico / catálogo F1-F11: [Google Doc "Funcionalidades"](https://docs.google.com/document/d/1s-TqqYvTXFPStkhGUkONsE5cTTvjER6EhpzKCEVS9lI/edit)
- Metodología de referencia para pasar de requerimientos vagos a especificaciones técnicas: [Transformar requerimientos vagos en especificaciones técnica.docx](https://livejaverianaedu-my.sharepoint.com/:w:/r/personal/marian_cabrerap_javeriana_edu_co/_layouts/15/Doc.aspx?sourcedoc=%7BC3868E1F-0705-4D8C-87FD-3E664DA103E3%7D&file=Transformar%20requerimientos%20vagos%20en%20especificaciones%20t%C3%A9cnica.docx&action=default&mobileredirect=true) (SharePoint Javeriana, requiere login institucional)
- Fuentes originales (en [`files/`](../../../files/)):
  - Anexo 1: `files/Anexo 1 HISTORIA DE USUARIOS EN INGENIERIA DE REQUERIMIENTOS.pdf`
  - Anexo 2: `files/Anexo 2. Documento Tecnico_V7_10marzo2025.docx`
  - PDF de carteleras/talleres (fotos de las carteleras hechas a mano en La Chorrera y UDENAR/Nariño, más matriz de importancia): `files/Resultados visita aliados - Expectativas contenido plataforma.pdf`
  - PDF de presentación de resultados con aliados (reporte de síntesis: perfiles, expectativas de contenido, tipos de usuario): `files/Anexo 06 - Resultados preliminares .pdf`

## Historial

| Fecha | Descripción |
|---|---|
| 2026-09-01 | Se crea la tarea. Extracción inicial de funcionalidades del Anexo 1 (HU-001 a HU-005), cruce con Anexo 2 y borrador de priorización. |
| 2026-09-06 | Se detecta que el Marco Teórico tiene un catálogo mucho más amplio (HU-06 a HU-30, F1-F11 + ~50 funcionalidades). Se borra `docs/requisitos/` y se reinicia la validación de forma más rigurosa. Se comparan Anexo 1, Anexo 2, PDF de carteleras y PDF de resultados con aliados contra el Marco Teórico, uno por uno, validando con Viviana en cada paso. Se detecta y corrige el cruce de nombres entre los dos PDFs de aliados. |
| 2026-09-07 | Se consolidan todos los hallazgos (incluyendo notas de co-creación adicionales) en un catálogo único: [catalogo-funcionalidades-borrador.md](catalogo-funcionalidades-borrador.md). Se reestructura este archivo de tarea con plantilla estándar (Objetivo / Contexto / Plan / Entregables / Referencias / Historial). |
| 2026-09-07 | Se marca la tarea como **blocker**: el siguiente paso (revisar viabilidad del catálogo) depende de la retroalimentación de los compañeros y de la revisión que se haga con ellos. |
| 2026-09-20 | Se revisa `PrototipoCOLFLUX/` (código, no solo documentos) contra el catálogo F01-F58 ya publicado en `Funcionalidades.pdf` v1.0.0. Se encuentran 4 funcionalidades ya prototipadas sin F asignada: diccionario de campo inverso (olor/color/textura → variable técnica), semáforo de aceptación comunitaria de términos, motor de inferencia dato↔diccionario en tiempo real, y análisis estadístico exploratorio en Python. Documentadas como F59-F62 en [docs/roadmap/funcionalidades-addendum.md](../../../docs/roadmap/funcionalidades-addendum.md) (addendum, no se edita el PDF original) y referenciadas desde el roadmap 3-6 meses. Pendiente: la misma revisión de viabilidad que el resto del catálogo. |
