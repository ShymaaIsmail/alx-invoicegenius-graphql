import graphene
from graphql_jwt.decorators import login_required
from .types import InvoiceType
from .models import Invoice


class InvoiceQuery(graphene.ObjectType):
    """Authenticated queries for accessing user invoices."""
    my_invoices = graphene.List(InvoiceType)
    invoice = graphene.Field(InvoiceType, id=graphene.ID(required=True))

    @login_required
    def resolve_my_invoices(self, info):
        user = info.context.user
        return (
            Invoice.objects
            .filter(user=user)
            .order_by('-uploaded_at')
            .prefetch_related('parsed_data')  # safe to prefetch; won't error if null
        )

    @login_required
    def resolve_invoice(self, info, id):
        user = info.context.user
        invoice = (
            Invoice.objects
            .filter(id=id, user=user)
            .select_related('parsed_data')  # will work only if parsed_data exists
            .first()
        )

        # If not processed, ignore parsed_data (optional logic)
        if invoice and not invoice.processed:
            invoice.parsed_data = None  # hide parsed_data if not processed
        return invoice
