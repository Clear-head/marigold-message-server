from typing import Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from src.domain.entity.user import User
from src.domain.repository.user_repository import UserRepository
from src.domain.value_object.user_id import UserId


class UserRepositoryImpl(UserRepository):

    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["users"]

    async def save(self, user: User) -> None:
        document = self._to_document(user)
        await self.collection.insert_one(document)

    async def find_by_id(self, user_id: str) -> Optional[User]:
        document = await self.collection.find_one({"_id": user_id})
        return self._to_entity(document) if document else None

    async def update(self, user: User) -> None:
        document = self._to_document(user)
        await self.collection.replace_one({"_id": user.id.value}, document)

    async def exists(self, user_id: str) -> bool:
        count = await self.collection.count_documents({"_id": user_id})
        return count > 0

    async def delete_by_id(self, user_id: int) -> bool:
        result = await self.collection.delete_one({"_id": user_id})
        return result.deleted_count > 0

    def _to_document(self, user: User) -> dict:
        return {
            "_id": user.id.value,
            "username": user.username,
            "created_at": user.created_at,
            "is_active": user.is_active
        }

    def _to_entity(self, document) -> User:
        return User(
            id=UserId(document["_id"]),
            username=document["username"],
            created_at=document["created_at"],
            is_active=document["is_active"]
        )