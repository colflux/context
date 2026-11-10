# Calidad de datos: zonas, roles y reglas de validación

**Estado:** propuesta para discutir con el equipo OE2 y con Martín (ecólogo) — no es una decisión tomada.

## El problema que lo origina

Llegó la queja de que Martín (ecólogo, encargado del contexto científico del OE2) le está diciendo directamente al Objetivo 1 que sus datos "están mal", generando friction entre objetivos. El mensaje que bajó fue "frenarlo".

Pero la corrección puntual no resuelve la causa: si alguien del equipo siente que tiene que intervenir ad-hoc para señalar que un dato está mal, es porque **no existe todavía un mecanismo dentro de la plataforma que haga esa señalización de forma sistemática** — ni reglas automáticas, ni un rol claro de quién valida qué, ni un canal formal para pedir corrección. Hoy esa reunión de los martes 2pm hace ese trabajo de forma manual e informal.

La propuesta de este documento es resolver la causa (un módulo de calidad de datos en la plataforma) en vez de solo la consecuencia (pedirle a Martín que no comente).

## Lo que ya existe hoy (punto de partida real)

- **[F11 — Flujo de validación/moderación + semáforo de calidad](../requisitos/funcionalidades/datos-y-carga/f11-validacion-semaforo-calidad.md):** hay un estado de validación (`subido/mapeado/validado/importado`) pero a nivel de **carga de archivo completa**, no de dato/registro individual. No hay semáforo visual ni estado "Publicado"/"Pendiente" por registro. No está definido quién aprueba/rechaza un dato individual.
- **[F57 — RBAC](../requisitos/funcionalidades/acceso-a-plataforma/f57-rbac-control-acceso-roles.md):** existen 4 niveles de acceso en cascada (`ciudadano < investigador < reportador < admin`) y un catálogo aparte de roles de proyecto (`RolUsuario`: coordinador/investigador/técnico). Ninguno de los dos modela todavía un rol tipo "validador de calidad de datos".
- Dos tareas en backlog que ya apuntaban a esto, de una reunión anterior del módulo de calidad (2026-09-01): [[calidad-datos-categorizacion]] y [[calidad-datos-trazabilidad]]. Este documento las retoma y les da forma de propuesta concreta.

## Propuesta: tres piezas separadas

La idea tiene tres partes que conviene discutir por separado porque tienen dueños distintos dentro del equipo:

### 1. Zonas de calidad de datos (pieza técnica — datos/plataforma)

Patrón a investigar/adaptar: la **arquitectura medallion** (bronze/silver/gold), común en plataformas de datos:

- **Bronze (crudo):** el dato tal como se subió, sin tocar. Se guarda siempre, aunque esté "mal" — es la fuente de verdad de lo que realmente se recibió.
- **Silver (validado/limpio):** el dato que pasó las reglas duras automáticas (tipos, rangos, campos obligatorios, duplicados) y/o correcciones manuales de alguien con el rol adecuado.
- **Gold (listo para análisis/publicación):** el dato ya curado, consistente y agregado si aplica, listo para alimentar modelos, reportes o el geoportal público.

No es la única opción — otros marcos de referencia a mirar antes de decidir: dimensiones estándar de calidad de datos (completitud, exactitud, consistencia, oportunidad, unicidad — usadas por ISO 8000 y DAMA-DMBOK), y herramientas de reglas declarativas tipo Great Expectations/dbt tests (no para adoptar la herramienta en sí, sino como referencia de cómo se modela una "regla de calidad" de forma reutilizable).

Preguntas abiertas para el equipo de datos (Vivi + Daniel):

- ¿Las tres zonas son estados de un mismo registro (`SubmuestraGEI.zona_calidad`) o tablas/particiones separadas?
- ¿Bronze es inmutable para siempre, o se purga después de un tiempo una vez que pasó a silver?
- ¿Cómo interactúa esto con `CargaArchivo.estado` que ya existe (F11) — se reemplaza, o conviven (carga completa vs. registro individual)?

### 2. Roles del flujo (pieza de proceso — quién hace qué)

Lo que falta formalizar, por fuera de la jerarquía de acceso de F57:

- **Quién sube** el dato (ya existe: cualquier nivel con permiso de escritura).
- **Quién valida/corrige directamente** (hoy informalmente Martín, u otro miembro del equipo con criterio científico).
- **Quién puede solicitar validación/corrección a un experto**, sin aplicarla él mismo — este es el rol que probablemente resuelve la tensión actual: Martín (o quien tenga ese rol) **señala y pide corrección**, pero no decide unilateralmente ni le dice directamente al Objetivo 1 que "está mal" por fuera del flujo.
- **Quién define las reglas de calidad** aplicables a cada fuente/tipo de dato (ver punto 3).

Esto convive con la reunión de los martes 2pm — la propuesta no es eliminarla, sino que deje de ser el único mecanismo: lo que hoy se resuelve 100% en esa reunión, debería resolverse en buena parte dentro de la plataforma (reglas automáticas + flujo de corrección), y la reunión quedaría para los casos que las reglas no logran capturar.

### 3. Motor de reglas de calidad (pieza de producto — cómo se definen y aplican)

Dos preguntas de diseño separadas:

- **¿Reglas personalizables por fuente de dato, o un consenso único por atributo?** Por ejemplo, un rango válido de temperatura puede ser distinto para una torre de flujo en páramo vs. en sabana — ¿eso se modela como regla por fuente/proyecto, o como una regla por atributo con excepciones?
- **¿Quién crea las reglas?** Si se abre un "módulo de creación de reglas por atributo", ¿lo usa cualquier investigador sobre su propia fuente, o solo alguien con el rol de experto/validador (ahí es donde entraría Martín formalmente, con autoridad explícita y no ad-hoc)?

Mínimo viable sugerido para no bloquear el avance: empezar con **reglas duras básicas automáticas** (tipo de dato, rango, obligatoriedad, duplicados) que no dependen de que nadie las cree manualmente, y dejar el módulo de reglas personalizables por atributo como una segunda fase.

## Relación con otras piezas de la plataforma

- No se puede avanzar reglas automáticas sin resolver primero [[calidad-datos-trazabilidad]] (quién subió, cómo se capturó el dato) — varias reglas de calidad dependen de saber el método de captura (ej. un rango válido puede depender del instrumento).
- El semáforo visual de F11 es el lugar natural para mostrar la zona de calidad (bronze/silver/gold) al usuario final.
- F57 (RBAC) necesitaría un rol nuevo o un ajuste a `RolUsuario` para modelar "validador experto" si se decide que es un rol formal distinto de nivel de acceso.

## Próximos pasos

- [ ] Llevar este documento a la reunión del equipo OE2 (martes 2pm) para decisión de alcance y fases.
- [ ] Sesión específica con Martín para que, como experto científico, defina qué reglas de calidad existen hoy de forma implícita en su cabeza y cuáles se pueden volver reglas explícitas en la plataforma — y para acordar su rol formal en el flujo (validador/solicitante de corrección, no corrector unilateral fuera de proceso).
- [ ] Decidir el MVP: reglas duras automáticas primero, módulo de reglas personalizables después.

## Referencias

- [F11 — Flujo de validación/moderación de datos + semáforo de calidad](../requisitos/funcionalidades/datos-y-carga/f11-validacion-semaforo-calidad.md)
- [F57 — Control de acceso basado en roles (RBAC)](../requisitos/funcionalidades/acceso-a-plataforma/f57-rbac-control-acceso-roles.md)
- `tasks/backlog/calidad-datos-categorizacion.md`
- `tasks/backlog/calidad-datos-trazabilidad.md`
