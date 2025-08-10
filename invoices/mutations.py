from graphene_file_upload.scalars import Upload
import graphene
from graphql_jwt.decorators import login_required
from django.core.files.base import ContentFile
from invoices.models import Invoice
from invoices.types import InvoiceType
from invoices.tasks import process_invoice_file
from invoices.utils import compute_file_hash
from storages.backends.s3boto3 import S3Boto3Storage


class UploadInvoice(graphene.Mutation):
    """
    Uploads an invoice file (PDF or image) to the system.

    This mutation:
    - Accepts `.pdf`, `.png`, `.jpg`, or `.jpeg` files.
    - Checks for duplicates using a file hash.
    - Stores the file in S3.
    - Creates an `Invoice` record with `PENDING` status.
    - Triggers background processing of the uploaded invoice.
    """

    class Arguments:
        file = Upload(
            required=True,
            description=(
                "The invoice file to upload. "
                "Supported formats: PDF, PNG, JPG, JPEG."
            )
        )

    invoice = graphene.Field(
        InvoiceType,
        description="The created invoice object. Null if the upload failed."
    )
    success = graphene.Boolean(
        description="Whether the upload was successful."
    )
    message = graphene.String(
        description="A message describing the result of the operation."
    )

    @login_required
    def mutate(self, info, file, **kwargs):
        user = info.context.user

        # Validate file type
        if not file.name.lower().endswith((".pdf", ".png", ".jpg", ".jpeg")):
            return UploadInvoice(
                success=False,
                message="Invalid file type. Allowed: PDF, PNG, JPG, JPEG.",
                invoice=None
            )

        # Compute file hash to detect duplicates
        file_content = file.read()
        file_hash = compute_file_hash(file_content)

        existing = Invoice.objects.filter(file_hash=file_hash, user=user).first()
        if existing:
            return UploadInvoice(
                success=False,
                message="Invoice already exists.",
                invoice=existing
            )

        # Save to S3
        s3_storage = S3Boto3Storage()
        path = s3_storage.save(f"invoices/{file.name}", ContentFile(file_content))

        # Create invoice record
        invoice = Invoice.objects.create(
            user=user,
            original_file=path,
            status="PENDING",
            file_hash=file_hash
        )

        # Trigger async processing
        process_invoice_file.delay(invoice.id)

        return UploadInvoice(
            success=True,
            message="Invoice uploaded successfully.",
            invoice=invoice
        )


class UploadInvoiceMutation(graphene.ObjectType):
    """
    Mutation group for handling invoice file uploads.
    """
    upload_invoice = UploadInvoice.Field(
        description="Upload a new invoice file to be processed."
    )
