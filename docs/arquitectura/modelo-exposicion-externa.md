# Modelo de datos: exposición externa de una unidad de muestreo

**Estado:** implementado (2026-11-03) — `FuenteExterna`/`ExposicionExterna` creados tal
como se diseñó, catálogo sembrado con `Fuego`/`Pastoreo`/`Cultivo`/`Drenaje`. Sin datos
previos que migrar (campos nuevos). Pendiente: lógica de pivoteo para que aparezca en la
plantilla descargable (ver sección Pendiente).

## El problema

Estos cuatro campos no describen un disturbio que ocurrió *en* la unidad de muestreo
(eso ya lo cubre [Disturbio](modelo-disturbio.md), con `anios_disturbio`,
`anios_desde_fin`, `estado_conservacion`...) — describen qué tan **cerca** está la unidad
de una fuente de alteración que está en otro lugar (un canal de drenaje, un incendio
cercano, ganado pastando al lado, un cultivo vecino). Es exposición al entorno, no
historial propio: forzarlo dentro de `UnidadMuestreoDisturbio` obligaría a rellenar
campos que no tienen sentido para una fuente externa (un canal de drenaje no "empieza y
termina" como un incendio).

## Decisión de diseño

Entidad propia, mismo patrón catálogo + instancia que el resto de esta sesión, pero
mucho más simple (solo dos campos por instancia):

```
FuenteExterna (catálogo)
  - nombre                  ej. "Fuego", "Pastoreo", "Cultivo", "Drenaje"

ExposicionExterna (instancia reportada)
  - unidad_muestreo         FK → UnidadMuestreo
  - fuente                  FK → FuenteExterna
  - distancia_m             DecimalField
```

### Mapeo de campos de la plantilla

| Campo de la plantilla | Campo del modelo |
|---|---|
| `distancia_fuego` | `ExposicionExterna.distancia_m` de la fila con `fuente="Fuego"` |
| `distancia_pastoreo` | `ExposicionExterna.distancia_m` de la fila con `fuente="Pastoreo"` |
| `distancia_cultivo` | `ExposicionExterna.distancia_m` de la fila con `fuente="Cultivo"` |
| `distancia_drenaje` | `ExposicionExterna.distancia_m` de la fila con `fuente="Drenaje"` |

`FuenteExterna` es un catálogo independiente del de `Disturbio` — aunque "Fuego" y
"Pastoreo" aparecen conceptualmente en ambos, un disturbio registrado (ocurrió acá) y una
exposición externa (ocurre cerca) son datos distintos y pueden coexistir sin conflicto.

## Pendiente

- Confirmar el origen/metodología de los 4 valores de `FuenteExterna.nombre`
  (`Fuego`, `Pastoreo`, `Cultivo`, `Drenaje`). No vienen de un estándar
  citado: son los mismos 4 campos fijos (`distancia_drenaje`, `distancia_fuego`,
  `distancia_pastoreo`, `distancia_cultivo`) que ya existían hardcodeados en
  `FlujoCamaras` desde `0001_initial.py` (plantilla original de cámaras), solo
  promovidos a catálogo el 2026-11-03 sin validar si son definitivos o si
  falta alguna fuente externa relevante (ej. carretera, cuerpo de agua,
  actividad minera).
- Lógica de pivoteo al agregar `ExposicionExterna` a
  `_VISTAS_DESNORMALIZADAS["submuestra_gei"]` (`backend/app/api/etl/views.py`) — mismo
  patrón de reverse-FK pendiente que `CoberturaManual`/`EcosistemaManual`/
  `UnidadMuestreoDisturbio`, explícitamente fuera de alcance de la implementación de
  2026-11-03 (ver tarea siguiente en `tasks/`).

## Referencias

- [Modelo de datos: disturbio de una unidad de muestreo](modelo-disturbio.md) — distinción entre disturbio propio y exposición externa.
- [Plantilla de carga/descarga: metadato y dato de CO2/CH4](plantilla-metadato-dato-co2-camaras.md)
