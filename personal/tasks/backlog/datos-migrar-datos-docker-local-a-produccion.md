# Migrar los datos del Postgres local de Docker a producción (colflux-DB)

**Estado:** completada (excepto SWAMP CH4, dado por perdido a pedido del usuario)
**Creada:** 2026-09-15

## Objetivo

Subir a producción (`dbCOLFLUX`, RDS `colflux-DB`) todos los datos que quedaron
"huérfanos" en el volumen de Docker Postgres local de este equipo
(`backend_postgres_data`), que nunca se migraron cuando el backend se
reconectó de ese Postgres local a RDS (ver [[conectar-base-datos-aws]]).

## Contexto

`conectar-base-datos-aws.md` documentó cómo se conectó el backend a RDS y
cómo se **eliminó** el Postgres local de Docker Compose (servicio `db`) tanto
en el `docker-compose.yml` como en el servidor de producción — pero esa tarea
nunca migró los *datos* que había en esos Postgres locales, solo cambió la
conexión hacia adelante. El volumen de este equipo (`backend_postgres_data`,
creado 2026-07-10) sigue existiendo en disco y todavía tiene datos reales.

### Diagnóstico (2026-09-15)

Se levantó temporalmente un contenedor `postgis/postgis:16-3.4-alpine` apuntando
al volumen `backend_postgres_data` (sin tocar producción) para inventariar
filas por tabla, y se comparó contra `dbCOLFLUX` real (vía
`docker compose run --rm web python manage.py shell`, usando la `DATABASE_URL`
ya configurada en `.env`, sin exponer la contraseña en ningún comando).

| Tabla | Local (Docker) | Producción (RDS) | Estado |
|---|---:|---:|---|
| `app_departamento` | 33 | 33 | ✅ ya migrado |
| `app_municipio` | 1.122 | 1.122 | ✅ ya migrado |
| `app_vereda` | **550.460** | **0** | 🔴 falta migrar — el hueco más grande |
| `app_sitio` | 113 | 0 | 🔴 falta migrar |
| `app_parcela` | 422 | 0 | 🔴 falta migrar |
| `app_proyecto` | 1 | 0 | 🔴 falta migrar |
| `app_fuentedatos` | 7 | 0 | 🔴 falta migrar |
| `app_cargaarchivo` | 55 | 0 | 🔴 falta migrar |
| `app_muestragei` | 605 | 0 | 🔴 falta migrar |
| `app_submuestragei` | 7.048 | 0 | 🔴 falta migrar |
| `app_muestrabiomasa` | 646 | 0 | 🔴 falta migrar |
| `app_muestramom` | 1.176 | 0 | 🔴 falta migrar |
| `app_submuestrasuelo` | 1.795 | 0 | 🔴 falta migrar |
| `app_unidadmuestreo` | 563 | 0 | 🔴 falta migrar |
| `app_unidadexperimental` | 17 | 0 | 🔴 falta migrar |
| `app_muestraambiental` | 9.245 | 0 | 🔴 falta migrar |
| `app_mapeocolumna` | 2.500 | 0 | 🔴 falta migrar |
| `app_cobertura` | 98 | 6 | 🔴 falta migrar (prod solo tiene el catálogo semilla) |
| `app_usuario` | 0 | 3 | (prod tiene sus propios usuarios reales, no tocar) |

**Hallazgo importante — posible pérdida de datos ya ocurrida:** según
[[migrar-etl-datos-a-frontend]] / la tarea de subir IDEAM al servidor, en
2026-09-07 ya se había importado con éxito "SWAMP CH4" (1.162
`SubmuestraGEI`, 147 `MuestraGEI`, etc.) **vía API contra el servidor de
producción** (`44.213.47.34`) — en ese momento el servidor todavía corría su
propio Postgres local en Docker (antes del cambio a RDS). Cuando
`conectar-base-datos-aws.md` "limpió el contenedor/volumen viejo en el
servidor" como parte del cambio a RDS, **no hay registro de que se haya hecho
un `pg_dump` de ese volumen del servidor antes de borrarlo**. Es decir: los
datos de SWAMP CH4 subidos el 2026-09-07 probablemente se perdieron en esa
limpieza y no están ni en producción ni en este volumen local (este volumen
es de la máquina de desarrollo, no del servidor). **Pendiente confirmar si
existe algún backup del volumen del servidor antes de darlo por perdido.**

### Complicación de esquema (no es un dump/restore trivial)

