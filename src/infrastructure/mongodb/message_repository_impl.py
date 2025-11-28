from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from src.domain.entity.message import Message
from src.domain.repository.message_repository import MessageRepository
from src.domain.value_object.message_content import MessageContent
from src.domain.value_object.room_id import RoomId
from src.domain.value_object.user_id import UserId


class MessageRepositoryImpl(MessageRepository):

    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["messages"]

    async def save(self, message: Message) -> None:
        document = self._to_document(message)
        await self.collection.insert_one(document)

    async def find_by_id(self, message_id: str) -> Optional[Message]:
        document = await self.collection.find_one({"_id": message_id})
        return self._to_entity(document) if document else None

    async def find_by_room(self, room_id: int, limit: int = 50, offset: int = 0) -> List[Message]:
        cursor = self.collection.find({"room_id": room_id}).sort("seq", 1).skip(offset).limit(limit)
        documents = await cursor.to_list(length=limit)
        return [self._to_entity(doc) for doc in documents]

    async def find_last_by_room(self, room_id: int) -> Optional[Message]:
        document = await self.collection.find_one(
            {"room_id": room_id},
            sort=[("seq", -1)]
        )
        return self._to_entity(document) if document else None

    async def delete_by_id(self, message_id: str) -> bool:
        result = await self.collection.delete_one({"_id": message_id})
        return result.deleted_count > 0

    async def count_by_room(self, room_id: int) -> int:
        return await self.collection.count_documents({"room_id": room_id})

    def _to_document(self, message: Message) -> dict:
        return {
            "_id": message.id,
            "content": message.content.value,
            "room_id": message.room_id.value,
            "sender_id": message.sender_id.value,
            "created_at": message.created_at,
            "seq": message.seq
        }

    def _to_entity(self, document: dict) -> Message:
        return Message(
            id=document["_id"],
            content=MessageContent(document["content"]),
            room_id=RoomId(document["room_id"]),
            sender_id=UserId(document["sender_id"]),
            created_at=document["created_at"],
            seq=document["seq"]
        )