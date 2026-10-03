from django.urls import path

from sales import views

# Define namespace which is required for the template
app_name = "sales"

urlpatterns = [
    # Load page /sales/
    path("", views.sales_view, name="sales"),
    # Load graphics
    path("data/", views.SalesAjaxView.as_view(), name="sales-data"),
]
