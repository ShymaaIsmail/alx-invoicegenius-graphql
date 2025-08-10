import graphene
from .queries import InvoiceQuery
from .mutations import UploadInvoiceMutation

class Query(InvoiceQuery, graphene.ObjectType):
    """Root Query for the InvoiceGenius GraphQL API."""
    pass

class Mutation(UploadInvoiceMutation, graphene.ObjectType):
    """Root Mutation for the InvoiceGenius GraphQL API."""
    pass

schema = graphene.Schema(
    query=Query,
    mutation=Mutation,
    description=(
        "InvoiceGenius GraphQL API\n\n"
        "Use this API to upload invoices, fetch your uploaded invoices, "
        "and view parsed invoice details. Authentication is required for all operations."
    )
)
