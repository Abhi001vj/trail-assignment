from django.core.validators import FileExtensionValidator
from django.db import models
from django_extensions.db.models import TimeStampedModel
from user.models import User
import csv


class Sale(TimeStampedModel):
    user = models.ForeignKey(User, related_name="sales", on_delete=models.CASCADE)
    sale_file = models.FileField(
        upload_to="sales/",
        validators=[FileExtensionValidator(allowed_extensions=["csv"])],
    )

    def get_sale_file_path(self):
        return self.sale_file.path

    def add_sales_data(self):
        with open(self.get_sale_file_path(), "r") as file:
            file_data = csv.DictReader(file)
            header = file_data.fieldnames

            for row in file_data:
                product = row["Product"]
                price = row["Price"]
                SalesData.objects.create(sale=self, product=product, price=float(price))


class SalesData(TimeStampedModel):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name="sales_data")
    product = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product} - {self.price}"
