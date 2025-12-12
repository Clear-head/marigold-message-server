from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entity.chat_room import ChatRoom


class ChatRoomRepository(ABC):

    @abstractmethod
    async def save(self, room: ChatRoom) -> None:
        pass

    @abstractmethod
    async def find_by_id(self, room_id: int) -> Optional[ChatRoom]:
        pass

    @abstractmethod
    async def find_by_participant(self, user_id: str) -> List[ChatRoom]:
        pass

    @abstractmethod
    async def update(self, room: ChatRoom) -> None:
        pass

    @abstractmethod
    async def delete_by_id(self, room_id: int) -> bool:
        pass

    @abstractmethod
    async def exists(self, room_id: int) -> bool:
        pass