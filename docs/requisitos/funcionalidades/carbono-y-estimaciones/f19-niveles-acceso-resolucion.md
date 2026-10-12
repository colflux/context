# F19 — Niveles de acceso graduados por resolución del dato

**Categoría:** Carbono y Estimaciones

## Objetivo

Que usuarios acreditados accedan a mayor resolución temporal y espacial que un usuario
general, distinto del RBAC por pantalla/permiso ([F57](../acceso-a-plataforma/f57-rbac-control-acceso-roles.md)).

## Contexto

No es "quién puede ver esta pantalla", sino "qué tan detallado es el dato que se le
sirve a cada quien" — p. ej. series diarias para un investigador acreditado vs.
agregados mensuales para un ciudadano.

## Qué hay

Existe un sistema de niveles (`Usuario.NIVEL_CHOICES`: ciudadano/investigador/
reportador/admin, `backend/app/models/datos.py:33-38`) con jerarquía en cascada
documentada explícitamente como permisos por acción ("investigador = además puede
descargar datos; reportador = además puede subir datos"), aplicado vía
`requiere_nivel`/`EscrituraRequiereNivel` (`backend/app/api/permisos.py`). El frontend
tiene `SolicitarNivelModal.tsx` y `SolicitudesNivelAdmin.tsx` para solicitar/aprobar
subir de nivel.

## Qué hace falta

Este es exactamente el RBAC por pantalla/permiso que el catálogo pide distinguir de
F19: no hay ninguna lógica que gradúe la **resolución** del dato servido (p. ej.
truncar precisión temporal/espacial, degradar a centroides o agregados mensuales para
"ciudadano" vs. series diarias/puntuales para "investigador acreditado"). Todos los
endpoints de series/geo devuelven la misma resolución a cualquier usuario; solo cambia
si puede o no descargar/escribir.
