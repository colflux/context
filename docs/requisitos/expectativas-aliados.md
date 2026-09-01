# Expectativas de aliados y comunidades

_Síntesis del Anexo 06 (Identificación de perfiles y expectativas) y "Resultados visita aliados" (carteleras de co-diseño con La Chorrera, UDENAR Grupo 1 y Nariño Grupo 2). A diferencia del [Anexo 1 y Anexo 2](problema-usuarios.md), que son documentos técnicos/contractuales del proyecto, esta es información recogida directamente de los usuarios finales en talleres de diagnóstico — útil para priorizar y para chequear que no se nos quede nada del lado del usuario._

## Tipos de usuario (Anexo 06)

El Anexo 06 nombra 6 tipos de usuario, sin permisos asociados (a diferencia de los 5 roles con permisos del Anexo 1):

- Investigadores
- Instituciones públicas
- Tomadores de decisiones
- Comunidades
- Estudiantes
- Público en general

**A reconciliar:** esta lista no mapea 1:1 con los 5 roles del Anexo 1 ([problema-usuarios.md](problema-usuarios.md)) — por ejemplo "Instituciones públicas" y "Tomadores de decisiones" no tienen un rol equivalente claro (¿son parte de "Cliente"? ¿de "Actor Territorial"?), y "Estudiantes"/"Público en general" tampoco aparecen en el Anexo 1. Vale la pena confirmar con Adriana si esto amplía los roles formales o si son sub-perfiles dentro de los ya definidos.

## Expectativas de contenido (Anexo 06)

- **Carbono**: contenidos de carbono, ciclo de carbono, estimaciones, mapa de carbono del país, reservas, factores de emisión.
- **Biodiversidad**
- **Imágenes satelitales**
- **Información descriptiva de Colflux** (institucional/proyecto)

Tipos de datos esperados: datos brutos de flujo, datos "claros" (procesados/entendibles), datos contextuales, datos para toma de decisiones — es decir, no solo el dato crudo, distintos niveles de elaboración para distintos usuarios.

## Expectativas de uso (Anexo 06)

Agrupadas por tema (lista larga del Anexo 06, ya recortada de duplicados):

- **Académico/investigativo**: uso académico e investigativo, capas de información, análisis de datos con incidencia política, exportar/descargar información, transferencia de conocimiento.
- **Territorial/comunitario**: información georreferenciada, respuestas específicas sobre territorios, defensa territorial, incidencia en políticas públicas, planeación institucional y comunitaria, fortalecimiento de capital social.
- **Colaboración institucional**: integración entre instituciones, oportunidades de colaboración, apoyar procesos de coordinación entre diferentes actores, redes de monitoreo, reportes nacionales y regionales.
- **Mercado de carbono**: bonos de carbono, conocer el comportamiento del mercado de carbono.
- **Predicción/planeación**: predicciones estratégicas de adaptación al cambio climático, definición de procesos de biodiversidad, estimaciones de contenidos de carbono.
- **Accesibilidad**: para todas las edades, información actualizada periódicamente, realizar gráficos y mapas.

## Requisitos de front (Anexo 06)

Cinco puntos explícitos sobre la interfaz, en orden de la lámina original:

1. Filtros
2. Fácil acceso
3. Gráficos entendibles
4. Lenguaje accesible y claro
5. Recursos visuales

## Resultados de talleres de co-diseño (visita a aliados)

Tres grupos construyeron una maqueta física de la plataforma y priorizaron funcionalidades con una matriz de importancia (+1 baja, +2 media, +3 alta).

### La Chorrera (comunidad)

| Prioridad | Funcionalidad |
|---|---|
| Alta (+3) | Geoportal interactivo con navegación territorial (por departamento, mapas interactivos, barra de búsqueda, login, descarga de datos) |
| Alta (+3) | Información ambiental, territorial y cultural (bosques, caranguchales, biodiversidad — peces/población/territorio —, carbono, cultura, precipitación; fotos de cultura y biodiversidad local por región) |
| Media (+2) | Educación y recursos multimedia (álbumes fotográficos, videos, cartillas, videojuegos) |
| Media (+2) | Accesibilidad IA, bot y comunicación (narrar la información, bot de WhatsApp, IA, sistema de notificaciones) |
| Media (+2) | Metodología y conexión entre comunidades (apartado de metodología/autores/lugares participantes; sección de red para interconexión e intercambio entre comunidades) |
| Baja (+1) | Filtros y visualización de datos (región, municipio, lluvia, temperatura, cobertura vegetal; gráficas y dashboards) |

