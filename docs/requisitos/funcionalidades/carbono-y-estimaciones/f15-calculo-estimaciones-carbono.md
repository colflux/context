# F15 — Cálculo de estimaciones de carbono

**Categoría:** Carbono y Estimaciones

## Objetivo

Que el backend calcule estimaciones de carbono y factores de emisión por ecosistema,
en vez de depender de que ese cálculo ya venga hecho en los datos de entrada.

## Contexto

Es lógica de backend/científica más que de interfaz. El catálogo original dejó
pendiente: ¿cómo se calculan exactamente esas estimaciones?

## Qué hay

El backend almacena directamente valores de carbono reportados por fuentes externas
(ya calculados fuera del sistema): `MuestraBiomasa.contenido_carbono`/`prom_tonc_ha`
(`backend/app/models/biomasa.py:16-24`), `SubmuestraSuelo.carbono_pct`/`soil_chem_c_org`
(`backend/app/models/suelo.py:76-88`), y flujos crudos CO2/CH4/N2O en `SubmuestraGEI`.
Los endpoints de reportes (`backend/app/api/reportes/views.py`) solo agregan
(`Avg`/`Count`) estos valores ya existentes por fecha/profundidad/taxón; no hay ningún
cálculo de factor de emisión ni fórmula de conversión biomasa→carbono en el código (no
hay constantes IPCC ni función que derive `contenido_carbono` desde DAP/altura/especie).

## Qué hace falta

- La lógica de cálculo en sí (factores de emisión por ecosistema, fórmulas alométricas
  biomasa→carbono). Hoy el "cálculo" ocurre fuera de la plataforma, en el archivo
  fuente, y solo se importa el resultado.
- El comentario en `reportes/views.py:46-51` confirma explícitamente que no se puede
  calcular carbono por especie con el esquema actual ("se usa el conteo de individuos
  como proxy").
