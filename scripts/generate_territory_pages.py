from pathlib import Path

root = Path(r'c:\Users\andre\Documents\COLFLUX\context\docs\social')
base = root / 'territorios'
base.mkdir(exist_ok=True)

territories = {
    'la-chorrera': {
        'title': 'La Chorrera',
        'subtitle': 'Área no municipalizada (corregimiento departamental) en el corazón del Amazonas.',
        'image': '../../assets/territorios/la-chorrera-1.jpg',
        'facts': [
            ('Tipo de entidad', 'Área no municipalizada (corregimiento departamental).'),
            ('Ubicación', 'Corazón del departamento del Amazonas, en la cuenca del río Igara Paraná.'),
            ('Extensión / altitud', '≈ 12.670 km², a 184 msnm.'),
            ('Clima', 'Cálido húmedo tropical (selva amazónica).'),
            ('Cómo llegar', 'No tiene acceso terrestre; se llega por vía fluvial o aérea desde Leticia.'),
            ('Biodiversidad', 'Selva amazónica primaria con senderos que atraviesan bosque tropical denso; flora y fauna típicas de la Amazonía profunda, cascadas ocultas y ríos de aguas oscuras. Es un territorio con poca intervención humana y alto valor de conservación.'),
            ('Economía', 'Economía de subsistencia basada en pesca, caza, cultivo de yuca y plátano, y artesanías indígenas.'),
            ('Cultura y atractivos', 'Territorio ancestral de los pueblos uitoto, bora, okaina y muinane; fue escenario histórico de la explotación cauchera a inicios del siglo XX. Ofrece ecoturismo comunitario, senderismo y contacto directo con tradiciones indígenas.'),
            ('Población', '≈ 3.878 habitantes, mayoritariamente indígena.'),
        ],
    },
    'leticia': {
        'title': 'Leticia',
        'subtitle': 'Capital del Amazonas colombiana, en la Triple Frontera y puerta de acceso a la Amazonía profunda.',
        'image': '../../assets/territorios/leticia-1.jpg',
        'facts': [
            ('Tipo de entidad', 'Municipio, capital del departamento del Amazonas.'),
            ('Ubicación', 'Extremo sur de Colombia, a orillas del río Amazonas, en la llamada “Triple Frontera” con Tabatinga (Brasil) y Santa Rosa (Perú).'),
            ('Extensión / altitud', '96 msnm.'),
            ('Clima', 'Cálido húmedo, temperatura promedio de 28 °C todo el año.'),
            ('Cómo llegar', 'Solo por vía aérea (aeropuerto Alfredo Vásquez Cobo) o fluvial; no tiene conexión terrestre con el resto de Colombia.'),
            ('Biodiversidad', 'Rodeada de selva amazónica; cerca están el Parque Nacional Natural Amacayacu (295.500 ha, con más de 500 especies de aves, 150 de mamíferos y numerosos reptiles) y los lagos de Tarapoto, hogar de delfines rosados y grises.'),
            ('Economía', 'Turismo de naturaleza, comercio fronterizo, pesca y servicios; es el principal centro económico y logístico del Amazonas colombiano.'),
            ('Cultura y atractivos', 'Malecón de Leticia, Parque Santander (famoso por el avistamiento de loros al atardecer), Museo Etnográfico del Banco de la República, Parque Ecológico Mundo Amazónico, cruces turísticos a Brasil y Perú, y excursiones a Puerto Nariño e Isla de los Micos.'),
            ('Población', '≈ 53.000 habitantes (DANE 2024), el municipio más poblado del Amazonas; población mestiza, indígena (ticuna, entre otras) y afrodescendiente.'),
        ],
    },
    'santiago': {
        'title': 'Santiago',
        'subtitle': 'Municipio del alto Putumayo, en el Valle de Sibundoy y rodeado por paisajes de montaña y páramo.',
        'image': '../../assets/territorios/putumayo-1.jpg',
        'facts': [
            ('Tipo de entidad', 'Municipio.'),
            ('Ubicación', 'Alto Putumayo, en el Valle de Sibundoy, cordillera de los Andes; limita con la Laguna de la Cocha (Nariño).'),
            ('Extensión / altitud', 'Entre 2.000 y 4.000 msnm.'),
            ('Clima', 'Frío de montaña y páramo.'),
            ('Biodiversidad', 'Rodeado por el Páramo del Bordoncillo; el Putumayo en general alberga más de mil especies de aves (más del 50% del total de Colombia) y la mayor cantidad de especies de primates del país, con conectividad entre Andes, Amazonía y Orinoquía.'),
            ('Economía', 'Agricultura de clima frío (papa, hortalizas), ganadería de leche y turismo rural.'),
            ('Cultura y atractivos', 'Paisajes campesinos, senderos ecoturísticos, cercanía al corredor cultural indígena inga y kamëntsá del Valle de Sibundoy.'),
            ('Población', '≈ 7.300 habitantes (DANE 2023-2024).'),
        ],
    },
    'calamar': {
        'title': 'Calamar',
        'subtitle': 'Municipio de la frontera amazónica del Guaviare, puerta a la selva profunda y la Serranía de Chiribiquete.',
        'image': '../../assets/territorios/guaviare-1.jpg',
        'facts': [
            ('Tipo de entidad', 'Municipio.'),
            ('Ubicación', 'Final de la principal vía terrestre del departamento del Guaviare, en el límite con la selva amazónica profunda.'),
            ('Biodiversidad', 'En su jurisdicción se encuentra buena parte del Parque Nacional Natural Serranía de Chiribiquete (4,3 millones de hectáreas), con tepuyes (mesetas rocosas), más de 2.130 especies de flora registradas (16 endémicas) y más de 75.000 pinturas rupestres de hasta 12.000 años de antigüedad. Es hogar de pueblos indígenas en aislamiento voluntario.'),
            ('Economía', 'Ganadería (corredor San José–Calamar), agricultura y explotación forestal.'),
            ('Cultura y atractivos', 'Puerta de entrada a la selva profunda, destino para viajeros experimentados en busca de desconexión total; balnearios naturales en caños y quebradas.'),
            ('Población', '≈ 9.800 habitantes (DANE 2023), tercer municipio más poblado del Guaviare.'),
        ],
    },
    'san-jose-del-guaviare': {
        'title': 'San José del Guaviare',
        'subtitle': 'Capital del departamento del Guaviare, en la confluencia entre la Amazonía y la Orinoquía.',
        'image': '../../assets/territorios/guaviare-1.jpg',
        'facts': [
            ('Tipo de entidad', 'Municipio, capital del departamento del Guaviare.'),
            ('Ubicación', 'Norte del departamento, en el límite entre la Orinoquía y la Amazonía, a orillas del río Guaviare.'),
            ('Clima', 'Cálido tropical, temperatura promedio de 24 °C.'),
            ('Biodiversidad', 'Cerca está la Serranía de La Lindosa, con el Cerro Azul y sus pictogramas milenarios; confluencia de ecosistemas de sabana, selva y afloramientos rocosos con alta diversidad de flora y fauna.'),
            ('Economía', 'Ganadería, agricultura, turismo de naturaleza y comercio regional.'),
            ('Cultura y atractivos', 'Parque de la Constitución (plaza principal), Cerro Azul, Ciudad de Piedra, caño Cristales de La Macarena (cercano), turismo comunitario indígena (jiw, tucano oriental, nukak).'),
            ('Población', '≈ 54.100 habitantes (DANE 2023), municipio más poblado del departamento.'),
        ],
    },
    'inirida': {
        'title': 'Inírida',
        'subtitle': 'Municipio de la Amazonía nororiental, capital del Guainía y punto de encuentro de ríos y humedales.',
        'image': '../../assets/territorios/inirida-1.jpg',
        'facts': [
            ('Tipo de entidad', 'Municipio, capital del departamento de Guainía.'),
            ('Ubicación', 'Nororiente de la Amazonía colombiana, cerca de las fronteras con Venezuela y Brasil; corazón de la Estrella Fluvial de Inírida, donde confluyen los ríos Inírida, Guaviare, Atabapo y Ventuari para formar el Orinoco.'),
            ('Clima', 'Cálido húmedo, temperatura promedio de 31,5 °C.'),
            ('Biodiversidad', 'La Estrella Fluvial de Inírida es humedal Ramsar de importancia internacional (≈ 250.000 ha); alberga los Cerros de Mavicure (formaciones rocosas de 1.700 millones de años, entre las más antiguas del planeta) y las sabanas de arena blanca donde crece la flor de Inírida.'),
            ('Economía', 'Comercio fluvial, turismo de naturaleza, pesca y minería artesanal.'),
            ('Cultura y atractivos', 'Cerros de Mavicure, Piedra de Mavizo (miradores de atardecer), jardín de la flor de Inírida, petroglifos del parque rupestre Amarrú, turismo comunitario indígena.'),
            ('Población', '≈ 36.500 habitantes (DANE 2022, con crecimiento sostenido), municipio más poblado de Guainía; tres de cada cuatro habitantes del departamento son indígenas (14 pueblos, entre ellos puinave, curripaco, piapoco y cubeo).'),
        ],
    },
    'el-cocuy': {
        'title': 'El Cocuy',
        'subtitle': 'Municipio andino cercano al Parque Nacional Natural El Cocuy, con paisajes de alta montaña y glaciares.',
        'image': '../../assets/territorios/cocuy-1.jpg',
        'facts': [
            ('Tipo de entidad', 'Municipio, provincia de Gutiérrez.'),
            ('Ubicación', 'Cordillera Oriental de los Andes; sede administrativa del Parque Nacional Natural El Cocuy (Sierra Nevada del Cocuy, Güicán y Chita).'),
            ('Extensión / altitud', 'El parque va de 600 a 5.330 msnm (Ritacuwa Blanco, punto más alto).'),
            ('Clima', 'Templado a nival, según la altitud (35 °C a -10 °C dentro del parque).'),
            ('Biodiversidad', 'El PNN El Cocuy (306.000 ha) alberga uno de los últimos glaciares de Colombia, más de 150 lagunas de origen glaciar, ecosistemas desde selva basal hasta páramo y superpáramo, y una fauna y flora de alta montaña únicas en el país.'),
            ('Economía', 'Ganadería de altura, agricultura de clima frío y turismo de montaña.'),
            ('Cultura y atractivos', 'Senderismo y montañismo regulado hacia los picos nevados, lagunas como La Plaza y Grande de la Sierra; turismo exigente que requiere aclimatación y permisos.'),
            ('Población', '≈ 4.300 habitantes (DANE 2023).'),
        ],
    },
    'guican-de-la-sierra': {
        'title': 'Güicán de la Sierra',
        'subtitle': 'Municipio boyacense vecino a El Cocuy, con ecosistemas de páramo y alta montaña.',
        'image': 'https://images.unsplash.com/photo-1500534623283-312aade485b7?auto=format&fit=crop&w=900&q=80',
        'facts': [
            ('Tipo de entidad', 'Municipio, provincia de Gutiérrez.'),
            ('Ubicación', 'Vecino de El Cocuy, en la Cordillera Oriental.'),
            ('Extensión / altitud', '2.880 msnm en su casco urbano; el 81% de su territorio hace parte del PNN El Cocuy.'),
            ('Clima', 'Frío de montaña a nival en las zonas altas.'),
            ('Biodiversidad', 'Comparte con El Cocuy picos nevados, glaciares, lagunas glaciares y extensos páramos; territorio de gran valor ecológico e importancia espiritual para el pueblo indígena U’wa.'),
            ('Economía', 'Agricultura y ganadería de páramo, turismo de naturaleza y montañismo.'),
            ('Cultura y atractivos', 'Montañas nevadas, aguas termales, “pozos azules”; centro cultural histórico del pueblo U’wa.'),
            ('Población', '≈ 4.350–4.500 habitantes, incluyendo cerca de 900 personas de la comunidad indígena U’wa.'),
        ],
    },
    'choachi': {
        'title': 'Choachí',
        'subtitle': 'Municipio cundinamarqués cercano a Bogotá, reconocido por sus cascadas y el páramo de Chingaza.',
        'image': '../../assets/territorios/chingaza-1.jpg',
        'facts': [
            ('Tipo de entidad', 'Municipio.'),
            ('Ubicación', 'A 36 km de Bogotá (cerca de una hora en carro), en los Cerros Orientales, en la provincia de Oriente.'),
            ('Extensión / altitud', '223 km² (210 km² de área rural); clima variado por su topografía.'),
            ('Clima', 'Templado, con zonas frías de páramo hacia el Parque Nacional Natural Chingaza.'),
            ('Cómo llegar', 'Ruta de bus Bogotá–Choachí; carretera que conecta con la capital en 1 a 1,5 horas.'),
            ('Biodiversidad', 'Uno de los municipios con mayor área de páramo protegida dentro del PNN Chingaza; alberga la cascada La Chorrera, la más alta de Colombia (590 m), la Cueva de los Monos, la cascada El Chiflón y el páramo de El Verjón.'),
            ('Economía', 'Agricultura, ganadería, turismo rural y de naturaleza.'),
            ('Cultura y atractivos', 'Reconocido en 2021 por la Organización Mundial del Turismo (OMT) como uno de los “Best Tourism Villages” del mundo; pueblo colonial de calles empedradas, termales de Santa Mónica, deportes extremos (torrentismo, escalada, cabalgatas) en el Parque Aventura La Chorrera.'),
            ('Población', '≈ 12.300 habitantes.'),
        ],
    },
    'fomeque': {
        'title': 'Fómeque',
        'subtitle': 'Municipio de montaña y páramo, clave para la captación de agua y la biodiversidad de Chingaza.',
        'image': '../../assets/territorios/chingaza-1.jpg',
        'facts': [
            ('Tipo de entidad', 'Municipio.'),
            ('Ubicación', 'A 56 km de Bogotá, en la Cordillera Oriental. Su nombre significa “El Bosque de los Zorros”.'),
            ('Extensión / altitud', 'Altitudes entre 1.600 y 4.020 msnm; compuesto por 32 veredas.'),
            ('Clima', 'Varía de templado a frío de páramo según la altitud.'),
            ('Biodiversidad', 'Cerca del 49% de su territorio hace parte del Parque Nacional Natural Chingaza (76.600 ha en 11 municipios), una de las principales “fábricas de agua” del país, que abastece de agua potable a cerca de 10 millones de personas; hábitat del venado coliblanco y otras especies de páramo y bosque altoandino.'),
            ('Economía', 'Agricultura (papa, hortalizas), ganadería y turismo ecológico.'),
            ('Cultura y atractivos', 'Iglesia de la Inmaculada Concepción, parque principal, Reserva Natural Páramo de las Burras, senderos de acceso al PNN Chingaza.'),
            ('Población', '≈ 13.100 habitantes.'),
        ],
    },
    'la-calera': {
        'title': 'La Calera',
        'subtitle': 'Municipio de la sabana de Bogotá, cercano a Chingaza y clave para la relación entre ciudad, agua y campo.',
        'image': '../../assets/territorios/chingaza-1.jpg',
        'facts': [
            ('Tipo de entidad', 'Municipio, provincia del Guavio.'),
            ('Ubicación', 'A 18 km al nororiente de Bogotá, cerca de las localidades de Chapinero y Usaquén.'),
            ('Extensión / altitud', 'Entre 2.600 y 3.000 msnm (pisos térmicos frío y páramo).'),
            ('Clima', 'Frío de montaña, agradable y fresco durante todo el año.'),
            ('Biodiversidad', 'En su territorio están el embalse de San Rafael y el acceso al embalse de Chuza (surtido por la laguna de Chingaza), además de un sector del Parque Nacional Natural Chingaza, con bosques nubosos y páramos que proveen buena parte del agua de Bogotá.'),
            ('Economía', 'Agricultura (papa, maíz, zanahoria), ganadería, piscicultura de trucha, minería de piedra caliza y turismo; alberga industrias como Cementos Samper (Cemex) y la planta de Agua Manantial (Coca-Cola Company).'),
            ('Cultura y atractivos', 'Cerro de La Pita (mirador y parapente), Ruta de Chingaza en bicicleta, discotecas y fincas de recreo en la vía Bogotá–La Calera; destino popular de ciclismo desde la capital.'),
            ('Población', '≈ 41.400 habitantes (DANE 2023), en crecimiento por su cercanía a Bogotá.'),
        ],
    },
    'villavicencio': {
        'title': 'Villavicencio',
        'subtitle': 'Capital del Meta y puerta de entrada a los Llanos Orientales colombianos.',
        'image': '../../assets/territorios/casanare-1.jpg',
        'facts': [
            ('Tipo de entidad', 'Municipio, capital del departamento del Meta.'),
            ('Ubicación', 'Piedemonte de la Cordillera Oriental, puerta de entrada a los Llanos Orientales.'),
            ('Biodiversidad', 'Ecosistemas estratégicos de piedemonte con aves migratorias y endémicas, mamíferos, reptiles, anfibios y alrededor de 400 especies de plantas registradas.'),
            ('Economía', 'Comercio, agroindustria (ganadería, arroz, palma), servicios y turismo; es el principal centro económico de la Orinoquía colombiana.'),
            ('Cultura y atractivos', 'Cultura llanera (joropo, coleo), gastronomía típica, encuentros de pueblos indígenas locales; en trámite legislativo su declaratoria como Distrito Especial Bioturístico, Cultural y Educativo.'),
            ('Población', '≈ 573.500 habitantes (DANE 2023), municipio más poblado del Meta y una de las principales ciudades de la Orinoquía.'),
        ],
    },
    'puerto-lleras': {
        'title': 'Puerto Lleras',
        'subtitle': 'Municipio llanero a orillas del río Ariari, con sabanas, fauna y cultura de la Orinoquía.',
        'image': '../../assets/territorios/casanare-1.jpg',
        'facts': [
            ('Tipo de entidad', 'Municipio.'),
            ('Ubicación', 'A orillas del río Ariari, en los Llanos Orientales del Meta.'),
            ('Extensión / altitud', '2.061 km²; ≈ 245-450 msnm.'),
            ('Clima', 'Cálido tropical de sabana (clima Am).'),
            ('Biodiversidad', 'Hace parte de las sabanas del Meta, con vegetación de gramíneas y palmeras, y fauna típica llanera como jaguares, venados y caimanes; el río Ariari (y su afluente el río Iraca) es eje central de la vida natural y económica del municipio.'),
            ('Economía', 'Ganadería, agricultura y pesca; economía muy ligada al régimen hídrico del río Ariari.'),
            ('Cultura y atractivos', 'Festival de Verano “La Perla del Ariari” (enero), cultura llanera, cabalgatas y actividades náuticas en el río.'),
            ('Población', '≈ 10.700 habitantes (DANE 2023-2024).'),
        ],
    },
    'san-luis-de-palenque': {
        'title': 'San Luis de Palenque',
        'subtitle': 'Municipio del Casanare sobre el río Pauto, con paisaje de sabana y tradición llanera.',
        'image': '../../assets/territorios/casanare-1.jpg',
        'facts': [
            ('Tipo de entidad', 'Municipio.'),
            ('Ubicación', 'Sobre una curva del río Pauto (afluente del río Meta), en plena llanura del Casanare.'),
            ('Extensión / altitud', '≈ 170 msnm.'),
            ('Clima', 'Cálido tropical de sabana.'),
            ('Biodiversidad', 'El Casanare es reconocido por sus extensas sabanas, morichales y red hídrica (ríos Meta, Cravo Sur, Cusiana, Pauto, entre otros); alberga chigüiros, babillas, anacondas, nutrias gigantes y más de 600 especies de aves. Cerca del municipio está la reserva natural El Encanto de Guanapalo (9.000 ha), ideal para el avistamiento de fauna llanera (venados, capibaras, pumas, osos palmeros).'),
            ('Economía', 'Ganadería extensiva, agricultura y, en menor medida, hidrocarburos.'),
            ('Cultura y atractivos', 'Rancho Museo El Llanerazo (objetos y tradiciones de la cultura llanera), safaris de observación de fauna, gastronomía llanera (mamona, carne a la llanera).'),
            ('Población', '≈ 8.900 habitantes (DANE 2023).'),
        ],
    },
}

for slug, data in territories.items():
    fact_html = '\n'.join(
        f'    <div class="territory-fact"><strong>{label}</strong><p>{value}</p></div>'
        for label, value in data['facts']
    )
    content = f'''---
hide:
  - toc
---

# {data['title']}

<div class="territory-detail">
  <div class="territory-detail-header">
    <img class="territory-detail-image" src="{data['image']}" alt="{data['title']}">
    <div>
      <p class="territory-summary">{data['subtitle']}</p>
    </div>
  </div>

  <div class="territory-fact-grid">
{fact_html}
  </div>

  <a class="territory-back-link" href="../territorios/">← Volver a territorios</a>
</div>
'''
    target = base / f'{slug}.md'
    target.write_text(content, encoding='utf-8')
    print(f'Created {target}')