### UDENAR Grupo 1

| Prioridad | Funcionalidad |
|---|---|
| Alta (+3) | Geoportal como centro de la plataforma, diferenciando zonas — despliega gráficos e info por territorio |
| Alta (+3) | Dashboard con filtros de información (gases de efecto invernadero por territorio, filtrable por fecha y condiciones) |
| Media (+2) | Imágenes y videos explicativos en cada sección |
| Media (+2) | Chatbot con IA para consultas rápidas |
| Media (+2) | Red integrada de investigadores |
| Baja (+1) | Juegos interactivos (todas las edades) |
| Baja (+1) | Contacto con personal desarrollador (control y seguimiento de la plataforma) |

También mencionan **acceso diferenciado por tipo de usuario** (quién puede editar/subir info) — ya cubierto por el requisito de RBAC en [funcionalidades.md](funcionalidades.md).

### Nariño Grupo 2

| Prioridad | Funcionalidad |
|---|---|
| Alta (+3) | Geoportal con restricción — info completa requiere login; selección por departamento |
| Alta (+3) | Filtros (lluvia, temperatura, cobertura vegetal; identificar región por ubicación/tiempo) — prioriza imágenes, video y juegos |
| Media (+2) | Comunicación (WhatsApp + chatbot; interés explícito en **versión disponible sin internet**) |
| Media (+2) | Contacto externo (líderes o entidades clave para preguntas directas) |
| Baja (+1) | Taller y pedagogía (sección de Tips con metodologías breves) |
| Baja (+1) | Wiki (sección de comentarios para retroalimentar el uso) |

## Funcionalidades nuevas frente a [funcionalidades.md](funcionalidades.md)

Estas ideas salen de los talleres y **no** están en la lista actual extraída del Anexo 1/Anexo 2 — se deberían evaluar para incorporar o descartar explícitamente:

- **Modo sin conexión / versión offline** (Nariño) — relevante dado el público de comunidades rurales con acceso limitado a internet; no aparece en ningún anexo técnico.
- **Juegos interactivos educativos** (La Chorrera, UDENAR, Nariño) — pedido en los 3 talleres, es de los ítems más consistentes entre grupos aunque puntuado como prioridad baja/media.
- **Red de investigadores / sección de interconexión entre comunidades** — funcionalidad social explícita, distinta del acceso a datos.
- **Sección de comentarios / retroalimentación sobre el uso** (wiki-like, Nariño).
- **Sección de Tips / metodología resumida en lenguaje breve**, separada del contenido técnico completo.
- **Contacto directo con desarrolladores o líderes/entidades clave** dentro de la plataforma.
- **Barra de búsqueda general** en el geoportal (La Chorrera) — no aparece explícita en funcionalidades.md, aunque hay "búsqueda avanzada por región" del Anexo 1.
- **Restricción de acceso a nivel de geoportal completo tras login** (Nariño) — más fuerte que el RBAC por dato/registro que ya describe el Anexo 1; confirmar si es "todo detrás de login" o solo ciertas capas.

El **bot de WhatsApp**, el **chatbot con IA** y el **RBAC/acceso diferenciado** ya estaban contemplados (ver [problema-usuarios.md](problema-usuarios.md) y [funcionalidades.md](funcionalidades.md)) — los talleres confirman que son de las funcionalidades más valoradas por las comunidades, no solo un requisito técnico del Anexo 2.

## Nota de alcance (del propio Anexo 06)

> Los resultados recogen la totalidad de las expectativas manifestadas, pero la implementación final está sujeta a criterios de priorización técnica, viabilidad y los objetivos core del proyecto.

Es decir: esta página es insumo para priorizar, no una lista de compromisos cerrados.
