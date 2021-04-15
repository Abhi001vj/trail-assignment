
from django.db import models
from django_extensions.db.models import TimeStampedModel
from user.models import User
import csv
from datetime import date


class SalesData(TimeStampedModel):
    product = models.CharField(max_length=30)
    revenue = models.DecimalField(max_digits=10, decimal_places=2)
    sales_number = models.IntegerField(default=0)
    user_id =  models.IntegerField(default=0)# models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=date.today) 

    def __str__(self):
        return f"{self.product} - {self.revenue}"
