# Wiki / manual de usuario

**Sesión de Claude:** session_01Qxi9vvTVEv2ykqB6yEGm7k
**Estado:** pendiente
**Creada:** 2026-09-17

## Objetivo

Crear una página o entrada de wiki con el manual de usuario que explique cómo reportar datos en la plataforma COLFLUX.

## Contexto

(Completar con más detalle: pasos concretos del flujo de reporte de datos a documentar, para quién es el manual, dónde se publicará.)

## Plan

- [x] Definir alcance: qué pasos del flujo de reporte de datos debe cubrir el manual
- [x] Elegir formato/herramienta (ej. wiki en el repo, sitio de documentación, etc.)
- [x] Redactar contenido (paso a paso de cómo reportar datos)
- [x] Publicar y enlazar desde el frontend/plataforma
- [ ] Actualizar la guía cuando el envío del formulario deje de ser mock (ver
      [[reportes-conectar-formulario-reportar-backend]]): documentar
      moderación/tiempos si aplica

## Entregables

- `wiki/docs/usuarios/guias/reportar-datos.md` — guía paso a paso: requisitos
  (nivel Reportador), cómo solicitarlo, los 4 campos del formulario con
  ejemplos de buena/mala descripción, y una nota de que el envío hoy es mock.
- Enlazada desde `frontend` en la card "Guía de reporte" de
  `src/pages/Participacion.tsx`, que navega internamente a `/reportar/guia`
  (`src/pages/GuiaReporte.tsx`), página que embebe la guía en un `iframe`
  (con link "Abrir en pestaña nueva" como respaldo) para que no se sienta
  como salir de la plataforma.

## Referencias

- `frontend`: `src/pages/Participacion.tsx`, `src/pages/ReportarFormulario.tsx`,
  `src/pages/GuiaReporte.tsx`
- `wiki`: `docs/usuarios/guias/reportar-datos.md`, `mkdocs.yml`

## Historial

| Fecha | Descripción |
|---|---|
| 2026-09-17 | Se crea la tarea. |
| 2026-09-21 | Se redacta la guía de "reportar datos" en la wiki (rol Reportador, cómo solicitarlo, los 4 campos del formulario con ejemplos) y se enlaza desde la card "Guía de reporte" en `Participacion.tsx`. De paso: se separó el formulario de reporte a una página propia (`/reportar/formulario`, antes vivía inline en `/reportar`), se reordenaron las cards del hub (Guía → Gestión de Datos → Formulario web) y el sidebar (Mapa → Indicadores → Reportar). Pendiente: el manual más amplio (cuenta, primeros pasos) sigue sin cubrir — esta sesión solo cerró el flujo de reporte. |
| 2026-09-21 | Se cambia el link de "Guía de reporte" de externo (nueva pestaña) a una página interna `/reportar/guia` que embebe la guía en `iframe`, para que no se sienta como salir de la plataforma. |
