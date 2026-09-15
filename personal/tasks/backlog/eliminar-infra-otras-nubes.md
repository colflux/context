# Eliminar infraestructura en otras nubes (Render, etc.)

**Estado:** pendiente
**Creada:** 2026-09-14

## Objetivo

Dar de baja los recursos desplegados en proveedores cloud distintos al
definitivo (por ejemplo Render), para evitar costos y recursos huérfanos
duplicados.

## Plan

- [ ] Identificar todos los proveedores cloud donde hay infraestructura
      desplegada actualmente (Render, etc.)
- [ ] Confirmar cuál es el proveedor definitivo antes de eliminar nada
- [ ] Eliminar los servicios/recursos en los proveedores que ya no se usan
- [ ] Verificar que no queden costos activos ni credenciales/API keys
      colgando de esos proveedores
