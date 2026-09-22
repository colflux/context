# Rediseñar el hero del home, agregar secciones (Sobre el proyecto, Explora COLFLUX, Aliados) y footer enriquecido

**Estado:** cerrada
**Creada:** 2026-09-21
**Cerrada:** 2026-09-21
**A cargo:** Viviana
**Sesión de Claude Code:** cerrada — retomar con una sesión nueva si hace falta continuar

## Objetivo

Rediseñar el hero del home del frontend (botones funcionales, indicadores reales) y agregar las secciones que Viviana pasó por captura de pantalla: "Sobre el proyecto" (¿Qué es COLFLUX?), "Explora COLFLUX" (3 tarjetas), "Aliados" (logos de instituciones) y un footer más completo (logo, enlaces, redes, contacto).

## Contexto

De paso, la tarea destapó un bloqueo de infraestructura no relacionado (el backend llevaba caído desde antes de esta sesión por un error de conexión a la base de datos de Lightsail) que había que resolver para poder mostrar indicadores reales en vez de datos inventados.

## Plan

- [x] Hero: botón amarillo "Reportar información" abre login si no hay sesión, navega a `/reportar` si la hay; botón "Explora los datos" habilitado hacia `/mapas`
- [x] Quitar iconos emoji y, luego, todo el bloque "Ciencia/Comunidad/Tecnología" y el subtítulo del hero (a pedido de Viviana, el hero quedó solo con título + botones)
- [x] Sección "Sobre el proyecto" (¿Qué es COLFLUX?) con foto real de campo
- [x] Sección "Explora COLFLUX" (Monitoreo/Comunidades/Datos)
- [x] Sección "Aliados": ubicar y recortar logos reales desde `context/files/Manual de identidad visual y logos/` (Aliados/ y PUJ/) + descargar el de "Ciencias" (Minciencias) desde su sitio oficial
- [x] Footer enriquecido: logo, enlaces de Plataforma, redes (Instagram + YouTube, con íconos SVG en vez de solo texto), botón de contacto + correo
- [x] Geoportal del hero (`EcosistemasMap`): contenedor más ancho que alto (antes seguía la silueta alargada de Colombia) mostrando el país completo, no recortado
- [x] Indicadores del hero (sitios/datos/usuarios/última medición) en formato tarjeta, con la fecha de última medición como nota secundaria (no como tarjeta grande) — conectados a datos reales, no inventados
- [x] **Bloqueante destapado:** diagnosticar por qué el backend no conecta a `colflux-DB` (Lightsail) — no era whitelist de IP (Lightsail "Public mode" no filtra por IP), sino que faltaba `sslmode=require` en la conexión de Django (el error "password authentication failed" era engañoso, el real era "no encryption"); además la contraseña en `backend/.env` estaba desactualizada, se corrigió con la vigente en la consola de Lightsail
- [x] Extender `/chart-data/` en el backend para exponer `total_sitios`, `total_mediciones`, `total_usuarios`, `ultima_medicion`
- [x] Conectar el frontend a ese endpoint (`useHomeStats` + `stats.service.ts`, React Query)
- [x] Hot-reload por polling en Docker/macOS (Vite no detectaba cambios en el bind mount)
- [x] Version bump a 1.3.1
- [x] Crear PRs en backend y frontend

## Entregables

**Backend:**
- [PR #20](https://github.com/colflux/backend/pull/20) — `chart-data` con indicadores nuevos, `sslmode=require`, y un commit aparte con trabajo de generalización de `resumen_geografico` a biomasa/COS que ya estaba sin commitear en el árbol de trabajo (ajeno a esta tarea, se incluyó a pedido de Viviana).

**Frontend:**
- [PR #25](https://github.com/colflux/frontend/pull/25) — rediseño del home (hero, secciones, footer, mapa, indicadores reales) en un commit, y un commit aparte con soporte de biomasa/COS en filtros/gráficas/geoportal que ya estaba sin commitear en el árbol (ajeno a esta tarea, incluido a pedido de Viviana).
- `frontend/src/assets/aliados/` — 8 logos: Ciencias (Minciencias, descargado de su sitio oficial), Javeriana, Universidad del Rosario, Universidad de Nariño, Alcaldía Mayor de Bogotá/Jardín Botánico (vienen en un solo lockup), IDEAM, CDA, Corporación Corredor del Jaguar.

## Pendientes (no bloqueantes)

- **Falta el logo de SGR** en Aliados: no se encontró una fuente oficial confiable descargable (el ícono de la captura de Viviana — figura de colores — no aparece en ningún repositorio de logos ni en el sitio de sgr.gov.co, que ya usa solo el branding genérico gov.co).
- **Footer "Síguenos"** solo tiene Instagram y YouTube — Facebook, LinkedIn y WhatsApp quedan pendientes si Viviana los pasa después.
- **CDA y Corredor del Jaguar** (logos de Aliados) traen fondo con degradado/sombra en el archivo original, no transparente limpio — se ven con un halo sutil en la franja; se podrían recortar si hace falta más nitidez.

## Referencias

- [[home-mapa-interactivo-ecosistemas-home]] — tarea previa que implementó `EcosistemasMap.tsx`; esta tarea ajustó su proporción para que se vea toda Colombia en un contenedor más ancho.
- [[db-aws]] — tarea previa de conexión a `colflux-DB`; esta sesión encontró y corrigió el motivo real de la caída del backend (SSL, no whitelist ni contraseña — aunque la contraseña también estaba desactualizada).
- `context/files/Manual de identidad visual y logos/` — fuente de los logos de aliados (carpetas `Aliados/` y `PUJ/`).

## Historial

| Fecha | Descripción |
|---|---|
| 2026-09-21 | Se rediseña el hero (botones funcionales, sin subtítulo ni bloque de features), se agregan las secciones Sobre el proyecto/Explora COLFLUX/Aliados y un footer enriquecido, siguiendo capturas de pantalla que pasó Viviana. Se ubican y recortan los logos de aliados desde el manual de identidad del repo `context`, y se descarga el de Minciencias ("Ciencias") de su sitio oficial; no se encuentra el de SGR. Al pedir levantar el backend en Docker para probar indicadores reales, se descubre que sigue caído desde antes de esta sesión por un error de conexión a `colflux-DB`; se diagnostica que la causa real es falta de `sslmode=require` (no whitelist de IP, que en Lightsail con "Public mode" no aplica) y una contraseña desactualizada en `.env`, se corrigen ambas y el backend levanta. Se extiende `/chart-data/` con los indicadores nuevos y se conecta el frontend. Se crean los PRs [backend#20](https://github.com/colflux/backend/pull/20) y [frontend#25](https://github.com/colflux/frontend/pull/25), cada uno con un commit aparte para trabajo ajeno a esta tarea (generalización de biomasa/COS) que estaba sin commitear en el árbol de trabajo de ambos repos y que Viviana pidió incluir. Se cierra la tarea. |
