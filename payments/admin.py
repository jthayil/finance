from django.contrib import admin
from payments.models import Payments, InvoicePayments


class PaymentsAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "received_amt", "buyer_id", "utr_file", "status"]


admin.site.register(Payments, PaymentsAdmin)


class InvoicePaymentsAdmin(admin.ModelAdmin):
    list_display = ["id", "payment_id", "allocated_amt", "tds_percent"]


admin.site.register(InvoicePayments, InvoicePaymentsAdmin)
