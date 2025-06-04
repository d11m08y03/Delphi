from fastapi import APIRouter, HTTPException, Depends, status
from app.domain.models.user import User
from app.interfaces.dependencies import get_user_repository, get_auth_service
from app.interfaces.schemas.auth_schemas import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
)
from app.services.auth_service import AuthService
from app.domain.interfaces.user_repository import UserRepository
from app.core.security import verify_password, hash_password

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=LoginResponse)
async def register(
    user_data: RegisterRequest,
    user_repo: UserRepository = Depends(get_user_repository),
    auth_service: AuthService = Depends(get_auth_service),
):
    existing_user = await user_repo.get_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered.",
        )

    hashed_password = hash_password(user_data.password)

    new_user = User(
        id=None,
        name=user_data.name,
        email=user_data.email,
        password_hash=hashed_password,
    )

    created_user = await user_repo.create(new_user)

    if not created_user.id:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user.",
        )

    access_token = auth_service.create_access_token(
        user_id=created_user.id, expires_in=3600
    )

    return LoginResponse(access_token=access_token)


@router.post("/login", response_model=LoginResponse)
async def login(
    login_data: LoginRequest,
    user_repo: UserRepository = Depends(get_user_repository),
    auth_service: AuthService = Depends(get_auth_service),
):
    user = await user_repo.get_by_email(login_data.email)
    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    if not user.id:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user.",
        )

    access_token = auth_service.create_access_token(user_id=user.id, expires_in=3600)

    return LoginResponse(access_token=access_token)
