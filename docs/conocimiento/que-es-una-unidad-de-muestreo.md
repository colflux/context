# ¿Qué es una unidad de muestreo?

Una **unidad de muestreo** es el espacio físico concreto donde se toma una medición o
muestra — es la pieza mínima sobre la que se reporta un dato. Un [sitio](que-es-un-ecosistema.md)
(un punto con coordenadas) puede tener varias unidades de muestreo dentro — varias
parcelas o transectos repartidos en el área, para capturar variabilidad interna en vez
de asumir que un solo punto representa todo el sitio.

Es un concepto distinto de **unidad experimental**: la unidad experimental es el "grupo"
o tratamiento que se está comparando (ej. "parcela con pastoreo" vs. "parcela sin
pastoreo" dentro de un mismo proyecto), mientras que la unidad de muestreo es cada
instancia física concreta donde efectivamente se mide.

## Tipos de unidad de muestreo

El diseño de muestreo en ecología usa distintas formas de unidad según qué se quiera
medir:

- **Parcela** (*plot*) — área delimitada (cuadrada, rectangular o circular) donde se
  cuenta/mide todo lo que hay dentro. Es la unidad más común para biomasa, cobertura
  vegetal y conteo de individuos.
- **Transecto** — línea (o franja angosta) a lo largo de la cual se toman mediciones o
  se registra lo que se cruza. Útil para capturar gradientes (ej. de altitud, de
  humedad) en una sola unidad.
- **Conglomerado** (*cluster*) — grupo de varias parcelas/puntos pequeños agrupados,
  tratados como una sola unidad de muestreo para efectos de diseño estadístico (reduce
  el costo de desplazamiento sin perder tanta información como un solo punto).

## Qué describe el "tamaño" y la "forma" de una unidad de muestreo

Una vez elegido el tipo, dos atributos la terminan de definir:

- **Forma** — cuadrada, rectangular o circular (para parcelas). Afecta cómo se calcula
  el área y qué tan fácil es delimitarla en campo.
- **Tamaño/área** — cuánto espacio cubre. El tamaño correcto depende de qué se está
  midiendo: una parcela para biomasa arbórea necesita ser más grande que una para
  musgo o suelo, porque los árboles están más dispersos. Para cámaras de gases
  (flujos CO₂/CH₄), el área suele ser mucho más chica (del orden de cm²), ya que la
  cámara cubre un área puntual del suelo, no una parcela de vegetación completa.

## Tipo de muestreo: probabilístico o no probabilístico

Además de la forma física de la unidad (parcela/transecto/conglomerado), hay otra
clasificación independiente: **cómo se eligió su ubicación** dentro del sitio.

**Probabilístico** — cada ubicación posible tiene una probabilidad conocida (y distinta
de cero) de ser seleccionada. Permite inferencia estadística válida: generalizar los
resultados a todo el sitio con un margen de error calculable. Subtipos comunes:

- *Aleatorio simple* — se sortean ubicaciones al azar dentro del área.
- *Sistemático* — se ubican a intervalos regulares (ej. una parcela cada 50 m sobre una grilla).
- *Estratificado* — se divide el área en estratos (ej. por altitud o cobertura) y se
  muestrea aleatoriamente dentro de cada uno, para asegurar representación de todos.
- *Por conglomerados* — se seleccionan grupos/clusters completos en vez de unidades
  individuales.

**No probabilístico** — las unidades se eligen por criterio de quien muestrea, no al
azar. No permite la misma inferencia estadística rigurosa, pero suele ser más práctico
en campo. Subtipos comunes:

- *Por conveniencia* — se muestrea donde es más fácil llegar/acceder.
- *Dirigido/intencional* (*purposive*) — se eligen sitios específicos porque cumplen
  alguna condición de interés (ej. justo donde hubo un incendio).
- *Por cuotas* — se fija cuántas unidades de cada categoría se necesitan, sin
  aleatorizar cuáles.

**Por qué importa:** determina qué tan válido es generalizar los resultados del
muestreo a todo el sitio/ecosistema. Un dato de flujo de carbono sacado de muestreo
probabilístico permite decir "el área X almacena en promedio Y toneladas de carbono con
un margen de error Z"; uno no probabilístico sigue siendo un dato válido, pero su
alcance interpretativo para generalizar es distinto.

## Por qué importa para Colflux

La mayoría de los campos de "cómo se midió" de la plantilla de datos (tipo de muestreo,
tipo de unidad, tamaño, forma, periodicidad) describen la unidad de muestreo, no el sitio
en general — porque son datos necesarios para poder comparar o combinar correctamente
mediciones de distintas unidades, incluso dentro de un mismo sitio.

## Referencias

- `backend/app/models/sitio.py` — `UnidadMuestreoTipo`, `UnidadExperimental`, `UnidadMuestreo`, `Parcela`, `Transecto` (modelo actual).
- [Plantilla de carga/descarga: metadato y dato de CO2/CH4](../arquitectura/plantilla-metadato-dato-co2-camaras.md)
