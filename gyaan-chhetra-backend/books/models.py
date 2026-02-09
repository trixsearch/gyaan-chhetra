import uuid
from django.db import models
from accounts.models import User


class Book(models.Model):
    """
    Master Book table
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    title = models.CharField(max_length=255)
    writer = models.CharField(max_length=255)

    genre = models.JSONField(
        default=list,
        blank=True,
        help_text="List of genres"
    )

    quantity = models.PositiveIntegerField()
    available_quantity = models.PositiveIntegerField()

    created_by = models.ForeignKey(
        User,
        related_name="books_created",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    updated_by = models.ForeignKey(
        User,
        related_name="books_updated",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["writer"]),
        ]

    def __str__(self):
        return f"{self.title} - {self.writer}"
