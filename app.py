import streamlit as st
import generator as gen
import os
import json
import re
import st_copy_to_clipboard as stc
import auth

TMP_DIR = "tmp/"
FILE_TYPES = ["docx"]
OPENAI_API_KEY = st.secrets["openai"]["OPENAI_API_KEY"]
OPENAI_BASE_URL = st.secrets["openai"]["OPENAI_BASE_URL"]

os.makedirs(TMP_DIR, exist_ok=True)

auth.key()

st.header("Generator recenzji")

answer = None


def clean_json_string(json_string):
    pattern = r'^```json\s*(.*?)\s*```$'
    cleaned_string = re.sub(pattern, r'\1', json_string, flags=re.DOTALL)
    return cleaned_string.strip()


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
                print(answer.content)

if answer:
    answer_json = json.loads(clean_json_string(answer.content))
    for idx, header in enumerate(gen.SECTIONS):
        st.text_area(header, value=answer_json[str(idx + 1)], height=180)
        stc.st_copy_to_clipboard(answer_json[str(idx + 1)], "Kopiuj do schowka", "Skopiowano do schowka", key=header)
