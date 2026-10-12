# F14 — Protocolo de validación por comité científico

**Categoría:** Datos y Carga

## Objetivo

Curaduría institucional de fuentes externas antes de integrarlas a la base de datos,
distinta de la validación por registro individual de
[F11](f11-validacion-semaforo-calidad.md).

## Contexto

El "comité científico" funciona como actor de gobernanza/moderación, no como usuario
que consume la plataforma.

## Qué hay

No se encontró evidencia de implementación en el código actual. Búsquedas por
"comite"/"committee"/"curaduria"/"curator" en backend no arrojaron modelos ni vistas.
Lo más cercano es `Publicacion`/`ResultadoPublicacion` (`app/models/publicacion.py`) con
un campo booleano `validacion_campo` (validación en campo, no institucional/comité) y
`datos_disponibles_repositorio`, que es metadata bibliográfica, no un flujo de
curaduría de fuentes externas.

## Qué hace falta

Todo: no existe un modelo de "comité científico" como actor, ni un estado de curaduría
institucional previo a integrar una fuente externa a la base de datos, ni distinción en
código entre esta validación institucional y la validación individual de F11 (que
tampoco existe completamente). Sería una capa nueva sobre `FuenteDatos`/`CargaArchivo`.
