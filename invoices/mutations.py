from graphene_file_upload.scalars import Upload
import graphene
from graphql_jwt.decorators import login_required
from django.core.files.base import ContentFile
from invoices.models import Invoice
from invoices.types import InvoiceType
from invoices.tasks import process_invoice_file
from invoices.utils import compute_file_hash
from storages.backends.s3boto3 import S3Boto3Storage  # import S3 storage


class UploadInvoice(graphene.Mutation):
    """Mutation to upload an invoice file."""
    class Arguments:
        file = Upload(required=True)

    invoice = graphene.Field(InvoiceType)
    success = graphene.Boolean()
    message = graphene.String()

    @login_required
    def mutate(self, info, file, **kwargs):
        user = info.context.user

        if not file.name.lower().endswith((".pdf", ".png", ".jpg", ".jpeg")):
            return UploadInvoice(success=False, message="Invalid file type.", invoice=None)

        file_content = file.read()
        file_hash = compute_file_hash(file_content)

        existing = Invoice.objects.filter(file_hash=file_hash).first()
        if existing:
            return UploadInvoice(success=False, message="Invoice already exists.", invoice=existing)

        s3_storage = S3Boto3Storage()  # create S3 storage instance explicitly
        path = s3_storage.save(f"invoices/{file.name}", ContentFile(file_content))

        invoice = Invoice.objects.create(
            user=user,
            original_file=path,
            status="PENDING",
            file_hash=file_hash
        )

        process_invoice_file.delay(invoice.id)

        return UploadInvoice(success=True, message="Invoice uploaded successfully.", invoice=invoice)


class UploadInvoiceMutation(graphene.ObjectType):
    upload_invoice = UploadInvoice.Field()
