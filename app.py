import streamlit as st
import random
import time

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Explorador Espacial Pro",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILOS CSS PERSONALIZADOS ---
st.markdown("""
<style>
    .main {
        background-color: #0f172a;
        color: #f1f5f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #1e293b;
        color: white;
        border: 1px solid #334155;
    }
    .stButton>button:hover {
        border-color: #3b82f6;
        color: #3b82f6;
    }
    .planet-card {
        background: rgba(30, 41, 59, 0.7);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #334155;
        margin-bottom: 20px;
    }
    .quiz-container {
        background-color: #1e293b;
        padding: 30px;
        border-radius: 20px;
        border-left: 5px solid #3b82f6;
    }
    h1, h2, h3 {
        color: #60a5fa !important;
    }
</style>
""", unsafe_allow_all_stdio=True)

# --- DATOS DEL SISTEMA SOLAR ---
DATA = {
    "Sol": {
        "tipo": "Estrella", "color": "🟡", "desc": "El centro de todo. Una enana amarilla gigante.",
        "quiz": {
            "fácil": {"q": "¿De qué color vemos al Sol?", "o": ["Verde", "Amarillo/Blanco", "Azul"], "a": "Amarillo/Blanco", "e": "Es una enana amarilla."},
            "medio": {"q": "¿Qué proceso genera la energía del Sol?", "o": ["Combustión", "Fisión", "Fusión Nuclear"], "a": "Fusión Nuclear", "e": "Fusiona hidrógeno para crear helio."},
            "pro master": {"q": "¿Cuál es la temperatura aproximada en el núcleo del Sol?", "o": ["15 millones °C", "5,000 °C", "1 millón °C"], "a": "15 millones °C", "e": "¡Es increíblemente caliente!"}
        }
    },
    "Mercurio": {
        "tipo": "Planeta", "color": "🔘", "desc": "Pequeño y veloz. El más cercano al sol.",
        "quiz": {
            "fácil": {"q": "¿Es Mercurio el planeta más grande?", "o": ["Sí", "No"], "a": "No", "e": "Es el más pequeño."},
            "medio": {"q": "¿Cuánto dura un año en Mercurio?", "o": ["88 días", "365 días", "10 días"], "a": "88 días", "e": "Viaja muy rápido alrededor del Sol."},
            "pro master": {"q": "¿Por qué Mercurio tiene cráteres tan visibles?", "o": ["Por volcanes", "Por falta de atmósfera", "Por el viento solar"], "a": "Por falta de atmósfera", "e": "No tiene escudo contra meteoritos."}
        }
    },
    "Tierra": {
        "tipo": "Planeta", "color": "🌍", "desc": "Nuestro hogar azul con agua líquida.",
        "quiz": {
            "fácil": {"q": "¿Cuántas lunas tiene la Tierra?", "o": ["0", "1", "2"], "a": "1", "e": "Solo tenemos a Selene (La Luna)."},
            "medio": {"q": "¿Qué gas es el más abundante en nuestra atmósfera?", "o": ["Oxígeno", "Nitrógeno", "CO2"], "a": "Nitrógeno", "e": "78% es Nitrógeno."},
            "pro master": {"q": "¿Cuál es la velocidad de rotación de la Tierra en el ecuador?", "o": ["1,670 km/h", "500 km/h", "10,000 km/h"], "a": "1,670 km/h", "e": "¡Aunque no lo sientas, vas volando!"}
        }
    },
    "Marte": {
        "tipo": "Planeta", "color": "🔴", "desc": "El planeta rojo. Hogar del Monte Olimpo.",
        "lunas": ["Phobos", "Deimos"],
        "quiz": {
            "fácil": {"q": "¿Por qué es rojo Marte?", "o": ["Tiene fuego", "Tiene mucho hierro oxidado", "Es pintura"], "a": "Tiene mucho hierro oxidado", "e": "Como una bicicleta vieja bajo la lluvia."},
            "medio": {"q": "¿Cómo se llama el volcán más grande de Marte?", "o": ["Etna", "Monte Olimpo", "Vesubio"], "a": "Monte Olimpo", "e": "Es 3 veces más alto que el Everest."},
            "pro master": {"q": "¿Cuál es el periodo orbital de Marte?", "o": ["687 días", "365 días", "1.5 años"], "a": "687 días", "e": "Casi el doble que la Tierra."}
        }
    },
    "Phobos": {
        "tipo": "Luna de Marte", "color": "🌑", "desc": "La luna más grande de Marte, tiene forma de papa.",
        "quiz": {
            "fácil": {"q": "¿A qué planeta pertenece Phobos?", "o": ["Júpiter", "Marte", "Saturno"], "a": "Marte", "e": "Es la pareja de Deimos."},
            "medio": {"q": "¿Qué forma tiene Phobos?", "o": ["Esfera perfecta", "Irregular (como papa)", "Plana"], "a": "Irregular (como papa)", "e": "No tiene suficiente gravedad para ser redonda."},
            "pro master": {"q": "¿Qué pasará con Phobos en el futuro?", "o": ["Chocará con Marte", "Se irá al espacio", "Se volverá un sol"], "a": "Chocará con Marte", "e": "Se acerca 2 metros cada 100 años."}
        }
    },
    "Júpiter": {
        "tipo": "Planeta", "color": "🟠", "desc": "Rey de los planetas. Un gigante gaseoso.",
        "lunas": ["Io", "Europa", "Ganímedes", "Calisto"],
        "quiz": {
            "fácil": {"q": "¿Qué es la Gran Mancha Roja?", "o": ["Un continente", "Una tormenta", "Un océano"], "a": "Una tormenta", "e": "Lleva activa siglos."},
            "medio": {"q": "¿Cuántas tierras caben dentro de Júpiter?", "o": ["10", "1,300", "500"], "a": "1,300", "e": "¡Es inmenso!"},
            "pro master": {"q": "¿De qué está hecho principalmente Júpiter?", "o": ["Roca", "Agua", "Hidrógeno y Helio"], "a": "Hidrógeno y Helio", "e": "Es casi una estrella fallida."}
        }
    },
    "Europa": {
        "tipo": "Luna de Júpiter", "color": "🧊", "desc": "Cuerpo helado. Posible océano interno.",
        "quiz": {
            "fácil": {"q": "¿De qué está cubierta la superficie de Europa?", "o": ["Roca", "Hielo", "Lava"], "a": "Hielo", "e": "Es una bola de nieve gigante."},
            "medio": {"q": "¿Qué buscan los científicos bajo el hielo de Europa?", "o": ["Oro", "Agua líquida/Vida", "Fósiles de dinosaurio"], "a": "Agua líquida/Vida", "e": "Es el lugar más probable para hallar vida."},
            "pro master": {"q": "¿Quién descubrió esta luna?", "o": ["Newton", "Galileo Galilei", "Elon Musk"], "a": "Galileo Galilei", "e": "En 1610 con su telescopio casero."}
        }
    },
    "Titán": {
        "tipo": "Luna de Saturno", "color": "🟠", "desc": "La única luna con atmósfera densa y lagos de metano.",
        "quiz": {
            "fácil": {"q": "¿Tiene Titán una atmósfera?", "o": ["Sí", "No"], "a": "Sí", "e": "Es muy espesa y naranja."},
            "medio": {"q": "¿De qué son los lagos en Titán?", "o": ["Agua", "Metano líquido", "Lava"], "a": "Metano líquido", "e": "Hace demasiado frío para el agua líquida."},
            "pro master": {"q": "¿Cuál es el componente principal de su atmósfera?", "o": ["Oxígeno", "Nitrógeno", "Metano"], "a": "Nitrógeno", "e": "Igual que la Tierra, pero sin oxígeno."}
        }
    }
}

