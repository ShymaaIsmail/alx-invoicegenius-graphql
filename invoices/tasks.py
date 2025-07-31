import mimetypes
import logging
from celery import shared_task
from invoices.models import Invoice
from ocr.utils import extract_text_from_pdf, extract_text_from_image
from ai_parser.utils import parse_invoice_text

logger = logging.getLogger(__name__)

@shared_task
def process_invoice_file(invoice_id):
    logger.info(f"Starting processing of invoice ID: {invoice_id}")

    try:
        invoice = Invoice.objects.get(id=invoice_id)
        logger.info(f"Invoice found: ID={invoice.id}, file={invoice.original_file}")

        file_path = invoice.original_file.path
        logger.info(f"File path resolved: {file_path}")

        mime_type, _ = mimetypes.guess_type(file_path)
        logger.info(f"Guessed MIME type: {mime_type}")

        if mime_type == "application/pdf":
            logger.info("Detected PDF file. Extracting text...")
            text = extract_text_from_pdf(file_path)
            logger.info(f"Extracted text length: {len(text) if text else 'None'}")
        elif mime_type and mime_type.startswith("image/"):
            logger.info("Detected image file. Extracting text...")
            text = extract_text_from_image(file_path)
            logger.info(f"Extracted text length: {len(text) if text else 'None'}")
        else:
            logger.warning(f"Unsupported MIME type for file: {file_path} (MIME: {mime_type})")
            invoice.status = "FAILED"
            invoice.processing_error = f"Unsupported MIME type: {mime_type}"
            invoice.save()
            logger.info("Invoice status set to FAILED due to unsupported MIME type.")
            return

        if not text:
            logger.warning(f"No text extracted from file: {file_path}")
            invoice.status = "FAILED"
            invoice.processing_error = "No text extracted from the invoice file."
            invoice.save()
            logger.info("Invoice status set to FAILED due to empty extracted text.")
            return

        logger.info("Parsing extracted text...")
        # parsed_data = parse_invoice_text(text)
        parsed_data =  {
            "vendor_name": "Berghotel",
            "invoice_number": "4572",
            "invoice_date": "2007-07-30",
            "total_amount": {
                "value": 54.5,
                "currency": "CHF"
            },
            "tax": {
                "value": 3.85,
                "currency": "CHF"
            }
            }
        logger.info(f"Parsed data: {parsed_data}")

        if parsed_data:
            invoice.vendor_name = parsed_data.get("vendor_name")
            invoice.invoice_number = parsed_data.get("invoice_number")
            invoice.invoice_date = parsed_data.get("invoice_date")
            invoice.total_amount = parsed_data.get("total_amount")
            invoice.tax = parsed_data.get("tax")
            invoice.status = "PROCESSED"
            invoice.processing_error = None
            logger.info("Invoice fields updated and status set to PROCESSED.")
        else:
            invoice.status = "FAILED"
            invoice.processing_error = "AI parsing failed: no data extracted from text."
            logger.warning("Parsing failed, no data extracted. Invoice marked as FAILED.")

        invoice.save()
        logger.info(f"Invoice ID {invoice_id} processing completed.")

    except Invoice.DoesNotExist:
        logger.error(f"Invoice with ID {invoice_id} does not exist.")
    except Exception as e:
        logger.exception(f"Unexpected error while processing invoice {invoice_id}: {e}")
        try:
            invoice.status = "FAILED"
            invoice.processing_error = str(e)
            invoice.save()
        except Exception:
            logger.error("Unable to save invoice error details.")
        logger.info("Invoice status set to FAILED due to processing error.")