El esquema de `app_rolusuario`/`app_usuariorol` cambió entre este volumen
local y producción (ver el rediseño de roles en [[conectar-base-datos-aws]]:
roles M2M → `Usuario.nivel` en cascada). Un `pg_dump`/`pg_restore` binario de
tabla por tabla puede chocar con migraciones más nuevas ya aplicadas en
`dbCOLFLUX`. La migración de datos de las tablas geográficas/GEI (que no
cambiaron de esquema) es segura por `pg_dump --table=... | psql`, pero
`app_usuario` y las tablas de roles **no deben tocarse** con este mecanismo
(prod ya tiene su propio estado de usuarios correcto).

## Resolución (2026-09-15)

El usuario confirmó: dar por perdidos los datos de SWAMP CH4 (punto pendiente
del hallazgo anterior) y migrar todo lo demás, excluyendo explícitamente
usuarios y roles.

Se encontró un comando de gestión ya escrito pero sin commitear
(`app/management/commands/migrar_datos_locales.py`, de una sesión anterior no
documentada) que automatizaba exactamente esta migración tabla por tabla. Se
auditó antes de correrlo y se le encontraron **dos problemas de seguridad
graves** que se corrigieron antes de ejecutar:

1. **Incluía `Institucion` en la migración con `TRUNCATE ... CASCADE`.**
   Producción ya tenía 1 fila real en `app_institucion` (creada después de
   que el volumen local quedara huérfano) y `Usuario.institucion_id`
   referencia esa tabla — un `TRUNCATE CASCADE` sobre `Institucion` habría
   **borrado en cascada los 3 usuarios reales de producción** (incluyendo
   los superusuarios de login). Se quitó `Institucion` de la migración por
   completo (local no tenía ninguna fila que aportar de todas formas).
2. **`TRUNCATE ... CASCADE` en general era peligroso** porque producción ya
   tiene tablas nuevas que no existían en el snapshot local
   (`DocumentoConocimiento`, `MedicionRapidaChat`, `SolicitudNivel`,
   `RegistroChatIA`, etc.), algunas con FK hacia tablas que sí se iban a
   truncar (p. ej. `Sitio`). Se reemplazó el `TRUNCATE` por una verificación
   de que la tabla destino esté vacía antes de cargar (si no lo está, el
   comando aborta en vez de truncar a ciegas). Se verificó con conteos
   exactos que todas las tablas de contenido estaban en 0 en `dbCOLFLUX`
   antes de correr la migración real.
3. Se agregó además un reseteo de secuencia (`setval`) después de cada
   carga, porque insertar con PKs explícitos deja la secuencia
   autoincremental desalineada (el próximo `INSERT` sin PK explícito
   habría chocado con un id ya usado).

**Ejecución:** `docker compose run --rm web python manage.py migrar_datos_locales`,
apuntando el origen a un contenedor temporal (`postgis/postgis:16-3.4-alpine`
sobre el volumen `backend_postgres_data`) expuesto en
`host.docker.internal:55432`. Corrida completa sin errores, verificada
tabla por tabla (conteo origen == conteo destino en cada paso):

| Tabla | Filas migradas |
|---|---:|
| `Vereda` | 550.460 |
| `MuestraAmbiental` | 9.245 |
| `AplicacionRegla` | 9.702 |
| `SubmuestraGEI` | 7.048 |
| `MapeoColumna` | 2.500 |
| `SubmuestraSuelo` | 1.795 |
| `MuestraMOM` | 1.176 |
| `UnidadMuestreo` | 563 |
| `MuestraBiomasa` | 646 |
| `Parcela` | 422 |
| `MuestraGEI` | 605 |
| `Sitio` | 113 |
| `Cobertura` | 98 |
| `CargaArchivo` | 55 |
| `UnidadExperimental` | 21 |
| `FuenteDatos` | 7 |
| `Disturbio` | 6 |
| `ReglaAutollenado` | 2 |
| `Proyecto` | 2 |
| (resto: `Vegetacion`, `Transecto`, `MonitoreoParcela`, etc.) | 0 (no tenían datos) |

`FuenteDatos.reportador_id` quedó en `NULL` para las 7 filas migradas (no se
migran usuarios; si se quiere reasignar el responsable original, es una
edición manual posterior). Post-migración se verificó que `app_usuario` (3)
y `app_institucion` (1) en producción quedaron intactos.

El comando (`migrar_datos_locales.py`) queda sin commitear en el repo del
backend — es de un solo uso, se puede borrar ahora que la migración está
verificada, o commitear como referencia histórica.

