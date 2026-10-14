from rest_framework import permissions, viewsets

from .models import Cart
from .serializers import CartSerializer


class CartViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows shopping carts to be viewed, created,
    updated, or deleted.
    """

    queryset = Cart.objects.all().order_by("-id")
    serializer_class = CartSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        queryset = Cart.objects.all().order_by("-id")
        if self.request.user.is_authenticated:
            return queryset.filter(user=self.request.user)
        return queryset.none()
