import logging
import mimetypes
from django.conf import settings
import requests
from tempfile import NamedTemporaryFile
from celery import shared_task
from dateutil.parser import parse
from django.utils import timezone
from invoices.models import Invoice, ParsedInvoiceData
from ocr.utils import extract_text_from_pdf, extract_text_from_image
from ai_parser.utils import parse_invoice_text

logger = logging.getLogger(__name__)


def get_download_filename(invoice):
    if invoice.original_file:
        return f"{settings.SITE_DOMAIN}{invoice.original_file.url}"
    return None

def normalize_date(date_str):
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
        file_url = get_download_filename(invoice)
        logger.info(f"Downloading invoice file from: {file_url}")

        response = requests.get(file_url)
        if response.status_code != 200:
            msg = f"Failed to download invoice file. HTTP {response.status_code}"
            logger.warning(msg)
            _mark_invoice_failed(invoice, msg)
            return

        with NamedTemporaryFile(delete=True, suffix=".pdf") as tmp_file:
            tmp_file.write(response.content)
            tmp_file.flush()

            mime_type, _ = mimetypes.guess_type(tmp_file.name)
            logger.info(f"Detected MIME type: {mime_type}")

            if mime_type == "application/pdf":
                text = extract_text_from_pdf(tmp_file.name)
            elif mime_type and mime_type.startswith("image/"):
                text = extract_text_from_image(tmp_file.name)
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

        logger.info(f"Parsing extracted text... {text}")
        parsed_data = parse_invoice_text(text)

        if not parsed_data:
            msg = "AI parsing failed: no data extracted from text."
            logger.warning(msg)
            _mark_invoice_failed(invoice, msg)
            return

        logger.info(f"Parsed data: {parsed_data}")
        total = parsed_data.get("total_amount", {})
        tax = parsed_data.get("tax", {})

        ParsedInvoiceData.objects.create(
            invoice=invoice,
            vendor=parsed_data.get("vendor_name"),
            invoice_date=normalize_date(parsed_data.get("invoice_date")),
            total_amount=total.get("value"),
            tax_amount=tax.get("value"),
            currency=total.get("currency") or tax.get("currency"),
            line_items=parsed_data.get("line_items") or [],
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
    invoice.status = Invoice.STATUS_FAILED
    invoice.processing_error = error_message
    invoice.processed = False
    invoice.processed_at = timezone.now()
    invoice.save()
    logger.info(f"Invoice {invoice.id} marked as FAILED: {error_message}")
