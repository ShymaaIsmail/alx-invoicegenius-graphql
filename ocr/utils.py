import os
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
from django.core.files.storage import default_storage


def extract_text_from_pdf(file_path):
    """Extract text from a PDF file using PyMuPDF."""
    text = ""

    full_path = file_path if os.path.isabs(file_path) else default_storage.path(file_path)

    with fitz.open(full_path) as doc:
        for page in doc:
            text += page.get_text()
    return text


def extract_text_from_image(file_path):
    """Extract text from an image file using Tesseract OCR."""
    full_path = file_path if os.path.isabs(file_path) else default_storage.path(file_path)

    image = Image.open(full_path)
    return pytesseract.image_to_string(image)
