from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.models.related_account import RelatedAccount


class RelatedAccountRepository(ABC):
    @abstractmethod
    async def create(self, related_account: RelatedAccount) -> RelatedAccount:
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[RelatedAccount]:
        pass

    @abstractmethod
    async def get_by_user_id(self, user_id: int) -> List[RelatedAccount]:
        pass

    @abstractmethod
    async def get_by_user_id_and_provider(
        self, user_id: int, provider: str
    ) -> Optional[RelatedAccount]:
        pass

    @abstractmethod
    async def update(self, related_account: RelatedAccount) -> RelatedAccount:
        pass

    @abstractmethod
    async def delete(self, id: int) -> None:
        pass
