import uuid

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.text import slugify


class Product(models.Model):
    # Basic product information
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()

    # Pricing and stock information
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )

    def generate_sku():
        return str(uuid.uuid4())

    # Additional product details
    sku = models.CharField(max_length=50, unique=True, default=generate_sku)
    stock = models.PositiveIntegerField(default=0)
    weight = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        help_text="Weight in kg",
        null=True,
        blank=True,
    )

    # Multimedia
    image = models.ImageField(upload_to="products/", null=True, blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return f"/products/{self.slug}/"

    def clean(self):
        super().clean()
        if (
            self.discount_price is not None
            and self.price is not None
            and self.discount_price >= self.price
        ):
            raise ValidationError(
                "The discount price must be less than the regular price."
            )

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while (
                Product.objects.filter(slug=slug).exclude(pk=self.pk).exists()
            ):
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    class Meta:
        ordering = ("-created_at",)
        indexes = (models.Index(fields=("is_active", "-created_at")),)
        constraints = (
            models.CheckConstraint(
                condition=models.Q(price__gte=0),
                name="price_non_negative",
            ),
            models.CheckConstraint(
                condition=(
                    models.Q(discount_price__lt=models.F("price"))
                    | models.Q(discount_price__isnull=True)
                ),
                name="discount_price_less_than_price",
                violation_error_message=(
                    "The discount price must be less than the regular price."
                ),
            ),
        )

    def __str__(self):
        return f"{self.name} - ${self.price}"
