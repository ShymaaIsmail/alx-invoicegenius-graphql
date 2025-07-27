import graphene
from .queries import InvoiceQuery
from .mutations import UploadInvoiceMutation

class Query(InvoiceQuery, graphene.ObjectType):
    pass

class Mutation(UploadInvoiceMutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
