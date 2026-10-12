# F62 — Análisis estadístico exploratorio de datos cargados

**Categoría:** Addendum — hallazgos del prototipo

## Objetivo

Ofrecer análisis exploratorio (no solo visualización) sobre un dataset de mediciones:
estadísticas descriptivas, evaluación de asimetría (skew) por variable, detección de
valores atípicos vía boxplots, matriz de correlación entre variables, y comparación de
variables por categoría (ej. tipo de vegetación) y condición (ej. día/noche), con
conclusiones redactadas.

## Contexto

Distinto de [F29](../visualizacion-y-reportes/f29-visualizacion-ciclo-carbono.md) (visualización/gráficos
configurables por el usuario final) y de
[F16](../carbono-y-estimaciones/f16-publicacion-modelos-predictivos.md) (publicar un
modelo predictivo ya construido): esto es el paso de análisis exploratorio *previo*,
típicamente hecho por un investigador o el equipo técnico sobre un dataset específico,
no una herramienta self-service para cualquier usuario.

## Qué hay

Implementado en el prototipo como notebook de Python (pandas/seaborn/matplotlib) sobre
un dataset fijo (`PrototipoCOLFLUX/estadis/Análisis correlaciones guatavita.ipynb`),
corrido manualmente, sin conexión al backend ni a datos cargados dinámicamente por
usuarios.

## Qué hace falta

- ¿Se automatiza como reporte generado por el sistema al cargar un dataset nuevo, o
  queda como herramienta de analista fuera de la plataforma (notebook aparte)?
- ¿A quién se le expone (solo investigadores acreditados)?
- Integrar la lógica del notebook a un flujo dentro de la plataforma (hoy es 100%
  manual y desconectado de datos en vivo).
