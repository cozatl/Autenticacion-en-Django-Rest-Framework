from django.conf import settings
from django.db import models

from product.models import Product


class Cart(models.Model):
    # user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    products = models.ManyToManyField(Product, blank=True)

    def __str__(self):
        return f"Cart #{self.id}"
