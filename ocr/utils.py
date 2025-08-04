# ocr/utils.py
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
from django.core.files.storage import default_storage

"""Utility functions for OCR processing."""

def extract_text_from_pdf(file_path):
    """Extract text from a PDF file using PyMuPDF."""
    text = ""
    full_path = default_storage.path(file_path)
    with fitz.open(full_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_text_from_image(file_path):
    """Extract text from an image file using Tesseract OCR."""
    full_path = default_storage.path(file_path)
    image = Image.open(full_path)
    return pytesseract.image_to_string(image)
