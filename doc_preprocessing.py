from typing import List
from langchain_core.documents import Document
from tqdm import tqdm

class preprocess_resume():
    def __init__(self):
        self.sections = {
                "標題": "",
            }
        self.prompts = {
            "標題": "以下文件的標題有哪些。",
        }
    
    def response_ans(self, retrieval_chain, input_txt, context):
        response = retrieval_chain.invoke({
            'input': input_txt,
            'context': context
        })
        return response

    def parse_resume(self, resume_documents: List[Document], retrieval_chain):
        resume_text = " ".join([doc.page_content for doc in resume_documents])

        for section, prompt in tqdm(self.prompts.items()):
            full_prompt = prompt + resume_text
            context = []
            response = self.response_ans(retrieval_chain, full_prompt, context)
            self.sections[section] = response['answer']
        
        return self.sections
