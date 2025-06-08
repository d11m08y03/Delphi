from abc import ABC, abstractmethod
from typing import Optional
from app.domain.models.user import User

class OAuth2Service(ABC):
    @abstractmethod
    async def authenticate_user(self, authorization_code: str) -> tuple[Optional[User], dict]:
        pass
