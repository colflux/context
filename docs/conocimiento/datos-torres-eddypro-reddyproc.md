# Datos de torres EC: de Eddypro a ReddyProc

## ¿Qué es una torre EC y cómo funciona?

Una torre de **covarianza de remolinos** (*eddy covariance*, EC) es un mástil instalado en el ecosistema, con sensores en la punta por encima del dosel vegetal (del pasto, del bosque, de la vegetación de páramo/humedal según el sitio). A diferencia de las cámaras de gases manuales (ver la sección "Flujos" en [¿Cómo se mide el carbono?](como-se-mide-el-carbono.md)), que se usan puntualmente en campo, una torre EC mide **de forma continua, 24/7**, sin que alguien tenga que estar presente tomando la muestra.

**Qué sensores lleva:**

- Un **anemómetro sónico 3D**, que mide la velocidad del viento en las tres direcciones (arriba/abajo, norte/sur, este/oeste) muchas veces por segundo (10-20 Hz).
- Un **analizador de gases** (infrarrojo, de respuesta rápida) que mide la concentración de CO₂, CH₄ y/o vapor de agua en el aire, a esa misma velocidad.

**La idea física detrás de la medición:** el aire no sube y baja de forma uniforme — se mueve en remolinos turbulentos ("eddies"). Cuando un remolino sube, puede traer aire con más o menos concentración del gas que cuando baja. Midiendo muchas veces por segundo tanto la velocidad vertical del viento como la concentración del gas, y calculando la **covarianza** entre ambas series (de ahí el nombre del método), se obtiene el flujo neto de ese gas entre el ecosistema y la atmósfera — sin necesidad de encerrar nada en una cámara.

- Si predominan los remolinos que suben con más gas que los que bajan, el ecosistema está **emitiendo** ese gas hacia la atmósfera (flujo positivo).
- Si predominan los que bajan con más gas que los que suben, el ecosistema lo está **absorbiendo/secuestrando** (flujo negativo).

Es el mismo concepto de "flujo positivo/negativo" que ya se explica para cámaras en [¿Cómo se mide el carbono?](como-se-mide-el-carbono.md) — la diferencia es el método: una torre EC lo hace de forma continua y automática, sobre toda un área (su "huella" o *footprint*, ver más abajo), en vez de puntualmente sobre un punto específico con una cámara.

**Por qué se necesita tanto procesamiento después:** medir 10-20 veces por segundo durante meses genera una cantidad enorme de datos crudos (viento + gas), que nadie puede interpretar directamente fila por fila. Por eso ese dato crudo pasa por dos etapas de software, descritas abajo, antes de convertirse en un flujo interpretable (un solo valor de flujo cada 30 minutos).

## 1. Eddypro — preprocesamiento

