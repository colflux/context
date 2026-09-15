# Pasar los datos locales de IDEAM al servidor

**Estado:** en progreso — 1/7 fuentes importadas, bloqueado por versión del backend remoto
**Creada:** 2026-09-07

## Objetivo

Migrar/sincronizar los datos de IDEAM (y otras fuentes) que actualmente están validados en local hacia el servidor de la plataforma Colflux, para que queden disponibles en el entorno productivo.

## Pasos

- [ ] Confirmar que la revisión local de los datos de IDEAM está completa (ver [[revisar-datos-ideam]])
- [ ] Definir el mecanismo de subida (script, endpoint de la API, carga manual, etc.)
- [ ] Ejecutar la carga de los datos al servidor
- [ ] Verificar que los datos quedaron íntegros y accesibles en el servidor

## Notas

Relacionado con [[revisar-datos-ideam]]. Depende de que esa tarea se cierre sin inconsistencias antes de subir los datos.

## Registro (2026-09-07)

Se ejecutó la carga vía API (`/api/proyectos/crear/`, `/api/fuentes-datos/crear/`, `/api/fuentes-datos/{id}/upload|carga/{carga}/mapeo|previsualizar|importar/` de `44.213.47.34`), replicando el mapeo de columnas exacto de cada carga ya importada en local.

**Resultado: solo SWAMP CH4 se importó completo** (1162 `SubmuestraGEI`, 147 `MuestraGEI`, 76 `UnidadMuestreo` nuevas, 3 `UnidadExperimental` nuevas). Las otras 6 fuentes (5 IDEAM + SWAMP Flujos CO2) quedaron creadas en el servidor pero sin datos importados — el bloqueo es de infraestructura del servidor remoto, no de los datos ni del mapeo. Detalle y plan de acción documentado en [[revisar-deploy-automatico-frontend]] (el backend remoto está desactualizado y el timeout de gunicorn es muy corto para archivos grandes).

**Para retomar:** una vez resueltos esos dos puntos, repetir la carga de las 6 fuentes pendientes (IDEAM CH4/CO2/COS/Biomasa/MOM, SWAMP Flujos CO2) con el mismo mecanismo.
