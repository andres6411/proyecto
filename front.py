import streamlit as st
from chatbot import predict_class, get_response, intents

st.title("Asistente virtual")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "first_message" not in st.session_state:
    st.session_state.first_message = True

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if st.session_state.first_message:
    with st.chat_message("assistant"):
        st.markdown("Hola, ¿cómo puedo ayudarte?")

    st.session_state.messages.append({"role": "assistant", "content": "Hola, ¿cómo puedo ayudarte?"})
    st.session_state.first_message = False  

# Opciones predefinidas (pills)
options = ["Hay problemas de conexión", "No puedo acceder a mi cuenta", "Tengo una pregunta sobre la facturación"]

# Mostrar las pills
selected_option = st.pills("Selecciona una opción:", options)

# Procesar la opción seleccionada
if selected_option:
    with st.chat_message("user"):
        st.markdown(selected_option)
    st.session_state.messages.append({"role": "user", "content": selected_option})

    # Predecir intención y generar respuesta
    insts = predict_class(selected_option)  # Usa la opción seleccionada como entrada
    res = get_response(insts, intents)

    with st.chat_message("assistant"):
        st.markdown(res)
    st.session_state.messages.append({"role": "assistant", "content": res})

# Entrada adicional por texto
if prompt := st.chat_input("¿Cómo puedo ayudarte?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    insts = predict_class(prompt)
    res = get_response(insts, intents)

    with st.chat_message("assistant"):
        st.markdown(res)
    st.session_state.messages.append({"role": "assistant", "content": res})

