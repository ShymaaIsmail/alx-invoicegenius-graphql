
# invoices/types.py

import graphene
from graphene import relay
from graphene_django.types import DjangoObjectType
from invoices.models import Invoice, ParsedInvoiceData


class LineItemType(graphene.ObjectType):
    """GraphQL type for line items in parsed invoice data."""
    description = graphene.String()
    quantity = graphene.Int()
    unit_price = graphene.Float()
    total_price = graphene.Float()


class ParsedInvoiceDataType(DjangoObjectType):
    """GraphQL type for ParsedInvoiceData model with line items."""
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
    """GraphQL type for Invoice model with additional fields."""
    parsed_data = graphene.Field(ParsedInvoiceDataType)
    is_valid_invoice = graphene.Boolean()


    class Meta:
        model = Invoice
        fields = "__all__"

    def resolve_parsed_data(self, info):
        """Resolve the parsed data for the invoice."""
        try:
            return self.parsed_data
        except ParsedInvoiceData.DoesNotExist:
            return None

    def resolve_is_valid_invoice(self, info):
        """Check if the invoice has valid parsed data."""
        if not hasattr(self, "parsed_data"):
            return False
        parsed = self.parsed_data
        return bool(parsed.vendor and parsed.invoice_date and parsed.total_amount)


class InvoiceNode(DjangoObjectType):
    """Relay-compatible GraphQL type for Invoice model."""
    is_valid_invoice = graphene.Boolean()

    class Meta:
        model = Invoice
        interfaces = (relay.Node,)
        fields = "__all__"
        filter_fields = {
            'status': ['exact'],
        }

    def resolve_is_valid_invoice(self, info):
        """Check if the invoice has valid parsed data."""
        if not hasattr(self, "parsed_data"):
            return False
        parsed = self.parsed_data
        return bool(parsed.vendor and parsed.invoice_date and parsed.total_amount)



=======
# invoices/types.py

import graphene
from graphene import relay
from graphene_django.types import DjangoObjectType
from invoices.models import Invoice, ParsedInvoiceData


class LineItemType(graphene.ObjectType):
    """GraphQL type for line items in parsed invoice data."""
    description = graphene.String()
    quantity = graphene.Int()
    unit_price = graphene.Float()
    total_price = graphene.Float()


class ParsedInvoiceDataType(DjangoObjectType):
    """GraphQL type for ParsedInvoiceData model with line items."""
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
    """GraphQL type for Invoice model with additional fields."""
    parsed_data = graphene.Field(ParsedInvoiceDataType)
    is_valid_invoice = graphene.Boolean()


    class Meta:
        model = Invoice
        fields = "__all__"

    def resolve_parsed_data(self, info):
        """Resolve the parsed data for the invoice."""
        try:
            return self.parsed_data
        except ParsedInvoiceData.DoesNotExist:
            return None

    def resolve_is_valid_invoice(self, info):
        """Check if the invoice has valid parsed data."""
        if not hasattr(self, "parsed_data"):
            return False
        parsed = self.parsed_data
        return bool(parsed.vendor and parsed.invoice_date and parsed.total_amount)


class InvoiceNode(DjangoObjectType):
    """Relay-compatible GraphQL type for Invoice model."""
    is_valid_invoice = graphene.Boolean()

    class Meta:
        model = Invoice
        interfaces = (relay.Node,)
        fields = "__all__"
        filter_fields = {
            'status': ['exact'],
        }

    def resolve_is_valid_invoice(self, info):
        """Check if the invoice has valid parsed data."""
        if not hasattr(self, "parsed_data"):
            return False
        parsed = self.parsed_data
        return bool(parsed.vendor and parsed.invoice_date and parsed.total_amount)




