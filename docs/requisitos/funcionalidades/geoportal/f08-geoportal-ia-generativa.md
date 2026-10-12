# F08 — Geoportal integrado con IA generativa

**Categoría:** Geoportal

## Objetivo

Que el usuario pregunte en lenguaje natural sobre lo que ve en el mapa/dashboard y
reciba interpretaciones automatizadas.

## Contexto

Distinto del motor de inferencia estructurado de
[F61](../addendum-prototipo/f61-motor-inferencia-dato-diccionario.md): aquí sí se
interpreta lenguaje natural.

## Qué hay

Hay un chatbot funcional en `ia-functions` (arquitectura hexagonal con RAG +
tool-calling, 4 proveedores LLM) que interpreta datos geoespaciales reales:
`mcp_server/backend_client.py:30-46` (`get_sitios()`, consume `/api/geo/sitios/`),
`mcp_server/tools/sitios.py:4-8` (`listar_sitios()`), `mcp_server/tools/mediciones.py:
10-69` (responde sobre promedio/mín/máx de CO2/CH4/N2O por sitio, vía
`/api/geo/resumen/` y `/api/geo/series/`). En frontend, el `ChatWidget`
(`AppLayout.tsx:26`) llama a `chatService.postChat` (`src/services/chat.service.ts:
32-35`).

## Qué hace falta

El chatbot está montado globalmente, no integrado específicamente al mapa/dashboard (no
responde "sobre lo que el usuario ve" en pantalla, solo sobre sitios/gases vía
tool-calling genérico). No cubre biomasa, carbono-stock, GPP ni cobertura vegetal —
reconocido como fuera de alcance en la propia documentación de `ia-functions`. Además,
`frontend/src/pages/InsightsIA.tsx` ("Insights IA") es texto estático hardcodeado (sin
llamada a servicio) — un mockup, no una interpretación generada dinámicamente del mapa.
