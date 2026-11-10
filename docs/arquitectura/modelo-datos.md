# Modelo de datos relacional

Esquema relacional completo de la base de datos de COLFLUX: sitios de monitoreo, proyectos,
flujo de cámaras, torres EC, caracterización de suelos y publicaciones científicas.

El esquema se mantiene directamente en dbdiagram.io/dbdocs (no en este repo), para que se
pueda editar sin pasar por un PR cada vez que cambia un campo. La wiki generada por dbdocs
incluye, por tabla, cada campo con su tipo, notas y relaciones — es la referencia a usar para
el detalle fino de campos:

[Ver wiki en dbdocs.io ↗](https://dbdocs.io/lviviana13/colfux-db?view=table_structure){ .md-button .md-button--primary target="_blank" }

[Ver/editar diagrama en dbdiagram.io ↗](https://dbdiagram.io/d/colfux-db-67b2aae2263d6cf9a05d08d0){ .md-button target="_blank" }

## Cómo sincronizarlo con los modelos de Django

El esquema de dbdiagram/dbdocs se mantiene a mano, así que con el tiempo se desincroniza de
los modelos reales. Para traerlo al día: `generate_catalogo` (el mismo management command que
genera `catalogo.json`/`catalogo.js`, ver [backend/app/catalogo/generator.py](https://github.com/colflux/backend/blob/main/app/catalogo/generator.py))
ahora también genera `docs/assets/data/colflux.dbml` — el esquema completo (tablas, campos,
tipos y relaciones) en el lenguaje que entiende dbdiagram.io (DBML), agrupado por los mismos
módulos que usa el catálogo.

Para aplicarlo:

1. Correr `python manage.py generate_catalogo` en el backend (o tomar el archivo generado en el
   último despliegue).
2. Abrir el diagrama en dbdiagram.io → `Import` → `DBML` → pegar el contenido de
   `colflux.dbml` (reemplaza el esquema completo; no hay API de escritura en el plan gratuito,
   así que este paso es manual).
3. Revisar el diff visual en el editor antes de guardar — el generador no sabe de la
   distribución/posición de las tablas en el lienzo, así que dbdiagram las reacomoda.
