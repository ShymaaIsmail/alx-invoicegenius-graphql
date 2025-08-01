from django.test import TestCase
from invoices.models import Invoice
from invoices.tasks import process_invoice_file
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch
from django.contrib.auth import get_user_model
User = get_user_model()


class InvoiceTaskTest(TestCase):
    @patch("ocr.utils.extract_text_from_pdf")
    @patch("ai_parser.utils.parse_invoice_text")
    def test_process_pdf_invoice(self, mock_parse, mock_extract):
        mock_extract.return_value = "Invoice Number: 123"
        mock_parse.return_value = {
            "invoice_number": "123",
            "vendor_name": "ACME Inc.",
            "invoice_date": "2024-07-31",
            "total_amount": "199.99",
            "tax": "9.99"
        }
        user = User.objects.create(username="testuser")
        file = SimpleUploadedFile("invoice.pdf", b"fake", content_type="application/pdf")
        invoice = Invoice.objects.create(user=user, original_file=file)
        process_invoice_file(invoice.id)
        invoice.refresh_from_db()
        self.assertEqual(invoice.status, "PROCESSED")