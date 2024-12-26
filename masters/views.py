import csv
import os
import threading

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter, SearchFilter

from fms.support import remove_office
from masters.models import HSN, Pincodes, Company, Inventory, Pincodes
from masters.serializers import CitySerializer, InventorySerializer
from masters.forms import (
    CompanyModelForm,
    HSNModelForm,
    InventoryModelForm,
    UserEditModelForm,
    UserModelForm,
)


@login_required
def v_inventory_list(request):
    inventories = Inventory.objects.all()
    return render(request, "masters/inventory/list.html", {"inventories": inventories})


@login_required
def v_inventory_create(request):
    context = {"hsn": HSN.objects.all()}
    if request.method == "POST":
        form = InventoryModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Inventory Added Successfully")
            return redirect("masters:inventory_list")
        else:
            print(form.errors)
            for field, err in form.errors.items():
                messages.warning(
                    request, request, str(field).replace("_", " ") + " : " + str(err[0])
                )
    return render(request, "masters/inventory/create.html", context)


@login_required
def v_inventory_import(request):
    status, message, data = False, "Import Failed", {}
    csv_file = request.FILES["csv_file"]
    if csv_file:
        decoded_file = csv_file.read().decode("utf-8").splitlines()
        reader = csv.DictReader(decoded_file)
        errors = []
        for row in reader:
            try:
                form = InventoryModelForm(
                    {
                        "name": row["Name"],
                        "description": row["Description"],
                        "min_stock": row["Min Stock"],
                        "sgst": row["SGST"],
                        "cgst": row["CGST"],
                        "igst": row["IGST"],
                        "rate": row["Rate"],
                        "qty": row["Qty"],
                    }
                )

                if form.is_valid():
                    obj, created = Inventory.objects.update_or_create(
                        name=form.cleaned_data["name"],
                        defaults={
                            "name": form.cleaned_data["name"],
                            "description": form.cleaned_data["description"],
                            "min_stock": form.cleaned_data["min_stock"],
                            "sgst": form.cleaned_data["sgst"],
                            "cgst": form.cleaned_data["cgst"],
                            "igst": form.cleaned_data["igst"],
                            "rate": form.cleaned_data["rate"],
                            "qty": form.cleaned_data["qty"],
                        },
                    )
                else:
                    messages.error(request, form.errors)

            except Exception as err:
                messages.error(request, f"Error importing row: {err}")

        if not errors:
            messages.success(request, "Import Successful")
        else:
            messages.warning(request, "Import Partially Successful")
    else:
        messages.error(request, "No CSV file provided")
    return redirect("masters:inventory_list")


@login_required
def v_inventory_template(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="inventories.csv"'
    writer = csv.writer(response)
    latest_records = Inventory.objects.all().order_by("qty", "min_stock")
    writer.writerow(
        ["Name", "Description", "Rate", "SGST", "CGST", "IGST", "Min Stock", "Qty"]
    )
    for record in latest_records:
        writer.writerow(
            [
                record.name,
                record.description,
                record.rate,
                record.sgst,
                record.cgst,
                record.igst,
                record.min_stock,
                "",
            ]
        )
    return response


@login_required
def v_inventory_edit(request, pk):
    inventory = get_object_or_404(Inventory, id=pk)
    if request.method == "POST":
        form = InventoryModelForm(request.POST, instance=inventory)
        if form.is_valid():
            form.save()
            messages.success(request, "Inventory Updated Successfully")
            return redirect("masters:inventory_list")
    context = {"item": inventory, "hsn": HSN.objects.all()}
    return render(request, "masters/inventory/edit.html", context)


class inventoryData(generics.ListAPIView):
    api_view = ["GET"]
    permission_classes = [IsAuthenticated]
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = [
        "id",
        "name",
        "rate",
        "qty",
        "min_stock",
        "sgst",
        "cgst",
        "igst",
    ]
    search_fields = "__all__"
    ordering_fields = "__all__"


@login_required
def v_user_list(request):
    users = User.objects.all()
    context = {"users": users}
    return render(request, "masters/user/list.html", context)


@login_required
def v_user_create(request):
    context = {}
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        form2 = UserModelForm(request.POST)
        if form.is_valid() and form2.is_valid():
            user = form.save()
            user.email = form2.cleaned_data["email"]
            user.first_name = form2.cleaned_data["first_name"]
            user.last_name = form2.cleaned_data["last_name"]
            user.is_superuser = form2.cleaned_data["is_superuser"]
            user.is_active = form2.cleaned_data["is_active"]
            user.save()
            messages.success(request, "User Added Successfully")
            return redirect("masters:user_list")
        else:
            print(form.errors)
            for field, err in form.errors.items():
                messages.warning(
                    request, str(field).replace("_", " ") + " : " + str(err[0])
                )
    return render(request, "masters/user/create.html", context)


@login_required
def v_user_edit(request, pk):
    user = get_object_or_404(User, id=pk)
    if request.method == "POST":
        form = UserEditModelForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "User Updated Successfully")
            return redirect("masters:user_list")
    context = {"user": user}
    return render(request, "masters/user/edit.html", context)


