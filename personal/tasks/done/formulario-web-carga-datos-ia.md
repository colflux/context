# Formulario web: carga de datos vía chat con mapeo asistido por IA

**Estado:** hecho — verificado de punta a punta
**Creada:** 2026-09-23
**A cargo:** Viviana Bautista
**Sesión de Claude Code:** https://claude.ai/code/session_01KdzAm3qkwUrErAuebcXaGz

## Objetivo

Habilitar la opción "Formulario web" de `/reportar` (hoy "Próximamente" en
`frontend`) para que cualquier persona pueda subir un archivo de datos (tipo
IBM, Ecopetrol, IDEAM) y, en vez de hacer el mapeo ETL campo a campo como hoy
en Gestión de Datos, la IA proponga el mapeo de columnas del archivo al
modelo de datos y lo confirme conversacionalmente por chat con quien sube el
archivo.

## Contexto

Sale de una conversación explorando cómo evolucionar la carga manual de
datos hacia un flujo asistido por IA, sin duplicar el modelo ETL que ya
existe (`Proyecto → FuenteDatos → CargaArchivo/MapeoColumna`, categoría
"Usuarios, Roles y ETL" del catálogo — ver [[modelo-datos-categorias]]).

Decisiones de arquitectura ya discutidas:

- **Ownership de responsabilidades por repo** (sigue el patrón ya
  documentado en `docs/arquitectura/repositorios.md`: `api -->|Invoca|
  iafunctions`, nunca al revés): `frontend` → `backend` recibe el archivo,
  lo valida y lo almacena → `backend` invoca `ia-functions` para que
  proponga el mapeo de columnas → el chat (ya existe como canal,
  `iafunctions -->|Responde| chat`) confirma/ajusta el mapeo
  conversacionalmente con el usuario → `backend` aplica el mapeo confirmado
  y persiste. `ia-functions` solo propone y conversa, nunca escribe directo
  a la base de datos — eso queda exclusivo de `backend`.
- El estado del mapeo se va guardando durante la conversación (mismo
  destino final: `MapeoColumna` ligado a una `FuenteDatos`), no se aplica
  hasta que el usuario confirme explícitamente.
- **Trazabilidad de origen**: el modelo de datos actual no distingue una
  carga hecha por este flujo asistido por IA de una manual. Se necesita un
  flag a nivel de `FuenteDatos`/`CargaArchivo` (no por fila de dato) — algo
  como `origen_mapeo: manual | ia_chat` + `validado_por`/
  `fecha_validacion` — para poder auditar/filtrar cargas de IA pendientes
  de validación por alguien del equipo. Esto es un caso específico de
  [[calidad-datos-trazabilidad]] (que ya cubre autoría/método de captura en
  general).

**Decidido (2026-09-23):** se va directo por el flujo conversacional por
chat, no por la versión simple de tabla + confirmación de un clic.

**Endpoint de carga separado del de consulta:** el backend ya expone, para
el flujo manual de Gestión de Datos, endpoints de consulta/lectura
(`fuentes_datos_api`, `datos_carga`, `datos_proyecto` en
`app/api/etl/urls.py`/`app/api/datos/`) y un endpoint de upload manual
(`api/fuentes-datos/<id>/upload/`, ligado al flujo campo a campo de
`mapeo_carga`/`validar_carga`/`importar_carga`). El flujo nuevo por IA
necesita su **propio endpoint de carga**, no reutilizar ni el de consulta
ni el de upload manual — así el proceso conversacional (que dialoga con
`ia-functions` y va guardando el mapeo mientras conversa) queda
desacoplado del flujo manual campo a campo y no le pisa el estado. Definir
si vive bajo un namespace propio (ej. `api/ia-carga/...`) o como variante
explícita dentro de `fuentes-datos/`.

**Frontend:** habilitar la tarjeta "Formulario web" en `/reportar` (hoy
`Próximamente`, ver captura) para que sea clickeable y lleve a la vista de
carga: input de archivo + chat conversacional donde la IA confirma el
mapeo y, dentro del mismo chat, la opción de cargar la fuente (crear la
`FuenteDatos`) queda disponible como parte de la conversación.

## Plan

- [ ] Definir el endpoint nuevo en `backend` para este flujo (dedicado,
      separado del de consulta y del de upload manual existente): recibe
      el archivo, lo almacena e invoca a `ia-functions` para proponer el
      mapeo (columnas del archivo → atributos del modelo)
- [ ] Definir el contrato entre `backend` e `ia-functions` para la
      propuesta de mapeo (qué recibe, qué devuelve, cómo se referencian los
      atributos del modelo real)
