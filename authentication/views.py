"""
Views for authentication app.
"""
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from django.contrib.auth import authenticate, logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
import logging

from .models import User
from .serializers import (
    UserSerializer,
    RegisterSerializer,
    AdminCreateUserSerializer,
    LoginSerializer,
    ChangePasswordSerializer,
    UpdateProfileSerializer
)
from core.permissions import IsAdminUser

logger = logging.getLogger(__name__)


class RegisterView(generics.CreateAPIView):
    """View for user registration (borrowers only)."""
    
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    
    def perform_create(self, serializer):
        """Override to ensure role is set to borrower."""
        user = serializer.save()
        logger.info(f"New user registered: {user.email}")
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = {
            'status': 'success',
            'message': 'User registered successfully. Please login.',
            'data': response.data
        }
        return response


@method_decorator(csrf_protect, name='dispatch')
class LoginView(APIView):
    """View for user login and JWT token generation."""
    
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            
            logger.info(f"User logged in: {user.email} (Role: {user.role})")
            
            return Response({
                'status': 'success',
                'message': 'Login successful',
                'data': {
                    'user': UserSerializer(user).data,
                    'tokens': {
                        'access': str(refresh.access_token),
                        'refresh': str(refresh),
                    }
                }
            }, status=status.HTTP_200_OK)
        
        return Response({
            'status': 'error',
            'message': 'Invalid credentials',
            'errors': serializer.errors
        }, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    """View for user logout (blacklist refresh token)."""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            logger.info(f"User logged out: {request.user.email}")
            
            return Response({
                'status': 'success',
                'message': 'Logout successful'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Logout error: {e}")
            return Response({
                'status': 'error',
                'message': 'Invalid token'
            }, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(generics.RetrieveUpdateAPIView):
    """View for user profile."""
    
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class ChangePasswordView(generics.UpdateAPIView):
    """View for changing user password."""
    
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            # Check old password
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({
                    'status': 'error',
                    'message': 'Old password is incorrect'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Set new password
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            logger.info(f"Password changed for user: {user.email}")
            
            return Response({
                'status': 'success',
                'message': 'Password changed successfully'
            })
        
        return Response({
            'status': 'error',
            'message': 'Validation error',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class UpdateProfileView(generics.UpdateAPIView):
    """View for updating user profile."""
    
    serializer_class = UpdateProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            
            logger.info(f"Profile updated for user: {user.email}")
            
            return Response({
                'status': 'success',
                'message': 'Profile updated successfully',
                'data': UserSerializer(user).data
            })
        
        return Response({
            'status': 'error',
            'message': 'Validation error',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


# Admin-specific views
class AdminCreateUserView(generics.CreateAPIView):
    """View for admin to create users (admin or borrower)."""
    
    serializer_class = AdminCreateUserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = {
            'status': 'success',
            'message': 'User created successfully',
            'data': response.data
        }
        return response


class AdminUserListView(generics.ListAPIView):
    """View for admin to list all users."""
    
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    
    def get_queryset(self):
        return User.objects.all().order_by('-date_joined')


class AdminUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View for admin to manage specific users."""
    
    serializer_class = AdminCreateUserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    lookup_field = 'uuid'
    
    def get_queryset(self):
        return User.objects.all()
    
    def perform_update(self, serializer):
        user = serializer.save()
        logger.info(f"Admin updated user: {user.email}")
    
    def perform_destroy(self, instance):
        email = instance.email
        instance.delete()
        logger.info(f"Admin deleted user: {email}")


# JWT Token Refresh View (custom to add status)
class CustomTokenRefreshView(TokenRefreshView):
    """Custom token refresh view with consistent response format."""
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            response.data = {
                'status': 'success',
                'message': 'Token refreshed successfully',
                'data': response.data
            }
        else:
            response.data = {
                'status': 'error',
                'message': 'Token refresh failed',
                'errors': response.data
            }
        
        return response