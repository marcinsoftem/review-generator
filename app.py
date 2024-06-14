import streamlit as st
import generator as gen
import os

TMP_DIR = "tmp/"
FILE_TYPES = ["docx"]
OPENAI_API_KEY = st.secrets["openai"]["OPENAI_API_KEY"]
OPENAI_BASE_URL = st.secrets["openai"]["OPENAI_BASE_URL"]

os.makedirs(TMP_DIR, exist_ok=True)

st.header("Generator recenzji")

with st.form("loader_form"):
    uploaded_file = st.file_uploader("Załaduj plik pracy", type=FILE_TYPES)
    if st.form_submit_button("Generuj recenzję"):
        with st.spinner("Trwa generowanie..."):
            if uploaded_file:
                file_path = TMP_DIR + uploaded_file.name
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                context_text = gen.load_docx(file_path)
                os.remove(file_path)
                answer = gen.generate(context_text, OPENAI_API_KEY, OPENAI_BASE_URL)
                st.write(answer.content)

