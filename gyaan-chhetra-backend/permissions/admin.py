from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == "ADMIN"
        )

# from .base import IsRole
# from accounts.constants import UserRole

# class IsAdmin(IsRole):
#     allowed_roles=[UserRole.ADMIN]