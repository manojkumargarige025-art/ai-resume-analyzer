from typing import Optional
from PyPDF2 import PdfReader

def extract_text_from_pdf(file_stream) -> str:
    """
    Extract text from an uploaded PDF (file-like object).
    """
    reader = PdfReader(file_stream)
    chunks = []
    for page in reader.pages:
        text = page.extract_text() or ""
        chunks.append(text)
    return "\n".join(chunks)

def clean_text(text: Optional[str]) -> str:
    if not text:
        return ""
    # basic cleanup
    return " ".join(text.replace("\t", " ").split())
