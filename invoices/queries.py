# invoices/queries.py or invoices/schema.py

import graphene
from graphql_jwt.decorators import login_required
from graphene_django.filter import DjangoFilterConnectionField
from invoices.models import Invoice
from invoices.types import InvoiceType, InvoiceNode
from invoices.filters import InvoiceFilter


class InvoiceQuery(graphene.ObjectType):
    """Authenticated GraphQL queries for accessing user invoices."""

    # Relay-compatible list with filtering
    my_invoices = DjangoFilterConnectionField(
        InvoiceNode,
        filterset_class=InvoiceFilter,
        description="List of invoices uploaded by the logged-in user with filters"
    )

    # Standard (non-relay) single invoice by ID
    invoice = graphene.Field(
        InvoiceType,
        id=graphene.ID(required=True),
        description="Fetch a specific invoice by ID"
    )

    @login_required
    def resolve_my_invoices(self, info, **kwargs):
        """Resolve the list of invoices for the authenticated user."""
        user = info.context.user
        return (
            Invoice.objects
            .filter(user=user)
            .order_by('-uploaded_at')
            .select_related('parsed_data')
        )

    @login_required
    def resolve_invoice(self, info, id):
        """Resolve a single invoice by ID for the authenticated user."""
        user = info.context.user
        invoice = (
            Invoice.objects
            .filter(id=id, user=user)
            .select_related('parsed_data')
            .first()
        )

        if invoice and (not invoice.processed):
            invoice.parsed_data = None

        return invoice
