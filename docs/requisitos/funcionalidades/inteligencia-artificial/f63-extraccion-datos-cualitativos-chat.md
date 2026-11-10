# F63 — Extracción de datos cualitativos desde chat a registro estructurado

**Categoría:** Inteligencia Artificial

!!! info "Caso de uso nuevo — diseñado en sesión, pendiente de validar con el equipo"
    No proviene del catálogo original (`Funcionalidades.pdf`) ni fue encontrado en el
    prototipo (a diferencia de F59-F62). Se numera F63 para poder referenciarlo desde
    tareas sin ambigüedad. La plantilla SMART para especificar requerimientos nuevos
    vive en [Requerimientos](../../requerimientos/buenos-requerimientos.md).

## Objetivo

Que una observación cualitativa narrada en lenguaje natural durante una conversación de
chat (ej. "el agua está turbia y huele a huevo podrido cerca del canal") se convierta en
un registro estructurado y trazable en la base de datos, con confirmación humana antes
de guardar — distinto de dictar un número de una medición (eso ya está declarado,
aunque inactivo, en F54/`mediciones_chat.py`).

## Contexto

Dos piezas ya existentes apuntan en esta dirección pero no están conectadas entre sí:

- F59 (diccionario de campo con interpretación técnica inversa) ya traduce una
  percepción sensorial en texto libre ("olor a huevo podrido") a una variable técnica y
  una regla cuantitativa — pero es un diccionario estático (CSV servido vía `/api/wiki`
  en el prototipo), no algo que se dispare desde una conversación ni que termine en un
  registro de base de datos.
- El patrón "proponer → confirmar" para escrituras asistidas por IA ya existe y
  funciona en `ia-functions/mcp_server/tools/carga_ia.py` (mapeo de columnas), y está
  declarado pero inactivo para mediciones en `mediciones_chat.py`.

Este caso de uso es la pieza que falta entre ambas: usar la lógica de F59 dentro del
chat de F54 para clasificar y extraer una observación cualitativa, y escribirla con el
mismo patrón de confirmación que ya probó `carga_ia.py`.

**Actores:** comunidad/persona en campo que reporta la observación por chat (WhatsApp o
canal de chat ya existente); comité científico (F14), como validador posterior del
registro propuesto por IA.

## Qué hay

- `ia-functions/app/domain/services/agent_orchestrator.py` — orquestador de chat con
  tool-calling y `AUTH_REQUIRED_TOOLS`, que ya distingue tools que requieren
  confirmación antes de escribir.
- `ia-functions/mcp_server/tools/carga_ia.py` — ejemplo real y funcional del patrón
  `proponer_*`/`confirmar_*` con persistencia (mapeo de columnas, no observaciones).
- `ia-functions/mcp_server/tools/mediciones_chat.py` — mismo patrón declarado para
  mediciones dictadas por chat, pero devuelve `NO_DISPONIBLE`: "el backend todavía no
  expone un endpoint de escritura para esto ni un campo de origen en su modelo de
  mediciones". Es para valores **cuantitativos** (variable + valor + unidad), no texto
  cualitativo.
- Diccionario de campo inverso (F59): en el prototipo, CSV de 7 columnas
  (categoría, término, definición, variable asociada, variable secundaria, regla
  cuantitativa, interpretación) — la lógica de mapeo texto→variable existe, pero vive
  fuera del backend actual y no está expuesta como tool del chatbot
  (`app/adapters/tools/rag_tool_provider.py` solo expone búsqueda semántica sobre
  documentos/diccionario indexado, no esta tabla de reglas).
- `app/domain/services/rag_service.py` / `pgvector_store.py` — búsqueda semántica ya
  indexada, reutilizable para encontrar si el texto libre del usuario coincide con un
  término conocido del diccionario antes de proponer una interpretación.
- Revisado `backend/app/models/` completo (`datos.py`, `sitio.py`, `mom.py`, `co2.py`,
  `biomasa.py`, `suelo.py`, `cobertura.py`) — no existe ningún modelo para observaciones
  cualitativas de texto libre. Todos los modelos de medición son campos científicos
  estrictamente cuantitativos (decimales, por ecosistema).

