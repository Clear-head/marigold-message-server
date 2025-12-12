from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entity.message import Message


class MessageRepository(ABC):

    @abstractmethod
    async def save(self, message: Message) -> None:
        pass

    @abstractmethod
    async def find_by_id(self, message_id: str) -> Optional[Message]:
        pass

    @abstractmethod
    async def find_by_room(self, room_id: int, limit: int = 50, offset: int = 0) -> List[Message]:
        pass

    @abstractmethod
    async def find_last_by_room(self, room_id: int) -> Optional[Message]:
        pass

    @abstractmethod
    async def delete_by_id(self, message_id: str) -> bool:
        pass

    @abstractmethod
    async def count_by_room(self, room_id: int) -> int:
        pass