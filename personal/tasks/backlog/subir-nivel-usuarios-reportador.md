# Subir nivel de varios usuarios a reportador

**Estado:** en progreso
**Creada:** 2026-09-17

## Objetivo

Que los usuarios reales identificados en `/team` puedan usar "Reportar",
subiéndolos de `Ciudadano` a `reportador`.

## Contexto

Sale de una revisión de la tabla de usuarios en `/team` (screenshot).
Usuarios identificados como `Ciudadano` que deberían pasar a
`reportador`:

- Alejandra Diaz (ID 7)
- Andrea Catalina Chaparro Guzmán (ID 6)
- Martin Otalora (ID 5)

Pendiente de confirmar: si Alejandra Gonzalez (ID 2) y daniel (ID 1),
actualmente `Admin`, también deben bajarse a `reportador` o se quedan
como están.

Ver [[definir-rol-y-habilitar-reportar]] para el gate que ya está
implementado en `frontend` (`useRolActual().tieneNivel('reportador')`).

## Plan

- [ ] Confirmar con Viviana si Alejandra Gonzalez y daniel también pasan
      a `reportador` o se mantienen como `Admin`
- [ ] Cambiar a `reportador` desde `/team`: Alejandra Diaz, Andrea
      Catalina Chaparro Guzmán, Martin Otalora

## Entregables

(Pendiente — falta completar los cambios de rol.)

## Referencias

- [[definir-rol-y-habilitar-reportar]]

## Historial

| Fecha | Descripción |
|---|---|
| 2026-09-17 | Se crea la tarea a partir de la revisión de la tabla de usuarios en `/team`. |
