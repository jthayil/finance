from rest_framework import serializers
from masters.models import Pincodes, Company, Inventory


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = "__all__"


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pincodes
        fields = "__all__"
