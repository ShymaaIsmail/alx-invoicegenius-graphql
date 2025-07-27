# invoices/types.py
import graphene
from graphene_django.types import DjangoObjectType
from invoices.models import Invoice

class InvoiceType(DjangoObjectType):
    class Meta:
        model = Invoice
        fields = "__all__"
