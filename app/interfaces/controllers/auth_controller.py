from fastapi import APIRouter, HTTPException, Depends, status
from app.interfaces.dependencies import get_user_repository, get_auth_service
from app.interfaces.schemas.auth_schemas import (
    RegisterRequest,
    LoginRequest,
    LoginResponse,
)
from app.domain.use_cases.auth_use_case import AuthUseCase

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=LoginResponse)
async def register(
    user_data: RegisterRequest,
    user_repo=Depends(get_user_repository),
    auth_service=Depends(get_auth_service),
):
    use_case = AuthUseCase(user_repo, auth_service)
    try:
        access_token = await use_case.register(
            name=user_data.name, email=user_data.email, password=user_data.password
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )

    return LoginResponse(token=access_token)


@router.post("/login", response_model=LoginResponse)
async def login(
    login_data: LoginRequest,
    user_repo=Depends(get_user_repository),
    auth_service=Depends(get_auth_service),
):
    use_case = AuthUseCase(user_repo, auth_service)
    try:
        access_token = await use_case.login(
            email=login_data.email, password=login_data.password
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )

    return LoginResponse(token=access_token)
