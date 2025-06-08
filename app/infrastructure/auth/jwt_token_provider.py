from jose import jwt
from typing import Any, Dict
from datetime import datetime, timedelta
from jose import jwt, ExpiredSignatureError, JWTError
from app.domain.interfaces.jwt_token_provider import JWTTokenProvider
from app.core.exceptions import AuthenticationError

class JoseJWTTokenProvider(JWTTokenProvider):
    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm

    def generate_token(self, data: Dict[str, Any], expires_in: int) -> str:
        expire = datetime.utcnow() + timedelta(seconds=expires_in)
        to_encode = data.copy()
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def decode_token(self, token: str) -> Dict[str, Any]:
        try:
            return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except ExpiredSignatureError:
            raise AuthenticationError("Token has expired")
        except JWTError as e:
            raise AuthenticationError(f"Invalid token: {str(e)}")
