from django.db.models import Sum
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from sale.models import SalesData
from sale.serializers import SalesDataSerializer
from sale.utils import get_count_and_total_price, get_maximum_revenue_sale
from django.db.models import Sum, Count

class SaleStatisticsView(ModelViewSet):
    permission_classes = [IsAuthenticated]

    permission_classes = [IsAuthenticated]
    serializer_class = SalesDataSerializer
    queryset = SalesData.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user_id=self.request.user.id)

    def create(self, request):
        sales_data = self.request.data.get("sales_data", [])
        # user_id = 
        objs = []
        for row in sales_data:
            product = row["product"]
            date = row["date"]
            sales_number = row["sales_number"]
            revenue = row["revenue"]
            user_id = row['user_id']
            objs.append(SalesData(user_id=user_id, date=date,sales_number=sales_number, product=product, revenue=float(revenue)))

        queryset = SalesData.objects.bulk_create(objs)
        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data)

    def get_stats(self, request, *args, **kwargs):
        all_sales = SalesData.objects.all()
        agg_results = all_sales.aggregate(total=Sum("revenue"))#get_count_and_total_price(all_sales)
        average_sales_all_user = agg_results['total'] / all_sales.count()

        sales = all_sales.filter(user_id=request.user.id)
        agg_results = sales.aggregate(total=Sum("revenue"))#get_count_and_total_price(sales)
        average_sales = agg_results['total'] /sales.count()

        highest_revenue_sale =  sales.order_by('-revenue').first() #get_maximum_revenue_sale(sales)

        product_highest_revenue = sales.values("product").annotate(total_revenue=Sum("revenue")).order_by("-total_revenue").first()
        product_highest_sales_number = sales.values("product").annotate(total_sales_number=Sum("sales_number")).order_by("-total_sales_number").first()

        data = {
            "average_sales_for_current_user": average_sales,
            "average_sale_all_user": average_sales_all_user,
            "highest_revenue_sale_for_current_user": {
                "sale_id": highest_revenue_sale.id,
                "revenue": highest_revenue_sale.revenue,
            },
            "product_highest_revenue_for_current_user": {
                'product_name': product_highest_revenue['product'],
                'price': product_highest_revenue['total_revenue']
            },
            "product_highest_sales_number_for_current_user":{
                'product_name': product_highest_sales_number['product'],
                'price': product_highest_sales_number['total_sales_number']

            }
        }

        return Response(data=data)
