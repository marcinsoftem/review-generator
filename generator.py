from langchain_core.documents import Document
from langchain_community.document_loaders import Docx2txtLoader
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

PROFIL = ("openai")
CHAT_MODEL = "gpt-4o"

SECTION_1 = "Czy treść pracy odpowiada tematowi określonemu w tytule"
SECTION_2 = "Ocena układu pracy (struktury, podziału, treści, kolejności rozdziałów, kompletnności tez itp.)"
SECTION_3 = "Merytoryczna ocena pracy"
SECTION_4 = "Czy, a jeśli tak, to w jakim zakresie praca stanowi nowe ujęcie problemu"
SECTION_5 = "Charakterystyka doboru i wykorzystania źródeł"
SECTION_6 = "Ocena formalnej strony pracy (poprawność językowa, opanowanie techniki pisania pracy, spis rzeczy, odsyłacze)"
SECTION_7 = "Ocena osiągniętych efektów uczenia się (patrz karta zajęć)"
SECTIONS = [SECTION_1, SECTION_2, SECTION_3, SECTION_4, SECTION_5, SECTION_6, SECTION_7]

PROMPT_TEMPLATE = """DOKUMENT:
{context}
PYTANIA:
1. {sections[0]}
2. {sections[1]}
3. {sections[2]}
4. {sections[3]}
5. {sections[4]}
6. {sections[5]}
7. {sections[6]}
INSTRUKCJA:
Jako promotor pracy dyplomowej stwórz recenzję odpowiadając na powyższe PYTANIA.
Odpowiedź przedstaw w formacie JSON gdzie kluczami są numery nagłówków."""


def clean_documents(pages: list[Document]) -> list[Document]:
    for doc in pages:
        doc.page_content = doc.page_content.replace('\xa0', ' ')
        doc.page_content = doc.page_content.replace('\t', ' ')
        doc.page_content = ''.join(doc.page_content.splitlines())
    return pages


def load_docx(file_path: str) -> list[Document]:
    return Docx2txtLoader(file_path).load()
def prepare_prompt(context_text: str, prompt_template: str) -> str:
    chat_prompt_template = ChatPromptTemplate.from_template(prompt_template)
    return chat_prompt_template.format(context=context_text, sections=SECTIONS)

def generate(prompt: str, openai_api_key: str, base_url: str) -> str:
    model = ChatOpenAI(openai_api_key=openai_api_key, base_url=base_url, model=CHAT_MODEL)
    response_text = model.invoke(prompt)
    return response_text