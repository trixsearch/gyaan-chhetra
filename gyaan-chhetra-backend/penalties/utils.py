from datetime import datetime, timezone


def calculate_penalty(due_date, return_date=None):
    today = return_date or datetime.now(timezone.utc)
    if today <= due_date:
        return 0

    days = (today - due_date).days
    return days * 1  # ₹1 per day