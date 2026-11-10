# ¿Qué es un disturbio?

Un **disturbio** (en inglés *disturbance*) es cualquier evento, puntual o prolongado, que
altera la estructura de un ecosistema, una comunidad o una población — cambiando la
disponibilidad de recursos (luz, agua, nutrientes, espacio) o la estructura física del
ambiente. No es necesariamente algo "malo" en sentido absoluto: muchos ecosistemas
tienen regímenes de disturbio natural a los que están adaptados (ej. el fuego en
sabanas), pero sí es siempre un evento que saca al ecosistema de su trayectoria previa.

## Tipos de disturbio

- **Naturales** — incendios (de origen natural), inundaciones, deslizamientos,
  vendavales, plagas, erupciones, heladas extremas.
- **Antrópicos** (de origen humano) — tala, quema controlada o no controlada, pastoreo,
  cultivo, drenaje de humedales, construcción de infraestructura, minería.

Un mismo sitio puede tener varios disturbios registrados a lo largo del tiempo — un
historial, no un evento único — y más de uno puede estar activo o reciente a la vez.

## Por qué importa para el monitoreo de carbono

El disturbio es central para interpretar los datos de flujo y de stocks de carbono que
mide Colflux:

- Cambia la cantidad de carbono que un ecosistema puede almacenar o liberar (ej. un
  incendio libera carbono acumulado en biomasa y suelo; el fin de un disturbio da paso a
  una recuperación que vuelve a capturar carbono con el tiempo).
- Permite interpretar correctamente por qué un sitio mide flujos o reservas distintas a
  las esperadas para su tipo de ecosistema — sin ese contexto, una diferencia real
  (causada por disturbio) podría leerse por error como una falla de medición.
- Define el **estado de conservación** del sitio (qué tan natural, seminatural, manejado,
  en plantación, o artificial/urbano está) — una de las variables que Colflux reporta por
  sitio.

## Qué datos se reportan sobre el disturbio de un sitio

Para cada evento de disturbio registrado se busca capturar: **qué tipo** de disturbio fue,
**cuándo empezó y/o hace cuántos años ocurrió**, **hace cuánto terminó** (si ya terminó),
el **estado de conservación** resultante, y si el sitio tiene alguna **figura de
protección legal** (reserva, parque nacional, etc.) que condicione o limite el disturbio.
Cuando hay más de un disturbio registrado en un mismo sitio, interesa además saber cuál
es el **dominante** — el que más influye en el estado actual del sitio.

## Referencias

- [Modelo de datos: disturbio](../arquitectura/modelo-disturbio.md) — cómo se modela esto en la plataforma Colflux (pendiente de documentar).
