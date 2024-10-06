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
from datetime import datetime
import logging
import ast
import re

class read_pdf_splitter():
    def __init__(self, llm_model):
        self.llm = llm_model
        self.prompt_response = PromptTemplate(
            input_variables=["resume"],
            template="""
            请分析以下中文履历文本，并将其分割成主要部分。对于每个部分，提供一个标题和相应的内容，内容靠近的东西会比较容易在同一个标题下，尤其是文本末尾的内容。对于每个部分，提供一个準確的[標題]和完整的相應內容，[不要省略任何內容]。
            以JSON格式返回结果，格式如下，有具體描述內容以及工作時間的標記為工作經歷：
            {{
                "sections": [
                    {{"title": "姓名"     , "content": "内容0"}},
                    {{"title": "部分标题1", "content": "内容1"}},
                    {{"title": "部分标题2", "content": "内容2"}},
                    {{"title": "網站連結" , "content": "内容3"}},
                    ...
                ]
            }}
            检查JSON格式是否正确。如果存在格式错误，请修正它们 确保转换过程中[不遗漏任何原始资讯]。

            履历文本：
            {resume}
            """
        )

        self.chain_response = LLMChain(llm=self.llm, prompt=self.prompt_response)


        self.response_dir = "llm_responses"
        if not os.path.exists(self.response_dir):
            os.makedirs(self.response_dir)

    def _save_to_txt(self, response):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.response_dir}/llm_response_{timestamp}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(response)
        logging.info(f"Response saved to file: {filename}")

    def _load_latest_response(self):
        files = [f for f in os.listdir(self.response_dir) if f.startswith("llm_response_") and f.endswith(".txt")]
        if not files:
            return None
        latest_file = max(files, key=lambda x: os.path.getctime(os.path.join(self.response_dir, x)))
        with open(os.path.join(self.response_dir, latest_file), 'r', encoding='utf-8') as f:
            return f.read()
    
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

    def parse_response(self, response_str):
        response_str = response_str.strip()
        response_str = re.sub(r'^```json\s*|```$', '', response_str, flags=re.MULTILINE)
        response_str = response_str.replace('"""', '').replace("'''", "")
        # print(response_str)
        try:
            data = json.loads(response_str)
        except:
            data = ast.literal_eval(response_str.strip())
        # print(data)

        resume = {}

        # Iterate through the sections
        for section in data['sections']:
            title = section['title']
            content = section.get('content')

            # Handle nested sections (like work experience)
            if 'sections' in section:
                subsections = []
                for subsection in section['sections']:
                    subsections.append({
                        'title': subsection['title'],
                        'content': subsection['content']
                    })
                resume[title] = subsections
            else:
                resume[title] = content
        return resume

    def llm_split_content(self, resume_text):
        # response = self.chain_response.run(resume=resume_text)
        # print("[INFO] Response: ", response)
        # self._save_to_txt(response)

        response = self._load_latest_response()
        sections = self.parse_response(response)

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

