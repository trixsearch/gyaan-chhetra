from datetime import datetime, timezone


def calculate_penalty(issue):
    """
    Penalty = ₹1 per day after due_date
    """
    due_date = issue.get("due_date")
    return_date = issue.get("return_date")

    if not due_date:
        return 0

    end_date = return_date or datetime.now(timezone.utc)

    if end_date <= due_date:
        return 0

    days_late = (end_date.date() - due_date.date()).days
    return days_late
