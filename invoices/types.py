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
    download_filename = graphene.String()
    is_valid_invoice = graphene.Boolean()


    class Meta:
        model = Invoice
        fields = "__all__"

    def resolve_parsed_data(self, info):
        try:
            return self.parsed_data
        except ParsedInvoiceData.DoesNotExist:
            return None

    def resolve_download_filename(self, info):
        request = info.context
        if self.original_file and request:
            return request.build_absolute_uri(self.original_file.url)
        return None

    def resolve_is_valid_invoice(self, info):
        parsed = self.parsed_data
        if not parsed:
            return False
        return bool(parsed.vendor and parsed.invoice_date and parsed.total_amount)

class InvoiceNode(DjangoObjectType):
    download_filename = graphene.String()
    is_valid_invoice = graphene.Boolean()

    class Meta:
        model = Invoice
        interfaces = (relay.Node,)
        fields = "__all__"
        filter_fields = {
            'status': ['exact'],
        }
    
    def resolve_download_filename(self, info):
        request = info.context
        if self.original_file and request:
            return request.build_absolute_uri(self.original_file.url)
        return None

    def resolve_is_valid_invoice(self, info):
        parsed = self.parsed_data
        if not parsed:
            return False
        return bool(parsed.vendor and parsed.invoice_date and parsed.total_amount)




