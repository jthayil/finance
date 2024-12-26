from django.forms import ModelForm
from .models import InvoiceItems, Invoices


class InvoicesModelForm(ModelForm):
    class Meta:
        model = Invoices
        fields = ["user", "invoice_no", "discount", "buyer", "shipTo"]


class InvoiceItemsModelForm(ModelForm):
    class Meta:
        model = InvoiceItems
        fields = ["invoice_id", "inventory_id", "item", "rate", "qty", "discount", "sgst", "cgst", "igst"]


# eof
