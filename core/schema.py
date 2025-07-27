# core/schema.py
import graphene

# Import query & mutation classes from each app
from authentication.schema import Query as AuthQuery, Mutation as AuthMutation
from invoices.schema import Query as InvoiceQuery, Mutation as InvoiceMutation

# Combine all app queries
class Query(
    AuthQuery,
    InvoiceQuery,
    graphene.ObjectType
):
    pass

# Combine all app mutations
class Mutation(
    AuthMutation,
    InvoiceMutation,
    graphene.ObjectType
):
    pass

# Final unified schema
schema = graphene.Schema(query=Query, mutation=Mutation)
