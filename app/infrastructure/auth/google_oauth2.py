import httpx
from app.domain.interfaces.oauth2_service import OAuth2Service
from app.domain.models.user import User
from app.core.config import settings
from app.core.exceptions import (
    InvalidTokenError,
    ProviderCommunicationError,
    MissingUserDataError,
)


class GoogleOAuth2Service(OAuth2Service):
    TOKEN_URL = "https://oauth2.googleapis.com/token"
    USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"

    async def authenticate_user(self, authorization_code: str) -> tuple[User, dict]:
        try:
            tokens = await self._exchange_code_for_tokens(authorization_code)

            userinfo = await self._get_user_info(tokens["access_token"])

            return self._create_user_from_info(userinfo), tokens

        except httpx.HTTPStatusError as e:
            raise ProviderCommunicationError(
                f"Google API returned error: {e.response.text}", original_error=e
            )
        except httpx.RequestError as e:
            raise ProviderCommunicationError(
                "Failed to communicate with Google OAuth service", original_error=e
            )

    async def _exchange_code_for_tokens(self, code: str) -> dict:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.TOKEN_URL,
                    data={
                        "client_id": settings.GOOGLE_CLIENT_ID,
                        "client_secret": settings.GOOGLE_CLIENT_SECRET,
                        "code": code,
                        "grant_type": "authorization_code",
                        "redirect_uri": settings.SERVER_URL
                        + "/api/auth/google-callback",
                    },
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                )
                response.raise_for_status()
                tokens = response.json()

                if not tokens.get("access_token"):
                    raise InvalidTokenError("No access token in response")

                return tokens

        except httpx.HTTPStatusError as e:
            raise ProviderCommunicationError(
                f"Token exchange failed: {e.response.text}", original_error=e
            )

    async def _get_user_info(self, access_token: str) -> dict:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    self.USERINFO_URL,
                    headers={"Authorization": f"Bearer {access_token}"},
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            raise ProviderCommunicationError(
                f"Failed to fetch user info: {e.response.text}", original_error=e
            )

    def _create_user_from_info(self, userinfo: dict) -> User:
        if not userinfo.get("email"):
            raise MissingUserDataError("Email is required but missing from user info")

        return User(
            id=None,
            name=userinfo.get("name", ""),
            email=userinfo["email"],
            password_hash="",
        )
