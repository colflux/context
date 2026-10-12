# F60 — Validación colaborativa de términos (semáforo de aceptación)

**Categoría:** Addendum — hallazgos del prototipo

## Objetivo

Dar a la comunidad un mecanismo para votar qué tan acertada es una definición del
diccionario/wiki, resumido en un semáforo de consenso.

## Contexto

Mecanismo de votación (0-100%) con un semáforo (rojo ≤30% / amarillo 31-70% / verde
≥71% / gris sin votos) calculado como promedio de todas las valoraciones recibidas por
término. No debe confundirse con el "semáforo de calidad" de
[F11](../datos-y-carga/f11-validacion-semaforo-calidad.md), que evalúa la confiabilidad
de un **dato medido**, no de una **definición del diccionario**. Tampoco es exactamente
[F25](../wiki-y-conocimiento/f25-wiki-colaborativa-proyecto.md) (wiki colaborativa), que
solo contempla historial de versiones y comentarios — la votación agregada es un
mecanismo distinto de consenso comunitario.

## Qué hay

No se encontró evidencia de implementación, ni en el prototipo ni en el backend/frontend
vigentes — es una capacidad identificada como hueco en el addendum, no prototipada aún.

## Qué hace falta

- ¿Quién puede votar (cualquier visitante o solo usuarios registrados)?
- ¿Qué pasa cuando un término llega a rojo — se revisa, se retira, se marca como
  controvertido?
- Diseño del modelo de datos y de la UI de votación (no existe ni como prototipo).
