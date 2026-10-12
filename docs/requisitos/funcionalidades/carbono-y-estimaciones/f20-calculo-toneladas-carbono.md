# F20 — Cálculo automático de toneladas de carbono almacenadas por región/ecosistema

**Categoría:** Carbono y Estimaciones

## Objetivo

Agregar automáticamente, por región o tipo de ecosistema, cuántas toneladas de carbono
hay almacenadas, a partir de los datos individuales cargados.

## Contexto

Es una agregación espacial sobre datos ya existentes, no una medición nueva.

## Qué hay

`MuestraBiomasa` ya trae `prom_tonc_ha`/`sd_tonc_ha`/`min_tonc_ha`/`max_tonc_ha`
(toneladas de carbono por hectárea, `backend/app/models/biomasa.py:19-27`) como
valores importados, y `biomasa_produccion` (`backend/app/api/reportes/views.py:97-128`)
los expone por sitio/departamento, pero sin ningún paso de cálculo — son datos tal cual
vienen del archivo fuente, sin agregación espacial a nivel región/ecosistema (no hay
`SUM(prom_tonc_ha * area_region)` ni join contra polígonos de ecosistema/cobertura).

## Qué hace falta

No existe agregación automática de carbono almacenado por región o tipo de
ecosistema/cobertura (`Cobertura`/`Vegetacion` en `app/models/cobertura.py` no se
cruzan con los valores de `MuestraBiomasa`/`SubmuestraSuelo` para ese fin); el único
"cálculo" disponible es un promedio simple por sitio/fecha, sin ponderar por área ni
extrapolar a extensión del ecosistema.
