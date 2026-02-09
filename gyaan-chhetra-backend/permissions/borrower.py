from .base import IsRole
from accounts.constants import UserRole


class IsBorrower(IsRole):
    allowed_roles = [UserRole.BORROWER]
