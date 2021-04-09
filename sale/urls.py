from django.urls import path
from rest_framework.routers import DefaultRouter

from sale.views import SaleViewSet, SaleStatisticsView

router = DefaultRouter(trailing_slash=False)
router.register("sales", SaleViewSet, basename="sales")

urlpatterns = router.urls


urlpatterns += [
    path("sale_statistics", SaleStatisticsView.as_view(), name="sale_statistics")
]
