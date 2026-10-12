# F28 — Portal de acceso e investigación avanzada

**Categoría:** Wiki y Conocimiento

## Objetivo

Portal para investigadores con búsqueda avanzada de datos por período/región.

## Contexto

Pensado como una experiencia diferenciada para el perfil investigador, más allá de la
consulta pública general.

## Qué hay

Existe un nivel de acceso `investigador` en el sistema de permisos
(`backend/app/api/permisos.py`, cascada `ciudadano < investigador < reportador <
admin`, y UI de solicitud de nivel en
`frontend/src/components/layout/SolicitarNivelModal.tsx`), pero es solo una etiqueta de
rol para gating de escritura (`EscrituraRequiereNivel`) — la lectura ya es libre para
todos los niveles (`SAFE_METHODS` sin restricción). La API geográfica
(`backend/app/api/geo/views.py`) sí soporta filtros por período (`anio`, `desde`,
`hasta`) y región (`municipio`, `departamento`, `region`, `sitio`), pero es la misma API
pública general, no un portal diferenciado para investigadores.

## Qué hace falta

No existe un portal separado ni una "búsqueda avanzada" exclusiva para investigadores —
el nivel `investigador` no desbloquea hoy ninguna capacidad de búsqueda adicional, solo
permisos de escritura futuros. Falta decidir y construir una experiencia/endpoint
diferenciado (ej. exportación masiva, filtros combinados más ricos, acceso a datos
crudos) que use el nivel `investigador` ya existente como base de control de acceso.
