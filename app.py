import streamlit as st
import random
import time

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Centro Espacial ASC y HFSR",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILOS CSS PERSONALIZADOS ---
st.markdown("""
<style>
    .main { background-color: #050b14; color: #f1f5f9; }
    .stButton>button {
        width: 100%; border-radius: 12px; height: 3.5em;
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        color: white; border: 1px solid #3b82f6;
        transition: all 0.3s ease; font-weight: bold; font-size: 1.1em;
    }
    .stButton>button:hover {
        border-color: #60a5fa; color: #60a5fa; transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
    }
    .planet-card {
        background: rgba(15, 23, 42, 0.8); padding: 25px;
        border-radius: 20px; border: 2px solid #334155;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .dashboard-panel {
        background: rgba(30, 41, 59, 0.5); padding: 15px;
        border-radius: 10px; border-left: 4px solid #10b981;
    }
    .game-over { text-align: center; color: #ef4444; }
    h1, h2, h3 { color: #60a5fa !important; }
</style>
""", unsafe_allow_html=True)

# --- BASE DE DATOS COMPLETA (2 NIVELES) ---
DATA = {
    "Sol": {
        "tipo": "Estrella", "color": "☀️", "desc": "El centro ardiente de nuestro sistema.",
        "quiz": {
            "normal": [
                {"q": "¿Qué es el Sol?", "o": ["Un planeta", "Una estrella", "Un cometa"], "a": "Una estrella", "e": "Es la estrella más cercana a nosotros."},
                {"q": "¿Qué proceso genera su energía?", "o": ["Fuego", "Fusión Nuclear", "Electricidad"], "a": "Fusión Nuclear", "e": "Fusiona átomos en su núcleo."},
                {"q": "¿De qué color vemos al Sol desde la Tierra?", "o": ["Verde", "Amarillo/Blanco", "Rojo"], "a": "Amarillo/Blanco", "e": "Nuestra atmósfera lo hace ver amarillento."},
                {"q": "¿Qué edad tiene aproximadamente el Sol?", "o": ["100 años", "4.6 mil millones de años", "1 millón de años"], "a": "4.6 mil millones de años", "e": "Está a la mitad de su vida útil."},
                {"q": "¿Qué gas es el más abundante en el Sol?", "o": ["Oxígeno", "Hidrógeno", "Helio"], "a": "Hidrógeno", "e": "El hidrógeno es su combustible principal."}
            ],
            "pro master": [
                {"q": "¿A qué temperatura está el núcleo del Sol?", "o": ["15 millones °C", "6,000 °C", "100,000 °C"], "a": "15 millones °C", "e": "El núcleo es el motor del Sol."},
                {"q": "¿Qué porcentaje de la masa del sistema solar está en el Sol?", "o": ["50%", "99.8%", "75%"], "a": "99.8%", "e": "¡Casi todo el peso del sistema es el Sol!"},
                {"q": "¿En qué estado de la materia se encuentra el Sol?", "o": ["Sólido", "Líquido", "Plasma"], "a": "Plasma", "e": "Es un gas supercaliente y cargado eléctricamente."},
                {"q": "¿Qué pasará con el Sol al final de su vida?", "o": ["Será agujero negro", "Gigante roja y luego enana blanca", "Explotará"], "a": "Gigante roja y luego enana blanca", "e": "Crecerá absorbiendo planetas y luego se encogerá."},
                {"q": "¿Cuánto tarda la luz del Sol en llegar a la Tierra?", "o": ["1 segundo", "8 minutos", "1 hora"], "a": "8 minutos", "e": "Viaja a 300,000 km/s pero está muy lejos."}
            ]
        }
    },
    "Mercurio": {
        "tipo": "Planeta", "color": "🔘", "desc": "Pequeño, veloz y lleno de cráteres.",
        "quiz": {
            "normal": [
                {"q": "¿Es el planeta más cercano al Sol?", "o": ["Sí", "No"], "a": "Sí", "e": "Es el primero del sistema solar."},
                {"q": "¿Es Mercurio el planeta más caliente?", "o": ["Sí", "No, es Venus"], "a": "No, es Venus", "e": "Venus gana por su densa atmósfera tóxica."},
                {"q": "¿Cuánto dura un año en Mercurio?", "o": ["88 días", "365 días", "10 días"], "a": "88 días", "e": "Viaja rapidísimo alrededor del Sol."},
                {"q": "¿Tiene lunas o anillos?", "o": ["Sí, ambos", "Ninguno", "Solo anillos"], "a": "Ninguno", "e": "Está muy cerca del Sol para retener lunas."},
                {"q": "¿Por qué tiene tantos cráteres?", "o": ["Por falta de atmósfera", "Son volcanes", "Aliens"], "a": "Por falta de atmósfera", "e": "No tiene protección contra los meteoritos."}
            ],
            "pro master": [
                {"q": "¿Qué sonda fue la primera en visitarlo en 1974?", "o": ["Mariner 10", "Voyager 1", "Cassini"], "a": "Mariner 10", "e": "Tomó las primeras fotos de cerca."},
                {"q": "¿Qué característica extraña tiene su núcleo?", "o": ["Es de diamante", "Es inusualmente grande y de hierro", "No tiene núcleo"], "a": "Es inusualmente grande y de hierro", "e": "Ocupa gran parte de su interior, haciéndolo muy denso."},
                {"q": "¿Qué es la 'Cuenca Caloris'?", "o": ["Un océano", "El cráter de impacto más grande de Mercurio", "Un volcán"], "a": "El cráter de impacto más grande de Mercurio", "e": "Se formó por el choque de un asteroide masivo."},
                {"q": "¿Tiene campo magnético?", "o": ["Sí, pero débil", "No", "Muy fuerte"], "a": "Sí, pero débil", "e": "Es apenas el 1% de la fuerza del de la Tierra."},
                {"q": "¿Cómo se llama su tenue capa de gases?", "o": ["Exosfera", "Troposfera", "No existe"], "a": "Exosfera", "e": "Son átomos atrapados temporalmente, no una atmósfera real."}
            ]
        }
    },
    "Venus": {
        "tipo": "Planeta", "color": "🟡", "desc": "El infierno del sistema solar. Caliente y tóxico.",
        "quiz": {
            "normal": [
                {"q": "¿Es Venus más caliente que Mercurio?", "o": ["Sí", "No"], "a": "Sí", "e": "Su atmósfera atrapa todo el calor como un invernadero."},
                {"q": "¿Se le conoce como el gemelo de la Tierra por su tamaño?", "o": ["Sí", "No"], "a": "Sí", "e": "Son casi idénticos en tamaño."},
                {"q": "¿En qué dirección rota Venus?", "o": ["Igual que la Tierra", "Al revés (retrógrada)"], "a": "Al revés (retrógrada)", "e": "Allí el Sol sale por el oeste."},
                {"q": "¿Qué gas domina su atmósfera?", "o": ["Oxígeno", "Dióxido de carbono (CO2)", "Helio"], "a": "Dióxido de carbono (CO2)", "e": "Es lo que crea su efecto invernadero extremo."},
                {"q": "¿Llueve agua en Venus?", "o": ["Sí", "No, llueve ácido"], "a": "No, llueve ácido", "e": "Sus densas nubes son de ácido sulfúrico."}
            ],
            "pro master": [
                {"q": "¿A qué temperatura promedio está Venus?", "o": ["460 °C", "100 °C", "1,000 °C"], "a": "460 °C", "e": "Es suficiente calor para derretir plomo."},
                {"q": "¿Qué sonda aterrizó y envió las primeras fotos desde su superficie en 1970?", "o": ["Venera 7", "Curiosity"], "a": "Venera 7", "e": "Fue una misión soviética épica que sobrevivió muy poco tiempo."},
                {"q": "¿Cómo es la presión en su superficie comparada con la Tierra?", "o": ["Igual", "90 veces mayor", "Menor"], "a": "90 veces mayor", "e": "Te aplastaría como si estuvieras a un kilómetro bajo el mar."},
                {"q": "¿Cómo se llama el monte más alto de Venus?", "o": ["Maxwell Montes", "Olimpo"], "a": "Maxwell Montes", "e": "Tiene unos 11 km de altura y 'nieve' de metales pesados."},
                {"q": "¿Tiene campo magnético protector?", "o": ["Sí, muy fuerte", "No tiene uno significativo"], "a": "No tiene uno significativo", "e": "Su núcleo no gira lo suficientemente rápido para generarlo."}
            ]
        }
    },
    "Tierra": {
        "tipo": "Planeta", "color": "🌍", "desc": "Nuestro hogar azul con agua líquida y vida.",
        "lunas": ["La Luna"],
        "quiz": {
            "normal": [
                {"q": "¿Qué porcentaje de la superficie de la Tierra está cubierto por agua?", "o": ["50%", "71%", "90%"], "a": "71%", "e": "Somos un planeta oceánico."},
                {"q": "¿Qué gas respiramos mayormente en nuestra atmósfera?", "o": ["Oxígeno", "Nitrógeno", "Dióxido de carbono"], "a": "Nitrógeno", "e": "El aire es 78% nitrógeno y solo 21% oxígeno."},
                {"q": "¿Cuánto tarda la Tierra en dar una vuelta completa al Sol?", "o": ["24 horas", "365 días", "30 días"], "a": "365 días", "e": "Este recorrido forma un año completo."},
                {"q": "¿Qué escudo invisible nos protege del viento solar?", "o": ["Campo magnético", "Capa de ozono", "Las nubes"], "a": "Campo magnético", "e": "Sin él, perderíamos nuestra atmósfera."},
                {"q": "¿Cómo se llaman las piezas gigantes que forman nuestra corteza terrestre?", "o": ["Placas tectónicas", "Ladrillos", "Continentes flotantes"], "a": "Placas tectónicas", "e": "Su movimiento causa los terremotos y forma montañas."}
            ],
            "pro master": [
                {"q": "¿A qué velocidad orbita la Tierra alrededor del Sol?", "o": ["107,000 km/h", "1,000 km/h", "10,000 km/h"], "a": "107,000 km/h", "e": "¡Viajamos rapidísimo por el espacio sin darnos cuenta!"},
                {"q": "¿De qué está hecho principalmente el núcleo interno de la Tierra?", "o": ["Lava", "Hierro y níquel sólidos", "Agua hirviendo"], "a": "Hierro y níquel sólidos", "e": "La inmensa presión lo mantiene sólido a pesar del calor."},
                {"q": "¿Cuál es el punto más profundo de los océanos?", "o": ["Fosa de las Marianas", "Fosa de las Tongas", "Gran Barrera"], "a": "Fosa de las Marianas", "e": "Tiene casi 11 kilómetros de profundidad."},
                {"q": "¿Qué edad tiene la Tierra?", "o": ["4.5 mil millones de años", "1 millón de años", "14 mil millones de años"], "a": "4.5 mil millones de años", "e": "Se formó poco después que el propio Sol."},
                {"q": "¿Qué fenómeno visual se crea cuando partículas solares chocan con los polos magnéticos?", "o": ["Arcos iris", "Auroras boreales y australes", "Eclipses"], "a": "Auroras boreales y australes", "e": "Es un espectacular show de luces naturales."}
            ]
        }
    },
    "Marte": {
        "tipo": "Planeta", "color": "🔴", "desc": "El planeta rojo. Hogar de robots exploradores.",
        "lunas": ["Phobos", "Deimos"],
        "quiz": {
            "normal": [
                {"q": "¿Por qué Marte se ve de color rojo?", "o": ["Tiene fuego", "Por el óxido de hierro", "Es pintura espacial"], "a": "Por el óxido de hierro", "e": "Básicamente está cubierto de polvo oxidado."},
                {"q": "¿Cuántas lunas tiene?", "o": ["1", "2", "Ninguna"], "a": "2", "e": "Son Phobos y Deimos, muy pequeñas y deformes."},
                {"q": "¿Cómo se llama el volcán más grande de Marte?", "o": ["Monte Olimpo", "Everest", "Vesubio"], "a": "Monte Olimpo", "e": "Es el volcán más grande de todo el sistema solar."},
                {"q": "¿Hace frío o calor en Marte?", "o": ["Mucho frío", "Mucho calor"], "a": "Mucho frío", "e": "Es un desierto helado, con temperaturas bajo cero."},
                {"q": "¿Cómo se llaman los robots con ruedas que exploran Marte?", "o": ["Rovers", "Aviones", "Drones"], "a": "Rovers", "e": "Como el Curiosity o el Perseverance."}
            ],
            "pro master": [
                {"q": "¿Qué es Valles Marineris?", "o": ["Un cañón gigante", "Un océano subterráneo", "Un cráter"], "a": "Un cañón gigante", "e": "Es un cañón tan grande que cruzaría todo Estados Unidos."},
                {"q": "¿Cuál es la presión atmosférica en Marte comparada con la Tierra?", "o": ["Aproximadamente 1%", "100%", "50%"], "a": "Aproximadamente 1%", "e": "Su atmósfera es extremadamente delgada y no permite agua líquida superficial."},
                {"q": "¿Por qué Marte perdió gran parte de su atmósfera original?", "o": ["Perdió su campo magnético protector", "Se congeló entera", "Choque de asteroides"], "a": "Perdió su campo magnético protector", "e": "Al enfriarse su núcleo, perdió el escudo y el viento solar barrió su aire."},
                {"q": "¿Qué color tiene el cielo marciano de día?", "o": ["Azul", "Rojo/Salmón", "Negro"], "a": "Rojo/Salmón", "e": "Debido a las finas partículas de polvo en suspensión en su atmósfera."},
                {"q": "¿Cómo se llama el primer helicóptero terrestre que logró volar en Marte?", "o": ["Ingenuity", "Apollo", "Sojourner"], "a": "Ingenuity", "e": "Hizo historia al realizar el primer vuelo controlado en otro planeta."}
            ]
        }
    },
    "Phobos": {
        "tipo": "Luna de Marte", "color": "🌑", "desc": "La luna más grande de Marte, condenada a chocar.",
        "quiz": {
            "normal": [
                {"q": "¿A qué planeta orbita Phobos?", "o": ["Júpiter", "Marte", "Tierra"], "a": "Marte", "e": "Es la compañera inseparable de Deimos."},
                {"q": "¿Es redonda como nuestra luna?", "o": ["Sí", "No, parece una papa"], "a": "No, parece una papa", "e": "Es demasiado pequeña para tener gravedad suficiente para hacerse esférica."},
                {"q": "¿Qué significa el nombre Phobos?", "o": ["Amor", "Miedo/Pánico", "Guerra"], "a": "Miedo/Pánico", "e": "En la mitología griega, es el dios del miedo."},
                {"q": "¿Cuántas veces da la vuelta a Marte en un solo día marciano?", "o": ["1 vez", "3 veces", "Tarda 1 mes"], "a": "3 veces", "e": "Orbita rapidísimo, saliendo por el oeste y poniéndose por el este."},
                {"q": "¿Tiene atmósfera respirable?", "o": ["Sí", "No"], "a": "No", "e": "No tiene masa suficiente para retener ningún gas."}
            ],
            "pro master": [
                {"q": "¿Qué destino fatal le espera a Phobos?", "o": ["Saldrá del sistema solar", "Chocará con Marte o formará un anillo", "Se volverá una estrella"], "a": "Chocará con Marte o formará un anillo", "e": "Su órbita decae y se acerca a Marte 2 metros cada 100 años."},
                {"q": "¿Cómo se llama su cráter de impacto más famoso que casi destruye la luna?", "o": ["Stickney", "Tycho", "Copérnico"], "a": "Stickney", "e": "Lleva el nombre del apellido de soltera de la esposa del descubridor."},
                {"q": "¿Cuál es su origen más probable según los científicos?", "o": ["Un asteroide capturado", "Un pedazo de la Tierra", "Viene de otra galaxia"], "a": "Un asteroide capturado", "e": "Su composición es muy similar a los asteroides oscuros del cinturón principal."},
                {"q": "¿Qué peculiaridad tiene la gravedad en la superficie de Phobos?", "o": ["Es altísima", "Es tan baja que podrías escapar saltando en una rampa", "No tiene gravedad"], "a": "Es tan baja que podrías escapar saltando en una rampa", "e": "Una persona de 70 kg pesaría unos gramos allí."},
                {"q": "¿A quién se le atribuye su descubrimiento en 1877?", "o": ["Galileo Galilei", "Asaph Hall", "Isaac Newton"], "a": "Asaph Hall", "e": "Descubrió tanto Phobos como Deimos."}
            ]
        }
    },
    "Deimos": {
        "tipo": "Luna de Marte", "color": "🌑", "desc": "La luna más pequeña y lejana de Marte.",
        "quiz": {
            "normal": [
                {"q": "¿A qué planeta pertenece Deimos?", "o": ["Venus", "Marte", "Urano"], "a": "Marte", "e": "Es la segunda y más pequeña luna de Marte."},
                {"q": "¿Tiene forma esférica perfecta?", "o": ["Sí", "No, es irregular"], "a": "No, es irregular", "e": "Como Phobos, parece una roca informe o una papa."},
                {"q": "¿Orbita más cerca o más lejos de Marte que Phobos?", "o": ["Más lejos", "Más cerca"], "a": "Más lejos", "e": "Deimos tiene una órbita mucho más amplia."},
                {"q": "¿Qué significa el nombre Deimos?", "o": ["Paz", "Terror", "Felicidad"], "a": "Terror", "e": "En la mitología, es hermano de Phobos (Miedo)."},
                {"q": "¿Por qué su superficie se ve más suave que la de Phobos?", "o": ["Tiene agua", "El polvo suelto (regolito) llena sus cráteres", "Es de plástico"], "a": "El polvo suelto (regolito) llena sus cráteres", "e": "Está cubierta de una gruesa capa de polvo estelar."}
            ],
            "pro master": [
                {"q": "¿Qué le pasará a Deimos en el futuro lejano?", "o": ["Chocará con Marte", "Se alejará al espacio", "Explotará"], "a": "Se alejará al espacio", "e": "A diferencia de Phobos, la órbita de Deimos se está expandiendo lentamente."},
                {"q": "¿Cuánto tarda en completar una órbita alrededor de Marte?", "o": ["30 horas", "1 año", "10 minutos"], "a": "30 horas", "e": "Tarda un poco más que un día marciano completo."},
                {"q": "¿De qué tipo de asteroide se sospecha que proviene Deimos?", "o": ["Tipo D o C (ricos en carbono)", "Tipo S (metálico)", "Hielo puro"], "a": "Tipo D o C (ricos en carbono)", "e": "Son cuerpos extremadamente oscuros."},
                {"q": "¿Si estuvieras en Marte, cómo verías a Deimos en el cielo?", "o": ["Como una gran luna llena", "Como una estrella brillante", "Como el sol"], "a": "Como una estrella brillante", "e": "Es tan pequeña y está tan lejos que no se vería como un disco claro."},
                {"q": "¿Cómo se llaman sus dos cráteres principales nombrados en honor a escritores?", "o": ["Swift y Voltaire", "García y Márquez", "Borges y Poe"], "a": "Swift y Voltaire", "e": "Ambos escritores mencionaron lunas marcianas en sus libros mucho antes de ser descubiertas."}
            ]
        }
    },
    "Júpiter": {
        "tipo": "Planeta", "color": "🟠", "desc": "El gigante gaseoso, el rey del sistema solar.",
        "lunas": ["Io", "Europa", "Ganímedes", "Calisto"],
        "quiz": {
            "normal": [
                {"q": "¿Es Júpiter el planeta más grande del sistema solar?", "o": ["Sí", "No"], "a": "Sí", "e": "Es el gigante indiscutible del vecindario."},
                {"q": "¿De qué está hecho principalmente Júpiter?", "o": ["Roca dura", "Gases (Hidrógeno y Helio)", "Hielo"], "a": "Gases (Hidrógeno y Helio)", "e": "Por eso se le clasifica como un 'Gigante Gaseoso'."},
                {"q": "¿Qué es la famosa Gran Mancha Roja?", "o": ["Un volcán gigante", "Una tormenta/huracán inmenso", "Un océano de lava"], "a": "Una tormenta/huracán inmenso", "e": "Lleva cientos de años girando sin parar."},
                {"q": "¿Cuántas Tierras cabrían dentro de Júpiter?", "o": ["10", "1,300", "50"], "a": "1,300", "e": "¡Su volumen es inmensamente superior al nuestro!"},
                {"q": "¿Cuánto dura un día en Júpiter?", "o": ["24 horas", "9.9 horas", "100 horas"], "a": "9.9 horas", "e": "Tiene el día más corto; gira rapidísimo sobre su propio eje."}
            ],
            "pro master": [
                {"q": "¿Qué misión de la NASA lo estudia desde el año 2016?", "o": ["Cassini", "Juno", "Voyager"], "a": "Juno", "e": "Juno ha revelado detalles increíbles de sus polos y gravedad."},
                {"q": "¿Cómo es el campo magnético de Júpiter en comparación al de la Tierra?", "o": ["Es más débil", "Es unas 20,000 veces más fuerte", "No tiene"], "a": "Es unas 20,000 veces más fuerte", "e": "Es el campo magnético planetario más poderoso y letal del sistema."},
                {"q": "¿Qué material exótico se encuentra en las profundidades de su océano interno?", "o": ["Agua dulce", "Hidrógeno metálico líquido", "Lava radiactiva"], "a": "Hidrógeno metálico líquido", "e": "Las presiones extremas convierten el gas en un metal conductor."},
                {"q": "¿Júpiter protege a la Tierra de impactos astronómicos?", "o": ["Sí, su inmensa gravedad desvía asteroides y cometas", "No, no afecta en nada", "Solo con sus anillos"], "a": "Sí, su inmensa gravedad desvía asteroides y cometas", "e": "Actúa como una 'aspiradora' espacial, protegiendo a los planetas interiores."},
                {"q": "¿Cuánto tarda Júpiter en orbitar al Sol (su año)?", "o": ["12 años terrestres", "1 año terrestre", "84 años terrestres"], "a": "12 años terrestres", "e": "A pesar de girar rápido sobre sí mismo, su recorrido alrededor del Sol es larguísimo."}
            ]
        }
    },
    "Io": {
        "tipo": "Luna de Júpiter", "color": "🌋", "desc": "El cuerpo más volcánicamente activo del sistema solar.",
        "quiz": {
            "normal": [
                {"q": "¿A qué planeta pertenece Io?", "o": ["Marte", "Júpiter", "Saturno"], "a": "Júpiter", "e": "Es la más cercana a Júpiter de las grandes lunas."},
                {"q": "¿Qué hay en toda la superficie de Io?", "o": ["Océanos de agua", "Cientos de volcanes activos", "Bosques densos"], "a": "Cientos de volcanes activos", "e": "Está cubierta de volcanes que cambian su superficie constantemente."},
                {"q": "¿De qué color se ve Io desde el espacio?", "o": ["Blanco hielo", "Amarillo, naranja y rojo", "Negro total"], "a": "Amarillo, naranja y rojo", "e": "Parece una pizza debido a los compuestos de azufre."},
                {"q": "¿Por qué Io tiene tantos volcanes?", "o": ["Por el calor del Sol", "Calentamiento por la gravedad (mareas) de Júpiter", "Tiene una caldera mágica"], "a": "Calentamiento por la gravedad (mareas) de Júpiter", "e": "Júpiter la estira y comprime, generando inmenso calor interno."},
                {"q": "¿Io tiene agua líquida?", "o": ["Sí, mucha", "No, está completamente seca"], "a": "No, está completamente seca", "e": "Todo el calor expulsó cualquier rastro de agua al espacio hace mucho."}
            ],
            "pro master": [
                {"q": "¿Qué forma alrededor de Júpiter el material que escapa de los volcanes de Io?", "o": ["Un anillo de fuego", "Un inmenso toroide de plasma", "Una nube de oxígeno"], "a": "Un inmenso toroide de plasma", "e": "Crea un anillo invisible de partículas cargadas y altamente radiactivas."},
                {"q": "¿Cómo se llama el volcán o lago de lava más potente de Io?", "o": ["Monte Olimpo", "Loki Patera", "Krakatoa espacial"], "a": "Loki Patera", "e": "Es un lago de lava masivo que periódicamente se hunde y renueva."},
                {"q": "¿Qué tan altos pueden llegar a ser los géiseres volcánicos de Io?", "o": ["10 metros", "Hasta 500 kilómetros", "1 kilómetro"], "a": "Hasta 500 kilómetros", "e": "Como tiene baja gravedad y no hay atmósfera, las columnas llegan directamente al espacio."},
                {"q": "¿A qué temperatura puede llegar la lava fresca en Io?", "o": ["100 °C", "1,600 °C", "10,000 °C"], "a": "1,600 °C", "e": "Es significativamente más caliente que la lava que se encuentra hoy en la Tierra."},
                {"q": "¿Cuál es la resonancia orbital que causa el calentamiento continuo de Io?", "o": ["1:2:4 con Europa y Ganímedes", "Resonancia con Saturno", "Ninguna"], "a": "1:2:4 con Europa y Ganímedes", "e": "Esta danza gravitacional entre lunas mantiene su órbita excéntrica y la fricción alta."}
            ]
        }
    },
    "Europa": {
        "tipo": "Luna de Júpiter", "color": "🧊", "desc": "Una luna de hielo con un misterioso océano subterráneo.",
        "quiz": {
            "normal": [
                {"q": "¿De qué está cubierta la superficie de Europa?", "o": ["Roca oscura", "Una capa gruesa de hielo", "Lava seca"], "a": "Una capa gruesa de hielo", "e": "Es como una inmensa bola de billar blanca y rayada."},
                {"q": "¿Qué creen los científicos que hay debajo de todo ese hielo?", "o": ["Oro macizo", "Un inmenso océano de agua líquida", "Fuego puro"], "a": "Un inmenso océano de agua líquida", "e": "Contiene más agua líquida que todos los océanos de la Tierra juntos."},
                {"q": "¿A qué planeta orbita?", "o": ["Saturno", "Urano", "Júpiter"], "a": "Júpiter", "e": "Es una de las cuatro famosas lunas galileanas."},
                {"q": "¿Europa es un buen lugar para buscar vida extraterrestre?", "o": ["Sí", "No"], "a": "Sí", "e": "Donde hay agua líquida y calor geotérmico, podría haber vida microscópica."},
                {"q": "¿Quién la descubrió junto con otras tres lunas en 1610?", "o": ["Isaac Newton", "Galileo Galilei", "Albert Einstein"], "a": "Galileo Galilei", "e": "Las descubrió usando un telescopio inventado por él mismo."}
            ],
            "pro master": [
                {"q": "¿Qué mecanismo calienta el interior de Europa para que su océano no se congele?", "o": ["El viento solar", "El calentamiento por fricción de marea con Júpiter", "Su núcleo radioactivo exclusivo"], "a": "El calentamiento por fricción de marea con Júpiter", "e": "El mismo mecanismo que crea volcanes en Io derrite el hielo interior de Europa."},
                {"q": "¿Qué lanza a veces Europa al espacio desde las grietas de su superficie?", "o": ["Rocas calientes", "Géiseres de vapor de agua", "Lava de amoníaco"], "a": "Géiseres de vapor de agua", "e": "El telescopio Hubble ha detectado estos chorros de agua saliendo al espacio."},
                {"q": "¿Qué misión de la NASA está diseñada para investigar su habitabilidad en los próximos años?", "o": ["Europa Clipper", "Cassini 2", "Artemis"], "a": "Europa Clipper", "e": "Hará docenas de sobrevuelos cercanos para escanear su hielo y océano."},
                {"q": "¿Qué compuesto da el tinte rojizo a las grandes fracturas de su superficie?", "o": ["Óxido de hierro", "Sales (como sulfato de magnesio) irradiadas", "Plástico alienígena"], "a": "Sales (como sulfato de magnesio) irradiadas", "e": "El agua del océano sale, se congela y la fuerte radiación de Júpiter cambia su color."},
                {"q": "¿Podría haber fuentes hidrotermales en su fondo oceánico oscuro?", "o": ["Sí, es una teoría principal", "Es físicamente imposible"], "a": "Sí, es una teoría principal", "e": "Estas fuentes aportarían la química y la energía necesarias para la vida sin luz solar."}
            ]
        }
    },
    "Ganímedes": {
        "tipo": "Luna de Júpiter", "color": "🔘", "desc": "La luna más grande de todo el sistema solar.",
        "quiz": {
            "normal": [
                {"q": "¿A qué planeta orbita Ganímedes?", "o": ["Saturno", "Tierra", "Júpiter"], "a": "Júpiter", "e": "Es la luna más grande de Júpiter y de todo nuestro sistema solar."},
                {"q": "¿Es Ganímedes más grande que el planeta Mercurio?", "o": ["Sí", "No"], "a": "Sí", "e": "Es inmensa, gana en tamaño aunque Mercurio pesa un poco más."},
                {"q": "¿De qué está hecha su superficie?", "o": ["Hielo y roca", "Lava pura", "Gas denso"], "a": "Hielo y roca", "e": "Es una mezcla de zonas antiguas oscuras y zonas más jóvenes claras."},
                {"q": "¿Se cree que tiene un océano bajo su gruesa corteza helada?", "o": ["Sí", "No"], "a": "Sí", "e": "Podría tener incluso más agua que la luna Europa, pero enterrada más profundo."},
                {"q": "¿Tiene cráteres en su superficie?", "o": ["Sí, muchos", "No, ninguno"], "a": "Sí, muchos", "e": "Especialmente en sus zonas oscuras más antiguas."}
            ],
            "pro master": [
                {"q": "¿Qué característica geofísica única tiene Ganímedes entre todas las lunas conocidas?", "o": ["Tiene un sistema de anillos", "Tiene su propio campo magnético global", "Tiene tormentas de arena"], "a": "Tiene su propio campo magnético global", "e": "Es la única luna que genera una magnetosfera a través de su núcleo de hierro líquido."},
                {"q": "¿Qué produce hermosas auroras en los polos de Ganímedes?", "o": ["La interacción de su campo magnético con el de Júpiter", "Volcanes invisibles", "El viento estelar directo"], "a": "La interacción de su campo magnético con el de Júpiter", "e": "Observar la oscilación de estas auroras con el Hubble confirmó su océano interno."},
                {"q": "¿Cuántas capas de hielo y océanos apilados podría tener según los modelos teóricos?", "o": ["Solo 1 océano bajo la corteza", "Varias capas alternas (como un sándwich de agua y hielos densos)", "Cero capas"], "a": "Varias capas alternas (como un sándwich de agua y hielos densos)", "e": "Las inmensas presiones pueden formar tipos de hielo extraños que son más pesados que el agua."},
                {"q": "¿Qué nave espacial de la Agencia Espacial Europea (ESA) se dirige a orbitarla exclusivamente?", "o": ["Europa Clipper", "JUICE (Jupiter Icy Moons Explorer)", "Juno"], "a": "JUICE (Jupiter Icy Moons Explorer)", "e": "Se convertirá en la primera nave en orbitar una luna de otro planeta de forma permanente."},
                {"q": "¿Ganímedes tiene algún tipo de atmósfera?", "o": ["No tiene absolutamente nada", "Una muy delgada (exosfera) de oxígeno", "Es densa como la de Venus"], "a": "Una muy delgada (exosfera) de oxígeno", "e": "La radiación descompone el hielo de la superficie liberando oxígeno débilmente."}
            ]
        }
    },
    "Calisto": {
        "tipo": "Luna de Júpiter", "color": "🌑", "desc": "La luna más antigua y acribillada a cráteres de Júpiter.",
        "quiz": {
            "normal": [
                {"q": "¿A qué planeta pertenece Calisto?", "o": ["Marte", "Júpiter", "Urano"], "a": "Júpiter", "e": "Es la cuarta luna galileana y la más alejada de las grandes."},
                {"q": "¿Su superficie está cubierta principalmente de qué?", "o": ["Volcanes activos", "Cráteres de impacto", "Lagos de metano"], "a": "Cráteres de impacto", "e": "Tiene cráteres sobre cráteres; es la superficie más acribillada del sistema solar."},
                {"q": "¿Cambia mucho la superficie de Calisto actualmente?", "o": ["Sí, tiene fuertes terremotos", "No, está muerta hace miles de millones de años"], "a": "No, está muerta hace miles de millones de años", "e": "A diferencia de Io o Europa, su superficie no se renueva."},
                {"q": "¿Es una luna grande o pequeña en el sistema solar?", "o": ["Muy grande", "Muy pequeña"], "a": "Muy grande", "e": "Es la tercera luna más grande del sistema solar (casi del tamaño de Mercurio)."},
                {"q": "¿De qué está compuesta en general?", "o": ["Mitad hielo y mitad roca", "Solo lava fundida", "Solo gas comprimido"], "a": "Mitad hielo y mitad roca", "e": "Es una mezcla bastante uniforme a diferencia de otras lunas."}
            ],
            "pro master": [
                {"q": "¿Por qué tiene tantos cráteres en comparación con la luna Europa?", "o": ["Atrae más meteoritos por su gravedad", "No tiene actividad geológica térmica que derrita y borre los cráteres", "Por culpa de los cometas"], "a": "No tiene actividad geológica térmica que derrita y borre los cráteres", "e": "Al estar muy lejos, Júpiter no la calienta por fricción de marea."},
                {"q": "¿Cómo se llama su enorme y antigua cuenca de impacto multi-anillo?", "o": ["Stickney", "Valhalla", "Cráter de Chicxulub"], "a": "Valhalla", "e": "Es una de las estructuras de impacto más grandes y misteriosas conocidas."},
                {"q": "¿Los científicos creen que tiene un océano líquido interno?", "o": ["No, está completamente congelada", "Sí, muy profundo e hipersalino, descubierto por campos magnéticos", "Es todo agua en el centro"], "a": "Sí, muy profundo e hipersalino, descubierto por campos magnéticos", "e": "Las lecturas de la sonda Galileo sugieren una capa conductora profunda."},
                {"q": "¿Por qué Calisto se considera una excelente base futura para misiones humanas a Júpiter?", "o": ["Tiene aire para respirar", "Está fuera del cinturón de radiación letal de Júpiter y tiene agua", "Tiene vegetación alienígena"], "a": "Está fuera del cinturón de radiación letal de Júpiter y tiene agua", "e": "Sería un puerto seguro para la exploración humana en el futuro distante."},
                {"q": "¿Cómo es el interior de Calisto comparado con la Tierra?", "o": ["Totalmente diferenciado en núcleo, manto y corteza", "Parcialmente diferenciado (una mezcla pastosa de roca y hielo)"], "a": "Parcialmente diferenciado (una mezcla pastosa de roca y hielo)", "e": "Nunca se calentó lo suficiente en su formación para separar el metal pesado del hielo ligero."}
            ]
        }
    },
    "Saturno": {
        "tipo": "Planeta", "color": "🪐", "desc": "El gigante con los anillos más espectaculares.",
        "lunas": ["Titán"],
        "quiz": {
            "normal": [
                {"q": "¿Por qué es famoso Saturno?", "o": ["Por ser de color rojo", "Por sus increíbles anillos gigantes", "Por no tener lunas"], "a": "Por sus increíbles anillos gigantes", "e": "Aunque otros planetas tienen anillos, los de Saturno son inmensos y brillantes."},
                {"q": "¿De qué están hechos sus anillos?", "o": ["Fuego espacial", "Pedazos de hielo y roca", "Nubes gaseosas"], "a": "Pedazos de hielo y roca", "e": "Son miles de millones de fragmentos cubiertos de hielo brillante."},
                {"q": "¿Es Saturno un planeta sólido en el que puedas pararte?", "o": ["Sí", "No, es un gigante gaseoso"], "a": "No, es un gigante gaseoso", "e": "Está hecho principalmente de gases ligeros."},
                {"q": "¿Qué tormenta extraña tiene en su polo norte?", "o": ["Un huracán de fuego", "Un vórtice/tormenta con forma de hexágono", "Un triángulo oscuro"], "a": "Un vórtice/tormenta con forma de hexágono", "e": "Es una de las geometrías más misteriosas del sistema solar."},
                {"q": "Si pudieras poner a Saturno en una bañera gigante llena de agua, ¿qué pasaría?", "o": ["Se hundiría como piedra", "Flotaría", "Explotaría"], "a": "Flotaría", "e": "Es el único planeta con una densidad menor que la del agua."}
            ],
            "pro master": [
                {"q": "¿A qué se deben las misteriosas divisiones oscuras en sus anillos (como la División de Cassini)?", "o": ["Cortes láser alienígenas", "La gravedad de pequeñas lunas 'pastoras' que limpian la zona", "Es una sombra del planeta"], "a": "La gravedad de pequeñas lunas 'pastoras' que limpian la zona", "e": "Estas pequeñas lunas moldean y mantienen el orden en los anillos."},
                {"q": "¿Qué pasará con los anillos de Saturno en un futuro distante?", "o": ["Crecerán y atraparán a la Tierra", "Desaparecerán cayendo al planeta en forma de lluvia de hielo", "Se volverán roca sólida"], "a": "Desaparecerán cayendo al planeta en forma de lluvia de hielo", "e": "Los científicos estiman que podrían desaparecer en 100 millones de años."},
                {"q": "¿Cuál es el espesor promedio de sus inmensos anillos?", "o": ["Apenas unos 10 metros de grosor", "1,000 kilómetros", "100 kilómetros"], "a": "Apenas unos 10 metros de grosor", "e": "A pesar de abarcar cientos de miles de kilómetros de ancho, son extremadamente delgados, ¡como una hoja de papel a escala!"},
                {"q": "¿Cuántas lunas conocidas tiene Saturno (hasta descubrimientos recientes)?", "o": ["Solo 1", "Alrededor de 146", "Exactamente 50"], "a": "Alrededor de 146", "e": "Recientemente destronó a Júpiter como el planeta con más lunas confirmadas."},
                {"q": "¿Qué sonda exploró profundamente Saturno y sus lunas durante 13 años antes de inmolarse en su atmósfera?", "o": ["Cassini-Huygens", "Curiosity", "Hubble"], "a": "Cassini-Huygens", "e": "Nos brindó casi todo el conocimiento moderno que tenemos de Saturno."}
            ]
        }
    },
    "Titán": {
        "tipo": "Luna de Saturno", "color": "🌫️", "desc": "La única luna con atmósfera espesa y lagos líquidos.",
        "quiz": {
            "normal": [
                {"q": "¿A qué planeta pertenece la luna Titán?", "o": ["Júpiter", "Urano", "Saturno"], "a": "Saturno", "e": "Es la joya más grande del sistema de Saturno."},
                {"q": "¿Qué característica tiene Titán que ninguna otra luna del sistema solar tiene?", "o": ["Una atmósfera densa y nublada", "Anillos de oro", "Forma de cubo"], "a": "Una atmósfera densa y nublada", "e": "No puedes ver su superficie desde el espacio debido al smog."},
                {"q": "¿Es Titán grande o pequeña?", "o": ["Muy grande", "Muy pequeña"], "a": "Muy grande", "e": "Es la segunda luna más grande del sistema solar, mayor que el planeta Mercurio."},
                {"q": "¿Hay lagos líquidos en la superficie de Titán?", "o": ["Sí, hay mares y lagos", "No, es un desierto seco"], "a": "Sí, hay mares y lagos", "e": "Pero no te gustaría nadar en ellos, ¡no son de agua!"},
                {"q": "¿De qué están hechos los mares, ríos y la lluvia en Titán?", "o": ["Agua salada", "Metano y etano líquidos", "Lava volcánica"], "a": "Metano y etano líquidos", "e": "Hace tanto frío (-179 °C) que el gas natural se vuelve líquido."}
            ],
            "pro master": [
                {"q": "¿Qué gas compone principalmente la gruesa atmósfera de Titán?", "o": ["Oxígeno", "Nitrógeno", "Helio puro"], "a": "Nitrógeno", "e": "¡Igual que la atmósfera de la Tierra! Es aproximadamente un 95% de nitrógeno."},
                {"q": "¿Qué sonda humana logró aterrizar con éxito en la superficie de Titán en 2005?", "o": ["Voyager 2", "La sonda Huygens (parte de la misión Cassini)", "El rover Spirit"], "a": "La sonda Huygens (parte de la misión Cassini)", "e": "Nos envió fotos inéditas desde la superficie con 'rocas' de hielo."},
                {"q": "¿De qué están hechas las inmensas dunas oscuras cerca del ecuador de Titán?", "o": ["Arena de silicio normal", "Partículas orgánicas complejas (plásticos/hidrocarburos) caídas del cielo", "Montañas de carbón caliente"], "a": "Partículas orgánicas complejas (plásticos/hidrocarburos) caídas del cielo", "e": "Parecen inmensos desiertos de arena de café molido alienígena."},
                {"q": "¿Por qué sería teóricamente muy fácil volar para un humano en Titán?", "o": ["Porque no hay absolutamente nada de gravedad", "Por la combinación de baja gravedad y una atmósfera súper densa", "Por el viento solar constante"], "a": "Por la combinación de baja gravedad y una atmósfera súper densa", "e": "¡Podrías ponerte alas artificiales en los brazos y despegar corriendo!"},
                {"q": "¿Qué misión de vanguardia (un helicóptero) planea enviar la NASA a Titán en 2028?", "o": ["Dragonfly", "Ingenuity 2", "Artemis 4"], "a": "Dragonfly", "e": "Este dron saltará de lugar en lugar estudiando la química prebiótica de la luna."}
            ]
        }
    },
    "Urano": {
        "tipo": "Planeta", "color": "🧊", "desc": "El gigante de hielo que gira de lado.",
        "lunas": ["Titania"],
        "quiz": {
            "normal": [
                {"q": "¿De qué color se ve el planeta Urano?", "o": ["Rojo fuerte", "Azul claro/Cian", "Amarillo brillante"], "a": "Azul claro/Cian", "e": "Su color se debe al gas metano en su alta atmósfera."},
                {"q": "¿Urano es frío o caliente?", "o": ["Es el planeta más frío del sistema solar", "El más caliente de todos"], "a": "Es el planeta más frío del sistema solar", "e": "A pesar de no ser el más alejado, sus temperaturas son récord, por eso es un 'Gigante de Hielo'."},
                {"q": "¿Urano tiene anillos?", "o": ["No, ninguno", "Sí, pero son oscuros y difíciles de ver", "Sí, más grandes que los de Saturno"], "a": "Sí, pero son oscuros y difíciles de ver", "e": "Tiene varios anillos estrechos compuestos de material oscuro."},
                {"q": "¿Qué peculiaridad tiene la forma en la que gira (su rotación)?", "o": ["Gira perfectamente derecho", "Gira acostado o de lado (casi a 98 grados)", "Gira al revés como Venus"], "a": "Gira acostado o de lado (casi a 98 grados)", "e": "Prácticamente rueda sobre su órbita alrededor del Sol."},
                {"q": "¿Fue Urano descubierto a simple vista o con un instrumento?", "o": ["A simple vista en la antigüedad", "Con un telescopio en 1781 por William Herschel"], "a": "Con un telescopio en 1781 por William Herschel", "e": "Fue el primer planeta descubierto en la historia moderna."}
            ],
            "pro master": [
                {"q": "¿Por qué los científicos creen que Urano gira de lado?", "o": ["Decisión cósmica", "Un impacto colosal con un objeto del tamaño de la Tierra en sus inicios", "El viento del Sol lo empujó"], "a": "Un impacto colosal con un objeto del tamaño de la Tierra en sus inicios", "e": "Este inmenso choque literalmente 'noqueó' al planeta de costado."},
                {"q": "¿Cuánto duran las extrañas estaciones del año en Urano?", "o": ["3 meses", "21 años terrestres de sol y luego 21 de oscuridad por polo", "No tiene estaciones"], "a": "21 años terrestres de sol y luego 21 de oscuridad por polo", "e": "Al estar acostado, cada polo apunta al Sol por décadas continuas."},
                {"q": "¿Qué única nave espacial en la historia ha pasado y tomado fotos cerca de Urano?", "o": ["Sonda Cassini", "Voyager 2 en 1986", "Telescopio James Webb"], "a": "Voyager 2 en 1986", "e": "Realizó un histórico sobrevuelo y no hemos vuelto desde entonces."},
                {"q": "¿De dónde provienen los nombres de la mayoría de las lunas de Urano (como Titania y Oberón)?", "o": ["Números romanos", "Personajes de las obras de William Shakespeare y Alexander Pope", "Dioses griegos menores"], "a": "Personajes de las obras de William Shakespeare y Alexander Pope", "e": "Es una tradición única en la nomenclatura del sistema solar."},
                {"q": "¿Cómo es el interior bajo las nubes de los Gigantes de Hielo (Urano y Neptuno)?", "o": ["Gas puro y caliente hasta el centro", "Un fluido caliente y denso de 'hielos' (agua, amoníaco, metano) sobre un núcleo rocoso", "Un cubo sólido de hielo de agua"], "a": "Un fluido caliente y denso de 'hielos' (agua, amoníaco, metano) sobre un núcleo rocoso", "e": "En astrofísica, moléculas como el agua o amoníaco se llaman 'hielos', aunque ahí estén a miles de grados bajo presión."}
            ]
        }
    },
    "Titania": {
        "tipo": "Luna de Urano", "color": "🌑", "desc": "La luna más grande de Urano con inmensos cañones.",
        "quiz": {
            "normal": [
                {"q": "¿A qué planeta pertenece la luna Titania?", "o": ["Neptuno", "Urano", "Saturno"], "a": "Urano", "e": "Es la reina de las lunas de su sistema."},
                {"q": "¿Es Titania la luna más grande de Urano?", "o": ["Sí", "No"], "a": "Sí", "e": "Aunque comparada con la luna de la Tierra es un poco más pequeña."},
                {"q": "¿Quién es Titania en la literatura antigua?", "o": ["La Reina de las Hadas en una obra de Shakespeare", "Una diosa romana", "Una bruja de cuentos"], "a": "La Reina de las Hadas en una obra de Shakespeare", "e": "Aparece en 'El sueño de una noche de verano'."},
                {"q": "¿De qué materiales está hecha Titania?", "o": ["Solo gas comprimido", "Aproximadamente mitad hielo y mitad roca", "Lava oscura"], "a": "Aproximadamente mitad hielo y mitad roca", "e": "Es una composición típica de las lunas frías exteriores."},
                {"q": "¿Tiene características impresionantes en su superficie?", "o": ["Sí, enormes cañones y fallas", "No, es completamente plana y lisa"], "a": "Sí, enormes cañones y fallas", "e": "Se ven como gigantescos 'arañazos' en la luna."}
            ],
            "pro master": [
                {"q": "¿Cómo se formaron probablemente los inmensos cañones en Titania (como Messina Chasmata)?", "o": ["El interior líquido se congeló y se expandió, rompiendo la corteza de hielo", "Por el impacto de un millón de asteroides", "Volcanes de fuego los excavaron"], "a": "El interior líquido se congeló y se expandió, rompiendo la corteza de hielo", "e": "Es igual a cuando pones una botella llena de agua en el congelador y el hielo la rompe."},
                {"q": "¿Tiene Titania una atmósfera apreciable?", "o": ["Sí, densa de metano", "No, solo una posibilidad remota de una traza infinitesimal de CO2", "Sí, pero de oxígeno"], "a": "No, solo una posibilidad remota de una traza infinitesimal de CO2", "e": "Es demasiado pequeña y fría para retener una atmósfera de verdad."},
                {"q": "¿Quién descubrió Titania?", "o": ["William Herschel", "Galileo", "Isaac Newton"], "a": "William Herschel", "e": "La descubrió el mismo astrónomo que descubrió el planeta Urano 6 años antes."},
                {"q": "¿Tenemos mapas completos de toda la superficie de Titania?", "o": ["Sí, mapas 3D al 100%", "No, la Voyager 2 solo pudo mapear cerca del 40% (el hemisferio iluminado)", "Solo tenemos dibujos"], "a": "No, la Voyager 2 solo pudo mapear cerca del 40% (el hemisferio iluminado)", "e": "El otro lado estaba en la oscuridad del invierno de décadas de Urano."},
                {"q": "¿Por qué hay menos cráteres gigantes en Titania que en la luna Calisto?", "o": ["Nunca cayeron meteoritos allí", "Antiguo criovulcanismo (erupciones de hielo y agua) resurfacing la luna en el pasado", "Los aliens los limpiaron"], "a": "Antiguo criovulcanismo (erupciones de hielo y agua) resurfacing la luna en el pasado", "e": "El hielo se derritió y borró las cicatrices más viejas antes de volver a congelarse."}
            ]
        }
    },
    "Neptuno": {
        "tipo": "Planeta", "color": "🔵", "desc": "El lejano gigante azul, hogar de los vientos más rápidos.",
        "lunas": ["Tritón"],
        "quiz": {
            "normal": [
                {"q": "¿De qué color es Neptuno?", "o": ["Verde brillante", "Azul oscuro/Cobalto", "Gris metálico"], "a": "Azul oscuro/Cobalto", "e": "Es un tono azul mucho más profundo e intenso que el de Urano."},
                {"q": "¿Es el último planeta oficial del sistema solar?", "o": ["Sí", "No, es Plutón"], "a": "Sí", "e": "Tras la reclasificación de Plutón, Neptuno es el 8vo y último."},
                {"q": "¿Hace calor o frío en Neptuno?", "o": ["Frío extremo", "Calor abrasador"], "a": "Frío extremo", "e": "Su lejanía al Sol lo convierte en un mundo gélido."},
                {"q": "¿Tiene tormentas o es un planeta tranquilo?", "o": ["No, es muy tranquilo", "Sí, tormentas y los vientos más fuertes del sistema solar"], "a": "Sí, tormentas y los vientos más fuertes del sistema solar", "e": "Los huracanes allí son aterradores."},
                {"q": "¿Tiene anillos a su alrededor?", "o": ["Sí, oscuros y delgados", "No tiene ninguno"], "a": "Sí, oscuros y delgados", "e": "Tienen zonas más gruesas llamadas 'arcos'."}
            ],
            "pro master": [
                {"q": "¿A qué velocidad pueden soplar los vientos en las tormentas de Neptuno?", "o": ["A más de 2,000 km/h (velocidad supersónica)", "150 km/h máximo", "500 km/h"], "a": "A más de 2,000 km/h (velocidad supersónica)", "e": "Estos vientos rompen la barrera del sonido de la Tierra, son un misterio termodinámico."},
                {"q": "¿Cómo fue descubierto Neptuno en 1846?", "o": ["Por accidente con un telescopio nuevo", "Mediante predicciones y cálculos matemáticos", "En un mapa antiguo maya"], "a": "Mediante predicciones y cálculos matemáticos", "e": "Matemáticos notaron que la gravedad de 'algo invisible' perturbaba la órbita de Urano y calcularon su posición exacta."},
                {"q": "¿Qué gas atmosférico le da su color azul oscuro característico?", "o": ["Ozono molecular", "Gas Metano", "Oxígeno líquido"], "a": "Gas Metano", "e": "El metano en la atmósfera absorbe fuertemente la luz roja del Sol y refleja el azul hacia nosotros."},
                {"q": "¿Qué era la 'Gran Mancha Oscura' observada en 1989?", "o": ["Un enorme volcán en erupción", "Una tormenta gigante del tamaño de la Tierra en el hemisferio sur", "Una luna nueva"], "a": "Una tormenta gigante del tamaño de la Tierra en el hemisferio sur", "e": "Fue observada por la Voyager 2, pero sorprendentemente desapareció años después."},
                {"q": "¿Por qué Neptuno es un planeta extremadamente tormentoso a pesar de estar tan lejos del Sol?", "o": ["Tiene un núcleo de antimateria", "Emite 2.6 veces más energía térmica de la que recibe del Sol", "Es mentira, no hay tormentas"], "a": "Emite 2.6 veces más energía térmica de la que recibe del Sol", "e": "Tiene una fuente de calor interna desconocida que impulsa sus violentos patrones climáticos."}
            ]
        }
    },
    "Tritón": {
        "tipo": "Luna de Neptuno", "color": "❄️", "desc": "La luna helada más grande de Neptuno con órbita al revés.",
        "quiz": {
            "normal": [
                {"q": "¿A qué planeta pertenece Tritón?", "o": ["Urano", "Neptuno", "Saturno"], "a": "Neptuno", "e": "Es la luna principal y dominante de Neptuno."},
                {"q": "¿De qué está cubierta su superficie?", "o": ["Lava volcánica", "Hielo brillante de nitrógeno y agua", "Arena del desierto"], "a": "Hielo brillante de nitrógeno y agua", "e": "Está congelado profundo y refleja mucha luz solar."},
                {"q": "¿Tritón es un lugar caliente o frío?", "o": ["Caliente", "Extremadamente frío (casi el cero absoluto)"], "a": "Extremadamente frío (casi el cero absoluto)", "e": "Es uno de los lugares más fríos medidos en el sistema solar (-235 °C)."},
                {"q": "¿Qué hace especial la forma en que orbita Tritón a su planeta?", "o": ["Orbita al revés (retrógrada) de la rotación de Neptuno", "No se mueve", "Hace espirales"], "a": "Orbita al revés (retrógrada) de la rotación de Neptuno", "e": "Va en sentido contrario, una rareza para una luna tan inmensa."},
                {"q": "¿Tritón nació junto a Neptuno o llegó de fuera?", "o": ["Nació de los anillos de Neptuno", "Fue capturado por la gravedad de Neptuno desde lejos"], "a": "Fue capturado por la gravedad de Neptuno desde lejos", "e": "Su órbita al revés es la prueba definitiva de que fue capturado."}
            ],
            "pro master": [
                {"q": "¿Qué fenómeno geológico asombroso descubrió la Voyager 2 en Tritón?", "o": ["Volcanes que expulsan fuego", "Géiseres activos de nitrógeno líquido (criovolcanes)", "Terremotos que dividen la luna"], "a": "Géiseres activos de nitrógeno líquido (criovolcanes)", "e": "Expulsan columnas de gas y polvo negro a kilómetros de altura en el espacio."},
                {"q": "¿De dónde proviene originariamente Tritón antes de ser capturado?", "o": ["Del Cinturón de Asteroides cercano a Marte", "Del lejano Cinturón de Kuiper (como Plutón)", "De una galaxia vecina"], "a": "Del lejano Cinturón de Kuiper (como Plutón)", "e": "Es un Objeto del Cinturón de Kuiper (KBO) capturado, muy similar a Plutón geológicamente."},
                {"q": "¿Qué le depara el futuro lejano a Tritón?", "o": ["Saldrá de su órbita y viajará al Sol", "Se acercará demasiado a Neptuno, se romperá y formará un anillo espectacular", "Se convertirá en un planeta"], "a": "Se acercará demasiado a Neptuno, se romperá y formará un anillo espectacular", "e": "Su órbita decae y eventualmente cruzará el Límite de Roche donde la gravedad lo destrozará."},
                {"q": "¿Qué es el extraño 'terreno de cantalupo' exclusivo de Tritón?", "o": ["Plantaciones alienígenas", "Una vasta superficie llena de depresiones que parece la piel de un melón", "Una llanura de cráteres de impacto perfectos"], "a": "Una vasta superficie llena de depresiones que parece la piel de un melón", "e": "Se cree que se formó por diapiro (masas de hielo cálido subiendo como en una lámpara de lava)."},
                {"q": "¿Tritón posee algún tipo de atmósfera?", "o": ["No, el frío la congela totalmente", "Sí, una atmósfera muy tenue de nitrógeno", "Sí, espesa de oxígeno"], "a": "Sí, una atmósfera muy tenue de nitrógeno", "e": "El débil calor del sol y el vulcanismo logran evaporar un poco del hielo de la superficie."}
            ]
        }
    }
}

