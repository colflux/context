# F26 — Espacio para publicar papers/estudios

**Categoría:** Wiki y Conocimiento

## Objetivo

Repositorio de estudios de investigadores externos, navegable y consultable.

## Contexto

Relacionado con [F16](../carbono-y-estimaciones/f16-publicacion-modelos-predictivos.md)
(publicación de modelos predictivos), pero aquí el foco es el documento/estudio en sí,
no el modelo ejecutable.

## Qué hay

Existe un modelo real en el backend, `Publicacion` (`backend/app/models/publicacion.py`),
con campos bibliográficos completos (DOI, ISBN, journal, abstract, keywords, autores
M2M vía `PublicacionAutor`, sitios asociados vía `PublicacionSitio`) y un modelo
relacionado `ResultadoPublicacion` para variables de resultados (COS, biomasa, flujos).
Sin embargo, es metadato interno del ETL — el propio código lo documenta como excluido
de catálogos públicos (`backend/app/api/etl/views.py:44`: "Excluye 'Publicaciones': es
metadato bibliográfico del proyecto, no..."). No se encontró ViewSet/endpoint API ni
página de frontend que exponga esto como repositorio navegable; en frontend,
`Educacion.tsx` solo tiene dos tarjetas hardcodeadas bajo la pestaña "Publicaciones"
sin datos reales ni carga dinámica.

## Qué hace falta

- Exponer `Publicacion` vía API pública (hoy solo vive en el modelo de datos del ETL,
  no en una vista REST).
- Construir el frontend real de repositorio (listado, filtros, descarga/enlace) — lo
  que hay en `Educacion.tsx` es solo maquetación visual sin funcionalidad de subida ni
  listado dinámico de papers externos.
