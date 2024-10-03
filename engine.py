from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader

from langchain.text_splitter import CharacterTextSplitter

class LLM_engine():
    def __init__(self):
        self.llm = Ollama(model="wangshenzhi/llama3-8b-chinese-chat-ollama-q8")
        self.embeddings = OllamaEmbeddings(model="wangshenzhi/llama3-8b-chinese-chat-ollama-q8", base_url="http://localhost:11434")
        print("[INFO] Embeddings: ", self.embeddings)
        self.set_template()
        print("[INFO] LLM: ", self.llm)


    def set_template(self):
        self.prompt = ChatPromptTemplate.from_messages([
            ('system', 'Answer the user\'s questions in Chinese, based on the context provided below:\n\n{context}'),
            ('user', 'Question: {input}'),
        ])

    