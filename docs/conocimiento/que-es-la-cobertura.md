# ¿Qué es la cobertura (de la tierra)?

La **cobertura de la tierra** (*land cover*) es lo que efectivamente cubre físicamente la
superficie de un punto — bosque, pastizal, cultivo, cuerpo de agua, área construida.
Es un concepto **observacional**: se puede determinar mirando el sitio o una imagen
satelital, sin necesidad de saber nada sobre el clima, la historia ecológica o el proceso
que la originó.

Es distinto de [ecosistema](que-es-un-ecosistema.md): el ecosistema es la unidad
funcional (comunidad biótica + ambiente abiótico interactuando), mientras que la
cobertura es la "foto" de qué hay ahora sobre el suelo. Dos sitios del mismo ecosistema
(ej. páramo) pueden tener coberturas distintas (pajonal, frailejonal, suelo desnudo por
disturbio), y viceversa: una misma cobertura (ej. pastizal) puede estar presente en
ecosistemas distintos.

## Los sistemas de clasificación de cobertura

No existe un único estándar universal — distintas instituciones y usos definen sus
propias categorías. Colflux reporta la cobertura de un sitio bajo varios sistemas en
paralelo, porque cada uno sirve para comparar con fuentes distintas:

- **IPCC** — categorías de uso de la tierra para inventarios de gases de efecto
  invernadero (Forest Land, Cropland, Grassland, Wetlands, Settlements, Other Land). Es
  el sistema que más importa para reportes de carbono internacionales, porque es el que
  usan los inventarios nacionales de GEI.
- **CLC (Corine Land Cover)** — sistema europeo adaptado por IDEAM para Colombia,
  orientado a cobertura/uso de la tierra en detalle (bosque denso, pastizal, cultivo,
  área urbana...).
- **IGBP** — clasificación global de 17 clases, la que usan productos satelitales como
  MODIS. Es también el campo de vegetación/ecosistema que exige reportar el estándar
  [BADM/AmeriFlux](estandar-badm-ameriflux.md) para cualquier torre de flujo.
- **Suelo IPCC** — no es cobertura vegetal sino tipo de suelo (mineral u orgánico),
  relevante porque el tipo de suelo condiciona cuánto carbono puede almacenar.
- **Nombre común** — la forma en que localmente se nombra la cobertura, sin ajustarse a
  ningún esquema formal (ej. "frailejonal", "pajonal").
- **Vegetación funcional** (*Plant Functional Type*) — clasifica la vegetación por cómo
  funciona (forma de vida, estrategia fisiológica), no por especie. Ej.: árbol
  caducifolio/perennifolio, gramínea C3/C4, arbusto, hierba/forbia, liana, suculenta,
  planta con aerénquima (tejido para sobrevivir en suelo inundado, típico de humedales).
  Es el esquema que usan los modelos globales de vegetación y carbono porque no necesita
  saber la especie exacta — alcanza con saber qué tipo funcional cubre cada área para
  estimar biomasa y flujos de forma comparable entre sitios distintos. Colflux reporta,
  por unidad de muestreo, hasta tres tipos (primaria/secundaria/terciaria) con su
  porcentaje de cobertura.

## Microtopografía: el microrrelieve dentro de una misma cobertura

La **microtopografía** es la variación de relieve a escala muy pequeña (centímetros)
dentro de un mismo punto — no la topografía general del terreno (cresta, ladera, valle),
sino el microrrelieve puntual donde se instala cada unidad de muestreo. Es un concepto
distinto de cobertura: dos cámaras bajo la misma cobertura (ej. turbera) pueden estar en
microrrelieves distintos y por eso medir flujos de carbono muy diferentes.

Es terminología estándar de la literatura de humedales y turberas, donde el microrrelieve
determina directamente cuánta agua hay en superficie:

- **Hummock** — montículo/cojín elevado, normalmente más seco.
- **Hollow** — depresión entre montículos, más húmeda.
- **Pool** — charco o superficie con agua libre permanente.
- **Lawns** — superficie plana entre montículos y depresiones, húmeda pero sin agua libre.
- **Ditch** — canal o zanja (natural o de drenaje antrópico).

**Por qué importa:** en un páramo o humedal, dos cámaras a pocos metros pueden dar
lecturas de CO₂/CH₄ muy distintas solo por estar una en un *Hummock* (más seco, más CO₂)
y otra en un *Pool* (más húmedo, más CH₄) — sin esta etiqueta, esas diferencias se verían
como "ruido" en vez de explicarse por el microrrelieve.

## Referencias

- [Modelo de datos: cobertura de una unidad de muestreo](../arquitectura/modelo-cobertura.md) — cómo se modela esto en la plataforma Colflux.
- [Modelo de datos: microtopografía de una unidad de muestreo](../arquitectura/modelo-microtopografia.md) — cómo se modela esto en la plataforma Colflux.
- [¿Qué es un ecosistema?](que-es-un-ecosistema.md)
- [El estándar BADM/AmeriFlux](estandar-badm-ameriflux.md)
