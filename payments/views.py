from django.http import JsonResponse
from django.shortcuts import render
from invoices.models import Invoices
from invoices.serializers import InvoicePaymentSerializer
from masters.models import Company
from payments.forms import InvoicePaymentsModelForm, PaymentsModelForm
from payments.models import Payments, InvoicePayments
from django_filters.rest_framework import DjangoFilterBackend
from payments.serializers import InvoicePaymentListSerializer, PaymentsSerializer, InvoicePaymentsSerializer
from django.db.models import Sum
from django.db.models.functions import Coalesce


from rest_framework import generics
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated


def v_payment_list(request):
    context = {}
    return render(request, "payments/list.html", context)


def v_payment_create(request):
    if request.method == "POST":
        print(request.POST)
        form = PaymentsModelForm(request.POST, request.FILES)
        if form.is_valid():
            o_payment = form.save()
            sez = PaymentsSerializer(o_payment)
            return JsonResponse(
                {"status": True, "message": "Successfully Saved", "data": sez.data},
                safe=False,
            )
        else:
            return JsonResponse(
                {"status": False, "message": "Failed Saving", "data": form.errors},
                safe=False,
            )
    context = {"company": Company.objects.exclude(provider=True)}
    return render(request, "payments/create.html", context)


def v_invoicepayment_create(request):
    if request.method == "POST":
        print(request.POST)
        form = InvoicePaymentsModelForm(request.POST)
        if form.is_valid():
            o_payment = form.save()
            sez = InvoicePaymentsSerializer(o_payment)
            return JsonResponse(
                {"status": True, "message": "Successfully Saved", "data": sez.data},
                safe=False,
            )
        else:
            return JsonResponse(
                {"status": False, "message": "Failed Saving", "data": form.errors},
                safe=False,
            )
    context = {}
    return render(request, "payments/create.html", context)


def v_pending_payment_of_company(request, pk):
    pending_list = []
    invoices = Invoices.objects.filter(buyer_id=pk, deleted=False).annotate(
        received_amt=Coalesce(Sum("invoicepayments__allocated_amt"), float(0))
    )
    for invoice in invoices:
        if invoice.received_amt < invoice.invoice_total():
            pending_list.append(invoice)
    serializer = InvoicePaymentSerializer(pending_list, many=True)
    return JsonResponse(serializer.data, safe=False)


class InvoicePaymentData(generics.ListAPIView):
    api_view = ["GET"]
    permission_classes = [IsAuthenticated]
    queryset = InvoicePayments.objects.all()
    serializer_class = InvoicePaymentListSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ["id"]
    search_fields = "__all__"
    ordering_fields = "__all__"
