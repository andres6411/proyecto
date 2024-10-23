import streamlit as st

st.title(" Asistente virtual")

if "messages" not in st.session_state:
    st.session_state.messages = []
    if "first message" not in st.session_state:
        st.session_state.first_message = True

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

                if st.session_state.first_message:
                    with st.chat_message("assistant"):
                        st.markdown("Hola, ¿cómo puedo ayudarte?")

                        st.session_state.message.append({"role": "assistant", "content": "Hola, ¿como puedo ayudarte?"})
                        st.session_state.first_message = False  


                        if prompt := st.chat_input("¿como puedo ayudarte?"):
                            with st.chat_message("user"):
                                st.markdown(prompt)
                                st.session_state.messages.append({"role": "user", "content": prompt})

                                with st.chat_message("assistent"):
                                    st.markdown(prompt)

                                    st. session_state.messages.append({"role": "assistent", "content": prompt})