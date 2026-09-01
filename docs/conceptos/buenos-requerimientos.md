# ¿Cómo crear buenos requerimientos?

Transformar requerimientos vagos en especificaciones técnicas claras, medibles y ejecutables.

## 🚫 El problema: requerimientos vagos

**Ejemplos MALOS (lo que evitar):**

- ❌ "Hay que crear una interfaz interactiva"
- ❌ "Necesitamos gráficas dinámicas"
- ❌ "El sistema debe permitir análisis geoespacial"
- ❌ "Hacer reportes de carbono"
- ❌ "Integrar datos de agua y biodiversidad"

**¿Por qué son malos?**

- No especifican **QUÉ** tipo de gráficas
- No dicen **PARA QUÉ** usuarios
- No definen **CÓMO** se usan
- Generan interpretaciones diferentes en cada persona
- No se pueden estimar tiempos/esfuerzos
- No se pueden validar cuándo están "listos"

## ✅ La solución: requerimientos SMART

Un buen requerimiento debe tener estos elementos:

1️⃣ **Especificidad** (qué exactamente)
2️⃣ **Contexto** (por qué lo necesitamos)
3️⃣ **Criterios de aceptación** (cómo validar que está listo)
4️⃣ **Restricciones** (limitaciones técnicas/de negocio)
5️⃣ **Actor/usuario** (quién lo usa)

## Estructura estándar de un requerimiento

```
REQUERIMIENTO: [Código único]
Versión: 1.0 | Fecha: DD/MM/YYYY | Estado: Aprobado

TÍTULO:
[Descripción corta del requerimiento]

PRIORIDAD:
☐ Crítico (MVP - Entrega inicial en 20 días)
☐ Alto (Primera fase - Meses 1-3)
☐ Medio (Segunda fase - Meses 4-9)
☐ Bajo (Futuras mejoras)

DESCRIPCIÓN:
[Párrafo que explique QUÉ se necesita y POR QUÉ]

ACTOR/USUARIO:
[Quién usa esto: Investigador, Tomador de decisiones, Administrador, etc.]

CASOS DE USO:
1. [Usuario quiere hacer X] → [El sistema debe Y]
2. [Usuario quiere hacer X] → [El sistema debe Y]

CRITERIOS DE ACEPTACIÓN:
1. Dado [contexto], cuando [acción], entonces [resultado esperado]
2. Dado [contexto], cuando [acción], entonces [resultado esperado]
3. Dado [contexto], cuando [acción], entonces [resultado esperado]

RESTRICCIONES/CONSIDERACIONES:
- Técnicas: [Tecnologías, formatos, estándares]
- Negocio: [Cumplimiento normativo, presupuesto]
- Datos: [Volumen, frecuencia, fuentes]

DEPENDENCIAS:
- Requiere: [Otro requerimiento]
- Depende de: [Datos/sistemas externos]

PREGUNTAS/DUDAS:
[Temas pendientes de aclarar con el equipo]
```