## Bug encontrado y corregido tras la migración (2026-09-15, sesión posterior)

El usuario reportó que el mapa de veredas/departamentos no se veía en
`/mapas` en producción. Diagnóstico: `Departamento` (33 filas) y `Municipio`
(1.122 filas) ya existían en `dbCOLFLUX` *antes* de esta tarea (por eso la
migración los saltó — los conteos ya coincidían), pero **nunca se les cargó
la columna `geom`** (0/33 y 0/1122 con geometría). El volumen local sí tenía
esa geometría completa (33/33 y 1121/1122). `Vereda` no tuvo este problema
porque el paso de migración la cargó explícitamente con `geom` incluido.

El frontend arma las opciones de los selects "Departamento"/"Municipio"/
"Vereda" y el choropleth del mapa a partir de
`GET /api/geo/resumen/?nivel=...` (`app/api/geo/views.py:resumen_geografico`),
que solo agrega geografías con al menos una `SubmuestraGEI` enlazada — y
devuelve su `geometry` desde `departamento.geom`/`municipio.geom`/`vereda.geom`.
Con `geom=None`, el mapa no podía dibujar el polígono aunque el dropdown en
sí sí tuviera la fila.

**Corrección aplicada** (confirmada explícitamente por el usuario antes de
escribir en producción): backfill de una sola columna, cruzando por
`codigo_dane` entre el volumen local (origen) y `dbCOLFLUX` — no toca ninguna
otra columna, no inserta/borra filas, no toca IDs ni FKs. Resultado:
33/33 departamentos y 1.121/1.122 municipios quedaron con `geom`. Verificado
llamando directo a `resumen_geografico(nivel=departamento)`: ya devuelve
Cundinamarca y Caldas (los dos con mediciones reales) con geometría no nula.

## Plan

- [x] Levantar el volumen local viejo en un contenedor temporal y confirmar qué tiene
- [x] Comparar tabla por tabla contra `dbCOLFLUX` (producción)
- [x] Confirmar con el usuario: SWAMP CH4 se da por perdido, migrar todo lo demás excluyendo usuarios/roles
- [x] Auditar y corregir el comando `migrar_datos_locales.py` (quitar `Institucion`, quitar `TRUNCATE CASCADE`, agregar reseteo de secuencia)
- [x] Ejecutar la migración completa y verificar conteos tabla por tabla
- [x] Verificar que `app_usuario`/`app_institucion` no se tocaron
- [x] Diagnosticar por qué el mapa de veredas/departamentos no se veía en producción tras la migración (geometría faltante en `Departamento`/`Municipio`, no en `Vereda`)
- [x] Backfill de `geom` en `Departamento`/`Municipio` cruzando por `codigo_dane`, confirmado con el usuario antes de escribir en producción
- [ ] Verificar visualmente en el navegador (`44.213.47.34/mapas`) que el mapa ya pinta departamentos/veredas correctamente
- [ ] Decidir si el volumen local (`backend_postgres_data`) se conserva como backup o se elimina, ahora que la migración está verificada
- [ ] Decidir si `migrar_datos_locales.py` se commitea (como referencia histórica) o se borra del repo del backend
- [ ] Revisar/reasignar manualmente `FuenteDatos.reportador_id` (quedó en NULL para las 7 fuentes migradas)
- [ ] El municipio sin geometría (1/1122, no cruzó por `codigo_dane`) queda sin identificar — revisar si importa (probablemente un caso de código DANE inconsistente entre fuentes)

## Referencias

- [[conectar-base-datos-aws]] — quitó el Postgres local sin migrar sus datos; causa raíz de esta tarea
- [[subir-datos-ideam-servidor]] — la carga de SWAMP CH4 del 2026-09-07 que probablemente se perdió
- Volumen Docker local: `backend_postgres_data` (creado 2026-07-10, `postgis/postgis:16-3.4-alpine`)
- `~/colflux/backend/.env` — `DATABASE_URL` de producción (`dbCOLFLUX`)

## Historial

| Fecha | Descripción |
|---|---|
| 2026-09-15 | Se crea la tarea a partir de una pregunta del usuario sobre migrar veredas/municipios. Se descubre que municipios/departamentos ya estaban migrados, pero veredas (550.460 filas) y toda la data GEI/ETL del volumen local nunca se subieron a producción. Se identifica además un riesgo de pérdida de datos: el volumen Postgres del servidor (distinto de este, borrado al migrar a RDS) pudo haberse eliminado sin backup, con la carga de SWAMP CH4 del 2026-09-07 adentro. |
