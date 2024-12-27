from rest_framework import serializers
from invoices.models import InvoiceItems, Invoices
from django.db.models import Sum


class InvoiceItemsSerializer(serializers.ModelSerializer):
    discount_amt = serializers.SerializerMethodField()
    total_amt = serializers.SerializerMethodField()

    def get_discount_amt(self, obj):
        if obj.discount != 0:
            amt = obj.rate * obj.qty
            return round(amt * (obj.discount / 100), 2)
        return 0
    
    def get_total_amt(self, obj):
        amt = (obj.qty * obj.rate) - self.get_discount_amt(obj)
        return round(amt + (amt * ((obj.sgst + obj.cgst + obj.igst) / 100)), 2)

    class Meta:
        model = InvoiceItems
        fields = "__all__"


class InvoiceItemSerializer(serializers.ModelSerializer):
    amount = serializers.FloatField(source="amount")
    tax = serializers.FloatField(source="tax")
    taxable_amount = serializers.FloatField(source="taxable_amount")

    class Meta:
        model = InvoiceItems
        fields = ["amount", "tax", "taxable_amount"]


class InvoiceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    buyer = serializers.CharField()
    inserted_On = serializers.DateTimeField()
    invoice_no = serializers.IntegerField()
    status = serializers.IntegerField()

    qty = serializers.SerializerMethodField()
    taxable_amt = serializers.SerializerMethodField()
    tax = serializers.SerializerMethodField()
    total_amt = serializers.SerializerMethodField()

    def get_qty(self, obj):
        return (
            InvoiceItems.objects.filter(invoice_id=obj.id).aggregate(total=Sum("qty"))[
                "total"
            ]
            or 0
        )

    def get_taxable_amt(self, obj):
        return sum(
            item.taxable_amt()
            for item in InvoiceItems.objects.filter(invoice_id=obj.id)
        )

    def get_tax(self, obj):
        return sum(
            item.tax_amt() for item in InvoiceItems.objects.filter(invoice_id=obj.id)
        )

    def get_total_amt(self, obj):
        amt = sum(
            item.total_amount()
            for item in InvoiceItems.objects.filter(invoice_id=obj.id)
        ) + self.get_tax(obj)
        return amt.__round__(2)

    class Meta:
        model = Invoices
        fields = [
            "id",
            "inserted_On",
            "buyer",
            "invoice_no",
            "qty",
            "taxable_amt",
            "tax",
            "total_amt",
            "status",
        ]
