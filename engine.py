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

    def read_pdf(self, path):
        loader = PyPDFLoader(path)
        docs = loader.load()
        content_list = [Document(page_content=line.strip()) for line in docs[0].page_content.split('\n') if line.strip()]

        text_splitter = CharacterTextSplitter(chunk_size=20, chunk_overlap=5)
        documents = text_splitter.split_documents(content_list)

        vectordb = FAISS.from_documents(documents, self.embeddings)
        self.retriever = vectordb.as_retriever()
        return documents

    def run(self):
        document_chain = create_stuff_documents_chain(self.llm, self.prompt)
        retrieval_chain = create_retrieval_chain(self.retriever, document_chain)
        return retrieval_chain