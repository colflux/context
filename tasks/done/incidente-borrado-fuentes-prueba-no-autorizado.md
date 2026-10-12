# Incidente: borrado no autorizado de fuentes "prueba" (IDs 28-32)

**Estado:** cerrada — pérdida aceptada, eran datos de prueba
**Creada:** 2026-09-22
**A cargo:** Viviana
**Sesión de Claude Code:** https://claude.ai/code/session_01M7sC4mxBtg46EAE2Ns6Pky
**Participantes:** Viviana

## Objetivo

Decidir qué hacer respecto a 5 fuentes de datos del proyecto "Prueba"
(IDs 28, 29, 30, 31, 32) que se borraron de producción (`44.213.47.34`) sin
autorización, durante una sesión de borrado autorizado de otras 5 fuentes
(las de IDEAM: Biomasa 26, COS 25, CH4 22, CO2 24, MOM 27).

## Contexto

El alcance autorizado por Viviana para esa sesión de borrado vía navegador
era explícitamente **solo las 5 fuentes IDEAM**. Mientras se ejecutaba ese
borrado (usando Claude-in-Chrome), apareció un modal de confirmación
inesperado para borrar una fuente "prueba" — ese modal se canceló de
inmediato, sin confirmar. Sin embargo, al verificar el estado real vía
`curl http://44.213.47.34/api/fuentes-datos/` después, solo quedaban 2
fuentes en total (ambas SWAMP) — es decir, las 5 fuentes "prueba" ya habían
sido borradas antes de ese punto, por un mecanismo distinto al modal
cancelado.

**Causa raíz no determinada.** Hipótesis no confirmada: alguna carrera de
re-render/reutilización de referencia del DOM en la automatización del
navegador hizo que un clic en cola aterrizara sobre la fila equivocada
después de cada borrado exitoso.

Se reportó de inmediato y de forma transparente a Viviana, incluyendo que
las fuentes parecían ser datos de prueba de Milena Gonzalez. **Viviana no
ha respondido todavía** qué hacer al respecto (si tiene registro de qué
contenían esas fuentes, si vale la pena intentar recuperarlas, o si se
acepta la pérdida por ser datos de prueba).

## Plan

- [x] Preguntarle a Viviana cómo proceder
- [x] Viviana confirma que no hace falta investigar ni recuperar — se
      acepta la pérdida (datos de prueba, sin valor real)

## Entregables

Ninguno — se cierra sin acción, pérdida aceptada por ser datos de prueba
sin valor real. Queda documentado el mecanismo sospechoso (carrera de
re-render/referencia del DOM en la automatización de borrado vía
navegador) por si se repite el patrón en el futuro.

## Referencias

- `revisar-datos-ideam.md` — tarea relacionada que motivó el borrado
  autorizado de las 5 fuentes IDEAM (para volver a subirlas desde cero con
  correcciones)

## Historial

| Fecha | Descripción |
|---|---|
| 2026-09-22 | Durante el borrado autorizado de 5 fuentes IDEAM vía navegador en producción, se detecta que 5 fuentes adicionales del proyecto "Prueba" (28-32) fueron borradas sin autorización. Se reporta de inmediato a Viviana, se detiene cualquier acción destructiva adicional, y se pregunta cómo proceder. |
| 2026-09-23 | Viviana confirma que está todo bien y que se puede cerrar la tarea — se acepta la pérdida sin investigación adicional ni intento de recuperación. |
