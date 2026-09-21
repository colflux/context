# Archivo de datos validado (swap) para prototipo de reporte

**Sesión de Claude:** session_01YUBhkSM9LKVCC5CYhFzgSf
**Estado:** en progreso
**Creada:** 2026-09-17

## Objetivo

Contar con un archivo de datos validado que se pueda subir a la plataforma, al menos para el prototipo, como insumo previo para poder documentar el flujo de reporte en [[wiki-manual-usuario]].

## Contexto

Antes de redactar el manual de usuario para reportar datos, se necesita un archivo de ejemplo ya validado (formato swap) que sirva como caso de prueba real del flujo de carga.

## Plan

- [ ] Definir qué formato/estructura debe tener el archivo swap para ser válido
- [ ] Conseguir o generar un archivo de ejemplo que cumpla la validación
- [ ] Probar la subida del archivo en el prototipo
- [ ] Dejar el archivo disponible como referencia para el manual de usuario

## Entregables

(Link o ruta del archivo validado una vez esté listo.)

## Referencias

- [[wiki-manual-usuario]]
- [[modelo-datos-categorias]]

## Historial

| Fecha | Descripción |
|---|---|
| 2026-09-17 | Se crea la tarea. |
| 2026-09-17 | Se mueve a en progreso. |
| 2026-09-17 | Sesión larga centrada en arreglar y mejorar la descarga de Excel desde `/etl/datos` (bug de permisos al descargar con `<a href>` sin token, orden de hojas/columnas, columnas ambiguas, columnas vacías, colores por categoría, diccionario de datos) — detalle completo en [[modelo-datos-categorias]]. La descarga ya funciona bien. Queda pendiente, fuera de esta tarea y de esta sesión: **Aleja** va a revisar que todos los datos se hayan subido correctamente a la plataforma (validación de datos, no de la descarga en sí). |
