from fastapi import APIRouter, HTTPException, status, Query, Depends
from app.infrastructure.auth.google_oauth2 import GoogleOAuth2Service
from app.core.config import settings
from app.infrastructure.db.sqlalchemy_user_repository import SQLAlchemyUserRepository
from app.domain.use_cases.oauth2_use_case import OAuth2UserUseCase
from app.infrastructure.db.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/auth/google", tags=["google_oauth2"])
oauth2_service = GoogleOAuth2Service()

async def get_oauth2_use_case(session: AsyncSession = Depends(get_session)) -> OAuth2UserUseCase:
    user_repo = SQLAlchemyUserRepository(session) 
    return OAuth2UserUseCase(user_repo)

@router.get("/login")
async def login():
    redirect_uri = settings.FRONTEND_REDIRECT_URL
    google_auth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={settings.GOOGLE_CLIENT_ID}"
        f"&redirect_uri={redirect_uri}"
        f"&response_type=code"
        f"&scope=openid email profile"
    )
    return {"auth_url": google_auth_url}


@router.get("/callback")
async def callback(
    code: str = Query(...),
    oauth2_use_case: OAuth2UserUseCase = Depends(get_oauth2_use_case)
):
    user = await oauth2_service.authenticate_user(code)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid OAuth2 code")

    user = await oauth2_use_case.create_or_update_user(user)

    return {"message": "User authenticated", "user": user}
