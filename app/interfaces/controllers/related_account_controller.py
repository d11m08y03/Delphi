from fastapi import APIRouter, Depends, HTTPException, status
from app.domain.use_cases.oauth2_use_case import OAuth2UserUseCase
from app.infrastructure.auth.google_oauth2 import GoogleOAuth2Service
from app.interfaces.dependencies import (
    get_oauth2_user_use_case,
    get_google_oauth2_service,
)
from app.interfaces.schemas.related_account_schemas import (
    RelatedAccountRequest,
    RelatedAccountResponse,
)

router = APIRouter()


@router.post("/related-accounts/google")
async def add_google_related_account(
    request: RelatedAccountRequest,
    oauth2_usecase: OAuth2UserUseCase = Depends(get_oauth2_user_use_case),
    google_service: GoogleOAuth2Service = Depends(get_google_oauth2_service),
):
    try:
        user, tokens = await google_service.authenticate_user(request.code)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Google OAuth failed: {str(e)}",
        )

    await oauth2_usecase.add_related_account(
        user_id=request.user_id,
        provider="google",
        account_email=user.email,
        access_token=tokens.get("access_token", ""),
        refresh_token=tokens.get("refresh_token"),
    )

    return RelatedAccountResponse(
        success=True, message="Related account added successfully"
    )
