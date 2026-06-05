import streamlit as st
import random

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
        transition: all 0.3s;
    }
    .stButton>button:hover {
        border-color: #3b82f6;
        color: #3b82f6;
        transform: scale(1.02);
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
""", unsafe_allow_html=True) # <-- AQUÍ ESTÁ LA CORRECCIÓN

# --- DATOS DEL SISTEMA SOLAR ---
DATA = {
    "Sol": {
        "tipo": "Estrella", "color": "🟡", "desc": "El centro de todo. Una enana amarilla gigante que nos da luz y calor.",
        "quiz": {
            "fácil": {"q": "¿De qué color vemos al Sol desde la Tierra?", "o": ["Verde", "Amarillo/Blanco", "Azul"], "a": "Amarillo/Blanco", "e": "Es una enana amarilla."},
            "medio": {"q": "¿Qué proceso genera la energía del Sol?", "o": ["Combustión", "Fisión", "Fusión Nuclear"], "a": "Fusión Nuclear", "e": "Fusiona hidrógeno para crear helio en su núcleo."},
            "pro master": {"q": "¿Cuál es la temperatura aproximada en el núcleo del Sol?", "o": ["15 millones °C", "5,000 °C", "1 millón °C"], "a": "15 millones °C", "e": "¡Es increíblemente caliente!"}
        }
    },
    "Mercurio": {
        "tipo": "Planeta", "color": "🔘", "desc": "Pequeño y veloz. Es el planeta más cercano al Sol y está lleno de cráteres.",
        "quiz": {
            "fácil": {"q": "¿Es Mercurio el planeta más grande?", "o": ["Sí", "No"], "a": "No", "e": "De hecho, es el más pequeño de todos."},
            "medio": {"q": "¿Cuánto dura un año en Mercurio?", "o": ["88 días", "365 días", "10 días"], "a": "88 días", "e": "Viaja muy rápido alrededor del Sol."},
            "pro master": {"q": "¿Por qué Mercurio tiene cráteres tan visibles?", "o": ["Por volcanes", "Por falta de atmósfera", "Por el viento solar"], "a": "Por falta de atmósfera", "e": "No tiene un escudo gaseoso que destruya los meteoritos antes de impactar."}
        }
    },
    "Tierra": {
        "tipo": "Planeta", "color": "🌍", "desc": "Nuestro hermoso hogar azul. El único lugar conocido con agua líquida en la superficie y vida.",
        "quiz": {
            "fácil": {"q": "¿Cuántas lunas tiene la Tierra?", "o": ["0", "1", "2"], "a": "1", "e": "Solo tenemos a nuestra compañera, la Luna."},
            "medio": {"q": "¿Qué gas es el más abundante en el aire que respiramos?", "o": ["Oxígeno", "Nitrógeno", "Dióxido de Carbono"], "a": "Nitrógeno", "e": "El 78% de nuestra atmósfera es Nitrógeno."},
            "pro master": {"q": "¿A qué velocidad gira la Tierra sobre sí misma en el ecuador?", "o": ["1,670 km/h", "500 km/h", "10,000 km/h"], "a": "1,670 km/h", "e": "¡Vas volando por el espacio aunque no lo sientas!"}
        }
    },
    "Marte": {
        "tipo": "Planeta", "color": "🔴", "desc": "El famoso planeta rojo. Tiene montañas altísimas y valles profundos.",
        "lunas": ["Phobos", "Deimos"],
        "quiz": {
            "fácil": {"q": "¿Por qué Marte se ve de color rojo?", "o": ["Tiene fuego", "Tiene mucho hierro oxidado", "Es pintura espacial"], "a": "Tiene mucho hierro oxidado", "e": "Su superficie es como una vieja bicicleta oxidada."},
            "medio": {"q": "¿Cómo se llama el volcán gigante de Marte?", "o": ["Monte Everest", "Monte Olimpo", "Monte Vesubio"], "a": "Monte Olimpo", "e": "¡Es unas tres veces más alto que el Monte Everest!"},
            "pro master": {"q": "¿Cuánto tarda Marte en dar una vuelta al Sol (su periodo orbital)?", "o": ["687 días", "365 días", "10 años"], "a": "687 días", "e": "Su año dura casi el doble que el nuestro en la Tierra."}
        }
    },
    "Phobos": {
        "tipo": "Luna de Marte", "color": "🌑", "desc": "La luna más grande de Marte. ¡Tiene forma de papa porque es muy pequeña!",
        "quiz": {
            "fácil": {"q": "¿A qué planeta orbita Phobos?", "o": ["Júpiter", "Marte", "Saturno"], "a": "Marte", "e": "Es la pareja inseparable de Deimos."},
            "medio": {"q": "¿Qué forma geométrica tiene Phobos?", "o": ["Esfera perfecta", "Irregular (como una papa)", "Plana"], "a": "Irregular (como una papa)", "e": "No tiene suficiente gravedad para aplastarse y hacerse redonda."},
            "pro master": {"q": "¿Qué destino le espera a Phobos en el futuro lejano?", "o": ["Chocará con Marte", "Saldrá volando al espacio", "Se volverá un pequeño planeta"], "a": "Chocará con Marte", "e": "La gravedad de Marte lo atrae cada vez más, acercándose 2 metros cada 100 años."}
        }
    },
    "Júpiter": {
        "tipo": "Planeta", "color": "🟠", "desc": "El rey indiscutible de los planetas. Un gigante gaseoso inmenso con tormentas eternas.",
        "lunas": ["Io", "Europa", "Ganímedes", "Calisto"],
        "quiz": {
            "fácil": {"q": "¿Qué es esa gran mancha roja que se ve en Júpiter?", "o": ["Un continente gigante", "Una tormenta", "Un océano de lava"], "a": "Una tormenta", "e": "Es un huracán gigantesco que lleva activo siglos."},
            "medio": {"q": "Si Júpiter fuera un frasco, ¿cuántas Tierras cabrían adentro?", "o": ["10", "1,300", "500"], "a": "1,300", "e": "¡Es inmensamente grande en comparación con nuestro planeta!"},
            "pro master": {"q": "¿De qué gases está hecho principalmente Júpiter?", "o": ["Roca y Polvo", "Oxígeno y Agua", "Hidrógeno y Helio"], "a": "Hidrógeno y Helio", "e": "Los mismos componentes que el Sol. ¡Casi fue una estrella!"}
        }
    },
    "Europa": {
        "tipo": "Luna de Júpiter", "color": "🧊", "desc": "Una bola de hielo brillante. Los científicos creen que esconde un secreto profundo.",
        "quiz": {
            "fácil": {"q": "¿De qué material está cubierta toda la superficie de Europa?", "o": ["Roca dura", "Hielo", "Lava hirviendo"], "a": "Hielo", "e": "Su exterior es como una gran pista de patinaje gigante."},
            "medio": {"q": "¿Qué creen los científicos que hay debajo de todo ese hielo?", "o": ["Oro y diamantes", "Un océano de agua líquida", "Fósiles alienígenas"], "a": "Un océano de agua líquida", "e": "Por eso es uno de los mejores lugares para buscar vida extraterrestre."},
            "pro master": {"q": "¿Qué famoso astrónomo descubrió esta luna?", "o": ["Isaac Newton", "Galileo Galilei", "Albert Einstein"], "a": "Galileo Galilei", "e": "La descubrió en el año 1610 usando un telescopio inventado por él mismo."}
        }
    },
    "Titán": {
        "tipo": "Luna de Saturno", "color": "🟡", "desc": "La luna más misteriosa. Es la única del sistema solar que tiene un cielo nublado y espeso.",
        "quiz": {
            "fácil": {"q": "¿Tiene Titán una atmósfera (cielo con gases) como la Tierra?", "o": ["Sí", "No"], "a": "Sí", "e": "¡Es muy espesa y de color anaranjado!"},
            "medio": {"q": "En Titán hay lagos y ríos, pero no son de agua... ¿de qué son?", "o": ["Lava caliente", "Metano líquido", "Ácido"], "a": "Metano líquido", "e": "Hace tanto frío que gases como el metano se vuelven líquidos."},
            "pro master": {"q": "¿Cuál es el gas principal que forma la atmósfera de Titán?", "o": ["Oxígeno", "Nitrógeno", "Helio"], "a": "Nitrógeno", "e": "Al igual que la Tierra, su cielo está hecho mayormente de Nitrógeno."}
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
if 'quiz_pool' not in st.session_state:
    st.session_state.quiz_pool = []

# --- LÓGICA DE TRIVIA ---
def start_quiz(diff):
    st.session_state.difficulty = diff
    st.session_state.quiz_active = True
    st.session_state.current_step = 0
    st.session_state.score = 0
    st.session_state.answers_history = []
    # Seleccionar 5 cuerpos aleatorios para preguntar
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

# --- INTERFAZ PRINCIPAL ---
st.title("🌌 Explorador del Sistema Solar")

if not st.session_state.quiz_active:
    # --- MODO EXPLORACIÓN ---
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("🚀 Centro de Control")
        search = st.selectbox("Elige un astro para investigar:", list(DATA.keys()))
        
        st.write("---")
        st.info("🎯 ¿Listo para poner a prueba tus conocimientos?")
        diff_choice = st.radio("Selecciona tu rango de piloto:", ["fácil", "medio", "pro master"], horizontal=True)
        if st.button("¡INICIAR TRIVIA GALÁCTICA!"):
            start_quiz(diff_choice)
            st.rerun()

    with col2:
        body = DATA[search]
        st.markdown(f"""
        <div class="planet-card">
            <h1 style="font-size: 3em; margin-bottom: 0;">{body['color']} {search}</h1>
            <p style='font-size: 1.2em; color: #94a3b8;'><strong>Categoría:</strong> {body['tipo']}</p>
            <hr style="border-color: #334155;">
            <p style='font-size: 1.3em; line-height: 1.6;'>{body['desc']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if "lunas" in body:
            st.markdown(f"🛰️ **Lunas principales que puedes explorar:** {', '.join(body['lunas'])}")

else:
    # --- MODO TRIVIA (Navegación bloqueada) ---
    if st.session_state.current_step < len(st.session_state.quiz_pool):
        body_name = st.session_state.quiz_pool[st.session_state.current_step]
        q_data = DATA[body_name]["quiz"][st.session_state.difficulty]
        
        st.progress((st.session_state.current_step) / 5)
        st.header(f"Pregunta {st.session_state.current_step + 1} de 5")
        
        with st.container():
            st.markdown(f"""
            <div class="quiz-container">
                <h3 style="margin-top: 0;">Objetivo escaneado: {body_name} {DATA[body_name]['color']}</h3>
                <p style='font-size: 1.5em; margin-bottom: 0;'>{q_data['q']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.write("")
            st.write("Selecciona tu respuesta:")
            for option in q_data['o']:
                if st.button(option, key=f"btn_{option}_{st.session_state.current_step}"):
                    next_question(option, q_data['a'], body_name)
                    st.rerun()
    else:
        # --- RESULTADOS FINALES ---
        st.balloons()
        st.header("🏁 ¡Misión Completada!")
        
        score = st.session_state.score
        if score == 5:
            msg = "¡ERES UN COMANDANTE GALÁCTICO! 🌟\nNo hay rincón del universo que no conozcas. ¡Impecable!"
        elif score >= 3:
            msg = "¡Buen trabajo, Explorador! 🛰️\nTienes un gran futuro en la astronomía. Estás listo para tu siguiente misión."
        else:
            msg = "¡Cadete! 👨‍🚀\nEl espacio es difícil. Necesitas más horas en el simulador de vuelo, ¡pero lo hiciste muy bien!"
            
        st.success(f"Puntaje Final: {score} de 5 correctas")
        st.write(f"### {msg}")
        
        st.write("---")
        st.subheader("📋 Resumen de tu expedición:")
        for res in st.session_state.answers_history:
            if res["correct"]:
                st.markdown(f"✅ **{res['body']}**: ¡Acertaste! *{res['explanation']}*")
            else:
                st.markdown(f"❌ **{res['body']}**: Fallaste esta vez. *{res['explanation']}*")
        
        st.write("")
        if st.button("Volver al Centro de Control"):
            st.session_state.quiz_active = False
            st.rerun()

# --- FOOTER ---
st.markdown("---")
st.caption("🌌 Creado para futuros astronautas | Desarrollado con Python y Streamlit")
