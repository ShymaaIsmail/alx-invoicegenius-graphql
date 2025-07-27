import mimetypes
import logging
from celery import shared_task
from invoices.models import Invoice
from ocr.utils import extract_text_from_pdf, extract_text_from_image
from ai_parser.utils import parse_invoice_text

logger = logging.getLogger(__name__)

@shared_task
def process_invoice_file(invoice_id):
    try:
        invoice = Invoice.objects.get(id=invoice_id)
        file_path = invoice.original_file.path

        mime_type, _ = mimetypes.guess_type(file_path)

        if mime_type == "application/pdf":
            text = extract_text_from_pdf(file_path)
        elif mime_type and mime_type.startswith("image/"):
            text = extract_text_from_image(file_path)
        else:
            logger.warning(f"Unsupported MIME type for file: {file_path}")
            invoice.status = "FAILED"
            invoice.save()
            return

        if not text:
            logger.warning(f"No text extracted from file: {file_path}")
            invoice.status = "FAILED"
            invoice.save()
            return

        parsed_data = parse_invoice_text(text)

        if parsed_data:
            invoice.vendor_name = parsed_data.get("vendor_name")
            invoice.invoice_number = parsed_data.get("invoice_number")
            invoice.invoice_date = parsed_data.get("invoice_date")
            invoice.total_amount = parsed_data.get("total_amount")
            invoice.tax = parsed_data.get("tax")
            invoice.status = "PROCESSED"
        else:
            invoice.status = "FAILED"

        invoice.save()

    except Invoice.DoesNotExist:
        logger.error(f"Invoice with ID {invoice_id} does not exist.")
    except Exception as e:
        logger.exception(f"Unexpected error while processing invoice {invoice_id}: {e}")
