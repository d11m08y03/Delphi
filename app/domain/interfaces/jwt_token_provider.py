from abc import ABC, abstractmethod
from typing import Any, Dict


class JWTTokenProvider(ABC):
    @abstractmethod
    def generate_token(self, data: Dict[str, Any], expires_in: int) -> str:
        pass

    @abstractmethod
    def decode_token(self, token: str) -> Dict[str, Any]:
        pass
