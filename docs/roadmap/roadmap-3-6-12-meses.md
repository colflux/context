# Roadmap de ejecución — Plataforma Colflux

**Creado:** 2026-09-20
**Fuente:** `files/plataforma/Funcionalidades.pdf` (v1.0.0, Sep 7 2026) — 9 casos de uso, ~40 historias de usuario, 58 funcionalidades (F01-F58) en 12 categorías, cruzado con el estado real de `personal/tasks/` (done/inprogress/blocked/backlog) al 2026-09-20. Complementado con [funcionalidades-addendum.md](funcionalidades-addendum.md) (F59-F62), encontradas en `PrototipoCOLFLUX/` pero sin mapear en el PDF original.

## Criterio de priorización

**Completar primero el MVP ya iniciado.** No se abren módulos nuevos (colaboración interinstitucional, sensores IoT, chatbot) mientras haya trabajo a medias en producción o bloqueado por una decisión pendiente. La lógica de las tres ventanas:

- **0-3 meses:** cerrar todo lo que ya está iniciado (inprogress/blocked) + huecos de seguridad críticos.
- **3-6 meses:** completar los módulos base que hoy tienen 0 avance pero son prerequisito de otros (calidad de datos, wiki/conocimiento, formularios pendientes).
- **6-12 meses:** abrir los módulos nuevos de mayor tamaño (sensores/IoT, colaboración interinstitucional, IA conversacional) sobre una base ya estable.

## Estado actual (qué ya existe)

Confirmado en `backend/app/api/` (módulos `geo`, `dashboard`, `reportes`, `etl`, `catalogo`, `usuario`, `institucion`, `proyecto`, `reportador`) y en tareas `done/`:

- Mapa interactivo de ecosistemas (geoportal base) — [[home-mapa-interactivo-ecosistemas-home]]
- ETL de carga y descarga de datos (Excel con formatos por categoría) — [[etl-datos-a-frontend]], [[modelo-datos-categorias]]
- Módulo de gráficas/reportes (biomasa, COS, MOM, flujos, tendencias) — implementado y en producción, ver [[reportes-modulo-graficas]]
- Roles de usuario y credenciales admin — [[users-rol-reportar]], [[users-admin-credenciales]]
- Conexión a base de datos productiva (RDS) — [[db-aws]]
- Automatización de deploy — [[deploy-automatizar-ecosistema-colflux]]
- IA/Insights — implementado pero **deshabilitado temporalmente** (commit `7acfa13`, 2026-09-20)
- Rendimiento de queries geoespaciales — [[rendimiento]]

## 0-3 meses (a Dic 2026) — Cerrar lo iniciado

| Ítem | F relacionadas | Tarea | Bloqueo/acción |
|---|---|---|---|
| Validar 3 puntos pendientes del módulo de gráficas con el ecólogo | F06, F29-F34 | [[reportes-modulo-graficas]] | Ya implementado y desplegado; solo falta validación de criterio (cobertura por sitio, carbono por taxón, unidades de flujos) |
| Cerrar recuperación de contraseña self-service | — (soporte a F57) | [[users-recuperar-pss]] | Faltan: variables `EMAIL_*` en `docker-compose.yml`, credencial Gmail, pantallas frontend, prueba end-to-end |
| Endurecer seguridad de la API (`permission_classes` reales) | F57, F58 | [[seguridad-api-backend]] | Crítico: API mutando datos sin autenticación real |
| Quitar Basic Auth de nginx en rutas de escritura | F57 | [[users-quitar-basic-auth-nginx-escritura-api]] | UX de admin, desbloquea uso normal de `/team` |
| Cerrar archivo de datos validado (swap) para prototipo | soporte a F09/F11 | [[datos-swap]] | Insumo para el manual de usuario |
| Redactar manual de usuario (flujo de reporte de datos) | F24 (parcial), F27 | [[wiki-manual-usuario]] | Sin iniciar; depende de [[datos-swap]] |
| Conectar formulario "Reportar" a endpoint real | soporte a F09 | [[reportes-conectar-formulario-reportar-backend]] | Hoy solo guarda estado en memoria |
| Subir a `reportador` los usuarios reales identificados | F57 | [[subir-nivel-usuarios-reportador]] | En progreso |
| Decidir reactivación de Insights (IA) o mantenerlo apagado | F08, F56 | — | Se deshabilitó el 2026-09-20; definir causa antes de reabrir |
| Dar de baja infraestructura huérfana (Render, etc.) | NFR (sostenibilidad) | [[nube-eliminar-infra-otras-nubes]] | Costo/riesgo de seguridad de recursos sin usar |
| Consolidar el catálogo de funcionalidades como fuente única | — | [[arquitectura-lista-funcionalidades]] | Ya resuelto por este mismo PDF; cerrar la tarea formalmente |

**No entra en este trimestre:** nada de colaboración interinstitucional, sensores IoT, ni chatbot — son módulos nuevos, no trabajo a medias.

## 3-6 meses (Ene-Mar 2027) — Completar módulos base sin iniciar