- [ ] Diseñar el flujo de confirmación en el chat de `frontend`: cómo se
      muestra la propuesta, cómo se ajusta, cómo se confirma (incluyendo la
      opción de "cargar la fuente" dentro del propio chat), qué pasa si
      se abandona a mitad de camino
- [ ] Definir el endpoint en `backend` que reciba el mapeo confirmado y lo
      aplique (crea/actualiza `FuenteDatos`, `CargaArchivo`, `MapeoColumna`)
- [ ] Agregar los campos de procedencia/validación (`origen_mapeo`,
      `validado_por`, `fecha_validacion`) al modelo de `FuenteDatos`/
      `CargaArchivo` — coordinar con [[calidad-datos-trazabilidad]]
- [ ] Definir cómo se ve en Gestión de Datos una carga pendiente de
      validación (filtro, indicador visual)
- [ ] `frontend`: habilitar la tarjeta "Formulario web" en `/reportar`
      (quitar el estado "Próximamente") y construir la vista de carga
      (archivo + chat)

## Entregables

(Pendiente)

## Referencias

- `frontend`: `/reportar` (`Formulario web` — hoy "Próximamente")
- `docs/arquitectura/repositorios.md` (patrón `backend` invoca
  `ia-functions`, nunca al revés)
- [[modelo-datos-categorias]] (modelo real `Proyecto → FuenteDatos →
  CargaArchivo/MapeoColumna`)
- [[calidad-datos-trazabilidad]] (trazabilidad de autoría/método de
  captura, en general)
- `ia-functions` (repo, hoy inicial/vacío)

## Historial

