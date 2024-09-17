from pypdf import PdfReader
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.schema import Document

import os
from docx2pdf import convert
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

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


class EnhancedPDFLoader():
    def __init__(self):
        print("EnhancedPDFLoader")

    def read_pdf(self, path):
        loader = PyPDFLoader(path)
        docs = loader.load()
        content_list = [Document(page_content=line.strip()) for line in docs[0].page_content.split('\n') if line.strip()]
        text_splitter = CharacterTextSplitter(chunk_size=20, chunk_overlap=5)
        documents = text_splitter.split_documents(content_list) 
        print(documents)
        return documents

    def extract_font_sizes(self, page):
        font_sizes = {}
        for obj in page['/Resources']['/Font'].values():
            if hasattr(obj, 'get'):
                font = obj.get('/BaseFont', 'Unknown')
                size = obj.get('/FontDescriptor', {}).get('/FontBBox', [0, 0, 0, 0])[3]
                font_sizes[font] = size
        return font_sizes

    def is_likely_title(self, line, font_size, threshold=1.2):
        if font_size > threshold:
            return True
        if line.isupper() and len(line.split()) <= 5:
            return True
        if line.istitle() and len(line.split()) <= 7:
            return True
        return False
    
if __name__ == "__main__":
    path = "中文履歷.pdf"

    # reader = EnhancedPDFLoader()
    # reader.read_pdf(path)

