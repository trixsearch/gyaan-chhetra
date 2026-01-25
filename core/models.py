from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
import uuid


class BaseModel(models.Model):
    """
    Abstract base model with common fields and methods.
    Implements soft delete pattern.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    deleted_at = models.DateTimeField(null=True, blank=True, db_index=True)
    is_deleted = models.BooleanField(default=False, db_index=True)
    
    class Meta:
        abstract = True
        ordering = ['-created_at']
    
    def soft_delete(self):
        """Soft delete the instance."""
        self.deleted_at = timezone.now()
        self.is_deleted = True
        self.save(update_fields=['deleted_at', 'is_deleted', 'updated_at'])
    
    def restore(self):
        """Restore a soft-deleted instance."""
        self.deleted_at = None
        self.is_deleted = False
        self.save(update_fields=['deleted_at', 'is_deleted', 'updated_at'])
    
    def hard_delete(self):
        """Permanently delete the instance."""
        super().delete()
    
    @classmethod
    def active_objects(cls):
        """Manager for active (non-deleted) objects."""
        return cls.objects.filter(is_deleted=False)
    
    @classmethod
    def deleted_objects(cls):
        """Manager for deleted objects."""
        return cls.objects.filter(is_deleted=True)


class AuditModel(BaseModel):
    """
    Base model with audit fields for tracking changes.
    """
    created_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_created'
    )
    updated_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_updated'
    )
    
    class Meta:
        abstract = True
    
    def save(self, *args, **kwargs):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        # Get current user from thread local (set by middleware)
        user = None
        try:
            from core.middleware import get_current_user
            user = get_current_user()
        except:
            pass
        
        if not self.pk and user and not self.created_by:
            self.created_by = user
        if user and not self.updated_by:
            self.updated_by = user
        
        super().save(*args, **kwargs)