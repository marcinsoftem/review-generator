import streamlit as st
import generator as gen
import os
import json
import re
import st_copy_to_clipboard as stc
import auth

TMP_DIR = "tmp/"
FILE_TYPES = ["docx"]
SECRETS_FILE = "./.streamlit/secrets.toml"

if os.path.exists(SECRETS_FILE):
    OPENAI_API_KEY = st.secrets["openai"]["OPENAI_API_KEY"]
    OPENAI_BASE_URL = st.secrets["openai"]["OPENAI_BASE_URL"]
    PIN_CODE = st.secrets["PIN_CODE"]
else:
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL")
    PIN_CODE = os.environ.get("PIN_CODE")

os.makedirs(TMP_DIR, exist_ok=True)

auth.key(PIN_CODE)

st.header("Generator recenzji")

answer = None


def clean_json_string(json_string):
    pattern = r'^```json\s*(.*?)\s*```$'
    cleaned_string = re.sub(pattern, r'\1', json_string, flags=re.DOTALL)
    return cleaned_string.strip()

def prompt_template_validation(prompt_template: str, keys: list[str]):
    for key in keys:
        if prompt_template.find(key) == -1:
            st.warning(f"W szablonie promptu musi znaleźć się znacznik {key}. Zaktualizuj szablon promptu i spróbuj ponownie.")
            st.stop()

with st.form("loader_form"):
    uploaded_file = st.file_uploader("Załaduj plik pracy", type=FILE_TYPES)
    prompt_template = st.text_area("Edytuj szblon promptu", value=gen.PROMPT_TEMPLATE, height=360)

    if st.form_submit_button("Generuj recenzję"):
        with st.spinner("Trwa generowanie..."):
            prompt_template_validation(prompt_template, ["{context}", "{sections[0]}", "{sections[1]}", "{sections[2]}", "{sections[3]}", "{sections[4]}", "{sections[5]}", "{sections[6]}"])
            if uploaded_file:
                file_path = TMP_DIR + uploaded_file.name
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                context_text = gen.load_docx(file_path)
                os.remove(file_path)
                prompt = gen.prepare_prompt(context_text, prompt_template)
                answer = gen.generate(prompt, OPENAI_API_KEY, OPENAI_BASE_URL)
                st.text_area("Podgląd pełnego promptu", value=prompt, height=200, disabled=True)
                st.write(answer.content)

if answer:
    answer_json = json.loads(clean_json_string(answer.content))
    for idx, header in enumerate(gen.SECTIONS):
        st.text_area(header, value=answer_json[str(idx + 1)], height=180)
        stc.st_copy_to_clipboard(answer_json[str(idx + 1)], "Kopiuj do schowka", "Skopiowano do schowka", key=header)
