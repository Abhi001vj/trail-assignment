from django.db.models import Sum


def get_count_and_total_price(sales):
    sum_ = 0
    sales = sales.filter(sales_data__isnull=False)
    for sale in sales.annotate(sum=Sum("sales_data")):
        sum_ = sum_ + sale.sum

    return sales.count(), sum_


def get_maximum_revenue_sale(sales):
    sales = sales.annotate(sum=Sum("sales_data")).order_by('-sum')

    return sales.first()
