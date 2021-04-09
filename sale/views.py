from django.db.models import Sum
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from sale.models import Sale, SalesData
from sale.serializers import SaleSerializer
from sale.utils import get_count_and_total_price, get_maximum_revenue_sale


class SaleViewSet(ModelViewSet):
    """
    #sales endpoint#

    **POST: /api/v1/sales**

        {
            "sale_file": CSV FILE
        }

    **Response**

        {
            "id": 1,
            "user": 1,
            "sale_file": "http://127.0.0.1:8000/media/sales/Trial_Assignment_Products_List_M7bQkoR.csv",
            "created": "2021-04-09T08:32:32.960012Z",
            "sales_data":[
                {
                    "id": 31,
                    "product": "Paper",
                    "price": "5.00",
                    "sale": 1,
                    "created": "2021-04-09T08:37:47.033630Z"
                },
            ]
        }

    **GET (Retrieve): /api/v1/sales/1**

        {
            "id": 1,
            "user": 1,
            "sale_file": "http://127.0.0.1:8000/media/sales/Trial_Assignment_Products_List_M7bQkoR.csv",
            "created": "2021-04-09T08:32:32.960012Z",
            "sales_data":[
                {
                    "id": 31,
                    "product": "Paper",
                    "price": "5.00",
                    "sale": 1,
                    "created": "2021-04-09T08:37:47.033630Z"
                },
            ]
        }

    **GET (List): /api/v1/sales**

        [
            {
                "id": 1,
                "user": 1,
                "sale_file": "http://127.0.0.1:8000/media/sales/Trial_Assignment_Products_List_M7bQkoR.csv",
                "created": "2021-04-09T08:32:32.960012Z",
                "sales_data":[
                    {
                        "id": 31,
                        "product": "Paper",
                        "price": "5.00",
                        "sale": 1,
                        "created": "2021-04-09T08:37:47.033630Z"
                    },
                ]
            }
        ]

    **PUT (Update fields): /api/v1/sales/1**

        {
            "sale_file": CSV FILE
        }

    ## Fields Legend: ##

        * sale_file - string - url of the sale file
        * created - DateTime
        * sales_data - Array of Object
            * product - string
            * price - Decimal
            * sale - PK of the Sale
            * created - DateTime

    """

    permission_classes = [IsAuthenticated]
    serializer_class = SaleSerializer
    queryset = Sale.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class SaleStatisticsView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        all_sales = Sale.objects.all()
        count, total = get_count_and_total_price(all_sales)
        average_sales_all_user = total / count

        sales = all_sales.filter(user=request.user)
        count, total = get_count_and_total_price(sales)
        average_sales = total / count

        highest_revenue_sale = get_maximum_revenue_sale(sales)

        product_highest_revenue = SalesData.objects.all().order_by('-price').first()

        data = {
            "average_sale": average_sales,
            "average_sale_all_user": average_sales_all_user,
            "highest_revenue_sale": {
                "sale_id": highest_revenue_sale.id,
                "amount": highest_revenue_sale.sum,
            },
            "product_highest_revenue": {
                'product_name': product_highest_revenue.product,
                'sale': product_highest_revenue.sale.id,
                'price': product_highest_revenue.price
            }
        }

        return Response(data=data)
