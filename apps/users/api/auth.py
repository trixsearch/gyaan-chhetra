from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth import get_user_model

User = get_user_model()

class RoleBasedTokenObtainPairView(TokenObtainPairView):
    """JWT with role-based claims"""
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            user = User.objects.get(username=request.data['username'])
            
            # Add custom claims
            refresh = RefreshToken.for_user(user)
            refresh['role'] = user.role
            refresh['permissions'] = self._get_user_permissions(user)
            
            response.data['refresh'] = str(refresh)
            response.data['access'] = str(refresh.access_token)
            
        return response
    
    def _get_user_permissions(self, user):
        """Get role-based permissions"""
        permissions = {
            'STUDENT': ['view_book', 'borrow_book', 'view_borrow_records'],
            'TEACHER': ['view_book', 'borrow_book', 'manage_students', 'manage_borrows'],
            'PRINCIPAL': ['full_access'],
        }
        return permissions.get(user.role, [])

class CustomPermission(permissions.BasePermission):
    """Role-based permission class"""
    
    def has_permission(self, request, view):
        user = request.user
        
        if not user.is_authenticated:
            return False
        
        # Principal has full access
        if user.role == 'PRINCIPAL':
            return True
        
        # Teacher permissions
        if user.role == 'TEACHER':
            allowed_actions = ['list', 'retrieve', 'create', 'update']
            if view.action in allowed_actions:
                return True
        
        # Student permissions
        if user.role == 'STUDENT':
            if view.action in ['list', 'retrieve']:
                return True
        
        return False