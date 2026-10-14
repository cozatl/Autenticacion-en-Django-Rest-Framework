from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ("slug",)

    def validate(self, attrs):
        price = attrs.get(
            "price",
            getattr(self.instance, "price", None),
        )
        discount = attrs.get(
            "discount_price",
            getattr(self.instance, "discount_price", None),
        )

        if discount is not None and price is not None and discount >= price:
            raise serializers.ValidationError(
                {
                    "discount_price": (
                        "The discount price must be less than "
                        "the regular price."
                    )
                }
            )
        return attrs
