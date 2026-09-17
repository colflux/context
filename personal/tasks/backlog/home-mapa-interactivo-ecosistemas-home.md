# Crear mapa interactivo de ecosistemas estratégicos para el home

**Estado:** pendiente
**Creada:** 2026-09-16

## Objetivo

Implementar en el home del frontend de COLFLUX un mapa interactivo de Colombia que resalte los departamentos donde se recopilarán datos para la plataforma (región andina, Orinoquía y Amazonía), inspirado en el mapa publicado por Pesquisa Javeriana.

## Contexto

El artículo "La primera base de datos sobre carbono y humedales en Colombia está en desarrollo" de Pesquisa Javeriana incluye un mapa estático de Colombia con los departamentos donde trabajará COLFLUX resaltados en verde, y anotaciones de texto con flechas señalando tres regiones:

- Región andina: humedales en forma de lagos, lagunas y pantanos.
- Orinoquía: humedales que incluyen esteros y morichales.
- Amazonía: humedales en zonas de inundación aledañas a ríos.

La idea es tener una versión interactiva de este mapa (no necesariamente idéntica en diseño) en el home del frontend, que permita destacar visualmente los departamentos de trabajo y, potencialmente, mostrar información al pasar el cursor o hacer clic sobre cada región.

## Plan

- [ ] Definir qué departamentos exactos corresponden a cada región (andina, Orinoquía, Amazonía) según los datos del proyecto
- [ ] Elegir librería/enfoque para el mapa interactivo (ej. GeoJSON de departamentos de Colombia + librería de mapas tipo Leaflet, D3, o un componente de mapas ya usado en el proyecto)
- [ ] Diseñar la interacción: resaltado de departamentos en verde, tooltips o popups con la descripción de cada región al hacer hover/click
- [ ] Implementar el componente en el home
- [ ] Validar que se vea bien en mobile y desktop

## Entregables

(Link al resultado final, o una anotación de por qué se cerró sin uno.)

## Referencias

- Artículo con el mapa de referencia: https://www.javeriana.edu.co/pesquisa/carbono-cambio-climatico-colflux/

## Historial

| Fecha | Descripción |
|---|---|
| 2026-09-16 | Se crea la tarea a partir del mapa de referencia visto en el artículo de Pesquisa Javeriana. |
