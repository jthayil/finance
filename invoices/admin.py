from django.contrib import admin

from invoices.models import Invoices, InvoiceItems

# Register your models here.
class InvoicesAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "invoice_no", "buyer", "shipTo", "shipTo", "status"]


admin.site.register(Invoices, InvoicesAdmin)


class InvoiceItemsAdmin(admin.ModelAdmin):
    list_display = ["id", "invoice_id", "inventory_id", "item", "sgst", "cgst", "igst", "rate", "qty"]


admin.site.register(InvoiceItems, InvoiceItemsAdmin)