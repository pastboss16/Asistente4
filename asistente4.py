import streamlit as st
import google.generativeai as genai

# Configurar clave API de Gemini
genai.configure(api_key="AIzaSyAc2lYPWGHOyuhANQNtab4HAFVAp5XBbPc")  

# Configuración de la página
st.set_page_config(page_title="Asistente de Apnea del Sueño", page_icon="😴")

# Título e introducción
st.title("😴 Chatbot: ¿Sufres de Apnea del Sueño?")
st.subheader("Conversemos sobre tus síntomas y averigüemos si necesitas ayuda médica.")

# Estilo visual personalizado
st.markdown("""
<style>
    .main {
        background-color: #eef6f9;
    }
    .stTextInput>div>div>input {
        background-color: #ffffff;
    }
    .stChatMessage {
        border-radius: 15px;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Inicializar historial del chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "¡Hola! 😄 Soy tu asistente virtual. Estoy aquí para ayudarte a entender si presentas síntomas relacionados con la apnea del sueño. "
                                         "¿Has notado ronquidos fuertes, pausas en tu respiración mientras duermes o somnolencia durante el día? Cuéntame tus síntomas."}
    ]

# Mostrar historial de mensajes
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Entrada del usuario
if prompt := st.chat_input("Describe tus síntomas aquí..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Información sobre la enfermedad como contexto
            info_apnea = """
            INFORMACIÓN MÉDICA SOBRE LA APNEA DEL SUEÑO:
            La apnea del sueño es un trastorno en el que la respiración se interrumpe repetidamente mientras duermes.
            Síntomas comunes:
            - Ronquidos fuertes
            - Pausas en la respiración mientras duermes (observadas por otros)
            - Despertarse con sensación de ahogo
            - Somnolencia excesiva durante el día
            - Dolor de cabeza matutino
            - Dificultad para concentrarse
            - Irritabilidad
            - Sequedad en la boca al despertar

            Este asistente no ofrece diagnóstico médico, pero puede ayudarte a identificar síntomas que podrían estar relacionados con la apnea del sueño.
            """

            model = genai.GenerativeModel("gemini-1.5-flash")

            contexto = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])

            respuesta = model.generate_content(
                f"Eres un asistente médico virtual que ayuda a identificar síntomas de apnea del sueño. Sé empático, claro y cuidadoso. "
                f"Usa la siguiente información médica como referencia:\n{info_apnea}\n\n"
                f"Conversación previa:\n{contexto}\n\n"
                f"Responde de forma amable, no des diagnósticos exactos pero sí sugiere visitar a un médico si los síntomas son preocupantes.",
                stream=False
            )

            respuesta_texto = respuesta.text if hasattr(respuesta, "text") else "Lo siento, no pude generar una respuesta en este momento."

            st.markdown(respuesta_texto)
            st.session_state.messages.append({"role": "assistant", "content": respuesta_texto})

        except Exception as e:
            st.error(f"Ocurrió un error: {e}")
            st.session_state.messages.append({
                "role": "assistant",
                "content": "Disculpa, no pude procesar tu solicitud. Intenta nuevamente más tarde."
            })
