from django.test import TestCase
from invoices.models import Invoice
from invoices.tasks import process_invoice_file
from django.contrib.auth import get_user_model
from unittest.mock import patch, MagicMock
from django.utils import timezone

User = get_user_model()

class InvoiceTaskTest(TestCase):
    @patch("invoices.tasks.requests.get")
    @patch("invoices.tasks.extract_text_from_pdf")
    @patch("invoices.tasks.parse_invoice_text")
    def test_process_pdf_invoice(self, mock_parse, mock_extract, mock_requests_get):
        # Mock the response from requests.get
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"%PDF-1.4\n%Fake PDF content\n"
        mock_requests_get.return_value = mock_response

        # Mock OCR and parser
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
        invoice = Invoice.objects.create(
            user=user,
            downloadFilename="https://example.com/fake_invoice.pdf",  # mock URL
            status="pending"
        )

        process_invoice_file(invoice.id)

        invoice.refresh_from_db()
        self.assertEqual(invoice.status, "processed")
        self.assertTrue(invoice.processed)
        self.assertIsNotNone(invoice.processed_at)
