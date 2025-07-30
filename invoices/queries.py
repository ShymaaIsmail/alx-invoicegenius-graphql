import graphene
from graphql_jwt.decorators import login_required
from .types import InvoiceType
from .models import Invoice


class InvoiceQuery(graphene.ObjectType):
    """Queries for invoices."""
    my_invoices = graphene.List(InvoiceType)
    invoice = graphene.Field(InvoiceType, id=graphene.ID(required=True))

    @login_required
    def resolve_my_invoices(self, info):
        user = info.context.user
        return Invoice.objects.filter(user=user).order_by('-uploaded_at')

    @login_required
    def resolve_invoice(self, info, id):
        user = info.context.user
        try:
            invoice = Invoice.objects.get(id=id, user=user)
            return invoice
        except Invoice.DoesNotExist:
            return None
