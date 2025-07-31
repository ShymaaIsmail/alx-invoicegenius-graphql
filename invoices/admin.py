from django.contrib import admin
from .models import Invoice, ParsedInvoiceData

admin.site.register(Invoice)
admin.site.register(ParsedInvoiceData)
