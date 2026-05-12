import pdfplumber
import re

def extract_text_from_pdf(file) -> str:
    """
   This is used to extract and cleans text from uploaded PDF resume.
    """
    text = ""
    
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    
    return clean_text(text)


def clean_text(text: str) -> str:
    """
    Cleans extracted text:
    - Removes extra whitespace
    - Removes special characters
    - Normalizes line breaks
    """
    # Removing extra spaces
    text = re.sub(r'[ \t]+', ' ', text)
    
    # Normalize line breaks
    text = re.sub(r'\n+', '\n', text)
    
    # Remove non-ASCII characters
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    return text