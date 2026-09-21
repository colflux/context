# Addendum al catálogo de funcionalidades — hallazgos del prototipo

**Creado:** 2026-09-20
**Fuente:** revisión de `PrototipoCOLFLUX/` (Backend-Colflux, Frontend-Colflux, estadis), cruzada contra `files/plataforma/Funcionalidades.pdf` (v1.0.0).

Este documento **no reemplaza ni edita** `Funcionalidades.pdf` — es un addendum. El prototipo construido antes del catálogo formal (F01-F58) incluye 4 capacidades que ya fueron implementadas (al menos como prueba de concepto) pero que no encajan limpiamente en ninguna F existente. Se numeran F59-F62 para poder referenciarlas desde tareas y el roadmap sin ambigüedad, y quedan pendientes de la misma revisión de viabilidad que el resto del catálogo (ver [[arquitectura-lista-funcionalidades]]).

## F59 — Diccionario de campo con interpretación técnica inversa

Traduce una **observación coloquial hecha en campo** (olor, color, textura del suelo al pisar, sensación ambiental, frases espontáneas) a una variable técnica, una regla cuantitativa de umbral y una interpretación ecológica. Es la dirección opuesta a F24 (que traduce término técnico → lenguaje simple para el ciudadano): aquí el punto de entrada es la percepción sensorial de quien está tomando la muestra, y la salida es la lectura técnica esperable.

Ejemplo real del prototipo: "olor a huevo podrido" → `Flujo de CH4 ≥ 0.0735 µmol/m²/s + Nivel del agua ≥ 8 cm` → "sugiere punto muy activo en producción o liberación de gases".

Implementado en el prototipo como CSV de 7 columnas (categoría, término, definición ecológica, variable asociada, variable secundaria, regla cuantitativa, interpretación) servido vía `/api/wiki`.

*Pendiente:* ¿vive dentro de F24 como una sección más, o es un módulo aparte orientado a quien captura el dato (no al público)? ¿quién mantiene y valida las reglas cuantitativas (comité científico, F14)?

## F60 — Validación colaborativa de términos del diccionario (semáforo de aceptación)

Mecanismo de votación (0-100%) sobre qué tan acertada es una definición del diccionario/wiki, con un semáforo (rojo ≤30% / amarillo 31-70% / verde ≥71% / gris sin votos) calculado como promedio de todas las valoraciones recibidas por término.

No debe confundirse con el "semáforo de calidad" de F11, que evalúa la confiabilidad de un **dato medido**, no de una **definición del diccionario**. Tampoco es exactamente F25 (wiki colaborativa), que solo contempla historial de versiones y comentarios — la votación agregada es un mecanismo distinto de consenso comunitario.

*Pendiente:* ¿quién puede votar (cualquier visitante o solo usuarios registrados)? ¿qué pasa cuando un término llega a rojo — se revisa, se retira, se marca como controvertido?

## F61 — Motor de inferencia dato↔diccionario en tiempo real

Dado un registro de medición real (CO2, CH4, nivel de agua, temperatura, etc.), evalúa automáticamente las reglas cuantitativas de **todos** los términos del diccionario (F59) y muestra cuáles aplican a esa medición específica. Es un parser de reglas determinístico (umbrales con operadores `≥`/`≤` combinados con AND/OR), no un modelo de IA — se diferencia de F08 (geoportal con IA generativa) en que no interpreta lenguaje natural, sino que evalúa condiciones estructuradas ya definidas en el diccionario.

Implementado en el prototipo dentro del dashboard de flujos (`evaluarReglaCuantitativa` en `dashboard.js`): al seleccionar una medición, anota automáticamente con qué términos del diccionario de campo coincide.

*Pendiente:* ¿corre en el backend o en el cliente? ¿se usa también para marcar datos entrantes automáticamente (ej. al cargar un CSV) o solo bajo demanda al consultar?

## F62 — Análisis estadístico exploratorio de datos cargados

Análisis exploratorio (no solo visualización) sobre un dataset de mediciones: estadísticas descriptivas, evaluación de asimetría (skew) por variable, detección de valores atípicos vía boxplots, matriz de correlación entre variables, y comparación de variables por categoría (ej. tipo de vegetación) y condición (ej. día/noche), con conclusiones redactadas.

Distinto de F29-F31 (visualización/gráficos configurables por el usuario final) y de F16 (publicar un modelo predictivo ya construido): esto es el paso de análisis exploratorio *previo*, típicamente hecho por un investigador o el equipo técnico sobre un dataset específico, no una herramienta self-service para cualquier usuario.

Implementado en el prototipo como notebook de Python (pandas/seaborn/matplotlib) sobre un dataset fijo (`estadis/Análisis correlaciones guatavita.ipynb`), corrido manualmente, sin conexión al backend ni a datos cargados dinámicamente por usuarios.

*Pendiente:* ¿se automatiza como reporte generado por el sistema al cargar un dataset nuevo, o queda como herramienta de analista fuera de la plataforma (notebook aparte)? ¿a quién se le expone (solo investigadores acreditados)?

## Referencias

- `files/plataforma/Funcionalidades.pdf` (catálogo original F01-F58)
- `PrototipoCOLFLUX/Backend-Colflux/src/main/resources/wiki_colflux.csv`
- `PrototipoCOLFLUX/Frontend-Colflux/diccionario.js`, `dashboard.js`
- `PrototipoCOLFLUX/estadis/Análisis correlaciones guatavita.ipynb`
- [[arquitectura-lista-funcionalidades]]
