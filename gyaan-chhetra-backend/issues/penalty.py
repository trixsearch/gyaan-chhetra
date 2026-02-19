from datetime import datetime, timezone
from .constants import IssueStatus

def calculate_penalty(issue):
    if issue.get("status") == IssueStatus.RETURNED:
        return 0

    due_date = issue.get("due_date")
    if not due_date:
        return 0

    now = datetime.now(timezone.utc)

    if now > due_date:
        days_late = (now - due_date).days
        return days_late * 10  # ₹10 per day

    return 0
