# F55 — Motor de IA para ingesta multi-formato

**Categoría:** Inteligencia Artificial

## Objetivo

Usar OCR, PLN y aprendizaje automático para limpiar, normalizar y validar datos que
llegan en distintos formatos (sensores, PDFs, audios, narrativas comunitarias) antes de
integrarlos a la base central.

## Contexto

Capacidad transversal de IA, distinta del mapeo de columnas asistido ya existente para
datos tabulares.

## Qué hay

Hay un flujo real de mapeo de columnas asistido por IA para Excel/CSV:
`ia-functions/mcp_server/tools/carga_ia.py`
(`proponer_mapeo_columnas`/`confirmar_mapeo_columnas`) consulta el catálogo de campos
del backend y deja que el LLM proponga el mapeo en el chat, con confirmación humana
antes de escribir (vía `agent_orchestrator.py`, `AUTH_REQUIRED_TOOLS`). El modelo
`CargaArchivo`/`MapeoColumna` (`backend/app/models/datos.py:188-383`) soporta este flujo
con `origen_mapeo` (`"manual"` vs `"ia_chat"`) y transformaciones (lookup, regex,
escala, etc.).

## Qué hace falta

Todo lo de OCR (PDFs) y procesamiento de audio/narrativas comunitarias — no se encontró
ninguna referencia a OCR, tesseract, transcripción de audio o Whisper en ningún repo.
Tampoco hay normalización/validación por ML más allá del mapeo de columnas asistido por
LLM; el alcance actual cubre solo datos tabulares estructurados (Excel/CSV), no
sensores en formatos crudos ni narrativas no estructuradas.
