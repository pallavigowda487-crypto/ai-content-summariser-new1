import PyPDF2
from typing import BinaryIO
from utils.text_cleaner import clean_text

def extract_text_from_pdf(file: BinaryIO) -> str:
    """
    Reads a PDF file and extracts all text.
    Handles empty or unreadable pages gracefully.
    """
    try:
        reader = PyPDF2.PdfReader(file)
        extracted_text = []
        
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text = page.extract_text()
            if text:
                extracted_text.append(text)
                
        full_text = " ".join(extracted_text)
        return clean_text(full_text)
    except Exception as e:
        raise ValueError(f"Failed to extract text from PDF: {str(e)}")
