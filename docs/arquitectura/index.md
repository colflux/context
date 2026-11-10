# Arquitectura

_Por construir._

Decisiones técnicas de la plataforma y el requisito que las origina.

- [Repositorios](repositorios.md) — inventario de repos del proyecto y diagrama de integración.
- [Diagrama C4](diagrama-c4.md) — misma integración, en notación C4 formal.
- [Git: conceptos y acuerdos de flujo de trabajo](git-flow.md) — qué es Git y de dónde viene, conceptos base, y una propuesta de modelo de ramas (GitHub Flow) pendiente de validar con el equipo.
- [Guía: levantar el ecosistema COLFLUX](guia-desarrollo-local.md) — cómo correr cada repositorio en local y cómo se conectan entre sí.
- [Modelo de datos relacional](modelo-datos.md) — links a la wiki de dbdocs.io y al diagrama de dbdiagram.io con el esquema completo.
- [Modelo de datos: series de tiempo de torre EC](modelo-datos-torre-ec.md) — propuesta de entidades nuevas (`MuestraTorre`/`SubmuestraEddy`/`SubmuestraReddy`) para cargar datos reales de Eddypro/ReddyProc, pendiente de validar con el equipo.
- [Calidad de datos: zonas, roles y reglas de validación](calidad-datos-zonas.md) — propuesta de zonas de calidad (bronze/silver/gold), roles del flujo de validación y motor de reglas, pendiente de discutir con el equipo OE2 y con Martín.
- [Modelo de datos: ecosistema/zonificación de un sitio](modelo-ecosistema.md) — propuesta de `TipoClasificacionEcosistema`/`ValorClasificacionEcosistema`/`Ecosistema`/`EcosistemaManual` para el campo "Ecosistema / Cobertura" de la plantilla CO2, pendiente de confirmar valores con Martín.
- [Modelo de datos: disturbio de una unidad de muestreo](modelo-disturbio.md) — propuesta de `Disturbio`/`UnidadMuestreoDisturbio` para los campos de disturbio y `DOM_DIST_MGMT` de la plantilla CO2, pendiente de confirmar con el equipo.
- [Modelo de datos: cobertura de una unidad de muestreo](modelo-cobertura.md) — propuesta de `ValorCobertura`/`CoberturaManual` (reemplaza `Cobertura` actual) para los campos `cobertura_IPCC`/`CLC`/`IGBP`/`nom_comun`/`Suelo IPCC` de la plantilla CO2, pendiente de confirmar valores y plan de migración de datos.
- [Modelo de datos: microtopografía de una unidad de muestreo](modelo-microtopografia.md) — propuesta de `Microtopografia` (catálogo) + `UnidadMuestreo.microtopografia` (reemplaza `MuestraAmbiental.microtopo`) para el campo `microtopografia` de la plantilla CO2, pendiente de confirmar con el equipo.
- [Modelo de datos: exposición externa de una unidad de muestreo](modelo-exposicion-externa.md) — propuesta de `FuenteExterna`/`ExposicionExterna` para los campos `distancia_drenaje/fuego/pastoreo/cultivo` de la plantilla CO2, pendiente de confirmar con el equipo.
