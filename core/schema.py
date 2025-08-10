import graphene

# Import query & mutation classes from each app
from authentication.schema import Query as AuthQuery, Mutation as AuthMutation
from invoices.schema import Query as InvoiceQuery, Mutation as InvoiceMutation


class Query(
    AuthQuery,
    InvoiceQuery,
    graphene.ObjectType
):
    """InvoiceGenius GraphQL API – Query root.

    Use these queries to:
    - Fetch your account details (`me`)
    - List and filter invoices you’ve uploaded
    - Retrieve parsed invoice data
    """
    pass


class Mutation(
    AuthMutation,
    InvoiceMutation,
    graphene.ObjectType
):
    """InvoiceGenius GraphQL API – Mutation root.

    Use these mutations to:
    - Authenticate (JWT / Google login)
    - Upload invoices for parsing
    - Manage your account session
    """
    pass


schema = graphene.Schema(
    query=Query,
    mutation=Mutation,

)
