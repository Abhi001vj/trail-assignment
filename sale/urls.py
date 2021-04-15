from django.urls import path
from rest_framework.routers import DefaultRouter

from sale.views import SaleStatisticsView

router = DefaultRouter(trailing_slash=False)
# router.register("sales", SaleViewSet, basename="sales")

urlpatterns = router.urls


urlpatterns += [
    path(
        "sales/",
        SaleStatisticsView.as_view({"post": "create"}),
        name="sales",
    ),
    path(
        "sale_statistics/",
        SaleStatisticsView.as_view({"get": "get_stats"}),
        name="sale_statistics",
    )
]
