from typing import Optional, Sequence, Annotated
from fastapi import Security, HTTPException, status

from src.auth.service import Auth
from src.user.schemas import UserInDb


class UserWithRole:
    auth = Auth()

    def __init__(self, roles: Optional[Sequence[str]]):
        self.roles = roles or []

    def __call__(
        self,
        user: Annotated[UserInDb, Security(auth.get_current_user, scopes=["read"])],
    ) -> UserInDb:
        if not self.roles:
            return user
        if user.role not in self.roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient access rights",
            )

        return user
