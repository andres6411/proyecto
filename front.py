import streamlit as st
import json
from chatbot import predict_class, get_response

st.title("Asistente virtual")

# Inicializar estado
if "messages" not in st.session_state:
    st.session_state.messages = []
if "first_message" not in st.session_state:
    st.session_state.first_message = True
if "model_path" not in st.session_state:
    st.session_state.model_path = "chatbot_model.h5"
if "options" not in st.session_state:
    st.session_state.options = []

# Cargar intents
with open('intents_spanish.json', 'r', encoding="utf-8") as f:
    intents = json.load(f)

# Mostrar mensajes previos
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Primera interacción del bot
if st.session_state.first_message:
    with st.chat_message("assistant"):
        st.markdown("Hola, ¿cómo puedo ayudarte?")
    st.session_state.messages.append({"role": "assistant", "content": "Hola, ¿cómo puedo ayudarte?"})
    st.session_state.first_message = False

# Actualizar opciones dinámicamente según el modelo actual
def update_options():
    options = []
    model_path = st.session_state.model_path
    if model_path == "chatbot_model.h5":
        for intent in intents['intents']:
            options.append(intent["tag"])
    else:
        tag = next((item for item in intents['intents'] if item.get("path") == model_path), None)
        if tag and "sub_intents" in tag:
            for sub_intent in tag["sub_intents"]:
                options.append(sub_intent["tag"])
    st.session_state.options = options

# Actualizar opciones al cargar
update_options()

# Mostrar las pills dinámicamente
selected_option = st.pills("Selecciona una opción:", st.session_state.options)

# Procesar selección
if selected_option:
    with st.chat_message("user"):
        st.markdown(selected_option)
    st.session_state.messages.append({"role": "user", "content": selected_option})

    # Predecir intención y generar respuesta
    insts = predict_class(selected_option, st.session_state.model_path)
    res = get_response(insts, intents, st.session_state.model_path)

    with st.chat_message("assistant"):
        st.markdown(res)
    st.session_state.messages.append({"role": "assistant", "content": res})

    # Actualizar modelo si es necesario
    tag = next((item for item in intents["intents"] if item["tag"] == insts[0]['intent']), None)
    if tag and "path" in tag:
        st.session_state.model_path = tag["path"]
        st.rerun()  # Forzar una recarga para actualizar las opciones

# Entrada adicional de texto
if prompt := st.chat_input("¿Cómo puedo ayudarte?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Procesar entrada de texto
    insts = predict_class(prompt, st.session_state.model_path)
    res = get_response(insts, intents, st.session_state.model_path)

    
    with st.chat_message("assistant"):
        st.markdown(res)
    st.session_state.messages.append({"role": "assistant", "content": res})

    # Actualizar modelo si es necesario
    tag = next((item for item in intents["intents"] if item["tag"] == insts[0]['intent']), None)
    if tag and "path" in tag:
        st.session_state.model_path = tag["path"]
        st.rerun()  # Forzar una recarga para actualizar las opciones