# --- ESTADO DE LA APLICACIÓN ---
if 'quiz_active' not in st.session_state:
    st.session_state.quiz_active = False
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'current_step' not in st.session_state:
    st.session_state.current_step = 0
if 'answers_history' not in st.session_state:
    st.session_state.answers_history = []
if 'difficulty' not in st.session_state:
    st.session_state.difficulty = "normal"
if 'target_body' not in st.session_state:
    st.session_state.target_body = "Sol"
if 'current_questions' not in st.session_state:
    st.session_state.current_questions = []

# --- FUNCIONES DEL JUEGO ---
def start_quiz(body, diff):
    st.session_state.target_body = body
    st.session_state.difficulty = diff
    st.session_state.quiz_active = True
    st.session_state.current_step = 0
    st.session_state.score = 0
    st.session_state.answers_history = []
    
    try:
        questions = DATA[body]["quiz"][diff]
        st.session_state.current_questions = random.sample(questions, len(questions))
    except KeyError:
        st.error("⚠️ Error cargando el nivel.")
        st.session_state.quiz_active = False

def check_answer(choice, correct, explanation, question_text):
    is_correct = (choice == correct)
    if is_correct:
        st.session_state.score += 1
    
    st.session_state.answers_history.append({
        "q": question_text,
        "correct": is_correct,
        "explanation": explanation
    })
    st.session_state.current_step += 1

