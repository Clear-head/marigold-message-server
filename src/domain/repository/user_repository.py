from abc import ABC, abstractmethod
from typing import Optional
from src.domain.entity.user import User


class UserRepository(ABC):

    @abstractmethod
    async def save(self, user: User) -> None:
        pass

    @abstractmethod
    async def find_by_id(self, user_id: str) -> Optional[User]:
        pass

    @abstractmethod
    async def update(self, user: User) -> None:
        pass

    @abstractmethod
    async def delete_by_id(self, user: User) -> None:
        pass

    @abstractmethod
    async def exists(self, user_id: str) -> bool:
        pass