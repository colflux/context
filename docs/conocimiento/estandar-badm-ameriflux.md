# El estándar BADM/AmeriFlux y los nombres de columna de la plantilla

> **Aviso:** la descripción general de AmeriFlux/BADM de este archivo reconstruye de memoria lo
> que se sabe del estándar — no fue verificada contra la documentación oficial completa. Sí se
> verificó puntualmente el vocabulario `DOM_DIST_MGMT` (ver sección abajo), confirmado contra la
> página oficial el 2026-11-09.

## El vocabulario `DOM_DIST_MGMT` (disturbio/manejo dominante)

Verificado contra [la página oficial de BADM Standards](https://ameriflux.lbl.gov/data/badm/badm-standards/DOM_DIST_MGMT)
(2026-11-09). 11 valores cerrados:

| Código (inglés) | Descripción oficial |
|---|---|
| Agriculture | Agricultural management of any kind, such as cultivation (including tillage, plowing, or discing), harvest, irrigation, pesticides, planting, or liming. |
| Drought | Prolonged water deficiency; hydrologic or climatic drought. |
| Fire | Wildfire or managed burns. |
| Forestry | Forest management such as logging of any kind, plantation planting, or herbicide application. |
| Grazing | Herbivory or browsing by mammals, managed or wild. |
| Hydrologic event | Drainage, persistent flooding, or chronic flooding. Does not include storm events or irrigation. |
| Land cover change | Land use and land cover change; invasion; woody or urban encroachment. |
| Pests and disease | Plant or soil damage from pests, insects, pathogens, blight, and other disease. |
| Storm or wind | Major storms including unusually high-precipitation and unusually high-wind events (hurricane, tornado, blizzard, hail, flooding from storm, etc). |
| Temperature extreme | Heat wave or freeze. |
| Undisturbed | No disturbance or management has occurred on the site. |

Este es el estándar detrás del catálogo `Disturbio` (ver
[Modelo de datos: disturbio de una unidad de muestreo](../arquitectura/modelo-disturbio.md)).

## ¿Qué es AmeriFlux?

**AmeriFlux** es la red de torres de covarianza de remolinos (*eddy covariance*, EC — ver
[Datos de torres EC](datos-torres-eddypro-reddyproc.md)) de las Américas. Es la contraparte
regional de **FLUXNET**, la red global de torres de flujo. Cada torre mide continuamente
flujos de CO₂, agua y energía entre un ecosistema y la atmósfera.

## ¿Qué es BADM?

**BADM** (*Biological, Ancillary, Disturbance, and Management data*) es el formato
estandarizado que usan AmeriFlux/FLUXNET para reportar los **metadatos del sitio** —
todo lo que no es el dato de flujo en sí, sino el contexto necesario para interpretarlo:
quién administra el sitio, dónde está, qué tipo de ecosistema es, qué disturbios o manejo
ha tenido, cómo se instrumentó.

Las siglas del nombre ya anticipan los grupos de variables: datos **biológicos**,
**ancilares** (contexto físico del sitio), de **disturbio** y de **manejo**.

## Referencias

- [Plantilla de carga/descarga: metadato y dato de CO2/CH4](../arquitectura/plantilla-metadato-dato-co2-camaras.md)
- [Modelo de datos: ecosistema/zonificación de un sitio](../arquitectura/modelo-ecosistema.md)
- [Datos de torres EC: de Eddypro a ReddyProc](datos-torres-eddypro-reddyproc.md)
