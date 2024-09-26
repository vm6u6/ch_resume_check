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
            "姓名": "這是誰的履歷，回答名子就好。",
            "工作經歷": "以下履歷中的工作經歷，列舉公司名稱以及職位，還有其所任職的時間，條列對應工作經歷跟內容。或是專案或專題內容。回答的格式為:\
                       先回答工作經驗，如果有專案再回答專案經驗。",
            "技能": "條列回答，履歷中的技術以及工具，不須提及經驗。",
            "教育背景": "以下內容，列舉學校名稱以及學系，還有其所在學的時間。",
            "證書": "以下內容有提到證書嗎，若沒有回答為[無]",
            "鏈結": "以下內容，列出其中的鏈結網址。"
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
