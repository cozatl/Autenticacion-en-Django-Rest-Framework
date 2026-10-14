from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from product.models import Product


class ProductModelTest(TestCase):
    """Unit test for Product model"""

    @classmethod
    def setUpTestData(cls):

        # Create a product instance for testing
        cls.product = Product.objects.create(
            name="Smartphone XYZ",
            description="Un teléfono inteligente de última generación",
            price=Decimal("299.99"),
            stock=50,
            is_active=True,
        )

    def test_product_creation(self):
        """Validate if product is created correctly and its
        attributes are saved."""
        product = self.product
        self.assertEqual(product.name, "Smartphone XYZ")
        self.assertEqual(product.price, Decimal("299.99"))
        self.assertEqual(product.stock, 50)
        # self.assertEqual(product.category.name, "Electrónica")
        self.assertTrue(product.is_active)

    def test_product_string_representation(self):
        """Validate the string representation of the product"""
        self.assertEqual(str(self.product), "Smartphone XYZ - $299.99")

    def test_product_price_positive(self):
        """Validate that the product price is not negative.

        This is a logical validation check.
        """
        product_invalid = Product(
            name="Producto Defectuoso",
            price=Decimal("-10.00"),
            stock=10,
            # category=self.category
        )
        # If using Django's model validation, you can call
        # full_clean() to trigger validation checks:
        with self.assertRaises((ValidationError, Exception)):
            product_invalid.full_clean()
            product_invalid.save()
