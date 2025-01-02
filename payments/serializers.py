from rest_framework import serializers
from masters.serializers import CompanySerializer
from payments.models import Payments, InvoicePayments


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = "__all__"


class InvoicePaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoicePayments
        fields = "__all__"


class InvoicePaymentListSerializer(serializers.ModelSerializer):
    buyer = serializers.CharField(source='payment_id.buyer_id.name')

    class Meta:
        model = InvoicePayments
        fields = ["payment_id", "buyer", "invoice_id", "allocated_amt", "inserted_On"]
