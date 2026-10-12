# F03 — Superposición y comparación de capas

**Categoría:** Geoportal

## Objetivo

Ver varias capas a la vez sin perder información, para encontrar correlaciones.

## Contexto

Depende de que exista primero un sistema de capas independientes
([F02](f02-sistema-capas-activables.md)) — hoy los toggles del mapa son excluyentes.

## Qué hay

No se encontró evidencia de implementación en el código actual. Las capas/toggles son
mutuamente excluyentes (Mapa vs. Satélite, Sitios vs. Regiones) — nunca se muestran dos
capas temáticas superpuestas. Tampoco hay referencia en PrototipoCOLFLUX (confirmado
que no tiene ningún componente de mapa).

## Qué hace falta

Todo: no hay slider de comparación, split-view, ni lógica para superponer variables
(ej. carbono + biodiversidad) y buscar correlaciones visuales.
