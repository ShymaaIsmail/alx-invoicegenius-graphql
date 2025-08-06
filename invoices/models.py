from django.db import models
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

s3_storage = S3Boto3Storage()

class Invoice(models.Model):
    """Model representing an invoice."""
    file_hash = models.CharField(max_length=64, unique=True, null=True, blank=True)  # SHA256 hash of file
    # Define possible statuses as constants
    STATUS_PENDING = 'pending'
    STATUS_PROCESSING = 'processing'
    STATUS_PROCESSED = 'processed'
    STATUS_FAILED = 'failed'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_PROCESSING, 'Processing'),
        (STATUS_PROCESSED, 'Processed'),
        (STATUS_FAILED, 'Failed'),
    ]

    # Use settings.AUTH_USER_MODEL for flexibility (in case you switch to a custom user model)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='invoices',
        help_text="Owner of this invoice"
    )
    original_file = models.FileField(
        upload_to='invoices/',
        storage=s3_storage,
        help_text="Original uploaded invoice file"
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the invoice was uploaded"
    )
    processed = models.BooleanField(
        default=False,
        help_text="Flag to indicate if OCR and AI parsing have completed"
    )
    processed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Timestamp when processing finished"
    )
    processing_error = models.TextField(
        blank=True,
        null=True,
        help_text="Error message if processing failed"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
        help_text="Current processing status"
    )

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["uploaded_at"]),
        ]

    def __str__(self):
        return f"Invoice {self.id} by {self.user} uploaded {self.uploaded_at.strftime('%Y-%m-%d %H:%M')} (status: {self.status})"


class ParsedInvoiceData(models.Model):
    invoice = models.OneToOneField(
        Invoice,
        on_delete=models.CASCADE,
        related_name='parsed_data',
        help_text="Invoice this parsed data belongs to"
    )
    vendor = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Vendor or supplier name"
    )
    invoice_date = models.DateField(
        blank=True,
        null=True,
        help_text="Date on the invoice"
    )
    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Total invoice amount"
    )
    tax_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Tax amount on the invoice"
    )
    currency = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        help_text="Currency code (e.g., USD, EUR)"
    )
    line_items = models.JSONField(
        blank=True,
        null=True,
        help_text="List of line items, each with details like description, quantity, price"
    )

    class Meta:
        verbose_name = 'Parsed Invoice Data'
        verbose_name_plural = 'Parsed Invoice Data'

    def __str__(self):
        return f"Parsed data for Invoice {self.invoice.id}"
