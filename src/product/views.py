from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView
from rest_framework import permissions, viewsets

from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be viewed, created, updated,
    or deleted.
    """

    queryset = Product.objects.all().order_by("-id")
    serializer_class = ProductSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class HomeProductCatalogView(ListView):
    model = Product
    template_name = "product/home_catalog.html"
    context_object_name = "products"

    def get_queryset(self):
        # Base query sorted by ID Descendent (most recent first)
        queryset = Product.objects.all().order_by("-id")

        # If user hasn't logged in, only show a preview of some records
        if not self.request.user.is_authenticated:
            return queryset[:8]

        # If user has logged in, show complete catalog
        return queryset


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "product/product_detail.html"
    context_object_name = "product"

    # Specify product search on URL will be by slug
    slug_field = "slug"
    slug_url_kwarg = "slug"
