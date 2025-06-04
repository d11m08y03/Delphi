from app.services.auth_service import AuthService
from app.domain.interfaces.user_repository import UserRepository
from app.domain.models.user import User
from typing import Optional


class UserUseCase:
    def __init__(self, auth_service: AuthService, user_repo: UserRepository):
        self.jwt_service = auth_service
        self.user_repo = user_repo

    async def get_by_id(self, token: str) -> Optional[User]:
        user_id = self.jwt_service.validate_access_token(token)
        if not user_id:
            raise ValueError("Invalid token")

        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        return user
