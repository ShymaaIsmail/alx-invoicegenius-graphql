# invoices/filters.py
import django_filters
from django_filters import OrderingFilter
from invoices.models import Invoice

class InvoiceFilter(django_filters.FilterSet):
    """FilterSet for Invoice model and related ParsedInvoiceData."""

    uploaded_from = django_filters.DateTimeFilter(
        field_name="uploaded_at",
        lookup_expr="gte",
        label="Uploaded after or on"
    )

    uploaded_to = django_filters.DateTimeFilter(
        field_name="uploaded_at",
        lookup_expr="lte",
        label="Uploaded before or on"
    )

    parsed_vendor = django_filters.CharFilter(
        field_name="parsed_data__vendor",
        lookup_expr="icontains",
        label="Vendor name contains"
    )

    parsed_invoice_date = django_filters.DateFilter(
        field_name="parsed_data__invoice_date",
        label="Invoice date"
    )

    parsed_total_amount = django_filters.NumberFilter(
        field_name="parsed_data__total_amount",
        label="Total amount"
    )

    order_by = OrderingFilter(
        fields=(
            ('uploaded_at', 'uploaded_at'),
            ('parsed_data__invoice_date', 'parsed_invoice_date'),
            ('parsed_data__total_amount', 'parsed_total_amount'),
        ),
        field_labels={
            'uploaded_at': 'Upload date',
            'parsed_data__invoice_date': 'Invoice date',
            'parsed_data__total_amount': 'Total amount',
        },
        label="Order by"
    )

    class Meta:
        model = Invoice
        fields = {
            "status": ["exact", "in"],
            "processed": ["exact"],
            "processing_error": ["isnull", "icontains"],
            "parsed_data__vendor": ["icontains"],
            "parsed_data__invoice_date": ["exact", "gte", "lte"],
            "parsed_data__total_amount": ["exact", "gte", "lte"],
        }
