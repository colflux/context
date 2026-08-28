# Diagrama C4

Misma información que el [diagrama de integración de Repositorios](repositorios.md), en notación **C4 formal** (nivel Contenedor), para quien prefiera ese estándar.

_Clic sobre el diagrama para ampliarlo a pantalla completa · Esc para cerrar._

```mermaid
%%{init: {
  "theme": "base",
  "themeVariables": {
    "fontSize": "16px",
    "primaryColor": "#eaf4f1",
    "primaryBorderColor": "#198A77",
    "primaryTextColor": "#1a1a1a",
    "lineColor": "#57270F",
    "tertiaryColor": "#f5f5f5"
  },
  "c4": {
    "diagramMarginX": 30,
    "diagramMarginY": 30,
    "c4ShapeMargin": 90,
    "c4ShapePadding": 20,
    "width": 220,
    "personFontSize": 15,
    "personFontFamily": "Inter",
    "external_personFontSize": 15,
    "systemFontSize": 15,
    "systemFontFamily": "Inter",
    "boundaryFontSize": 15,
    "messageFontSize": 14
  }
}}%%
C4Container
    title Contenedores del sistema COLFLUX

    Person(usuario, "Usuario final / investigador")
    Person(equipo, "Equipo técnico")

    Container_Boundary(frontend, "frontend") {
        Component(geoportal, "Geoportal", "Sección", "Mapas y visualización de datos")
        Component(wikiseccion, "Wiki", "Sección", "Conceptos y documentación para usuario final")
        Component(chat, "Chat", "Sección", "Asistente conversacional")
    }

    Container_Boundary(backend, "backend") {
        Container(api, "API backend", "Django + PostGIS")
        Container(iafunctions, "ia-functions", "Microservicios IA")
        ContainerDb(db, "DB", "PostgreSQL/PostGIS")
    }

    System_Ext(context, "context", "Docs del equipo (este repo)")

    Rel(usuario, geoportal, "Usa")
    Rel(usuario, wikiseccion, "Consulta")
    Rel(usuario, chat, "Pregunta")
    Rel(api, geoportal, "Sirve datos")
    Rel(api, wikiseccion, "Sirve contenido")
    Rel(iafunctions, chat, "Responde")
    Rel(api, iafunctions, "Invoca")
    Rel(api, db, "Lee / escribe")
    Rel(equipo, context, "Mantiene")
```
