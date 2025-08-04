from django.test import TestCase
from ocr.utils import extract_text_from_pdf, extract_text_from_image

class OCRUtilsTest(TestCase):
    def test_extract_text_from_pdf(self):
        text = extract_text_from_pdf("ocr/tests/sample_invoice.pdf")
        self.assertTrue("Invoice" in text or len(text) > 0)

    def test_extract_text_from_image(self):
        text = extract_text_from_image("ocr/tests/sample_invoice.jpg")
        self.assertTrue("Invoice" in text or len(text) > 0)
