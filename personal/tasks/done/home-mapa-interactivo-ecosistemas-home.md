# Crear mapa interactivo de ecosistemas estratégicos para el home

**Estado:** cerrada
**Creada:** 2026-09-16
**Cerrada:** 2026-09-20

## Objetivo

Implementar en el home del frontend de COLFLUX un mapa interactivo de Colombia que resalte los departamentos donde se recopilarán datos para la plataforma (región andina, Orinoquía y Amazonía), inspirado en el mapa publicado por Pesquisa Javeriana.

## Contexto

El artículo "La primera base de datos sobre carbono y humedales en Colombia está en desarrollo" de Pesquisa Javeriana incluye un mapa estático de Colombia con los departamentos donde trabajará COLFLUX resaltados en verde, y anotaciones de texto con flechas señalando tres regiones:

- Región andina: humedales en forma de lagos, lagunas y pantanos.
- Orinoquía: humedales que incluyen esteros y morichales.
- Amazonía: humedales en zonas de inundación aledañas a ríos.

La idea es tener una versión interactiva de este mapa (no necesariamente idéntica en diseño) en el home del frontend, que permita destacar visualmente los departamentos de trabajo y, potencialmente, mostrar información al pasar el cursor o hacer clic sobre cada región.

## Plan

- [x] Definir qué departamentos exactos corresponden a cada región (andina,
      Orinoquía, Amazonía) según los datos del proyecto — se usó el mapeo
      oficial de `backend/app/migrations/0019_seed_regiones_departamentos.py`
      (regiones `Andes`, `Orinoquia`, `Amazonas`), no el catálogo completo de
      6 regiones DANE sino solo estas 3 (Caribe/Pacífico/Insular quedan fuera,
      como en el mapa de referencia)
- [x] Elegir librería/enfoque para el mapa interactivo — nada de
      `maplibre-gl` (eso es para el mapa "grande" de `/mapas`, ya lo tiene
      `GeoMap.tsx`). Para el home se generaron paths SVG estáticos a partir
      de `backend/data/departamentos.gpkg` (límites oficiales DANE) con un
      script Python (`geopandas`/`shapely`, geometría simplificada,
      proyección equirectangular con corrección de latitud), sin agregar
      dependencias nuevas al frontend
- [x] Diseñar la interacción: departamentos de las 3 regiones en verde
      (`brand-green`), resto atenuados; anotaciones fijas (texto + flecha
      curva, igual que el mapa de Datawrapper del artículo); al hacer click
      en un departamento resaltado se abre una tarjeta con su nombre, su
      región y una foto (misma interacción que el mapa de referencia, que
      muestra una foto de Casanare al hacer click)
- [x] Implementar el componente en el home — `EcosistemasMap.tsx`, usado en
      `Home.tsx` reemplazando el placeholder de emojis en el hero
- [x] Validar que se vea bien en mobile y desktop — probado en el navegador
      en desktop (claro/oscuro, hover funcionando); en mobile se validó por
      CSS (el contenedor está dentro del grid `md:grid-cols-2` que colapsa a
      una columna, y el `<svg>` usa `viewBox` con `w-full h-full`, así que
      siempre se ajusta al ancho disponible) — no se pudo probar con resize
      real de ventana porque la extensión de Chrome se desconectó a mitad de
      la verificación

## Entregables

- `frontend/src/assets/data/colombiaDepartamentos.ts` — paths SVG de los 33
  departamentos (generados desde `departamentos.gpkg`, no se commitea el
  script porque es un one-off, pero queda documentado acá: `geopandas`,
  `simplify(0.015)`, proyección equirectangular con corrección
  `cos(lat0)`, normalizado a `viewBox="0 0 600 760"`)
- `frontend/src/components/home/EcosistemasMap.tsx` — tarjeta "Geoportal
  COLFLUX": header simple, mapa grande con anotaciones fijas (texto +
  flecha curva) para las 3 regiones, click en un departamento resaltado
  abre una tarjeta con foto (rota entre 4 fotos reales de campo, ver
  abajo), y footer con CTA "Abrir geoportal" a `/mapas`
- `frontend/src/assets/ecosistemas/` — fotos por departamento pasadas por
  Viviana (Amazonas, Putumayo, Guainía, Guaviare, Casanare, Boyacá,
  Cundinamarca) + `paramo-{1..4}.jpg` de
  `PrototipoCOLFLUX/Frontend-Colflux/assets/img/ecosistemas/` como
  respaldo genérico para los departamentos sin foto propia (Meta,
  Vichada, Bogotá D.C.). La foto de Casanare es de Dreamstime (banco de
  imágenes comercial) — pendiente confirmar licencia o reemplazarla si
  esto sale a producción pública.
- `frontend/src/pages/Home.tsx` — integrado en el hero, columna del mapa
  ensanchada (`grid-cols-[1fr_1.2fr]`) para que el mapa se vea más grande
