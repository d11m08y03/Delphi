import httpx
from typing import Optional
from app.domain.interfaces.oauth2_service import OAuth2Service
from app.domain.models.user import User
from app.core.config import settings

class GoogleOAuth2Service(OAuth2Service):
    TOKEN_URL = "https://oauth2.googleapis.com/token"
    USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"

    async def authenticate_user(self, authorization_code: str) -> Optional[User]:
        async with httpx.AsyncClient() as client:
            token_resp = await client.post(
                self.TOKEN_URL,
                data={
                    "client_id": settings.GOOGLE_CLIENT_ID,
                    "client_secret": settings.GOOGLE_CLIENT_SECRET,
                    "code": authorization_code,
                    "grant_type": "authorization_code",
                    "redirect_uri": settings.FRONTEND_REDIRECT_URL,
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
            token_resp.raise_for_status()
            tokens = token_resp.json()
            access_token = tokens.get("access_token")

            if not access_token:
                return None

            userinfo_resp = await client.get(
                self.USERINFO_URL,
                headers={"Authorization": f"Bearer {access_token}"},
            )
            userinfo_resp.raise_for_status()
            userinfo = userinfo_resp.json()

            return User(
                id=None,  
                name=userinfo.get("name"),
                email=userinfo.get("email"),
                password_hash="",  # no password since OAuth2 user
            )
