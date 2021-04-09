from django.db import transaction
from rest_framework import serializers
from .models import Sale, SalesData
import csv


class SalesDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesData
        fields = ["id", "product", "price", "sale", "created"]
        extra_kwargs = {
            "id": {"read_only": True},
        }


class SaleSerializer(serializers.ModelSerializer):
    sales_data = SalesDataSerializer(many=True, required=False)

    class Meta:
        model = Sale
        fields = ["id", "user", "sale_file", "created", "sales_data"]
        extra_kwargs = {
            "id": {"read_only": True},
            "user": {"required": False},
        }

    def validate(self, attrs):
        if "user" not in attrs:
            attrs["user"] = self.context["request"].user

        return super(SaleSerializer, self).validate(attrs)

    def create(self, validated_data):
        validated_data.pop("sales_data", [])
        with transaction.atomic():
            sale = super(SaleSerializer, self).create(validated_data)
            sale.add_sales_data()

        sale.refresh_from_db()
        return sale

    def update(self, instance, validated_data):
        validated_data.pop("sales_data", [])
        with transaction.atomic():
            instance = super(SaleSerializer, self).update(instance, validated_data)
            sales_data = instance.sales_data.all()
            sales_data.delete()
            instance.add_sales_data()

        instance.refresh_from_db()
        return instance
