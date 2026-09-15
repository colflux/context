# Asignar contraseña de acceso a los usuarios reales que aún no tienen login

**Estado:** pendiente
**Creada:** 2026-09-14

## Objetivo

Que todos los usuarios reales del equipo (`/api/usuarios/`) puedan
loguearse con el sistema de login real, no solo Viviana.

## Contexto

Sale de [[implementar-login-real]]: se implementó login real (usuario +
contraseña por correo) y se hizo el bootstrap de una sola cuenta —
Viviana Bautista (`lviviana13@gmail.com`) — con una contraseña temporal
para poder verificar el flujo end-to-end.

Los demás usuarios reales ya existentes en la base (Alejandra Diaz,
Andrea Chaparro, Martin) **no tienen `auth_user` vinculado todavía**, así
que no pueden loguearse hasta que alguien les asigne una contraseña desde
`/team` (editar usuario → campo "Contraseña de acceso"). Además, para
que un usuario pueda tener contraseña necesita tener `correo` o
`correo_institucional` diligenciado — hoy varios de ellos aparecen "Sin
correo" en la tabla de `/team`, así que ese dato hay que completarlo
primero.

## Plan

- [ ] Completar el correo de los usuarios reales que aún no lo tienen
- [ ] Asignarles contraseña desde `/team` (uno por uno, comunicándosela
      por un canal seguro, no por este repo)
- [ ] Cambiar la contraseña temporal de Viviana (puesta solo para
      verificar el flujo) por una real

## Referencias

- [[implementar-login-real]]
