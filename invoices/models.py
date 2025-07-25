from django.db import models
from django.contrib.auth.models import User

class Invoice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invoices')
    original_file = models.FileField(upload_to='invoices/')  # saved in media/invoices/
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)  # OCR+AI done?
    processed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Invoice {self.id} by {self.user.username} uploaded {self.uploaded_at}"

class ParsedInvoiceData(models.Model):
    invoice = models.OneToOneField(Invoice, on_delete=models.CASCADE, related_name='parsed_data')
    vendor = models.CharField(max_length=255, blank=True, null=True)
    invoice_date = models.DateField(blank=True, null=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    currency = models.CharField(max_length=10, blank=True, null=True)
    line_items = models.JSONField(blank=True, null=True)  # list of dicts, e.g., [{item, qty, price}]

    def __str__(self):
        return f"Parsed data for Invoice {self.invoice.id}"
