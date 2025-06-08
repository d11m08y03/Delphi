from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.domain.use_cases.user_use_case import UserUseCase
from app.interfaces.dependencies import get_user_use_case
from app.interfaces.schemas.user_schemas import UserDetailsSchema

router = APIRouter(prefix="/api/user", tags=["User"])
security = HTTPBearer()


@router.get("/info", response_model=UserDetailsSchema)
async def trust(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    user_use_case: UserUseCase = Depends(get_user_use_case),
):
    try:
        token = credentials.credentials

        if not (user := await user_use_case.get_by_id(token)):
            raise ValueError("User not found")

        return UserDetailsSchema(
            email=user.email, first_name=user.name, last_name=user.name
        )

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token"
        )
