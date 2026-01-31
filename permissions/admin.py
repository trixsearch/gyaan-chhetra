from .base import IsRole
from accounts.constants import UserRole

class IsAdmin(IsRole):
    allowed_roles=[UserRole.ADMIN]