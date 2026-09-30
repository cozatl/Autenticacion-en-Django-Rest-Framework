from datetime import timedelta

from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import View

# from .models import Order, OrderItem, Product
from order_manager.models import Order


# class SalesAjaxView(View):
#     def get(self, request, *args, **kwargs):
#         data = {}
#         if request.user.is_staff:
#             qs = Order.objects.all().by_weeks_range(
#                 weeks_ago=5, number_of_weeks=5
#             )
#             if request.GET.get("type") == "week":
#                 days = 7
#                 start_date = timezone.now().today() - timedelta(
#                     days=days - 1
#                 )
#                 datetime_list = []
#                 labels = []
#                 sales_items = []
#                 for x in range(days):
#                     new_time = start_date + timedelta(days=x)
#                     datetime_list.append(new_time)
#                     labels.append(new_time.strftime("%a"))
#                     new_qs = qs.filter(
#                         created_at__day=new_time.day,
#                         created_at__month=new_time.month,
#                     )
#                     day_total = new_qs.totals_data()["total__sum"] or 0
#                     sales_items.append(day_total)
#                 data["labels"] = labels
#                 data["data"] = sales_items
#         return JsonResponse(data)
class SalesAjaxView(View):
    def get(self, request, *args, **kwargs):
        data = {}
        if request.user.is_staff:
            qs = Order.objects.by_weeks_range(weeks_ago=5, number_of_weeks=5)
            if request.GET.get("type") == "week":
                days = 7
                start_date = timezone.localdate() - timedelta(days=days - 1)
                labels, sales_items = [], []
                for x in range(days):
                    day = start_date + timedelta(days=x)
                    labels.append(day.strftime("%a"))
                    day_total = (
                        qs.filter(created_at__date=day).totals_data()[
                            "total__sum"
                        ]
                        or 0
                    )
                    sales_items.append(float(day_total))
                data["labels"] = labels
                data["data"] = sales_items
        return JsonResponse(data)


def sales_view(request):
    return render(request, "sales/sales.html")
