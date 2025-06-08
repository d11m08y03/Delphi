from app.core.exceptions import AppError, AuthorizationError
from app.core.security import hash_password, verify_password
from app.domain.interfaces.user_repository import UserRepository
from app.domain.models.user import User
from app.services.auth_service import AuthService


class AuthUseCase:
    def __init__(self, user_repo: UserRepository, auth_service: AuthService):
        self.user_repo = user_repo
        self.auth_service = auth_service

    async def login(self, email: str, password: str) -> str:
        user = await self.user_repo.get_by_email(email)

        if not user or not verify_password(password, user.password_hash):
            raise AuthorizationError("Invalid email or password.")

        if not user.id:
            raise AppError("Could not find user id")

        return self.auth_service.create_access_token(user_id=user.id, expires_in=3600)

    async def register(self, name: str, email: str, password: str) -> str:
        existing_user = await self.user_repo.get_by_email(email)
        if existing_user:
            raise AppError("Email is already registered.")

        hashed_password = hash_password(password)

        new_user = User(id=None, name=name, email=email, password_hash=hashed_password)

        created_user = await self.user_repo.create(new_user)

        if not created_user.id:
            raise Exception("Failed to create user.")

        return self.auth_service.create_access_token(
            user_id=created_user.id, expires_in=3600
        )
