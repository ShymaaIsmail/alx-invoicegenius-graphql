from django.db import models
from invoices.models import Invoice

class OCRJob(models.Model):
    invoice = models.OneToOneField(Invoice, on_delete=models.CASCADE, related_name='ocr_job')
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    success = models.BooleanField(default=False)
    extracted_text = models.TextField(blank=True, null=True)
    error_message = models.TextField(blank=True, null=True)

    def __str__(self):
        status = "Success" if self.success else "Failed"
        return f"OCR Job for Invoice {self.invoice.id} - {status}"
