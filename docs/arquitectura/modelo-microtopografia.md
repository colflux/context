# Modelo de datos: microtopografía de una unidad de muestreo

**Estado:** implementado (2026-11-03) — `Microtopografia` creada, `UnidadMuestreo.microtopografia`
agregado, datos de `MuestraAmbiental.microtopo` migrados y el campo viejo eliminado.
Pendiente: agregar `UnidadMuestreo.microtopografia` a
`_VISTAS_DESNORMALIZADAS["submuestra_gei"]` (`backend/app/api/etl/views.py`) para que
aparezca en la plantilla descargable — es un FK hacia adelante desde `UnidadMuestreo`, no
necesita lógica de pivote nueva, solo falta sumarlo a la cadena de campos planos.

## El problema

El campo `microtopo` (Hummock/Hollow/Pool/Lawns/Ditch) vive hoy en `MuestraAmbiental`
(`backend/app/models/co2.py`), un modelo de lectura ambiental repetida por fecha/hora —
igual que `soil_temp`, `water_level`, etc. Pero la microtopografía describe el terreno
físico donde está instalada la cámara, no algo que varíe medición a medición. Además,
`MuestraAmbiental.unidad_muestreo` es una FK inversa desde `UnidadMuestreo`, lo que repite
el mismo problema técnico que [Cobertura](modelo-cobertura.md): el mecanismo de
`_campos_planos`/`cadena` en `backend/app/api/etl/views.py` solo sigue FKs hacia adelante,
así que hoy no se puede exportar a la hoja Metadato sin lógica de pivote nueva.

## Decisión de diseño

A diferencia de Ecosistema/Cobertura/Disturbio, la microtopografía **no necesita**
catálogo de tipos + catálogo de valores permitidos: tiene una sola lista cerrada y fija,
ya definida en el código (`MICROTOPO_CHOICES`), terminología estándar de la literatura de
humedales que no se espera que cambie. El patrón correcto es el mismo que `Disturbio`
(catálogo simple, sin split Tipo/Valor).

## Esquema propuesto

```
Microtopografia (catálogo)
  - nombre                  ej. "Hummock", "Hollow", "Pool", "Lawns", "Ditch"

UnidadMuestreo
  - microtopografia         FK → Microtopografia (nuevo campo; reemplaza MuestraAmbiental.microtopo)
```

Se reporta una sola vez por unidad de muestreo, como un atributo fijo de dónde está
instalada la cámara — no una serie de tiempo.

## Pendiente

- Agregar el campo a `_VISTAS_DESNORMALIZADAS["submuestra_gei"]` para que aparezca en la
  plantilla descargable (ver nota de Estado arriba).
- Si la microtopografía llegara a cambiar entre lecturas de una misma unidad de muestreo
  (ej. por inundación estacional), reconsiderar si debe volver a vivir en
  `MuestraAmbiental` en vez de `UnidadMuestreo`.

## Referencias

- [¿Qué es la cobertura (de la tierra)?](../conocimiento/que-es-la-cobertura.md) — sección "Microtopografía".
- [Modelo de datos: cobertura de una unidad de muestreo](modelo-cobertura.md) — mismo patrón de reverse-FK pendiente de pivote.
- `backend/app/models/co2.py` — `MuestraAmbiental.microtopo`, `MICROTOPO_CHOICES`.
- [Plantilla de carga/descarga: metadato y dato de CO2/CH4](plantilla-metadato-dato-co2-camaras.md)