@login_required
def v_company_list(request):
    company = Company.objects.all()
    context = {"companies": company}
    return render(request, "masters/company/list.html", context)


@login_required
def v_company_create(request):
    if request.method == "POST":
        form = CompanyModelForm(request.POST)
        if form.is_valid():
            o_pincode = Pincodes.objects.filter(pincode=request.POST["pincode"]).first()
            o_company = form.save()
            o_company.pincode = o_pincode
            o_company.save()
            messages.success(request, "Company Added Successfully")
            return redirect("masters:company_list")
        else:
            print(form.errors)
            for field, err in form.errors.items():
                messages.warning(
                    request, request, str(field).replace("_", " ") + " : " + str(err[0])
                )
    return render(request, "masters/company/create.html", {})


@login_required
def v_company_edit(request, pk):
    company = get_object_or_404(Company, id=pk)
    if request.method == "POST":
        form = CompanyModelForm(request.POST, instance=company)
        if form.is_valid():
            o_pincode = Pincodes.objects.filter(pincode=request.POST["pincode"]).first()
            o_company = form.save()
            o_company.pincode = o_pincode
            o_company.save()
            messages.success(request, "Company Updated Successfully")
            return redirect("masters:company_list")
    context = {"company": company}
    return render(request, "masters/company/edit.html", context)


@login_required
def import_pincodes():
    unique_pincodes = {}
    pincode_objs = []
    pincode_filepath = os.path.join(settings.BASE_DIR, "static", "pincode.csv")
    if os.path.exists(pincode_filepath):
        with open(pincode_filepath, mode="r", newline="") as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                pincode_city = remove_office(row["OfficeName"])
                if row["StateName"] not in unique_pincodes.keys():
                    unique_pincodes[row["StateName"]] = {row["Pincode"]: [pincode_city]}
                else:
                    if row["Pincode"] not in unique_pincodes[row["StateName"]].keys():
                        unique_pincodes[row["StateName"]].update(
                            {row["Pincode"]: [pincode_city]}
                        )
                    else:
                        if (
                            pincode_city
                            not in unique_pincodes[row["StateName"]][row["Pincode"]]
                        ):
                            unique_pincodes[row["StateName"]][row["Pincode"]].append(
                                pincode_city
                            )

    if len(unique_pincodes) > 0:
        for states, pincodes in unique_pincodes.items():
            for pincode, districts in pincodes.items():
                for district in districts:
                    pincode_objs.append(
                        Pincodes(
                            state=states.strip().title(),
                            pincode=pincode,
                            city=district,
                            country="India",
                        )
                    )

    if len(pincode_objs) > 0:
        Pincodes.objects.bulk_create(pincode_objs, batch_size=1000)


@login_required
def v_pincode_list(request):
    return render(request, "masters/pincode/list.html", {})


@login_required
def v_pincode_create(request):
    t = threading.Thread(target=import_pincodes)
    t.start()
    messages.info(request, "Import Started")
    return redirect("masters:pincode_list")


@method_decorator(cache_page(60 * 15), name="dispatch")
class pincodeData(generics.ListAPIView):
    api_view = ["GET"]
    permission_classes = [IsAuthenticated]
    queryset = Pincodes.objects.all()
    serializer_class = CitySerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = [
        "id",
        "pincode",
        "city",
        "state",
        "country",
    ]
    search_fields = "__all__"
    ordering_fields = "__all__"


@login_required
def v_hsn_list(request):
    hsn_codes = HSN.objects.all()
    context = {"hsn": hsn_codes}
    return render(request, "masters/hsn/list.html", context)


@login_required
def v_hsn_create(request):
    if request.method == "POST":
        form = HSNModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Company Added Successfully")
            return redirect("masters:hsn_list")
        else:
            print(form.errors)
            for field, err in form.errors.items():
                messages.warning(
                    request, request, str(field).replace("_", " ") + " : " + str(err[0])
                )
    return render(request, "masters/hsn/create.html", {})


@login_required
def v_hsn_edit(request, pk):
    hsn = get_object_or_404(HSN, id=pk)
    if request.method == "POST":
        form = HSNModelForm(request.POST, instance=hsn)
        if form.is_valid():
            form.save()
            messages.success(request, "HSN Updated Successfully")
            return redirect("masters:hsn_list")
    context = {"hsn": hsn}
    return render(request, "masters/hsn/edit.html", context)
