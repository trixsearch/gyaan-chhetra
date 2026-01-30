"""
Custom User model with UUID as primary key.
"""
import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import EmailValidator
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)


class UserManager(BaseUserManager):
    """
    Custom manager for User model.
    """
    
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a regular user with an email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        
        logger.info(f"User created: {email}")
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with admin permissions.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 'admin')
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model using UUID as primary key.
    """
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('borrower', 'Borrower'),
    ]
    
    # UUID as primary key
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    
    # Required fields
    email = models.EmailField(
        max_length=255,
        unique=True,
        validators=[EmailValidator()],
        verbose_name='Email Address'
    )
    
    # Personal information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    
    # Role-based field
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='borrower'
    )
    
    # Status fields
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    # Timestamps
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True, blank=True)
    
    # Additional borrower information
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    # Django auth fields
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['role']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return self.email
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def is_admin(self):
        return self.role == 'admin'
    
    @property
    def is_borrower(self):
        return self.role == 'borrower'
    
    def get_short_name(self):
        return self.first_name
    
    def save(self, *args, **kwargs):
        # Ensure email is lowercase
        self.email = self.email.lower()
        
        # If user is admin, ensure staff permissions
        if self.role == 'admin':
            self.is_staff = True
        
        super().save(*args, **kwargs)
        
        logger.info(f"User saved: {self.email} (Role: {self.role})")