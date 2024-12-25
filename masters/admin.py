from django.contrib import admin
from masters.models import HSN, Pincodes, Company, Inventory


class CompanyAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "provider",
        "name",
        "gstin",
        "bank",
        "bank_account_holder",
        "bank_no",
        "bank_ifsc",
    ]


admin.site.register(Company, CompanyAdmin)


class HSNAdmin(admin.ModelAdmin):
    list_display = [
        "hsn_code",
        "description",
    ]


admin.site.register(HSN, HSNAdmin)


class InventoryAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "hsn_id",
        "rate",
        "qty",
        "min_stock",
        "sgst",
        "cgst",
        "igst",
    ]


admin.site.register(Inventory, InventoryAdmin)


class PincodesAdmin(admin.ModelAdmin):
    list_display = ["pincode", "city", "state", "country"]


admin.site.register(Pincodes, PincodesAdmin)
