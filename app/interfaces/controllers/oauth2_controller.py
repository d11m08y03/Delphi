from fastapi import APIRouter, Depends, Query
from fastapi.responses import RedirectResponse

from app.core.config import settings
from app.core.exceptions import OAuthError
from app.domain.use_cases.oauth2_use_case import OAuth2UserUseCase
from app.infrastructure.auth.google_oauth2 import GoogleOAuth2Service
from app.interfaces.dependencies import (
    get_auth_service,
    get_google_oauth2_service,
    get_oauth2_user_use_case,
)
from app.interfaces.schemas.oauth2_schemas import OAuth2LoginResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/api/auth", tags=["google_oauth2"])


@router.get("/google-login", response_model=OAuth2LoginResponse)
async def login():
    google_auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth?"
        "scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email%20"
        "https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fdrive.readonly%20"
        "https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile&"
        "access_type=offline&"
        "response_type=code&"
        f"client_id={settings.GOOGLE_CLIENT_ID}&"
        f"redirect_uri={settings.SERVER_URL}/api/auth/google-callback"
    )

    return OAuth2LoginResponse(redirect_url=google_auth_url)


@router.get("/google-callback")
async def callback(
    code: str = Query(...),
    oauth2_use_case: OAuth2UserUseCase = Depends(get_oauth2_user_use_case),
    auth_service: AuthService = Depends(get_auth_service),
    google_oauth2_service: GoogleOAuth2Service = Depends(get_google_oauth2_service),
):
    user, tokens = await google_oauth2_service.authenticate_user(code)
    if not user or not tokens:
        raise OAuthError("Invalid OAuth2 code")

    domain_user = await oauth2_use_case.create_or_update_user(
        oauth_user=user,
        provider="google",
        account_email=user.email,
        access_token=tokens.get("access_token"),
        refresh_token=tokens.get("refresh_token"),
    )

    if domain_user.id is None:
        raise OAuthError("User ID is missing")

    access_token = auth_service.create_access_token(
        user_id=domain_user.id, expires_in=3600
    )

    frontend_redirect_url = f"{settings.FRONTEND_REDIRECT_URL}?token={access_token}"

    return RedirectResponse(url=frontend_redirect_url, status_code=302)
