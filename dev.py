from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from engine import LLM_engine

def main(path):
    LLM = LLM_engine()
    LLM.read_pdf(path)
    retrieval_chain = LLM.run()

    context = []
    input_text = input('>>> ')
    while input_text.lower() != 'bye':
        response = retrieval_chain.invoke({
            'input': input_text,
            'context': context
        })
        print(response['answer'])
        context = response['context']
        input_text = input('>>> ')



if __name__ == "__main__":
    path = "中文履歷.pdf"
    main(path)