## Casos de uso

1. Usuario comunitario describe una observación sensorial en el chat → el sistema la
   clasifica, extrae campos estructurados y la propone para confirmación antes de
   guardarla.
2. Usuario confirma la observación propuesta → el sistema la persiste con origen
   `"ia_chat"` y estado `"pendiente_validacion"`.
3. Comité científico revisa observaciones pendientes → puede aprobarlas, rechazarlas o
   pedir aclaración (reutilizando el semáforo de calidad de F11/F60).
4. El sistema cruza la observación contra el diccionario de campo inverso (F59) →
   sugiere una interpretación técnica (variable + regla), marcada explícitamente como
   sugerencia de IA, no como medición real.

## Criterios de aceptación

1. Dado un mensaje de chat con una observación sensorial, cuando el usuario lo envía,
   entonces el sistema propone un registro estructurado (categoría, texto original,
   sitio si se puede inferir, fecha) sin guardarlo todavía.
2. Dado un registro propuesto, cuando el usuario confirma explícitamente, entonces el
   sistema lo persiste con origen=`"ia_chat"` y estado=`"pendiente_validacion"`.
3. Dado un registro propuesto, cuando el usuario no confirma (lo ignora o lo rechaza),
   entonces el sistema no escribe nada en la base de datos.
4. Dado un texto que coincide con un término conocido del diccionario de campo inverso,
   cuando se extrae la observación, entonces se adjunta la interpretación técnica
   sugerida, marcada como "sugerencia de IA" y no como medición validada.
5. Dado un registro en estado `"pendiente_validacion"`, cuando un miembro del comité
   científico lo revisa, entonces puede cambiarlo a `"validado"` o `"rechazado"`,
   quedando trazable quién y cuándo lo hizo.

## Qué hace falta

- **Modelo de datos nuevo** en el backend: algo como `ObservacionCualitativa` con texto
  original, categoría (olor/color/textura/fauna/clima percibido/otro), sitio (FK
  opcional — en chat comunitario la ubicación puede ser imprecisa o inferirse de la
  conversación), fecha, canal/origen (`"ia_chat"` vs `"manual"`, mismo patrón que
  `origen_mapeo` en `MapeoColumna`), interpretación técnica sugerida (trazable a F59,
  marcada explícitamente como sugerencia de IA y no como medición), y estado de
  validación (reutilizando el semáforo de F11/F60 en vez de inventar uno nuevo).
- **Endpoint de escritura** en el backend para ese modelo — hoy no existe ninguno,
  igual que para el caso cuantitativo de F54.
- **Tool de extracción** en `ia-functions` que: (a) detecte si un mensaje del chat es
  una observación de campo y no solo conversación general, (b) extraiga los campos
  estructurados, (c) opcionalmente consulte el diccionario F59 para sugerir una
  interpretación técnica, y (d) proponga el registro para confirmación — siguiendo el
  patrón ya probado de `carga_ia.py`, no el stub inactivo de `mediciones_chat.py` (que
  es para otro tipo de dato).
- **Conectar F59 al chat**: hoy el diccionario inverso no es una tool del orquestador;
  haría falta exponerlo (vía `tool_registry.py`) para que el chat lo consulte en vivo.
- **Consentimiento y privacidad** al extraer cualquier indicador de una conversación —
  mismo pendiente ya señalado en F54, sigue sin resolverse en el orquestador ni en el
  modelo de conversaciones.
- **Decisión pendiente de validar con el equipo**: ¿toda observación cualitativa debe
  matchear un término conocido del diccionario F59 para aceptarse, o se permite
  registrar texto libre sin interpretación técnica (quedando solo como dato cualitativo
  crudo, pendiente de que alguien del comité científico lo interprete después)?
- **Otras preguntas abiertas**: ¿quién puede confirmar el registro — la misma persona
  que lo narra en el chat, o se requiere un segundo actor (moderador) antes de que
  llegue al comité científico? ¿se generaliza esto a un modelo de "formulario
  cualitativo" común (mismo pendiente abierto en F10), o se crea un modelo específico
  solo para esta observación?
