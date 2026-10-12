# F16 — Publicación de modelos predictivos

**Categoría:** Carbono y Estimaciones

## Objetivo

Que un investigador pueda publicar un modelo predictivo (proyecciones, cruces de
variables) como recurso consultable por otros actores.

## Contexto

El catálogo original dejó pendiente: ¿cómo se ve "publicado" en la interfaz? ¿quién
puede consultarlo? ¿incluye metadatos/metodología?

## Qué hay

Existe `Publicacion`/`ResultadoPublicacion` (`backend/app/models/publicacion.py`), que
permite registrar referencias bibliográficas con resultados por variable (incluye COS,
Biomasa_Total_C, flujos) y un campo `metodologia` de texto libre por resultado — es un
catálogo de citas/artículos, no un modelo predictivo ejecutable. En
`PrototipoCOLFLUX/estadis/Análisis correlaciones guatavita.ipynb` hay un análisis
exploratorio de correlaciones (CO2/CH4 vs. variables climáticas, por tipo de cobertura)
en un notebook Jupyter standalone, nunca integrado al backend ni expuesto en UI.

## Qué hace falta

- No existe ningún mecanismo de "publicar" un modelo predictivo como recurso
  consultable interactivo.
- No hay UI de publicación/consulta, ni control de quién puede consultarlo, ni
  metadatos de metodología estructurados (solo texto libre en
  `Publicacion`/`ResultadoPublicacion`).
- El análisis del prototipo es un artefacto de exploración de datos, no un modelo
  productivo publicable.
