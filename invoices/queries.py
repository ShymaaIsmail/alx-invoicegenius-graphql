import graphene
from graphql_jwt.decorators import login_required
from graphene_django.filter import DjangoFilterConnectionField
from invoices.models import Invoice
from invoices.types import InvoiceType, InvoiceNode
from invoices.filters import InvoiceFilter


class InvoiceQuery(graphene.ObjectType):
    """
    Authenticated GraphQL queries for retrieving and filtering invoices.

    Provides:
    - A Relay-compatible list of invoices with filtering support (`my_invoices`).
    - A standard query for fetching a single invoice by ID (`invoice`).
    """

    my_invoices = DjangoFilterConnectionField(
        InvoiceNode,
        filterset_class=InvoiceFilter,
        description=(
            "Retrieve a paginated, filterable list of invoices uploaded by the logged-in user. "
            "Supports Relay cursor-based pagination and filtering by fields such as `status`, "
            "`uploaded_at`, or `file_hash`."
        )
    )

    invoice = graphene.Field(
        InvoiceType,
        id=graphene.ID(required=True, description="The unique ID of the invoice."),
        description="Fetch details of a specific invoice by its unique ID."
    )

    @login_required
    def resolve_my_invoices(self, info, **kwargs):
        """
        Returns all invoices belonging to the authenticated user, ordered by most recent uploads.
        Includes parsed data when available.
        """
        user = info.context.user
        return (
            Invoice.objects
            .filter(user=user)
            .order_by('-uploaded_at')
            .select_related('parsed_data')
        )

    @login_required
    def resolve_invoice(self, info, id):
        """
        Retrieves a single invoice by ID for the authenticated user.

        If the invoice is still being processed (`processed=False`),
        the `parsed_data` field will be `null` until processing completes.
        """
        user = info.context.user
        invoice = (
            Invoice.objects
            .filter(id=id, user=user)
            .select_related('parsed_data')
            .first()
        )

        if invoice and not invoice.processed:
            invoice.parsed_data = None

        return invoice
