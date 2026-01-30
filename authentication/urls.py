"""
URL configuration for authentication app.
"""
from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView
from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    ProfileView,
    ChangePasswordView,
    UpdateProfileView,
    AdminCreateUserView,
    AdminUserListView,
    AdminUserDetailView,
    CustomTokenRefreshView
)

urlpatterns = [
    # Public endpoints
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    
    # User endpoints (authenticated)
    path('profile/', ProfileView.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('update-profile/', UpdateProfileView.as_view(), name='update-profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # Token endpoints
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # Admin endpoints
    path('admin/users/create/', AdminCreateUserView.as_view(), name='admin-create-user'),
    path('admin/users/', AdminUserListView.as_view(), name='admin-user-list'),
    path('admin/users/<uuid:uuid>/', AdminUserDetailView.as_view(), name='admin-user-detail'),
]