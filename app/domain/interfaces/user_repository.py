from abc import ABC, abstractmethod
from typing import Optional
from app.domain.models.user import User

class UserRepository(ABC):
    @abstractmethod
    async def create(self, user: User) -> User:
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[User]:
        pass

    @abstractmethod
    async def update(self, user: User) -> User:
        pass
