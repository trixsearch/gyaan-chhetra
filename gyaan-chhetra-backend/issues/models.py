import uuid
from django.db import models
from accounts.models import User
from books.models import Book


class Issue(models.Model):
    """
    Book issue lifecycle:
    ISSUED → RETURNED → (optional) PENALIZED
    """
    STATUS_CHOICES = (
        ("ISSUED", "Issued"),
        ("RETURNED", "Returned"),
        ("OVERDUE", "Overdue"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    borrower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="issues"
    )

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="issues"
    )

    issued_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    returned_at = models.DateTimeField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="ISSUED"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-issued_at"]

    def __str__(self):
        return f"{self.book.title} → {self.borrower.email}"
