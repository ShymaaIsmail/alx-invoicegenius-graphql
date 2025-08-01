
# invoices/tests/test_models.py
from django.test import TestCase
from invoices.models import Invoice
from django.contrib.auth import get_user_model

from django.core.files.uploadedfile import SimpleUploadedFile
User = get_user_model()


class InvoiceModelTest(TestCase):
    def test_create_invoice(self):
        user = User.objects.create(username="testuser")
        file = SimpleUploadedFile("invoice.pdf", b"fake content", content_type="application/pdf")
        invoice = Invoice.objects.create(user=user, original_file=file)
        self.assertIsNotNone(invoice.id)
