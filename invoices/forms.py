from django.forms import ModelForm
from .models import InvoiceItems, Invoices


class InvoicesModelForm(ModelForm):
    class Meta:
        model = Invoices
        fields = ["user", "invoice_no", "buyer", "shipTo"]


class InvoiceItemsModelForm(ModelForm):
    class Meta:
        model = InvoiceItems
        fields = ["invoice_id", "inventory_id", "item", "sgst", "cgst", "igst", "rate", "qty"]


# eof
