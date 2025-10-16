import os
import mimetypes
import fitz  # PyMuPDF
import docx
from bs4 import BeautifulSoup

class DocumentParserAgent:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.file_type = self.detect_file_type()
        self.text = ""
        self.metadata = {}

    def detect_file_type(self):
        mime_type, _ = mimetypes.guess_type(self.file_path)
        if mime_type:
            if "pdf" in mime_type:
                return "pdf"
            elif "word" in mime_type or self.file_path.endswith(".docx"):
                return "docx"
            elif "html" in mime_type or self.file_path.endswith(".html"):
                return "html"
        raise ValueError("Unsupported file type")

    def extract_text_and_metadata(self):
        if self.file_type == "pdf":
            return self._parse_pdf()
        elif self.file_type == "docx":
            return self._parse_docx()
        elif self.file_type == "html":
            return self._parse_html()

    def _parse_pdf(self):
        doc = fitz.open(self.file_path)
        self.text = "\n".join(page.get_text() for page in doc)
        self.metadata = {
            "title": doc.metadata.get("title", "Unknown"),
            "author": doc.metadata.get("author", "Unknown"),
            "source": os.path.basename(self.file_path)
        }

    def _parse_docx(self):
        doc = docx.Document(self.file_path)
        self.text = "\n".join(p.text for p in doc.paragraphs)
        self.metadata = {
            "title": doc.core_properties.title or "Unknown",
            "author": doc.core_properties.author or "Unknown",
            "source": os.path.basename(self.file_path)
        }

    def _parse_html(self):
        with open(self.file_path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
        self.text = soup.get_text()
        self.metadata = {
            "title": soup.title.string if soup.title else "Unknown",
            "author": "Unknown",  # Could extract from meta tags
            "source": os.path.basename(self.file_path)
        }

    def run(self):
        self.extract_text_and_metadata()
        return {
            "file_type": self.file_type,
            "text": self.text,
            "metadata": self.metadata
        }
