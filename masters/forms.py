from django.forms import ModelForm
from django.contrib.auth.models import User

from masters.models import HSN, Company, Inventory


class UserModelForm(ModelForm):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "is_superuser",
            "is_active",
        ]


class UserEditModelForm(ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]


class CompanyModelForm(ModelForm):
    class Meta:
        model = Company
        fields = ["name", "address", "gstin", "mobile", "email", "pan", "state", "bank", "bank_account_holder", "bank_no", "bank_ifsc", "bank_branch", "provider"]


class HSNModelForm(ModelForm):
    class Meta:
        model = HSN
        fields = ["hsn_code", "description"]


class InventoryModelForm(ModelForm):
    class Meta:
        model = Inventory
        fields = "__all__"