- Lista final de departamentos resaltados (más acotada que el catálogo
  completo de regiones): andina = Bogotá D.C./Cundinamarca, Boyacá;
  Orinoquía = Meta, Casanare, Vichada; Amazonía = Amazonas, Putumayo,
  Guainía, Guaviare (Antioquia y Caquetá se quitaron a pedido de
  Viviana; Guaviare se agregó después)
- PR: https://github.com/colflux/frontend/pull/21 (rama
  `feat/home-mapa-ecosistemas`, basada en `main`, no en
  `feat/reportes-modulo-graficas` que era la rama activa en el working
  directory pero tenía trabajo ajeno sin commitear)

## Referencias

- Artículo con el mapa de referencia: https://www.javeriana.edu.co/pesquisa/carbono-cambio-climatico-colflux/

## Historial

| Fecha | Descripción |
|---|---|
| 2026-09-16 | Se crea la tarea a partir del mapa de referencia visto en el artículo de Pesquisa Javeriana. |
| 2026-09-18 | Se abre el navegador para revisar el mapa real del artículo (era un mapa de Datawrapper, no una imagen estática): coroplético de departamentos en verde con 3 anotaciones (andina, Orinoquía, Amazonía). Se confirma con Viviana que el home necesita una versión mucho más liviana que `GeoMap.tsx` (que usa `maplibre-gl` y datos en vivo del backend), no ese componente reutilizado. Se implementa `EcosistemasMap.tsx` (SVG estático, sin librerías de mapas) y se integra en `Home.tsx`. |
| 2026-09-18 | Viviana pasa un mockup ("Geoportal COLFLUX": header con filtros Todos/Páramos/Humedales, controles +/− de zoom, footer con CTA). Se rediseña el componente para calzar con el mockup: filtros funcionales (Páramos → solo región andina, Humedales → Orinoquía + Amazonía), anotaciones con flecha curva estáticas (antes eran tooltip on-hover), footer con botón "Abrir geoportal" a `/mapas`. Se detecta y excluye del mapa el archipiélago de San Andrés (código DANE 88): al ser geográficamente aislado al noroeste, se veía como un punto suelto cerca del texto de la anotación andina; se regeneran los paths SVG sin ese departamento para que el continente aproveche mejor el `viewBox`. Verificado en navegador en claro/oscuro. |
| 2026-09-18 | Viviana pide quitar los botones de filtro (Todos/Páramos/Humedales) y agrandar el mapa; también cuestiona si tiene sentido que los controles +/− decorativos "funcionen" — se quitan ambos (filtros y controles +/−) por ser UI que no hacía nada real, y se ensancha la columna del mapa en `Home.tsx`. Viviana además señala que en el mapa del artículo, al hacer click en un departamento (ej. Casanare) aparece una tarjeta con una foto — se vuelve a probar en el navegador con varios clicks y se confirma: sí es un comportamiento real del mapa de Datawrapper (antes no se había detectado). Como el proyecto no tiene fotos reales por departamento (`Sitio` no guarda fotos), se ofrecen opciones; Viviana elige reusar 4 fotos de campo reales de páramo que estaban en `PrototipoCOLFLUX/Frontend-Colflux/assets/img/ecosistemas/` en vez del ícono abstracto `hero.png`. Se implementa el click → tarjeta con foto + nombre de departamento + región, con resaltado de borde y apertura hacia el lado con más espacio. Verificado en claro/oscuro. |
| 2026-09-18/19 | Viviana acota la lista de departamentos por región a una más específica (ej. solo Bogotá/Cundinamarca/Boyacá en andina, sin todo el catálogo de la región Andes), y luego pide quitar Antioquia y Caquetá que se habían colado. Viviana empieza a pasar fotos reales por departamento una por una (Amazonas, Putumayo, Guainía, Guaviare, Casanare, Boyacá, Cundinamarca); se agregan como mapeo `FOTOS_POR_DEPARTAMENTO` con fallback a las fotos de páramo para los departamentos sin foto propia (Meta, Vichada, Bogotá D.C.). Se avisa a Viviana que la foto de Casanare es de Dreamstime (stock comercial, no libre de derechos) y que Guaviare no estaba en la lista de resaltados pese a tener foto — decide agregar Guaviare a Amazonía. |
| 2026-09-20 | Viviana pide crear rama y PR. Se detecta que el working directory está parado en `feat/reportes-modulo-graficas` con cambios sin commitear ajenos a esta tarea (login, auth, reportes) — se crea un git worktree aparte basado en `main` para no mezclar ese trabajo, y se abre el PR #21 (`feat/home-mapa-ecosistemas` → `main`) solo con los archivos del mapa. El PR queda con conflicto porque `main` avanzó (se había mergeado el módulo de reportes, que también tocaba `Home.tsx` con el gate de rol `reportador`) — se hace rebase sobre `origin/main`, se resuelve el único conflicto (dos imports nuevos en la misma línea) y se hace push --force-with-lease. Se cierra la tarea. |
