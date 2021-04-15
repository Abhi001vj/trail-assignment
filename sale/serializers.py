from django.db import transaction
from rest_framework import serializers
from .models import SalesData
import csv


class SalesDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesData
        fields = ["id", "product", "revenue", "sales_number", "date", "user_id"]
        extra_kwargs = {
            "id": {"read_only": True},
        }

