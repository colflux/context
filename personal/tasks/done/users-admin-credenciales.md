# Procedimiento para recuperar acceso cuando se pierde la contraseña de admin

**Estado:** en progreso
**Creada:** 2026-09-17

## Objetivo

Dejar documentado un procedimiento repetible para cuando un usuario
admin (o cualquier usuario) pierda su contraseña y no exista todavía un
flujo de "recuperar contraseña" self-service en `frontend`/`backend`.

## Contexto

Surgió al asignarle contraseña a Viviana Bautista (admin, ID 3,
`lviviana13@gmail.com`), que no tenía una asignada. Como no hay
recuperación de contraseña por correo implementada aún, la única vía es
que alguien con acceso al servidor la resetee manualmente desde el
contenedor del backend en producción.

Restricción importante: Claude no puede escribir/generar la contraseña
directamente en ningún campo ni ejecutarla por shell en nombre del
usuario (política sin excepciones, aunque el usuario lo autorice). Lo
que sí puede hacer es generar una contraseña aleatoria segura y dejar
listo el comando exacto para que la persona dueña de la cuenta (o un
admin) lo ejecute ella misma.

## Procedimiento (validado 2026-09-17 con Viviana Bautista)

1. Conectarse por SSH al servidor de producción
   (`ubuntu@ip-172-26-15-69`).
2. Ubicar el contenedor del backend corriendo (`docker ps`) — en
   producción es `backend-web` (no `web`; ese nombre solo aplica en
   local con `docker compose`).
3. Ejecutar:
   ```bash
   docker exec -it backend-web python manage.py changepassword <email-o-username>
   ```
   Pide la contraseña nueva dos veces por consola (no queda en el
   historial de shell).
4. Verificar que el `Usuario` (dominio) y el `auth.User` sigan bien
   enlazados:
   ```bash
   docker exec -it backend-web python manage.py check_usuarios_huerfanos
   ```
   (Comando agregado en [[asignar-contrasenas-usuarios-reales]] tras
   encontrar registros huérfanos la primera vez que se tocaron
   contraseñas en prod.)
5. Comunicar la contraseña nueva a la persona dueña de la cuenta por un
   canal seguro (no por este repo ni por chat sin cifrar).

## Plan

- [x] Validar el procedimiento manual con un caso real (Viviana
      Bautista, admin)
- [ ] Evaluar si vale la pena implementar un flujo self-service de
      "olvidé mi contraseña" en `frontend`/`backend` para no depender de
      acceso SSH al servidor
- [ ] Documentar este procedimiento también en
      `docs/arquitectura/guia-desarrollo-local.md` o donde corresponda
      para que no dependa de esta tarea

## Entregables

Procedimiento validado arriba. Pendiente decidir si se formaliza com![alt text](image.png)o
documentación permanente o se implementa un flujo automático.

## Referencias

- [[asignar-contrasenas-usuarios-reales]]

## Historial

| Fecha | Descripción |
|---|---|
| 2026-09-17 | Se crea la tarea a partir de la necesidad real de resetear la contraseña de Viviana Bautista (admin). Se documenta el procedimiento manual vía `manage.py changepassword` en el contenedor `backend-web` de producción. |
