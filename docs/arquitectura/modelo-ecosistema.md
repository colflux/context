# Modelo de datos: ecosistema/zonificación de un sitio

**Estado:** implementado parcialmente (2026-11-03) — `TipoClasificacionEcosistema`,
`ValorClasificacionEcosistema` y `EcosistemaManual` creados y sembrados con la lista
tentativa de valores IDEAM (Páramo, Turbera, Bosque, Periglaciar, Sabana, Humedal) **sin
confirmar con Martín** — decisión explícita del usuario de avanzar con catálogos
tentativos. El modelo `Ecosistema` (área real/geometría oficial) sigue sin implementarse:
no hay shapefile/geopackage oficial disponible, queda fuera de alcance. Pendiente:
confirmar la lista de valores con Martín y lógica de pivoteo para la plantilla (ver
sección Pendiente).

## El problema

El campo 17 de la hoja Metadato ("Ecosistema / Cobertura") necesita guardar a qué
ecosistema (Páramo, Turbera, Bosque, Periglaciar, Sabana, Humedal...) pertenece un punto
de muestreo. No existe hoy ninguna entidad `Ecosistema` en el modelo — se confirmó por
grep que la única referencia es `Proyecto.ESCALA_CHOICES` (incluye "Ecosistema" como
opción de escala espacial, entidad no relacionada).

## Decisión de diseño

Se separan tres responsabilidades que antes se pensaron como una sola entidad genérica
de "Zonificación":

1. **Catálogo de sistemas de clasificación y sus valores permitidos** — hoy solo IDEAM,
   pero deja la puerta abierta a otros (Holdridge, Ramsar) sin tener que migrar de nuevo.
2. **El dato digitado** — lo que la persona en campo reporta al momento de muestrear.
3. **El área real** — el polígono geográfico oficial (capa IDEAM/IAvH), para validar a
   futuro si el dato digitado coincide con dónde cae el punto en la capa oficial. Es la
   misma lógica que *[Calidad de datos: zonas, roles y reglas de validación](calidad-datos-zonas.md)*
   propone como regla dura automática — en este caso, una regla espacial
   (point-in-polygon) en vez de una regla de tipo/rango.

Se descartó la idea inicial de una entidad `Zonificacion`/`TipoZonificacion` genérica a
nivel de `Sitio`: hoy no hay un caso de uso confirmado para más de un sistema de
clasificación a la vez, así que se prefiere no construir esa generalización todavía
(ver `CLAUDE.md` raíz — no diseñar para requisitos hipotéticos).

### Nivel de granularidad: `UnidadMuestreo`, no `Sitio`

El dato digitado se guarda por **unidad de muestreo**, no por sitio: distintas
parcelas/réplicas dentro de un mismo sitio pueden caer en ecosistemas distintos (ej. una
parcela en zona de transición Páramo/Turbera). Esto además es consistente con que otros
campos de Metadato ya reportados por unidad de muestreo ("Tipo muestreo", "Tipo unidad de
muestreo", "Tamaño", "Forma") viven en ese mismo nivel, no en `Sitio`.

## Esquema propuesto

```
TipoClasificacionEcosistema (catálogo)
  - nombre                  ej. "IDEAM"

ValorClasificacionEcosistema (catálogo de valores permitidos, uno por fila)
  - tipo        FK → TipoClasificacionEcosistema
  - valor       ej. "Páramo", "Turbera", "Bosque", "Periglaciar", "Sabana", "Humedal"

Ecosistema (área real — capa oficial, geometría; trabajo futuro)
  - tipo        FK → TipoClasificacionEcosistema
  - valor       FK → ValorClasificacionEcosistema
  - geom        PolygonField (PostGIS)

EcosistemaManual (dato digitado por el equipo de campo)
  - unidad_muestreo   FK → UnidadMuestreo
  - tipo              FK → TipoClasificacionEcosistema
  - valor             FK → ValorClasificacionEcosistema
  - estado_conservacion   # movido acá desde el diseño original de Disturbio en la
  - proteccion_legal      # migración 0124_mover_estado_conservacion_a_ecosistema
```

En la plantilla, `ValorClasificacionEcosistema.valor` aparece con la etiqueta de columna
`ecosistema_IDEAM` (`backend/app/api/etl/views.py`, `_COLUMNAS_PIVOTE_METADATO_GEI`).

`EcosistemaManual` permite varias filas por `UnidadMuestreo` (una por sistema de
clasificación), siguiendo el mismo patrón que ya usa `Cobertura`/`TipoCobertura` para
varias filas por `Sitio`.

## Pendiente

- Confirmar con Martín la lista cerrada de valores de `ValorClasificacionEcosistema`
  para el tipo "IDEAM" — lo implementado (Páramo, Turbera, Bosque, Periglaciar, Sabana,
  Humedal) es reconstrucción de literatura general, no una lista oficial verificada; si
  cambia, requiere migración de datos de los valores ya sembrados.
- Conseguir la capa oficial (shapefile/geopackage del "Mapa de Ecosistemas
  Continentales, Costeros y Marinos de Colombia" IDEAM/IGAC/IAvH/Invemar/SINCHI) para
  poblar `Ecosistema` — sin esto, ese modelo ni siquiera se crea, y la validación
  espacial no se puede hacer todavía.
- Agregar `EcosistemaManual` a `_VISTAS_DESNORMALIZADAS["submuestra_gei"]` en
  `backend/app/api/etl/views.py` para que el campo 17 aparezca en la plantilla
  descargable — lógica de pivoteo nueva (reverse-FK desde `UnidadMuestreo`), fuera de
  alcance de la implementación de 2026-11-03.

## Referencias

- [Plantilla de carga/descarga: metadato y dato de CO2/CH4](plantilla-metadato-dato-co2-camaras.md)
- [Calidad de datos: zonas, roles y reglas de validación](calidad-datos-zonas.md)
- `docs/conocimiento/que-es-un-ecosistema.md` — contexto de literatura ecológica
