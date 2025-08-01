# invoices/types.py

import graphene
from graphene import relay
from graphene_django.types import DjangoObjectType
from invoices.models import Invoice, ParsedInvoiceData


class LineItemType(graphene.ObjectType):
    description = graphene.String()
    quantity = graphene.Int()
    unit_price = graphene.Float()
    total_price = graphene.Float()


class ParsedInvoiceDataType(DjangoObjectType):
    line_items = graphene.List(LineItemType)

    class Meta:
        model = ParsedInvoiceData
        fields = "__all__"

    def resolve_line_items(self, info):
        try:
            return self.line_items or []
        except Exception:
            return []


class InvoiceType(DjangoObjectType):
    parsed_data = graphene.Field(ParsedInvoiceDataType)

    class Meta:
        model = Invoice
        fields = "__all__"

    def resolve_parsed_data(self, info):
        try:
            return self.parsed_data
        except ParsedInvoiceData.DoesNotExist:
            return None


class InvoiceNode(DjangoObjectType):
    class Meta:
        model = Invoice
        interfaces = (relay.Node,)
        fields = "__all__"
        filter_fields = {
            'status': ['exact'],
        }
