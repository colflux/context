# F61 — Motor de inferencia dato↔diccionario en tiempo real

**Categoría:** Addendum — hallazgos del prototipo

## Objetivo

Dado un registro de medición real (CO2, CH4, nivel de agua, temperatura, etc.), evaluar
automáticamente las reglas cuantitativas de todos los términos del diccionario
([F59](f59-diccionario-campo-inverso.md)) y mostrar cuáles aplican a esa medición
específica.

## Contexto

Es un parser de reglas determinístico (umbrales con operadores `≥`/`≤` combinados con
AND/OR), no un modelo de IA — se diferencia de
[F08](../geoportal/f08-geoportal-ia-generativa.md) (geoportal con IA generativa) en que
no interpreta lenguaje natural, sino que evalúa condiciones estructuradas ya definidas
en el diccionario.

## Qué hay

Implementado en el prototipo dentro del dashboard de flujos
(`evaluarReglaCuantitativa` en `PrototipoCOLFLUX/Frontend-Colflux/dashboard.js`): al
seleccionar una medición, anota automáticamente con qué términos del diccionario de
campo coincide. No forma parte del backend ni frontend vigentes.

## Qué hace falta

- ¿Corre en el backend o en el cliente?
- ¿Se usa también para marcar datos entrantes automáticamente (ej. al cargar un CSV) o
  solo bajo demanda al consultar?
- Portar la lógica de `dashboard.js` del prototipo al stack vigente.
