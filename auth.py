import streamlit as st

def key(key : str):
    if not("auth_key" in st.session_state and st.session_state["auth_key"] == key):
        with st.form("key_form"):
            st.session_state["auth_key"] = st.text_input("Podaj kod, aby skorzystć z aplikacji")
            if st.form_submit_button("Zaloguj"):
                if st.session_state["auth_key"] != key:
                    st.warning("Kod jest nieprawidłowy")
                else:
                    st.experimental_rerun()
            st.stop()