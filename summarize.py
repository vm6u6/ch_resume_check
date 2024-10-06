from typing import List
from langchain_core.documents import Document
from tqdm import tqdm

class summarize_resume():
    def __init__(self, resume_text: str, job_description: str):
        self.resume_text = resume_text
        self.job_description = job_description
            