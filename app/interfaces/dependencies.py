from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from app.domain.interfaces.related_account_repository import RelatedAccountRepository
from app.domain.use_cases.oauth2_use_case import OAuth2UserUseCase
from app.domain.interfaces.user_repository import UserRepository
from app.domain.use_cases.user_use_case import UserUseCase
from app.infrastructure.auth.google_oauth2 import GoogleOAuth2Service
from app.infrastructure.db.dependencies import get_user_repository
from app.infrastructure.db.dependencies import get_related_account_repository
from app.services.auth_service import AuthService
from app.core.config import settings
from app.core.exceptions import AuthenticationError


def get_oauth2_user_use_case(
    user_repo: UserRepository = Depends(get_user_repository),
    related_account_repo: RelatedAccountRepository = Depends(
        get_related_account_repository
    ),
) -> OAuth2UserUseCase:
    return OAuth2UserUseCase(user_repo, related_account_repo)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_auth_service() -> AuthService:
    from app.infrastructure.auth.jwt_token_provider import JoseJWTTokenProvider

    token_provider = JoseJWTTokenProvider(
        settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM
    )
    return AuthService(token_provider)

def get_google_oauth2_service() -> GoogleOAuth2Service:
    return GoogleOAuth2Service();


def get_current_user_id(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service),
) -> int:
    try:
        return auth_service.validate_access_token(token)
    except JWTError as e:
        raise AuthenticationError("Invalid or expired token") from e


def get_user_use_case(
    auth_service: AuthService = Depends(get_auth_service),
    user_repo: UserRepository = Depends(get_user_repository),
) -> UserUseCase:
    return UserUseCase(auth_service, user_repo)
