# Entender el problema y los usuarios

_Síntesis del Anexo 2 (Documento Técnico) y el Anexo 1 (Casos de Uso e Historias de Usuario). No es contenido nuevo — es lo que ya está en ambos documentos, organizado para responder "quién usa la plataforma y qué necesita lograr"._

## El problema

**Problema central** (Anexo 2, sección 2.1):

> Insuficiente generación, gestión y transferencia del conocimiento alrededor de las dinámicas de carbono en ecosistemas no forestales (páramos, sabanas, bosques de galería, morichales, humedales y sus suelos orgánicos), en las regiones Centro Oriente, Llanos y Centro Sur - Amazonía de Colombia.

**Por qué importa ahora mismo:**

- **Cero (0)** plataformas digitales existen hoy para consultar la dinámica de carbono en estos ecosistemas en Colombia (línea base 2024, revisión de mercado de 25 plataformas).
- La información que sí existe está dispersa en artículos técnico-científicos y reportes puntuales, en lenguaje técnico no accesible para comunidades locales — genera una barrera lingüística, cultural y social.
- Sin esta información, las comunidades no pueden tomar decisiones efectivas sobre su territorio ni acceder a oportunidades de mercados de carbono sin depender de un intermediario técnico.

**Lo que la plataforma (OE2) debe resolver:**

> Desarrollar una plataforma para el monitoreo integrado, consulta y reporte de la dinámica de carbono que complemente los inventarios existentes, reconociendo el papel de la diversidad y el agua en estas dinámicas, y garantizando un acceso abierto y democrático a la información.

## Los usuarios

Del Anexo 1 (Historias de Usuario HU-001 a HU-005). Cinco roles, con permisos y necesidades distintas:

_Nota sobre la fuente: estos 5 roles concretos (con sus permisos) fueron definidos por Adriana en el Anexo 1 — el Anexo 2 **no** trae una lista formal de roles de usuario. El Anexo 2 solo exige que exista **control de acceso basado en roles (RBAC)** como requisito de seguridad (lo repite varias veces, sin nombrar los roles) y menciona de forma genérica la diversidad de usuarios a cubrir ("desde corporaciones autónomas regionales hasta comunidades indígenas o campesinas", "investigadores o instituciones gubernamentales" para datos sensibles). La sección "Análisis de participantes" del Anexo 2 tampoco aplica aquí — esos son actores institucionales del proyecto (universidades aliadas, departamentos, municipios), no roles de usuario de la plataforma._

| Actor | Quién es | Qué necesita lograr | Permisos |
|---|---|---|---|
| **Investigador (Interno)** | Científico de la entidad líder (PUJ y aliadas) | Registrar datos de monitoreo en campo, validar información, realizar análisis/modelado avanzado, exportar bases completas y publicar modelos predictivos | Control total: lectura, escritura y validación |
| **Investigador Externo** | Académico o universidad aliada | Consultar investigaciones, descargar capas GIS, aportar sus propios hallazgos científicos, validar la rigurosidad metodológica | Lectura general; escritura restringida a sus propios registros/proyectos (sujeta a revisión) |
| **Actor Territorial** | Líder indígena, campesino, comunidad o gobierno local | Consultar el estado de los recursos de su territorio en lenguaje simple y visual, reportar alertas (tala ilegal, contaminación, deforestación, incendios) | Consulta y aportes/comentarios comunitarios — **sin permiso de editar datos duros** de investigación (modo solo lectura) |
| **Analista** | Administra, procesa y valida la información del sistema | Filtrar por fecha/región/indicadores clave, generar y exportar reportes consolidados (PDF, Excel, GeoJSON) | Procesa y valida — rol operativo, no de investigación de campo |
| **Cliente** | Consume el resultado final (dashboard) | Visualizar indicadores consolidados en tiempo real, aplicar filtros, exportar reportes | Exclusivo de lectura, reportería y visualización de alto nivel |

**Canales por los que cada actor accede** (Anexo 2, Actividad 2.3) — relevante porque no todos los usuarios tienen el mismo acceso a infraestructura digital:

- **App con IA generativa** y **portal tradicional** (Geoportal + Dashboard) — canal principal para Investigadores, Analista y Cliente.
- **Bot de WhatsApp** — pensado específicamente para comunidades rurales e indígenas (Actor Territorial) con acceso limitado a infraestructura digital avanzada.

## De aquí en adelante

Estos usuarios y sus necesidades son la base para escribir requisitos verificables. Cada requisito nuevo debería poder trazarse a uno de estos actores y a lo que necesita lograr — no a una decisión técnica (eso va en [Arquitectura](../arquitectura/index.md)).
