"""
Serializers for authentication app.
"""
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    
    class Meta:
        model = User
        fields = [
            'uuid',
            'email',
            'first_name',
            'last_name',
            'role',
            'phone_number',
            'address',
            'date_joined',
            'last_login'
        ]
        read_only_fields = ['uuid', 'date_joined', 'last_login']


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    
    password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=8,
        style={'input_type': 'password'}
    )
    confirm_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name',
            'password',
            'confirm_password',
            'phone_number',
            'address'
        ]
    
    def validate(self, attrs):
        """Validate registration data."""
        if attrs['password'] != attrs.pop('confirm_password'):
            raise serializers.ValidationError({
                'password': 'Passwords do not match.'
            })
        
        # Check if email already exists
        if User.objects.filter(email=attrs['email'].lower()).exists():
            raise serializers.ValidationError({
                'email': 'User with this email already exists.'
            })
        
        return attrs
    
    def create(self, validated_data):
        """Create a new user."""
        # All new registrations are borrowers by default
        validated_data['role'] = 'borrower'
        
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data.get('phone_number'),
            address=validated_data.get('address')
        )
        
        return user


class AdminCreateUserSerializer(serializers.ModelSerializer):
    """Serializer for admin creating users (admin or borrower)."""
    
    password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=8,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name',
            'password',
            'role',
            'phone_number',
            'address'
        ]
    
    def validate(self, attrs):
        """Validate admin user creation."""
        # Check if email already exists
        if User.objects.filter(email=attrs['email'].lower()).exists():
            raise serializers.ValidationError({
                'email': 'User with this email already exists.'
            })
        
        # Ensure role is either admin or borrower
        if attrs['role'] not in ['admin', 'borrower']:
            raise serializers.ValidationError({
                'role': 'Role must be either "admin" or "borrower".'
            })
        
        return attrs
    
    def create(self, validated_data):
        """Create a new user."""
        password = validated_data.pop('password')
        
        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            role=validated_data['role'],
            phone_number=validated_data.get('phone_number'),
            address=validated_data.get('address')
        )
        
        user.set_password(password)
        user.save()
        
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer for user login."""
    
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        required=True,
        style={'input_type': 'password'},
        trim_whitespace=False
    )
    
    def validate(self, attrs):
        """Validate login credentials."""
        email = attrs.get('email').lower()
        password = attrs.get('password')
        
        # Authenticate user
        user = authenticate(
            request=self.context.get('request'),
            email=email,
            password=password
        )
        
        if not user:
            msg = _('Unable to log in with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')
        
        if not user.is_active:
            msg = _('User account is disabled.')
            raise serializers.ValidationError(msg, code='authorization')
        
        attrs['user'] = user
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for changing password."""
    
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(
        required=True,
        min_length=8
    )
    confirm_password = serializers.CharField(required=True)
    
    def validate(self, attrs):
        """Validate password change."""
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({
                'new_password': 'Passwords do not match.'
            })
        
        return attrs


class UpdateProfileSerializer(serializers.ModelSerializer):
    """Serializer for updating user profile."""
    
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'phone_number',
            'address'
        ]