[Eddypro](https://www.licor.com/env/support/EddyPro/software.html) toma los datos crudos de alta frecuencia (viento 3D + concentración de gases) y calcula, para cada ventana de 30 minutos, el flujo promedio aplicando las correcciones estándar de la literatura EC (rotación de coordenadas, corrección espectral, WPL, etc.). La salida típica es un CSV "full output" con una fila por media hora y columnas agrupadas así:

| Grupo | Qué contiene |
|---|---|
| `file_info` | Fecha, hora, día juliano, si es de día/noche, registros usados |
| `corrected_fluxes_and_quality_flags` | Los flujos ya corregidos: `co2_flux`, `ch4_flux`, `h2o_flux`, `H` (calor sensible), `LE` (calor latente), `Tau` (esfuerzo cortante), cada uno con su flag de calidad `qc_*` (0=bueno, 1=aceptable, 2=descartar) y su error aleatorio `rand_err_*` |
| `storage_fluxes` / `vertical_advection_fluxes` | Términos de almacenamiento y advección vertical bajo el punto de medición (relevantes en dosel alto) |
| `gas_densities_concentrations_and_timelags` | Densidad/concentración molar de cada gas y el time-lag aplicado |
| `air_properties` | Temperatura del aire y sónica, presión, densidad del aire, humedad relativa, VPD, punto de rocío |
| `unrotated_wind` / `rotated_wind` / `rotation_angles_for_tilt_correction` | Viento antes y después de la rotación de coordenadas, y los ángulos de corrección aplicados |
| `turbulence` | `u*` (velocidad de fricción), TKE, longitud de Monin-Obukhov (`L`), razón de Bowen |
| `footprint` | Huella de la torre: distancia donde se origina el 10/30/50/70/90% de la señal medida (importa para saber qué área real está "viendo" la torre) |
| `uncorrected_fluxes` | Los mismos flujos pero sin corrección espectral, para comparar |
| `statistical_flags` / `spikes` / `diagnostic_flags_LI-7200` / `diagnostic_flags_LI-7700` | Banderas de control de calidad de la prueba estadística y diagnósticos propios de los analizadores de gas (LI-7200 para CO₂/H₂O, LI-7700 para CH₄) |
| `variances` / `covariances` | Varianzas y covarianzas crudas usadas para calcular los flujos |

Archivo de referencia en este repo: `files/archivos-torres/eddypro_Guatavita_2_2024_full_output_2025-04-27T022924_adv.csv` (torre Guatavita ST2, ~169 columnas, una fila cada 30 minutos durante 2024).

## 2. ReddyProc — postprocesamiento

[ReddyProc](https://www.bgc-jena.mpg.de/5622399/ReddyProc) toma la salida de Eddypro (los flujos ya corregidos, típicamente `co2_flux`/NEE, junto con variables meteorológicas) y hace dos cosas que Eddypro no hace:

- **Filtrado por u\*** (velocidad de fricción): descarta los períodos de turbulencia insuficiente (de noche, típicamente), donde el flujo medido no es confiable.
- **Gap-filling y partición del flujo**: rellena los huecos (sensor caído, período descartado por u\*) con un modelo basado en variables meteorológicas, y separa el flujo neto de CO₂ (NEE) en sus dos componentes: respiración del ecosistema (`Reco`) y productividad primaria bruta (`GPP`).

## Integración en Colflux

Actualmente se definió subir a la plataforma la salida de **Eddypro** como dato primario y obligatorio por torre. Razones:

- **Trazabilidad y control de calidad propio.** La salida de Eddypro conserva los flujos corregidos *sin* el filtrado ni el relleno de huecos de ReddyProc, junto con sus flags de calidad (`qc_*`) y errores aleatorios por variable. Eso permite que Colflux aplique su propio criterio de filtrado/gap-filling más adelante, en vez de heredar directamente las decisiones metodológicas (filtro de u*, modelo de relleno) que trae empaquetadas la salida de ReddyProc.
- **Consistencia entre torres.** No todas las torres del proyecto necesariamente van a tener un postprocesamiento en ReddyProc hecho de la misma forma (depende de quién lo corra y con qué parámetros); la salida de Eddypro es el formato estándar que cualquier torre EC genera, así que cargar siempre ese nivel asegura que el dato entrante sea comparable entre sitios.
- **No se pierde la corrección física.** Eddypro ya aplica las correcciones estándar del método (rotación de coordenadas, corrección espectral, WPL), así que el dato que se sube no es "crudo sin procesar" — es el flujo ya calculado, solo sin el paso adicional de limpieza/relleno de ReddyProc.

**¿Y ReddyProc?** Tiene sentido subirlo también, pero como **dataset derivado y opcional** por torre, no como requisito. ReddyProc aporta algo que Eddypro no calcula: el relleno de huecos (gap-filling) y la partición del flujo neto de CO₂ en respiración del ecosistema (`Reco`) y productividad primaria bruta (`GPP`) — procesamiento que sería costoso reimplementar dentro de Colflux. Si una torre tiene ese postprocesamiento disponible, cargarlo permite mostrar esas métricas sin reconstruir el análisis.

La razón para no tratarlo igual que Eddypro es la misma de consistencia entre torres: si se vuelve obligatorio, dos torres dejan de ser comparables a ese nivel cuando su ReddyProc fue corrido con parámetros distintos (filtro de u* diferente, modelo de relleno diferente) o cuando una torre simplemente no tiene ese postprocesamiento hecho todavía. Por eso el modelo nuevo debe cubrir las columnas de Eddypro como base obligatoria, y dejar el ReddyProc como una extensión aparte, asociable a la torre cuando exista.

