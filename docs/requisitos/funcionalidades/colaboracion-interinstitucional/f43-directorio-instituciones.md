# F43 — Directorio de instituciones y mapa de investigación

**Categoría:** Colaboración Interinstitucional

## Objetivo

Mostrar qué institución tiene qué datos, y quién investiga dónde.

## Contexto

Va más allá de un catálogo administrativo: busca ser una herramienta de descubrimiento
para otros investigadores.

## Qué hay

CRUD básico de instituciones: modelo `Institucion`
(`backend/app/models/proyecto.py:6-18`, campos `nombre`, `correo`), API REST
(`InstitucionViewSet` en `backend/app/api/institucion/views.py`) y UI de administración
(`frontend/src/components/admin/team/InstitucionesAdmin.tsx`). `Usuario.institucion`
(FK, `backend/app/models/datos.py:47`) vincula cada persona a una institución.

## Qué hace falta

No es un directorio navegable con mapa de investigación — falta geolocalización de
instituciones, vista de "qué institución tiene qué datos" y "quién investiga dónde";
hoy es solo una tabla administrativa de nombre/correo.
