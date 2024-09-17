## According the STAR priciple


class modified_resume():
    def __init__(self):
        self.sections = {
                "姓名": "",
                "工作經歷": "",
                "技能": "",
                "教育背景": "",
                "證書": ""
            } 

        self.star_prompts = {
            "工作經歷": """
            你是寫履歷專家。
            使用STAR原則重新組織原始工作經歷。

            以下為STAR原則的定義:
            1. Situation(情境):描述背景、面臨的問題或困難。如果是非知名企業，簡介公司的產品服務。
            2. Task(任務):說明您被分配的任務或提出的解決方案。
            3. Action(行動):詳述您採取的具體行動和應用的技能。
            4. Result(結果):量化成果，使用商業術語描述對公司或客戶的影響。

            以下為原始工作經歷：
            """
        }      

    def response_ans(self, retrieval_chain, input_txt, context):
        response = retrieval_chain.invoke({
            'input': input_txt,
            'context': context
        })
        return response
         

    def modify_resume(self, resume_text, retrieval_chain, summarized_sections):

        for section, content in summarized_sections.items():
            if section in self.star_prompts:
                full_prompt = self.star_prompts[section] + content
                context = []
                response = self.response_ans(retrieval_chain, full_prompt, context)
                self.sections[section] = response['answer']
            else:
                self.sections[section] = content
        
        return self.sections











