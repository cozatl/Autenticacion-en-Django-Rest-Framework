from django.urls import path

from sales import views

# Define namespace which is required for the template
app_name = "sales"

urlpatterns = [
    path("", views.sales_view, name="sales_list"),
    path(
        "agregar/<int:product_id>/",
        views.add_to_cart,
        name="add_to_cart",
    ),
    path("procesar/", views.process_order, name="process_order"),
]