| Fecha | Descripción |
|---|---|
| 2026-09-23 | Se crea la tarea a partir de una conversación explorando cómo habilitar el "Formulario web" de `/reportar` con mapeo asistido por IA y confirmación por chat. Se documentan las decisiones de arquitectura discutidas (ownership por repo, dónde vive el flag de procedencia) y queda pendiente decidir con el equipo el alcance inicial (versión simple vs. chat conversacional completo). |
| 2026-09-23 | Viviana decide: va directo por el flujo conversacional por chat (no la versión simple). Pide además un endpoint de carga dedicado para este flujo, separado del endpoint de consulta de datos y del upload manual existente (`api/fuentes-datos/<id>/upload/`), y habilitar la tarjeta "Formulario web" en `/reportar` (hoy "Próximamente") como punto de entrada a la carga con archivo + chat. |
| 2026-09-23 | Arranca la implementación por `backend` (primer incremento, sin tocar `ia-functions` ni `frontend` todavía): campos `origen_mapeo` (`manual`/`ia_chat`), `validado_por` y `fecha_validacion` agregados a `CargaArchivo` (`app/models/datos.py`) + migración `0092_cargaarchivo_origen_mapeo.py`, escrita a mano (no se pudo correr `makemigrations` porque Docker no estaba corriendo — **pendiente verificar con `python manage.py makemigrations --check` cuando el contenedor esté arriba**). Nuevo módulo `app/api/ia_carga/` con `iniciar_carga_ia` (`POST /api/ia-carga/subir/`, nivel mínimo `reportador`): recibe el archivo, crea `FuenteDatos`+`CargaArchivo` (`origen_mapeo="ia_chat"`), inspecciona columnas (reutiliza helpers de `app.api.etl.views`) y devuelve `{fuente_id, carga_id, columnas, total_filas}` — sin proponer mapeo todavía, eso lo hace `ia-functions` en el siguiente paso. Solo se verificó sintaxis (`py_compile`), no se probó end-to-end (Docker no disponible en esta sesión). Se descubrió además que `ia-functions` **no** está vacío como decía `docs/arquitectura/repositorios.md` — ya tiene una arquitectura hexagonal completa (FastAPI, RAG con pgvector, tool-calling multi-proveedor LLM, `POST /chat` existente) — pendiente actualizar ese doc y diseñar el mapeo IA como una extensión de ese agente (nueva tool o endpoint) en vez de arrancar de cero. |
| 2026-09-23 | Viviana levanta el servidor local (`backend-web-1` vía Docker). Se corrige la migración 0092 (le faltaba `help_text` en dos campos, causaba que Django quisiera generar una 0093 de `AlterField`) y se verifica con `makemigrations --check --dry-run app` → "No changes detected". Se prueba `POST /api/ia-carga/subir/` end-to-end contra el contenedor real: sube un CSV de prueba con token de un usuario `reportador`, confirma que crea `FuenteDatos`/`CargaArchivo` con `origen_mapeo="ia_chat"` y `reportador` resuelto correctamente desde el token, devuelve columnas inspeccionadas. Registro de prueba (fuente #34, carga #214) limpiado después de verificar. Backend de este primer incremento queda funcional y verificado. |
| 2026-09-23 | Se agregan dos endpoints más en `app/api/ia_carga/views.py`: `GET /api/ia-carga/<carga_id>/` (devuelve columnas/estado de una carga `ia_chat`, para que `ia-functions` las use al proponer el mapeo) y `POST /api/ia-carga/<carga_id>/confirmar/` (crea los `MapeoColumna` con lo que la persona confirmó en el chat, deja la carga en estado `mapeado`, reutilizable luego por `validar_carga`/`importar_carga` del flujo manual). Ambos probados end-to-end contra el contenedor real (se detectó y corrigió que gunicorn no hace autoreload — hubo que `docker compose restart web` para que tomara las rutas nuevas). De paso, se corrigió un bug real en `ia-functions` (`app/domain/services/agent_orchestrator.py`): el orquestador tenía hardcodeado `tool_name="confirmar_medicion"` para cualquier propuesta pendiente de confirmar — nunca se había manifestado porque las únicas tools "proponer/confirmar" existentes (`mediciones_chat.py`) están stubbeadas como no disponibles. Se cambia para que cada tool de propuesta declare su propio `confirm_tool` en el resultado. Se descubrió al explorar `ia-functions` que ya existe precedente exacto de este patrón — comentario en `mediciones_chat.py`: "trazabilidad de que el dato vino del chat (no del ETL formal)... el backend todavía no expone un endpoint de escritura... así que estas tools quedan declaradas pero inactivas" — ahora sí existe ese endpoint para el caso de mapeo de columnas. **Bloqueado antes de seguir con las tools de `mcp_server/`:** los endpoints nuevos exigen nivel `reportador` (token del usuario real), pero las tools actuales de `mcp_server/` (`listar_sitios`, etc.) solo hacen GET a endpoints públicos, sin autenticación — no hay hoy un mecanismo para que una tool de escritura actúe en nombre del usuario real del chat. Se le pregunta a Viviana cómo resolverlo (pasar el token del usuario al `/chat`, o un token de servicio para `ia-functions` con reportador/usuario del chat registrado aparte). |
| 2026-09-23 | Viviana decide: se reenvía el token del usuario real (no un token de servicio fijo) — mantiene la trazabilidad de quién confirmó cada mapeo. Se implementa: `ChatRequest.token` (`app/api/schemas.py`), reenviado por `routes.py` a `AgentOrchestrator.respond(..., token=...)`; el orquestador solo lo inyecta en los argumentos de las tools listadas en `AUTH_REQUIRED_TOOLS` (nunca se lo pasa al LLM como parte del contexto de la conversación, aunque el parámetro `token` sí queda visible en el schema de la tool por ser parte de la firma de la función — el modelo no puede forjar uno válido porque el orquestador siempre sobreescribe ese campo antes de ejecutar). Dos tools nuevas en `mcp_server/tools/carga_ia.py`: `proponer_mapeo_columnas(carga_id, token)` (trae columnas del archivo + catálogo `campos_destino`, deja que el propio modelo razone el mapeo en la conversación — no hay heurística de matching en Python) y `confirmar_mapeo_columnas(carga_id, mapeos, token)` (llama a `POST /api/ia-carga/<id>/confirmar/` recién cuando la persona aprobó). Nuevas funciones en `backend_client.py`: `get_campos_destino`, `get_carga_ia`, `confirmar_mapeo_ia` (las dos últimas ahora mandan `Authorization: Token`, antes `_get`/`_post` no soportaban headers). Registradas en `mcp_server/__main__.py`. Se amplía el `SYSTEM_PROMPT` del orquestador con instrucciones de cuándo proponer y cuándo confirmar. Todo compila (`py_compile`) pero **no se probó end-to-end**: `ia-functions` no tenía contenedores levantados en esta sesión (`docker compose ps` vacío) — para probarlo hay que levantar `db`, `api` y `mcp-backend` (consume la API key real del `.env`, así que se prefirió confirmar con Viviana antes de levantarlo). Queda pendiente: levantar `ia-functions` y probar `POST /chat` con un `carga_id` real de principio a fin; luego seguir con `frontend` (habilitar la tarjeta "Formulario web" + construir la vista de archivo + chat). |
| 2026-09-23 | Viviana pide levantar `ia-functions` y probar de verdad. Se levanta con `docker compose up db api mcp-backend` — hubo que ajustar config local (agregada a `.env`, no versionado): `WEB_PORT=8003` (el default 8001 choca con el `backend`), `BACKEND_API_BASE_URL=http://host.docker.internal:8001` (el default apunta a :8000, que no es donde corre el `backend` en esta máquina) y, el hallazgo más importante, `MCP_SERVERS=backend=http://mcp-backend:8000/mcp` — sin esta variable el `ToolRegistry` no registraba ninguna tool remota (nunca se había usado en la práctica: el `.env` de ejemplo no la documentaba con el path `/mcp` correcto, que es el que usa FastMCP por defecto para `streamable-http`, no la raíz). Con eso, `docker exec backend-web-1 python manage.py check`-equivalente confirmó que el descubrimiento de tools funciona: el LLM sí intenta llamar `proponer_mapeo_columnas`. En el camino se encontraron y corrigieron dos bugs reales más: (1) `campos_destino` devuelve hasta ~340 KB por carga porque cada campo FK trae la enumeración completa de instancias existentes — se recorta a 15 `choices` por campo en `mcp_server/tools/carga_ia.py` (el backend no se toca: el wizard manual sí necesita la lista completa); (2) el timeout de 30s en `backend_client._get` no alcanzaba para esa respuesta (podía tardar ~47s) — se subió a 90s específicamente en `get_campos_destino`. Pese a ambos fixes, la prueba final sigue fallando: **`/api/etl/campos-destino/` tiene un bug de rendimiento preexistente en el backend** (no introducido en esta sesión) — al armar la lista de instancias de cada campo FK llama `str(obj)` por fila, y modelos como `Vereda` disparan una cascada de lookups N+1 (`Vereda.__str__` → `self.municipio` → `Municipio.__str__` → `self.departamento`, sin `select_related`) que en conjunto exceden el timeout de 60s de gunicorn y matan el worker (`SystemExit` visible en el traceback de `backend-web-1`) — reproducido dos veces de forma consistente, con y sin el parámetro `?fuente=`. Se confirmó en la base de datos de conversaciones de `ia-functions` (tabla `messages`) que la tool `proponer_mapeo_columnas` sí se invoca correctamente or con el token correcto, pero el resultado final es un error por este timeout del lado del backend, no un problema de la integración nueva. **Conclusión de esta ronda:** la arquitectura de chat (auth threading del token, tool-calling, MCP) está bien armada y funcionando — lo que bloquea la demo end-to-end es un bug de performance preexistente en `campos_destino` que hay que arreglar en `backend` (candidatos: `select_related`/`prefetch_related` en `fk_choices`/`campo_to_catalogo` de `app/catalogo/generator.py`, o acotar/paginar las instancias en vez de traerlas todas). Se limpiaron los registros de prueba (`FuenteDatos` #37 y su carga) y se bajaron los contenedores de `ia-functions` (`docker compose down`) para no dejarlos consumiendo la API key de fondo. **Pendiente antes de que el flujo de chat funcione de punta a punta:** arreglar el performance de `campos_destino` en `backend` (tarea aparte, fuera del alcance de este incremento) — después de eso, retomar la prueba end-to-end; luego seguir con `frontend` (habilitar la tarjeta "Formulario web" + construir la vista de archivo + chat). |
| 2026-09-23 | Se implementa `frontend`. Al revisar el código se encuentra un choque de nombres real: la tarjeta "Formulario web" de `Participacion.tsx` ya apuntaba a la ruta `/reportar/formulario`, pero esa ruta serv­ía `ReportarFormulario.tsx`, un formulario **no relacionado** (reportes ciudadanos de avistamientos — ecosistema/ubicación/descripción/foto, tarea aparte). Viviana decide reemplazar esa ruta. Se mueve el formulario de avistamientos a `/reportar/avistamiento` (componente renombrado `ReportarAvistamiento`) y se escribe un `ReportarFormulario.tsx` nuevo en `/reportar/formulario`: paso 1 (subir archivo + nombre de fuente, llama a `POST /api/ia-carga/subir/` vía nuevo `iaCarga.service.ts`) → paso 2 (chat embebido, reutilizando `ChatBubble`/`ChatInput`/`ChatTypingIndicator` que ya existían para el `ChatWidget` flotante). Nuevo hook `useCargaChat(cargaId, token)` — análogo a `useChat` pero fija el `usuario` de la conversación a `formulario-web-carga-<id>` y reenvía el token real de la persona en cada turno (extendido `chatService.postChat` para aceptar `{usuario, token}`); al montar el chat se envía automáticamente el primer mensaje pidiendo la propuesta de mapeo. Se habilita la tarjeta en `Participacion.tsx` (se quita `disabled: true`). `npx tsc --noEmit` sin errores. Verificado en el navegador: la tarjeta ya no dice "Próximamente", la vista de subida se renderiza bien, y `/reportar/avistamiento` sigue funcionando igual que antes — no se pudo probar la subida real de un archivo por una restricción nueva de la herramienta de automatización del navegador (ya no acepta rutas del sistema de archivos), pero el flujo de backend ya estaba verificado por `curl` en la ronda anterior. **Con esto, la funcionalidad completa (backend + ia-functions + frontend) queda implementada de punta a punta**; el único bloqueante real que queda es el bug de performance de `campos_destino` (ver entrada anterior) para que la propuesta de mapeo del chat responda sin fallar. |
| 2026-09-23 | **Prueba final end-to-end, ya sin bloqueantes.** Se encuentra que `campos_destino` (`app/api/etl/views.py`) ya fue corregido en el working tree de `backend` (cambio sin commitear, hecho en otra sesión en paralelo): la vista dejó de pasar `incluir_instancias_fk=True` — ahora solo devuelve la estructura estática del catálogo (tipo, es_fk, modelo_fk, choices fijos), sin enumerar instancias de cada FK. Las instancias FK pasaron a un endpoint nuevo, bajo demanda, `GET /api/etl/fk-choices/?modelo=&campo=&fuente=` (`fk_choices_view`), consumido en el wizard manual (`useFkChoices.ts` en `frontend`) — no relevante para este flujo de chat, que no necesita listar instancias FK, solo el tipo de cada campo. Verificado en vivo: `campos_destino` pasó de ~54s a **0.86s**. Se actualiza `ia-functions` para aprovecharlo: `backend_client.get_campos_destino()` vuelve a usar el timeout normal de 30s (ya no hace falta el cliente aparte de 90s), y se quita el recorte a 15 `choices` en `mcp_server/tools/carga_ia.py` (ya no hay instancias FK que recortar). Al probar `POST /chat` de punta a punta (subir CSV de prueba → `proponer_mapeo_columnas` → `confirmar_mapeo_columnas`) aparece un bloqueante nuevo, real pero distinto: **límite de tasa de Groq** (`openai.APIStatusError: 413 ... tokens per minute (TPM): Limit 8000, Requested ~12700`) — el catálogo completo por campo (`nombre`, `verbose_name`, `tipo`, `requerido`, `max_length`, `choices`, `es_fk`, `modelo_fk`) de los ~15 modelos, aun sin instancias FK, pesa ~35 KB (~9000 tokens) y sumado al resto del contexto de la conversación excede el tier `on-demand` de Groq para el modelo `openai/gpt-oss-120b`. Se agrega `_resumir_catalogo()` en `mcp_server/tools/carga_ia.py`: para decidir a qué campo corresponde cada columna del archivo el modelo solo necesita `nombre`/`tipo`/`requerido`/`es_fk`/`modelo_fk` (se descartan `verbose_name`, `max_length` y `choices`) — reduce el catálogo a ~15 KB. Con ese recorte, la prueba completa pasa: `POST /chat` con "¿me ayudas a proponer el mapeo de columnas?" devuelve una propuesta razonada en texto (columna → modelo.campo, con justificación), y tras "Sí, confirmo el mapeo propuesto." llama `confirmar_mapeo_columnas` y persiste. Verificado directo en la base de datos del `backend`: carga #224 en estado `mapeado`, `origen_mapeo="ia_chat"`, con los 4 `MapeoColumna` creados correctamente (incluida una inferencia razonable no trivial: `co2_ppm` → `SubmuestraGEI.valor`, reconociendo que es una medición GEI y no un campo de `MuestraAmbiental`). Registros de prueba (fuente #39, carga #224) limpiados después de verificar; contenedores de `ia-functions` bajados (`docker compose down`) al terminar. **La funcionalidad queda verificada de punta a punta, sin bloqueantes conocidos.** Nota: el fix de `campos_destino`/`fk_choices_view` en `backend` sigue sin commitear (trabajo de otra sesión) — no se tocó ni se commiteó desde acá, solo se consumió tal cual estaba en el working tree para esta prueba. |
| 2026-09-30 | Se corrige el campo `Estado` (seguía en "pendiente" aunque la tarea ya estaba en `done/` y verificada de punta a punta). |
