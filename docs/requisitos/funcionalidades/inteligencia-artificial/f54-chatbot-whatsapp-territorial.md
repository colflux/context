# F54 — Chatbot de WhatsApp con IA conversacional territorial

**Categoría:** Inteligencia Artificial

## Objetivo

Responder en lenguaje local y derivar métricas ambientales (inundaciones, sequías,
flujos CH4/CO2) directamente de las conversaciones comunitarias — un canal de captura
de datos, no solo de consulta.

## Contexto

El catálogo original dejó pendiente: consentimiento y privacidad al extraer indicadores
de las conversaciones.

## Qué hay

Existe un chatbot conversacional con tool-calling
(`ia-functions/app/domain/services/agent_orchestrator.py`) con RAG sobre
documentos/diccionario de campo (`app/domain/services/rag_service.py`,
`app/adapters/vectorstore/pgvector_store.py`) y tools de consulta de mediciones GEI
(`mcp_server/tools/mediciones.py`, `sitios.py`) vía la API del backend — pero es un
canal de chat genérico (API HTTP/MCP), no hay integración con WhatsApp/Twilio en ningún
repo (`ia-functions`, `backend`, prototipos). El módulo
`mcp_server/tools/mediciones_chat.py` declara explícitamente tools para "escribir
mediciones dictadas por chat" (`proponer_guardar_medicion`, `confirmar_medicion`) pero
ambas retornan `NO_DISPONIBLE` porque "el backend todavía no expone un endpoint de
escritura para esto ni un campo de origen en su modelo de mediciones".

## Qué hace falta

- Todo el canal WhatsApp: no existe ninguna integración de mensajería ni evidencia de
  Twilio/WhatsApp Business API.
- La captura de indicadores ambientales desde conversaciones comunitarias está
  deshabilitada a propósito en el código actual.
- El pendiente de consentimiento/privacidad al extraer indicadores sigue abierto — no
  hay lógica de consentimiento en el orquestador ni en el modelo de conversaciones.
