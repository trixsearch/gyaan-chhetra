import uuid
from django.db import models
from django.conf import settings
from issues.models import Issue


class Penalty(models.Model):
    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("PAID", "Paid"),
        ("WAIVED", "Waived"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # 🔗 STRONG RELATION TO ISSUE
    issue = models.OneToOneField(
        Issue,
        on_delete=models.CASCADE,
        related_name="penalty"
    )

    amount = models.DecimalField(max_digits=8, decimal_places=2)

    reason = models.TextField(blank=True)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="penalties_created"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"₹{self.amount} – {self.issue.borrower.email}"
