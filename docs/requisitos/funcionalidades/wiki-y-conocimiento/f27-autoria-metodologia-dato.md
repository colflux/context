# F27 — Sección de autoría/metodología por dato o fuente

**Categoría:** Wiki y Conocimiento

## Objetivo

Dejar constancia de la "autoridad sobre el dato": metodología, autores y lugares
participantes, por dato o por fuente.

## Contexto

El catálogo original dejó pendiente: ¿es una página general del proyecto o un metadato
por cada dato/registro individual?

## Qué hay

Hay metadatos de metodología a nivel de registro individual en varios modelos:
`backend/app/models/mom.py` (`MuestraMOM`) tiene campos como `metodologia_muestreo_mom`,
`metodologia_muestreo_dfm_dgm`, `metodologia_tamano`, `metodologia_amp_to`,
`metodologia_hojarasca`; `backend/app/models/suelo.py` también referencia metodología;
y `Publicacion`/`ResultadoPublicacion` (`publicacion.py`) incluyen `metodologia` por
resultado y autores vinculados a sitios. Esto es "autoría/metodología por dato", ya
existente como estructura de datos, pero no hay evidencia de que se exponga como
sección visible en la UI (ninguna vista en frontend muestra estos campos al usuario).

## Qué hace falta

Definir si la UI expone esto como metadato por registro (ya hay campos en el modelo de
datos para soportarlo) o como página general del proyecto (no implementada, se
traslaparía con [F25](f25-wiki-colaborativa-proyecto.md)); falta el endpoint/serializer
que agregue estos metadatos de forma consultable y el componente de frontend que los
muestre.
