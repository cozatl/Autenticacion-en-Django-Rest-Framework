from rest_framework import permissions, viewsets

from .models import Order
from .serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows orders to be viewed, created, updated, or deleted.
    """

    queryset = Order.objects.all().order_by("-created_at")
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        queryset = Order.objects.all().order_by("-created_at")
        if self.request.user.is_authenticated:
            return queryset.filter(cart__user=self.request.user)
        return queryset.none()
