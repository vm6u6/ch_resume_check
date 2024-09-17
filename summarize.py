

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
            "姓名": "姓名",
            "工作經歷": "簡潔回答，履歷中的工作經歷",
            "技能": "簡潔回答，履歷中提到的專業技能",
            "教育背景": "教育背景",
            "證書": "履歷中提到的任何證書"
        }

    def response_ans(self, retrieval_chain, input_txt, context):
        response = retrieval_chain.invoke({
            'input': input_txt,
            'context': context
        })
        return response

    def parse_resume(self, resume_text, retrieval_chain):
        for section, prompt in self.prompts.items():
            full_prompt = prompt + resume_text
            context = []
            response = self.response_ans(retrieval_chain, full_prompt,  context)
            self.sections[section] = response['answer']
        return self.sections
