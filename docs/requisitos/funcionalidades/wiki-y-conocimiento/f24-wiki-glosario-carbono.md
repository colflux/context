# F24 — Wiki de conocimiento sobre carbono + glosario no técnico

**Categoría:** Wiki y Conocimiento

## Objetivo

Explicar a ciudadanos qué es el carbono, su ciclo, estimaciones, mapa nacional,
reservas y factores de emisión, con un diccionario que traduce términos técnicos a
lenguaje simple.

## Contexto

El catálogo original dejó pendiente: ¿página aparte, tooltips inline, o buscador propio
del glosario?

## Qué hay

En el frontend actual, `frontend/src/pages/Educacion.tsx` tiene una página "Aprende y
participa" con pestañas estáticas (Recursos, Cursos, Videos, Publicaciones, Encuentros)
y tarjetas hardcodeadas sobre carbono/ecosistemas (ej. "¿Qué es el carbono y por qué es
importante?"), pero sin contenido real ni backend — son datos mock en el componente. En
`PrototipoCOLFLUX` (no vigente) sí existe algo más cercano a un glosario:
`Frontend-Colflux/diccionario.html` + `diccionario.js` con buscador y filtro por
categoría, consumiendo un endpoint Java `/api/wiki` (`WikiController.java`,
`WikiService.java`) que lee de `wiki_colflux.csv`; ese CSV trae observaciones
ecológicas y reglas cuantitativas (ej. "Olor a pantano" → variable Flujo CH4), más
parecido a un glosario de campo (ver [F59](../addendum-prototipo/f59-diccionario-campo-inverso.md))
que a contenido ciudadano, y el `diccionario.csv` asociado está vacío.

## Qué hace falta

- Todo el backend actual: no tiene modelo ni endpoint de wiki ni glosario.
- El contenido de `Educacion.tsx` es estático y de ejemplo, no editorial real.
- Sigue sin resolver si será página aparte, tooltips inline o buscador propio — el
  prototipo sugiere un patrón de buscador+filtro que podría servir de referencia, pero
  no es código vigente ni cubre el enfoque ciudadano (ciclo del carbono, mapa nacional,
  reservas, factores de emisión).
