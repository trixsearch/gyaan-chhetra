"""
Custom permission classes for role-based access control.
"""
from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """
    Permission check for admin users.
    """
    
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            request.user.role == 'admin'
        )


class IsBorrowerUser(permissions.BasePermission):
    """
    Permission check for borrower users.
    """
    
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            request.user.role == 'borrower'
        )


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Permission check for object ownership or admin access.
    """
    
    def has_object_permission(self, request, view, obj):
        # Admin can access anything
        if request.user.role == 'admin':
            return True
        
        # Users can only access their own objects
        return obj.user == request.user


class AdminOrReadOnly(permissions.BasePermission):
    """
    Allow read-only for all, but write only for admin.
    """
    
    def has_permission(self, request, view):
        # Allow GET, HEAD, OPTIONS for all authenticated users
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        # Write permissions only for admin
        return bool(
            request.user and 
            request.user.is_authenticated and 
            request.user.role == 'admin'
        )