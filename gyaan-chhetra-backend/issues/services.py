from django.utils.timezone import now
from penalties.models import Penalty

FINE_PER_DAY = 10  # ₹10 per day


def return_issue(issue, admin_user):
    issue.status = "RETURNED"
    issue.returned_at = now()
    issue.save()

    if issue.returned_at > issue.due_date:
        days = (issue.returned_at - issue.due_date).days

        Penalty.objects.create(
            issue=issue,
            amount=days * FINE_PER_DAY,
            reason=f"Late return by {days} days",
            created_by=admin_user
        )
