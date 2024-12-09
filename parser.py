import pdfplumber
import pytesseract
import pandas as pd
from docx import Document
from PIL import Image


def parse_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

def parse_image(file_path):
    image = Image.open(file_path)
    text = pytesseract.image_to_string(image)
    return text

def parse_docx(file_path):
    doc = Document(file_path)
    text = "\n".join([p.text for p in doc.paragraphs])
    return text

def extract_excelcsv(file_path):
    """Extract structured data from an Excel/CSV file."""
    df = pd.read_excel(file_path) if file_path.endswith('.xlsx') else pd.read_csv(file_path)
    df = df.fillna("")
    return df.to_string()


def extract_attachment(file_path):
    
    # Handle file extensions
    if file_path.endswith('.pdf'):
        return parse_pdf(file_path)
    elif file_path.endswith(('.jpg', '.jpeg', '.png')):
        return parse_image(file_path)
    elif file_path.endswith('.docx'):
        return parse_docx(file_path)
    elif file_path.endswith(('.csv', '.xlsx')):
        return extract_excelcsv(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_path}")