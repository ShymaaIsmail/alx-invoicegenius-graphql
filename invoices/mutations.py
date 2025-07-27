# invoices/mutations.py
from graphene_file_upload.scalars import Upload
import graphene
from graphql_jwt.decorators import login_required
from invoices.models import Invoice
from invoices.types import InvoiceType
from invoices.tasks import process_invoice_file
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

class UploadInvoiceMutation(graphene.Mutation):
    class Arguments:
        file = Upload(required=True)

    invoice = graphene.Field(InvoiceType)
    success = graphene.Boolean()
    message = graphene.String()

    @login_required
    def mutate(self, info, file, **kwargs):
        user = info.context.user

        if not file.name.lower().endswith((".pdf", ".png", ".jpg", ".jpeg")):
            return UploadInvoiceMutation(success=False, message="Invalid file type.", invoice=None)

        path = default_storage.save(f"invoices/{file.name}", ContentFile(file.read()))

        invoice = Invoice.objects.create(
            user=user,
            original_file=path,
            status="PENDING"
        )

        process_invoice_file.delay(invoice.id)

        return UploadInvoiceMutation(success=True, message="Invoice uploaded successfully.", invoice=invoice)
