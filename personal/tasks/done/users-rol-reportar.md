# Definir qué rol puede usar "Reportar" y habilitar el gate

**Estado:** cerrada
**Creada:** 2026-09-14
**Cerrada:** 2026-09-15

## Objetivo

Que la página "Reportar" (`/reportar` en `frontend`, participación
ciudadana) vuelva a estar disponible, pero solo para el rol que
corresponda — no abierta a cualquiera como estaba antes.

## Contexto

Sale de [[implementar-login-real]]: al cerrar el login real, Viviana pidió
deshabilitar por ahora el acceso a "Reportar" en toda la navegación
(nav superior, sidebar de `/mapas`, CTA y card de `Home.tsx`) porque
"ya quedamos qué rol lo tenía" — la decisión de qué rol puede reportar
se tomó en otro momento/canal, pero no llegó a implementarse como gate
real. Se dejó la página tratada igual que los ítems "próximamente"
(`Sensores`, `Capas`, etc. en `AppSidebar.tsx`): atenuada, sin link
activo, pero la ruta `/reportar` sigue existiendo y es accesible por URL
directa.

## Plan

- [x] Confirmar/recordar qué rol (`reportador`, u otro) debe tener acceso
      a "Reportar" — confirmado: `reportador` en adelante (`reportador`,
      `admin`)
- [x] Decidir el patrón de gate: redirect silencioso como `/team`
      (`useRolActual().tieneNivel('reportador')`), consistente con
      `Team.tsx`
- [x] Reactivar los links en `Navbar.tsx`, `AppSidebar.tsx`,
      `Home.tsx` (CTA + card) una vez implementado el gate — ahora
      condicionados a `tieneNivel('reportador')`; sin ese nivel se
      mantiene el estado atenuado "próximamente" que ya existía
- [ ] Evaluar si la página en sí (`Participacion.tsx`) necesita
      conectarse a un endpoint real — hoy el formulario es un mock que
      no envía nada al backend (queda pendiente, fuera de alcance de
      esta tarea)

## Entregables

Implementado en `frontend`: `src/hooks/useRolActual.ts` ya exponía
`tieneNivel`; se usó en `Navbar.tsx`, `AppSidebar.tsx`, `Home.tsx` y
`Participacion.tsx` (esta última con redirect a `/` si el usuario no
tiene el nivel, igual que `Team.tsx` redirige a `/data`).

## Referencias

- [[implementar-login-real]]

## Historial

| Fecha | Descripción |
|---|---|
| 2026-09-14 | Se crea la tarea. |
| 2026-09-15 | Se confirma el rol (`reportador`) y se implementa el gate en `frontend`. Se cierra; queda pendiente conectar el formulario a un endpoint real, fuera de alcance. |
