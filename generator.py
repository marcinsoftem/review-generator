from langchain_core.documents import Document
from langchain_community.document_loaders import Docx2txtLoader
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

PROFIL = ("openai")
CHAT_MODEL = "gpt-4o"

PROMPT_TEMPLATE = """
DOKUMENT:
{context}
PYTANIA:
Czy treść pracy odpowiada tematowi określonemu w tytule?
Ocena układu pracy (struktury, podziału, treści, kolejności rozdziałów, kompletności tez itp.)
Merytoryczna ocena pracy
Czy, a jeśli tak, to w jakim zakresie praca stanowi nowe ujęcie problemu?
Charakterystyka doboru i wykorzystania źródeł
Ocena formalnej strony pracy (poprawność językowa, opanowanie techniki pisania pracy, spis rzeczy, odsyłacze) 
Ocena osiągniętych efektów uczenia się (patrz karta zajęć)
INSTRUKCJA:
Jako promotor pracy dyplomowej stwórz recenzję odpowiadając na powyższe PYTANIA.
"""


def clean_documents(pages: list[Document]) -> list[Document]:
    for doc in pages:
        doc.page_content = doc.page_content.replace('\xa0', ' ')
        doc.page_content = doc.page_content.replace('\t', ' ')
        doc.page_content = ''.join(doc.page_content.splitlines())
    return pages


def load_docx(file_path: str) -> list[Document]:
    return Docx2txtLoader(file_path).load()


def generate(context_text: str, openai_api_key: str, base_url: str) -> str:
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text)
    # print(prompt)
    model = ChatOpenAI(openai_api_key=openai_api_key, base_url=base_url, model=CHAT_MODEL)
    response_text = model.invoke(prompt)
    return response_text
