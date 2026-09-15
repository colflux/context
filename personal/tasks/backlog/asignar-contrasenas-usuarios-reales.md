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
- [x] Cambiar la contraseña temporal de Viviana (puesta solo para
      verificar el flujo) por una real — hecho el 2026-09-15 (contraseña
      real vía shell de Django, no por `/team`; guardada en
      `personal/tasks/inprogress/.credenciales`, gitignoreado).

## Notas

**2026-09-15:** al cambiar la contraseña de Viviana se encontró que el
bootstrap de `implementar-login-real` había dejado registros `Usuario`
(dominio) y `auth.User` desalineados en producción — dos `Usuario`
duplicados sin correo o sin `auth_user`, y un `auth.User` superusuario
(`admin`/correo de Daniel) sin `Usuario` ligado — que hacían fallar el
login con "Credenciales inválidas" pese a la contraseña correcta. Se
limpiaron los huérfanos y se agregó `manage.py check_usuarios_huerfanos`
en `backend` (corre en cada arranque del contenedor `web`, advertencia no
bloqueante) para detectar esto antes de que vuelva a pasar — relevante
para cuando se asignen contraseñas al resto de usuarios reales en esta
misma tarea: conviene correr ese comando después de cada asignación
masiva para confirmar que quedaron bien enlazados.

De paso, se subió el nivel de Milena González (ya tenía `auth_user`
propio, este cambio no formaba parte de esta tarea) de `ciudadano` a
`reportador`.

## Referencias

- [[implementar-login-real]]
