import logging
import mimetypes
from celery import shared_task
from dateutil.parser import parse
from django.utils import timezone
from invoices.models import Invoice, ParsedInvoiceData
from ocr.utils import extract_text_from_pdf, extract_text_from_image
from ai_parser.utils import parse_invoice_text

logger = logging.getLogger(__name__)


def normalize_date(date_str):
    """Convert a messy date string to YYYY-MM-DD format."""
    if not date_str:
        return None
    try:
        dt = parse(date_str, dayfirst=True)
        return dt.date()
    except Exception:
        logger.error(f"Failed to parse date: {date_str}")
        return None

@shared_task
def process_invoice_file(invoice_id):
    logger.info(f"Starting processing of invoice ID: {invoice_id}")

    try:
        invoice = Invoice.objects.get(id=invoice_id)
        logger.info(f"Invoice found: ID={invoice.id}, file={invoice.original_file}")

        file_path = invoice.original_file.path
        mime_type, _ = mimetypes.guess_type(file_path)
        logger.info(f"Detected MIME type: {mime_type}")

        # Extract text based on file type
        if mime_type == "application/pdf":
            text = extract_text_from_pdf(file_path)
        elif mime_type and mime_type.startswith("image/"):
            text = extract_text_from_image(file_path)
        else:
            msg = f"Unsupported MIME type: {mime_type}"
            logger.warning(msg)
            _mark_invoice_failed(invoice, msg)
            return

        if not text:
            msg = "No text extracted from the invoice file."
            logger.warning(msg)
            _mark_invoice_failed(invoice, msg)
            return

        logger.info(f"Parsing extracted text...{text}")
        parsed_data = parse_invoice_text(text)
        #parsed_data= {'vendor_name': 'Berghotel', 'invoice_number': '4572', 'invoice_date': '30. 07. 2007/13:29: 17', 'total_amount': {'value': 54.5, 'currency': 'CHF'}, 'tax': {'value': 3.85, 'currency': 'CHF'}, 'line_items': [{'description': 'Latte Macchiato', 'quantity': 2, 'unit_price': 4.5, 'total_price': 9.0}, {'description': 'Gloki', 'quantity': 1, 'unit_price': 6.0, 'total_price': 6.0}, {'description': 'Schweinschnitzel', 'quantity': 1, 'unit_price': 22.0, 'total_price': 22.0}, {'description': 'Chasspatz', 'quantity': 14, 'unit_price': None, 'total_price': None}]}
        if not parsed_data:
            msg = "AI parsing failed: no data extracted from text."
            logger.warning(msg)
            _mark_invoice_failed(invoice, msg)
            return

        logger.info(f"Parsed data: {parsed_data}")

        # Extract nested data safely
        total = parsed_data.get("total_amount", {})
        tax = parsed_data.get("tax", {})

        ParsedInvoiceData.objects.create(
        invoice=invoice,
        vendor=parsed_data.get("vendor_name"),
        invoice_date= normalize_date(parsed_data.get("invoice_date")),
        total_amount=total.get("value"),
        tax_amount=tax.get("value"),
        currency=total.get("currency") or tax.get("currency"),
        line_items= parsed_data.get("line_items") or []
    )

        invoice.status = Invoice.STATUS_PROCESSED
        invoice.processed = True
        invoice.processed_at = timezone.now()
        invoice.processing_error = None
        invoice.save()
        logger.info(f"Invoice ID {invoice_id} processing completed successfully.")

    except Invoice.DoesNotExist:
        logger.error(f"Invoice with ID {invoice_id} does not exist.")
    except Exception as e:
        logger.exception(f"Unexpected error while processing invoice {invoice_id}: {e}")
        _mark_invoice_failed(invoice, str(e))


def _mark_invoice_failed(invoice, error_message):
    """Helper to update invoice with failure status."""
    invoice.status = Invoice.STATUS_FAILED
    invoice.processing_error = error_message
    invoice.processed = False
    invoice.processed_at = timezone.now()
    invoice.save()
    logger.info(f"Invoice {invoice.id} marked as FAILED: {error_message}")
