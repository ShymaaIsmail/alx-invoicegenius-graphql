from django.contrib import admin
from .models import Invoice, ParsedInvoiceData

"""Register your models here to make them accessible in the Django admin interface."""

admin.site.register(Invoice)
admin.site.register(ParsedInvoiceData)
