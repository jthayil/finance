from django.forms import ModelForm
from payments.models import Payments, InvoicePayments


class PaymentsModelForm(ModelForm):
    class Meta:
        model = Payments
        fields = ["user", "utr_file", "buyer_id"]


class InvoicePaymentsModelForm(ModelForm):
    class Meta:
        model = InvoicePayments
        fields = "__all__"


# eof
