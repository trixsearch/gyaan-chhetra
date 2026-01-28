# user.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class Role(models.TextChoices):
    STUDENT = 'STUDENT', 'Student'
    TEACHER = 'TEACHER', 'Teacher'
    PRINCIPAL = 'PRINCIPAL', 'Principal'

class CustomUser(AbstractUser):
    role = models.CharField(max_length=20, choices=Role.choices)
    mobile_number = models.CharField(max_length=15, unique=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['role', 'is_active']),
            models.Index(fields=['mobile_number']),
        ]