# --- INICIALIZACIÓN DE ESTADO ---
if 'quiz_active' not in st.session_state:
    st.session_state.quiz_active = False
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'current_step' not in st.session_state:
    st.session_state.current_step = 0
if 'answers_history' not in st.session_state:
    st.session_state.answers_history = []
if 'difficulty' not in st.session_state:
    st.session_state.difficulty = "fácil"

# --- LÓGICA DE TRIVIA ---
def start_quiz(diff):
    st.session_state.difficulty = diff
    st.session_state.quiz_active = True
    st.session_state.current_step = 0
    st.session_state.score = 0
    st.session_state.answers_history = []
    # Seleccionar 5 preguntas aleatorias de los cuerpos disponibles
    st.session_state.quiz_pool = random.sample(list(DATA.keys()), 5)

def next_question(choice, correct, body_name):
    is_correct = choice == correct
    if is_correct:
        st.session_state.score += 1
    
    st.session_state.answers_history.append({
        "body": body_name,
        "correct": is_correct,
        "explanation": DATA[body_name]["quiz"][st.session_state.difficulty]["e"]
    })
    st.session_state.current_step += 1

# --- INTERFAZ ---
st.title("🌌 Explorador del Sistema Solar 2.0")

if not st.session_state.quiz_active:
    # MODO EXPLORACIÓN
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("🚀 Menú de Navegación")
        search = st.selectbox("Elige un astro:", list(DATA.keys()))
        
        st.info("🎯 ¿Listo para el reto?")
        diff_choice = st.radio("Dificultad:", ["fácil", "medio", "pro master"], horizontal=True)
        if st.button("¡INICIAR TRIVIA GALÁCTICA!"):
            start_quiz(diff_choice)
            st.rerun()

    with col2:
        body = DATA[search]
        st.markdown(f"""
        <div class="planet-card">
            <h1>{body['color']} {search}</h1>
            <p style='font-size: 1.2em;'><strong>Tipo:</strong> {body['tipo']}</p>
            <hr>
            <p style='font-size: 1.1em;'>{body['desc']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if "lunas" in body:
            st.write("🛰️ **Lunas principales:** " + ", ".join(body["lunas"]))

else:
    # MODO TRIVIA (BLOQUEADO)
    if st.session_state.current_step < len(st.session_state.quiz_pool):
        body_name = st.session_state.quiz_pool[st.session_state.current_step]
        q_data = DATA[body_name]["quiz"][st.session_state.difficulty]
        
        st.progress((st.session_state.current_step) / 5)
        st.header(f"Pregunta {st.session_state.current_step + 1} de 5")
        
        with st.container():
            st.markdown(f"""
            <div class="quiz-container">
                <h3>Sobre: {body_name}</h3>
                <p style='font-size: 1.3em;'>{q_data['q']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.write("")
            for option in q_data['o']:
                if st.button(option, key=f"btn_{option}_{st.session_state.current_step}"):
                    next_question(option, q_data['a'], body_name)
                    st.rerun()
    else:
        # RESULTADOS FINALES
        st.balloons()
        st.header("🏁 ¡Misión Completada!")
        
        score = st.session_state.score
        if score == 5:
            msg = "¡ERES UN COMANDANTE GALÁCTICO! 🌟 No hay rincón del universo que no conozcas."
        elif score >= 3:
            msg = "¡Buen trabajo, Explorador! 🛰️ Estás listo para tu siguiente misión."
        else:
            msg = "¡Cadete! 👨‍🚀 Necesitas más horas en el simulador de vuelo, ¡pero lo hiciste bien!"
            
        st.success(f"Puntaje Final: {score}/5")
        st.write(f"### {msg}")
        
        with st.expander("Ver Resumen de Misión"):
            for res in st.session_state.answers_history:
                icon = "✅" if res["correct"] else "❌"
                st.write(f"{icon} **{res['body']}**: {res['explanation']}")
        
        if st.button("Volver al Centro de Control"):
            st.session_state.quiz_active = False
            st.rerun()

# --- FOOTER ---
st.markdown("---")
st.caption("Creado para futuros astronautas de 12 años | 🛰️ GitHub/Streamlit/Railway")