| Ítem | F relacionadas | Justificación |
|---|---|---|
| Módulo de calidad: categorización de confiabilidad | F11 | [[calidad-datos-categorizacion]] — prerequisito para que el semáforo de calidad (F11) tenga criterio real, no solo estado binario |
| Evaluar portar del prototipo: diccionario de campo inverso, semáforo de aceptación comunitaria y motor de inferencia dato↔diccionario | F59, F60, F61 (ver [addendum](funcionalidades-addendum.md)) | [[prototipo-evaluar-portar-diccionario-campo]] — ya existen como prueba de concepto en `PrototipoCOLFLUX/`; falta decidir viabilidad y si migran al backend real |
| Trazabilidad: quién sube el dato y cómo se capturó | F11, F27 | [[calidad-datos-trazabilidad]] |
| Revisar modelos de datos de cobertura vegetal | soporte a F11 | [[datos-modelos-cobertura]] |
| Terminar de migrar datos IDEAM al servidor | soporte a F41 (a futuro) | [[subir-datos-ideam-servidor]] — bloqueado por versión de backend remoto; desbloquear primero el deploy |
| Wiki de conocimiento sobre carbono + glosario no técnico | F24 | Público general; no depende de nada más iniciado |
| Guardar/centralizar links de noticias relevantes | soporte a F24/F26 | [[wiki-guardar-links-noticias-colflux]] |
| Formulario "Capacidad de Adaptación al Cambio Climático" | F10 | Definir tipo de dato por campo (escala del índice, moneda) antes de construir |
| Captura de coordenadas GPS en formularios de campo | F07 | Habilita que [[reportes-conectar-formulario-reportar-backend]] y F09 georreferencien automáticamente |
| Restricción de edición + comentarios comunitarios | F12 | Sobre el modelo de datos ya existente, sin depender de otros módulos nuevos |
| Exportación de metadatos metodológicos | F17 | Extiende la descarga ya construida en [[modelo-datos-categorias]] |
| Revisar y cerrar feedback de datos de IDEAM ya cargados | soporte a F11 | [[revisar-datos-ideam]] |
| Dar seguimiento al formulario de sugerencias/issues | NFR (UX feedback) | [[revisar-formulario-sugerencias-issues]] |
| Reactivar Insights de forma estable (si se decidió mantenerlo) | F08, F56 | Ya con causa raíz resuelta desde el trimestre anterior |

## 6-12 meses (Abr-Sep 2027) — Módulos nuevos

Se abren solo si el trimestre anterior cerró limpio (sin bloqueos heredados):

- **Alertas y notificaciones** (F39, F40): umbral + WhatsApp — depende de tener datos de calidad ya categorizados (3-6 meses).
- **Monitoreo de red y sensores** (F36-F38): dashboard de estado + ingesta IoT en tiempo real — es infraestructura nueva, requiere decisión de hardware/proveedor (LoRa/Wi-Fi/4G) antes de estimar.
- **Colaboración interinstitucional** (F41-F46): integración con IDEAM/Ecopetrol, portal consolidado, mensajería entre investigadores — depende de que la sincronización de datos externos (IDEAM) ya esté resuelta, no solo migrada una vez.
- **Inteligencia artificial ampliada** (F54-F56): chatbot de WhatsApp conversacional, motor de ingesta multi-formato (OCR/PLN), recomendación de contenido — construir sobre la base ya estabilizada de Insights.
- **Builder de dashboards personalizados y directorio de proyectos** (F33, F35, F42-F44): una vez el módulo de reportes (0-3 meses) esté cerrado y validado por más de un ciclo de uso real.
- **RBAC completo con matriz de ~18 actores + Habeas Data** (F57, F58): formalizar la matriz de permisos ahora que hay más roles reales en uso (reportador, investigador, actor territorial) para diseñarla con casos reales en vez de en abstracto.
- **Niveles de acceso graduados por resolución del dato** (F19): requiere que ya exista una base de usuarios acreditados vs. generales, que surge de operar el RBAC un tiempo.

## Explícitamente fuera de alcance

- **CU-06 — Gestión de bonos y mercado de carbono**: descartado del scope del proyecto (ver Funcionalidades.pdf, observaciones CU-06).
- **Cuentas institucionales/organizacionales**: no aplica, la plataforma no se comercializa.
- **Espacios educativos multimedia** (álbumes, cartillas, videojuegos): sin definición suficiente, no se estima hasta que haya una HU concreta.

## Riesgos / decisiones pendientes que pueden mover el roadmap

1. **Tensión login vs. datos abiertos**: el grupo de Nariño pidió restringir todo acceso sin login, lo cual choca con el principio de datos abiertos. Sin resolver esto, F19 y F58 no se pueden diseñar con certeza.
2. **Causa de la desactivación de Insights** (commit `7acfa13`, 2026-09-20): si es un problema de costo/estabilidad, condiciona si F08/F54-F56 se plantean con el mismo proveedor de IA o hay que cambiarlo.
3. **CU-07/CU-08** (incidencia territorial, colaboración interinstitucional) están marcados en el PDF como "se plasma como caso de uso si se requiere" — no confirmados aún como scope real; antes de invertir en el bloque de 6-12 meses correspondiente, confirmar con el equipo si siguen vigentes.
4. **Sostenibilidad post-financiación**: ninguna funcionalidad del roadmap resuelve el NFR de "plan de mantenimiento técnico post-financiación" — es una conversación aparte, no una funcionalidad de producto.

## Referencias

- `files/plataforma/Funcionalidades.pdf`
- [[arquitectura-lista-funcionalidades]]
- Tareas citadas en `personal/tasks/{done,inprogress,blocked,backlog}/`
