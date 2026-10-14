from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    # password is write-only for security reasons so it's never
    # exposed in responses
    password = serializers.CharField(
        write_only=True,
        required=False,
        style={"input_type": "password"},
    )

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "full_name",
            "password",
            "is_active",
            "staff",
            "admin",
        )
        read_only_fields = ("id", "timestamp")

    def create(self, validated_data):
        # Uses custom manager to hash password automatically
        password = validated_data.pop("password", None)
        is_staff = validated_data.pop("staff", False)
        is_admin = validated_data.pop("admin", False)
        user = User.objects.create_user(
            **validated_data,
            password=password,
            is_staff=is_staff,
            is_admin=is_admin,
        )
        return user

    def update(self, instance, validated_data):
        # Extracts password if it was provided in the update payload
        # (PUT/PATCH)
        password = validated_data.pop("password", None)
        instance.email = validated_data.get("email", instance.email)
        instance.full_name = validated_data.get(
            "full_name", instance.full_name
        )
        instance.is_active = validated_data.get(
            "is_active", instance.is_active
        )

        # Updates regular fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Properly hashes and updates the password only if a new one was passed
        if password:
            instance.set_password(password)

        # Updates the staff status if provided
        if "staff" in validated_data:
            instance.staff = validated_data.get("staff")

        # Updates the admin status if provided
        if "admin" in validated_data:
            instance.admin = validated_data.get("admin")

        instance.save()
        return instance
