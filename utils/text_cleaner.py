import re

def clean_text(text: str) -> str:
    """
    Cleans and normalizes text by removing extra whitespaces,
    newline characters, and other noise.
    """
    if not text:
        return ""
    
    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    
    # Strip leading/trailing whitespaces
    text = text.strip()
    
    return text
