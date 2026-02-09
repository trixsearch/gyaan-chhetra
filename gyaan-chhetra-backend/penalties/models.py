import uuid
from django.db import models
from django.conf import settings


class Penalty(models.Model):
    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("PAID", "Paid"),
        ("WAIVED", "Waived"),
    )

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    borrower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="penalties"
    )

    issue_uuid = models.UUIDField()

    amount = models.DecimalField(max_digits=8, decimal_places=2)

    reason = models.TextField()

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.UUIDField()  # admin UUID

    def __str__(self):
        return f"{self.borrower.email} – ₹{self.amount} ({self.status})"
