from django.test import TestCase
from invoices.models import Invoice
from invoices.tasks import process_invoice_file
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch, MagicMock
from django.contrib.auth import get_user_model

User = get_user_model()

class InvoiceTaskTest(TestCase):
    @patch("fitz.open")  # patch the external library function directly
    @patch("invoices.tasks.extract_text_from_pdf")
    @patch("invoices.tasks.parse_invoice_text")
    def test_process_pdf_invoice(self, mock_parse, mock_extract, mock_fitz_open):
        mock_doc = MagicMock()
        mock_fitz_open.return_value.__enter__.return_value = mock_doc

        mock_extract.return_value = "Invoice Number: 123"
        mock_parse.return_value = {
            "invoice_number": "123",
        "vendor_name": "ACME Inc.",
        "invoice_date": "2024-07-31",
        "total_amount": {"value": 199.99, "currency": "USD"},
        "tax": {"value": 9.99, "currency": "USD"},
        "line_items": []
        }

        user = User.objects.create(username="testuser")
        file = SimpleUploadedFile("invoice.pdf", b"%PDF-1.4\n%Fake PDF content\n")
        invoice = Invoice.objects.create(user=user, original_file=file)

        process_invoice_file(invoice.id)
        invoice.refresh_from_db()
        self.assertEqual(invoice.status, "processed")
