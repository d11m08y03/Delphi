from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from app.domain.use_cases.oauth2_use_case import OAuth2UserUseCase
from app.domain.interfaces.user_repository import UserRepository
from app.infrastructure.db.dependencies import get_user_repository
from app.services.auth_service import AuthService
from app.core.config import settings
from app.core.exceptions import AuthenticationError


def get_oauth2_user_use_case(
    user_repo: UserRepository = Depends(get_user_repository),
) -> OAuth2UserUseCase:
    return OAuth2UserUseCase(user_repo)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_auth_service() -> AuthService:
    from app.infrastructure.auth.jwt_token_provider import JoseJWTTokenProvider

    token_provider = JoseJWTTokenProvider(
        settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM
    )
    return AuthService(token_provider)


def get_current_user_id(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service),
) -> int:
    try:
        return auth_service.validate_access_token(token)
    except JWTError as e:
        # Raise your custom AuthenticationError here
        raise AuthenticationError("Invalid or expired token") from e
