from langchain.schema import Document

import os
from docx2pdf import convert
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from langchain_core.documents import Document

from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams
import pdfplumber
from langchain_community.document_loaders import PyPDFLoader
import PyPDF2

from langchain_community.llms import Ollama
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_text_splitters import CharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import json
from typing import List, Tuple

class read_pdf_splitter():
    def __init__(self, llm_model):
        self.llm = llm_model
        self.prompt = PromptTemplate(
            input_variables=["resume"],
            template="""
            请分析以下中文履历文本，并将其分割成主要部分。对于每个部分，提供一个标题和相应的内容，内容靠近的东西会比较容易在同一个标题下。
            以JSON格式返回结果，格式如下，有具體描述內容以及工作時間的標記為工作經歷：
            {{
                "sections": [
                    {{"title": "姓名"     , "content": "部分内容0"}},
                    {{"title": "部分标题1", "content": "部分内容1"}},
                    {{"title": "部分标题2", "content": "部分内容2"}},
                    {{"title": "網站連結" , "content": "部分内容3"}},
                    ...
                ]
            }}
            
            履历文本：
            {resume}
            """
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

    # def read_pdf(self, path):
    #     loader = PyPDFLoader(path)
    #     docs = loader.load()
    #     res = [Document(page_content=line.strip()) for line in docs[0].page_content.split('\n') if line.strip()]

    #     merge_res = ''
    #     for i in res:
    #         str = i.page_content
    #         merge_res += str
    #     return merge_res
    
    def read_pdf(self, path):
        laparams = LAParams(line_overlap=0.5, char_margin=2.0, line_margin=0.5, word_margin=0.1)
        full_text = extract_text(path, laparams=laparams)
        lines = [line.strip() for line in full_text.split('\n') if line.strip()]
        merge_res = '\n'.join(lines)

        return merge_res

    def split_content(self, text):
        text_splitter = RecursiveCharacterTextSplitter(
            separators=["\n\n", "\n", "。", "，", " ", ""],
            chunk_size=60,
            chunk_overlap=50,
            length_function=len,
        )
        chunks = text_splitter.split_text(text)

        return chunks

    def llm_split_content(self, resume_text):
        response = self.chain.run(resume=resume_text)
        print(response)

        try:
            result = json.loads(response)
            sections = [(section['title'], section['content']) for section in result['sections']]

        except json.JSONDecodeError:
            sections = self._manual_split(response)
        
        return sections

    def _manual_split(self, text: str) -> List[Tuple[str, str]]:
        lines = text.split('\n')
        sections = []
        current_title = ""
        current_content = []

        for line in lines:
            if line.strip().startswith(("部分标题", "标题")):
                if current_title:
                    sections.append((current_title, '\n'.join(current_content)))
                current_title = line.split(':', 1)[-1].strip()
                current_content = []
            elif line.strip().startswith("内容:"):
                current_content.append(line.split(':', 1)[-1].strip())
            else:
                current_content.append(line.strip())

        if current_title:
            sections.append((current_title, '\n'.join(current_content)))

        return sections


class WordToPDFConverter:
    def __init__(self):
        print("WordToPDFConverter initialized")

    def convert_using_docx2pdf(self, input_path, output_path=None):
        """
        Convert Word document to PDF using docx2pdf library.
        """
        try:
            if output_path is None:
                output_path = os.path.splitext(input_path)[0] + '.pdf'
            
            convert(input_path, output_path)
            print(f"Conversion completed. PDF saved as: {output_path}")
        except Exception as e:
            print(f"An error occurred during conversion: {e}")

    def convert_using_reportlab(self, input_path, output_path=None):
        """
        Convert Word document to PDF using python-docx and reportlab libraries.
        This method provides more control over the conversion process but may not preserve all formatting.
        """
        try:
            if output_path is None:
                output_path = os.path.splitext(input_path)[0] + '.pdf'
            
            # Read the Word document
            doc = Document(input_path)
            
            # Create a PDF document
            pdf = SimpleDocTemplate(output_path, pagesize=letter)
            styles = getSampleStyleSheet()
            flowables = []

            # Convert each paragraph to a PDF paragraph
            for para in doc.paragraphs:
                p = Paragraph(para.text, styles['Normal'])
                flowables.append(p)

            # Build the PDF
            pdf.build(flowables)
            print(f"Conversion completed. PDF saved as: {output_path}")
        except Exception as e:
            print(f"An error occurred during conversion: {e}")

if __name__ == "__main__":
    test = read_pdf_splitter()
    path = "中文履歷.pdf"
    res = test.read_pdf(path)
    chunks = test.llm_split_content(res)

