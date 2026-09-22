# Evaluar portar del prototipo: diccionario de campo, semáforo de aceptación y motor de inferencia

**Estado:** pendiente
**Creada:** 2026-09-20
**A cargo:** Viviana Bautista
**Sesión de Claude Code:** https://claude.ai/code/session_01PLhTY5eDrHYCgJ2PUWg8RP

## Objetivo

Decidir si F59, F60 y F61 (ver [funcionalidades-addendum.md](../../../docs/roadmap/funcionalidades-addendum.md)) se portan del prototipo (`PrototipoCOLFLUX/`) al backend/frontend reales, y si el análisis exploratorio de F62 se automatiza o se deja como herramienta aparte de analista.

## Contexto

Al revisar `PrototipoCOLFLUX/` (Backend-Colflux en Spring, Frontend-Colflux en HTML/JS vanilla) se encontraron 4 funcionalidades ya prototipadas que no tienen F asignada en `Funcionalidades.pdf` v1.0.0:

- **F59** — diccionario de campo con interpretación técnica inversa (olor/color/textura → variable + regla cuantitativa + interpretación), en `wiki_colflux.csv`.
- **F60** — semáforo de aceptación comunitaria de términos del diccionario (votación 0-100%, no confundir con el semáforo de calidad de dato de F11).
- **F61** — motor de inferencia dato↔diccionario en tiempo real (`evaluarReglaCuantitativa` en `dashboard.js`): dado un registro de medición, anota automáticamente qué términos del diccionario aplican.
- **F62** — análisis estadístico exploratorio en Python (notebook `estadis/Análisis correlaciones guatavita.ipynb`) sobre un dataset fijo, sin conexión al backend.

El prototipo está construido en un stack distinto (Java/Spring Boot vs. Django/DRF del backend real), así que "portar" implica reimplementar la lógica, no mover código directamente.

## Plan

- [ ] Revisar con el equipo si F59/F60/F61 aportan valor real al flujo de captura de datos en campo (¿lo usa el ecólogo o el actor territorial hoy?)
- [ ] Si aplica, definir dónde vive el diccionario de campo (F59) en el modelo de datos real: ¿tabla nueva, o extensión de `catalogo`/`etl`?
- [ ] Decidir si el semáforo de aceptación (F60) es necesario o si el flujo real de validación (F11/F14) ya cubre la necesidad de confianza en el diccionario
- [ ] Evaluar si el motor de inferencia (F61) corre en backend (Django) o se queda en frontend, y si debe aplicarse también a datos cargados en bloque (no solo bajo demanda)
- [ ] Decidir si F62 se automatiza como reporte generado por el sistema o se mantiene como notebook de analista fuera de la plataforma

## Entregables

(Pendiente — depende de la decisión del equipo.)

## Referencias

- [docs/roadmap/funcionalidades-addendum.md](../../../docs/roadmap/funcionalidades-addendum.md)
- `PrototipoCOLFLUX/Backend-Colflux/src/main/resources/wiki_colflux.csv`
- `PrototipoCOLFLUX/Frontend-Colflux/diccionario.js`, `dashboard.js`
- `PrototipoCOLFLUX/estadis/Análisis correlaciones guatavita.ipynb`
- [[arquitectura-lista-funcionalidades]]

## Historial

| Fecha | Descripción |
|---|---|
| 2026-09-20 | Se crea la tarea a partir de la revisión de `PrototipoCOLFLUX/` pedida en `personal/TODAY.md`. Se documentan los hallazgos como F59-F62 en el addendum del catálogo; queda pendiente la decisión de viabilidad/portabilidad con el equipo. |
