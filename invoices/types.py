import graphene
from graphene_django.types import DjangoObjectType
from invoices.models import Invoice, ParsedInvoiceData

class ParsedInvoiceDataType(DjangoObjectType):
    class Meta:
        model = ParsedInvoiceData
        fields = "__all__"

class InvoiceType(DjangoObjectType):
    parsed_data = graphene.Field(ParsedInvoiceDataType)

    class Meta:
        model = Invoice
        fields = "__all__"

    def resolve_parsed_data(self, info):
        # Avoid exception if parsed_data does not exist
        try:
            return self.parsed_data
        except ParsedInvoiceData.DoesNotExist:
            return None
