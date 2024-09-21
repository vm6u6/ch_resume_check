from typing import List
from langchain_core.documents import Document
from tqdm import tqdm

class summarize_resume():
    def __init__(self):
        self.sections = {
                "姓名": "",
                "工作經歷": "",
                "技能": "",
                "教育背景": "",
                "證書": ""
            }
        self.prompts = {
            "姓名": "以上資訊中，履歷上的姓名",
            "工作經歷": "簡潔回答，履歷中的工作經歷，列舉公司名稱以及職位，還有其所任職的時間",
            "技能": "簡潔回答，履歷中的專業技能",
            "教育背景": "教育背景，列舉學校名稱以及學系，還有其所在學的時間",
            "證書": "履歷中提到的任何證書，若沒有再標記為[無]"
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
