from app.domain.interfaces.jwt_token_provider import JWTTokenProvider


class AuthService:
    def __init__(self, token_provider: JWTTokenProvider):
        self.token_provider = token_provider

    def create_access_token(self, user_id: int, expires_in: int = 3600) -> str:
        payload = {"user_id": user_id}
        return self.token_provider.generate_token(payload, expires_in)

    def validate_access_token(self, token: str) -> int:
        payload = self.token_provider.decode_token(token)
        return payload["user_id"]
