from rest_framework import serializers
from django.contrib.auth import authenticate

from .models import User
from .constants import UserRole


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=UserRole.CHOICES)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        role = data.get("role")

        user = authenticate(email=email, password=password)

        if not user:
            raise serializers.ValidationError("Invalid email or password")

        if not user.is_active:
            raise serializers.ValidationError("User account is disabled")

        if user.role != role:
            raise serializers.ValidationError("Invalid role for this account")

        data["user"] = user
        return data
