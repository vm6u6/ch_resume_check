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

if __name__ == "__main__":
    path = "中文履歷.pdf"


