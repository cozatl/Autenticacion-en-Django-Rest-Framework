from django.urls import path

from product.views import (
    HomeProductCatalogView,
    ProductDetailView,
)

# Define namespace which is required for the template
app_name = "products"

urlpatterns = [
    path("", HomeProductCatalogView.as_view(), name="home"),
    path(
        "products/<slug:slug>/",
        ProductDetailView.as_view(),
        name="product-detail",
    ),
]
