# F59 — Diccionario de campo con interpretación técnica inversa

**Categoría:** Addendum — hallazgos del prototipo

## Objetivo

Traducir una observación coloquial hecha en campo (olor, color, textura del suelo al
pisar, sensación ambiental, frases espontáneas) a una variable técnica, una regla
cuantitativa de umbral y una interpretación ecológica — la dirección opuesta a
[F24](../wiki-y-conocimiento/f24-wiki-glosario-carbono.md) (que traduce término técnico
→ lenguaje simple para el ciudadano).

## Contexto

Aquí el punto de entrada es la percepción sensorial de quien está tomando la muestra,
y la salida es la lectura técnica esperable. Ejemplo real del prototipo: "olor a huevo
podrido" → `Flujo de CH4 ≥ 0.0735 µmol/m²/s + Nivel del agua ≥ 8 cm` → "sugiere punto
muy activo en producción o liberación de gases".

## Qué hay

Implementado como prueba de concepto en `PrototipoCOLFLUX/Backend-Colflux`: un CSV de 7
columnas (categoría, término, definición ecológica, variable asociada, variable
secundaria, regla cuantitativa, interpretación), servido vía el endpoint `/api/wiki`.
No forma parte del backend ni frontend vigentes.

## Qué hace falta

- ¿Vive dentro de F24 como una sección más, o es un módulo aparte orientado a quien
  captura el dato (no al público)?
- ¿Quién mantiene y valida las reglas cuantitativas (comité científico, ver
  [F14](../datos-y-carga/f14-validacion-comite-cientifico.md))?
- Migrar del CSV del prototipo a un modelo de datos propio en el backend vigente.