# --- INTERFAZ PRINCIPAL ---
st.title("🛰️ Centro de Control Orbital")
st.markdown("Bienvenido al simulador. Prepárate para explorar la galaxia y poner a prueba tu conocimiento astronómico.")

if not st.session_state.quiz_active:
    # --- PANTALLA: CENTRO DE CONTROL INTERACTIVO ---
    col1, col2 = st.columns([1.2, 2])
    
    with col1:
        st.markdown("<div class='dashboard-panel'>", unsafe_allow_html=True)
        st.subheader("🎛️ Panel de Navegación")
        # Mostrar todos los astros de la DATA
        search = st.selectbox("🎯 Elige un astro para investigar:", list(DATA.keys()))
        
        st.write("---")
        st.write("⚙️ **Configuración del Simulador:**")
        # Solo dos opciones de nivel
        diff_choice = st.radio("Dificultad de la Misión:", ["normal", "pro master"], horizontal=True)
        
        st.write("")
        if st.button("🚀 ¡INICIAR MISIÓN DE EXPLORACIÓN!"):
            start_quiz(search, diff_choice)
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        body = DATA[search]
        st.markdown(f"""
        <div class="planet-card">
            <h1 style="font-size: 3.5em; margin: 0; text-align: center;">{body['color']} {search}</h1>
            <div style="display: flex; justify-content: space-around; margin-top: 15px;">
                <span style="background: #1e293b; padding: 5px 15px; border-radius: 10px; border: 1px solid #3b82f6;"><strong>Clase:</strong> {body['tipo']}</span>
                <span style="background: #1e293b; padding: 5px 15px; border-radius: 10px; border: 1px solid #10b981;"><strong>Estado:</strong> Escaneado ✅</span>
            </div>
            <hr style="border-color: #334155; margin: 20px 0;">
            <p style='font-size: 1.3em; line-height: 1.6; text-align: center;'>{body['desc']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if "lunas" in body:
            st.info(f"🛰️ **Satélites destacables:** {', '.join(body['lunas'])}")

else:
    # --- PANTALLA: MODO TRIVIA EN CURSO ---
    total_q = len(st.session_state.current_questions)
    
    if st.session_state.current_step < total_q:
        q_data = st.session_state.current_questions[st.session_state.current_step]
        
        progress = st.session_state.current_step / total_q
        st.progress(progress)
        
        st.markdown(f"### Misión en curso: Explorando **{st.session_state.target_body}** (Nivel: {st.session_state.difficulty.upper()})")
        st.write(f"**Pregunta {st.session_state.current_step + 1} de {total_q}**")
        
        st.markdown(f"""
        <div class="planet-card" style="border-color: #60a5fa;">
            <h2 style='text-align: center;'>{q_data['q']}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        options = q_data['o'].copy()
        random.Random(q_data['q']).shuffle(options)
        
        st.write("---")
        cols = st.columns(len(options))
        for idx, option in enumerate(options):
            with cols[idx]:
                if st.button(option, key=f"opt_{idx}"):
                    check_answer(option, q_data['a'], q_data['e'], q_data['q'])
                    st.rerun()
    else:
        # --- PANTALLA: RESULTADOS Y CELEBRACIÓN / GAME OVER ---
        score = st.session_state.score
        
        if score >= 3:
            # VICTORIA
            st.markdown("<h1 style='text-align: center;'>🎉 ¡Misión Completada con Éxito! 🎉</h1>", unsafe_allow_html=True)
            st.balloons()
            with st.spinner("Procesando medalla estelar..."):
                time.sleep(1.5)
            st.snow()
            
            if score == total_q:
                msg = "¡ERES UN COMANDANTE GALÁCTICO! 🌟\nConoces el universo como la palma de tu mano."
            else:
                msg = "¡Buen trabajo, Explorador! 🛰️\nTu conocimiento astronómico es brillante."
                
            st.success(f"Puntaje: {score}/{total_q} - {msg}")
            
        else:
            # GAME OVER: SUPERNOVA
            st.markdown("""
            <div class='game-over'>
                <h1 style='font-size: 5em; color: #ef4444;'>☀️💥🌋</h1>
                <h2>¡GAME OVER CRÍTICO!</h2>
                <p style='font-size: 1.2em;'>Tu falta de conocimiento desestabilizó el núcleo... <strong>¡El Sol se ha convertido en una Supernova!</strong></p>
                <img src="https://media.giphy.com/media/ceHKRKMR6Ojao/giphy.gif" style="max-width: 400px; border-radius: 15px; margin: 20px 0;">
            </div>
            """, unsafe_allow_html=True)
            st.error(f"Puntaje: {score}/{total_q} - ¡Cadete, debes volver urgentemente a la academia de vuelo espacial!")

        # Resumen de respuestas
        st.write("---")
        with st.expander("📋 Ver reporte de la caja negra (Respuestas)"):
            for idx, res in enumerate(st.session_state.answers_history):
                if res["correct"]:
                    st.markdown(f"✅ **Q{idx+1}:** {res['q']}  \n*¡Acertaste! {res['explanation']}*")
                else:
                    st.markdown(f"❌ **Q{idx+1}:** {res['q']}  \n*Error.* {res['explanation']}")
        
        st.write("")
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            if st.button("🔄 Volver al Centro de Control"):
                st.session_state.quiz_active = False
                st.rerun()

# --- FOOTER ACTUALIZADO ---
st.markdown("---")
st.markdown("<p style='text-align: center; color: #94a3b8;'>👨‍🚀 Creado para futuros astronautas | Desarrollado por ASC y HFSR 🚀</p>", unsafe_allow_html=True)
