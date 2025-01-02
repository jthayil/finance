from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated

from fms.dj_support import render_file_else_response
from masters.models import Company, Inventory

from invoices.forms import InvoiceItemsModelForm, InvoicesModelForm
from invoices.models import InvoiceItems, Invoices
from invoices.serializers import InvoiceItemsSerializer, InvoiceSerializer


@login_required
def v_dashboard(request):
    return render(request, "invoice/dashboard.html", {})


@login_required
def v_invoice_list(request):
    customer = Company.objects.filter(provider=False)
    context = {"customers": customer}
    return render(request, "invoice/list.html", context)


@login_required
def v_invoice_create(request):
    f_invoice = InvoicesModelForm()

    if request.method == "POST":
        f_invoice = InvoicesModelForm(request.POST)
        if f_invoice.is_valid():
            invoice = f_invoice.save()
            return redirect("invoices:invoice_item_create", fk=invoice.id, pk=0)
        else:
            for field, err in f_invoice.errors.items():
                messages.warning(
                    request, str(field).replace("_", " ") + " : " + str(err[0])
                )

    context = {"vendors": Company.objects.all(), "form": f_invoice}
    return render(request, "invoice/create.html", context)


@login_required
def v_invoice_fingerpost(request, pk):
    invoice = get_object_or_404(Invoices, id=pk)
    if invoice.status == 1:
        return redirect("invoices:invoice_receipt", pk=invoice.id)
    return redirect("invoices:invoice_update", pk=invoice.id)


@login_required
def v_invoice_generate(request, pk):
    invoice = get_object_or_404(Invoices, id=pk)
    if request.method == "POST":
        f_invoice = InvoicesModelForm(request.POST, instance=invoice)
        if f_invoice.is_valid():
            items = InvoiceItems.objects.filter(invoice_id=pk)
            for item in items:
                item.inventory_id.qty -= item.qty
                item.inventory_id.save()
            invoice.status = 1
            invoice.save()
            messages.success(request, "Invoice Generated")
            return redirect("invoices:invoice_list")
        else:
            for field, err in f_invoice.errors.items():
                messages.warning(
                    request, str(field).replace("_", " ") + " : " + str(err[0])
                )

    context = {"vendors": Company.objects.all(), "form": f_invoice}
    return render(request, "invoice/create.html", context)


@login_required
def v_invoice_update(request, pk):
    invoice = get_object_or_404(Invoices, id=pk)
    f_invoice = InvoicesModelForm(instance=invoice)

    if request.method == "POST":
        f_invoice = InvoicesModelForm(request.POST, instance=invoice)
        if f_invoice.is_valid():
            invoice = f_invoice.save()
            return redirect("invoices:invoice_list")
        else:
            for field, err in f_invoice.errors.items():
                messages.warning(
                    request, str(field).replace("_", " ") + " : " + str(err[0])
                )

    context = {"vendors": Company.objects.all(), "invoice": invoice, "form": f_invoice}
    return render(request, "invoice/update.html", context)


@login_required
def v_invoice_item_create(request, fk, pk):
    supplier = Company.objects.get(provider=True)
    invoice = get_object_or_404(Invoices, id=fk)
    context = {
        "invoice": invoice,
        "inventory": Inventory.objects.all(),
    }
    if invoice.buyer.state == supplier.state:
        context.update({"igst_flag": False})
    else:
        context.update({"igst_flag": True})
    form = InvoiceItemsModelForm()
    context.update({"form": form})

    # Update
    if pk != 0:
        invoice_item = get_object_or_404(InvoiceItems, id=pk)
        context.update({"invoice_item": invoice_item})

    # Create & Update
    if request.method == "POST":
        if pk != 0:
            f_invoice_item = InvoiceItemsModelForm(request.POST, instance=invoice_item)
        else:
            f_invoice_item = InvoiceItemsModelForm(request.POST)
        if f_invoice_item.is_valid():
            invoice_item = f_invoice_item.save()
            messages.success(request, "Saved Successfully")
            return redirect("invoices:invoice_update", pk=fk)
        else:
            for field, err in f_invoice_item.errors.items():
                messages.warning(
                    request, str(field).replace("_", " ") + " : " + str(err[0])
                )

    return render(request, "items/create.html", context)


@login_required
def v_invoice_receipt(request, pk):
    invoice = get_object_or_404(Invoices, id=pk)
    invoice_items = InvoiceItems.objects.filter(invoice_id=pk)
    supplier = Company.objects.get(provider=True)
    context = {"invoice": invoice, "invoice_items": invoice_items, "supplier": supplier}
    return render(request, "invoice/receipt.html", context)


@login_required
def v_invoice_pdf(request, pk):
    invoice = get_object_or_404(Invoices, id=pk)
    invoice_items = InvoiceItems.objects.filter(invoice_id=pk)
    supplier = Company.objects.get(provider=True)
    context = {"invoice": invoice, "invoice_items": invoice_items, "supplier": supplier}
    status, response = render_file_else_response(
        "invoice/receipt_copy.html", context, output_as_file=False
    )
    if status:
        return response


@login_required
def v_invoice_item_delete(request, pk):
    try:
        invoice = get_object_or_404(InvoiceItems, id=pk)
        invoice.delete()
        return JsonResponse(True, safe=False)
    except Exception as err:
        print(err)
    return JsonResponse("Item cannot be deleted", safe=False)


class invoiceItemsData(generics.ListAPIView):
    api_view = ["GET"]
    permission_classes = [IsAuthenticated]
    queryset = InvoiceItems.objects.all()
    serializer_class = InvoiceItemsSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ["id", "invoice_id", "inventory_id", "deleted"]
    search_fields = "__all__"
    ordering_fields = "__all__"


class invoiceData(generics.ListAPIView):
    api_view = ["GET"]
    permission_classes = [IsAuthenticated]
    queryset = Invoices.objects.all()
    serializer_class = InvoiceSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ["id", "invoice_no", "buyer", "inserted_On", "deleted"]
    search_fields = "__all__"
    ordering_fields = "__all__"
