import uuid
from datetime import datetime, timezone


def utc_now():
    return datetime.now(timezone.utc)


def create_audit_fields(user_uuid: str) -> dict:
    """
    Fields to be added ONLY at document creation time.
    These fields MUST NEVER change.
    """
    return {
        "uuid": str(uuid.uuid4()),
        "created_at": utc_now(),
        "updated_at": utc_now(),
        "created_by": user_uuid,
        "updated_by": user_uuid,
    }


def update_audit_fields(user_uuid: str) -> dict:
    """
    Fields to be updated on EVERY document update.
    """
    return {
        "updated_at": utc_now(),
        "updated_by": user_uuid,
    }
