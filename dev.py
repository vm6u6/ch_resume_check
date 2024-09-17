
'''LOAD LLM ENGINE'''
from engine import LLM_engine


from summarize import summarize_resume
from modified import modified_resume
from output_newLayer import output_newLayer

class ch_resume_checker():
    def __init__(self):
        self.LLM = LLM_engine()

        self.summerize_tool = summarize_resume()

        self.modified_tool = modified_resume()

        self.output_tool = output_newLayer()


    def main(self, path):
        self.LLM.read_pdf(path)
        retrieval_chain = self.LLM.run()
        input_text = "，用中文回答。"
        summerized_section = self.summerize_tool.parse_resume(input_text, retrieval_chain)
        
        print("======================= [ SUMMARIZED ] =======================")
        for i in (summerized_section):
            print("[INFO] KEY: ", i)
            print("[INFO] VALUE: ", summerized_section[i])
            print()

        print("======================= [ MODIFIED ] =======================")
        modified_section = self.modified_tool.modify_resume(input_text, retrieval_chain, summerized_section)

        for i in (modified_section):
            print(modified_section[i])
            print()

        return 0
    

if __name__ == "__main__":
    path = "中文履歷.pdf"
    test = ch_resume_checker()
    test.main(path)