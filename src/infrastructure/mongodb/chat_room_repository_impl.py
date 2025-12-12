from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from src.domain.entity.chat_room import ChatRoom
from src.domain.repository.chat_room_repository import ChatRoomRepository
from src.domain.value_object.room_id import RoomId
from src.domain.value_object.user_id import UserId


class ChatRoomRepositoryImpl(ChatRoomRepository):

    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["chat_rooms"]

    async def save(self, room: ChatRoom) -> None:
        document = self._to_document(room)
        await self.collection.insert_one(document)

    async def find_by_id(self, room_id: int) -> Optional[ChatRoom]:
        document = await self.collection.find_one({"_id": room_id})
        return self._to_entity(document) if document else None

    async def find_by_participant(self, user_id: str) -> List[ChatRoom]:
        cursor = self.collection.find({"participant_ids": user_id})
        documents = await cursor.to_list(length=None)
        return [self._to_entity(doc) for doc in documents]

    async def update(self, room: ChatRoom) -> None:
        document = self._to_document(room)
        await self.collection.replace_one({"_id": room.id.value}, document)

    async def delete_by_id(self, room_id: int) -> bool:
        result = await self.collection.delete_one({"_id": room_id})
        return result.deleted_count > 0

    async def exists(self, room_id: int) -> bool:
        count = await self.collection.count_documents({"_id": room_id})
        return count > 0

    def _to_document(self, room: ChatRoom) -> dict:
        return {
            "_id": room.id.value,
            "name": room.name,
            "creator_id": room.creator_id.value,
            "participant_ids": room.participant_ids,
            "created_at": room.created_at
        }

    def _to_entity(self, document: dict) -> ChatRoom:
        return ChatRoom(
            id=RoomId(document["_id"]),
            name=document["name"],
            creator_id=UserId(document["creator_id"]),
            participant_ids=document["participant_ids"],
            created_at=document["created_at"]
        )