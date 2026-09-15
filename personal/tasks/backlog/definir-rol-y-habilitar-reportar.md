# Definir qué rol puede usar "Reportar" y habilitar el gate

**Estado:** pendiente
**Creada:** 2026-09-14

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

- [ ] Confirmar/recordar qué rol (`reportador`, u otro) debe tener acceso
      a "Reportar"
- [ ] Decidir el patrón de gate: ¿redirect silencioso como `/team`
      (`useRolActual`), o mostrar la página igual mostrando qué compone
      pero con partes deshabilitadas?
- [ ] Reactivar los links en `Navbar.tsx`, `AppSidebar.tsx`,
      `Home.tsx` (CTA + card) una vez implementado el gate
- [ ] Evaluar si la página en sí (`Participacion.tsx`) necesita
      conectarse a un endpoint real — hoy el formulario es un mock que
      no envía nada al backend

## Referencias

- [[implementar-login-real]]
