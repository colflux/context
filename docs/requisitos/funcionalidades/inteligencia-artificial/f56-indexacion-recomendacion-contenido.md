# F56 — Indexación y recomendación automática de contenido

**Categoría:** Inteligencia Artificial

## Objetivo

Que la IA clasifique automáticamente la información y recomiende contenidos según el
interés y la necesidad de cada usuario.

## Contexto

Capacidad transversal de IA sobre el contenido ya publicado en la plataforma.

## Qué hay

Existe indexación semántica real vía RAG:
`ia-functions/app/domain/services/chunking.py` fragmenta texto,
`app/adapters/vectorstore/pgvector_store.py` lo indexa en Postgres+pgvector (tabla
`document_chunks` con columnas `collection`, `embedding`), y
`app/adapters/tools/rag_tool_provider.py` expone búsqueda semántica
(`buscar_documentos`, `buscar_diccionario`) como tools del chatbot. Esto es
clasificación/búsqueda por significado sobre contenido ya indexado (entrevistas,
informes, notas de campo, diccionario de observaciones cualitativas), consultado
reactivamente.

## Qué hace falta

No hay recomendación proactiva ("te puede interesar X") ni perfilado de usuario por
interés/necesidad — lo implementado es búsqueda semántica a demanda, no un motor de
recomendación. Tampoco hay evidencia de clasificación automática de contenido entrante
(tagging/categorización) más allá de la `collection` fija que se asigna manualmente al
ingestar (`documents` vs `dictionary`).
